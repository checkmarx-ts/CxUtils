import pyodbc
import os.path
import csv

# Defines Site Option types
USER_DEFINED = 2

# Defines value to column mappings for option file
USER_DEFINED_COL = 0
QUERY_ID_COL = 1
QUERY_NAME_COL = 2
SEVERITY_COL = 3
PACKAGE_ID_COL = 4
LANGUAGE_NAME_COL = 5
GROUP_NAME_COL = 6
PACKAGE_TYPE_COL = 7
PACKAGE_TYPE_NAME_COL = 8
PRESET_ID_COL = 9
COMMENT_COL = 10

## Queries
qry_fetch_all_presets = 'SELECT Id, Name from Presets'
qry_find_all_queries = 'SELECT QueryId, Name, Severity, PackageId from QueryVersion WHERE IsActive=1'
qry_find_cur_query_ver = 'SELECT QueryVersionCode FROM QueryVersion WHERE QueryId=? AND IsActive=1'
qry_find_group_name = 'SELECT Name, LanguageName, PackageType, PackageTypeName FROM QueryGroup WHERE PackageId=?'
qry_find_preset_id_for_query = 'SELECT PresetId from Preset_Details WHERE QueryId=?'
qry_update_query = 'UPDATE Query SET Severity=?, PackageId=? WHERE QueryId=?'
qry_update_query_ver = 'UPDATE QueryVersion SET Severity=?, PackageId=? WHERE QueryVersionCode=?'
qry_add_query_to_preset = 'INSERT into Preset_Details values(?, ?, \'0\')'
qry_update_package_info = 'UPDATE QueryGroup SET PackageType=?, PackageTypeName=? WHERE PackageId=?'

def connect_cx_db(odbc_name):
    """
    Establishes connection to Checkmarx DB
    """
    conn = pyodbc.connect(f'DSN={odbc_name};Trusted_Connection=yes;')
    return conn.cursor()

def read_options_map():
    """
    Reads the query.csv option map.
    """
    option_map = []
    if os.path.isfile('query.csv'):
        with open('query.csv') as opts:
            opts_reader = csv.reader(opts, delimiter=',')
            # Always dispose of the first row, it contains the uneeded header
            first_row = True
            for row in opts_reader:
                if first_row != True:
                    option_map.append(row)
                else:
                    first_row = False
    return option_map

def create_option_row():
    """
    Generates a new 'empty' option row
    """
    opt = []
    #opt.append(1)                         # Query Option
    opt.append(1)                         # Not User Defined
    opt.append(0)                         # QueryId
    opt.append('None')                    # Query Name
    opt.append(0)                         # Severity
    opt.append(0)                         # PackageId
    opt.append('')                        # Language Name
    opt.append('None')                    # Group Name
    opt.append(0)                         # PackageType
    opt.append('None')                    # PackageType Name
    opt.append(0)                         # PresetId
    opt.append('')                        # Comment
    return opt

def write_options_map(option_map, target_file):
    """
    Writes the site options map to specified CSV file.
    """
    with open(target_file, mode='w', newline ='\n') as opts:
        opts_writer = csv.writer(opts, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in option_map:
            opts_writer.writerow(row)
