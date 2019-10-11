function Output-Stage {
    param ([String]$text)

    Write-Host -ForegroundColor White -BackgroundColor Gray $text
}

$cmdPath = Split-Path -Path $PSCommandPath
$cmdName = Split-Path -Path $PSCommandPath -Leaf

function Restart {
    Start-Process -FilePath powershell.exe -Wait -NoNewWindow -WorkingDirectory $cmdPath -ArgumentList "-Command", "$cmdPath\$cmdName"
}

$chocoLocoData = Get-Command choco.exe -ErrorAction SilentlyContinue

if ($null -eq $chocoLocoData) {
    Output-Stage "Installing Chocolatey"
    Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

    Output-Stage "Re-starting Script with new environment...."
    Restart

    exit
}
else {
    $ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
    if (Test-Path($ChocolateyProfile)) {
        Import-Module "$ChocolateyProfile"
    }
}

Output-Stage "Installing Support Packages via Chocolatey"
choco install -y 7zip python3
refreshenv

$pythonLoc = (Get-Command python -ErrorAction SilentlyContinue).Path
if ($null -eq $pythonLoc) {
    Output-Stage "Restarting to pick up Python path..."
    Restart
}

Output-Stage "Installing numpy"
pip install numpy


Output-Stage "Installing IIS"
DISM /online /enable-feature /all /featurename:IIS-WebServer 

Output-Stage "Enabling Websockets in IIS"
DISM /online /enable-feature /featurename:IIS-WebSockets

Output-Stage "Installing iis-arr via Chocolatey"
choco install -y iis-arr



$tightVNCURL = "https://www.tightvnc.com/download/2.8.23/tightvnc-2.8.23-gpl-setup-64bit.msi"

$noVNCVersion = "1.1.0"
$noVNCURL = "https://github.com/novnc/noVNC/archive/v${noVNCVersion}.zip"
$noVNCPath = "C:\noVNC-${noVNCVersion}"

$webSockifyURL = "https://github.com/novnc/websockify/archive/master.zip"
$webSockifyPath = "c:\websockify-master"

Output-Stage "Installing TightVNC"
Invoke-WebRequest -Uri $tightVNCURL -Method Get -OutFile tightvnc.msi
Start-Process -NoNewWindow -Wait -FilePath msiexec.exe -ArgumentList "/i", "tightvnc.msi", "/quiet", "/norestart", "ADDLOCAL=Server",
"SET_ALLOWLOOPBACK=1", "VALUE_OF_ALLOWLOOPBACK=1", "SET_LOOPBACKONLY=1", "VALUE_OF_LOOPBACKONLY=1", "SET_DISCONNECTACTION=1",
"VALUE_OF_DISCONNECTACTION=1", "SET_RUNCONTROLINTERFACE=1", "VALUE_OF_RUNCONTROLINTERFACE=0", "SET_USEVNCAUTHENTICATION=1",
"VALUE_OF_USEVNCAUTHENTICATION=0"


Output-Stage "Installing noVNC"
Invoke-WebRequest -Uri $noVNCURL -Method Get -OutFile NoVnc.zip
Start-Process -NoNewWindow -Wait -FilePath 7z.exe -ArgumentList "x", "NoVnc.zip", "-oc:\", "-y" 
Copy-Item -Path $noVNCPath\vnc.html -Destination $noVNCPath\index.html


Output-Stage "Installing Websockify"
Invoke-WebRequest -Uri $webSockifyURL -Method Get -OutFile Websockify.zip
Start-Process -NoNewWindow -Wait -FilePath 7z.exe -ArgumentList "x", "Websockify.zip", "-oc:\", "-y" 
schtasks /create /tn "Start Websockify" /sc onstart /ru "NT AUTHORITY\NETWORKSERVICE" /tr "cmd.exe /v:off /s /k 'cd $webSockifyPath&& $pythonLoc -m websockify --web $noVNCPath 8000 localhost:5900'"
schtasks /run /tn "Start Websockify"


Output-Stage "Configuring IIS ARR"
Set-WebConfigurationProperty -Filter "/system.webServer/proxy" -PSPAth "IIS:\sites" -name enabled -Value "true"


