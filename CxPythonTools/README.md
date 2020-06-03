# Checkmarx Python tools

## Code Repository

This code repository contains several Checkmarx tools written in Python.

All tools will display their command 'help':

    > python3.8 <Tool-Name>.py --help

All tools will run under version 3 of Python (Python 3.7+). 
Python (for your OS) can be downloaded from: https://www.python.org/downloads/

Some of the tools have extra Python package requirements. Make sure you have
the latest version of 'pip'. From a 'elevated' (Admin) command prompt, run

    > python3.8 -m pip install pip

If this complains that you already have 'pip' installed but should upgrade, run

    > python3.8 -m pip install --upgrade pip

If the terminal complains that 'python3.8' is not found, try just 'python'.

To apply the required packages, run

    > pip install <package-name>

On Windows, the following 'extra' pip install commands may need to be issued:

    > pip install python-interface
    > pip install tqdm
    > pip install opencv-python

## Tool Functions

--- Tools Listing ---

1) CxProjectCreator#            - Creates Checkmarx Projects/Branches given either .properties or .plist files. 
2) CxProjectStatisticsReporter1 - Creates a Checkmarx Projects 'statistics' report of scans in a single .html file.
3) CxApplicationScanner1        - Runs SAST and/or OSA scans for a Project from Repo(s) defined in a .plist file.
4) CxGitLabGetAllProjects1      - Creates the .plist file(s) for CxApplicationScanner1 from GitLab project(s)/group(s).
5) CxTFSGetAllProjects1         - Creates the .plist file(s) for CxApplicationScanner1 from TFS (Git-based) project(s)/group(s).

* A .plist is a 'properties list' file. Essentially this is an XML rendering of a Dictionary or an Array of Dictionaries.
  This is an XML version of a JSON file.

## Tool #1 Notes (CxProjectCreator#)

1) CxProjectCreator2 - Creates Checkmarx Projects/Branches given .properties files. 
2) CxProjectCreator3 - Creates Checkmarx Projects/Branches given .plist files. 

--- Extra Package requirement(s) ---

Run 'pip install <package-name>' for:

1) zope.interface
2) requests
3) requests_toolbelt

--- Source File(s) for the Tool(s) ---

    --- Commands ---
 1) CxProjectCreator2.py
 2) CxProjectCreator3.py

    --- Classes ---
 3) CxProjectCreation1.py                           
 4) CxProjectCreationCollection1.py                 
 5) CxProjectCreationCollectionCheckmarxDefaults1.py
 6) CxProjectCreationCollectionInterfaceDefaults1.py
 7) CxProjectData1.py                               
 8) CxProjectDataCollectionDefaults1.py             
 9) CxProjectScan1.py                               
10) CxRestAPIProjectCreationBase1.py                
11) CxRestAPIStatistics1.py                         
12) CxRestAPITokenAuthenticationBase1.py            
13) CxServerEndpoint1.py                            
14) DrcDirectoryFileSearch1.py                      

--- Documentation File(s) for the Tool(s) ---

 1) CxProjectCreator3_README.md - Extra Documentation for CxProjectCreator3.

## Tool #2 Notes (CxProjectStatisticsReporter1)

--- Extra Package requirement(s) ---

Run 'pip install <package-name>' for:

1) requests

--- Source File(s) for the Tool(s) ---

   --- Command ---
1) CxProjectStatisticsReporter1.py     

   --- Classes ---
2) CxProjectData1.py                   
3) CxProjectDataCollection1.py         
4) CxProjectDataCollectionDefaults1.py 
5) CxProjectScan1.py                   
6) CxRestAPIProjectStatisticsBase1.py  
7) CxRestAPIStatistics1.py             
8) CxRestAPITokenAuthenticationBase1.py
9) CxServerEndpoint1.py                

--- Documentation File(s) for the Tool(s) ---

1) CxProjectStatisticsReporter1_Tool_Documentation_09102019.pdf   - Documentation in a PDF file.
2) CxProjectStatisticsReporter1_Tool_Documentation_09102019.pages - Base Documentation in a 'pages' file (MacOSX).

## Tool #3 Notes (CxApplicationScanner1)

--- Extra Package requirement(s) ---

Run 'pip install <package-name>' for:

1) zope.interface
2) requests
3) requests_toolbelt

--- Source File(s) for the Tool(s) ---

    --- Command ---
 1) CxApplicationScanner1.py     

    --- Classes ---
 2) CxApplicationScannerGITZipper1.py               
 3) CxApplicationScannerInterfaceZipper1.py         
 4) CxProjectCreation1.py                           
 5) CxProjectCreationCollection1.py                 
 6) CxProjectCreationCollectionCheckmarxDefaults1.py
 7) CxProjectCreationCollectionInterfaceDefaults1.py
 8) CxProjectData1.py                               
 9) CxProjectDataCollectionDefaults1.py             
10) CxProjectScan1.py                               
11) CxRestAPIProjectCreationBase1.py                
12) CxRestAPIStatistics1.py                         
13) CxRestAPITokenAuthenticationBase1.py            
14) CxServerEndpoint1.py                            
15) DrcDirectoryFileSearch1.py                      

    --- Extra Control ---
16) CxExt.txt

--- Documentation File(s) for the Tool(s) ---

1) CxApplicationScanner1_README.md - Extra Documentation for CxApplicationScanner1.

## Tool #4 Notes (CxGitLabGetAllProjects1)

--- Extra Package requirement(s) ---

Run 'pip install <package-name>' for:

1) requests

--- Source File(s) for the Tool(s) ---

   --- Command ---
1) CxGitLabGetAllProjects1.py

   --- Classes ---
2) CxGitLabProjectData1.py                   
3) CxGitLabProjectDataCollection1.py         
4) CxGitLabProjectsRestAPIBase1.py           
5) CxGitLabRestAPITokenAuthenticationBase1.py
6) CxGitLabServerEndpoint1.py                
7) CxRestAPIStatistics1.py                   

## Tool #5 Notes (CxTFSGetAllProjects1)

--- Extra Package requirement(s) ---

Run 'pip install <package-name>' for:

1) requests

--- Source File(s) for the Tool(s) ---

   --- Command ---
1) CxTFSGetAllProjects1.py

   --- Classes ---
2) CxTFSProjectData1.py          
3) CxTFSProjectDataCollection1.py
4) CxTFSProjectsRestAPIBase1.py  
5) CxTFSServerEndpoint1.py       
6) CxRestAPIStatistics1.py       

--- Documentation File(s) for the Tool(s) ---

1) CxTFSGetAllProjects1_README.md - Extra Documentation for CxTFSGetAllProjects1.


