######## Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password
$presetName = "Test Preset"

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
######## Delete Preset by ID ########
function deletePreset($proxy, $sessionId, $presetId){
    $res = $proxy.DeletePreset($sessionId, $presetId)
    if($res.IsSuccesfull){
        return $res
    } else{
        Write-Host "Failed to Delete Preset ${presetId} : " $res.ErrorMessage
        exit 1
    }
}

$proxy = getProxy $domain
$sessionId = login $proxy $username $password
$presets = getPresets $proxy $sessionId


foreach($preset in $presets){
    $presetId = $preset.ID
    $pName = $preset.PresetName
    if($pName -eq $presetName){
        $presetDeleted = deletePreset $proxy $sessionId $presetId
        Write-Host "Preset ${presetName} deleted with success !"
        break
    }
}