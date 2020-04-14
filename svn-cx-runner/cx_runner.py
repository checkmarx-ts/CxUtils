import svn.remote
import cx_runner_options as cx_opts
import cx_runner_logs as cx_logs
import cx_svn_utils as cx_svn
import cx_maven_utils as cx_maven
import cx_sast_utils as cx_sast
import cx_utils as cx_utils
from getpass import getpass
from datetime import datetime

cx_logs.start_log()
cx_utils.read_cli_opts()
cx_utils.clean_working_dir("")
if cx_opts.svn_password == None:
    print("Please enter the SVN server password.")
    cx_opts.svn_password = getpass()
if cx_opts.cx_password == None:
    print("Please enter the Checkmarx server password.")
    cx_opts.cx_password = getpass()
print("Reading projects from SVN Server")
now = datetime.now()
nowStr = now.strftime("%Y-%m-%d %H:%M:%S")
cx_logs.create_log_entry(msg = "Started sending scans at [{}] from SVN server [{}] to Checkmarx Server [{}]".format(nowStr, cx_opts.svn_server, cx_opts.cx_server))
client = svn.remote.RemoteClient(cx_opts.svn_server, username = cx_opts.svn_username, password = cx_opts.svn_password) 
repo_list = client.list(extended=True)
cx_svn.read_targets_file()
for repo_entry in repo_list:
    if repo_entry["is_directory"] == True and cx_svn.is_project_active(repo_entry['name']):
        print("\nFound Repo: {}".format(repo_entry['name']))
        proj_url, tag_date = cx_svn.find_last_commit_url(repo_entry['name'])
        if proj_url:
            print("    Repo URL: {}".format(proj_url))
            proj = svn.remote.RemoteClient(proj_url, username = cx_opts.svn_username, password = cx_opts.svn_password)
            proj.checkout(cx_opts.working_dir)
            print("    Successfully checked out project.")
            cx_maven.get_maven_deps(repo_entry['name'], tag_date)
            cx_utils.count_lines_of_code(repo_entry['name'], tag_date)
            cx_sast.run_scan(repo_entry['name'], tag_date)
            cx_utils.clean_working_dir("    ")
now = datetime.now()
nowStr = now.strftime("%Y-%m-%d %H:%M:%S")
cx_logs.create_log_entry(msg = "Finished sending scans at [{}] from SVN server [{}] to Checkmarx Server [{}]".format(nowStr, cx_opts.svn_server, cx_opts.cx_server))
cx_logs.write_log()
print("\nFinished!")