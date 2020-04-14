import subprocess
import shutil
import os
import cx_runner_logs as cx_logs
import cx_runner_options as cx_opts

def run_scan(repo_name, tag_date):
    if cx_opts.checkmarx_scan:
        print("    Dispatching scan to Checkmarx.")
        location_path = os.getcwd() + "\\" + cx_opts.working_dir_raw
        
        sast = subprocess.Popen([cx_opts.cx_cli_path, 
                                    "Scan",
                                    "-v",
                                    "-CxServer",
                                    cx_opts.cx_server,
                                    "-projectName",
                                    "\"CxServer\\{}\"".format(repo_name),
                                    "-CxUser",
                                    cx_opts.cx_username,
                                    "-CxPassword",
                                    cx_opts.cx_password,
                                    "-Locationtype",
                                    "folder",
                                    "-locationpath",
                                    location_path,
                                    "-Preset",
                                    cx_opts.cx_preset],
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            bufsize=0)
        sast.stdin.close()
        status = True
        for line in sast.stdout:
            if "Scan progress request failure" in line:
                status = False
                msg = "Checkmarx encountered scan request error scanning the project [{}] with release date [{}].".format(repo_name, tag_date)
                cx_logs.create_log_entry(status = "error", msg = msg, name = repo_name, release_date = tag_date)
                print("    " + msg)
            elif "Unsuccessful login" in line:
                status = False
                msg = "Checkmarx encountered and unsuccessful login scanning the project [{}] with release date [{}].".format(repo_name, tag_date)
                cx_logs.create_log_entry(status = "error", msg = msg, name = repo_name, release_date = tag_date)
                print("    " + msg)
            print(line.strip())
        if status:
            msg = "Checkmarx succesfully scaned the project [{}] with release date [{}].".format(repo_name, tag_date)
            cx_logs.create_log_entry(msg = msg, name = repo_name, release_date = tag_date)
            print("    " + msg)
    else:
        print("    Skipping Checkmarx scan.")
