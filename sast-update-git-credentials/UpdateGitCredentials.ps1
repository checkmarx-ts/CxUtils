######################################################################
#
# UpdateGitCredentials.ps1
#
######################################################################

<#
.SYNOPSIS
A Script To Update CxSAST Project Git Credentials

.DESCRIPTION
This script will update the Git credentials set in a SAST project to use a new git username and password (or PAT).  If no projects to update are specified, it attempts to update all projects.  

Projects can be specified by a comma separated list of SAST project ids or piped to the script from an external source as full project name paths (e.g. "/CxServer/Team/Project").

The SAST user will require team membership that gives visibility to all projects that need to be updated.

If using a PAT for Git repository authentication, the Git username can be set to "git".

Projects that do not have Git settings will not be updated.  Projects that have Git settings will retain the Git repository URL and branch settings.  The Git username/password/token is not verified as valid when set.

By default, the configuration settings are not changed unless the -write flag is included as a command line parameter.

If the 'gitpassword' parameter is not provided, a server-to-PAT mapping can be defined in the 'HostToPATMap.ps1' script.  See the documentation for HostToPATMap.ps1

.PARAMETER server
The URL to the SAST server.

.PARAMETER username
The SAST account username.

.PARAMETER password
The SAST account password.

.PARAMETER gitusername
The Git repo username to use for the Git credentials. Defaults to 'git'

.PARAMETER gitpassword
The password or PAT for accessing the Git repository.

.PARAMETER projectids
A comma separated list of project ids for projects to update.

.PARAMETER write
A flag that, if included, writes the updated credentials to the SAST projects having Git settings.

.PARAMETER output
The name of the log file to output.  A default one will be created if this parameter is not specified.

.INPUTS
An array of SAST project names.  These project names should be the full project path (e.g. /CxServer/Team/Project).

.OUTPUTS
None


.EXAMPLE
.\UpdateGitSettings.ps1 -server "http://localhost" -username "admin" -password "sast_password" -gitusername git -gitpassword "P@$$w0rd!123"

Outputs a log file showing what changes will be made to all projects without changing any settings.

.EXAMPLE
.\UpdateGitSettings.ps1 -server "http://localhost" -username "admin" -password "sast_password"

Outputs a log file showing what changes will be made to all projects without changing any settings.

.EXAMPLE
.\UpdateGitSettings.ps1 -server "http://localhost" -username "admin" -password "sast_password" -gitusername git -gitpassword "P@$$w0rd!123" -projectids "1,2,3" -write

Updates the git credentials for SAST projects with ids 1, 2, and 3.

.EXAMPLE
.\UpdateGitSettings.ps1 -server "http://localhost" -username "admin" -password "sast_password" -gitusername git -gitpassword "P@$$w0rd!123" -write

Updates the git credentials for all SAST projects that have previously been configured with Git settings.


.EXAMPLE
Get-Content project-list.txt | .\UpdateGitSettings.ps1 -server "http://localhost" -username "admin" -password "sast_password" -gitusername git -gitpassword "P@$$w0rd!123" -write

Updates the git credentials for projects with paths specified in the project-list.txt file. The contents of project-list.txt could have a list of
project paths, e.g.:

/CxServer/TeamA/Project1
/CxServer/TeamA/Project2
/CxServer/TeamB/Project1
/CxServer/TeamC/Project1

.EXAMPLE
"/CxServer/Team/Project" | .\UpdateGitSettings.ps1 -server "http://localhost" -username "admin" -password "sast_password" -gitusername git -gitpassword "P@$$w0rd!123" -write

Updates credentials for a single project selected by full project name.

#>

param (
    [string]$server = "http://localhost",
    [Parameter(Mandatory = $true)][string]$username,
    [Parameter(Mandatory = $true)][string] $password,
    [string] $gitusername = "git",
    [string] $gitpassword,
    [string]$projectids = "",
    [Parameter(ValueFromPipeline = $true)][string]$projectnames,
    [switch]$write,
    [string]$output = ".\Git_Credential_Update_Script_Output"
)

