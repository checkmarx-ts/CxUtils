# CxApplicationScanner1.py

## Checkmarx Application 'Scanner' Tool #1

This is Python tool to create an application zip file and scan it via the Rest API.

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

6) Make sure you have the latest version of 'zope.interface'. From a 'elevated' (Admin) command prompt, 
   run: pip install zope.interface

5) Make sure you have the latest version of 'requests_toolbelt'. From a 'elevated' (Admin) command prompt, 
   run: pip install requests_toolbelt

7) On Windows:

       a) The following 'extra' pip install commands may need to be issued:
           pip install python-interface
           pip install tqdm
           pip install opencv-python

8) Download the 'CxApplicationScanner1.zip' (zip) file and extract it to a subdirectory (on the Checkmarx POC/Manager machine).

9) In a 'normal' command prompt, CD into the tool directory (containing the 'CxApplicationScanner1.py' file). 
   Run: python CxApplicationScanner1.py --help 

   This should display 'help' like the following:

        CxApplicationScanner1.py (v1.0111): The Checkmarx Application 'scanner' via Rest API #1
        is starting execution from Server [DRCMBP3-4.local] on [2019/11/11 at 10:09:08] under Python [v3.7.3]...

        Usage: CxApplicationScanner1.py [options]

        Options:
          -h, --help            show this help message and exit
          -v, --verbose         Run VERBOSE
          -r, --recursive       Search Directory PATHS recursively
          -c, --case-sensitive  Search Directory PATHS with case-sensitivity
          -d DIRECTORY-of-Files-to-Process, --data-directory=DIRECTORY-of-Files-to-Process
                                Directory with file(s) to process
          -p FILE-PATTERNS, --file-patterns=FILE-PATTERNS
                                File 'patterns' to search for (semicolon delimited)
                                [default is '*.properties']
          --url=Checkmarx-Server-URL
                                Checkmarx Server URL - Protocol/Host/Port - sample:
                                --url=http://hostname:8080
          --user=Checkmarx-UserId
                                Checkmarx Authentication UserId
          --pswd=Checkmarx-Password
                                Checkmarx Authentication Password
          -o OUTPUT_SCANNER_FILE, --output-scanner-file=OUTPUT_SCANNER_FILE
                                (Output) Scanner 'report' file [generated]
          -w APP_WORK_DIR, --app-work-dir=APP_WORK_DIR
                                Application 'work' directory [generated to - MUST be
                                Empty]
          --git-user=Git-UserId
                                Git (authentication) UserId
          --git-pswd=Git-Password
                                Git (authentication) Password

## Extra Setup instructions

--- Commands used by the Tool ---

1) The tool requires the use of a 'zip' command:

    a) For Windows, this is 7-zip: 

       Install the '7z' command and make sure that it is in the PATH used by the command prompt.

    b) For *Nix (Linux/Mac), this is the builtin 'zip' command.

       Make sure that 'zip' can be issued in a command prompt and that the system finds the executable.

## Operation

--- How to run the Tool ---

1) In order to have the 'plist' control file (required by CxApplicationScanner1.py) to provide it the 
   'Application' information needed to create and scan a zip file, the tool 'CxTFSGetAllProjects1.py'
   MUST have been run first to produce these control files (see 'CxTFSGetAllProjects1_README.md').

2) In a 'normal' command prompt, CD into the tool directory (containing the 'CxApplicationScanner1.py' file).
   You MUST create an (empty) 'working' directory for the tool to generate the .zip file to be scanned.

   Run: 
       python CxApplicationScanner1.py
       -v 
       --url protocol://<Checkmarx-hostname-or-IP>:<port#>
       --user <name (Checkmarx)> 
       --pswd <password (Checkmarx)>
       -o CxApplicationScanner1_report.txt 
       -d Generated_App_Plists
       -p "App-Project_1.plist" 
       -w ./AppScanner_WorkDir 
       --git-user <name (Git)>
       --git-pswd <password (Git)>
       > CxApplicationScanner1.ot1_10042019.log 2>&1 

   Where: 
       a) The command can all be on one line. It's broken out to separate lines here to make it easier to read.
       c) The --url needs to be updated to point to your Checkmarx host (by DNS name or IP). Like 'https://192.168.2.190:8080'.
       d) The --user is your Checkmarx User name (aka, ID).
       e) The --pswd is your Checkmarx (User) password.
       f) The -o is the output 'report' file to be generated.
       g) The -d is an existing directory where the generated Project (App) 'plist' files were written out to.
       h) The -p is the filename of the generated Project (App) 'plist' to be scanned.
       i) The -w is an existing (empty) directory where the generated Project (App) zip file will be created.
       j) The --git-user is your Git User name (aka, ID).
       k) The --git-pswd is your Git (User) password.

   Then:
       a) Zip up and send back the files 'CxApplicationScanner1_report.txt' and 'CxApplicationScanner1.ot1_10042019.log' and
          add all of the generated contents in the 'AppScanner_WorkDir' directory.

## Future Enhancements

--- Extra capability ---

1) Add support to put (TFS) URL/User/PAT into a config file and bypass the command line input.

