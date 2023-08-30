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
.PARAMETER limit
The maximum number of objects to retrieve in a single API call (defaults to 200)
.PARAMETER quiet
Don't print completion message when script finishes
.PARAMETER scanId
Return the data for the specified scan
.EXAMPLE
C:\PS> .\cxInsight_CxOne.ps1 -ApiKey eyJhbG...y4J22
.EXAMPLE
C:\PS> .\cxInsight_CxOne.ps1 -ApiKey eyJhbG...y4J22 -DaySpan 180
.EXAMPLE
C:\PS> .\cxInsight_CxOne.ps1 -ApiKey eyJhbG...y4J22 -Limit 500
.EXAMPLE
C:\PS> .\cxInsight_CxOne.ps1 -ApiKey eyJhbG...y4J22 -ScanId 5c7ffe5f-ff3c-473a-beb9-a59d8f6143b8
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
    $exclProjectName,
    [int]$limit = 200,
    [string]$scanId,
    [switch]
    $quiet
)

Set-StrictMode -Version 1.0

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
    while ($tokenheader.Length % 4) { Write-Debug "Invalid length for a Base-64 char array or string, adding ="; $tokenheader += "=" }
    Write-Debug "Base64 encoded (padded) header:"
    Write-Debug $tokenheader

    #Payload
    $tokenPayload = $token.Split(".")[1].Replace('-', '+').Replace('_', '/')
    #Fix padding as needed, keep adding "=" until string length modulus 4 reaches 0
    while ($tokenPayload.Length % 4) { Write-Verbose "Invalid length for a Base-64 char array or string, adding ="; $tokenPayload += "=" }
    Write-Debug "Base64 encoded (padded) payload:"
    Write-Debug $tokenPayload
    #Convert to Byte array
    $tokenByteArray = [System.Convert]::FromBase64String($tokenPayload)
    #Convert to string array
    $tokenArray = [System.Text.Encoding]::ASCII.GetString($tokenByteArray)
    Write-Debug "Decoded array in JSON format:"
    Write-Debug $tokenArray
    #Convert from JSON to PSObject
    $tokobj = $tokenArray | ConvertFrom-Json
    Write-Debug "Decoded Payload:"

    return $tokobj
}

class CxOneClient {
    [string]$ApiBaseUrl
    [string]$ApiKey
    [string]$IamBaseUrl
    [string]$Instance
    [object]$JwtData
    [int]$limit
    [string]$Tenant
    [string]$AccessToken

    CxOneClient([string]$ApiKey, [int]$limit) {
        $this.ApiKey = $ApiKey
        $this.limit = $limit
        $this.JwtData = Parse-JWTtoken $ApiKey
        $this.IamBaseUrl = $this.JwtData.iss
        $bits = $this.IamBaseUrl.Split("/")
        $scheme = $bits[0] # Note that this includes the : after the
                           # scheme (e.g., "https:").
        $this.Tenant = $bits[5]
        $hostname = $bits[2]
        # If the IAM base URL ends with "ast.checkmarx.net", we assume
        # that we are dealing with a multi-tenant instance and derive
        # the API URL accordingly. For single-tenant instances, we
        # assume that the API URL will be the same as the IAM URL.
        Write-Debug "Hostname is $hostname"
        if ($hostname.EndsWith("iam.checkmarx.net")) {
            Write-Verbose "Assuming a multi-tenant instance"
            $bits = $hostname.Split(".")
            switch ($bits.Length) {
                3 {
                    $this.Instance = "us"
                    $this.ApiBaseUrl = "$scheme//ast.checkmarx.net/api"
                }
                4 {
                    $this.Instance = $bits[0]
                    $this.ApiBaseUrl = "$scheme//" + $this.Instance + ".ast.checkmarx.net/api"
                }
                default {
                    Write-Error $hostname + ": unexpected hostname format" -ErrorAction Stop
                }
            }
        } else {
            Write-Verbose "Assuming a single-tenant instance"
            $this.ApiBaseUrl = "$scheme//" + $hostname + "/api"
        }

        Write-Debug "IAM base URL: $($this.IamBaseUrl)"
        Write-Debug "API base URL: $($this.ApiBaseUrl)"

        $this.Connect()
    }

