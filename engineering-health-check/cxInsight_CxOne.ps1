<#
.SYNOPSIS
Retrieve SAST scan data from a CxOne tenant
.DESCRIPTION
Retrieve SAST scan data from a CxOne tenant for analysis by the Checkmarx Professional Services team.
.PARAMETER apiKey
The CxOne API key to use to connect to CxOne.
.PARAMETER daySpan
The number of days from the current day
.PARAMETER startDate
The start date of the date range you would like to collect data (Format: yyyy-mm-DD)
.PARAMETER endDate
The end date of the date range you would like to collect data (Format: yyyy-mm-DD)
.PARAMETER exclProjectName
Exclude the project name from the output
.EXAMPLE
C:\PS> .\cxInsight_CxOne.ps1 -ApiKey eyJhbG...y4J22
.EXAMPLE
C:\PS> .\cxInsight_CxOne.ps1 -ApiKey eyJhbG...y4J22 -DaySpan 180
.NOTES
Author:  Checkmarx Professional Services
Date:    2023-02-08
Updated: 2023-03-07
#>
param (
    # A CxOne API key
    [Parameter(Mandatory=$true)]
    [string]$apiKey,
    [int]$daySpan = 90,
    [string]$startDate = ((Get-Date).AddDays(-$DaySpan).ToString("yyyy-MM-dd")),
    [string]$endDate = (Get-Date -format "yyyy-MM-dd"),
    [Parameter(Mandatory=$False)]
    [switch]
    $exclProjectName
)

# See https://www.michev.info/Blog/Post/2140/decode-jwt-access-and-id-tokens-via-powershell
function Parse-JWTtoken {
    [cmdletbinding()]
    param([Parameter(Mandatory=$true)][string]$token)

    #Validate as per https://tools.ietf.org/html/rfc7519
    #Access and ID tokens are fine, Refresh tokens will not work
    if (!$token.Contains(".") -or !$token.StartsWith("eyJ")) { Write-Error "Invalid token" -ErrorAction Stop }

    #Header
    $tokenheader = $token.Split(".")[0].Replace('-', '+').Replace('_', '/')
    #Fix padding as needed, keep adding "=" until string length modulus 4 reaches 0
    while ($tokenheader.Length % 4) { Write-Verbose "Invalid length for a Base-64 char array or string, adding ="; $tokenheader += "=" }
    Write-Verbose "Base64 encoded (padded) header:"
    Write-Verbose $tokenheader

    #Payload
    $tokenPayload = $token.Split(".")[1].Replace('-', '+').Replace('_', '/')
    #Fix padding as needed, keep adding "=" until string length modulus 4 reaches 0
    while ($tokenPayload.Length % 4) { Write-Verbose "Invalid length for a Base-64 char array or string, adding ="; $tokenPayload += "=" }
    Write-Verbose "Base64 encoded (padded) payoad:"
    Write-Verbose $tokenPayload
    #Convert to Byte array
    $tokenByteArray = [System.Convert]::FromBase64String($tokenPayload)
    #Convert to string array
    $tokenArray = [System.Text.Encoding]::ASCII.GetString($tokenByteArray)
    Write-Verbose "Decoded array in JSON format:"
    Write-Verbose $tokenArray
    #Convert from JSON to PSObject
    $tokobj = $tokenArray | ConvertFrom-Json
    Write-Verbose "Decoded Payload:"

    return $tokobj
}

class CxOneClient {
    [string]$ApiBaseUrl
    [string]$ApiKey
    [string]$IamBaseUrl
    [string]$Instance
    [object]$JwtData
    [string]$Tenant
    [string]$AccessToken

    CxOneClient([string]$ApiKey) {
        $this.ApiKey = $ApiKey
        $this.JwtData = Parse-JWTtoken $ApiKey
        $this.IamBaseUrl = $this.JwtData.iss
        $bits = $this.IamBaseUrl.Split("/")
        $this.Tenant = $bits[5]
        $hostname = $bits[2]
        $bits = $hostname.Split(".")
        switch ($bits.Length) {
            3 {
                $this.Instance = "us"
                $this.ApiBaseUrl = "https://ast.checkmarx.net/api"
            }
            4 {
                $this.Instance = $bits[0]
                $this.ApiBaseUrl = "https://" + $this.Instance + ".ast.checkmarx.net/api"
            }
            default {
                Write-Error $hostname + ": unexpected hostname format" -ErrorAction Stop
            }
        }
        $this.Connect()
    }

    [void] Connect() {
        $params = @{
            grant_type = "refresh_token"
            client_id = "ast-app"
            refresh_token = $this.ApiKey
        }
        $uri = $this.IamBaseUrl + "/protocol/openid-connect/token"
        $this.AccessToken = (Invoke-RestMethod $uri -Method POST -Body $params).access_token
        Write-Verbose "Access Token: $($this.AccessToken)"
    }

    [object] InvokeApi($ApiPath) {
        $headers = @{
            Accept = "application/json; version=1.0"
            Authorization = "Bearer $($this.AccessToken)"
        }
        $uri = "$($this.ApiBaseUrl)$ApiPath"
        Write-Verbose "URI: $uri"
        $response = (Invoke-RestMethod $uri -Method GET -Headers $headers)
        return $response
    }

