
import os;
import traceback;
import re;
import string;
import sys;
import collections;

class CxProjectCreation:

    sClassMod                  = __name__;
    sClassId                   = "CxProjectCreation";
    sClassVers                 = "(v1.0532)";
    sClassDisp                 = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                 = False;

    sCxProjectBaseName         = None;
    sCxProjectName             = None;
    bCxProjectIsPublic         = False;
    sCxProjectScanType         = None;
    sCxProjectTeam             = None;
    sCxProjectVersion          = None;
    sCxProjectTeamName         = None;
    sCxProjectPresetName       = None;
    sCxProjectEngineConfigName = None;
    asCxProjectBranchNames     = None;          # Array of 'name(s)' of 'branches' of a given Project.

    # Fields that are determined by 'lookup' or Rest API response:

    sCxProjectId               = None;
    sCxProjectTeamId           = None;
    sCxProjectPresetId         = None;
    sCxProjectEngineConfigId   = None;
    dictCxProjectBranchedNames = None;          # Dictionary of 'branched' Project 'name(s)': ["project-branch-name", "project-branch_project-id"]

    # Fields that can be used to 'anchor' other item(s):

    objCxProjectExtraField1    = None;          # AppCollectionName
    objCxProjectExtraField2    = None;          # AooRepos (Application 'repo(s)' dictionary)
    objCxProjectExtraField3    = None;          # Cx 'sast' Scan data
    objCxProjectExtraField4    = None;          # Cx 'osa' Scan data

    # Fields that control 'scan' of the Project:

    sCxProjectSASTZipFilespec  = None;
    sCxProjectOSAZipFilespec   = None;

    def __init__(self, trace=False, cxprojectname=None, cxprojectispublic=True, cxprojectscantype=None, cxprojectteamname=None, cxprojectpresetname=None, cxprojectengineconfigname=None, cxprojectbranchnames=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxProjectName(cxprojectname=cxprojectname);
            self.setCxProjectIsPublic(cxprojectispublic=cxprojectispublic);
            self.setCxProjectScanType(cxprojectscantype=cxprojectscantype);
            self.setCxProjectTeamName(cxprojectteamname=cxprojectteamname);
            self.setCxProjectPresetName(cxprojectpresetname=cxprojectpresetname);
            self.setCxProjectEngineConfigName(cxprojectengineconfigname=cxprojectengineconfigname);
            self.setCxProjectBranchNames(cxprojectbranchnames=cxprojectbranchnames);

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

    def getCxProjectBaseName(self):

        return self.sCxProjectBaseName;

    def setCxProjectBaseName(self, cxprojectbasename=None):

        self.sCxProjectBaseName = cxprojectbasename;

        if self.sCxProjectBaseName != None:

            self.sCxProjectBaseName = self.sCxProjectBaseName.strip();

        if self.sCxProjectBaseName == None or \
           len(self.sCxProjectBaseName) < 1:
         
            self.sCxProjectBaseName = None;
         
    def getCxProjectName(self):

        return self.sCxProjectName;

    def setCxProjectName(self, cxprojectname=None):

        self.sCxProjectName = cxprojectname;

        if self.sCxProjectName != None:

            self.sCxProjectName = self.sCxProjectName.strip();

        if self.sCxProjectName == None or \
           len(self.sCxProjectName) < 1:

            self.sCxProjectName = None;

    def getCxProjectIsPublic(self):

        return self.bCxProjectIsPublic;

    def setCxProjectIsPublic(self, cxprojectispublic=False):

        self.bCxProjectIsPublic = cxprojectispublic;

    def getCxProjectScanType(self):

        return self.sCxProjectScanType;

    def setCxProjectScanType(self, cxprojectscantype=None):

        self.sCxProjectScanType = cxprojectscantype;

        if self.sCxProjectScanType != None:

            self.sCxProjectScanType = self.sCxProjectScanType.strip();

        if self.sCxProjectScanType == None or \
            len(self.sCxProjectScanType) < 1:

            self.sCxProjectScanType = None;

            return;

        self.sCxProjectScanType = self.sCxProjectScanType.lower();

        if self.sCxProjectScanType != "both" and \
           self.sCxProjectScanType != "sast" and \
           self.sCxProjectScanType != "osa":

            self.sCxProjectScanType = None;

    def getCxProjectTeam(self):

        return self.sCxProjectTeam;

    def setCxProjectTeam(self, cxprojectteam=None):

        self.sCxProjectTeam = cxprojectteam;

        if self.sCxProjectTeam != None:

            self.sCxProjectTeam = self.sCxProjectTeam.strip();

        if self.sCxProjectTeam == None or \
           len(self.sCxProjectTeam) < 1:

            self.sCxProjectTeam = None;

    def getCxProjectVersion(self):

        return self.sCxProjectVersion;

    def setCxProjectVersion(self, cxprojectversion=None):

        self.sCxProjectVersion = cxprojectversion;

        if self.sCxProjectVersion != None:

            self.sCxProjectVersion = self.sCxProjectVersion.strip();

        if self.sCxProjectVersion == None or \
           len(self.sCxProjectVersion) < 1:

            self.sCxProjectVersion = None;

    def getCxProjectTeamName(self):

        return self.sCxProjectTeamName;

    def setCxProjectTeamName(self, cxprojectteamname=None):

        self.sCxProjectTeamName = cxprojectteamname;

        if self.sCxProjectTeamName != None:

            self.sCxProjectTeamName = self.sCxProjectTeamName.strip();

        if self.sCxProjectTeamName == None or \
           len(self.sCxProjectTeamName) < 1:

            self.sCxProjectTeamName = None;

    def getCxProjectPresetName(self):

        return self.sCxProjectPresetName;

    def setCxProjectPresetName(self, cxprojectpresetname=None):

        self.sCxProjectPresetName = cxprojectpresetname;

        if self.sCxProjectPresetName != None:

            self.sCxProjectPresetName = self.sCxProjectPresetName.strip();

        if self.sCxProjectPresetName == None or \
           len(self.sCxProjectPresetName) < 1:

            self.sCxProjectPresetName = None;

    def getCxProjectEngineConfigName(self):

        return self.sCxProjectEngineConfigName;

    def setCxProjectEngineConfigName(self, cxprojectengineconfigname=None):

        self.sCxProjectEngineConfigName = cxprojectengineconfigname;

        if self.sCxProjectEngineConfigName != None:

            self.sCxProjectEngineConfigName = self.sCxProjectEngineConfigName.strip();

        if self.sCxProjectEngineConfigName == None or \
           len(self.sCxProjectEngineConfigName) < 1:

            self.sCxProjectEngineConfigName = None;

    def getCxProjectBranchNames(self):

        return self.asCxProjectBranchNames;

    def setCxProjectBranchNames(self, cxprojectbranchnames=None):

        if cxprojectbranchnames == None:

            return;

        sCxProjectBranchNames   = cxprojectbranchnames;
        asSetProjectBranchNames = None;

        if type(sCxProjectBranchNames) == list:

            asSetProjectBranchNames = sCxProjectBranchNames;

        else:

            if type(sCxProjectBranchNames) == str:

                if sCxProjectBranchNames != None:

                    sCxProjectBranchNames = sCxProjectBranchNames.strip();

                if sCxProjectBranchNames == None or \
                    len(sCxProjectBranchNames) < 1:

                    self.asCxProjectBranchNames = None;

                    return;

                asSetProjectBranchNames = sCxProjectBranchNames.split(',');

        if asSetProjectBranchNames == None or \
           len(asSetProjectBranchNames) < 1:

            self.asCxProjectBranchNames = None;

            return;

        for sSetProjectBranchName in asSetProjectBranchNames:

            sSetProjectBranchName = sSetProjectBranchName.strip();

            if sSetProjectBranchName == None or \
               len(sSetProjectBranchName) < 1:

                continue;

            if self.asCxProjectBranchNames == None:

                self.asCxProjectBranchNames = [];

            self.asCxProjectBranchNames.append(sSetProjectBranchName);

    # Fields that are determined by 'lookup' or Rest API response:

    def getCxProjectId(self):

        return self.sCxProjectId;

    def setCxProjectId(self, cxprojectid=None):

        if type(cxprojectid) == str:

            self.sCxProjectId = cxprojectid;

            if self.sCxProjectId != None:

                self.sCxProjectId = self.sCxProjectId.strip();

            if self.sCxProjectId == None or \
               len(self.sCxProjectId) < 1:

                self.sCxProjectId = "";

        else:

            self.sCxProjectId = ("%d" % cxprojectid);

    def getCxProjectTeamId(self):

        return self.sCxProjectTeamId;

    def setCxProjectTeamId(self, cxprojectteamid=None):

        self.sCxProjectTeamId = cxprojectteamid;

        if self.sCxProjectTeamId == None or \
           len(self.sCxProjectTeamId) < 1:

            self.sCxProjectTeamId = "";

    def getCxProjectPresetId(self):

        return self.sCxProjectPresetId;

    def setCxProjectPresetId(self, cxprojectpresetid=None):

        if type(cxprojectpresetid) == str:

            self.sCxProjectPresetId = cxprojectpresetid;

            if self.sCxProjectPresetId != None:

                self.sCxProjectPresetId = self.sCxProjectPresetId.strip();

            if self.sCxProjectPresetId == None or \
               len(self.sCxProjectPresetId) < 1:

                self.sCxProjectPresetId = "";

        else:

            self.sCxProjectPresetId = ("%d" % cxprojectpresetid);

    def getCxProjectEngineConfigId(self):

        return self.sCxProjectEngineConfigId;

    def setCxProjectEngineConfigId(self, cxprojectengineconfigid=None):

        if type(cxprojectengineconfigid) == str:

            self.sCxProjectEngineConfigId = cxprojectengineconfigid;

            if self.sCxProjectEngineConfigId != None:

                self.sCxProjectEngineConfigId = self.sCxProjectEngineConfigId.strip();

            if self.sCxProjectEngineConfigId == None or \
               len(self.sCxProjectEngineConfigId) < 1:

                self.sCxProjectEngineConfigId = "";

        else:

            self.sCxProjectEngineConfigId = ("%d" % cxprojectengineconfigid);

    def getCxProjectBranchedNames(self):

        return self.dictCxProjectBranchedNames;

    def setCxProjectBranchedNames(self, cxprojectbranchednames=None):

        if type(cxprojectbranchednames) == dict:

            self.dictCxProjectBranchedNames = cxprojectbranchednames;

            if self.dictCxProjectBranchedNames == None or \
               len(self.dictCxProjectBranchedNames) < 1:

                self.dictCxProjectBranchedNames = None;

        else:

            self.dictCxProjectBranchedNames = None;

    # Extra field(s):

    def getCxProjectExtraField1(self):

        return self.objCxProjectExtraField1;

    def setCxProjectExtraField1(self, cxprojectextrafield1=False):

        self.objCxProjectExtraField1 = cxprojectextrafield1;

    def getCxProjectExtraField2(self):

        return self.objCxProjectExtraField2;

    def setCxProjectExtraField2(self, cxprojectextrafield2=False):

        self.objCxProjectExtraField2 = cxprojectextrafield2;

    def getCxProjectExtraField3(self):

        return self.objCxProjectExtraField3;

    def setCxProjectExtraField3(self, cxprojectextrafield3=False):

        self.objCxProjectExtraField3 = cxprojectextrafield3;

    def getCxProjectExtraField4(self):

        return self.objCxProjectExtraField4;

    def setCxProjectExtraField4(self, cxprojectextrafield4=False):

        self.objCxProjectExtraField4 = cxprojectextrafield4;

    def getCxProjectSASTZipFilespec(self):

        return self.sCxProjectSASTZipFilespec;

    def setCxProjectSASTZipFilespec(self, cxprojectsastzipfilespec=False):

        self.sCxProjectSASTZipFilespec = cxprojectsastzipfilespec;

        if self.sCxProjectSASTZipFilespec != None:

            self.sCxProjectSASTZipFilespec = self.sCxProjectSASTZipFilespec.strip();

        if self.sCxProjectSASTZipFilespec == None or \
           len(self.sCxProjectSASTZipFilespec) < 1:

            self.sCxProjectSASTZipFilespec = None;

    def getCxProjectOSAZipFilespec(self):

        return self.sCxProjectOSAZipFilespec;

    def setCxProjectOSAZipFilespec(self, cxprojectosazipfilespec=False):

        self.sCxProjectOSAZipFilespec = cxprojectosazipfilespec;

        if self.sCxProjectOSAZipFilespec != None:

            self.sCxProjectOSAZipFilespec = self.sCxProjectOSAZipFilespec.strip();

        if self.sCxProjectOSAZipFilespec == None or \
           len(self.sCxProjectOSAZipFilespec) < 1:

            self.sCxProjectOSAZipFilespec = None;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'sCxProjectBaseName' is [%s]..." % (self.sClassDisp, self.sCxProjectBaseName));
            print("%s The contents of 'sCxProjectName' is [%s]..." % (self.sClassDisp, self.sCxProjectName));
            print("%s The contents of 'bCxProjectIsPublic' is [%s]..." % (self.sClassDisp, self.bCxProjectIsPublic));
            print("%s The contents of 'sCxProjectScanType' is [%s]..." % (self.sClassDisp, self.sCxProjectScanType));
            print("%s The contents of 'sCxProjectTeam' is [%s]..." % (self.sClassDisp, self.sCxProjectTeam));
            print("%s The contents of 'sCxProjectVersion' is [%s]..." % (self.sClassDisp, self.sCxProjectVersion));
            print("%s The contents of 'sCxProjectTeamName' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamName));
            print("%s The contents of 'sCxProjectPresetName' is [%s]..." % (self.sClassDisp, self.sCxProjectPresetName));
            print("%s The contents of 'sCxProjectEngineConfigName' is [%s]..." % (self.sClassDisp, self.sCxProjectEngineConfigName));
            print("%s The contents of 'asCxProjectBranchNames' is [%s]..." % (self.sClassDisp, self.asCxProjectBranchNames));
            print("%s The contents of 'sCxProjectId' is [%s]..." % (self.sClassDisp, self.sCxProjectId));
            print("%s The contents of 'sCxProjectTeamId' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamId));
            print("%s The contents of 'sCxProjectPresetId' is [%s]..." % (self.sClassDisp, self.sCxProjectPresetId));
            print("%s The contents of 'sCxProjectEngineConfigId' is [%s]..." % (self.sClassDisp, self.sCxProjectEngineConfigId));
            print("%s The contents of 'dictCxProjectBranchedNames' is [%s]..." % (self.sClassDisp, self.dictCxProjectBranchedNames));
            print("%s The contents of 'objCxProjectExtraField1' is [%s]..." % (self.sClassDisp, self.objCxProjectExtraField1));
            print("%s The contents of 'objCxProjectExtraField2' is [%s]..." % (self.sClassDisp, self.objCxProjectExtraField2));
            print("%s The contents of 'objCxProjectExtraField3' is [%s]..." % (self.sClassDisp, self.objCxProjectExtraField3));
            print("%s The contents of 'objCxProjectExtraField4' is [%s]..." % (self.sClassDisp, self.objCxProjectExtraField4));
            print("%s The contents of 'sCxProjectSASTZipFilespec' is [%s]..." % (self.sClassDisp, self.sCxProjectSASTZipFilespec));
            print("%s The contents of 'sCxProjectOSAZipFilespec' is [%s]..." % (self.sClassDisp, self.sCxProjectOSAZipFilespec));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'sCxProjectBaseName' is [%s], " % (self.sCxProjectBaseName));
        asObjDetail.append("'sCxProjectName' is [%s], " % (self.sCxProjectName));
        asObjDetail.append("'bCxProjectIsPublic' is [%s], " % (self.bCxProjectIsPublic));
        asObjDetail.append("'sCxProjectScanType' is [%s], " % (self.sCxProjectScanType));
        asObjDetail.append("'sCxProjectTeam' is [%s], " % (self.sCxProjectTeam));
        asObjDetail.append("'sCxProjectVersion' is [%s], " % (self.sCxProjectVersion));
        asObjDetail.append("'sCxProjectTeamName' is [%s], " % (self.sCxProjectTeamName));
        asObjDetail.append("'sCxProjectPresetName' is [%s], " % (self.sCxProjectPresetName));
        asObjDetail.append("'sCxProjectEngineConfigName' is [%s], " % (self.sCxProjectEngineConfigName));
        asObjDetail.append("'asCxProjectBranchNames' is [%s], " % (self.asCxProjectBranchNames));
        asObjDetail.append("'sCxProjectId' is [%s], " % (self.sCxProjectId));
        asObjDetail.append("'sCxProjectTeamId' is [%s], " % (self.sCxProjectTeamId));
        asObjDetail.append("'sCxProjectPresetId' is [%s], " % (self.sCxProjectPresetId));
        asObjDetail.append("'sCxProjectEngineConfigId' is [%s], " % (self.sCxProjectEngineConfigId));
        asObjDetail.append("'dictCxProjectBranchedNames' is [%s], " % (self.dictCxProjectBranchedNames));
        asObjDetail.append("'objCxProjectExtraField1' is [%s], " % (self.objCxProjectExtraField1));
        asObjDetail.append("'objCxProjectExtraField2' is [%s], " % (self.objCxProjectExtraField2));
        asObjDetail.append("'objCxProjectExtraField3' is [%s], " % (self.objCxProjectExtraField3));
        asObjDetail.append("'objCxProjectExtraField4' is [%s], " % (self.objCxProjectExtraField4));
        asObjDetail.append("'sCxProjectSASTZipFilespec' is [%s], " % (self.sCxProjectSASTZipFilespec));
        asObjDetail.append("'sCxProjectOSAZipFilespec' is [%s]. " % (self.sCxProjectOSAZipFilespec));

        return ''.join(asObjDetail);

    def toPrettyString(self):

        return self.toPrettyStringWithWidths();

    def toPrettyStringWithWidths(self, dictcxprojectcreationcollectionstats=None):

        dictCxProjectCreationCollectionStats = None;

        if dictcxprojectcreationcollectionstats != None:

            if self.bTraceFlag == True:

                print("%s 'dictcxprojectcreationcollectionstats' Type is [%s]..." % (self.sClassDisp, type(dictcxprojectcreationcollectionstats)));

            if type(dictcxprojectcreationcollectionstats) == dict or \
                type(dictcxprojectcreationcollectionstats) == collections.defaultdict:

                dictCxProjectCreationCollectionStats = dictcxprojectcreationcollectionstats;

            else:

                dictCxProjectCreationCollectionStats = collections.defaultdict(int);

        else:

            dictCxProjectCreationCollectionStats = collections.defaultdict(int);

        # Dictionary collection of 'width' counters...
        # Keys: "cWidthCxProjectName",
        #       "cWidthCxProjectId",
        #       "cWidthCxProjectTeamName",
        #       "cWidthCxProjectTeamId",
        #       "cWidthCxProjectPresetName",
        #       "cWidthCxProjectPresetId",
        #       "cWidthCxProjectEngineConfigName",
        #       "cWidthCxProjectEngineConfigId".
        # Note: ALL Key(s) are initialized to 0 (Zero).

        dictCxProjectCreationCollectionStats.setdefault("cWidthCxProjectName",             70);
        dictCxProjectCreationCollectionStats.setdefault("cWidthCxProjectId",               8);
        dictCxProjectCreationCollectionStats.setdefault("cWidthCxProjectTeamName",         48);
        dictCxProjectCreationCollectionStats.setdefault("cWidthCxProjectTeamId",           36);
        dictCxProjectCreationCollectionStats.setdefault("cWidthCxProjectPresetName",       48);
        dictCxProjectCreationCollectionStats.setdefault("cWidthCxProjectPresetId",         36);
        dictCxProjectCreationCollectionStats.setdefault("cWidthCxProjectEngineConfigName", 24);
        dictCxProjectCreationCollectionStats.setdefault("cWidthCxProjectEngineConfigId",   2);

        cWidthCxProjectName             = dictCxProjectCreationCollectionStats["cWidthCxProjectName"];    
        cWidthCxProjectId               = dictCxProjectCreationCollectionStats["cWidthCxProjectId"];    
        cWidthCxProjectTeamName         = dictCxProjectCreationCollectionStats["cWidthCxProjectTeamName"];    
        cWidthCxProjectTeamId           = dictCxProjectCreationCollectionStats["cWidthCxProjectTeamId"];    
        cWidthCxProjectPresetName       = dictCxProjectCreationCollectionStats["cWidthCxProjectPresetName"];    
        cWidthCxProjectPresetId         = dictCxProjectCreationCollectionStats["cWidthCxProjectPresetId"];    
        cWidthCxProjectEngineConfigName = dictCxProjectCreationCollectionStats["cWidthCxProjectEngineConfigName"];    
        cWidthCxProjectEngineConfigId   = dictCxProjectCreationCollectionStats["cWidthCxProjectEngineConfigId"];    

        if self.bTraceFlag == True:

            print(" = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ");
            print("%s 'dictcxprojectcreationcollectionstats' is [%s]..." % (self.sClassDisp, dictcxprojectcreationcollectionstats));
            print("%s 'dictCxProjectCreationCollectionStats' is [%s]..." % (self.sClassDisp, dictCxProjectCreationCollectionStats));
            print("%s 'cWidthCxProjectName' is [%d]..." % (self.sClassDisp, cWidthCxProjectName));
            print("%s 'cWidthCxProjectId' is [%d]..." % (self.sClassDisp, cWidthCxProjectId));
            print("%s 'cWidthCxProjectTeamName' is [%d]..." % (self.sClassDisp, cWidthCxProjectTeamName));
            print("%s 'cWidthCxProjectTeamId' is [%d]..." % (self.sClassDisp, cWidthCxProjectTeamId));
            print("%s 'cWidthCxProjectPresetName' is [%d]..." % (self.sClassDisp, cWidthCxProjectPresetName));
            print("%s 'cWidthCxProjectPresetId' is [%d]..." % (self.sClassDisp, cWidthCxProjectPresetId));
            print("%s 'cWidthCxProjectEngineConfigName' is [%d]..." % (self.sClassDisp, cWidthCxProjectEngineConfigName));
            print("%s 'cWidthCxProjectEngineConfigId' is [%d]..." % (self.sClassDisp, cWidthCxProjectEngineConfigId));
            print(" = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ");
            print("");

        asObjDetail = list();

        asObjDetail.append("Project ");
        asObjDetail.append("'Name' [%*s], "              % (cWidthCxProjectName, self.sCxProjectName));
        asObjDetail.append("'Base Name' [%s], "          % (self.sCxProjectBaseName));
        asObjDetail.append("'Id' [%-*s], "               % (cWidthCxProjectId, self.sCxProjectId));
        asObjDetail.append("'Is Public?' [%5s], "        % (self.bCxProjectIsPublic));
        asObjDetail.append("'Scan Type' [%s], "          % (self.sCxProjectScanType));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team' [%s], "               % (self.sCxProjectTeam));
        asObjDetail.append("'Version' [%s], "            % (self.sCxProjectVersion));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team Name' [%*s], "         % (cWidthCxProjectTeamName, self.sCxProjectTeamName));
        asObjDetail.append("'Team Id' [%*s], "           % (cWidthCxProjectTeamId, self.sCxProjectTeamId));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Preset Name' [%*s], "       % (cWidthCxProjectPresetName, self.sCxProjectPresetName));
        asObjDetail.append("'Preset Id' [%*s], "         % (cWidthCxProjectPresetId, self.sCxProjectPresetId));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'EngineConfig Name' [%*s], " % (cWidthCxProjectEngineConfigName, self.sCxProjectEngineConfigName));
        asObjDetail.append("'EngineConfig Id' [%*s]. "   % (cWidthCxProjectEngineConfigId, self.sCxProjectEngineConfigId));
        asObjDetail.append("\n");

        if self.dictCxProjectBranchedNames != None and \
            len(self.dictCxProjectBranchedNames) > 0:

            for sCxProjectBranchedName in self.dictCxProjectBranchedNames.keys():

                if sCxProjectBranchedName == None:

                    continue;

                sCxProjectBranchedId = self.dictCxProjectBranchedNames[sCxProjectBranchedName];

                asObjDetail.append("............");
                asObjDetail.append("Branched Project ");
                asObjDetail.append("'Name' [%*s], " % (cWidthCxProjectName, sCxProjectBranchedName));
                asObjDetail.append("'Id' [%*s]. "   % (cWidthCxProjectId, sCxProjectBranchedId));
                asObjDetail.append("\n");

        if self.objCxProjectExtraField1 != None:

            asObjDetail.append("............");
            asObjDetail.append("'Extra' Project field #1 ");
            asObjDetail.append("'Value' [%s]. " % (self.objCxProjectExtraField1));
            asObjDetail.append("\n");

        if self.objCxProjectExtraField2 != None:

            asObjDetail.append("............");
            asObjDetail.append("'Extra' Project field #2 ");
            asObjDetail.append("'Value' [%s]. " % (self.objCxProjectExtraField2));
            asObjDetail.append("\n");

        if self.objCxProjectExtraField3 != None:

            asObjDetail.append("............");
            asObjDetail.append("'Extra' Project field #3 ");
            asObjDetail.append("'Value' [%s]. " % (self.objCxProjectExtraField3));
            asObjDetail.append("\n");

        if self.objCxProjectExtraField4 != None:

            asObjDetail.append("............");
            asObjDetail.append("'Extra' Project field #4 ");
            asObjDetail.append("'Value' [%s]. " % (self.objCxProjectExtraField4));
            asObjDetail.append("\n");

        if self.sCxProjectSASTZipFilespec != None:

            asObjDetail.append("............");
            asObjDetail.append("Zip filespec for 'SAST' [%s]. " % (self.sCxProjectSASTZipFilespec));
            asObjDetail.append("\n");

        if self.sCxProjectOSAZipFilespec != None:

            asObjDetail.append("............");
            asObjDetail.append("Zip filespec for 'OSA' [%s]. " % (self.sCxProjectOSAZipFilespec));
            asObjDetail.append("\n");

        return ''.join(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

