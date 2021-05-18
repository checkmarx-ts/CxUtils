[CmdletBinding()]
Param(

    [Parameter(Mandatory=$False)]
    [switch]
    $v,

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String]
    $configFile = "",

    [Parameter(Mandatory = $False)]
    [String]
    $serviceUrl,

    [Parameter(Mandatory = $False)]
    [String]
    $username,

    [Parameter(Mandatory = $False)]
    [String]
    $pass,

    [Parameter(Mandatory = $True, ParameterSetName = "DatesRange")]
    [Parameter(Mandatory = $True, ParameterSetName = "RollingDate")]
    [Parameter(Mandatory = $True, ParameterSetName = "NumOfScans")]
    [switch]
    $StartRetention,    

    [Parameter(Mandatory = $True, ParameterSetName = "NumOfScans")]
    [switch]
    $ByNumOfScans,

    [Parameter(Mandatory = $True, ParameterSetName = "NumOfScans")]
    [Int]
    $numOfScansToKeep,

    [Parameter(Mandatory = $True, ParameterSetName = "DatesRange")]
    [switch]
    $ByDateRange,

    [Parameter(Mandatory = $False, ParameterSetName = "DatesRange")]
    [Datetime]
    $startDate,

    [Parameter(Mandatory = $True, ParameterSetName = "DatesRange")]
    [Datetime]
    $endDate,

    [Parameter(Mandatory = $True, ParameterSetName = "RollingDate")]
    [switch]
    $ByRollingDate,

    [Parameter(Mandatory = $True, ParameterSetName = "RollingDate")]
    [int]
    $rollingDateRange,

    [Parameter(Mandatory = $False, ParameterSetName = "DatesRange")]
    [Parameter(Mandatory = $False, ParameterSetName = "NumOfScans")]
    [int]
    $retentionDurationLimit,

    [Parameter(Mandatory = $True, ParameterSetName = "stop")]
    [switch]
    $StopRetention
)

# CxSAST REST API auth values
[String] $CX_REST_GRANT_TYPE = "password"
[String] $CX_REST_SCOPE = "sast_rest_api"
[String] $CX_REST_CLIENT_ID = "resource_owner_client"
# Constant shared secret between this client and the Checkmarx server.
[String] $CX_REST_CLIENT_SECRET = "014DF517-39D1-4453-B7B3-9930C563627C"


# -----------------------------------------------------------------
# Reads config from JSON file
# -----------------------------------------------------------------
Class Config {

    hidden $config
    hidden [IO] $io
    [String] $configFile

    # Constructs and loads configuration from given path
    Config ([String] $configFile) {
        $this.io = [IO]::new()
        $this.configFile = $configFile
        $this.LoadConfig()
    }

    # Loads configuration from configured path
    LoadConfig () {
        try {
            $cp = $this.configFile
            $configFilePath = (Get-Item -Path $cp).FullName
            $this.io.Log("Loading config from $configFilePath")
            $this.config = Get-Content -Path $configFilePath -Raw | ConvertFrom-Json
        }
        catch {
            $this.io.Log("Provided configuration file at [" + $this.configFile + "] is missing / corrupt.")
            exit -1
        }
    }

    [PsCustomObject] GetConfig() {
        return $this.config
    }
}

# -----------------------------------------------------------------
# DateTime Utility
# -----------------------------------------------------------------
Class DateTimeUtil {

    # Gets timestamp in UTC in configured format
    [String] NowUTCFormatted() {
        return $this.Format($this.NowUTC())
    }

    # Gets timestamp in UTC
    [DateTime] NowUTC() {
        return (Get-Date).ToUniversalTime()
    }

    # Converts to UTC and formats
    [String] ToUTCAndFormat([DateTime] $dateTime) {
        return $this.Format($dateTime.ToUniversalTime())
    }

    # Formats time based on configured format
    [String] Format([DateTime] $dateTime) {
        return $dateTime.ToString($script:config.log.timeFormat)
    }

}

# -----------------------------------------------------------------
# Input/Output Utility
# -----------------------------------------------------------------
Class IO {

    # General logging
    hidden [String] $LOG_FOLDER = "."
    static [String] $LOG_FILE = "cx_data_retention.log"
    hidden [DateTimeUtil] $dateUtil = [DateTimeUtil]::new()

    IO () {
        if ($script:logFolder) {
            $this.LOG_FOLDER = $script:logFolder
        }
    }

    # Logs given message to configured log file
    Log ([String] $message) {
        # Write to log file
        $this.WriteToFile($message, [IO]::LOG_FILE)
        # Also write to console
        $this.Console($message)
    }

    # Write given string to host console
    Console ([String] $message) {
        Write-Host $this.AddTimestamp($message)
    }

    # Write a pretty header output
    WriteHeader() {
        $this.Log("------------------------------------------------------------------------")
        $this.Log("Checkmarx Data Retention")
        $this.Log("Checkmarx Manager: $($script:config.cx.host)")
        $this.Log("Logs: $($this.LOG_FOLDER)")
        $this.Log("Data Retention Duration Limit (hours): $($script:config.dataRetention.durationLimitHours)")
        $this.Log("------------------------------------------------------------------------")
    }

    # Utility that writes to given file
    hidden WriteToFile([String] $message, [String] $file) {
        $filePath = Join-Path -Path $this.LOG_FOLDER -ChildPath $file
        Add-content $filePath -Value $this.AddTimestamp($message)
    }

    hidden [String] AddTimestamp ([String] $message) {
        return $this.dateUtil.NowUTCFormatted() + ": " + $message
    }
}