    [void] Connect() {
        $params = @{
            grant_type = "refresh_token"
            client_id = "ast-app"
            refresh_token = $this.ApiKey
        }
        Write-Verbose "Retrieving token..."
        $uri = $this.IamBaseUrl + "/protocol/openid-connect/token"
        $resp = Invoke-RestMethod $uri -Method POST -Body $params
        Write-Debug "Response: ${resp}"
        $this.AccessToken = $resp.access_token
        Write-Verbose "Token retrieved"
    }

    [object] InvokeArrayApi($ApiPath, $resultsProperty, $offsetByCount) {
        Write-Debug "InvokeArrayApi: ApiPath: ${ApiPath}, resultsProperty: ${resultsProperty}, offsetByCount: ${offsetByCount}"
        $headers = @{
            Accept = "application/json; version=1.0"
            Authorization = "Bearer $($this.AccessToken)"
        }
        $uri = "$($this.ApiBaseUrl)$ApiPath"
        Write-Verbose "URI: $uri"
        $count = 0
        $offset = 0
        $totalCount = 0
        $response = $null
        if ($apiPath.contains("?")) {
            $sep = "&"
        } else {
            $sep = "?"
        }
        $results = [System.Collections.ArrayList]::new()
        do {
            $uriWithOffset ="$uri${sep}offset=${offset}&limit=$($this.limit)"
            Write-Verbose "URI with offset: $uriWithOffset"
            $response = $this.InvokeApi($uriWithOffset, "GET", $headers)
            if ( $null -eq $response ) {
                Write-Warning 'InvokeApi() returned `$null. Results may be incomplete.'
                break
            }
            $retrieved = $response.$resultsProperty.length
            Write-Debug "Retrieved ${retrieved} items"
            if ($response.$resultsProperty.length -eq 0 -and $response.totalCount -gt 0) {
                Write-Host "Warning: invoking ${uriWithOffset} returned 0 results"
                break
            }
            $count += $retrieved
            if ($offsetByCount) {
                $offset = $count
            } else {
                $offset += 1
            }
            $results.AddRange($response.$resultsProperty)
            # Annoyingly, some API responses have the filteredTotalCount
            # property but others do not.
            if ($response.PSObject.Properties.name -match "filteredTotalCount") {
                $totalCount = $response.filteredTotalCount
            } else {
                $totalCount = $response.totalCount
            }
            Write-Debug "Count: ${count}, total count: $totalCount"
        } while ($count -lt $totalCount)
        return $results
    }

    [object] InvokeObjectApi($ApiPath) {
        $headers = @{
            Accept = "application/json; version=1.0"
            Authorization = "Bearer $($this.AccessToken)"
        }
        $uri = "$($this.ApiBaseUrl)$ApiPath"
        Write-Verbose "URI: $uri"
        $response = $this.InvokeApi($uri, "GET", $headers)
        return $response
    }

    [object] InvokeApi($uri, $method, $headers) {
        $response = $null
        try {
            $response = Invoke-RestMethod $uri -Method GET -Headers $headers
        } catch {
            $statusCode = $_.Exception.Response.StatusCode.value__
            switch ($statusCode) {
                401 {
                    Write-Verbose "Received a 401 response. Reconnecting..."
                    $this.Connect()
                    $response = Invoke-RestMethod $uri -Method GET -Headers $headers
                }
                404 {
                    Write-Host "Received a 404 response for ${uri}"
                }
                default {
                    Write-Error "Received a ${statusCode} response for ${uri}" -ErrorAction stop
                }
            }
        }
        return $response
    }

    [object] GetProjects() {
        $ApiPath = "/projects"
        $projects = $this.InvokeArrayApi($ApiPath, "projects")
        return $projects
    }

