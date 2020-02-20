<#
.SYNOPSIS
    Powershell script to Find Potential Folder/Files exclusions over CxSRC
.DESCRIPTION
    For purposes of Project configuration tuning at large scale for all projects scanned, 
    I’ve created a Powershell script that goes over the CxSrc folder and find potential 
    Folders/Files exclusions in order to:
    - Reduce LOC
    - Reduce Time Scanning
    - Reduce FPs rate
.PARAMETER Path
    The path to the .
.PARAMETER LiteralPath
    Specifies a path to one or more locations. Unlike Path, the value of
    LiteralPath is used exactly as it is typed. No characters are interpreted
    as wildcards. If the path includes escape characters, enclose it in single
    quotation marks. Single quotation marks tell Windows PowerShell not to
    interpret any characters as escape sequences.
#>
Param(
    # Checkmarx Server URL (i.e. https://checkmarx.company.com)
    [Parameter(
        Position = 0,
        Mandatory = $true,
        HelpMessage = "Checkmarx Server URL (i.e. https://checkmarx.company.com)"
    )][string] $cxserver = "http://localhost",
    # Checkmarx Username (i.e. first.last@company.com)
    [Parameter(
        Position = 1,
        Mandatory = $true,
        HelpMessage = "Checkmarx Username (i.e. first.last@company.com)"
    )][string] $cxUsername = "admin@cx",
    # Checkmarx Password
    [Parameter(
        Position = 2,
        Mandatory = $true,
        HelpMessage = "Checkmarx Password"
    )][string] $cxPassword,
    # Checkmarx Source Folder (i.e. D:\CxSrc)
    [Parameter(
        Position = 3,
        Mandatory = $true,
        HelpMessage = "Checkmarx Source Folder (i.e. D:\CxSrc)"
    )][string] $cxSrcFolder,
    # Exclusions file generated (i.e. D:\exclusions.json)
    [Parameter(
        Position = 4,
        Mandatory = $false,
        HelpMessage = "Exclusions file generated (i.e. D:\exclusions.json)"
    )][string] $generatedFile = "exclusions.json"
)

