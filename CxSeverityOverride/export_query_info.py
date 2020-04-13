import site_options_libs as so

odbc_name = 'checkmarx'
# Connect to database and read query options
print('Connecting to Cx DB')
cursor = so.connect_cx_db(odbc_name)
cursor2 = so.connect_cx_db(odbc_name)
cursor3 = so.connect_cx_db(odbc_name)

print('Exporting Preset Information...')
presetRecords = cursor.execute(so.qry_fetch_all_presets)
presetRows = presetRecords.fetchall()    
so.write_options_map(presetRows, 'presets.csv')


print('Exporting Query Information')
query_map = []
# Add row that contains the column headers to the export
query_def = so.create_option_row()
query_def[so.USER_DEFINED_COL] = 'UserDefined (1 - No, 2 - Yes) [REQUIRED]'
query_def[so.QUERY_ID_COL] = 'QueryId'
query_def[so.QUERY_NAME_COL] = 'QueryName'
query_def[so.SEVERITY_COL] = 'Severity [REQUIRED]'
query_def[so.PACKAGE_ID_COL] = 'PackageId [REQUIRED]'
query_def[so.LANGUAGE_NAME_COL] = 'Language Name' 
query_def[so.GROUP_NAME_COL] = 'Group Name'
query_def[so.PACKAGE_TYPE_COL] = 'PackageType'
query_def[so.PACKAGE_TYPE_NAME_COL] = 'PackageType Name'
query_def[so.PRESET_ID_COL] = 'PresetId'
query_def[so.COMMENT_COL] = 'User comments [OPTIONAL]'
query_map.append(query_def)

# Read Query info from Cx Database
queries_cur = cursor.execute(so.qry_find_all_queries)
row = queries_cur.fetchone() 
while row: 
    print(f'Found Query: "{row[1]}", QueryId: {row[0]}')
    query_def = so.create_option_row()
    query_def[so.QUERY_ID_COL] = row[0]
    query_def[so.QUERY_NAME_COL] = row[1]
    query_def[so.SEVERITY_COL] = row[2]
    query_def[so.PACKAGE_ID_COL] = row[3]
    # Find the associated group name
    group_cur = cursor2.execute(so.qry_find_group_name, row[3])
    groupInfo = group_cur.fetchone() 
    query_def[so.GROUP_NAME_COL] = groupInfo[0]
    query_def[so.LANGUAGE_NAME_COL] = groupInfo[1]
    query_def[so.PACKAGE_TYPE_COL] = groupInfo[2]
    query_def[so.PACKAGE_TYPE_NAME_COL] = groupInfo[3]
    # Find the associated preset
    preset_details = cursor3.execute(so.qry_find_preset_id_for_query, row[0])
    presetInfo = preset_details.fetchall()
    preset_ids = []
    for row in presetInfo:
            preset_ids.append(row[0])
    query_def[so.PRESET_ID_COL] = preset_ids
    # Need to handle the group name
    query_map.append(query_def)
    row = queries_cur.fetchone() 
# Compare Cx DB queries against Query info found in current file
print(f'Merging existing site options.')
opts_map = so.read_options_map()
for opt_row in opts_map:
    for q_row_idx, q_row in enumerate(query_map):
        # Does this Query exist in the current site_options.csv file?
        if q_row_idx != 0 and int(opt_row[so.QUERY_ID_COL]) == int(q_row[so.QUERY_ID_COL]) and int(opt_row[so.USER_DEFINED_COL]) == so.USER_DEFINED:
            print(f'Found user defined option for QueryId: {opt_row[so.QUERY_ID_COL]}, Query Name: {opt_row[so.QUERY_NAME_COL]}')
            q_row[so.USER_DEFINED_COL] = opt_row[so.USER_DEFINED_COL]
            q_row[so.QUERY_NAME_COL] = opt_row[so.QUERY_NAME_COL]
            q_row[so.SEVERITY_COL] = opt_row[so.SEVERITY_COL]
            q_row[so.PACKAGE_ID_COL] = opt_row[so.PACKAGE_ID_COL]            
            q_row[so.LANGUAGE_NAME_COL] = opt_row[so.LANGUAGE_NAME_COL]
            q_row[so.GROUP_NAME_COL] = opt_row[so.GROUP_NAME_COL]
            q_row[so.PACKAGE_TYPE_COL] = opt_row[so.PACKAGE_TYPE_COL]
            q_row[so.PACKAGE_TYPE_NAME_COL] = opt_row[so.PACKAGE_TYPE_NAME_COL]
            q_row[so.PRESET_ID_COL] = opt_row[so.PRESET_ID_COL]
            q_row[so.COMMENT_COL] = opt_row[so.COMMENT_COL]
# Write out the Query Map that was created
so.write_options_map(query_map, 'query.csv')
print('Exported Query Information')