    [object] GetScans($FromDate, $ToDate) {

        $ApiPath = "/scans/?from-date=${FromDate}&to-date=${ToDate}"
        $scans = $this.InvokeArrayApi($ApiPath, "scans", $true)
        return $scans
    }

    [object] GetScan($scanId) {

        $ApiPath = "/scans/${scanId}"
        $scans = $this.InvokeObjectApi($ApiPath)
        return $scans
    }

    [object] GetSastMetaData($ScanId) {

        $ApiPath = "/sast-metadata/$ScanId"
        $scans = $this.InvokeObjectApi($ApiPath)
        return $scans
    }

    [object] GetSastMetaDataMetrics($ScanId) {

        $ApiPath = "/sast-metadata/$ScanId/metrics"
        $scans = $this.InvokeObjectApi($ApiPath)
        return $scans
    }

    [object] GetSastScanResults($ScanId) {

        $ApiPath = "/sast-results/?scan-id=${ScanId}"
        $scanResults = $this.InvokeArrayApi($ApiPath, "results", $true)
        return $scanResults
    }

    [object] GetResultsForAllScanners($ScanId) {

        $ApiPath = "/results/?scan-id=${ScanId}"
        $scanResults = $this.InvokeArrayApi($ApiPath, "results", $false)
        return $scanResults
    }
}

class SastMetadata {
    # Scan metadata
    [int]$loc
    [int]$fileCount
    [bool]$isIncremental
    [bool]$isIncrementalCanceled
    [string]$incrementalCancelReason
    [string]$baseId
    [int]$addedFilesCount
    [int]$changedFilesCount
    [double]$changePercentage
    [string]$queryPreset
    # Scan metadata metrics
    [int]$totalScannedFilesCount
    [int]$totalScannedLoc
    [object]$languages
}

class Scan {
    # Scan fields
    [string]$id
    [string]$status
    [object]$statusDetails
    [string]$branch
    [DateTime]$createdAt
    [DateTime]$updatedAt
    [string]$projectId
    [string]$projectName
    [string]$initiator
    [object]$tags
    [string]$type
    [object]$engines
    [string]$sourceType
    [string]$sourceOrigin
    [object]$sastMetadata
    [object]$results

    Scan($client, $scan, $exclProjectName) {
        $this.id = $scan.id
        $this.status = $scan.status
        $this.statusDetails = @{}
        foreach ($statusDetails in $scan.statusDetails) {
            $this.statusDetails[$statusDetails.name] = $statusDetails.status
        }
        $this.branch = $scan.branch
        $this.createdAt = $scan.createdAt
        $this.updatedAt = $scan.updatedAt
        $this.projectId = $scan.projectId
        if (! $exclProjectName) {
            $this.projectName = $scan.projectName
        }
        $this.initiator = $scan.initiator
        $this.tags = $scan.tags
        # The type property is the only metadata property that we are interested in
        $this.type = $scan.metadata.type
        $this.engines = $scan.engines
        $this.sourceType = $scan.sourceType
        $this.sourceOrigin = $scan.sourceOrigin

        if ($this.status -ne "Failed") {
            if ($this.statusDetails.sast -eq "Completed") {
                $this.getSastMetadata($client, $scan.id)
            }

            $this.getScanResults($client, $scan.id)
        }
    }

    getScanResults($client, $scanId) {
        $GetResultsForAllScannersResult = $client.GetResultsForAllScanners($scanId)
        $this.results = @{}
        foreach ($result in $GetResultsForAllScannersResult) {
            $engine = $result.type
            if (-not ($this.results.Keys -contains $engine)) {
                $this.results[$engine] = @{}
                $this.results[$engine]["count"] = 0
                $this.results[$engine]["severity"] = @{}
                $this.results[$engine]["state"] = @{}
                $this.results[$engine]["status"] = @{}
            }
            $this.results[$engine]["count"] += 1
            if ($this.results[$engine]["severity"].Keys -contains $result.severity) {
                $this.results[$engine]["severity"][$result.severity] += 1
            } else {
                $this.results[$engine]["severity"][$result.severity] = 1
            }
            if ($this.results[$engine]["state"].Keys -contains $result.state) {
                $this.results[$engine]["state"][$result.state] += 1
            } else {
                $this.results[$engine]["state"][$result.state] = 1
            }
            if ($this.results[$engine]["status"].Keys -contains $result.status) {
                $this.results[$engine]["status"][$result.status] += 1
            } else {
                $this.results[$engine]["status"][$result.status] = 1
            }
        }
    }

