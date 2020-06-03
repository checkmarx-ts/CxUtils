
import optparse;
import os;
import traceback;
import platform;
import re;
import string;
import sys;

from datetime import datetime;

import CxServerEndpoint1;
import CxProjectData1;
import CxProjectDataCollection1;

optParser                    = optparse.OptionParser();
sScriptId                    = optParser.get_prog_name();
sScriptVers                  = "(v1.0515)";
sScriptDisp                  = sScriptId+" "+sScriptVers+":"
cScriptArgc                  = len(sys.argv);

bVerbose                     = False;
sScriptCxServerURL           = None;
sScriptCxAuthUserId          = None;
sScriptCxAuthPassword        = None;
sScriptOutputStatsReportFile = "";
sScriptOutputStatsHtmlFile   = "";

def main():

    try:

        sPythonVers = ("v%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro));
        sServerNode = platform.node();
        dtNow       = datetime.now();
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

        print("%s The Checkmarx Project 'statistics' via Rest API #1 is starting execution from Server [%s] on [%s] under Python [%s]..." % (sScriptDisp, sServerNode, sDTNowStamp, sPythonVers));
        print("");

        optParser.add_option("-v", "--verbose", dest="run_verbose", default=False, help="Run VERBOSE", action="store_true");
        optParser.add_option("--url", dest="cx_server_url", default="", help="Checkmarx Server URL - Protocol/Host/Port - sample: --url=http://hostname:8080", metavar="Checkmarx-Server-URL");
        optParser.add_option("--user", dest="cx_auth_user", default="", help="Checkmarx Authentication UserId", metavar="Checkmarx-UserId");
        optParser.add_option("--pswd", dest="cx_auth_pswd", default="", help="Checkmarx Authentication Password", metavar="Checkmarx-Password");
        optParser.add_option("-o", "--output-report-file", dest="output_report_file", default="", help="(Output) 'statistics' report file [generated]");
        optParser.add_option("-f", "--output-html-file", dest="output_html_file", default="", help="(Output) 'statistics' Html (report) file [generated]");
     
        (options, args) = optParser.parse_args();
     
        bVerbose                     = options.run_verbose;
        sScriptCxServerURL           = options.cx_server_url.strip();
        sScriptCxAuthUserId          = options.cx_auth_user.strip();
        sScriptCxAuthPassword        = options.cx_auth_pswd.strip();
        sScriptOutputStatsReportFile = options.output_report_file.strip();
        sScriptOutputStatsHtmlFile   = options.output_html_file.strip();
     
        if bVerbose == True:
     
            print("%s Command VERBOSE flag is [%s]..." % (sScriptDisp, bVerbose));
            print("");
            print("%s Command Checkmarx Server URL is [%s]..." % (sScriptDisp, sScriptCxServerURL));
            print("%s Command Checkmarx Authentication UserId is [%s]..." % (sScriptDisp, sScriptCxAuthUserId));
            print("%s Command Checkmarx Authentication Password is [%s]..." % (sScriptDisp, sScriptCxAuthPassword));
            print("%s Command (Output) 'statistics' report file is [%s]..." % (sScriptDisp, sScriptOutputStatsReportFile));
            print("%s Command (Output) 'statistics' Html (report) file is [%s]..." % (sScriptDisp, sScriptOutputStatsHtmlFile));
            print("");

        if sScriptCxServerURL != None:

            sScriptCxServerURL = sScriptCxServerURL.strip();

        if sScriptCxServerURL == None or \
           len(sScriptCxServerURL) < 1:

            sScriptCxServerURL = None;

        else:

            sScriptCxServerURLLow = sScriptCxServerURL.lower();

            if sScriptCxServerURLLow.startswith("http://")  == False and \
               sScriptCxServerURLLow.startswith("https://") == False:

                sScriptCxServerURL = None;

        if sScriptCxServerURL != None:

            sScriptCxServerURL = sScriptCxServerURL.strip();

        if sScriptCxServerURL == None or \
           len(sScriptCxServerURL) < 1:

            print("");
            print("%s The Checkmarx Server URL is None or Empty - this MUST be supplied - Error!" % (sScriptDisp));
            print("");

            return False;

        if sScriptCxAuthUserId != None:

            sScriptCxAuthUserId = sScriptCxAuthUserId.strip();

        if sScriptCxAuthUserId == None or \
            len(sScriptCxAuthUserId) < 1:

            sScriptCxAuthUserId = None;

            print("");
            print("%s The Checkmarx Auth UserId is None or Empty - this SHOULD be supplied - Warning!" % (sScriptDisp));
            print("");

        if sScriptCxAuthPassword != None:

            sScriptCxAuthPassword = sScriptCxAuthPassword.strip();

        if sScriptCxAuthPassword == None or \
            len(sScriptCxAuthPassword) < 1:

            sScriptCxAuthPassword = None;

            print("");
            print("%s The Checkmarx Auth Password is None or Empty - this SHOULD be supplied - Warning!" % (sScriptDisp));
            print("");

        if sScriptOutputStatsReportFile != None:

            sScriptOutputStatsReportFile = sScriptOutputStatsReportFile.strip();

        if sScriptOutputStatsReportFile == None or \
           len(sScriptOutputStatsReportFile) < 1:

            print("%s Checkmarx (Output) 'statistics' report filename is None or Empty - this output will be bypassed - Warning!" % (sScriptDisp));

            sScriptOutputStatsReportFile == None;

        else:

            if bVerbose == True:

                print("");
                print("%s Generating the Checkmarx (Output) 'statistics' report into the file [%s]..." % (sScriptDisp, sScriptOutputStatsReportFile));
                print("");

        if sScriptOutputStatsHtmlFile != None:

            sScriptOutputStatsHtmlFile = sScriptOutputStatsHtmlFile.strip();

        if sScriptOutputStatsHtmlFile == None or \
           len(sScriptOutputStatsHtmlFile) < 1:

            print("%s Checkmarx (Output) 'statistics' Html (report) filename is None or Empty - this output will be bypassed - Warning!" % (sScriptDisp));

            sScriptOutputStatsHtmlFile == None;

        else:

            if bVerbose == True:

                print("");
                print("%s Generating the Checkmarx (Output) 'statistics' Html (report) into the file [%s]..." % (sScriptDisp, sScriptOutputStatsHtmlFile));
                print("");

        bProcessingError = False;

        cxServerEndpoint = CxServerEndpoint1.CxServerEndpoint(trace=bVerbose, cxserverendpointactive=True, cxserverurl=sScriptCxServerURL, cxauthuserid=sScriptCxAuthUserId, cxauthpassword=sScriptCxAuthPassword);

        if cxServerEndpoint == None:

            print("");
            print("%s The CxServerEndpoint object is None - this object failed to create - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxServerEndpoint (after init) is:" % (sScriptDisp));
            print(cxServerEndpoint.toString());
            print("");

        cxProjCollection = CxProjectDataCollection1.CxProjectDataCollection(trace=bVerbose, cxserverendpoint=cxServerEndpoint);

        if cxProjCollection == None:

            print("");
            print("%s The CxProjectDataCollection object is None - this object failed to create - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxProjectDataCollection (after init) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");

        bProjCollectionMetaOk = cxProjCollection.loadCxProjectDataMetaDataToCollectionFromRestAPI();

        if bProjCollectionMetaOk == False:

            print("");
            print("%s The CxProjectDataCollection.loadCxProjectDataMetaDataToCollectionFromRestAPI() call failed - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxProjectDataCollection (after meta data load) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");

        bProjCollectionLoadOk = cxProjCollection.loadCxProjectDataCollectionFromRestAPI();

        if bProjCollectionLoadOk == False:

            print("");
            print("%s The CxProjectDataCollection.loadCxProjectDataCollectionFromRestAPI() call failed - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxProjectDataCollection (after project load) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");

        bGenerateScanDeltaOk = cxProjCollection.generateCxProjectDataCollectionScansDelta();

        if bGenerateScanDeltaOk == False:
     
            print("");
            print("%s The CxProjectDataCollection.generateCxProjectDataCollectionScansDelta() call failed - Error!" % (sScriptDisp));
            print("");
     
            return False;
     
        if bVerbose == True:

            print("");
            print("%s CxProjectDataCollection (after scans delta) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");

        bProjCollectionReportOk = cxProjCollection.generateCxProjectDataCollectionReport();
     
        if bProjCollectionReportOk == False:
     
            print("");
            print("%s The CxProjectDataCollection.generateCxProjectDataCollectionReport() call failed - Error!" % (sScriptDisp));
            print("");
     
            return False;
     
        if bVerbose == True:

            print("");
            print("%s CxProjectDataCollection (after generate report) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");

        asCxProjectDataCollectionReport = cxProjCollection.getCxProjectDataCollectionReportAsList();
     
        if asCxProjectDataCollectionReport == None or \
            len(asCxProjectDataCollectionReport) < 1:

            print("");
            print("%s The CxProjectDataCollection generated 'statistics' report is None or 'empty' - Error!" % (sScriptDisp));
            print("");
     
            return False;
     
        print('\n'.join(asCxProjectDataCollectionReport));
        print("");
     
        if sScriptOutputStatsReportFile != None:
     
            sScriptOutputStatsReportFile = sScriptOutputStatsReportFile.strip();
     
        if sScriptOutputStatsReportFile != None and \
            len(sScriptOutputStatsReportFile) > 0:
     
            bSaveDataCollectionReportOk = cxProjCollection.saveCxProjectDataCollectionReportToFile(outputprojectdatacollectionreportfile=sScriptOutputStatsReportFile);
     
            if bSaveDataCollectionReportOk == False:
     
                print("");
                print("%s The CxProjectDataCollection generated 'statistics' report failed to save to the file [%s] - Error!" % (sScriptDisp, sScriptOutputStatsReportFile));
                print("");
     
                bProcessingError = True;

        bProjCollectionHtmlOk = cxProjCollection.generateCxProjectDataCollectionHtml();

        if bProjCollectionHtmlOk == False:

            print("");
            print("%s The CxProjectDataCollection.generateCxProjectDataCollectionHtml() call failed - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxProjectDataCollection (after generate html) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");

        asCxProjectDataCollectionHtml = cxProjCollection.getCxProjectDataCollectionHtmlAsList();

        if asCxProjectDataCollectionHtml == None or \
            len(asCxProjectDataCollectionHtml) < 1:

            print("");
            print("%s The CxProjectDataCollection generated 'statistics' Html (report) is None or 'empty' - Error!" % (sScriptDisp));
            print("");

            return False;

        print('\n'.join(asCxProjectDataCollectionHtml));
        print("");

        if sScriptOutputStatsHtmlFile != None:

            sScriptOutputStatsHtmlFile = sScriptOutputStatsHtmlFile.strip();

        if sScriptOutputStatsHtmlFile != None and \
            len(sScriptOutputStatsHtmlFile) > 0:

            bSaveDataCollectionHtmlOk = cxProjCollection.saveCxProjectDataCollectionHtmlToFile(outputprojectdatacollectionhtmlfile=sScriptOutputStatsHtmlFile);

            if bSaveDataCollectionHtmlOk == False:

                print("");
                print("%s The CxProjectDataCollection generated 'statistics' Html (report) failed to save to the file [%s] - Error!" % (sScriptDisp, sScriptOutputStatsHtmlFile));
                print("");

                bProcessingError = True;

        dtNow       = datetime.now();
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

        print("");
        print("%s The Checkmarx Project 'statistics' via Rest API #1 is ending execution from Server [%s] on [%s] under Python [%s]..." % (sScriptDisp, sServerNode, sDTNowStamp, sPythonVers));
        print("");

    except Exception as inst:

        print("%s 'main()' - exception occured..." % (sScriptDisp));
        print(type(inst));
        print(inst);

        excType, excValue, excTraceback = sys.exc_info();
        asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

        print("- - - ");
        print('\n'.join(asTracebackLines));
        print("- - - ");

        return False;

    return True;

if __name__ == '__main__':

    try:

        pass;

    except Exception as inst:

        print("%s '<before>-main()' - exception occured..." % (sScriptDisp));
        print(type(inst));
        print(inst);

        excType, excValue, excTraceback = sys.exc_info();
        asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

        print("- - - ");
        print('\n'.join(asTracebackLines));
        print("- - - ");

    bCmdExecOk = main();

    if bCmdExecOk == False:

        print("%s Exiting with a Return Code of (31)..." % (sScriptDisp));

        sys.exit(31);

    print("%s Exiting with a Return Code of (0)..." % (sScriptDisp));

    sys.exit(0);

