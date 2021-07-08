 param(
    [Parameter(Mandatory = $true)]
    [hashtable]$session,
    [Parameter(Mandatory = $true)]
    [string]$payload,
    [Parameter(Mandatory = $true)]
    [string]$url_suffix,
    [Parameter(Mandatory = $true)]
    [string]$soap_action

)

$soap_url = New-Object System.Uri $session.base_url, $url_suffix

$headers = @{
    SOAPAction = $soap_action;
}

if ($true -eq $session.soap_session.v9) {
    . "support\rest_util.ps1"

    $v9_headers = GetAuthHeaders $session
    $headers = $headers + $v9_headers
}

Write-Debug "SOAP Request: action [$soap_action] at [$soap_url]"
$headers | %{Write-Debug $_}
Write-Debug $payload

$response = Invoke-WebRequest -ContentType "text/xml" -Method "Post" -Headers $headers -Body $payload -Uri $soap_url

if (200 -eq $response.StatusCode) {
    $content = New-Object System.Xml.XmlDocument
    $content.LoadXml($response.Content)

    if ($true -eq [Convert]::ToBoolean($content.DocumentElement.SelectSingleNode("//*[local-name() = 'IsSuccesfull']").InnerText)) {
        $response
    }
    else {
        $msg = $content.DocumentElement.SelectSingleNode("//*[local-name() = 'ErrorMessage']").InnerText
        throw "SOAP Request failed: $msg"
    }
}
else {
    throw "Error invoking SOAP method [$($headers.SOAPAction)] at [$soap_url]: response code is $($response.StatusCode)"
}


