######## Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password
######## File Config ########
$xmlfile = "Queries.xml"

######## Get Proxy ########
function getProxy($domain){
    return New-WebServiceProxy -Uri ${domain}/CxWebInterface/Portal/CxWebService.asmx?wsdl
}
######## Login ########
function login($proxy, $user, $pass){
    $proxyType = $proxy.gettype().Namespace

    $credentials = new-object ("$proxyType.Credentials")
    $credentials.User = $user
    $credentials.Pass = $pass
    $res = $proxy.Login($credentials, 1033) 
    
    if($res.IsSuccesfull){
        return $res.SessionId
    } else{
        Write-Host "Login Failed : " $res.ErrorMessage
        exit 1
    }
}
######## Get All Queries ########
function getQueries($proxy, $sessionId){
    $res = $proxy.GetQueryCollection($sessionId)
    if($res.IsSuccesfull){
        return $res.QueryGroups
    } else {
        Write-Host "Error Retrieving Queries : " $res.ErrorMessage
    }
}

$proxy = getProxy $domain
$sessionId = login $proxy $username $password
$queriesCollection = getQueries $proxy $sessionId

######## Create the XML File Tags ########
$xmlWriter = New-Object System.XMl.XmlTextWriter($xmlfile,$Null)
$xmlWriter.Formatting = 'Indented'
$xmlWriter.Indentation = 1
$XmlWriter.IndentChar = "`t"
$xmlWriter.WriteStartElement("Queries")
$xmlWriter.WriteEndElement()
$xmlWriter.Flush()
$xmlWriter.Close()

######## Create File ########
$xmlDoc = [System.Xml.XmlDocument](Get-Content $xmlfile);

$queriesCustomized = 0
$queryGroups = $queriesCollection

######## Parse Queries ########
foreach($group in $queryGroups){
    $isCustomized = $group.PackageType -eq "Corporate" -OR $group.PackageType -eq "Team" -OR $group.PackageType -eq "Project"
    if($isCustomized){
        $queries = $group.Queries
        $queriesCustomized += $queries.Count
        foreach($query in $queries){
            $queryNode = $xmlDoc.CreateElement("Query")
            $out = $xmlDoc.SelectSingleNode("//Queries").AppendChild($queryNode)
            $out = $xmlDoc.Save($xmlfile)

            $QueryID = $queryNode.AppendChild($xmlDoc.CreateElement("QueryID"));
            $out = $QueryID.AppendChild($xmlDoc.CreateTextNode($query.QueryId));
            $PackageID = $queryNode.AppendChild($xmlDoc.CreateElement("PackageID"));
            $out = $PackageID.AppendChild($xmlDoc.CreateTextNode($query.PackageId));
            $Name = $queryNode.AppendChild($xmlDoc.CreateElement("Name"));
            $out = $Name.AppendChild($xmlDoc.CreateTextNode($query.Name));
            $Cwe = $queryNode.AppendChild($xmlDoc.CreateElement("Cwe"));
            $out = $Cwe.AppendChild($xmlDoc.CreateTextNode($query.Cwe));
            $Severity = $queryNode.AppendChild($xmlDoc.CreateElement("Severity"));
            $out = $Severity.AppendChild($xmlDoc.CreateTextNode($query.Severity));
            $GroupName = $queryNode.AppendChild($xmlDoc.CreateElement("GroupName"));
            $out = $GroupName.AppendChild($xmlDoc.CreateTextNode($group.Name));
            $Source = $queryNode.AppendChild($xmlDoc.CreateElement("Source"));
            $out = $Source.AppendChild($xmlDoc.CreateTextNode($query.Source));
            $IsEncrypted = $queryNode.AppendChild($xmlDoc.CreateElement("IsEncrypted"));
            $out = $IsEncrypted.AppendChild($xmlDoc.CreateTextNode([System.Convert]::ToString($query.IsEncrypted).toLower()));
            $IsReadOnly = $queryNode.AppendChild($xmlDoc.CreateElement("IsReadOnly"));
            $out = $IsReadOnly.AppendChild($xmlDoc.CreateTextNode([System.Convert]::ToString($group.IsReadOnly).toLower()));
            $Version = $queryNode.AppendChild($xmlDoc.CreateElement("Version"));
            $out = $Version.AppendChild($xmlDoc.CreateTextNode($query.QueryVersionCode));
            $IsExecutable = $queryNode.AppendChild($xmlDoc.CreateElement("IsExecutable"));
            $out = $IsExecutable.AppendChild($xmlDoc.CreateTextNode([System.Convert]::ToString($query.IsExecutable).toLower()));
            $PackageTypeName = $queryNode.AppendChild($xmlDoc.CreateElement("PackageTypeName"));
            $out = $PackageTypeName.AppendChild($xmlDoc.CreateTextNode($group.PackageTypeName));
            $PackageType = $queryNode.AppendChild($xmlDoc.CreateElement("PackageType"));
            $out = $PackageType.AppendChild($xmlDoc.CreateTextNode($query.PackageId));
            $LanguageName = $queryNode.AppendChild($xmlDoc.CreateElement("LanguageName"));
            $out = $LanguageName.AppendChild($xmlDoc.CreateTextNode($group.LanguageName));
            $Language = $queryNode.AppendChild($xmlDoc.CreateElement("Language"));
            $out = $Language.AppendChild($xmlDoc.CreateTextNode($group.Language));
        
            $EngineMetadata = $queryNode.AppendChild($xmlDoc.CreateElement("EngineMetadata"));
            $out = $EngineMetadata.SetAttribute("p3:nil", "true")
            $out = $EngineMetadata.SetAttribute("xmlns:p3", "http://www.w3.org/2001/XMLSchema-instance")
            $out = $xmlDoc.Save($xmlfile)
        }
    }
}
Write-Host "Queries Customized Extracted : " $queriesCustomized
    