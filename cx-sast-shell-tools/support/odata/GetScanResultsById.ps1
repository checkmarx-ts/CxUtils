param(
    [Parameter(Mandatory=$true)]
    [hashtable]$Session,
    [Parameter(Mandatory=$true)]
    [String]$ScanId,
    [Parameter(Mandatory=$false)]
    [ValidateSet("Information", "Low", "Medium", "High")]
    [String]$Severity,
    [Parameter(Mandatory=$false)]
    [ValidateSet("To Verify", "Not Exploitable", "Confirmed", "Urgent", "Proposed Not Exploitable")]
    [String]$State

)

. "$PSScriptRoot/../rest_util.ps1"

$ODataScanResultsBaseUrl = [String]::Format("/CxWebInterface/odata/v1/Scans({0})/Results", $ScanId)
$ODataUrl = $ODataScanResultsBaseUrl

if($Severity) {
    $SeverityFillter = [String]::Format("Severity eq '{0}'", $Severity)
    $ODataUrl = [String]::Concat($ODataScanResultsBaseUrl, "?`$filter=", $SeverityFillter)
}

if($State) {
    $ResultStateIds = @{
        "To Verify" = "0";
        "Not Exploitable" = "1";
        "Confirmed" = "2";
        "Urgent" = "3";
        "ProposedNotExploitable" = "4";
    }
    $StateId = $ResultStateIds[$State]
    $StateFillter = [String]::Format("StateId eq {0}", $StateId)
    $ODataUrl = [String]::Concat($ODataScanResultsBaseUrl, "?`$filter=", $StateFillter)
}

if($SeverityFillter -and $StateFillter) {
    $SeverityAndStateFillter = [String]::Concat($SeverityFillter, " and ", $StateFillter)
    $ODataUrl = [String]::Concat($ODataScanResultsBaseUrl, "?`$filter=", $SeverityAndStateFillter)
}



$RequestUrl = New-Object System.Uri $Session.base_url, $ODataUrl

Write-Debug "ScanId: $ScanId Severity: $Severity State: $State StateId: $StateId ODataUrl: $ODataUrl"

$Headers = GetRestHeadersForJsonRequest($Session)

Write-Debug $RequestUrl

try {
    $Response = Invoke-RestMethod -Method 'GET' -Uri $RequestUrl -Headers $Headers
    return $Response
}
catch {
    Write-Output "StatusCode:" $_.Exception.Response.StatusCode.value__
    Write-Output "StatusDescription:" $_.Exception.Response.StatusDescription
    throw "Error on: $method $endpoint"
}