    getSastMetadata($client, $scanId) {
        Write-Verbose "Retrieving SAST metadata"
        $GetSastMetaDataResult = $client.GetSastMetaData($ScanId)
        $GetSastMetaDataMetricsResult = $client.GetSastMetaDataMetrics($ScanId)
        $this.sastMetadata = [SastMetadata]::new()
        $this.sastMetadata.loc = $GetSastMetaDataResult.loc
        $this.sastMetadata.fileCount = $GetSastMetaDataResult.fileCount
        $this.sastMetadata.isIncremental = $GetSastMetaDataResult.isIncremental
        $this.sastMetadata.isIncrementalCanceled = $GetSastMetaDataResult.isIncrementalCanceled
        $this.sastMetadata.incrementalCancelReason = $GetSastMetaDataResult.incrementalCancelReason
        $this.sastMetadata.baseId = $GetSastMetaDataResult.baseId
        $this.sastMetadata.addedFilesCount = $GetSastMetaDataResult.addedFilesCount
        $this.sastMetadata.changedFilesCount = $GetSastMetaDataResult.changedFilesCount
        $this.sastMetadata.changePercentage = $GetSastMetaDataResult.changePercentage
        $this.sastMetadata.queryPreset = $GetSastMetaDataResult.queryPreset

        $this.sastMetadata.totalScannedFilesCount = $GetSastMetaDataMetricsResult.totalScannedFilesCount
        $this.sastMetadata.totalScannedLoc = $GetSastMetaDataMetricsResult.totalScannedLoc
        if ($GetSastMetaDataMetricsResult.totalScannedFilesCount -gt 0) {
            # We wrap the right hand side in @() to force an array even when
            # there is only one language
            $this.sastMetadata.languages = @($GetSastMetaDataMetricsResult.scannedFilesPerLanguage.psobject.properties | foreach-object { $_.name })
        }
    }
}

$client = [CxOneClient]::new($ApiKey, $limit)
if ($scanId) {
    $GetScanResult = $client.GetScan($scanId)
    $scan = [Scan]::new($client, $GetScanResult, $exclProjectName)
    $scan | ConvertTo-Json -Depth 5
} else {
    # Dates should be in RFC3339 Date (Extend) format (e.g. 2021-06-02T12:14:18.028555Z)
    $StartDate = "${StartDate}T00%3A00%3A00Z"
    $EndDate = "${EndDate}T00%3A00%3A00Z"

    $getScansResult = $client.GetScans($StartDate, $EndDate)
    $scans = @()
    foreach ($scan in $getScansResult) {
        $scans += [Scan]::new($client, $scan, $exclProjectName)
    }

    $scans | ConvertTo-Json -Depth 5 | Out-File -Encoding utf8 -FilePath ".\scan-data.json"

    $files = @(".\scan-data.json")
    # Compress-Archive was introduced in PowerShell version 5.
    if ($PSVersionTable.PSVersion.Major -gt 4) {
        Compress-Archive -Path $files -DestinationPath ".\data.zip" -Force
        Remove-Item -Path $files
        if ( ! $quiet) {
            Read-Host -Prompt "The script was successful. Please send the 'data.zip' file in this directory to your Checkmarx Engineer. Press Enter to exit"
        }
    }
    elseif ( ! $quiet) {
        Read-Host -Prompt "The script was successful. Please send the ${files} file(s) in this directory to your Checkmarx Engineer. Press Enter to exit"
    }
}
