
import os;
import traceback;
import platform;
import re;
import string;
import sys;
import collections;
import zope.interface;
import subprocess;

import CxProjectCreation1;

from zope.interface import implementer;
from CxApplicationScannerInterfaceZipper1 import CxApplicationScannerInterfaceZipper;

# ass CxApplicationScannerGITZipper(interface.implements(CxApplicationScannerInterfaceZipper)):
@implementer(CxApplicationScannerInterfaceZipper)
class CxApplicationScannerGITZipper(object):

    sClassMod                 = __name__;
    sClassId                  = "CxApplicationScannerGITZipper";
    sClassVers                = "(v1.0201)";
    sClassDisp                = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                = False;

    sGitAuthUserId            = None;
    sGitAuthPassword          = None;

    # Project 'generated' field(s):

    sCxApplicationWorkDir     = None;
    sCxApplicationZip         = None;

    # Misc. variables:

    sPlatform                 = None;
    bPlatformIsWindows        = False;

    # Zip 'include' file extensions:

    asCxApplicationZipInclude = ["*.apex",
                                 "*.apexp",
                                 "*.asax",
                                 "*.ascx",
                                 "*.asp",
                                 "*.aspx",
                                 "*.bas",
                                 "*.bdy",
                                 "*.c",
                                 "*.c++",
                                 "*.cc",
                                 "*.cgi",
                                 "*.cls",
                                 "*.component",
                                 "*.conf",
                                 "*.config",
                                 "*.cpp",
                                 "*.cs",
                                 "*.cshtml",
                                 "*.csproj",
                                 "*.ctl",
                                 "*.ctp",
                                 "*.cxx",
                                 "*.dsr",
                                 "*.ec",
                                 "*.erb",
                                 "*.fnc",
                                 "*.frm",
                                 "*.go",
                                 "*.gradle",
                                 "*.groovy",
                                 "*.gsh",
                                 "*.gsp",
                                 "*.gtl",
                                 "*.gvy",
                                 "*.gy ",
                                 "*.h",
                                 "*.h++",
                                 "*.handlebars",
                                 "*.hbs",
                                 "*.hh",
                                 "*.hpp",
                                 "*.htm",
                                 "*.html",
                                 "*.hxx",
                                 "*.inc",
                                 "*.jade",
                                 "*.java",
                                 "*.javasln",
                                 "*.js",
                                 "*.jsf",
                                 "*.json",
                                 "*.jsp",
                                 "*.jspf",
                                 "*.lock",
                                 "*.m",
                                 "*.master",
                                 "*.-meta.xml",
                                 "*.mf",
                                 "*.object",
                                 "*.page",
                                 "*.pc",
                                 "*.pck",
                                 "*.php",
                                 "*.php3",
                                 "*.php4",
                                 "*.php5",
                                 "*.phtm",
                                 "*.phtml",
                                 "*.pkb",
                                 "*.pkh",
                                 "*.pks",
                                 "*.pl",
                                 "*.plist",
                                 "*.pls",
                                 "*.plx",
                                 "*.pm",
                                 "*.prc",
                                 "*.project",
                                 "*.properties",
                                 "*.psgi",
                                 "*.py",
                                 "*.rb",
                                 "*.report",
                                 "*.rhtml",
                                 "*.rjs",
                                 "*.rxml",
                                 "*.scala",
                                 "*.should_neve_match_anything_9gdfg4",
                                 "*.sln",
                                 "*.spc",
                                 "*.sqb",
                                 "*.sqf",
                                 "*.sqh",
                                 "*.sql",
                                 "*.sqp",
                                 "*.sqt",
                                 "*.sqtb",
                                 "*.sqth",
                                 "*.sqv",
                                 "*.swift",
                                 "*.tag",
                                 "*.tgr",
                                 "*.tld",
                                 "*.tpb",
                                 "*.tpl",
                                 "*.tps",
                                 "*.trg",
                                 "*.trigger",
                                 "*.ts",
                                 "*.tsx",
                                 "*.twig",
                                 "*.vb",
                                 "*.vbp",
                                 "*.vbs",
                                 "*.wod",
                                 "*.workflow",
                                 "*.xaml",
                                 "*.xhtml",
                                 "*.xib",
                                 "*.xml",
                                 "*.xsaccess",
                                 "*.xsapp",
                                 "*.xsjs",
                                 "*.xsjslib"
                                ];

    def __init__(self, trace=False, cxapplicationworkdir=None, gitauthuserid=None, gitauthpassword=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxApplicationWorkDir(cxapplicationworkdir=cxapplicationworkdir);
            self.setGitAuthUserId(gitauthuserid=gitauthuserid);
            self.setGitAuthPassword(gitauthpassword=gitauthpassword);

            self.sPlatform          = platform.system();
            self.bPlatformIsWindows = self.sPlatform.startswith('Windows');

            if self.bPlatformIsWindows == False:

                self.bPlatformIsWindows = self.sPlatform.startswith('Microsoft');

        except Exception as inst:

            print("%s '__init__()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

    def getTraceFlag(self):

        return self.bTraceFlag;

    def setTraceFlag(self, trace=False):

        self.bTraceFlag = trace;

    def getCxApplicationWorkDir(self):

        return self.sCxApplicationWorkDir;

    def setCxApplicationWorkDir(self, cxapplicationworkdir=None):

        self.sCxApplicationWorkDir = cxapplicationworkdir;

        if self.sCxApplicationWorkDir != None:

            self.sCxApplicationWorkDir = self.sCxApplicationWorkDir.strip();

        if self.sCxApplicationWorkDir == None or \
           len(self.sCxApplicationWorkDir) < 1:

            self.sCxApplicationWorkDir = None;

    def getCxApplicationZip(self):

        return self.sCxApplicationZip;

    def setCxApplicationZip(self, cxapplicationzip=None):

        self.sCxApplicationZip = cxapplicationzip;

        if self.sCxApplicationZip != None:

            self.sCxApplicationZip = self.sCxApplicationZip.strip();

        if self.sCxApplicationZip == None or \
           len(self.sCxApplicationZip) < 1:
         
            self.sCxApplicationZip = None;
         
    def getGitAuthUserId(self):

        return self.sGitAuthUserId;

    def setGitAuthUserId(self, gitauthuserid=None):

        self.sGitAuthUserId = gitauthuserid;

        if self.sGitAuthUserId != None:

            self.sGitAuthUserId = self.sGitAuthUserId.strip();

        if self.sGitAuthUserId == None or \
           len(self.sGitAuthUserId) < 1:

            self.sGitAuthUserId = None;

    def getGitAuthPassword(self):

        return self.sGitAuthPassword;

    def setGitAuthPassword(self, gitauthpassword=None):

        self.sGitAuthPassword = gitauthpassword;

        if self.sGitAuthPassword != None:

            self.sGitAuthPassword = self.sGitAuthPassword.strip();

        if self.sGitAuthPassword == None or \
           len(self.sGitAuthPassword) < 1:

            self.sGitAuthPassword = None;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'sGitAuthUserId' is [%s]..." % (self.sClassDisp, self.sGitAuthUserId));
            print("%s The contents of 'sGitAuthPassword' is [%s]..." % (self.sClassDisp, self.sGitAuthPassword));
            print("%s The contents of 'sCxApplicationWorkDir' is [%s]..." % (self.sClassDisp, self.getCxApplicationWorkDir()));
            print("%s The contents of 'sCxApplicationZip' is [%s]..." % (self.sClassDisp, self.getCxApplicationZip()));
            print("%s The contents of 'sPlatform' is [%s]..." % (self.sClassDisp, self.sPlatform));
            print("%s The contents of 'bPlatformIsWindows' is [%s]..." % (self.sClassDisp, self.bPlatformIsWindows));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'sGitAuthUserId' is [%s], " % (self.sGitAuthUserId));
        asObjDetail.append("'sGitAuthPassword' is [%s], " % (self.sGitAuthPassword));
        asObjDetail.append("'sCxApplicationWorkDir' is [%s], " % (self.getCxApplicationWorkDir()));
        asObjDetail.append("'sCxApplicationZip' is [%s]. " % (self.getCxApplicationZip()));
        asObjDetail.append("'sPlatform' is [%s], " % (self.sPlatform));
        asObjDetail.append("'bPlatformIsWindows' is [%s]. " % (self.bPlatformIsWindows));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def generateCxApplicationSASTZip(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        return self.__generateCxApplicationZip(cxprojectcreation=cxprojectcreation, cxprojectziptargettype="sast");

    def generateCxApplicationOSAZip(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        return self.__generateCxApplicationZip(cxprojectcreation=cxprojectcreation, cxprojectziptargettype="osa");

    def __generateCxApplicationZip(self, cxprojectcreation=None, cxprojectziptargettype=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined for the Checkmarx CxProjectCreation(s) Collection - one CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        sCxProjectZipTargetType = cxprojectziptargettype;

        if sCxProjectZipTargetType != None:

            sCxProjectZipTargetType = sCxProjectZipTargetType.strip();

        if sCxProjectZipTargetType == None or \
            len(sCxProjectZipTargetType) < 1:

            sCxProjectZipTargetType = "sast";

        if sCxProjectZipTargetType != "sast" and \
           sCxProjectZipTargetType != "osa":

            sCxProjectZipTargetType = "sast";

        if self.sCxApplicationWorkDir != None:

            self.sCxApplicationWorkDir = self.sCxApplicationWorkDir.strip();

        if self.sCxApplicationWorkDir == None or \
            len(self.sCxApplicationWorkDir) < 1:

            self.sCxApplicationWorkDir = None;

            print("");
            print("%s NO Application 'work' directory has been specified nor defined - an Application 'work' directory MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        self.sCxApplicationWorkDir = os.path.realpath(self.sCxApplicationWorkDir);

        if not os.path.isdir(self.sCxApplicationWorkDir):

            print("");
            print("%s The Application 'work' directory of [%s] is NOT a valid directory - a valid directory MUST be supplied - Warning!" % (self.sClassDisp, self.sCxApplicationWorkDir));
            print("");

            return False;

        bProcessingError = False;

        try:

            sCxProjectName = cxProjectCreation.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the Project 'zipping' of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            print("");
            print("%s For a CxProjectCreation named [%s] using a 'work' directory of [%s] to create an application zip..." % (self.sClassDisp, sCxProjectName, self.sCxApplicationWorkDir));

            sAppCollDir = cxProjectCreation.getCxProjectExtraField1();

            if sAppCollDir != None:

                sAppCollDir = sAppCollDir.strip();

            if sAppCollDir == None or \
                len(sAppCollDir) < 1:

                sAppCollDir = "DefaultCollection";

            sAppCollDir = sAppCollDir.replace(' ', '-');
            sAppProjDir = sCxProjectName.replace(' ', '-');

            # --------------------------------------------------------------------------------------------------
            # CxProjectCreationCollection1.CxProjectCreationCollection (v1.0563):  CxProjectCreation element (  1) of (  1):
            # Project 'Name' [JWS_App-Project_1], 'Base Name' [JWS_App-Project_1], 'Id' [390264], 'Is Public?' [ True], 
            # ........'Team' [None], 'Version' [None], 
            # ........'Team Name' [\CxServer\SP\Company\Users], 'Team Id' [22222222-2222-448d-b029-989c9070eb23], 
            # ........'Preset Name' [Checkmarx Default], 'Preset Id' [36], 
            # ........'EngineConfig Name' [Default Configuration], 'EngineConfig Id' [1]. 
            # ............'Extra' Project field #1 'Value' [JWebsoftwareDev]. 
            # ............'Extra' Project field #2 'Value' [[{'RepoBranches': [{'BranchIsActive': 'true', 'BranchName': 'refs/heads/master'}],
            #                                                 'RepoIsActive': 'true', 
            #                                                 'RepoRemoteURL': 'http://darylc-laptop:9080/tfs/JWebsoftwareDev/_git/JWS_App-Project_1', 
            #                                                 'RepoSshURL': 'ssh://darylc-laptop:22/tfs/JWebsoftwareDev/_git/JWS_App-Project_1',
            #                                                 'RepoTitle': 'JWS_App-Project_1', 
            #                                                 'RepoURL': 'http://192.168.2.190:9080/tfs/JWebsoftwareDev/_apis/git/repositories/6f23a004-735a-4df6-909b-17571d9f06b1'}]]. 
            # ............'Extra' Project field #3 'Value' [{'Action': 'Scan', 'id': '1450529'}]. 
            # --------------------------------------------------------------------------------------------------

            listAppRepos = cxProjectCreation.getCxProjectExtraField2();

            if listAppRepos == None or \
               type(listAppRepos) != list or \
               len(listAppRepos) < 1:

               print("");
               print("%s For a CxProjectCreation named [%s] there are NO Application Repo(s) defined - at least 1 MUST be defined - Warning!" % (self.sClassDisp, sCxProjectName));
               print("");

               self.sCxApplicationZip = None;

               return False;

            for dictAppRepoItem in listAppRepos:

                if dictAppRepoItem == None or \
                   type(dictAppRepoItem) != dict or \
                   len(dictAppRepoItem) < 1:

                    continue;

                sAppRepoName = dictAppRepoItem["RepoTitle"];

                if sAppRepoName != None:

                    sAppRepoName = sAppRepoName.strip();

                if sAppRepoName == None or \
                    len(sAppRepoName) < 1:

                    sAppRepoName = "DefaultRepo";

                sAppRepoDir = sAppRepoName.replace(' ', '-');

                sAppRepoIsActive    = dictAppRepoItem["RepoIsActive"];
                sAppRepoIsActiveLow = sAppRepoIsActive.lower();

                if sAppRepoIsActiveLow != "true":

                    print("%s For a CxProjectCreation named [%s] the Application Repo named [%s] is marked NOT 'active' - bypassing the Repo - Warning!" % (self.sClassDisp, sCxProjectName, sAppRepoName));

                    continue;

                sAppRepoRemoteURL = dictAppRepoItem["RepoRemoteURL"];

                if sAppRepoRemoteURL != None:

                    sAppRepoRemoteURL = sAppRepoRemoteURL.strip();

                if sAppRepoRemoteURL == None or \
                    len(sAppRepoRemoteURL) < 1:

                    print("%s For a CxProjectCreation named [%s] the Application Repo named [%s] does NOT have a 'remoteURL' - bypassing the Repo - Warning!" % (self.sClassDisp, sCxProjectName, sAppRepoName));

                    continue;

                sAppRepoTargetDirspec = os.path.join(self.sCxApplicationWorkDir, sAppCollDir, sAppProjDir, sAppRepoDir);

                if not os.path.isdir(sAppRepoTargetDirspec):

                    print("%s The Application Repo 'target' directory of [%s] is NOT a valid directory - creating it - Warning!" % (self.sClassDisp, sAppRepoTargetDirspec));

                    os.makedirs(sAppRepoTargetDirspec);

                    print("%s For a CxProjectCreation named [%s] type [%s] created an application repo 'target' directory of [%s]..." % (self.sClassDisp, sCxProjectName, sCxProjectZipTargetType, sAppRepoTargetDirspec));

                sAppRepoBranch = None;

                listAppRepoBranches = dictAppRepoItem["RepoBranches"];

                if listAppRepoBranches != None and \
                   type(listAppRepoBranches) == list and \
                   len(listAppRepoBranches) > 0:

                    for dictAppRepoBranch in listAppRepoBranches:

                        if dictAppRepoBranch == None:

                            continue;

                        sAppRepoBranchIsActive    = dictAppRepoBranch["BranchIsActive"];
                        sAppRepoBranchIsActiveLow = sAppRepoBranchIsActive.lower();

                        if sAppRepoBranchIsActiveLow != "true":

                            continue;

                        sAppRepoBranch = dictAppRepoBranch["BranchName"]; 

                        if sAppRepoBranch != None:

                            sAppRepoBranch = sAppRepoBranch.strip();

                        if sAppRepoBranch == None or \
                            len(sAppRepoBranch) < 1:

                            continue;

                        asAppRepoBranchTokens = sAppRepoBranch.rpartition("/");

                        if asAppRepoBranchTokens == None or \
                            len(asAppRepoBranchTokens) < 3:

                            break;

                        sAppRepoBranch = asAppRepoBranchTokens[2];

                        break;

                bCloneAppRepoBranchOk = self.__cloneCxAppRepoBranchToDirectory(appreporemoteurl=sAppRepoRemoteURL, apprepobranch=sAppRepoBranch, apprepotargetdir=sAppRepoTargetDirspec);

                if bCloneAppRepoBranchOk == False:

                    print("");
                    print("%s '__cloneCxAppRepoBranchToDirectory()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    continue;

            # Zip up the App Repo(s)...

            sAppRepoTargetZipDirspec  = os.path.join(self.sCxApplicationWorkDir, sAppCollDir, sAppProjDir);
            sAppRepoTargetZipFile     = "%s_%s_%s.zip" % (sAppCollDir, sAppProjDir, sCxProjectZipTargetType);
            sAppRepoTargetZipFilespec = os.path.join(self.sCxApplicationWorkDir, sAppRepoTargetZipFile);

        #   bAppRepoZippedOk = self.__zipCxAppRepoWorkDirectoryToFile(apprepozipfile=sAppRepoTargetZipFilespec, apprepotargetdir=sAppRepoTargetDirspec);
        #   bAppRepoZippedOk = self.__zipCxAppRepoWorkDirectoryToFile(apprepozipfile=sAppRepoTargetZipFilespec, apprepotargetdir=sAppRepoTargetZipDirspec);
            bAppRepoZippedOk = self.__zipCxAppRepoWorkDirectoryToFile(apprepozipfile=sAppRepoTargetZipFilespec, apprepotargetdir=sAppRepoTargetZipDirspec, apprepotargettype=sCxProjectZipTargetType);

            if bAppRepoZippedOk == False:

                print("");
                print("%s '__zipCxAppRepoWorkDirectoryToFile()' [%s] API call failed - Error!" % (self.sClassDisp, sCxProjectZipTargetType));
                print("");

                return False;

        #   self.sCxApplicationZip = "/CheckMarx_Resources/CheckMarx.Demo/SQLInjectionSample_base/SQLInjectionSample.zip";
            self.sCxApplicationZip = sAppRepoTargetZipFilespec;

            print("%s For a CxProjectCreation named [%s] created an application zip of [%s]..." % (self.sClassDisp, sCxProjectName, self.sCxApplicationZip));
            print("");

        except Exception as inst:

            print("%s '__generateCxApplicationZip()' [%s] - exception occured..." % (self.sClassDisp, sCxProjectZipTargetType));
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

    def __cloneCxAppRepoBranchToDirectory(self, appreporemoteurl=None, apprepobranch=None, apprepotargetdir=None):

        sAppRepoRemoteURL = appreporemoteurl;

        if sAppRepoRemoteURL != None:

            sAppRepoRemoteURL = sAppRepoRemoteURL.strip();

        if sAppRepoRemoteURL == None or \
            len(sAppRepoRemoteURL) < 1:

            print("");
            print("%s NO Application Repo 'remote' URL has been specified nor defined - this MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        sAppRepoBranch = apprepobranch;

        if sAppRepoBranch != None:

            sAppRepoBranch = sAppRepoBranch.strip();

        if sAppRepoBranch == None or \
            len(sAppRepoBranch) < 1:

            sAppRepoBranch = None;

        sAppRepoTargetDir = apprepotargetdir;

        if sAppRepoTargetDir != None:

            sAppRepoTargetDir = sAppRepoTargetDir.strip();

        if sAppRepoTargetDir == None or \
            len(sAppRepoTargetDir) < 1:

            print("");
            print("%s NO Application Repo 'target' directory has been specified nor defined - this MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        sAppRepoTargetDirspec = os.path.realpath(sAppRepoTargetDir);

        if not os.path.isdir(sAppRepoTargetDirspec):

            print("");
            print("%s The Application Repo 'target' directory of [%s] is NOT a valid directory - a valid directory MUST be supplied - Warning!" % (self.sClassDisp, sAppRepoTargetDirspec));
            print("");

            return False;

        bProcessingError = False;

        try:

            sGitRepoRemoteURL = sAppRepoRemoteURL;

            # Check for Git credentials - if available, rewrite the URL:

            if self.sGitAuthUserId != None:

                self.sGitAuthUserId = self.sGitAuthUserId.strip();

            if self.sGitAuthUserId != None and \
                len(self.sGitAuthUserId) > 0:

                asAppRepoRemoteURLTokens = sAppRepoRemoteURL.partition("://");

                if asAppRepoRemoteURLTokens == None or \
                    len(asAppRepoRemoteURLTokens) < 3:

                    print("");
                    print("%s The Application Repo 'remote' URL of [%s] failed to partition on '://' for Git 'user/password' - Error!" % (self.sClassDisp, sAppRepoRemoteURL));
                    print("");

                    return False;

                if self.sGitAuthPassword != None:

                    self.sGitAuthPassword = self.sGitAuthPassword.strip();

                if self.sGitAuthPassword == None or \
                    len(self.sGitAuthPassword) < 1:

                    sGitRepoRemoteURL = ("%s://%s@%s" % (asAppRepoRemoteURLTokens[0], self.sGitAuthUserId, asAppRepoRemoteURLTokens[2]));

                else:

                    sGitRepoRemoteURL = ("%s://%s:%s@%s" % (asAppRepoRemoteURLTokens[0], self.sGitAuthUserId, self.sGitAuthPassword, asAppRepoRemoteURLTokens[2]));

            # Generate the physical command line.

            sAppRepoCloneCmd = None;

            if sAppRepoBranch != None and \
                len(sAppRepoBranch) > 0:

                sAppRepoCloneCmd = "git clone --branch %s %s %s" % (sAppRepoBranch, sGitRepoRemoteURL, sAppRepoTargetDirspec);

            else:

                sAppRepoCloneCmd = "git clone %s %s" % (sGitRepoRemoteURL, sAppRepoTargetDirspec);

            if sAppRepoCloneCmd != None:

                sAppRepoCloneCmd = sAppRepoCloneCmd.strip();

            if sAppRepoCloneCmd == None or \
                len(sAppRepoCloneCmd) < 1:

                print("");
                print("%s The Application Repo 'git clone' command failed to generate - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("%s Running the 'git' command of [%s]..." % (self.sClassDisp, sAppRepoCloneCmd));

            gitCloneProcess = subprocess.run(sAppRepoCloneCmd, shell=True, text=True, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT); 
            sGitCloneStdout = gitCloneProcess.stdout;
            sGitCloneStderr = gitCloneProcess.stderr;

            if sGitCloneStdout != None and \
                len(sGitCloneStdout) > 0:

                print("%s 'stdout' from the 'git' command of [%s] is:" % (self.sClassDisp, sAppRepoCloneCmd));
                print(sGitCloneStdout);

            if sGitCloneStderr != None and \
                len(sGitCloneStderr) > 0:

                print("%s 'stderr' from the 'git' command of [%s] is:" % (self.sClassDisp, sAppRepoCloneCmd));
                print(sGitCloneStderr);

            gitCloneCmdRC = gitCloneProcess.returncode;

            if gitCloneCmdRC != 0:

                print("%s The 'git' command of [%s] returned a 'bad' (NON-Zero) RC of [%d]..." % (self.sClassDisp, sAppRepoCloneCmd, gitCloneCmdRC));

            else:

                print("%s The 'git' command of [%s] returned a 'good' RC of [%d]..." % (self.sClassDisp, sAppRepoCloneCmd, gitCloneCmdRC));

        except Exception as inst:

            print("%s '__cloneCxAppRepoBranchToDirectory()' - exception occured..." % (self.sClassDisp));
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

    def __zipCxAppRepoWorkDirectoryToFile(self, apprepozipfile=None, apprepotargetdir=None, apprepotargettype="sast"):

        sAppRepoZipFile = apprepozipfile;

        if sAppRepoZipFile != None:

            sAppRepoZipFile = sAppRepoZipFile.strip();

        if sAppRepoZipFile == None or \
            len(sAppRepoZipFile) < 1:

            print("");
            print("%s NO Application Repo 'target' Zip file has been specified nor defined - this MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        sAppRepoZipFilespec = sAppRepoZipFile;

        sAppRepoTargetDir = apprepotargetdir;

        if sAppRepoTargetDir != None:

            sAppRepoTargetDir = sAppRepoTargetDir.strip();

        if sAppRepoTargetDir == None or \
            len(sAppRepoTargetDir) < 1:

            print("");
            print("%s NO Application Repo 'target' directory has been specified nor defined - this MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        sAppRepoTargetDirspec = os.path.realpath(sAppRepoTargetDir);

        if not os.path.isdir(sAppRepoTargetDirspec):

            print("");
            print("%s The Application Repo 'target' directory of [%s] is NOT a valid directory - a valid directory MUST be supplied - Warning!" % (self.sClassDisp, sAppRepoTargetDirspec));
            print("");

            return False;

        sAppRepoTargetZipDirspec = os.path.join(sAppRepoTargetDirspec, "*");

        sAppRepoTargetType = apprepotargettype;

        if sAppRepoTargetType != None:

            sAppRepoTargetType = sAppRepoTargetType.strip();

        if sAppRepoTargetType == None or \
            len(sAppRepoTargetType) < 1:

            sAppRepoTargetType = "sast";

        if sAppRepoTargetType != "sast" and \
           sAppRepoTargetType != "osa":

            sAppRepoTargetType = "sast";

        bProcessingError = False;

        try:

            # Collect the --include parameter string.

            sAppZipInc = ' '.join(self.asCxApplicationZipInclude);

            # Generate the physical command line.

            sAppRepoZipCmd = None;

            if self.bPlatformIsWindows == True:

                if sAppRepoTargetType == "sast":

                #   7z a -r -tzip C:\public_hda2\JWeb.Software\CheckMarx_Projects\Python_Utilities\CxRestAPI\JwsDev_WorkDir\JWebsoftwareDev_JWS_App-Project_1.zip *.cpp *.java *.swift
                #   sAppRepoZipCmd = "7z %s %s --include %s" % (sAppRepoZipFile, sAppRepoTargetDirspec, sAppZipInc);
                    sAppRepoZipCmd = "7z a -r -tzip %s %s" % (sAppRepoZipFile, sAppZipInc);

                else:

                    sAppRepoZipCmd = "7z a -r -tzip %s *" % (sAppRepoZipFile);

            else:

                if sAppRepoTargetType == "sast":

                    sAppRepoZipCmd = "zip -r %s %s --include %s" % (sAppRepoZipFile, sAppRepoTargetZipDirspec, sAppZipInc);

                else:

                    sAppRepoZipCmd = "zip -r %s %s" % (sAppRepoZipFile, sAppRepoTargetZipDirspec);

            if sAppRepoZipCmd != None:

                sAppRepoZipCmd = sAppRepoZipCmd.strip();

            if sAppRepoZipCmd == None or \
                len(sAppRepoZipCmd) < 1:

                print("");
                print("%s The Application Repo 'zip' command failed to generate - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("%s Running the 'zip' command for [%s] of [%s]..." % (self.sClassDisp, sAppRepoTargetType, sAppRepoZipCmd));

            sAppRepoOrigCwd = os.getcwd();

            # Run the command to 'zip' the Working directory:

            if self.bPlatformIsWindows == True:

                os.chdir(sAppRepoTargetDirspec);

            zipCmdProcess = subprocess.run(sAppRepoZipCmd, shell=True, text=True, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT); 
            sZipCmdStdout = zipCmdProcess.stdout;
            sZipCmdStderr = zipCmdProcess.stderr;

            if self.bPlatformIsWindows == True:

                os.chdir(sAppRepoOrigCwd);

            if sZipCmdStdout != None and \
                len(sZipCmdStdout) > 0:

                print("%s 'stdout' from the 'zip' command of [%s] is:" % (self.sClassDisp, sAppRepoZipCmd));
                print(sZipCmdStdout);

            if sZipCmdStderr != None and \
                len(sZipCmdStderr) > 0:

                print("%s 'stderr' from the 'zip' command of [%s] is:" % (self.sClassDisp, sAppRepoZipCmd));
                print(sZipCmdStderr);

            zipCmdCmdRC = zipCmdProcess.returncode;

            if zipCmdCmdRC != 0:

                print("%s The 'zip' command of [%s] returned a 'bad' (NON-Zero) RC of [%d]..." % (self.sClassDisp, sAppRepoZipCmd, zipCmdCmdRC));

            else:

                print("%s The 'zip' command of [%s] returned a 'good' RC of [%d]..." % (self.sClassDisp, sAppRepoZipCmd, zipCmdCmdRC));

        except Exception as inst:

            print("%s '__zipCxAppRepoWorkDirectoryToFile()' [%s] - exception occured..." % (self.sClassDisp, sAppRepoTargetType));
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

