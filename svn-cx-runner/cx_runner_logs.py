import json
import cx_runner_options as cx_opts

run_log = []

def start_log():
    f = open(cx_opts.log_file, "w")
    f.write(json.dumps(run_log, indent=4, sort_keys=False))
    f.close()

def create_log_entry(status = "success", msg = "", name = "", release_date = "", files_count=0, comment_lines=0, blank_lines=0, code_lines=0, total_lines_count=0):
    log_entry = {}
    log_entry["status"] = status
    log_entry["name"] = name
    log_entry["release_date"] = release_date
    log_entry["files_count"] = files_count
    log_entry["comment_lines"] = comment_lines
    log_entry["blank_lines"] = blank_lines
    log_entry["code_lines"] = code_lines
    log_entry["total_lines_count"] = total_lines_count
    log_entry["msg"] = msg
    run_log.append(log_entry)
    write_log()

def write_log():
    f = open(cx_opts.log_file, "w")
    f.write(json.dumps(run_log, indent=4, sort_keys=False))
    f.close()