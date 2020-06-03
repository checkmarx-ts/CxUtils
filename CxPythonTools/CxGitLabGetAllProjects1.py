
import optparse;
import os;
import traceback;
import platform;
import re;
import string;
import sys;
import collections;

from datetime import datetime;

import CxGitLabServerEndpoint1;
import CxGitLabProjectData1;
import CxGitLabProjectDataCollection1;

optParser               = optparse.OptionParser();
sScriptId               = optParser.get_prog_name();
sScriptVers             = "(v2.0205)";
sScriptDisp             = sScriptId+" "+sScriptVers+":"
cScriptArgc             = len(sys.argv);

bVerbose                = False;
sScriptGitLabGroup      = None;
sScriptGitLabServerURL  = None;
sScriptGitLabUserId     = None;
sScriptGitLabPassword   = None;
sScriptOutputReportFile = "";
sScriptOutputPlistsDir  = "";

def main():

    try:

        sPythonVers = ("v%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro));
        sServerNode = platform.node();
        dtNow       = datetime.now();
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

        print("%s The Checkmarx GitLab 'Get-ALL-Projects' via Rest API #1 is starting execution from Server [%s] on [%s] under Python [%s]..." % (sScriptDisp, sServerNode, sDTNowStamp, sPythonVers));
        print("");

        optParser.add_option("-v", "--verbose", dest="run_verbose", default=False, help="Run VERBOSE", action="store_true");
        optParser.add_option("-g", "--group", dest="gitlab_group", default="", help="GitLab Group", metavar="GitLab-Group");
        optParser.add_option("--url", dest="gitlab_server_url", default="", help="GitLab Server URL - Protocol/Host/Port - sample: --url=http://hostname:8080", metavar="GitLab-Server-URL");
        optParser.add_option("--user", dest="gitlab_user_id", default="", help="GitLab Authentication UserId", metavar="GitLab-UserId");
        optParser.add_option("--pswd", dest="gitlab_password", default="", help="GitLab Authentication (UserId) Password", metavar="GitLab-Password");
        optParser.add_option("-o", "--output-report-file", dest="output_report_file", default="", help="(Output) 'report' file [generated]");
        optParser.add_option("-p", "--output-plists-dir", dest="output_plists_dir", default="", help="(Output) 'plists' directory [generated to]");
     
        (options, args) = optParser.parse_args();
     
        bVerbose                = options.run_verbose;
        sScriptGitLabGroup      = options.gitlab_group.strip();
        sScriptGitLabServerURL  = options.gitlab_server_url.strip();
        sScriptGitLabUserId     = options.gitlab_user_id.strip();
        sScriptGitLabPassword   = options.gitlab_password.strip();
        sScriptOutputReportFile = options.output_report_file.strip();
        sScriptOutputPlistsDir  = options.output_plists_dir.strip();
     
        if bVerbose == True:
     
            print("%s Command VERBOSE flag is [%s]..." % (sScriptDisp, bVerbose));
            print("");
            print("%s Command GitLab Group is [%s]..." % (sScriptDisp, sScriptGitLabGroup));
            print("%s Command GitLab Server URL is [%s]..." % (sScriptDisp, sScriptGitLabServerURL));
            print("%s Command GitLab UserId is [%s]..." % (sScriptDisp, sScriptGitLabUserId));
            print("%s Command GitLab (UserId) Password is [%s]..." % (sScriptDisp, sScriptGitLabPassword));
            print("%s Command (Output) 'report' file is [%s]..." % (sScriptDisp, sScriptOutputReportFile));
            print("%s Command (Output) 'plists' directory is [%s]..." % (sScriptDisp, sScriptOutputPlistsDir));
            print("");

        if sScriptGitLabGroup != None:

            sScriptGitLabGroup = sScriptGitLabGroup.strip();

        if sScriptGitLabGroup == None or \
            len(sScriptGitLabGroup) < 1:

            print("");
            print("%s The GitLab 'group' is None or Empty - this MUST be supplied - Error!" % (sScriptDisp));
            print("");

            return False;

        if sScriptGitLabServerURL != None:

            sScriptGitLabServerURL = sScriptGitLabServerURL.strip();

        if sScriptGitLabServerURL == None or \
           len(sScriptGitLabServerURL) < 1:

            sScriptGitLabServerURL = None;

        else:

            sScriptGitLabServerURLLow = sScriptGitLabServerURL.lower();

            if sScriptGitLabServerURLLow.startswith("http://")  == False and \
               sScriptGitLabServerURLLow.startswith("https://") == False and \
               sScriptGitLabServerURLLow.startswith("ssh://")   == False:

                sScriptGitLabServerURL = None;

        if sScriptGitLabServerURL != None:

            sScriptGitLabServerURL = sScriptGitLabServerURL.strip();

        if sScriptGitLabServerURL == None or \
           len(sScriptGitLabServerURL) < 1:

            print("");
            print("%s The GitLab Server URL is None or Empty - this MUST be supplied - Error!" % (sScriptDisp));
            print("");

            return False;

        if sScriptGitLabUserId != None:

            sScriptGitLabUserId = sScriptGitLabUserId.strip();

        if sScriptGitLabUserId == None or \
           len(sScriptGitLabUserId) < 1:

            sScriptGitLabUserId = None;

            print("");
            print("%s The GitLab UserId is None or Empty - this SHOULD be supplied - Warning!" % (sScriptDisp));
            print("");

        if sScriptGitLabPassword != None:

            sScriptGitLabPassword = sScriptGitLabPassword.strip();

        if sScriptGitLabPassword == None or \
            len(sScriptGitLabPassword) < 1:

            sScriptGitLabPassword = None;

            print("");
            print("%s The GitLab (UserId) Password is None or Empty - this SHOULD be supplied - Warning!" % (sScriptDisp));
            print("");

        if sScriptOutputReportFile != None:

            sScriptOutputReportFile = sScriptOutputReportFile.strip();

        if sScriptOutputReportFile == None or \
           len(sScriptOutputReportFile) < 1:

            sScriptOutputReportFile == "CxGitLabGetAllProjects1_response.json";

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

        cxGitLabServerEndpoint = CxGitLabServerEndpoint1.CxGitLabServerEndpoint(trace=bVerbose, cxgitlabserverendpointactive=True, cxgitlabserverurl=sScriptGitLabServerURL, cxgitlabgroup=sScriptGitLabGroup, cxgitlabuserid=sScriptGitLabUserId, cxgitlabpassword=sScriptGitLabPassword);

        if cxGitLabServerEndpoint == None:

            print("");
            print("%s The CxGitLabServerEndpoint object is None - this object failed to create - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxGitLabServerEndpoint (after init) is:" % (sScriptDisp));
            print(cxGitLabServerEndpoint.toString());
            print("");

        if cxGitLabServerEndpoint.getCxGitLabServerEndpointActiveFlag() == False:

            print("");
            print("%s The CxGitLabServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (sScriptDisp));
            print("");

            return False;

        cxGitLabProjCollection = CxGitLabProjectDataCollection1.CxGitLabProjectDataCollection(trace=bVerbose, cxgitlabserverendpoint=cxGitLabServerEndpoint);
     
        if cxGitLabProjCollection == None:
     
            print("");
            print("%s The CxGitLabProjectDataCollection object is None - this object failed to create - Error!" % (sScriptDisp));
            print("");
     
            return False;
     
        if bVerbose == True:
     
            print("");
            print("%s CxGitLabProjectDataCollection (after init) is:" % (sScriptDisp));
            print(cxGitLabProjCollection.toString());
            print("");
     
        bGitLabProjCollectionInitialDataLoadOk = cxGitLabProjCollection.loadCxGitLabProjectDataInitialDataToCollectionFromRestAPI();
     
        if bGitLabProjCollectionInitialDataLoadOk == False:
     
            print("");
            print("%s The CxGitLabProjectDataCollection.loadCxGitLabProjectDataInitialDataToCollectionFromRestAPI() call failed - Error!" % (sScriptDisp));
            print("");
     
            return False;
     
        if bVerbose == True:
     
            print("");
            print("%s CxGitLabProjectDataCollection (after InitialData load) is:" % (sScriptDisp));
            print(cxGitLabProjCollection.toString());
            print("");
     
        bGenerateProjReportOk = cxGitLabProjCollection.generateCxGitLabProjectDataCollectionReport();
     
        if bGenerateProjReportOk == False:
     
            print("");
            print("%s The CxGitLabProjectDataCollection.generateCxGitLabProjectDataCollectionReport() call failed - Error!" % (sScriptDisp));
            print("");
     
            return False;
     
        if bVerbose == True:
     
            print("");
            print("%s CxGitLabProjectDataCollection (after report) is:" % (sScriptDisp));
            print(cxGitLabProjCollection.toString());
            print("");
     
        if sScriptOutputReportFile != None:
     
            sScriptOutputReportFile = sScriptOutputReportFile.strip();
     
        if sScriptOutputReportFile != None and \
            len(sScriptOutputReportFile) > 0:
     
            bSaveGitLabProjCollectionReportOk = cxGitLabProjCollection.saveCxGitLabProjectDataCollectionReportToFile(outputprojectdatacollectionreportfile=sScriptOutputReportFile);
     
            if bSaveGitLabProjCollectionReportOk == False:
     
                print("");
                print("%s The CxGitLabProjectDataCollection generated 'report' failed to save to the file [%s] - Error!" % (sScriptDisp, sScriptOutputReportFile));
                print("");
     
                bProcessingError = True;
     
        if sScriptOutputPlistsDirspec != None:
     
            sScriptOutputPlistsDirspec = sScriptOutputPlistsDirspec.strip();
     
        if sScriptOutputPlistsDirspec != None and \
            len(sScriptOutputPlistsDirspec) > 0:
     
            bSaveGitLabProjPlistsToDirectoryOk = cxGitLabProjCollection.saveCxGitLabProjectDataCollectionAsPlistToDirectory(outputprojectdatacollectionplistsdir=sScriptOutputPlistsDirspec);
     
            if bSaveGitLabProjPlistsToDirectoryOk == False:
     
                print("");
                print("%s The CxGitLabProjectDataCollection 'plist(s)' failed to save to the directory [%s] - Error!" % (sScriptDisp, sScriptOutputPlistsDirspec));
                print("");
     
                bProcessingError = True;

        dtNow       = datetime.now();
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

        print("");
        print("%s The Checkmarx GitLab 'Get-ALL-Projects' via Rest API #1 is ending execution from Server [%s] on [%s] under Python [%s]..." % (sScriptDisp, sServerNode, sDTNowStamp, sPythonVers));
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