begin {

    if ($gitpassword -eq "") {

        if ( (Test-Path "HostToPATMap.ps1" -PathType Leaf) ) {
            . ((Get-Location).Path + "\HostToPATMap.ps1")
            if ($null -eq $patMap) {
                Write-Host "A mapping file named 'HostToPATMap.ps1' must define a hash named '`$patMap'."
                Write-Host "Execution will not continue."
                exit 1
            }

            # URL format function when using a host to PAT mapping
            $gitUrlFunc = {
                param([string]$url)

                foreach ($regex in $patMap.Keys) {

                    $r = [System.Text.RegularExpressions.Regex]::new($regex)
                    if ($r.IsMatch($url) ) {

                        $gitUrl = [System.UriBuilder]::new($url)
    
                        # Url decode is done in case the PAT is URL encoded
                        $gitUrl.UserName = "git"
                        $gitUrl.Password = [System.Web.HttpUtility]::UrlEncode([System.Web.HttpUtility]::UrlDecode($patMap[$regex]))
            
                        return $gitUrl.Uri
                    }
                }
                throw "No token map match for $url"
            }
        }

    }
    else {
        # URL format function when using a single Git username/password (or token)
        $gitUrlFunc = {
            param([string]$url)

            $gitUrl = [System.UriBuilder]::new($url)
    
            # Url decode is done in case the username/pass is given to the script already encoded
            $gitUrl.UserName = [System.Web.HttpUtility]::UrlEncode([System.Web.HttpUtility]::UrlDecode($gitusername))
            $gitUrl.Password = [System.Web.HttpUtility]::UrlEncode([System.Web.HttpUtility]::UrlDecode($gitpassword))

            return $gitUrl.Uri
        }
    }

    function WriteToLogFile($message) {
        Write-Host $message
        $message >> $logFilePath
    }
    

    function getBannerLine($text, $size) {
    
        if ($text.Length -eq 0) {
            return $text.PadLeft($size, '#')
        }
        elseif ($text.Length -gt $size) {
            return $text
        }
        else {
    
            if ($text.Length % 2 -ne 0) {
                $leftAdj = 1
            }
            else {
                $leftAdj = 0
            }
    
            $centerText = [int]($text.Length / 2)
            $offset = [int]$size / 2 - ($centerText + 1)
    
            return "".PadLeft($offset + $leftAdj, '#') + " " + $text + " " + "".PadLeft($offset, '#')
        }
    }


    $basePath = $output

    $timestamp = Get-Date -Format o | ForEach-Object { $_ -replace ":", "." }
    $logFilePath = $basePath + $timestamp + '.txt'


    if ($write -eq $false) {
        WriteToLogFile $(getBannerLine "" 50)
        WriteToLogFile $(getBannerLine "DRY  RUN" 50)
        WriteToLogFile $(getBannerLine "THE -write PARAMETER WAS NOT SPECIFIED" 50)
        WriteToLogFile $(getBannerLine "NO DATA WILL BE CHANGED" 50)
        WriteToLogFile $(getBannerLine "" 50)
    }



    $cxSastServer = [System.UriBuilder]::new($server)
    $cxUsername = $username
    $cxPassword = $password
    $noGitSettings = 0

    function makeUri ([System.UriBuilder] $baseUri, [string] $path) {
        return [System.Uri]::new($baseUri.Uri, $path)
    }

    function getOAuth2Token() {
        $body = @{
            username      = $cxUsername
            password      = $cxPassword
            grant_type    = "password"
            scope         = "access_control_api sast_api"
            client_id     = "resource_owner_sast_client"
            client_secret = "014DF517-39D1-4453-B7B3-9930C563627C"
        }
        try {
            $response = Invoke-RestMethod -uri (makeUri $cxSastServer "cxrestapi/auth/identity/connect/token") -method post -body $body -contenttype 'application/x-www-form-urlencoded'
        }
        catch {
            Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
            Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
            throw "Could not authenticate"
        }
        return $response.token_type + " " + $response.access_token
    }

    function getAllProjects($token) {
        $headers = @{
            Authorization = $token
            Accept        = "application/json;v=2.0"
        }
        try {
            $teamResponse = Invoke-RestMethod -uri (makeUri $cxSastServer "cxrestapi/auth/teams") -method get -headers $headers
            $teamHash = @{}
            foreach ($team in $teamResponse) {
                $teamHash[$team.id] = $team.fullName
            }

            $projResponse = Invoke-RestMethod -uri (makeUri $cxSastServer "cxrestapi/projects") -method get -headers $headers
            $projectByIdHash = @{}
            $projectByNameHash = @{}
            foreach ($project in $projResponse) {
                $name = $teamHash[$project.teamId] + "/" + $project.name
                $projectByIdHash[$project.id] = $name
                $projectByNameHash[$name] = $project.id
            }

            return $projectByIdHash, $projectByNameHash

        }
        catch {
            Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
            Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
            throw "Cannot retrieve all projects"
        }
    }


    function setProjectGitSettings($token, $projectId, $gitRepoUrl, $gitRepoBranch) {
        $headers = @{
            Authorization  = $token
            Accept         = "*/*"
            "Content-Type" = "application/json"
        }
        $body = @{
            url    = $gitRepoUrl
            branch = $gitRepoBranch
        } | ConvertTo-Json

        try {
            Invoke-RestMethod -uri (makeUri $cxSastServer "cxrestapi/projects/${projectId}/sourceCode/remoteSettings/git") -method post -headers $headers -body $body | Out-Null
        }
        catch {
            Write-Host $_.Exception
            Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
            Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        }
    }


    function getProjectGitSettings($token, $projectId) {
        $headers = @{
            Authorization = $token
            Accept        = "application/json;v=1.0"
        }
        try {
            $response = Invoke-RestMethod -uri (makeUri $cxSastServer "cxrestapi/projects/${projectId}/sourceCode/remoteSettings/git") -method get -headers $headers 
            return $response
        }
        catch {
            if ($_.Exception.Response.StatusCode -eq 404) {
                return $null
            }
            Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
            Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
            throw "Error setting Git settings in project with id ${projectId}"
        }
    }


    #generate auth token for checkmarx
    $token = getOAuth2Token
    $projById, $projByName = (getAllProjects $token)


    # determine the target projects
    # all projects are targets if specific project ids have not been set
    $targetProjects = @()

    if ($projectids -ne "") {
        $ids = $projectids.Split(",")
        foreach ($id in $ids) {
            if ($projById.keys -contains $id) {
                $targetProjects += $id
            }
            else {
                WriteToLogFile "Project with id ${id} does not exist."
            }
        }
    }
}


