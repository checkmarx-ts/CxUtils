import os
import sys
import xmltodict

def convert_date (checkmarx_date):

    # Tuesday, June 11, 2019 3:25:42 PM

    split_string = checkmarx_date.split(",")

    month_day_str = split_string[1].strip()
    year_time_str = split_string[2].strip()

    year_str = year_time_str.split()

    month_str = month_day_str.split()[0]
    day_str = month_day_str.split()[1]

    if (month_str == "January"):
        month_str = "01"
    elif (month_str == "February"):
        month_str = "02"
    elif (month_str == "March"):
        month_str = "03"
    elif (month_str == "April"):
        month_str = "04"
    elif (month_str == "May"):
        month_str = "05"
    elif (month_str == "June"):
        month_str = "06"
    elif (month_str == "July"):
        month_str = "07"
    elif (month_str == "August"):
        month_str = "08"
    elif (month_str == "September"):
        month_str = "09"
    elif (month_str == "October"):
        month_str = "10"
    elif (month_str == "November"):
        month_str = "11"
    elif (month_str == "December"):
        month_str = "12"
    else: 
        month_str = "ERROR"
    
    final = year_str[0] + "-" + month_str + "-" + day_str

    return (final)

def convert_state (checkmarx_state):
    if checkmarx_state == "0":
        state_str = "To Verify"
    elif checkmarx_state == "1":
        state_str = "Not Exploitable"
    elif checkmarx_state == "2":
        state_str = "Confirmed"
    elif checkmarx_state == "3":
        state_str = "Urgent"
    elif checkmarx_state == "4":
        state_str = "Proposed Not Exploitable"
    elif checkmarx_state == "5":
        state_str = "Must Fix"
    elif checkmarx_state == "6":
        state_str = "Requires further triage"
    else:
        state_str = "ERROR"

    return (state_str)


def parse_xml(doc):

    if doc and 'CxXMLResults' in doc:
        xml_results = doc['CxXMLResults']

        if xml_results and 'Query' in xml_results:

            # need to convert checkmarx date into a single string

            date = convert_date (xml_results["@ScanStart"])

            # create file

            filename = xml_results["@ProjectName"] + "." + date + ".csv"
            f= open(forward_filename,"w+")
            f.write ("projectname,loc,language,scandate,sid,Direct Link,Query Name,CWE,Status,Result State,Result Severity,Source File,Assigned User\n")

            # loop through all the results and write to file

            for query in xml_results['Query']:

                results = query['Result']
                list_results = []
                if isinstance(results, list):
                    list_results = results
                else:
                    list_results.append(results)
                for result in list_results:

                    path = result['Path']

                    f.write (str(xml_results["@ProjectName"]) + "," +
                             str(xml_results["@LinesOfCodeScanned"]) + "," +
                             str (query["@Language"]) + "," +
                             str (date) + "," +
                             str (path["@SimilarityId"]) + "," +
                             str (result['@DeepLink']) + "," +
                             str (query["@name"]) + "," +
                             str (query["@cweId"]) + "," +
                             str (result['@Status']) + "," +
                             str (convert_state(result["@state"])) + "," +
                             str (result["@Severity"]) + "," +
                             str (result['@FileName']) + "," +
                             str (result['@AssignToUser']) + "," +
                             "\n")

            f.close()

#-----------------------------------------------------------------------------------------------------

# this script takes the XML report and converts it into a csv that can be 'fowarded' into splunk enterprise

args = sys.argv

xml_report = args[1]
forward_filename = args[2]

# this will parse the XML files so we can read them

with open(xml_report, encoding='UTF8') as fd:
    document = xmltodict.parse(fd.read())

parse_xml(document)
