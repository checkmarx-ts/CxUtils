# cxgit 
Powershell utility designed to help answer the question "I have XXX repositories, how many CxProjects do I need"?

The concept is that it will quiz Gitlab, Github or BitBucket via API for a list of repos associated with the Personal Access Token.  It then clones each repo and runs the CLOC tool against it. The CLOC tool should reside in the local directory, and if it is not found the user is asked if the script is allowed to download it.

There IS housekeeping, and after the CLOC tool completes the directory is deleted.



# Prerequisites
* Git installed
* Microsoft Excel
* Powershell
* Windows Operating System


# Usage

The script writes a simple CSV file of project name & GIT URL for each repo. It then clones each repo in turn and runs the CLOC tool, extracting languages used and LOC. This is then written to a separate CSV. The script has a list of languages it is interested in and e.g. will not count XML, JSON files.

There is a spreadsheet that will consume the results and list the number of Cx Project licenses required to support the repos scanned, using the metric of 10 MS (<20KLOC) per Cx Project license. The Excel data source needs to be manually refreshed.

This WILL potentially take a long time to run, so I would leave it running overnight 😊

* Open Powershell and run the following commands

```
git clone https://github.com/checkmarx-ts/CxUtils.git
move .\CxUtils\cxgit C:\
cd C:\cxgit
.\scan_all_repos.ps1

```
* Choose your repository type and enter your Personal Access Token
* Once Excel opens, click Data>Refresh All and save the file

Note:  You will need to enter your username and token in the windows credential pop-up for GitLab

# Authors
Andrew Thoompson, Sales Engineering - Initial work
Sam Quakenbush, Sam Quakenbush - Readme

# License
This project is licensed under TBD

# Updates
Added some missing languages
Changed GitHub REST API to use Org instead of User
