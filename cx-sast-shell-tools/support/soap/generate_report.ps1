param(
    [Parameter(Mandatory = $true)]
    [hashtable]$session,
    [Parameter(Mandatory = $true)]
    [String]$scan_id
)

$templatepath = "$PSScriptRoot"
Import-LocalizedData -BaseDirectory $templatepath -FileName CxReportTemplate.psd1 -BindingVariable ReportTemplate

$soap_path = "/cxwebinterface/Portal/CxWebService.asmx"

$soap_url = New-Object System.Uri $session.base_url, $soap_path

$soap_action = "http://Checkmarx.com/CreateScanReport"
#$headers = @{
#    SOAPAction = "http://Checkmarx.com/CreateScanReport";
#}

$xml_template = @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:chec="http://Checkmarx.com">
   <soapenv:Header/>
   <soapenv:Body>
      <chec:CreateScanReport>
         <chec:SessionID>{0}</chec:SessionID>
         <chec:Report>
            <chec:Type>{1}</chec:Type>
            <chec:ScanID>{2}</chec:ScanID>
            <chec:DisplayData>
               <chec:Queries>
                  <chec:All>{3}</chec:All>
                  <chec:IDs>
                     <!--Zero or more repetitions:-->
                     <chec:long>{4}</chec:long>
                  </chec:IDs>
               </chec:Queries>
               <chec:ResultsSeverity>
                  <chec:All>{5}</chec:All>
                  <chec:High>{6}</chec:High>
                  <chec:Medium>{7}</chec:Medium>
                  <chec:Low>{8}</chec:Low>
                  <chec:Info>{9}</chec:Info>
               </chec:ResultsSeverity>
               
               <chec:ResultsState>
                  <chec:All>{10}</chec:All>
                  
                  <chec:IDs>
                     <!--Zero or more repetitions:-->
                     <chec:long>{11}</chec:long>
                  </chec:IDs>
               </chec:ResultsState>
               
               <chec:DisplayCategories>
                  <chec:All>{12}</chec:All>
                  
                  <chec:IDs>
                     <!--Zero or more repetitions:-->
                     <chec:long>{13}</chec:long>
                  </chec:IDs>
               </chec:DisplayCategories>
               
               <chec:ResultsAssigedTo>
                  <chec:All>{14}</chec:All>
                  
                  <chec:IDs>
                     <!--Zero or more repetitions:-->
                     <chec:long>{15}</chec:long>
                  </chec:IDs>
                  
                  <chec:Usernames>
                     <!--Zero or more repetitions:-->
                     <chec:string>{16}</chec:string>
                  </chec:Usernames>
               </chec:ResultsAssigedTo>
               
               <chec:ResultsPerVulnerability>
                  <chec:All>{17}</chec:All>
                  <chec:Maximimum>{18}</chec:Maximimum>
               </chec:ResultsPerVulnerability>
               
               <chec:HeaderOptions>
                  <chec:Link2OnlineResults>{19}</chec:Link2OnlineResults>
                  <chec:Team>{20}</chec:Team>
                  <chec:CheckmarxVersion>{21}</chec:CheckmarxVersion>
                  <chec:ScanComments>{22}</chec:ScanComments>
                  <chec:ScanType>{23}</chec:ScanType>
                  <chec:SourceOrigin>{24}</chec:SourceOrigin>
                  <chec:ScanDensity>{25}</chec:ScanDensity>
               </chec:HeaderOptions>
               
               <chec:GeneralOption>
                  <chec:OnlyExecutiveSummary>{26}</chec:OnlyExecutiveSummary>
                  <chec:TableOfContents>{27}</chec:TableOfContents>
                  <chec:ExecutiveSummary>{28}</chec:ExecutiveSummary>
                  <chec:DisplayCategories>{29}</chec:DisplayCategories>
                  <chec:DisplayLanguageHashNumber>{30}</chec:DisplayLanguageHashNumber>
                  <chec:ScannedQueries>{31}</chec:ScannedQueries>
                  <chec:ScannedFiles>{32}</chec:ScannedFiles>
                  <chec:VulnerabilitiesDescription>{33}</chec:VulnerabilitiesDescription>
               </chec:GeneralOption>
               
               <chec:ResultsDisplayOption>
                  <chec:AssignedTo>{34}</chec:AssignedTo>
                  <chec:Comments>{35}</chec:Comments>
                  <chec:Link2Online>{36}</chec:Link2Online>
                  <chec:ResultDescription>{37}</chec:ResultDescription>
                  <chec:SnippetsMode>{38}</chec:SnippetsMode>
               </chec:ResultsDisplayOption>
            </chec:DisplayData>
         </chec:Report>
      </chec:CreateScanReport>
   </soapenv:Body>
</soapenv:Envelope>
"@.ToString()

$body = [String]::Format($xml_template, 
                        $session.soap_session.sessionID, 
                        $ReportTemplate.reportType,
                        $scan_id,
                        $ReportTemplate.queries.all,
                        $ReportTemplate.queries.ids,
                        $ReportTemplate.resultSeverity.all,
                        $ReportTemplate.resultSeverity.high,
                        $ReportTemplate.resultSeverity.medium,
                        $ReportTemplate.resultSeverity.low,
                        $ReportTemplate.resultSeverity.info,
                        $ReportTemplate.resultState.all,
                        $ReportTemplate.resultState.ids,
                        $ReportTemplate.displayCategories.all,
                        $ReportTemplate.displayCategories.ids,
                        $ReportTemplate.resultsAssignedTo.all,
                        $ReportTemplate.resultsAssignedTo.ids,
                        $ReportTemplate.resultsAssignedTo.usernames,
                        $ReportTemplate.resultsPerVuln.all,
                        $ReportTemplate.resultsPerVuln.max,
                        $ReportTemplate.headerOptions.link2online,
                        $ReportTemplate.headerOptions.team,
                        $ReportTemplate.headerOptions.version,
                        $ReportTemplate.headerOptions.scanComments,
                        $ReportTemplate.headerOptions.scanType,
                        $ReportTemplate.headerOptions.sourceOrigin,
                        $ReportTemplate.headerOptions.scanDensity,
                        $ReportTemplate.generalOptions.onlyExecutiveSummary,
                        $ReportTemplate.generalOptions.tableOfContents,
                        $ReportTemplate.generalOptions.exectuiveSummary,
                        $ReportTemplate.generalOptions.displayCategories,
                        $ReportTemplate.generalOptions.displayLanguageHash,
                        $ReportTemplate.generalOptions.scannedQueries,
                        $ReportTemplate.generalOptions.scannedFiles,
                        $ReportTemplate.generalOptions.vulnDescriptions,
                        $ReportTemplate.resultsDisplayOption.assignedTo,
                        $ReportTemplate.resultsDisplayOption.comments,
                        $ReportTemplate.resultsDisplayOption.link2online,
                        $ReportTemplate.resultsDisplayOption.resultsDescription,
                        $ReportTemplate.resultsDisplayOption.snippetsMode)


$response = &"support/soap/soap_request.ps1" $session $body $soap_url $soap_action

   $content = New-Object System.Xml.XmlDocument
   $content.LoadXml($response.Content)

$reportID = $content.DocumentElement.SelectSingleNode("//*[local-name() = 'ID']").InnerText   

return $reportID