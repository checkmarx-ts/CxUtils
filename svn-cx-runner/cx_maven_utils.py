import subprocess
import shutil
import cx_runner_logs as cx_logs
import cx_runner_options as cx_opts

def get_maven_deps(repo_name, tag_date):
    if cx_opts.maven_dependencies:
        print("    Downloading Maven dependencies.")
        #mvn = subprocess.Popen([shutil.which("mvn"), "dependency:unpack-dependencies", "-DoutputDirectory=maven_src"],
        mvn = subprocess.Popen(["mvn", "dependency:unpack-dependencies", "-DoutputDirectory=maven_src"],
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            bufsize=0,
                            cwd=cx_opts.working_dir,
                            shell=True)
        mvn.stdin.close()
        status = True
        for line in mvn.stdout:
            if "[ERROR]" in line:
                status = False
            print(line.strip())
        if status:
            msg = "Maven succesfully downloaded source dependencies for the project [{}] with release date [{}].".format(repo_name, tag_date)
            cx_logs.create_log_entry(msg = msg, name = repo_name, release_date = tag_date)
            print("    " + msg)
        else:
            msg = "Maven encountered error downloading source dependencies for the project [{}] with release date [{}].".format(repo_name, tag_date)
            cx_logs.create_log_entry(status = "error", msg = msg, name = repo_name, release_date = tag_date)
            print("    " + msg)
    else:
        print("    Skipping Maven dependency download.")