$restEndpoint = $cxserver + "/cxrestapi"
$exclusionFolderList = @(
    "test", # Tests
    "mock", # Tests
    "spec", # Tests
    "unit", # Tests
    "debug", # Tests
    "e2e", #Tests
    "androidTest", # Tests (Android)
    "build", # Build Folders
    "dist", # Build Folders
    "deploy", # Build Folders
    "venv", # Build Folders (Python)
    "maven", # Build Folders
    "gradle", # Build Folders (Android)
    "target", # Build Folders
    "example", # Dead Code
    "sample", # Dead Code
    "bin", # Non-relevant folders
    "gen", # Non-relevant folders
    "docs", # Non-relevant folders
    "proguard", # Non-relevant folders (Android)
    "lint", # Non-relevant folders
    "images", # Non-relevant folders
    "swagger", # Non-relevant folders (Swagger)
    "coverage", # Non-relevant folders
    "generated", # Non-relevant folders
    ".vs", # Non-relevant folders (Visual Studio)
    ".idea", # Non-relevant folders (IntelliJ IDEA)
    ".temp", # Non-relevant folders (Temporary)
    ".tmp", # Non-relevant folders (Temporary)
    ".grunt", # Non-relevant folders (Grunt)
    ".cache", # Non-relevant folders (Cache)
    ".dynamodb", # Non-relevant folders (Dinamo DB)
    ".fusebox", # Non-relevant folders (Fusebox)
    ".serverless", # Non-relevant folders (Serverless)
    ".nyc_output", # Non-relevant folders (NYC)
    ".git", # Non-relevant folders (Git)
    ".github", # Non-relevant folders (Github)
    ".dependabot", # Non-relevant folders (Dependabot)
    ".semaphore", # Non-relevant folders (Semaphore CI)
    ".circleci", # Non-relevant folders (Circle CI)
    ".vscode", # Non-relevant folders (VS Code)
    ".nuget", # Non-relevant folders (CSharp)
    ".mvn", # Non-relevant folders (Maven)
    ".m2", # Non-relevant folders (Maven)
    ".DS_Store", # Non-relevant folders
    ".sass-cache", # Non-relevant folders
    ".gradle", # Non-relevant folders (Android)
    "__pycache__", # Non-relevant folders (Python)
    ".pytest_cache", # Non-relevant folders (Python)
    ".settings", # Non-relevant folders (CSharp)
    "imageset", # Non-relevant folders (IOS)
    "xcuserdata", # Non-relevant folders (IOS)
    "xcshareddata", # Non-relevant folders (IOS)
    "xcassets", # Non-relevant folders (IOS)
    "appiconset", # Non-relevant folders (IOS)
    "xcodeproj", # Non-relevant folders (IOS)
    "framework", # Non-relevant folders (IOS)
    "lproj", # Non-relevant folders (IOS)
    "__MACOSX", # Non-relevant folders (IOS)
    "css", # CSS not supported
    "react", #3rd Party Libraries (React)
    "yui", #3rd Party Libraries
    "node_modules", #3rd Party Libraries (Node JS)
    "jquery", #3rd Party Libraries (JS)
    "angular", #3rd Party Libraries (JS)
    "bootstrap", #3rd Party Libraries (JS)
    "modernizr", #3rd Party Libraries (JS)
    "bower_components", #3rd Party Libraries (Bower)
    "jspm_packages", #3rd Party Libraries (JS)
    "typings", #3rd Party Libraries (Typescript)
    "dojo", #3rd Party Libraries
    "package", #3rd Party Libraries (CSharp)
    "vendor", #3rd Party Libraries (Golang)
    "xjs" #3rd Party Libraries (JS)
)
$exclusionFileList = @(
    "min.js", # 3rd Party Libraries (JS)
    ".spec", # Tests (JS/Typescript/Node JS)
    "test", # Tests
    "mock" # Tests
)

function getOAuth2Token() {
    $body = @{
        username      = $cxUsername
        password      = $cxPassword
        grant_type    = "password"
        scope         = "sast_rest_api"
        client_id     = "resource_owner_client"
        client_secret = "014DF517-39D1-4453-B7B3-9930C563627C"
    }
    
    try {
        $response = Invoke-RestMethod -uri "${restEndpoint}/auth/identity/connect/token" -method post -body $body -contenttype 'application/x-www-form-urlencoded'
        return $response.token_type + " " + $response.access_token
    }
    catch {
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        Write-Host "Could not authenticate - Project Name will not be discovered"
        return $null
    }
}
function getProjectById($id) {
    try {
        $response = Invoke-RestMethod -uri "${restEndpoint}/projects/${id}" -method get -headers $authHeader
        return $response
    }
    catch {
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        Write-Host "Cannot Get Project ${id}"
        return $null
    }
}
function getProjectExcludeSettingsById($id) {
    try {
        $response = Invoke-RestMethod -uri "${restEndpoint}/projects/${id}/sourceCode/excludeSettings" -method get -headers $authHeader
        return $response
    }
    catch {
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        Write-Host "Cannot Get Project ${id} Exclude Settings"
        return $null
    }
}

