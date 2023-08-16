# Checkmarx Professional Services Utilities

This is a curated set of utilities maintained by Checkmarx Professional Services and made available for public consumption.  This is a collection of scripts, tutorials, source code, and anything else that may be useful for use in the field by Checkmarx employees or customers.

**To report issues or obtain help with any of the utilties in this repository, please engage Checkmarx Professional Services.**


## The List

Project | Description
--------|------------
[CheckPotentialFoldersFilesExclusions](CheckPotentialFoldersFilesExclusions) | For purposes of Project configuration tuning at large scale for all projects scanned, it was created this Powershell script that goes over the CxSrc folder and find potential Folders/Files exclusions in order to: Reduce LOC, Reduce Time Scanning and Reduce FPs rate.
[crawl-and-scan](crawl-and-scan) | Crawl a Git repo's commits, scanning each from oldest to latest.
[custom-engine-configs](custom-engine-configs) | SQL stored procedure to create/modify engine configurations
[cx-batch-scan](cx-batch-scan) | PowerShell script that uses CxFlow to scan a comma-separated list of GitHub repositories in a batch mode.
[cx-flow-ado](cx-flow-ado) | Sample CxFlow Docker image for Azure DevOps Pipelines
[cx-jenkins-lib](cx-jenkins-lib) | Jenkins Pipeline shared library example
[cx-sast-scans-analysis](cx-sast-scans-analysis) | Powershell utility to pull scan data / build metrics from a CxSAST instance
[cx-sast-shell-tools](cx-sast-shell-tools) | A collection of powershell scripts that use the SAST APIs to perform business functions
[cx-sca-search](cx-sca-search) | Tool to search for a given open-source library name in the results of prior Checkmarx SCA scans. This search tool complements the search capability in the current SCA results User Interface, which limits searches to the current scan.
[CxFlowDemoInstance](CxFlowDemoInstance) | Scripting to create a full path demonstration environment for Cx-Flow on your local machine in under 10 minutes.
[cxgit](cxgit) | Powershell utility designed to help answer the question "I have XXX repositories, how many CxProjects do I need"?
[CxPythonTools](CxPythonTools) | Checkmarx Python tools
[cxsast-report-redaction](cxsast-report-redaction) | Utility to redact the CxSAST PDF reports by keeping only the first page of metadata.
[cxsast_engine_cleanup](cxsast_engine_cleanup) | Batch file designed to cleanup scans & logs from CxSAST engine servers 
[cxsast_mass_testscan](cxsast_mass_testscan) | This repository has scripts for scanning using CxFlow or CxCLI.  The scripts ingest a text file of public git repos. 
[CxSASTRestApiExample](CxSASTRestApiExample) | This powershell template demonstrates how to use the Checkmarx SAST REST API endpoints using token authentication.
[CxSeverityOverride](CxSeverityOverride) | A python based utility that would allow the user to change the severity of the query, package type of the query and/or add the query to multiple presets at the same time.
[CxSOAP-API-Examples](CxSOAP-API-Examples) | Checkmarx SOAP API Examples (8.X versions)
[data-retention](data-retention) | Controls (Starts & Stops) data retention.  Given the URL of a specific Checkmarx web interface, starts a data retention by deleting either all scans within a specified date range or all but the last X scans for each project.
[data-retention-clean-orphaned-src](data-retention-clean-orphaned-src) | Cleans up orphaned source folders in CxSrc
[engineering-health-check](engineering-health-check) | Powershell scripts that run the odata query used for Engineering Health Checks
[force-scans](force-scans) | Powershell script that submits forced scans from a list of projects mapped to source code in CxSrc via a CSV file
[installAndRun-CxConsole](installAndRun-CxConsole) | Powershell script to auto-download and execute the Checkmarx CLI
[JenkinsDemoInstance](JenkinsDemoInstance) | Using Docker desktop, create an instance of Jenkins running under selected versions of the JDK.  Standalone and master/agent configurations are supported.  Settings are persisted in a local directory so that configurations are not lost when the Docker container is stopped.
[LinuxEngineInstall](LinuxEngineInstall) | A script that will download the linux engine(currently from 9.3 installer) update the server.env with values provided by user, start docker and run the engine on Amazon Linux.
[multi-repo-whitelist-scan](multi-repo-whitelist-scan) | Script to clone multiple git repos, remove unrecognized file types, and scan as one project using the CxCLI from a linux bash shell
[perfmon](perfmon) | This script makes it easy to get up and running with Perfmon to monitor your Checkmarx infrastructure
[post-scan-email-any-report](post-scan-email-any-report) | Scripts for a post-scan action that allows email distribution lists to be defined in the post-scan action configuration rather than embedded in a script.
[sast-update-git-credentials](sast-update-git-credentials) | Enables setting Git credentials on all or selected SAST projects.
[svn-cx-runner](svn-cx-runner) | Utility that iterates through SVN repo, downloads Maven dependencies and creates Checkmarx projects.
[TruffleHogCxQL](TruffleHogCxQL) | A port of the TruffleHog secrets detector.  It finds potential secrets through Regular Expression matches and High Entropy string detection.
[user-type-migration](user-type-migration) | A process to generate SQL Statements to migrate from one user type to another (e.g. LDAP to SAML)
[WindowsNoRDP](WindowsNoRDP) | A script that will configured the ability to log into a server's desktop using VNC over HTTP.  Primarily made to facilitate access to Checkmarx training VMs, this is useful in situations where RDP port 3389 access to a training instance may be blocked by a corporate firewall.
[modify-preset](modify-preset) | A PowerShell Script to update an existing preset with a new one across all projects