
import optparse;
import os;
import traceback;
import platform;
import re;
import string;
import sys;

from datetime import datetime;

import CxProjectCreationCollectionCheckmarxDefaults1;
import CxServerEndpoint1;
import CxProjectCreation1;
import CxProjectCreationCollection1;
import CxApplicationScannerGITZipper1;

optParser                = optparse.OptionParser();
sScriptId                = optParser.get_prog_name();
sScriptVers              = "(v1.0111)";
sScriptDisp              = sScriptId+" "+sScriptVers+":"
cScriptArgc              = len(sys.argv);

bVerbose                 = False;
bScriptCxForceDelete     = False;
bScriptRecursive         = False;
bScriptCaseSensitive     = False;
sScriptDirectory         = "";
sScriptFilePatterns      = "";
sScriptCxServerURL       = None;
sScriptCxAuthUserId      = None;
sScriptCxAuthPassword    = None;
sScriptOutputScannerFile = "";
sScriptAppWorkDir        = "";
sScriptGitUserId         = None;
sScriptGitPassword       = None;

def main():

    try:

        sPythonVers = ("v%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro));
        sServerNode = platform.node();
        dtNow       = datetime.now();
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

        print("%s The Checkmarx Application 'scanner' via Rest API #1 is starting execution from Server [%s] on [%s] under Python [%s]..." % (sScriptDisp, sServerNode, sDTNowStamp, sPythonVers));
        print("");

        optParser.add_option("-v", "--verbose", dest="run_verbose", default=False, help="Run VERBOSE", action="store_true");
        optParser.add_option("--force-delete", dest="cx_force_delete", default=False, help=optparse.SUPPRESS_HELP, action="store_true");
        optParser.add_option("-r", "--recursive", dest="search_recursive", default=False, help="Search Directory PATHS recursively", action="store_true");
        optParser.add_option("-c", "--case-sensitive", dest="case_sensitive", default=False, help="Search Directory PATHS with case-sensitivity", action="store_true");
        optParser.add_option("-d", "--data-directory", dest="data_directory", default="", help="Directory with file(s) to process", metavar="DIRECTORY-of-Files-to-Process");
        optParser.add_option("-p", "--file-patterns", dest="file_patterns", default="*.plist", help="File 'patterns' to search for (semicolon delimited) [default is '*.properties']", metavar="FILE-PATTERNS");
        optParser.add_option("--url", dest="cx_server_url", default="", help="Checkmarx Server URL - Protocol/Host/Port - sample: --url=http://hostname:8080", metavar="Checkmarx-Server-URL");
        optParser.add_option("--user", dest="cx_auth_user", default="", help="Checkmarx Authentication UserId", metavar="Checkmarx-UserId");
        optParser.add_option("--pswd", dest="cx_auth_pswd", default="", help="Checkmarx Authentication Password", metavar="Checkmarx-Password");
        optParser.add_option("-o", "--output-scanner-file", dest="output_scanner_file", default="", help="(Output) Scanner 'report' file [generated]");
        optParser.add_option("-w", "--app-work-dir", dest="app_work_dir", default="", help="Application 'work' directory [generated to - MUST be Empty]");
        optParser.add_option("--git-user", dest="git_user", default="", help="Git (authentication) UserId", metavar="Git-UserId");
        optParser.add_option("--git-pswd", dest="git_pswd", default="", help="Git (authentication) Password", metavar="Git-Password");
     
        (options, args) = optParser.parse_args();
     
        bVerbose                 = options.run_verbose;
        bScriptCxForceDelete     = options.cx_force_delete;
        bScriptRecursive         = options.search_recursive;
        bScriptCaseSensitive     = options.case_sensitive;
        sScriptDirectory         = options.data_directory.strip();
        sScriptFilePatterns      = options.file_patterns.strip();
        sScriptCxServerURL       = options.cx_server_url.strip();
        sScriptCxAuthUserId      = options.cx_auth_user.strip();
        sScriptCxAuthPassword    = options.cx_auth_pswd.strip();
        sScriptOutputScannerFile = options.output_scanner_file.strip();
        sScriptAppWorkDir        = options.app_work_dir.strip();
        sScriptGitUserId         = options.git_user.strip();
        sScriptGitPassword       = options.git_pswd.strip();
     
        if bVerbose == True:
     
            print("%s Command VERBOSE flag is [%s]..." % (sScriptDisp, bVerbose));

            if bScriptCxForceDelete == True:

                print("%s Command Checkmarx 'force' Delete flag is [%s]..." % (sScriptDisp, bScriptCxForceDelete));

            print("");
            print("%s Command Search 'recursive' flag is [%s]..." % (sScriptDisp, bScriptRecursive));
            print("%s Command Search 'case-sensitive' flag is [%s]..." % (sScriptDisp, bScriptCaseSensitive));
            print("%s Command Data Directory to search is [%s]..." % (sScriptDisp, sScriptDirectory));
            print("%s Command File 'patterns' to search for are [%s]..." % (sScriptDisp, sScriptFilePatterns));
            print("%s Command Checkmarx Server URL is [%s]..." % (sScriptDisp, sScriptCxServerURL));
            print("%s Command Checkmarx Authentication UserId is [%s]..." % (sScriptDisp, sScriptCxAuthUserId));
            print("%s Command Checkmarx Authentication Password is [%s]..." % (sScriptDisp, sScriptCxAuthPassword));
            print("%s Command (Output) Scanner 'report' file is [%s]..." % (sScriptDisp, sScriptOutputScannerFile));
            print("%s Command Application 'work' directory is [%s]..." % (sScriptDisp, sScriptAppWorkDir));
            print("%s Command Git (authentication) UserId is [%s]..." % (sScriptDisp, sScriptGitUserId));
            print("%s Command Git (authentication) Password is [%s]..." % (sScriptDisp, sScriptGitPassword));
            print("");

        if len(sScriptDirectory) < 1:

            print("%s Command received a Data Directory string to search that is 'null' or Empty - Error!" % (sScriptDisp));

            return False;

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

        if sScriptOutputScannerFile != None:

            sScriptOutputScannerFile = sScriptOutputScannerFile.strip();

        if sScriptOutputScannerFile == None or \
           len(sScriptOutputScannerFile) < 1:

            print("%s Checkmarx (Output) Scanner 'report' file is None or Empty - this output will be bypassed - Warning!" % (sScriptDisp));

            sScriptOutputScannerFile == None;

        else:

            if bVerbose == True:

                print("");
                print("%s Generating the Checkmarx (Output) Scanner 'report' into the file [%s]..." % (sScriptDisp, sScriptOutputScannerFile));
                print("");

        if sScriptAppWorkDir != None:

            sScriptAppWorkDir = sScriptAppWorkDir.strip();

        if sScriptAppWorkDir == None or \
            len(sScriptAppWorkDir) < 1:

            sScriptAppWorkDir = None;

            print("");
            print("%s The supplied Application 'work' directory is None or Empty - this MUST be supplied - Error!" % (sScriptDisp));
            print("");

            return False;

        sScriptAppWorkDirspec = os.path.realpath(sScriptAppWorkDir);

        if not os.path.isdir(sScriptAppWorkDirspec):

            print("");
            print("%s The Application 'work' directory of [%s] is NOT a valid directory - a valid directory MUST be supplied - Warning!" % (sScriptDisp, sScriptAppWorkDirspec));
            print("");

            return False;

        if sScriptGitUserId != None:

            sScriptGitUserId = sScriptGitUserId.strip();

        if sScriptGitUserId == None or \
            len(sScriptGitUserId) < 1:

            sScriptGitUserId = None;

        if sScriptGitPassword != None:

            sScriptGitPassword = sScriptGitPassword.strip();

        if sScriptGitPassword == None or \
            len(sScriptGitPassword) < 1:

            sScriptGitPassword = None;

        bProcessingError = False;

        cxProjDefaults = CxProjectCreationCollectionCheckmarxDefaults1.CxProjectCreationCollectionCheckmarxDefaults(trace=bVerbose);

        if cxProjDefaults == None:

            print("");
            print("%s The CxProjectCreationCollectionCheckmarxDefaults object is None - this object failed to create - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxProjectCreationCollectionCheckmarxDefaults (after init) is:" % (sScriptDisp));
            print(cxProjDefaults.toString());
            print("");

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

        if cxServerEndpoint.getCxServerEndpointActiveFlag() == False:

            print("");
            print("%s The CxServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (sScriptDisp));
            print("");

            return False;

        cxProjCollection = CxProjectCreationCollection1.CxProjectCreationCollection(trace=bVerbose, searchrecursive=bScriptRecursive, searchcasesensitive=bScriptCaseSensitive, searchdirectory=sScriptDirectory, searchfilepatterns=sScriptFilePatterns, cxserverendpoint=cxServerEndpoint, cxprojectcreationcollectiondefaults=cxProjDefaults);

        if cxProjCollection == None:

            print("");
            print("%s The CxProjectCreationCollection object is None - this object failed to create - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxProjectCreationCollection (after init) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");

        cxProjCollection.dumpCxProjectCreationCollectionDefaultsFromSuppliedObject();

        bProjCollectionPlistLoadOk = cxProjCollection.loadCxProjectCreationCollectionFromPlistFiles();
     
        if bProjCollectionPlistLoadOk == False:
     
            print("");
            print("%s The CxProjectCreationCollection.loadCxProjectCreationCollectionFromPlistFiles() call failed - Error!" % (sScriptDisp));
            print("");
     
            return False;
     
        if bVerbose == True:
     
            print("");
            print("%s CxProjectCreationCollection (after 'plist' load) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");

        bProjCollectionMetaLoadOk = cxProjCollection.loadCxProjectCreationMetaDataToCollectionFromRestAPI();

        if bProjCollectionMetaLoadOk == False:

            print("");
            print("%s The CxProjectCreationCollection.loadCxProjectCreationMetaDataToCollectionFromRestAPI() call failed - Error!" % (sScriptDisp));
            print("");

            return False;

        if bVerbose == True:

            print("");
            print("%s CxProjectCreationCollection (after MetaData load) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");

    #   cxProjectCreation1 = CxProjectCreation1.CxProjectCreation(trace=bVerbose, cxprojectname="CxProjCreationMainTest1", cxprojectispublic=True, cxprojectteamname="\\CxServer\\SP\\Company\\Users", cxprojectpresetname="Checkmarx Default", cxprojectengineconfigname="Default Configuration", cxprojectbranchnames=["Branch1"]);
    #
    #   if cxProjectCreation1 == None:
    #
    #       print("");
    #       print("%s Failed to create a CxProjectCreation object - Error!" % (sScriptDisp));
    #       print("");
    #
    #       return False;
    #
    #   if bVerbose == True:
    #
    #       print("");
    #       print("%s CxProjectCreation (after init) is:" % (sScriptDisp));
    #       print(cxProjectCreation1.toString());
    #       print("");
    #
    #   bAddProjCreationToCollectionOk = cxProjCollection.addCxProjectCreationToCxProjectCreationCollection(cxprojectcreation=cxProjectCreation1);
    #
    #   if bAddProjCreationToCollectionOk == False:
    #
    #       print("");
    #       print("%s The CxProjectCreationCollection.addCxProjectCreationToCxProjectCreationCollection() call failed - Error!" % (sScriptDisp));
    #       print("");
    #
    #       return False;
    #
    #   if bVerbose == True:
    #
    #       print("");
    #       print("%s CxProjectCreationCollection (after add) is:" % (sScriptDisp));
    #       print(cxProjCollection.toString());
    #       print("");
     
    # TEMP:
    #
    #   return False;
    #
    # TEMP:
     
        if bScriptCxForceDelete == False:
     
            bCreateProjBranchesOk = cxProjCollection.createCxProjectsAndBranchesFromCxProjectCreationCollection();
     
            if bCreateProjBranchesOk == False:
     
                print("");
                print("%s The CxProjectCreationCollection.createCxProjectsAndBranchesFromCxProjectCreationCollection() call failed - Error!" % (sScriptDisp));
                print("");
     
                return False;
     
            if bVerbose == True:
     
                print("");
                print("%s CxProjectCreationCollection (after create) is:" % (sScriptDisp));
                print(cxProjCollection.toString());
                print("");
     
            bCxProjectWasCreatedByRestAPIFlag = cxProjCollection.getCxProjectWasCreatedByRestAPIFlag();

            if bCxProjectWasCreatedByRestAPIFlag == False:

                print("");
                print("%s The CxProjectCreationCollection did NOT 'create' ANY Project(s) - bypassing the reload of MetaData..." % (sScriptDisp));
                print("");

            else:

                print("");
                print("%s The CxProjectCreationCollection DID 'create' Project(s) - reloading the MetaData..." % (sScriptDisp));
                print("");

                bProjCollectionMetaLoad2Ok = cxProjCollection.loadCxProjectCreationMetaDataToCollectionFromRestAPI();

                if bProjCollectionMetaLoad2Ok == False:

                    print("");
                    print("%s The CxProjectCreationCollection.loadCxProjectCreationMetaDataToCollectionFromRestAPI() call failed <reload> - Error!" % (sScriptDisp));
                    print("");

                    return False;

                if bVerbose == True:

                    print("");
                    print("%s CxProjectCreationCollection (after MetaData reload) is:" % (sScriptDisp));
                    print(cxProjCollection.toString());
                    print("");

            cxApplicationZipper = CxApplicationScannerGITZipper1.CxApplicationScannerGITZipper(trace=bVerbose, cxapplicationworkdir=sScriptAppWorkDirspec, gitauthuserid=sScriptGitUserId, gitauthpassword=sScriptGitPassword);

            if cxApplicationZipper == None:

                print("");
                print("%s The CxApplicationScannerGITZipper object is None - this object failed to create - Error!" % (sScriptDisp));
                print("");

                return False;

            if bVerbose == True:

                print("");
                print("%s CxApplicationScannerGITZipper (after init) is:" % (sScriptDisp));
                print(cxApplicationZipper.toString());
                print("");

            cxProjCollection.setCxApplicationZipper(cxapplicationzipper=cxApplicationZipper);

            bScanProjectsOk = cxProjCollection.scanCxProjectsViaPlistFromCollection();

            if bScanProjectsOk == False:

                print("");
                print("%s The CxProjectCreationCollection.scanCxProjectsViaPlistFromCollection() call failed - Error!" % (sScriptDisp));
                print("");

                return False;

            if bVerbose == True:

                print("");
                print("%s CxProjectCreationCollection (after scanning) is:" % (sScriptDisp));
                print(cxProjCollection.toString());
                print("");

        else:
     
            bDeleteProjBranchesOk = cxProjCollection.deleteCxProjectsAndBranchesFromCxProjectCreationCollection();
     
            if bDeleteProjBranchesOk == False:
     
                print("");
                print("%s The CxProjectCreationCollection.deleteCxProjectsAndBranchesFromCxProjectCreationCollection() call failed - Error!" % (sScriptDisp));
                print("");
     
                return False;
     
            if bVerbose == True:
     
                print("");
                print("%s CxProjectCreationCollection (after 'force' delete) is:" % (sScriptDisp));
                print(cxProjCollection.toString());
                print("");
     
        bGenerateProjReportOk = cxProjCollection.generateCxProjectCreationCollectionReport();
     
        if bGenerateProjReportOk == False:
     
            print("");
            print("%s The CxProjectCreationCollection.generateCxProjectCreationCollectionReport() call failed - Error!" % (sScriptDisp));
            print("");
     
            return False;
     
        if bVerbose == True:
     
            print("");
            print("%s CxProjectCreationCollection (after report) is:" % (sScriptDisp));
            print(cxProjCollection.toString());
            print("");
     
        asCxProjectCreationCollectionReport = cxProjCollection.getCxProjectCreationCollectionReportAsList();
     
        if asCxProjectCreationCollectionReport == None or \
            len(asCxProjectCreationCollectionReport) < 1:
     
            print("");
            print("%s The CxProjectCreationCollection generated 'report' is None or 'empty' - Error!" % (sScriptDisp));
            print("");
     
            return False;
     
        print('\n'.join(asCxProjectCreationCollectionReport));
     
        if sScriptOutputScannerFile != None:
     
            sScriptOutputScannerFile = sScriptOutputScannerFile.strip();
     
        if sScriptOutputScannerFile != None and \
            len(sScriptOutputScannerFile) > 0:
     
            bSaveCreationCollectionOk = cxProjCollection.saveCxProjectCreationCollectionReportToFile(outputprojectcreationcollectionfile=sScriptOutputScannerFile);
     
            if bSaveCreationCollectionOk == False:
     
                print("");
                print("%s The CxProjectCreationCollection generated 'report' failed to save to the file [%s] - Error!" % (sScriptDisp, sScriptOutputScannerFile));
                print("");
     
                bProcessingError = True;

        dtNow       = datetime.now();
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

        print("");
        print("%s The Checkmarx Application 'scanner' via Rest API #1 is ending execution from Server [%s] on [%s] under Python [%s]..." % (sScriptDisp, sServerNode, sDTNowStamp, sPythonVers));
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

