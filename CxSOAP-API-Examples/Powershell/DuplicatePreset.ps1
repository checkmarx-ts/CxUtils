######## Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password
$presetName = "Test Preset"
$duplicatedPresetName = "Checkmarx Default"


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
######## Duplicate Preset ########
function duplicatePreset($proxy, $sessionId, $username, $presetName, $duplicatedPreset){
    $proxyType = $proxy.gettype().Namespace
    $preset = new-object ("$proxyType.CxPresetDetails")
    $preset.isUserAllowToDelete = $true
    $preset.isUserAllowToUpdate = $true
    $preset.isPublic = $true
    $preset.IsDuplicate = $true
    $preset.name = $presetName
    $preset.owner = $username
    $preset.owningteam = $duplicatedPreset.owningteam
    $preset.queryIds = $duplicatedPreset.queryIds

    $res = $proxy.CreateNewPreset($sessionId, $preset)
    if($res.IsSuccesfull){
        return $res.preset
    } else{
        Write-Host "Failed to Duplicate Preset ${presetName}:" $res.ErrorMessage
        Write-Host "Preset might already exists or Invalid Preset Name"
        exit 1
    }
}
######## Get Presets ########
function getPresets($proxy, $sessionId){
    $res = $proxy.GetPresetList($sessionId)
    if($res.IsSuccesfull){
        return $res.PresetList
    } else{
        Write-Host "Failed to Get Presets : " $res.ErrorMessage
        exit 1
    }
}
######## Get Preset Details ########
function getPresetDetails($proxy, $sessionId, $presetId){
    $res = $proxy.GetPresetDetails($sessionId, $presetId)
    if($res.IsSuccesfull){
        return $res.preset
    } else{
        Write-Host "Failed to Get Preset ${presetId} Details : " $res.ErrorMessage
        exit 1
    }
}

$proxy = getProxy $domain
$sessionId = login $proxy $username $password
$presets = getPresets $proxy $sessionId

foreach($preset in $presets){
    $presetId = $preset.ID
    $pName = $preset.PresetName
    if($pName -eq $duplicatedPresetName){
        $presetDetails = getPresetDetails $proxy $sessionId $presetId
        $presetDeleted = duplicatePreset $proxy $sessionId $username $presetName $presetDetails
        Write-Host "Preset ${presetName} duplicated with success !"
        break
    }
}
