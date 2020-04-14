# Checkmarx Professional Services Power Hacks

This is a curated set of hacks maintained by the Checkmarx Professional Services and made available for public consumption.  This is a collection of scripts, tutorials, source code, and anything else that may be useful for use in the field by Checkmarx employees or customers.

## The List

Project | Description
--------|------------
[CheckPotentialFoldersFilesExclusions](CheckPotentialFoldersFilesExclusions) | For purposes of Project configuration tuning at large scale for all projects scanned, it was created this Powershell script that goes over the CxSrc folder and find potential Folders/Files exclusions in order to: Reduce LOC, Reduce Time Scanning and Reduce FPs rate.
[CxFlowDemoInstance](CxFlowDemoInstance) | Scripting to create a full path demonstration environment for Cx-Flow on your local machine in under 10 minutes.
[JenkinsDemoInstance](JenkinsDemoInstance) | Using Docker desktop, create an instance of Jenkins running under selected versions of the JDK.  Standalone and master/agent configurations are supported.  Settings are persisted in a local directory so that configurations are not lost when the Docker container is stopped.
[TruffleHogCxQL](TruffleHogCxQL) | A port of the TruffleHog secrets detector.  It finds potential secrets through Regular Expression matches and High Entropy string detection.
[WindowsNoRDP](WindowsNoRDP) | A script that will configured the ability to log into a server's desktop using VNC over HTTP.  Primarily made to facilitate access to Checkmarx training VMs, this is useful in situations where RDP port 3389 access to a training instance may be blocked by a corporate firewall.
[CxSeverityOverride](CxSeverityOverride) | A python based utility that would allow the user to change the severity of the query, package type of the query and/or add the query to multiple presets at the same time.
[cx-flow-ado](cx-flow-ado) | Sample CxFlow Docker image for Azure DevOps Pipelines
[cx-sast-scans-analysis](cx-sast-scans-analysis) | Powershell utility to pull scan data / build metrics from a CxSAST instance
[cx-sca-search](cx-sca-search) | Tool to search for a given open-source library name in the results of prior Checkmarx SCA scans. This search tool complements the search capability in the current SCA results User Interface, which limits searches to the current scan.
[cx-jenkins-lib](cx-jenkins-lib) | Jenkins Pipeline shared library example
[svn-cx-runner](svn-cx-runner) | Utility that iterates through SVN repo, downloads Maven dependencies and creates Checkmarx projects.
[CxSOAP-API-Examples](CxSOAP-API-Examples) | Checkmarx SOAP API Examples (8.X versions)