process {
    if ( -not $null -eq $projectnames) {
        foreach ($name in $projectnames) {
            if ($projByName.keys -contains $name) {
                $targetProjects += $projByName[$name]
            }
            else {
                WriteToLogFile "Project with name ${name} does not exist."
            }
        }
    }
}


end {
    if ($targetProjects.Count -eq 0) {

        WriteToLogFile "No project names or ids specified, all projects will be changed."

        $targetProjects = $projById.keys
    }

    foreach ($projectId in $targetProjects) {
        $projectName = $projById[[int]$projectId]

        $projectGitSettings = getProjectGitSettings $token $projectId

        if ($null -eq $projectGitSettings) {
            $noGitSettings += 1
            WriteToLogFile "${projectName} [${projectId}] has no Git settings to change!"
            continue
        }

        WriteToLogFile "${projectName} [${projectId}] Current URL: $($projectGitSettings.url) BRANCH: $($projectGitSettings.branch)"

        try { 
            $gitUrl = &$gitUrlFunc $projectGitSettings.url
            $gitRepoBranch = $projectGitSettings.branch

            if ($true -eq $write) {
                setProjectGitSettings $token $projectId $gitUrl $gitRepoBranch
            }

            WriteToLogFile "${projectName} [${projectId}] updated: $($gitUrl)"
        }
        catch {
            WriteToLogFile $_
            $noGitSettings += 1
        }
    }

    WriteToLogFile ""
    WriteToLogFile "$($targetProjects.Count) projects targetted."
    WriteToLogFile ""
    WriteToLogFile "There were $noGitSettings projects found with no matching Git settings; these have not been updated."
    WriteToLogFile "Complete"
}
