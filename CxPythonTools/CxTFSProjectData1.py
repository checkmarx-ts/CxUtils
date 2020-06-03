
import os;
import traceback;
import re;
import string;
import sys;
import collections;
import plistlib;

class CxTFSProjectData(object):

    sClassMod                 = __name__;
    sClassId                  = "CxTFSProjectData";
    sClassVers                = "(v1.0316)";
    sClassDisp                = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                = False;

    sCxProjectId              = "-undefined-";
    sCxProjectName            = None;
    sCxProjectDetailsURL      = None;
    sCxProjectState           = None;
    sCxProjectRevision        = None;
    bCxProjectIsPublic        = False;

    sCxProjectCollectionURL   = None;
    sCxProjectTeamId          = None;
    sCxProjectTeamName        = None;
    sCxProjectTeamURL         = None;
    sCxProjectTeamDescription = None;
    sCxProjectTeamIdentityURL = None;
    sCxProjectTeamProjectName = None;
    sCxProjectTeamProjectId   = None;

    dictCxProjectLinks        = None;
    dictCxProjectDefaultTeam  = None;
    dictCxProjectCollection   = None;
    dictCxProjectTeam         = None;
    dictCxProjectTeamIdentity = None;

    listCxProjectRepos        = None;       # A 'list' of Dictionaries for the Repo(s) of a Project...

    def __init__(self, trace=False, cxprojectid=0, cxprojectname=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxProjectId(cxprojectid=cxprojectid);
            self.setCxProjectName(cxprojectname=cxprojectname);

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

    def getCxProjectId(self):

        return self.sCxProjectId;

    def setCxProjectId(self, cxprojectid=None):

        if cxprojectid == None:

            return;

        if type(cxprojectid) == str:

            self.sCxProjectId = cxprojectid;

            if self.sCxProjectId != None:

                self.sCxProjectId = self.sCxProjectId.strip();

            if self.sCxProjectId == None or \
               len(self.sCxProjectId) < 1:

                self.sCxProjectId = "";

        else:

            iCxProjectId = cxprojectid;

            if iCxProjectId < 0:

                self.sCxProjectId = "";

            else:

                self.sCxProjectId = ("%d" % iCxProjectId);

    def getCxProjectName(self):

        return self.sCxProjectName;

    def setCxProjectName(self, cxprojectname=None):

        self.sCxProjectName = cxprojectname;

        if self.sCxProjectName == None or \
           len(self.sCxProjectName) < 1:

            self.sCxProjectName = None;

    def getCxProjectDetailsURL(self):

        return self.sCxProjectDetailsURL;

    def setCxProjectDetailsURL(self, cxprojectdetailsurl=None):

        self.sCxProjectDetailsURL = cxprojectdetailsurl;

        if self.sCxProjectDetailsURL == None or \
           len(self.sCxProjectDetailsURL) < 1:

            self.sCxProjectDetailsURL = None;

    def getCxProjectState(self):

        return self.sCxProjectState;

    def setCxProjectState(self, cxprojectstate=None):

        self.sCxProjectState = cxprojectstate;

        if self.sCxProjectState == None or \
           len(self.sCxProjectState) < 1:

            self.sCxProjectState = None;

    def getCxProjectRevision(self):

        return self.sCxProjectRevision;

    def setCxProjectRevision(self, cxprojectrevision=None):

        self.sCxProjectRevision = cxprojectrevision;

        if self.sCxProjectRevision == None or \
           len(self.sCxProjectRevision) < 1:

            self.sCxProjectRevision = None;

    def getCxProjectIsPublic(self):

        return self.bCxProjectIsPublic;

    def setCxProjectIsPublic(self, cxprojectispublic=False):

        self.bCxProjectIsPublic = cxprojectispublic;

    def getCxProjectCollectionURL(self):

        return self.sCxProjectCollectionURL;

    def setCxProjectCollectionURL(self, cxprojectcollectionurl=None):

        self.sCxProjectCollectionURL = cxprojectcollectionurl;

        if self.sCxProjectCollectionURL == None or \
           len(self.sCxProjectCollectionURL) < 1:

            self.sCxProjectCollectionURL = None;

    def getCxProjectTeamId(self):

        return self.sCxProjectTeamId;

    def setCxProjectTeamId(self, cxprojectteamid=None):

        self.sCxProjectTeamId = cxprojectteamid;

        if self.sCxProjectTeamId == None or \
           len(self.sCxProjectTeamId) < 1:

            self.sCxProjectTeamId = None;

    def getCxProjectTeamName(self):

        return self.sCxProjectTeamName;

    def setCxProjectTeamName(self, cxprojectteamname=None):

        self.sCxProjectTeamName = cxprojectteamname;

        if self.sCxProjectTeamName == None or \
           len(self.sCxProjectTeamName) < 1:

            self.sCxProjectTeamName = None;

    def getCxProjectTeamURL(self):

        return self.sCxProjectTeamURL;

    def setCxProjectTeamURL(self, cxprojectteamurl=None):

        self.sCxProjectTeamURL = cxprojectteamurl;

        if self.sCxProjectTeamURL == None or \
           len(self.sCxProjectTeamURL) < 1:

            self.sCxProjectTeamURL = None;

    def getCxProjectTeamDescription(self):

        return self.sCxProjectTeamDescription;

    def setCxProjectTeamDescription(self, cxprojectteamdescription=None):

        self.sCxProjectTeamDescription = cxprojectteamdescription;

        if self.sCxProjectTeamDescription == None or \
           len(self.sCxProjectTeamDescription) < 1:

            self.sCxProjectTeamDescription = None;

    def getCxProjectTeamIdentityURL(self):

        return self.sCxProjectTeamIdentityURL;

    def setCxProjectTeamIdentityURL(self, cxprojectteamidentityurl=None):

        self.sCxProjectTeamIdentityURL = cxprojectteamidentityurl;

        if self.sCxProjectTeamIdentityURL == None or \
           len(self.sCxProjectTeamIdentityURL) < 1:

            self.sCxProjectTeamIdentityURL = None;

    def getCxProjectTeamProjectName(self):

        return self.sCxProjectTeamProjectName;

    def setCxProjectTeamProjectName(self, cxprojectteamprojectname=None):

        self.sCxProjectTeamProjectName = cxprojectteamprojectname;

        if self.sCxProjectTeamProjectName == None or \
           len(self.sCxProjectTeamProjectName) < 1:

            self.sCxProjectTeamProjectName = None;

    def getCxProjectTeamProjectId(self):

        return self.sCxProjectTeamProjectId;

    def setCxProjectTeamProjectId(self, cxprojectteamprojectid=None):

        self.sCxProjectTeamProjectId = cxprojectteamprojectid;

        if self.sCxProjectTeamProjectId == None or \
           len(self.sCxProjectTeamProjectId) < 1:

            self.sCxProjectTeamProjectId = None;

    def getCxProjectLinks(self):

        return self.dictCxProjectLinks;

    def setCxProjectLinks(self, cxprojectlinks=None):

        self.dictCxProjectLinks = cxprojectlinks;

        if self.dictCxProjectLinks == None or \
           len(self.dictCxProjectLinks) < 1:

            self.dictCxProjectLinks = None;

    def getCxProjectDefaultTeam(self):

        return self.dictCxProjectDefaultTeam;

    def setCxProjectDefaultTeam(self, cxprojectdefaultteam=None):

        self.dictCxProjectDefaultTeam = cxprojectdefaultteam;

        if self.dictCxProjectDefaultTeam == None or \
           len(self.dictCxProjectDefaultTeam) < 1:

            self.dictCxProjectDefaultTeam = None;

    def getCxProjectCollection(self):

        return self.dictCxProjectCollection;

    def setCxProjectCollection(self, cxprojectcollection=None):

        self.dictCxProjectCollection = cxprojectcollection;

        if self.dictCxProjectCollection == None or \
           len(self.dictCxProjectCollection) < 1:

            self.dictCxProjectCollection = None;

    def getCxProjectTeam(self):

        return self.dictCxProjectTeam;

    def setCxProjectTeam(self, cxprojectteam=None):

        self.dictCxProjectTeam = cxprojectteam;

        if self.dictCxProjectTeam == None or \
           len(self.dictCxProjectTeam) < 1:

            self.dictCxProjectTeam = None;

    def getCxProjectTeamIdentity(self):

        return self.dictCxProjectTeamIdentity;

    def setCxProjectTeamIdentity(self, cxprojectteamidentity=None):

        self.dictCxProjectTeamIdentity = cxprojectteamidentity;

        if self.dictCxProjectTeamIdentity == None or \
           len(self.dictCxProjectTeamIdentity) < 1:

            self.dictCxProjectTeamIdentity = None;

    def getCxProjectRepos(self):

        return self.listCxProjectRepos;

    def setCxProjectRepos(self, cxprojectrepos=None):

        self.listCxProjectRepos = cxprojectrepos;

        if self.listCxProjectRepos == None or \
           len(self.listCxProjectRepos) < 1:

            self.listCxProjectRepos = None;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'sCxProjectId' is [%s]..." % (self.sClassDisp, self.sCxProjectId));
            print("%s The contents of 'sCxProjectName' is [%s]..." % (self.sClassDisp, self.sCxProjectName));
            print("%s The contents of 'sCxProjectDetailsURL' is [%s]..." % (self.sClassDisp, self.sCxProjectDetailsURL));
            print("%s The contents of 'sCxProjectState' is [%s]..." % (self.sClassDisp, self.sCxProjectState));
            print("%s The contents of 'sCxProjectRevision' is [%s]..." % (self.sClassDisp, self.sCxProjectRevision));
            print("%s The contents of 'bCxProjectIsPublic' is [%s]..." % (self.sClassDisp, self.bCxProjectIsPublic));
            print("%s The contents of 'sCxProjectCollectionURL' is [%s]..." % (self.sClassDisp, self.sCxProjectCollectionURL));
            print("%s The contents of 'sCxProjectTeamId' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamId));
            print("%s The contents of 'sCxProjectTeamName' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamName));
            print("%s The contents of 'sCxProjectTeamURL' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamURL));
            print("%s The contents of 'sCxProjectTeamDescription' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamDescription));
            print("%s The contents of 'sCxProjectTeamIdentityURL' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamIdentityURL));
            print("%s The contents of 'sCxProjectTeamProjectName' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamProjectName));
            print("%s The contents of 'sCxProjectTeamProjectId' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamProjectId));
            print("%s The contents of 'dictCxProjectLinks' is [%s]..." % (self.sClassDisp, self.dictCxProjectLinks));
            print("%s The contents of 'dictCxProjectDefaultTeam' is [%s]..." % (self.sClassDisp, self.dictCxProjectDefaultTeam));
            print("%s The contents of 'dictCxProjectCollection' is [%s]..." % (self.sClassDisp, self.dictCxProjectCollection));
            print("%s The contents of 'dictCxProjectTeam' is [%s]..." % (self.sClassDisp, self.dictCxProjectTeam));
            print("%s The contents of 'dictCxProjectTeamIdentity' is [%s]..." % (self.sClassDisp, self.dictCxProjectTeamIdentity));
            print("%s The contents of 'listCxProjectRepos' is [%s]..." % (self.sClassDisp, self.listCxProjectRepos));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'sCxProjectId' is [%s], " % (self.sCxProjectId));
        asObjDetail.append("'sCxProjectName' is [%s], " % (self.sCxProjectName));
        asObjDetail.append("'sCxProjectDetailsURL' is [%s], " % (self.sCxProjectDetailsURL));
        asObjDetail.append("'sCxProjectState' is [%s], " % (self.sCxProjectState));
        asObjDetail.append("'sCxProjectRevision' is [%s], " % (self.sCxProjectRevision));
        asObjDetail.append("'bCxProjectIsPublic' is [%s], " % (self.bCxProjectIsPublic));
        asObjDetail.append("'sCxProjectCollectionURL' is [%s], " % (self.sCxProjectCollectionURL));
        asObjDetail.append("'sCxProjectTeamId' is [%s], " % (self.sCxProjectTeamId));
        asObjDetail.append("'sCxProjectTeamName' is [%s], " % (self.sCxProjectTeamName));
        asObjDetail.append("'sCxProjectTeamURL' is [%s], " % (self.sCxProjectTeamURL));
        asObjDetail.append("'sCxProjectTeamDescription' is [%s], " % (self.sCxProjectTeamDescription));
        asObjDetail.append("'sCxProjectTeamIdentityURL' is [%s], " % (self.sCxProjectTeamIdentityURL));
        asObjDetail.append("'sCxProjectTeamProjectName' is [%s], " % (self.sCxProjectTeamProjectName));
        asObjDetail.append("'sCxProjectTeamProjectId' is [%s], " % (self.sCxProjectTeamProjectId));
        asObjDetail.append("'dictCxProjectLinks' is [%s], " % (self.dictCxProjectLinks));
        asObjDetail.append("'dictCxProjectDefaultTeam' is [%s], " % (self.dictCxProjectDefaultTeam));
        asObjDetail.append("'dictCxProjectCollection' is [%s], " % (self.dictCxProjectCollection));
        asObjDetail.append("'dictCxProjectTeam' is [%s], " % (self.dictCxProjectTeam));
        asObjDetail.append("'dictCxProjectTeamIdentity' is [%s], " % (self.dictCxProjectTeamIdentity));
        asObjDetail.append("'listCxProjectRepos' is [%s]. " % (self.listCxProjectRepos));

        return ''.join(asObjDetail);

    def toPrettyString(self):

        asObjDetail = list();

        asObjDetail.append("Project ");
        asObjDetail.append("'Id' [%-s], "               % (self.sCxProjectId));
        asObjDetail.append("'Name' [%s], "              % (self.sCxProjectName));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Is Public?' [%5s], "       % (self.bCxProjectIsPublic));
        asObjDetail.append("'State' [%s], "             % (self.sCxProjectState));
        asObjDetail.append("'Revision' [%s], "          % (self.sCxProjectRevision));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Details URL' [%s], "       % (self.sCxProjectDetailsURL));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Collection URL' [%s], "    % (self.sCxProjectCollectionURL));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team URL' [%s], "          % (self.sCxProjectTeamURL));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team Identity URL' [%s], " % (self.sCxProjectTeamIdentityURL));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team Id' [%s], "           % (self.sCxProjectTeamId));
        asObjDetail.append("'Team Name' [%s], "         % (self.sCxProjectTeamName));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team Project Id' [%s], "   % (self.sCxProjectTeamProjectId));
        asObjDetail.append("'Team Project Name' [%s], " % (self.sCxProjectTeamProjectName));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team Description' [%s], "  % (self.sCxProjectTeamDescription));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Links' [%s], "             % (self.dictCxProjectLinks));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'DefaultTeam' [%s], "       % (self.dictCxProjectDefaultTeam));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Collection' [%s], "        % (self.dictCxProjectCollection));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team' [%s], "              % (self.dictCxProjectTeam));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team Identity' [%s], "     % (self.dictCxProjectTeamIdentity));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Repo(s)' [%s]. "           % (self.listCxProjectRepos));
        asObjDetail.append("\n");
        asObjDetail.append("........");

        return ''.join(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def populateCxTFSProjectDataFromJsonDictionary(self, dictcxtfsprojectdata=None):
 
        bProcessingError = False;

        if dictcxtfsprojectdata == None:

            return False;

        dictCxTFSProjectData = dictcxtfsprojectdata;

        if dictCxTFSProjectData == None or \
            len(dictCxTFSProjectData) < 1:

            print("");
            print("%s NO Checkmarx CxTFSProjectData dictionary object has been supplied - at CxTFSProjectData dictionary MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            # --------------------------------------------------------------------------------------------------
            # {
            #  "id": "705ff45a-11cf-406d-8e04-823aff3b3ab6",
            #  "name": "TFSSampleProject1",
            #  "url": "http://192.168.2.190:9080/tfs/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6",
            #  "state": "wellFormed",
            #  "revision": 8,
            #  "visibility": "private"
            # }
            # --------------------------------------------------------------------------------------------------

            sTFSProjectId         = dictCxTFSProjectData["id"];
            sTFSProjectName       = dictCxTFSProjectData["name"];
            sTFSProjectDetailsURL = dictCxTFSProjectData["url"];
            sTFSProjectState      = dictCxTFSProjectData["state"];
            iTFSProjectRevision   = dictCxTFSProjectData["revision"];
            sTFSProjectVisibility = dictCxTFSProjectData["visibility"];

            if sTFSProjectId != None:

                sTFSProjectId = sTFSProjectId.strip();

            if sTFSProjectId == None or \
                len(sTFSProjectId) < 1:

                self.sCxProjectId = None;

            else:

                self.sCxProjectId = sTFSProjectId;
            
            if sTFSProjectName != None:

                sTFSProjectName = sTFSProjectName.strip();

            if sTFSProjectName == None or \
                len(sTFSProjectName) < 1:

                self.sCxProjectName = None;

            else:

                self.sCxProjectName = sTFSProjectName;

            if sTFSProjectDetailsURL != None:

                sTFSProjectDetailsURL = sTFSProjectDetailsURL.strip();

            if sTFSProjectDetailsURL == None or \
                len(sTFSProjectDetailsURL) < 1:

                self.sCxProjectDetailsURL = None;

            else:

                self.sCxProjectDetailsURL = sTFSProjectDetailsURL;

            if sTFSProjectState != None:

                sTFSProjectState = sTFSProjectState.strip();

            if sTFSProjectState == None or \
                len(sTFSProjectState) < 1:

                self.sCxProjectState = None;

            else:

                self.sCxProjectState = sTFSProjectState;

            self.sCxProjectRevision = "%d" % (iTFSProjectRevision);

            sTFSProjectVisibilityLow = sTFSProjectVisibility.lower();

            if sTFSProjectVisibilityLow == "private":

                self.bCxProjectIsPublic = False;

            else:

                self.bCxProjectIsPublic = True;

        except Exception as inst:
 
            print("%s 'populateCxTFSProjectDataFromJsonDictionary()' - exception occured..." % (self.sClassDisp));
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
 
    def saveCxTFSProjectDataAsPlistToDirectory(self, outputprojectdataplistdir=None, cxtfscollection=None):

        sOutputProjectDataPlistDirspec = outputprojectdataplistdir;

        if sOutputProjectDataPlistDirspec != None:

            sOutputProjectDataPlistDirspec = sOutputProjectDataPlistDirspec.strip();

        if sOutputProjectDataPlistDirspec == None or \
            len(sOutputProjectDataPlistDirspec) < 1:

            print("");
            print("%s The supplied (Output) 'plist' directory is None or Empty - this MUST be supplied - Error!" % (self.sClassDisp));
            print("");

            return False;

        sCxTFSCollectionName = cxtfscollection;

        if sCxTFSCollectionName != None:

            sCxTFSCollectionName = sCxTFSCollectionName.strip();

        if sCxTFSCollectionName == None or \
            len(sCxTFSCollectionName) < 1:

            sCxTFSCollectionName = "-unknown-";

        bProcessingError = False;

        try:

            # --------------------------------------------------------------------------------------------------
            # [
            #   {
            #       "id": "6f23a004-735a-4df6-909b-17571d9f06b1",
            #       "name": "JWS_App-Project_1",
            #       "url": "http://192.168.2.190:9080/tfs/JWebsoftwareDev/_apis/git/repositories/6f23a004-735a-4df6-909b-17571d9f06b1",
            #       "project": {
            #           "id": "dc408339-e04f-4582-9b50-65e9182fcb3a",
            #           "name": "JWS_App-Project_1",
            #           "description": "JWS_App-Project_1 description",
            #           "url": "http://192.168.2.190:9080/tfs/JWebsoftwareDev/_apis/projects/dc408339-e04f-4582-9b50-65e9182fcb3a",
            #           "state": "wellFormed",
            #           "revision": 9,
            #           "visibility": "private"
            #       },
            #       "defaultBranch": "refs/heads/master",
            #       "remoteUrl": "http://darylc-laptop:9080/tfs/JWebsoftwareDev/_git/JWS_App-Project_1",
            #       "sshUrl": "ssh://darylc-laptop:22/tfs/JWebsoftwareDev/_git/JWS_App-Project_1"
            #   }
            # ]
            # --------------------------------------------------------------------------------------------------

            # Generate the (Output) 'plist' Array of Repo Dictionaries:

            listOutputCxProjectRepos = [];

            for cxProjectRepo in self.listCxProjectRepos:

                if cxProjectRepo == None or \
                   type(cxProjectRepo) != dict or \
                   len(cxProjectRepo) < 1:

                    continue;

                dictCxProjectRepo         = {}; 
                listCxProjectRepoBranches = [];
                dictCxProjectRepoBranch   = {};

                dictCxProjectRepoBranch["BranchIsActive"] = "true";
                dictCxProjectRepoBranch["BranchName"]     = cxProjectRepo["defaultBranch"];

                listCxProjectRepoBranches.append(dictCxProjectRepoBranch);

                dictCxProjectRepo = {}; 

                dictCxProjectRepo["RepoTitle"]     = cxProjectRepo["name"];
                dictCxProjectRepo["RepoIsActive"]  = "true";
                dictCxProjectRepo["RepoURL"]       = cxProjectRepo["url"];
                dictCxProjectRepo["RepoRemoteURL"] = cxProjectRepo["remoteUrl"];
                dictCxProjectRepo["RepoSshURL"]    = cxProjectRepo["sshUrl"];
                dictCxProjectRepo["RepoBranches"]  = listCxProjectRepoBranches;

                listOutputCxProjectRepos.append(dictCxProjectRepo);

            # Generate the (Output) 'plist' Dictionary:

            dictOutputCxProjectPlist = {};

            dictOutputCxProjectPlist["AppName"]           = self.sCxProjectName;
            dictOutputCxProjectPlist["AppIsActive"]       = "true";
            dictOutputCxProjectPlist["AppCollectionName"] = sCxTFSCollectionName;
            dictOutputCxProjectPlist["AppProjectId"]      = self.sCxProjectId;
            dictOutputCxProjectPlist["AppRepos"]          = listOutputCxProjectRepos;

            # Generate the (Output) 'plist' file from the Dictionary:

            sOutputCxProjectFile = os.path.join(sOutputProjectDataPlistDirspec, ("%s.plist" % (self.sCxProjectName)));

            print("%s Generating the (Output) 'plist' file of [%s]..." % (self.sClassDisp, sOutputCxProjectFile));

            plistlib.writePlist(dictOutputCxProjectPlist, sOutputCxProjectFile);

            print("%s Generated the (Output) 'plist' file of [%s]..." % (self.sClassDisp, sOutputCxProjectFile));
            print("");

        except Exception as inst:
 
            print("%s 'saveCxTFSProjectDataAsPlistToDirectory()' - exception occured..." % (self.sClassDisp));
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
 
