<#
.SYNOPSIS
A script that defines a PAT mapping based on Git URL pattern matching.


.DESCRIPTION
This script is used to define a single variable named "$patMap" that contains a key/value pair where:

- The "key" is a regular expression that matches a Git clone URL
- The "value" is a PAT that will be used as the user credential when cloning the Git repository

Executing this script does nothing; it is used by UpdateGitCredentials.ps1 only.  Modify the contents of this script to define your own host to PAT mapping.


.INPUTS
None

.OUTPUTS
None

.LINK
https://www.regular-expressions.info/tutorial.html
https://regex101.com/


.EXAMPLE
>
Apply a PAT for all Git repositories with a matching server name:

$patMap = @{
    "bitbucket.org" = "<bitbucket PAT>"
    "github.com" = "<github PAT>"
    "mygitserver.local" = "<PAT for your enterprise SCM>" 
}


.EXAMPLE
>
Apply a different PAT for Git repositories on the same server that has multiple organizations:

$patMap = @{
    "github.com.org1" = "<github org1 PAT>"
    "github.com.org2" = "<github org2 PAT>"
}

.EXAMPLE
>
Apply a PAT for Git repositories that clone via HTTP, leaving existing SSH credentials unchanged:

$patMap = @{
    "http.*github.com" = "<github PAT>"
}

#>


$patMap = @{
    "bitbucket.org" = "<bitbucket PAT>"
    "github.com" = "<github PAT>"
    "mygitserver.local" = "<PAT for your enterprise SCM>" 
}