Output-Stage "Configuring IIS DefaultAppPool"
&"${env:windir}\system32\inetsrv\appcmd.exe" set apppool DefaultAppPool /autoStart:true /startMode:AlwaysRunning
&"${env:windir}\system32\inetsrv\appcmd.exe" start apppool /apppool.name:DefaultAppPool


Output-Stage "Configuring URL Rewrite Rules"
Output-Stage "-- VNC without trailing slash redirect"
Add-WebConfiguration -Filter "/system.webServer/rewrite/globalRules" -PSPAth "IIS:\sites" -Value @{name = "Bad VNC URL"; stopProcessing = "true" }
Set-WebConfigurationProperty -Filter "/system.webServer/rewrite/globalRules/rule[@name='Bad VNC URL']/match" -PSPAth "IIS:\sites" -name url -Value ".*(vnc)$"
Add-WebConfiguration -Filter "/system.webServer/rewrite/globalRules/rule[@name='Bad VNC URL']/conditions" -PSPAth "IIS:\sites" -Value @{input = "{URL}"; pattern = "/$"; negate = "true" }
Set-WebConfiguration -Filter "/system.webServer/rewrite/globalRules/rule[@name='Bad VNC URL']/action" -PSPAth "IIS:\sites" -Value @{type = "Redirect"; url = "http://{HTTP_HOST}/vnc/" }

Output-Stage "-- VNC Rewrite to Websockify"
Add-WebConfiguration -Filter "/system.webServer/rewrite/globalRules" -PSPAth "IIS:\sites" -Value @{name = "NoVNC Rewrite"; stopProcessing = "true" }
Set-WebConfigurationProperty -Filter "/system.webServer/rewrite/globalRules/rule[@name='NoVNC Rewrite']/match" -PSPAth "IIS:\sites" -name url -Value ".*(vnc/)$"
Add-WebConfiguration -Filter "/system.webServer/rewrite/globalRules/rule[@name='NoVNC Rewrite']/conditions" -PSPAth "IIS:\sites" -Value @{input = "{HTTP_HOST}"; pattern = ".*" }
Set-WebConfiguration -Filter "/system.webServer/rewrite/globalRules/rule[@name='NoVNC Rewrite']/action" -PSPAth "IIS:\sites" -Value @{type = "Rewrite"; url = "http://localhost:8000/" }

Output-Stage "-- VNC Content Rewrite to Websockify"
Add-WebConfiguration -Filter "/system.webServer/rewrite/globalRules" -PSPAth "IIS:\sites" -Value @{name = "NoVNCContent"; stopProcessing = "true" }
Set-WebConfigurationProperty -Filter "/system.webServer/rewrite/globalRules/rule[@name='NoVNCContent']/match" -PSPAth "IIS:\sites" -name url -Value ".*(vnc)(/?.*)$"
Add-WebConfiguration -Filter "/system.webServer/rewrite/globalRules/rule[@name='NoVNCContent']/conditions" -PSPAth "IIS:\sites" -Value @{input = "{HTTP_HOST}"; pattern = ".*" }
Set-WebConfiguration -Filter "/system.webServer/rewrite/globalRules/rule[@name='NoVNCContent']/action" -PSPAth "IIS:\sites" -Value @{type = "Rewrite"; url = "http://localhost:8000{R:2}" }

Output-Stage "-- VNC Websocket Rewrite to Websockify"
Add-WebConfiguration -Filter "/system.webServer/rewrite/globalRules" -PSPAth "IIS:\sites" -Value @{name = "NoVNC Websockify"; stopProcessing = "true" }
Set-WebConfigurationProperty -Filter "/system.webServer/rewrite/globalRules/rule[@name='NoVNC Websockify']/match" -PSPAth "IIS:\sites" -name url -Value ".*(websockify)$"
Add-WebConfiguration -Filter "/system.webServer/rewrite/globalRules/rule[@name='NoVNC Websockify']/conditions" -PSPAth "IIS:\sites" -Value @{input = "{HTTP_HOST}"; pattern = ".*" }
Set-WebConfiguration -Filter "/system.webServer/rewrite/globalRules/rule[@name='NoVNC Websockify']/action" -PSPAth "IIS:\sites" -Value @{type = "Rewrite"; url = "http://localhost:8000/websockify" }

Output-Stage "Resetting IIS"
iisreset

Output-Stage "Complete: Navigate to http://{hostname}/vnc to access the noVNC start page."
