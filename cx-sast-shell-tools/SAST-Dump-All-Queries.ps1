<#

    .SYNOPSIS
        Dumps all CxQL queries currently in the system.

    .DESCRIPTION
        This script is experimental.

        It is currently intended primarily to allow a validation of current CxQL script contents. It produces a file
        "CxQL_queries.xml" containing all of the query CxQL.


    .PARAMETER sast_url
        The URL to the CxSAST instance.

    .PARAMETER username
        The name of the user in the CxSAST system.

    .PARAMETER password
        The password for the user in the CxSAST system.

    .PARAMETER dbg
        (Optional Flag) Runs in debug mode and prints verbose information to the screen while processing. 

#>
param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$sast_url,
    [Parameter(Mandatory = $true)]
    [String]$username,
    [Parameter(Mandatory = $true)]
    [String]$password,
    [Switch]$dbg
)

. "support/debug.ps1"

setupDebug($dbg.IsPresent)

$session = &"support\rest\sast\login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent -soap_login_script "support/soap/audit/login.ps1"

try {
    $response = &"support\soap\audit\getquerycollection.ps1" $session
}
catch {
    throw $_
}
finally {
    $logout = &"support\soap\audit\logout.ps1" $session
    if ($true -ne $logout) {
        Write-Output WARNING - Logout failed.
    }
}

$response | Out-File -Encoding "UTF8" "CxQL_queries.xml"