$exclusions = @()
$cxSrcFolder = $cxSrcFolder.ToLowerInvariant()
if(Test-Path $cxSrcFolder -PathType Container){
    
    $token = getOAuth2Token
    if ($token) {
        $authHeader = @{
            Authorization = $token
        } 
    }
    $children = Get-ChildItem -Path $cxSrcFolder -recurse
    $totalCount = $children.Count
    Write-Host "`nAnalysing ${totalCount} Files/Folders..."

    for ($i = 0; $i -lt $totalCount; $i++) {
        $percentage = [math]::Round(($i / $totalCount) * 100, 2)
        if([math]::Round($percentage, 0) % 5 -eq 0){
            Write-Host "Progress...${i} out of ${totalCount} (${percentage}%)"
            Write-Progress -Activity "Analysing ${i} out of ${totalCount} Files/Folders..." -Status "${percentage}% Complete:" -PercentComplete $percentage
        }
        $child = $children[$i]
        $shortName = $child.PSChildName
        $fullPath = $child.FullName.ToLowerInvariant()
        $projectId = $fullPath.Split("_")[0].Replace("${cxSrcFolder}\", "")
        if ($child.PSIsContainer) {
            # Is Folder
            foreach ($exclusionFolder in $exclusionFolderList) {
                if ($shortName -match $exclusionFolder) {
                    $exclusions += @{
                        projectId = $projectId
                        type      = "folder"
                        shortName = $shortName
                        fullPath  = $fullPath
                    }
                    break;
                }
            }
        }
        else {
            # Is File
            foreach ($c in $child) {
                $shortName = $c.PSChildName
                $fullPath = $c.FullName
                foreach ($exclusionFile in $exclusionFileList) {
                    if ($shortName -match $exclusionFile) {
                        $exclusions += @{
                            projectId = $projectId
                            type      = "file"
                            shortName = $shortName
                            fullPath  = $fullPath
                        }
                        break;
                    }
                }
            }
        }
    }

    ### Group Exclusions per Project IDs
    $finalExclusions = @()
    foreach ($exclusion in $exclusions) {
        $projectId = $exclusion.projectId
        $shortName = $exclusion.shortName
        $fullPath = $exclusion.fullPath
        $type = $exclusion.type
        $addNew = $true
        for ($i = 0; $i -lt $finalExclusions.Count; $i++) {
            if ($finalExclusions[$i].projectId -eq $projectId) {
                $shortNames = @()
                $fullPaths = @()
                $proposedExclusions = $finalExclusions[$i].proposedExclusions
                if ($type -eq "file") {
                    $files = $proposedExclusions.files
                    $shortNames = $files.shortNames
                    $fullPaths = $files.fullPaths
                    if ($fullPaths -notcontains $fullPath) {
                        $finalExclusions[$i].proposedExclusions.files.fullPaths += $fullPath
                    }
                    if ($shortNames -notcontains $shortName) {
                        $finalExclusions[$i].proposedExclusions.files.shortNames += $shortName
                    }
                }
                else {
                    $folders = $proposedExclusions.folders
                    $shortNames = $folders.shortNames
                    $fullPaths = $folders.fullPaths
                    if ($fullPaths -notcontains $fullPath) {
                        $finalExclusions[$i].proposedExclusions.folders.fullPaths += $fullPath
                    }
                    if ($shortNames -notcontains $shortName) {
                        $finalExclusions[$i].proposedExclusions.folders.shortNames += $shortName
                    }
                }
                $addNew = $false
                break
            }
        }
        if ($addNew) {
            if ($token) {
                $project = getProjectById $projectId
                if ($project) {
                    $excludeSettings = getProjectExcludeSettingsById $projectId
                }
            }
            $files = @{
                shortNames = @()
                fullPaths  = @()
            }
            $folders = @{
                shortNames = @()
                fullPaths  = @()
            }
            if ($type -eq "file") {
                $files = @{
                    shortNames = @($shortName)
                    fullPaths  = @($fullPath)
                }
            }
            else {
                $folders = @{
                    shortNames = @($shortName)
                    fullPaths  = @($fullPath)
                }
            }

            $finalExclusions += @{
                projectId          = $projectId
                projectName        = $project.name
                teamId             = $project.teamId
                currentExclusions  = @{
                    folders = @($excludeSettings.excludeFoldersPattern)
                    files   = @($excludeSettings.excludeFilesPattern)
                }
                proposedExclusions = @{
                    files   = $files
                    folders = $folders
                }  
            }
        }
    }

    $finalExclusions = ($finalExclusions | ConvertTo-Json -Depth 99)
    $finalExclusions | Out-File $generatedFile
    Write-Host "`nPotential exclusions TODO:" $exclusions.Count
    Write-Host "File ${generatedFile} was generated !`n"
} else {
    Write-Host "Folder ${cxSrcFolder} does not exists"
}
