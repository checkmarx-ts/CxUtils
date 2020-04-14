import sys
import subprocess
import shutil
import os
import stat
import cx_runner_logs as cx_logs
import cx_runner_options as cx_opts

def read_cli_opts():
    print("Testing args")
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == "--use_targets":
                cx_opts.use_targets = True
            if "--milestone_ver" in arg:
                tokens = arg.split("=")
                if len(tokens) > 1:
                    try:
                        depth = int(tokens[1])
                        if depth == 0 or depth == 1:
                            cx_opts.milestone_ver = depth
                        else:
                            print("Error reading milesone depth, only 0 or 1 are allowed!")
                            sys.exit()
                    except ValueError:
                        print("Error reading milesone depth!")
                        sys.exit()
                else:
                    print("Error reading milesone depth!")
    print("Milestone depth (0 means latest, 1 previous, etc): {}".format(cx_opts.milestone_ver))
    print("Reading (targets.txt): {}".format(cx_opts.use_targets))

def del_evenReadonly(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

def clean_working_dir(padding):
    print(padding + "Removing previous temp directory, please wait..")
    if os.path.exists(cx_opts.working_dir):            
        try:
            shutil.rmtree(cx_opts.working_dir, onerror=del_evenReadonly)
        except OSError as err:
            print(padding + "Error removing working directory")
            print(padding + err)
    print(padding + "Temp directory removed")

def count_lines_of_code(repo_name, tag_date):
    if cx_opts.count_loc:
        print("    Counting lines of code")
        #mvn = subprocess.Popen([shutil.which(cx_opts.cloc_prg_name), "."],
        mvn = subprocess.Popen([cx_opts.cloc_prg_name, "."],
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            bufsize=0,
                            cwd=cx_opts.working_dir,
                            shell=True)
        for line in mvn.stdout:
            if "SUM" in line:
                sums = line.split()
                msg = "Counted projects LOC.".format(repo_name, tag_date)
                cx_logs.create_log_entry(msg = msg, 
                                         name = repo_name, 
                                         release_date = tag_date, 
                                         files_count=int(sums[1]), 
                                         comment_lines=int(sums[3]), 
                                         blank_lines=int(sums[2]), 
                                         code_lines=int(sums[4]), 
                                         total_lines_count=(int(sums[2]) + int(sums[3]) + int(sums[4])))
            print(line.strip())