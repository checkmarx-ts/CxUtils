param(
    [Parameter(Mandatory = $true)]
    [hashtable]$session
)






# $soap_url = New-Object System.Uri $session.base_url, "/cxwebinterface/Audit/CxAuditWebService.asmx"


# $headers = @{
#     SOAPAction = "http://Checkmarx.com/v7/GetQueryCollection";
# }

$xml_template = @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v7="http://Checkmarx.com/v7">
   <soapenv:Header/>
   <soapenv:Body>
      <v7:GetQueryCollection>
         <v7:sessionId>{0}</v7:sessionId>
      </v7:GetQueryCollection>
   </soapenv:Body>
</soapenv:Envelope>
"@.ToString()

$body = [String]::Format($xml_template, $session.soap_session.SessionID)

$response = &"support\soap\soap_request.ps1" $session $body "/cxwebinterface/Audit/CxAuditWebService.asmx" "http://Checkmarx.com/v7/GetQueryCollection"

$response.Content


