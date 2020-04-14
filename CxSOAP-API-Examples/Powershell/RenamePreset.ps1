######## Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password
$oldPresetName = "Test Preset"
$newPresetName = "Test Preset 123"

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
######## Rename Preset by ID ########
function renamePreset($proxy, $sessionId, $oldPreset, $newPresetName){
    $proxyType = $proxy.gettype().Namespace
    $preset = new-object ("$proxyType.CxPresetDetails")
    $preset.isUserAllowToDelete = $oldPreset.isUserAllowToDelete
    $preset.isUserAllowToUpdate = $oldPreset.isUserAllowToUpdate
    $preset.isPublic = $oldPreset.isPublic
    $preset.IsDuplicate = $oldPreset.IsDuplicate
    $preset.id = $oldPreset.id
    $preset.name = $newPresetName
    $preset.owner = $oldPreset.owner
    $preset.owningteam = $oldPreset.owningteam
    $preset.queryIds = $oldPreset.queryIds

    $res = $proxy.UpdatePreset($sessionId, $preset)
    if($res.IsSuccesfull){
        return $res
    } else{
        Write-Host "Failed to Rename Preset ${presetId} to ${newPresetName} : " $res.ErrorMessage
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
    if($pName -eq $oldPresetName){
        $presetDetails = getPresetDetails $proxy $sessionId $presetId
        $presetRenamed = renamePreset $proxy $sessionId $presetDetails $newPresetName
        Write-Host "Preset ${oldPresetName} was updated to ${newPresetName} with success !"
        break
    }
}