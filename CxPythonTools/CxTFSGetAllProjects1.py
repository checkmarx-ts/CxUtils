
import optparse;
import os;
import traceback;
import platform;
import re;
import string;
import sys;
import collections;

from datetime import datetime;

import CxTFSServerEndpoint1;
import CxTFSProjectData1;
import CxTFSProjectDataCollection1;

optParser               = optparse.OptionParser();
sScriptId               = optParser.get_prog_name();
sScriptVers             = "(v2.0303)";
sScriptDisp             = sScriptId+" "+sScriptVers+":"
cScriptArgc             = len(sys.argv);

bVerbose                = False;
sScriptTFSCollection    = None;
sScriptTFSServerURL     = None;
sScriptTFSUserId        = None;
sScriptTFSPAT           = None;
sScriptOutputReportFile = "";
sScriptOutputPlistsDir  = "";

def main():

    try:

        sPythonVers = ("v%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro));
        sServerNode = platform.node();
        dtNow       = datetime.now();
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

        print("%s The Checkmarx TFS 'Get-ALL-Projects' via Rest API #1 is starting execution from Server [%s] on [%s] under Python [%s]..." % (sScriptDisp, sServerNode, sDTNowStamp, sPythonVers));
        print("");

        optParser.add_option("-v", "--verbose", dest="run_verbose", default=False, help="Run VERBOSE", action="store_true");
        optParser.add_option("--collection", dest="tfs_collection", default="DefaultCollection", help="TFS Collection - Default 'DefaultCollection'", metavar="TFS-Collection");
        optParser.add_option("--url", dest="tfs_server_url", default="", help="TFS Server URL - Protocol/Host/Port - sample: --url=http://hostname:8080", metavar="TFS-Server-URL");
        optParser.add_option("--user", dest="tfs_user_id", default="", help="TFS Authentication UserId", metavar="TFS-UserId");
        optParser.add_option("--pat", dest="tfs_pat", default="", help="TFS Authentication PAT (Personal Access Token)", metavar="TFS-PAT");
        optParser.add_option("-o", "--output-report-file", dest="output_report_file", default="", help="(Output) 'report' file [generated]");
        optParser.add_option("-p", "--output-plists-dir", dest="output_plists_dir", default="", help="(Output) 'plists' directory [generated to]");
     
        (options, args) = optParser.parse_args();
     
        bVerbose                = options.run_verbose;
        sScriptTFSCollection    = options.tfs_collection.strip();
        sScriptTFSServerURL     = options.tfs_server_url.strip();
        sScriptTFSUserId        = options.tfs_user_id.strip();
        sScriptTFSPAT           = options.tfs_pat.strip();
        sScriptOutputReportFile = options.output_report_file.strip();
        sScriptOutputPlistsDir  = options.output_plists_dir.strip();
     
        if bVerbose == True:
     
            print("%s Command VERBOSE flag is [%s]..." % (sScriptDisp, bVerbose));
            print("");
            print("%s Command Tfs Collection is [%s]..." % (sScriptDisp, sScriptTFSCollection));
            print("%s Command Tfs Server URL is [%s]..." % (sScriptDisp, sScriptTFSServerURL));
            print("%s Command Tfs UserId is [%s]..." % (sScriptDisp, sScriptTFSUserId));
            print("%s Command Tfs PAT (Personal Access Token) is [%s]..." % (sScriptDisp, sScriptTFSPAT));
            print("%s Command (Output) 'plists' directory is [%s]..." % (sScriptDisp, sScriptOutputPlistsDir));
            print("");

        if sScriptTFSServerURL != None:

            sScriptTFSServerURL = sScriptTFSServerURL.strip();

        if sScriptTFSServerURL == None or \
           len(sScriptTFSServerURL) < 1:

            sScriptTFSServerURL = None;

        else:

            sScriptTFSServerURLLow = sScriptTFSServerURL.lower();

            if sScriptTFSServerURLLow.startswith("http://")  == False and \
               sScriptTFSServerURLLow.startswith("https://") == False and \
               sScriptTFSServerURLLow.startswith("ssh://")   == False:

                sScriptTFSServerURL = None;

        if sScriptTFSServerURL != None:

            sScriptTFSServerURL = sScriptTFSServerURL.strip();

        if sScriptTFSServerURL == None or \
           len(sScriptTFSServerURL) < 1:

            print("");
            print("%s The TFS Server URL is None or Empty - this MUST be supplied - Error!" % (sScriptDisp));
            print("");

            return False;

        if sScriptTFSUserId != None:

            sScriptTFSUserId = sScriptTFSUserId.strip();

        if sScriptTFSUserId == None or \
           len(sScriptTFSUserId) < 1:

            sScriptTFSUserId = None;

            print("");
            print("%s The TFS UserId is None or Empty - this SHOULD be supplied - Warning!" % (sScriptDisp));
            print("");

        if sScriptTFSPAT != None:

            sScriptTFSPAT = sScriptTFSPAT.strip();

        if sScriptTFSPAT == None or \
            len(sScriptTFSPAT) < 1:

            sScriptTFSPAT = None;

            print("");
            print("%s The TFS PAT (Personal Access Token) is None or Empty - this SHOULD be supplied - Warning!" % (sScriptDisp));
            print("");

        if sScriptOutputReportFile != None:

            sScriptOutputReportFile = sScriptOutputReportFile.strip();

        if sScriptOutputReportFile == None or \
           len(sScriptOutputReportFile) < 1:

            sScriptOutputReportFile == "CxTFSGetAllProjects1_response.json";

            print("%s Checkmarx (Output) 'report' file is None or Empty - defaulting to file [%s] - Warning!" % (sScriptDisp, sScriptOutputReportFile));

        else:

            if bVerbose == True:

                print("");
                print("%s Generating the Checkmarx (Output) 'report' into the file [%s]..." % (sScriptDisp, sScriptOutputReportFile));
                print("");

        if sScriptOutputPlistsDir != None:

            sScriptOutputPlistsDir = sScriptOutputPlistsDir.strip();

        if sScriptOutputPlistsDir == None or \
            len(sScriptOutputPlistsDir) < 1:

            sScriptOutputPlistsDir = None;

            print("");
            print("%s The supplied (Output) 'plists' directory is None or Empty - this MUST be supplied - Error!" % (sScriptDisp));
            print("");

            return False;

        sScriptOutputPlistsDirspec = os.path.realpath(sScriptOutputPlistsDir);

        if not os.path.isdir(sScriptOutputPlistsDirspec):

            print("");
            print("%s The (Output) 'plists' directory of [%s] is NOT a valid directory - a valid directory MUST be supplied - Warning!" % (sScriptDisp, sScriptOutputPlistsDirspec));
            print("");

            return False;

        bProcessingError = False;

        cxTFSServerEndpoint = CxTFSServerEndpoint1.CxTFSServerEndpoint(trace=bVerbose, cxtfsserverendpointactive=True, cxtfsserverurl=sScriptTFSServerURL, cxtfsuserid=sScriptTFSUserId, cxtfspat=sScriptTFSPAT);

        if cxTFSServerEndpoint == None:

            print("");
            print("%s The CxTFSServerEndpoint object is None - this object failed to create - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxTFSServerEndpoint (after init) is:" % (sScriptDisp));
            print(cxTFSServerEndpoint.toString());
            print("");

        if cxTFSServerEndpoint.getCxTFSServerEndpointActiveFlag() == False:

            print("");
            print("%s The CxTFSServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (sScriptDisp));
            print("");

            return False;

        cxTFSProjCollection = CxTFSProjectDataCollection1.CxTFSProjectDataCollection(trace=bVerbose, cxtfsserverendpoint=cxTFSServerEndpoint, cxtfscollection=sScriptTFSCollection);

        if cxTFSProjCollection == None:

            print("");
            print("%s The CxTFSProjectDataCollection object is None - this object failed to create - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxTFSProjectDataCollection (after init) is:" % (sScriptDisp));
            print(cxTFSProjCollection.toString());
            print("");

        bTFSProjCollectionInitialDataLoadOk = cxTFSProjCollection.loadCxTFSProjectDataInitialDataToCollectionFromRestAPI();

        if bTFSProjCollectionInitialDataLoadOk == False:

            print("");
            print("%s The CxTFSProjectDataCollection.loadCxTFSProjectDataInitialDataToCollectionFromRestAPI() call failed - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxTFSProjectDataCollection (after InitialData load) is:" % (sScriptDisp));
            print(cxTFSProjCollection.toString());
            print("");

        bGenerateProjReportOk = cxTFSProjCollection.generateCxTFSProjectDataCollectionReport();

        if bGenerateProjReportOk == False:

            print("");
            print("%s The CxTFSProjectDataCollection.generateCxTFSProjectDataCollectionReport() call failed - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxTFSProjectDataCollection (after report) is:" % (sScriptDisp));
            print(cxTFSProjCollection.toString());
            print("");

        if sScriptOutputReportFile != None:

            sScriptOutputReportFile = sScriptOutputReportFile.strip();

        if sScriptOutputReportFile != None and \
            len(sScriptOutputReportFile) > 0:

            bSaveTFSProjCollectionReportOk = cxTFSProjCollection.saveCxTFSProjectDataCollectionReportToFile(outputprojectdatacollectionreportfile=sScriptOutputReportFile);

            if bSaveTFSProjCollectionReportOk == False:

                print("");
                print("%s The CxTFSProjectDataCollection generated 'report' failed to save to the file [%s] - Error!" % (sScriptDisp, sScriptOutputReportFile));
                print("");

                bProcessingError = True;

        if sScriptOutputPlistsDirspec != None:

            sScriptOutputPlistsDirspec = sScriptOutputPlistsDirspec.strip();

        if sScriptOutputPlistsDirspec != None and \
            len(sScriptOutputPlistsDirspec) > 0:

            bSaveTFSProjPlistsToDirectoryOk = cxTFSProjCollection.saveCxTFSProjectDataCollectionAsPlistsToDirectory(outputprojectdatacollectionplistsdir=sScriptOutputPlistsDirspec);

            if bSaveTFSProjPlistsToDirectoryOk == False:

                print("");
                print("%s The CxTFSProjectDataCollection 'plist(s)' failed to save to the directory [%s] - Error!" % (sScriptDisp, sScriptOutputPlistsDirspec));
                print("");

                bProcessingError = True;

        dtNow       = datetime.now();
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

        print("");
        print("%s The Checkmarx TFS 'Get-ALL-Projects' via Rest API #1 is ending execution from Server [%s] on [%s] under Python [%s]..." % (sScriptDisp, sServerNode, sDTNowStamp, sPythonVers));
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

    if bProcessingError == True:

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

