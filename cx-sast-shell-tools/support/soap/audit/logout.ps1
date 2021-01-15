param(
   [Parameter(Mandatory = $true)]
   [hashtable]$session
)

if ($true -ne $session.soap_session.v9) {

   $xml_template = @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v7="http://Checkmarx.com/v7">
   <soapenv:Header/>
   <soapenv:Body>
      <v7:Logout>
         <v7:sessionID>{0}</v7:sessionID>
      </v7:Logout>
   </soapenv:Body>
</soapenv:Envelope>
"@.ToString()

   $body = [String]::Format($xml_template, $session.soap_session.SessionID)

   &"support\soap\soap_request.ps1" $session $body "/cxwebinterface/Audit/CxAuditWebService.asmx" "http://Checkmarx.com/v7/Logout"
}
$true
