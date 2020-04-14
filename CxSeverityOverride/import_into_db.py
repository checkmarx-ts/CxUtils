import pyodbc
import site_options_libs as so

odbc_name = 'checkmarx'
# Connect to database and read query options
print('Beginning Conversion')
opts_map = so.read_options_map()
cursor = so.connect_cx_db(odbc_name)
print(f'Connected to database through ODBC connection: {odbc_name}!')
# Reads the Query options and make updates where appropriate
for opts in opts_map:
    user_defined = int(opts[so.USER_DEFINED_COL])
    query_id = opts[so.QUERY_ID_COL]
    query_name = opts[so.QUERY_NAME_COL]
    package_id = opts[so.PACKAGE_ID_COL]
    package_type = opts[so.PACKAGE_TYPE_COL]
    package_type_name = opts[so.PACKAGE_TYPE_NAME_COL]
    severity = opts[so.SEVERITY_COL]
    comment = opts[so.COMMENT_COL]
    presetString = opts[so.PRESET_ID_COL]
    presetList = (str(presetString)[1:-1]).split(",")
    
    if user_defined == so.USER_DEFINED:
        cursor.execute(so.qry_find_cur_query_ver, query_id)
        qry = cursor.fetchone()
        if qry:
            qvc = qry[0]
            for preset_id in presetList:
                cursor.execute(so.qry_add_query_to_preset,preset_id, query_id)
            cursor.execute(so.qry_update_query, severity, package_id, query_id)
            cursor.execute(so.qry_update_query_ver, severity, package_id, qvc)
            cursor.execute(so.qry_update_package_info,package_type,package_type_name,package_id)
            
            cursor.commit()
            print(f'Updated Query {query_name}, QueryId: {query_id}, Severity: {severity} \n Preset(s): {presetList}')
        else:
            print('Didnt find Query!')
print('Done Updating Queries')
