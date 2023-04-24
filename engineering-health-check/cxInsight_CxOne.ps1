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
.EXAMPLE
C:\PS> .\cxInsight_CxOne.ps1 -ApiKey eyJhbG...y4J22
.EXAMPLE
C:\PS> .\cxInsight_CxOne.ps1 -ApiKey eyJhbG...y4J22 -DaySpan 180
.EXAMPLE
C:\PS> .\cxInsight_CxOne.ps1 -ApiKey eyJhbG...y4J22 -Limit 500
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
    [int]$limit = 200
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
        $resp = Invoke-RestMethod $uri -Method POST -Body $params
        Write-Debug "Response: ${resp}"
        $this.AccessToken = $resp.access_token
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
            Write-Debug "Retrieved $($response.$resultsProperty.length) items"
            if ($response.$resultsProperty.length -eq 0 -and $response.totalCount -gt 0) {
                Write-Host "Warning: invoking ${uriWithOffset} returned 0 results"
                break
            }
            $count += $response.$resultsProperty.length
            if ($offsetByCount) {
                $offset += $count
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
                }
                404 {
                    Write-Host "Received a 404 response for ${uri}"
                }
                default {
                    Write-Error "Received a ${statusCode} response for ${uri}"
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
    # Scan metadata metrics
    [object]$languages
    # Scan results
    [object]$results
}

# Dates should be in RFC3339 Date (Extend) format (e.g. 2021-06-02T12:14:18.028555Z)
$StartDate = "${StartDate}T00%3A00%3A00Z"
$EndDate = "${EndDate}T00%3A00%3A00Z"

$client = [CxOneClient]::new($ApiKey, $limit)
$getScansResult = $client.GetScans($StartDate, $EndDate)
$scans = @()
foreach ($scan in $getScansResult) {
    $GetSastMetaDataResult = $client.GetSastMetaData($Scan.id)
    $GetSastMetaDataMetricsResult = $client.GetSastMetaDataMetrics($Scan.id)
    $GetResultsForAllScannersResult = $client.GetResultsForAllScanners($scan.id)
    $results = @{}
    foreach ($result in $GetResultsForAllScannersResult) {
        $engine = $result.type
        if (-not ($results.Keys -contains $engine)) {
            $results[$engine] = @{}
            $results[$engine]["count"] = 0
            $results[$engine]["severity"] = @{}
            $results[$engine]["state"] = @{}
            $results[$engine]["status"] = @{}
        }
        $results[$engine]["count"] += 1
        if ($results[$engine]["severity"].Keys -contains $result.severity) {
            $results[$engine]["severity"][$result.severity] += 1
        } else {
            $results[$engine]["severity"][$result.severity] = 1
        }
        if ($results[$engine]["state"].Keys -contains $result.state) {
            $results[$engine]["state"][$result.state] += 1
        } else {
            $results[$engine]["state"][$result.state] = 1
        }
        if ($results[$engine]["status"].Keys -contains $result.status) {
            $results[$engine]["status"][$result.status] += 1
        } else {
            $results[$engine]["status"][$result.status] = 1
        }
    }

    $newScan = [Scan]::new()
    $newScan.id = $scan.id
    $newScan.status = $scan.status
    $newScan.statusDetails = @{}
    foreach ($statusDetails in $scan.statusDetails) {
        $newScan.statusDetails[$statusDetails.name] = $statusDetails.status
    }
    $newScan.branch = $scan.branch
    $newScan.createdAt = $scan.createdAt
    $newScan.updatedAt = $scan.updatedAt
    $newScan.projectId = $scan.projectId
    if (! $exclProjectName) {
        $newScan.projectName = $scan.projectName
    }
    $newScan.initiator = $scan.initiator
    $newScan.tags = $scan.tags
    # The type property is the only metadata property that we are interested in
    $newScan.type = $scan.metadata.type
    $newScan.engines = $scan.engines
    $newScan.sourceType = $scan.sourceType
    $newScan.sourceOrigin = $scan.sourceOrigin

    $newScan.loc = $GetSastMetaDataResult.loc
    $newScan.fileCount = $GetSastMetaDataResult.fileCount
    $newScan.isIncremental = $GetSastMetaDataResult.isIncremental
    $newScan.isIncrementalCancelled = $GetSastMetaDataResult.isIncrementalCancelled
    $newScan.incrementalCancelledReason = $GetSastMetaDataResult.incrementalCancelledReason
    $newScan.baseId = $GetSastMetaDataResult.baseId
    $newScan.addedFilesCount = $GetSastMetaDataResult.addedFilesCount
    $newScan.changedFilesCount = $GetSastMetaDataResult.changedFilesCount
    $newScan.changePercentage = $GetSastMetaDataResult.changePercentage
    $newScan.queryPreset = $GetSastMetaDataResult.queryPreset

    # We wrap the right hand side in @() to force an array even when
    # there is only one language
    $newScan.languages = @($GetSastMetaDataMetricsResult.scannedFilesPerLanguage.psobject.properties | foreach-object { $_.name })

    $newScan.results = $results

    $scans += $newScan
}

$scans | ConvertTo-Json -Depth 5 | Out-File -Encoding utf8 -FilePath ".\scan-data.json"

$files = @(".\scan-data.json")
# Compress-Archive was introduced in PowerShell version 5.
if ($PSVersionTable.PSVersion.Major -gt 4) {
    Compress-Archive -Path $files -DestinationPath ".\data.zip" -Force
    Remove-Item -Path $files
}
