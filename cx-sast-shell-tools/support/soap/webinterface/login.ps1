param(
    [System.Uri]$sast_url,
    [String]$username,
    [String]$password
)



$soap_path = "/cxwebinterface/Portal/CxWebService.asmx"

$soap_url = New-Object System.Uri $sast_url, $soap_path



$headers = @{
    SOAPAction = "http://Checkmarx.com/Login";
}

$xml_template = @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:chec="http://Checkmarx.com">
   <soapenv:Header/>
   
   <soapenv:Body>
      <chec:Login>
         <chec:applicationCredentials>
            <chec:User>{0}</chec:User>
            <chec:Pass>{1}</chec:Pass>
         </chec:applicationCredentials>
         <chec:lcid>{2}</chec:lcid>
      </chec:Login>
   </soapenv:Body>
</soapenv:Envelope>
"@.ToString()

$body = [String]::Format($xml_template, $username, $password, $(Get-WinSystemLocale).LCID)

$session = @{}

$response = Invoke-WebRequest -ContentType "text/xml" -Method "Post" -Headers $headers -Body $body -Uri $soap_url

if (200 -eq $response.StatusCode) {
    $payload = New-Object System.Xml.XmlDocument
    $payload.LoadXml($response.Content)

    Write-Debug $response.Content

    # Check success is false - 9.x fails because this method is no longer supported.
    if ($true -eq [Convert]::ToBoolean($payload.DocumentElement.SelectSingleNode("//*[local-name() = 'IsSuccesfull']").InnerText)) {
        $session.v9 = $false
        $session.SessionID = $payload.DocumentElement.SelectSingleNode("//*[local-name() = 'SessionId']").InnerText
        Write-Debug "Server is not v9"
    }
    else {

        # 9.x returns IsSuccessfull=false and also does not have SessionId
        if ($null -ne $payload.DocumentElement.SelectSingleNode("//*[local-name() = 'SessionId']") ) {
            throw "Unexpected response from SOAP method [$($headers.SOAPAction)] at [$soap_url]"
        }
        else {
            $session.v9 = $true
            $session.SessionID = 0
            Write-Debug "v9 server detected"
        }
    }
}
else {
    throw "Error invoking SOAP method [$($headers.SOAPAction)] at [$soap_url]: response code is $($response.StatusCode)"
}

$session
