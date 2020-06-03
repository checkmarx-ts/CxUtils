# CxTFSGetAllProjects1.py

## Checkmarx TFS 'Get-ALL-Projects' Tool #1

This is Python tool to enumerate a TFS Project(s) structure via the Rest API.

## Beta

This project is still in BETA and has not been officially released.

## Setup instructions

--- How to setup to run the Tool ---

1) Make sure that a version of Python 3 (v3.4+) is installed. You can download Python (for your OS) from: https://www.python.org/downloads/

2) Make sure you have the latest version of 'pip'. From a 'elevated' (Admin) command prompt, 
   run: python -m pip install pip

3) Make sure you have the latest version of 'requests'. From a 'elevated' (Admin) command prompt, 
   run: pip install requests

4) Make sure you have the latest version of 'certifi'. From a 'elevated' (Admin) command prompt, 
   run: pip install certifi

5) Make sure you have the latest version of 'requests_toolbelt'. From a 'elevated' (Admin) command prompt, 
   run: pip install requests_toolbelt

6) Make sure you have the latest version of 'interface'. From a 'elevated' (Admin) command prompt, 
   run: pip install interface

7) Download the 'CxTFSGetAllProjects1.zip' (zip) file and extract it to a subdirectory (on the Checkmarx POC/Manager machine).

8) In a 'normal' command prompt, CD into the tool directory (containing the 'CxTFSGetAllProjects1.py' file). 
   Run: python CxTFSGetAllProjects1.py --help 

   This should display 'help' like the following:

        CxTFSGetAllProjects1.py (v2.0303): The Checkmarx TFS 'Get-ALL-Projects' via Rest API #1
        is starting execution from Server [DRCMBP3-4.local] on [2019/10/01 at 15:58:42] under Python [v3.7.3]...

        Usage: CxTFSGetAllProjects1.py [options]

        Options:
          -h, --help            show this help message and exit
          -v, --verbose         Run VERBOSE
          --collection=TFS-Collection
                                TFS Collection - Default 'DefaultCollection'
          --url=TFS-Server-URL  TFS Server URL - Protocol/Host/Port - sample:
                                --url=http://hostname:8080
          --user=TFS-UserId     TFS Authentication UserId
          --pat=TFS-PAT         TFS Authentication PAT (Personal Access Token)
          -o OUTPUT_REPORT_FILE, --output-report-file=OUTPUT_REPORT_FILE
                                (Output) 'report' file [generated]
          -p OUTPUT_PLISTS_DIR, --output-plists-dir=OUTPUT_PLISTS_DIR
                                (Output) 'plists' directory [generated to]

## Operation

--- How to run the Tool ---

1) In a 'normal' command prompt, CD into the tool directory (containing the 'CxTFSGetAllProjects1.py' file).
   You should also create a 'working' directory to capture the generated Project (App or Application)
   'plist' files (with a 'md' or 'mkdir' command).
   Run: python CxTFSGetAllProjects1.py
                 -v 
                 --collection DefaultCollection
                 --url protocol://<TFS-hostname-or-IP>:<port#>
                 --user <name (TFS)> 
                 --pat <PAT (Personal Access Token) (TFS)>
                 -o CxTFSGetAllProjects1_report.txt
                 -p Generated_App_Plists
                 > CxTFSGetAllProjects1.ot1_10012019.log 2>&1 

   Where: 
       a) The command can all be on one line. It's broken out to separate lines here to make it easier to read.
       b) The --collection is the TFS Collection that you're pulling Project (App) data from.
       c) The --url needs to be updated to point to your TFS host (by DNS name or IP). Like 'https://192.168.2.190:8090'.
       d) The --user is your TFS User name (aks, ID).
       e) The --pat is your TFS PAT (Personal Access Token).
       f) The -o is the output 'report' file to be generated.
       g) The -p is an existing directory where the generated Project (App) 'plist' files are written out to.

   Then:
       a) Zip up and send back the files 'CxTFSGetAllProjects1_report.txt' and 'CxTFSGetAllProjects1.ot1_10012019.log' and
          add all of the generated 'plist' files in the 'Generated_App_Plists' directory.

## Future Enhancements

--- Extra capability ---

1) TFS Project structure is a 'hive'. There will eventually be more Rest calls but the output from this will help that process.
2) Added support to put (TFS) URL/User/PAT into a config file and bypass the command line input.

