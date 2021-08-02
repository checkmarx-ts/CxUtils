# SAST Repository History Scanner

This project will start scanning the code in a repository on a specified branch from the first commit up until the latest commit.  Originally this was made to populate enough data in a SAST system to demonstrate analysis with CxAnalytix.  There may be many more applications for this type of operation.

It currently executes a scan in a Docker image with Maven, NPM, .Net Core SDK 3.1, Python 3, and Python 2.7 installed.  It will execute both a SAST and an OSA scan for each selected commit for a selected branch of a selected repository.

# How it Works

## Build the Docker Image

`docker build -t repocrawl .`

The image builds from the (CxCLI-Docker)[https://github.com/checkmarx-ts/CxCLI-Docker] base image.

## Run the Docker Image

This command executes the crawler image using the environment variables set in `env_squirrelmail`.  

`docker run -it --env-file env_squirrelmail repocrawl`

The environment file might look like:

```
GIT_URL=https://github.com/RealityRipple/squirrelmail.git
CX_USER="<username>"
CX_PASSWORD="<password>"
CX_SERVER="<server>"
CX_PROJECT="CxServer/squirrelmail"
HASH_STEP=7
```

# Environment Variables

The image execution is controlled by the environment variables listed below.


|Variable|Required|Default|Description|
|-|-|-|-|
|`CX_PASSWORD`|Y|None|The password for the matching CX_USER value.|
|`CX_PRESET`|N|All|The preset to use while scanning.|
|`CX_PROJECT`|Y|None|The name of the project in the form of `/<team path>/<project name>`.|
|`CX_SERVER`|Y|None|The CxSAST server URL.|
|`CX_USER`|Y|None|The CxSAST user account.|
|`GIT_URL`|Y|None|The Git clone URL.|
|`HASH_STEP`||N|10|The number of commits to skip between each commit.|
|`START_HASH`|N|None|The hash value of the commit to start the crawl.  Set to the last hash scanned and it will start scanning at the next commit hash.|
|`TARGET_BRANCH`|N|master|The name of the branch to crawl in the repository specified by GIT_URL.|

# Operational Specifics

Some projects may have a large number of small commits.  In this case, a larger value for `HASH_STEP` may be better than smaller values.

You can run multiple instances of the container concurrently to scan different projects using separate environment files.

Each scan is given a comment with the commit hash corresponding to the code being scanned.  This allows you to specify `START_HASH` to continue the crawl if it is interrupted.
