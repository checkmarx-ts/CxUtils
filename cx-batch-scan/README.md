# cx-batch-scan
PowerShell script that uses CxFlow to scan a comma-separated list of GitHub repositories in a batch mode.

# Supported Cx SAST Version
Works with CxSAST 8.9+

# Usage
    .\cx-batch-scan.ps1 -if {repo-list.csv} [-of {results.csv}] [-config {application.yml}] [-async] [-maxScans {N}]

    Parameters:
    -if {repo-list.csv} - comma-separated file of GitHub repos to process; at a minimum, repo name and URL should be specified; branch is optional; master is assumed. 
    -of {results.csv} - (optional) results file, where each repo will be marked as success or failure, without extra info output
    -config {application.yml} - (optional) yml configuration file to pass to CxFlow; application.yml is used by default
    -async - (optional) specify to run scans asynchronously; be careful, as it could overwhelm the CxSAST instance
    -maxScans {N} - (optional) limit processing to the fist N rows; use for debugging or to run in chunks
    
    The CxFlow .yml configuration file needs to be updated with valid CxSAST base URL, credentials, and team information, as well as Guthub information.  CxSAST projects will be named based on RepoName column + branch, e.g., "MyRepo_develop". Team designation follows CxFlow rules.
    
    The script expects cx-flow-1.6.2.jar to be located in the working folder.  Modify the path below if it is different, or if running on Java 11.

# Authors
Igor Matlin, Checkmarx Professional Services - Initial work

# License
This project is licensed under TBD