# -----------------------------------------------------------------
# REST request body
# -----------------------------------------------------------------
Class RESTBody {

    [String] $grantType
    [String] $scope
    [String] $clientId
    [String] $clientSecret

    RESTBody(
        [String] $grantType,
        [String] $scope,
        [String] $clientId,
        [String] $clientSecret
    ) {
        $this.grantType = $grantType
        $this.scope = $scope
        $this.clientId = $clientId
        $this.clientSecret = $clientSecret
    }
}



# -----------------------------------------------------------------
# REST Client
# -----------------------------------------------------------------
Class RESTClient {

    [String] $baseUrl
    [RESTBody] $restBody

    hidden [String] $token
    hidden [IO] $io = [IO]::new()

    # Constructs a RESTClient based on given base URL and body
    RESTClient ([String] $cxHost, [RESTBody] $restBody) {
        $this.baseUrl = $cxHost + "/cxrestapi"
        $this.restBody = $restBody
    }

    <#
    # Logins to the CxSAST REST API
    # and returns an API token
    #>
    [bool] login ([String] $username, [String] $password) {
        [bool] $isLoginSuccessful = $False
        $body = @{
            username      = $username
            password      = $password
            grant_type    = $this.restBody.grantType
            scope         = $this.restBody.scope
            client_id     = $this.restBody.clientId
            client_secret = $this.restBody.clientSecret
        }

        [psobject] $response = $null
        try {
            $loginUrl = $this.baseUrl + "/auth/identity/connect/token"
            if ($script:v) {
              $this.io.Log("Logging into Checkmarx CxSAST...")
            }
            $response = Invoke-RestMethod -uri $loginUrl -method POST -body $body -contenttype 'application/x-www-form-urlencoded'
        }
        catch {
            if ($script:v) {
              $this.io.Log("$_")
            }
            $this.io.Log("Could not authenticate against Checkmarx REST API. Reason: HTTP [$($_.Exception.Response.StatusCode.value__)] - $($_.Exception.Response.StatusDescription).")
        }

        if ($response -and $response.access_token) {
            $isLoginSuccessful = $True
            # Track token internally
            $this.token = $response.token_type + " " + $response.access_token
        }


        return $isLoginSuccessful
    }

    <#
    # Invokes a given REST API
    #>
    [Object] invokeAPI ([String] $requestUri, [String] $method, [Object] $body, [int] $apiResponseTimeoutSeconds) {

        # Sanity : If not logged in, do not proceed
        if ( ! $this.token) {
            throw "Must execute login() first, prior to other API calls."
        }

        $headers = @{
            "Authorization" = $this.token
            "Accept"        = "application/json;v=1.0"
        }

        $response = $null

        try {
            $uri = $this.baseUrl + $requestUri
            if ($method -ieq "GET") {
                $response = Invoke-RestMethod -Uri $uri -Method $method -Headers $headers -TimeoutSec $apiResponseTimeoutSeconds
            }
            else {
                $response = Invoke-RestMethod -Uri $uri -Method $method -Headers $headers -Body $body -TimeoutSec $apiResponseTimeoutSeconds
            }
        }
        catch {
            $this.io.Log("REST API call failed : [$($_.exception.Message)]")
            $this.io.Log("Status Code: $($_.exception.Response.StatusCode)")
            $this.io.Log("$_")
        }

        return $response
    }
}



