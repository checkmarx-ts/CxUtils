

function setupDebug ([boolean]$dbg){

    if ($true -eq $dbg) {
        $global:DebugPreference = "Continue"
    }
    else {
        $global:DebugPreference = "SilentlyContinue"
    }

}