    [object] GetProjects() {
        $ApiPath = "/projects"
        $projects = $this.InvokeApi($ApiPath)
        return $projects
    }

    [object] GetScans($FromDate, $ToDate) {

        $ApiPath = "/scans/?from-date=${FromDate}&to-date=${ToDate}"
        $scans = $this.InvokeApi($ApiPath)
        return $scans
    }

    [object] GetSastMetaData($ScanId) {

        $ApiPath = "/sast-metadata/$ScanId"
        $scans = $this.InvokeApi($ApiPath)
        return $scans
    }

    [object] GetSastScanResults($ScanId) {

        $ApiPath = "/sast-results/?scan-id=${ScanId}"
        $scanResults = $this.InvokeApi($ApiPath)
        return $scanResults
    }

    [object] GetResultsForAllScanners($ScanId) {

        $ApiPath = "/results/?scan-id=${ScanId}"
        $scanResults = $this.InvokeApi($ApiPath)
        return $scanResults
    }
}

class Scan {
    # Scan fields
    [string]$id
    [string]$status
    [string]$branch
    [DateTime]$createdAt
    [DateTime]$updatedAt
    [string]$projectId
    [string]$projectName
    [string]$initiator
    [string]$tags
    [string]$metadata
    [string]$engines
    [string]$sourceType
    [string]$sourceOrigin
    # Scan metadata
    [int]$loc
    [int]$fileCount
    [bool]$isIncremental
    [bool]$isIncrementalCancelled
    [string]$incrementalCancelledReason
    [string]$baseId
    [int]$addedFilesCount
    [int]$changedFilesCount
    [double]$changePercentage
    [string]$queryPreset
    # Scan results
    # - Severities
    [int]$totalResults
    [int]$high
    [int]$medium
    [int]$low
    [int]$info
    # - States
    [int]$toVerify
    [int]$confirmed
    [int]$proposedNotExploitable
    [int]$notExploitable
    [int]$urgent
    # - Statuses
    [int]$new
    [int]$recurrent
}

# Dates should be in RFC3339 Date (Extend) format (e.g. 2021-06-02T12:14:18.028555Z)
$StartDate = "${StartDate}T00%3A00%3A00Z"
$EndDate = "${EndDate}T00%3A00%3A00Z"

$client = [CxOneClient]::new($ApiKey)
$getProjectsResult =  $client.GetProjects()
$getScansResult = $client.GetScans($StartDate, $EndDate)
$scans = @()
foreach ($scan in $getScansResult.Scans) {
    $GetSastMetaDataResult = $client.GetSastMetaData($Scan.id)
    $GetSastScanResultsResult = $client.GetSastScanResults($Scan.id)
    $severities = @{}
    $states = @{}
    $statuses = @{}
    $totalResults = 0
    foreach ($result in $getSastScanResultsResult.results) {
        $Severities[$result.severity] += 1
        $States[$result.state] += 1
        $Statuses[$result.status] += 1
        $totalResults += 1
    }

    $newScan = [Scan]::new()
    $newScan.id = $scan.id
    $newScan.status = $scan.status
    $newScan.branch = $scan.branch
    $newScan.createdAt = $scan.createdAt
    $newScan.updatedAt = $scan.updatedAt
    $newScan.projectId = $scan.projectId
    if (! $exclProjectName) {
        $newScan.projectName = $scan.projectName
    }
    $newScan.initiator = $scan.initiator
    $newScan.tags = $scan.tags
    $newScan.metadata = $scan.metadata
    $newScan.engines = $scan.engines
    $newScan.sourceType = $scan.sourceType
    $newScan.sourceOrigin = $scan.sourceOrigin

    $newScan.loc = $getScanMetaDataResult.loc
    $newScan.fileCount = $getScanMetaDataResult.fileCount
    $newScan.isIncremental = $getScanMetaDataResult.isIncremental
    $newScan.isIncrementalCancelled = $getScanMetaDataResult.isIncrementalCancelled
    $newScan.incrementalCancelledReason = $getScanMetaDataResult.incrementalCancelledReason
    $newScan.baseId = $getScanMetaDataResult.baseId
    $newScan.addedFilesCount = $getScanMetaDataResult.addedFilesCount
    $newScan.changedFilesCount = $getScanMetaDataResult.changedFilesCount
    $newScan.changePercentage = $getScanMetaDataResult.changePercentage
    $newScan.queryPreset = $getScanMetaDataResult.queryPreset

    $newScan.totalResults = $totalResults
    $newScan.high = $severities["HIGH"]
    $newScan.medium = $severities["MEDIUM"]
    $newScan.low = $severities["LOW"]
    $newScan.info = $severities["INFO"]
    # - States
    $newScan.toVerify = $states["TO_VERIFY"]
    $newScan.confirmed = $states["CONFIRMED"]
    $newScan.proposedNotExploitable = $states["PROPOSED_NOT_EXPLOITABLE"]
    $newScan.notExploitable = $states["NOT_EXPLOITABLE"]
    $newScan.urgent = $states["URGENT"]
    # - Statuses
    $newScan.new = $statuses["NEW"]
    $newScan.recurrent = $statuses["RECURRENT"]

    $scans += $newScan
}

$scans | ConvertTo-Json