# -----------------------------------------------------------------
# Data Retention Execution
# -----------------------------------------------------------------
Class DataRetention {

    hidden [IO] $io
    hidden [PSObject] $config
    hidden [RESTClient] $cxSastRestClient

    DataRetention([PSObject] $config) {
        $this.io = [IO]::new()
        $this.config = $config
    }

    # Executes data retention
    Execute() {

        # Create a RESTBody specific to CxSAST REST API calls
        $cxSastRestBody = [RESTBody]::new($script:CX_REST_GRANT_TYPE, $script:CX_REST_SCOPE, $script:CX_REST_CLIENT_ID, $script:CX_REST_CLIENT_SECRET)
        # Create a REST Client for CxSAST REST API
        $this.cxSastRestClient = [RESTClient]::new($this.config.cx.host, $cxSastRestBody)

        # Login to the CxSAST server
        [bool] $isLoginOk = $this.cxSastRestClient.login($this.config.cx.username, $this.config.cx.password)

        if ($isLoginOk -eq $True) {
            if ($script:v) {
                $this.io.Log("Login was successful.")
            }

            # Modes of running DR:
            # - KEEP X number of scans for each project
            # - DELETE scans that match given date range
            #     - Explicit date range
            #         - If start date is missing, go back sufficient number of years (Ex.1900 is a safe starting point)
            #     - Rolling : delete scans that occurred prior to given number of days
            #         - Start date is set back a sufficient number of years (Ex.1900 is a safe starting point)
            if ($script:ByNumOfScans) {
                $this.io.Log("Running data retention by number of scans.")
                $this.ExecByNumOfScans($script:numOfScansToKeep, $this.config.dataRetention.durationLimitHours)
            }
            elseif ($script:ByDateRange) {
                #     - Explicit date range
                #         - If start date is missing, go back sufficient number of years (Ex.1900 is a safe starting point)
                if (!$script:startDate) {
                    $script:startDate = (Get-Date "1900-01-01")
                }
                $this.io.Log("Running data retention by date range.")
                $this.ExecByDateRange($script:startDate, $script:endDate, $this.config.dataRetention.durationLimitHours)
            }
            elseif ($script:ByRollingDate) {
                #     - Rolling : delete scans that occurred prior to given number of days
                #         - Start date is set back a sufficient number of years (Ex.1900 is a safe starting point)
                $script:startDate = (Get-Date "1900-01-01")
                $script:endDate = (Get-Date).AddDays(-$script:rollingDateRange)
                $this.io.Log("Running data retention by rolling days.")
                $this.ExecByDateRange($script:startDate, $script:endDate, $this.config.dataRetention.durationLimitHours)
            }
            
            if ($script:StopRetention) {
                $this.io.Log("Stopping data retention.")
                $this.StopDataRetention()
            } 
            else {
                $this.io.Log("Initiated data retention. The process will run in the background and may take a while, depending on criteria used.")
                $this.io.Log("Please check the Last Executed Data Retention status at http(s)://<checkmarx_host>/cxwebclient/DataRetention.aspx")
            }
        }

    }

    # Run data retention by number of scans
    [Object] ExecByNumOfScans([int] $numOfScansToKeep, [int] $dataRetentionDurationLimitHrs) {
        $this.io.Log("ExecByNumOfScans: Number of scans to keep: [$numOfScansToKeep]")

        $dataRetentionParams = @{
          NumOfSuccessfulScansToPreserve = $numOfScansToKeep
          durationLimitInHours = $dataRetentionDurationLimitHrs
        }
        [String] $apiUrl = "/sast/dataRetention/byNumberOfScans"
        return $this.cxSastRestClient.invokeAPI($apiUrl, 'POST', $dataRetentionParams, 0)
    }

    # Run data retention by date range
    [Object] ExecByDateRange([DateTime] $startDate, [DateTime] $endDate, [int] $dataRetentionDurationLimitHrs) {
        $this.io.Log("ExecByDateRange: Start Date: [$startDate], End Date: [$endDate]")

        $dataRetentionParams = @{
            startDate = $startDate
            endDate = $endDate
            durationLimitInHours = $dataRetentionDurationLimitHrs
        }
        [String] $apiUrl = "/sast/dataRetention/byDateRange"
        return $this.cxSastRestClient.invokeAPI($apiUrl, 'POST', $dataRetentionParams, 0)
    } 

    # Stop data retention
    [Object] StopDataRetention() {

        [String] $apiUrl = "/sast/dataRetention/stop"
        return $this.cxSastRestClient.invokeAPI($apiUrl, 'POST', $null, 0)
    } 
}


# ========================================== #
# ============ Execution Entry ============= #
# ========================================== #

# Load configuration
[String] $config = ".\data_retention_config.json"

If ($configFile) {
    if(!(Test-Path $configFile)) {
        Write-Host "Could not read from given config path [$configFile]"
        Exit
    }
    else {
        $config = $configFile
    }
}

[PSCustomObject] $config = [Config]::new($config).GetConfig()

# Initialize log folder
[String] $logFolder = "."
if ($config) {
    $logFolder = $config.log.folder
    if (!(Test-Path $logFolder)) {
        New-Item -ItemType Directory -Force -Path $logFolder
    }    
}
$logFolder = (Get-Item -Path $logFolder).FullName

# Override config from command line params, if provided
if ($username) { $config.cx.username = $username }
if ($pass) { $config.cx.password = $pass }
if ($serviceUrl) { $config.cx.host = $serviceUrl }
if ($retentionDurationLimit) { $config.dataRetention.durationLimitHours = $retentionDurationLimit }

[IO] $io = [IO]::new()
$io.WriteHeader()

[DataRetention] $dataRetention = [DataRetention]::new($config)
$dataRetention.Execute()
