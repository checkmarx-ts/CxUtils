# CxProjectCreator3.py

## Checkmarx Project/Branch 'Creator' Tool #3

This is Python tool to create an application with optional brances as project(s) in Checkmarx via the Rest API.

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

7) On Windows:

       a) The following 'extra' pip install commands may need to be issued:
           pip install python-interface
           pip install tqdm
           pip install opencv-python

       b) In the Python installation directory the 'interface' package

           <Python-installation-directory>\Lib\site-packages\interface

          This directory may be named with an upper-case 'I' as 'Interface',
          if it is, rename it to 'interface' (lower-case 'i').

8) Download the 'CxProjectCreator3_1.zip' (zip) file and extract it to a subdirectory (on the Checkmarx POC/Manager machine).

9) In a 'normal' command prompt, CD into the tool directory (containing the 'CxProjectCreator3.py' file). 
   Run: python CxProjectCreator3.py --help 

   This should display 'help' like the following:

        CxProjectCreator3.py (v1.0403): The Checkmarx Project 'creation' via Rest API #3 is starting execution from Server [DRCMBP3-4.local] on [2019/11/22 at 15:08:35] under Python [v3.7.3]...

        Usage: CxProjectCreator3.py [options]

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
          -o OUTPUT_CREATION_FILE, --output-creation-file=OUTPUT_CREATION_FILE
                                (Output) Creation 'report' file [generated]

## Operation

--- How to run the Tool ---

1) In a 'normal' command prompt, CD into the tool directory (containing the 'CxProjectCreator3.py' file).

   Run: 
       python CxProjectCreator3.py
       -v 
       --url protocol://<Checkmarx-hostname-or-IP>:<port#>
       --user <name (Checkmarx)> 
       --pswd <password (Checkmarx)>
       -o CxProjectCreator3_report.txt 
       -d App_Plists
       -p "App-Project_1.plist" 
       > CxProjectCreator3.ot1_11222019.log 2>&1 

   Where: 
       a) The command can all be on one line. It's broken out to separate lines here to make it easier to read.
       c) The --url needs to be updated to point to your Checkmarx host (by DNS name or IP). Like 'https://192.168.2.190:8080'.
       d) The --user is your Checkmarx User name (aka, ID).
       e) The --pswd is your Checkmarx (User) password.
       f) The -o is the output 'report' file to be generated.
       g) The -d is an existing directory where the Project (App) 'plist' files are stored in.
       h) The -p is the filename of the Project (App) 'plist' to use to create Checkmarx Project(s)/Branch(s).

   Then:
       a) Zip up and send back the files 'CxProjectCreator3_report.txt' and 'CxProjectCreator3.ot1_11222019.log'.

