import sys
import datetime
import svn.remote
import cx_runner_logs as cx_logs
import cx_runner_options as cx_opts

target_list = None

def read_targets_file():
    global target_list
    if cx_opts.use_targets:
        msg = "Target list activated, reading (targets.txt)."
        print(msg)
        cx_logs.create_log_entry(msg = msg)
        try:
            with open('targets.txt', 'r') as f:
                target_list = f.read().splitlines()
        except FileNotFoundError:
            print("Could not read (targets.txt)!")
            sys.exit()
        print(target_list)
        print("Target list read.")
    else:
        msg = "Target list is NOT active, all projects will be processed."
        print(msg)
        cx_logs.create_log_entry(msg = msg)

def is_project_active(project):
    global target_list
    if cx_opts.use_targets == False:
        return True
    else:
        for target in target_list:
            if project == target:
                return True
        msg = "Found project {} in SVN but skipping it because its not in (targets.txt).".format(project)
        cx_logs.create_log_entry(msg = msg)
        print("    " + msg)
        return False        

def extract_tag_info(tag, repo_name):
    is_milestone = False
    tag_tokens = tag.split(".")
    if len(tag_tokens[1]) == 2:
        # Format matches YYYY.mm.dd-M20500622-01
        if tag[11] == "M":
            is_milestone = True
        tag_dt = datetime.datetime.strptime(tag[0:10], '%Y.%m.%d')
        tag_label = tag_dt.strftime("%Y.%m.%d")
        return (tag_dt, is_milestone, tag_label)
    elif len(tag_tokens[1]) == 4:
        # Format matches YYYY.mm00.0-MYYYYmmdd-01
        if tag[12] == "M":
            is_milestone = True
            tag_dt = datetime.datetime.strptime(tag[13:21], '%Y%m%d')
        else:
            is_milestone = False
            tag_dt = datetime.datetime.strptime(tag[12:20], '%Y%m%d')
        tag_label = tag_dt.strftime("%Y.%m.%d")
        return (tag_dt, is_milestone, tag_label)
    else:
        # Unknown!
        print("    Date Style Unknown!: {}".format(tag))
        msg = "Encountered unknown SVN tag datetime format [{}]".format(tag)
        cx_logs.create_log_entry(status = "error", msg = msg, name = repo_name)
        tag_dt = datetime.datetime.now()
        tag_label = tag_dt.strftime("%Y.%m.%d")
        return (tag_dt, is_milestone, tag_label)

def find_last_commit_url(repo_name):
    """
    Within a given repo there should be a 'tags' folder. This scans the tags 
    folder to find the entry with the most recent datestamp. Each tag is 
    assumed to have a format like this: 

        /<repo_name>/tags/2019.10.05-M20500622-01

                    2019.10.05-M20500622-01
    # -> New sample 2019.1100.0-M20191123-01 <-- This version has the date after the M

    NOTE: The 'M' after the 2019.10.05 date indicates 'Milestone'. We skip tags without that.
    """
    newest_dt = None
    tag_label = ""
    prev_project_url = project_url = None
    try:
        tags_url = (cx_opts.svn_server + "/" + repo_name + "/tags")
        repo = svn.remote.RemoteClient(tags_url, username = cx_opts.svn_username, password = cx_opts.svn_password)
        tag_list = repo.list(extended=True)
        for tag_entry in tag_list:
            tag_dt, is_milestone, tag_label = extract_tag_info(tag_entry["name"], repo_name)
            if is_milestone:
                if newest_dt == None or newest_dt <= tag_dt:
                    print("    Found New Milestone")                    
                    prev_project_url = project_url
                    newest_dt = tag_dt
                    project_url = tags_url + "/" + tag_entry["name"]
        if cx_opts.milestone_ver == 1 and prev_project_url is not None:
            # In the case we should use the previous mileston, if it exists
            print("    reverting to previous milestone!")
            project_url = prev_project_url
        if project_url != None:
            msg = "Found release version for SVN project [{}] with release date [{}].".format(repo_name, tag_label)
            print("    " + msg)
            cx_logs.create_log_entry(msg = msg, name = repo_name, release_date = tag_label)
    except svn.exception.SvnException:
        msg = "A current release version could not be determined for SVN project '{}' because a SVN 'tags' folder could not be located!".format(repo_name)
        print("    " + msg)
        cx_logs.create_log_entry(status = "error", msg = msg, name = repo_name)
    return (project_url, tag_label)