<#
    Checkmarx CxSAST Batch Scan Initiator. Delegates to the CxFlow (https://github.com/checkmarx-ltd/cx-flow) to run scans.
    Checkmarx Professional Services

    Usage: .\cx-batch-scan.ps1 -if {repo-list.csv} [-of {results.csv}] [-config {application.yml}] [-async]

    Parameters:
    -if {repo-list.csv} comma-separated file of GitHub repos to process; at the minimum repo name and URL should be specified; 
                        branch is optional; master is assumed. 
    -of {results.csv}   (optional) results file, where each repo will be marked as success or failure, without extra info output 
    -config {application.yml} (optional) yml configuration file to pass to CxFlow; application.yml is used by default 
    -async              (optional) specify to run scans asynchronously; be careful, as it could overwhelm the CxSAST instance
    -maxScans {N}       (optional) limit processing to the fist N rows; use for debugging or to run in chunks
    
    The CxFlow .yml configuration file needs to be updated with valid CxSAST base URL, credentials, and team information, 
    as well as Guthub information.  CxSAST projects will be named based on RepoName column + branch, e.g., "MyRepo_develop".
    Team designation follows CxFlow rules.
    
    The script expects cx-flow-1.6.2.jar to be located in the working folder.  Modify the path below if it is different, 
    or if running on Java 11. 
#>

param (
    [Parameter(Mandatory=$true)]
    [ValidateScript({
        if( -Not ($_ | Test-Path) ){
            throw "File or folder does not exist"
        }
        return $true
    })]
    [System.IO.FileInfo]$if,

    [Parameter(Mandatory=$false)]
    [System.IO.FileInfo]$of,

    [Parameter(Mandatory=$false)]
    [String]$config = './application.yml',

    [switch]$async,

    [Parameter(Mandatory=$false)]
    [UInt16]$maxScans = [UInt16]::MaxValue
)

[System.IO.FileInfo]$cxflow_executable = 'cx-flow-1.6.2.jar' 

# Construct base command to run 
[String]$console_command_base = "java -jar " + $cxflow_executable.FullName + " --spring.config.location=" + $config + " --scan --github"

try {
    # check if we need to write success/fail to a file
    [bool]$keep_records = $false
    if($of.FullName.Length -gt 0) {
        $keep_records = $true
        $message = "RepoName,RepoURL,Branch,CxProject,Result"
        $message | Out-File -FilePath $of.FullName
    }

    # Read the input file and convert from CSV
    [PSCustomObject]$repoList = Get-Content $if | Out-String | ConvertFrom-Csv
    [String] $message = "Processing " + $if + ". Total repos: " + $repoList.Length
    Write-Output $message

    # Process each line
    foreach ($repo in $repoList) {
        # Repo URL must be specified
        if($repo.RepoURL.Length -eq 0) {
            if($keep_records) {
                $message = $repo.RepoName + ",Not_Provided,N/A,N/A,N/A"
                $message | Out-File -FilePath $of.FullName -Append
            }
            $message = "Repo URL is not set .. skipping."
            Write-Output $message
            continue    
        }

        [uri]$repo_url = $repo.RepoURL
        $message = "Processing " + $repo.RepoURL
        Write-Output $message

        # Set branch to be master, unless specified otherwise
        [string]$branch = 'master'
        if($repo.Branch.Length -gt 0) {
            $branch = $repo.Branch;
            Write-Debug ("Using provded branch " + $repo.branch)
        } 

        # Use RepoName as the base for the project name
        [string]$project = $repo.RepoName;
        if($project.Length -eq 0) {
            # if not provided, use repo URL to derive name
            # expect: https://github.com/namespace/repo.git
            # convert to namespace_repo
            # first, extract /namespace/repo.git
            $project = $repo_url.LocalPath
            if($project.StartsWith('/')) {
                # remove leading /
                $project = $project.Substring(1);
            }
            # discard .git
            $project = $project.Split('.')[0]
            # replace / with _
            $project = $project.Replace('/','_')
        }

        # add branch to form Cx project name
        $project = $project + '_' + $branch
        Write-Debug ("Using " + $project + " as Cx project name")

        [string]$command = $console_command_base + ' --repo-url=' + $repo_url.ToString() + ' --branch=' + $branch + ' --cx-project=' + $project

        # check if need to run async
        if($async) {
            Write-Debug "Running asynchronous scan"
            $command += " --bug-tracker=NONE"
        }
        
        # use unique log file for this scan
        $command += " --logging.file.name=cx-flow-" + $project +".log"

        $global:LASTEXITCODE = 0
        try {
            Write-Output ("Executing: " + $command)
            Invoke-Expression -Command $command > $null
            
            #if scan completed successfully, display results
            if($LASTEXITCODE -eq 0) {
                $message = $repo_url.ToString() + " scan successful."
            }
            else {
                $message = $repo_url.ToString() + " was not submitted successfully. Exit code: " + $LASTEXITCODE + ".."
            }
            Write-Output $message
        }
        catch {
            #TODO: Output more detailed diagnostics based on return code
            Write-Error "Exception executing scan!"
            Write-Error "Exception: $($_.Exception.Message)"
        }

        if($keep_records) {
            $message = $repo.RepoName + "," + $repo_url.ToString() + "," + $repo.branch + "," + $project + "," + $LASTEXITCODE
            $message | Out-File -FilePath $of.FullName -Append
        }

        $maxScans--;
        if($maxScans -lt 0) {
            Write-Output "Reached max scans .. exiting"
            break
        }
    }
}
finally {

}

