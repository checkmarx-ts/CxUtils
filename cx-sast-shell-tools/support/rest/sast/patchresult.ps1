param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [String]$scanId,
    [Parameter(Mandatory=$true)]
    [String]$resultId,
    [Parameter(Mandatory=$true)]
    [String]$resultStateId,
    [Parameter(Mandatory=$true)]
    [String]$Comment
)

. "support/rest_util.ps1"

$rest_url = [String]::Format("/cxrestapi/sast/scans/{0}/results/{1}", $scanId, $resultId)
$request_url = New-Object System.Uri $session.base_url, $rest_url

Write-Debug "Update result state for scanId: $scanId, resultId: $resultId"

#create body for update
$body_elems = @{
    state = $resultStateId;
    comment = $Comment;
}

$body = GetQueryStringFromHashtable $body_elems

Write-Debug $body

$headers = GetRestHeadersForJsonRequest($session)

Write-Debug $request_url

try {
    $response = Invoke-RestMethod -Method 'Patch' -Uri $request_url -Headers $headers -ContentType "application/x-www-form-urlencoded" -Body $body 
    return $response
}
catch {
    Write-Output "StatusCode:" $_.Exception.Response.StatusCode.value__
    Write-Output "StatusDescription:" $_.Exception.Response.StatusDescription
    throw "Error on: $method $endpoint"
}
