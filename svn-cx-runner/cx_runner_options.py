# Address to root of SVN repo
svn_server = "http://192.168.1.151/svn/myrepo"
# Determines the milestone to D/L. 0 = current, 1 = previous.
milestone_ver = 0
# Use targets files to determine which files to read
use_targets = False
# Directory to create repo copies in
working_dir_raw = "working"
working_dir = ("./" + working_dir_raw)
# Username to log into SVN server with. You will be prompted if you don't specify password.
svn_username = "admin"
svn_password = None
# Name of log file
log_file = "cx_runner_log.json"
# Checkmarx account information. You will be prompted if you don't specify password.
cx_cli_path = "c:\\cx_cli\\runCxConsole.cmd"
cx_server = "http://localhost"
cx_username = "jarmstrong"
cx_password = None
cx_preset = "Default"
# Download Maven dependencies (True | False)
maven_dependencies = True
# Run Checkmarx scan (True | False)
checkmarx_scan = False
# Use clock to count lines of code.
count_loc = True
# Name of clock executable
cloc_prg_name = "cloc.exe"