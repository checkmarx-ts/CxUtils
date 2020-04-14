Description
-----------

The script was originally developed for a client with custom SVN use case.

The script does the following:

1. Connects to a target folder on an SVN server and interates through the 
folders found there. 
2. Each found folder is downloaded into a working folder. The latest version 
of the SVN project will be checked out by looking at the tags in the targets 
'tags' folder. Only tags with an M in them are considered milestones and the 
latest release date will be the target used. Currently two tag formats are 
supported:

   // Format 1, the 2019.10.05 represents the milestone date and proceeds the -M.
   2019.10.05-M20500622-01

   // Format 2, 20191123 represents the milestone date and follows the M
   2019.1100.0-M20191123-01
	
3. If a POM file is in the folder than Maven is used to download the source 
files for all of the dependencies.
4. The contents of the SVN folder and the Maven dependencies are sent to a 
Checkmars server for processing. The Checkmarx project will have the same name 
as the SVN folder and if the project already exists a new scan will be 
initiated for the existing project.
5. Finally, after the scan is complete the working folder will be deleted before
the script moves on to the next SVN folder. 

The script creates a JSON log file with comprehesive information each of the 
steps performed on every target found. Except for the script start and finish
logs the entries for each target will always be grouped together. You can use
the information to generate reports about success and failures as well how many
lines of code were found in each target. The general format of each log entry
looks like this:

   {
     // Either "success" or "error"
     "status": "success",
     // The name describe the target being examined
     "name": "",
     // The calculated release date determined by looking at the tag
     "release_date": "",
     // How many files were found in the target
     "files_count": 0,
     // How many comment lines were found
     "comment_lines": 0,
     // How many blank lines were found in the project
     "blank_lines": 0,
     // How many lines of code were found
     "code_lines": 0,
     // The toal of all comment + blank + code lines
     "total_lines_count": 0,
     // A message the describes exactly what this log entry is (see the legend below)
     "msg": "A message"
    }

The following messages can be found in the JSON log entries:

   "Started sending scans at [{}] from SVN server [{}] to Checkmarx Server [{}]"

   "Finished sending scans at [{}] from SVN server [{}] to Checkmarx Server [{}]"

   "Target list activated, reading (targets.txt)."

   "Found project {} in SVN but skipping it because its not in (targets.txt).".format(project)

   "Target list is NOT active, all projects will be processed."

   "Counted projects LOC."

   "Encountered unknown SVN tag datetime format [{}]"

   "Found release version for SVN project [{}] with release date [{}]."

   "A current release version could not be determined for SVN project '{}' because a SVN 'tags' folder could not be located!"

   "Maven succesfully downloaded source dependencies for the project [{}] with release date [{}]."

   "Maven encountered error downloading source dependencies for the project [{}] with release date [{}]."

   "Checkmarx encountered scan request error scanning the project [{}] with release date [{}]."

   "Checkmarx encountered and unsuccessful login scanning the project [{}] with release date [{}]."

   "Checkmarx succesfully scaned the project [{}] with release date [{}]."

Command Usage
-------------

To run the script just do this: 

    python cx_runner.py

Normally the script downloads and runs all of the projects found in the SVN 
target but there is an alternative mode that read a file named (targets.txt)
and only execute the targets found in there. The (targets.txt) file a simply
text file with one target per line. To use the targets file do this:

    python cx_runner.py --use_targets

Normally the script sends the most recent script to Checkmarx. You can tell 
the script to send the previous milestone to Checkmarx though. If there isn't
a previous milestone the script will use the current one. To scan the previous
milestone do this:

    python cx_runner.py --milestone_ver=1
    

Configuring svn_cx_runner
-------------------------

The script is configured by customing the following options in (cx_runner_options.py):

svn_server: specifies the address of the SVN server.

milestone_ver: determines the milestone to D/L. 0 = current, 1 = previous.

use_targets: use (targets.txt) file to determine which projects to process.

working_dir_raw: the folder to download the SVN contents to. This folder will be 
automatically created and deleted as the script runs. The folder will be created
inside the svn_cx_runner folder by default.

svn_username: username to log into the SVN server with.

svn_password: password to log into the SVN server with. If this is set to None 
the user will be prompted for the password when the script runs. 

log_file: the name of the file to log the runtime too. This will always be stored 
inside the svn_cx_runner folder.

cx_cli_path: specifies the location of the Checkmarx CLI tool.

cx_server: the address of the Checkmarx server

cx_username: the Checkmarx username to use.

cx_password: password for the Checkmarx server. If this is set to None the user 
will be prompted for the password when the script runs. 

cx_preset: the Checkmarx preset to scan projects with.

maven_dependencies: if True the svn_cx_runner will attempt to download Maven 
dependencies when POM files are found. 

checkmarx_scan: if True then svn_cx_runner wlll attempt to sencd projects to 
Checkmarx.

count_loc: if True then the script will user the cloc utility to count the 
lines of code in the project. 

cloc_prg_name: the location of cloc.exe program. 
