
import os;
import traceback;
import platform;
import re;
import string;
import sys;
import collections;

from datetime import datetime;

import CxServerEndpoint1;
import CxProjectData1;
import CxRestAPIProjectStatisticsBase1;

class CxProjectDataCollection(object):

    sClassMod                        = __name__;
    sClassId                         = "CxProjectDataCollection";
    sClassVers                       = "(v1.0574)";
    sClassDisp                       = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                       = False;
    cxServerEndpoint                 = None;
    dictCxProjectDataCollection      = None;
    asCxProjectDataCollectionReport  = None;
    asCxProjectDataCollectionHtml    = None;

    # Project Collection 'meta' data:

    dictCxAllTeams                   = None;
    dictCxAllPresets                 = None;
    dictCxAllEngineConfigurations    = None;

    # CxRestAPI object(s):

    cxProjectDataRestAPI             = None;

    # Project Collection stats:

#   cLongestProjectName              = 0;
#   cMaxProjectId                    = 0;
#   cLongestProjectTeamId            = 0;
#   cMaxProjectLinks                 = 0;
#   cMaxProjectCustomFields          = 0;

    # Project Collection stats:

    dictCxProjectDataCollectionStats = collections.defaultdict(int);
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

    # Misc. variables:

    sPlatform                        = None;
    bPlatformIsWindows               = False;

    def __init__(self, trace=False, cxserverendpoint=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxServerEndpoint(cxserverendpoint=cxserverendpoint);

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

    def getCxServerEndpoint(self):

        return self.cxServerEndpoint;

    def setCxServerEndpoint(self, cxserverendpoint=None):

        self.cxServerEndpoint = cxserverendpoint;

    def getCxProjectDataCollection(self):

        return self.dictCxProjectDataCollection;

    def setCxProjectDataCollection(self, cxprojectdatacollection=None):

        self.dictCxProjectDataCollection = cxprojectdatacollection;

    def getCxProjectDataCollectionReportAsList(self):

        return self.asCxProjectDataCollectionReport;

    def getCxProjectDataCollectionHtmlAsList(self):

        return self.asCxProjectDataCollectionHtml;

    def getCxProjectMetaDataAllTeams(self):

        return self.dictCxAllTeams;

    def addCxProjectMetaDataAllTeams(self, cxteamfullname=None, cxteamid=None):

        sCxTeamFullName = cxteamfullname;

        if sCxTeamFullName != None and \
            type(sCxTeamFullName) == bytes:

            sCxTeamFullName = sCxTeamFullName.decode("utf-8");

        if sCxTeamFullName != None:

            sCxTeamFullName = sCxTeamFullName.strip();

        if sCxTeamFullName == None or \
            len(sCxTeamFullName) < 1:

            return;

        if cxteamid == None:

            return;

        sCxTeamId = "0";

        if type(cxteamid) == str:

            sCxTeamId = cxteamid;

            if sCxTeamId != None:

                sCxTeamId = sCxTeamId.strip();

            if sCxTeamId == None or \
               len(sCxTeamId) < 1:

                sCxTeamId = "0";

        else:

            iCxTeamId = cxteamid;

            if iCxTeamId < 0:

                sCxTeamId = "0";

            else:

                sCxTeamId = ("%d" % iCxTeamId);

        if self.dictCxAllTeams == None:

            self.dictCxAllTeams = collections.defaultdict();

        self.dictCxAllTeams[sCxTeamFullName] = sCxTeamId;

    def getCxProjectMetaDataAllPresets(self):

        return self.dictCxAllPresets;

    def addCxProjectMetaDataAllPresets(self, cxpresetname=None, cxpresetdict=None):

        sCxPresetName = cxpresetname;

        if sCxPresetName != None and \
            type(sCxPresetName) == bytes:

            sCxPresetName = sCxPresetName.decode("utf-8");

        if sCxPresetName != None:

            sCxPresetName = sCxPresetName.strip();

        if sCxPresetName == None or \
            len(sCxPresetName) < 1:

            return;

        dictCxPreset = cxpresetdict;

        if dictCxPreset == None or \
            len(dictCxPreset) < 1:

            return;

        if self.dictCxAllPresets == None:

            self.dictCxAllPresets = collections.defaultdict();

        self.dictCxAllPresets[sCxPresetName] = dictCxPreset;

    def getCxProjectMetaDataAllEngineConfigurations(self):

        return self.dictCxAllEngineConfigurations;

    def addCxProjectMetaDataAllEngineConfigurations(self, cxengineconfigname=None, cxengineconfigid=None):

        sCxEngineConfigName = cxengineconfigname;

        if sCxEngineConfigName != None and \
            type(sCxEngineConfigName) == bytes:

            sCxEngineConfigName = sCxEngineConfigName.decode("utf-8");

        if sCxEngineConfigName != None:

            sCxEngineConfigName = sCxEngineConfigName.strip();

        if sCxEngineConfigName == None or \
            len(sCxEngineConfigName) < 1:

            return;

        sCxEngineConfigId = cxengineconfigid;

        if sCxEngineConfigId != None:

            sCxEngineConfigId = sCxEngineConfigId.strip();

        if sCxEngineConfigId == None or \
            len(sCxEngineConfigId) < 1:

            sCxEngineConfigId = "";

        if self.dictCxAllEngineConfigurations == None:

            self.dictCxAllEngineConfigurations = collections.defaultdict();

        self.dictCxAllEngineConfigurations[sCxEngineConfigName] = sCxEngineConfigId;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));

            if self.cxServerEndpoint == None:

                print("%s The 'cxServerEndpoint' has NOT been set..." % (self.sClassDisp));

            else:

                print("%s The 'cxServerEndpoint' is [%s]..." % (self.sClassDisp, self.cxServerEndpoint));

            if self.dictCxProjectDataCollection == None:

                print("%s The 'dictCxProjectDataCollection' has NOT been set..." % (self.sClassDisp));

            else:

                print("%s The 'dictCxProjectDataCollection' is [%s]..." % (self.sClassDisp, self.dictCxProjectDataCollection));

            print("%s The contents of 'asCxProjectDataCollectionReport' is [%s]..." % (self.sClassDisp, self.asCxProjectDataCollectionReport));
            print("%s The contents of 'asCxProjectDataCollectionHtml' is [%s]..." % (self.sClassDisp, self.asCxProjectDataCollectionHtml));
            print("%s The contents of 'dictCxAllTeams' is [%s]..." % (self.sClassDisp, self.dictCxAllTeams));
            print("%s The contents of 'dictCxAllPresets' is [%s]..." % (self.sClassDisp, self.dictCxAllPresets));
            print("%s The contents of 'dictCxAllEngineConfigurations' is [%s]..." % (self.sClassDisp, self.dictCxAllEngineConfigurations));
            print("%s The contents of 'sPlatform' is [%s]..." % (self.sClassDisp, self.sPlatform));
            print("%s The contents of 'bPlatformIsWindows' is [%s]..." % (self.sClassDisp, self.bPlatformIsWindows));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'cxServerEndpoint' is [%s], " % (self.cxServerEndpoint));
        asObjDetail.append("'dictCxProjectDataCollection' is [%s], " % (self.dictCxProjectDataCollection));
        asObjDetail.append("'asCxProjectDataCollectionReport' is [%s], " % (self.asCxProjectDataCollectionReport));
        asObjDetail.append("'asCxProjectDataCollectionHtml' is [%s], " % (self.asCxProjectDataCollectionHtml));
        asObjDetail.append("'dictCxAllTeams' is [%s], " % (self.dictCxAllTeams));
        asObjDetail.append("'dictCxAllPresets' is [%s], " % (self.dictCxAllPresets));
        asObjDetail.append("'dictCxAllEngineConfigurations' is [%s], " % (self.dictCxAllEngineConfigurations));
        asObjDetail.append("'sPlatform' is [%s], " % (self.sPlatform));
        asObjDetail.append("'bPlatformIsWindows' is [%s]. " % (self.bPlatformIsWindows));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def loadCxProjectDataMetaDataToCollectionFromRestAPI(self):

    #   self.bTraceFlag = True;

        if self.cxServerEndpoint == None:

            print("");
            print("%s NO CxServerEndpoint has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxServerEndpoint.getCxServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            if self.cxProjectDataRestAPI == None:

                self.cxProjectDataRestAPI = CxRestAPIProjectStatisticsBase1.CxRestAPIProjectStatisticsBase(trace=self.bTraceFlag, cxserverendpoint=self.cxServerEndpoint, cxprojectdatacollection=self);

                if self.cxProjectDataRestAPI == None:

                    print("");
                    print("%s Failed to create a CxRestAPIProjectStatisticsBase object - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            bGetProjMetaOk = self.cxProjectDataRestAPI.getCxRestAPIProjectDataMetaData();

            if bGetProjMetaOk == False:

                print("");
                print("%s 'cxProjectDataRestAPI.getCxRestAPIProjectDataMetaData()' API call failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'loadCxProjectDataMetaDataToCollectionFromRestAPI()' - exception occured..." % (self.sClassDisp));
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

    def loadCxProjectDataCollectionFromRestAPI(self):

    #   self.bTraceFlag = True;

        if self.cxServerEndpoint == None:

            print("");
            print("%s NO CxServerEndpoint has been specified nor defined for the Checkmarx CxProjectCreation(s) Collection - one CxServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxServerEndpoint.getCxServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            print("%s The Checkmarx CxProjectData(s) Collection is executing on the OS [%s] which is 'Windows' [%s]..." % (self.sClassDisp, self.sPlatform, self.bPlatformIsWindows));
            print("");

            if self.cxProjectDataRestAPI == None:

                self.cxProjectDataRestAPI = CxRestAPIProjectStatisticsBase1.CxRestAPIProjectStatisticsBase(trace=self.bTraceFlag, cxserverendpoint=self.cxServerEndpoint, cxprojectdatacollection=self);

                if self.cxProjectDataRestAPI == None:

                    print("");
                    print("%s Failed to create a CxRestAPIProjectStatisticsBase object - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            bGetProjStatsOk = self.cxProjectDataRestAPI.getCxRestAPIProjectStatistics();

            if bGetProjStatsOk == False:

                print("");
                print("%s 'cxProjectDataRestAPI.getCxRestAPIProjectStatistics()' API call failed - Error!" % (self.sClassDisp));
                print("");

                bProcessingError = True;

        except Exception as inst:

            print("%s 'loadCxProjectDataCollectionFromRestAPI()' - exception occured..." % (self.sClassDisp));
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

    def addCxProjectDataToCxProjectDataCollection(self, cxprojectdata=None):

    #   self.bTraceFlag = True;

        cxProjectData = cxprojectdata;

        if cxProjectData == None:

            print("");
            print("%s NO CxProjectData has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.dictCxProjectDataCollection == None:

            if self.bTraceFlag == True:

                print("%s The object 'dictCxProjectDataCollection' has NOT been set - creating an internal instance..." % (self.sClassDisp));

            self.dictCxProjectDataCollection = collections.defaultdict(); 

        bProcessingError = False;

        try:

            sCxProjectName = cxProjectData.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectData has a 'name' that is None or 'empty' - bypassing the addition of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            self.dictCxProjectDataCollection[sCxProjectName] = cxProjectData;

            if self.bTraceFlag == True:

                print("%s CxProjectData named [%s] added to the CxProjectDataCollection..." % (self.sClassDisp, sCxProjectName));

            bGatherProjStats = self.gatherCxProjectDataStatistics(cxprojectdata=cxProjectData);

            if bGatherProjStats == False:

                print("");
                print("%s 'gatherCxProjectDataStatistics()' API call failed - Warning!" % (self.sClassDisp));
                print("");

            bResolveIdsToNamesOk = self.resolveCxProjectIdsToNames(cxprojectdata=cxProjectData);

            if bResolveIdsToNamesOk == False:

                print("");
                print("%s 'resolveCxProjectIdsToNames()' API call failed - Error!" % (self.sClassDisp));
                print("");

                bProcessingError = True;

            if self.bTraceFlag == True:

                print("%s CxProjectData named [%s] of [%s] after Names-to-IDs 'resolution'..." % (self.sClassDisp, sCxProjectName, cxProjectData));

        except Exception as inst:

            print("%s 'addCxProjectDataToCxProjectDataCollection()' - exception occured..." % (self.sClassDisp));
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

    def gatherCxProjectDataStatistics(self, cxprojectdata=None):

    #   self.bTraceFlag = True;

        cxProjectData = cxprojectdata;

        if cxProjectData == None:

            print("");
            print("%s NO CxProjectData has been specified nor defined for the Checkmarx CxProjectData(s) Collection - one CxProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

        #   # Gather 'max' field width stats:
        #
        #   if len(sCxProjectName) > self.cLongestProjectName:
        #
        #       self.cLongestProjectName = len(sCxProjectName);
        #
        #   cDataMaxProjectId = len(cxProjectData.getCxProjectId());
        #
        #   if cDataMaxProjectId > self.cMaxProjectId:
        #
        #       self.cMaxProjectId = cDataMaxProjectId;
        #
        #   cDataLongestProjectTeamId = len(cxProjectData.getCxProjectTeamId());
        #
        #   if cDataLongestProjectTeamId > self.cLongestProjectTeamId:
        #
        #       self.cLongestProjectTeamId = cDataLongestProjectTeamId;

            # Gather 'longest' field 'width' stats:

            sCxProjectName = cxProjectData.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectData has a 'name' that is None or 'empty' - bypassing the gathering of stats for this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            if len(sCxProjectName) > self.dictCxProjectDataCollectionStats["cWidthCxProjectName"]:

                self.dictCxProjectDataCollectionStats["cWidthCxProjectName"] = len(sCxProjectName);

            sCxProjectId = cxProjectData.getCxProjectId();

            if sCxProjectId != None:

                sCxProjectId = sCxProjectId.strip();

            if sCxProjectId != None   and \
                len(sCxProjectId) > 0 and \
                len(sCxProjectId) > self.dictCxProjectDataCollectionStats["cWidthCxProjectId"]:

                    self.dictCxProjectDataCollectionStats["cWidthCxProjectId"] = len(sCxProjectId);

        #   sCxProjectTeamName = cxProjectData.getCxProjectTeamName();
        #
        #   if sCxProjectTeamName != None:
        #
        #       sCxProjectTeamName = sCxProjectTeamName.strip();
        #
        #   if sCxProjectTeamName != None   and \
        #       len(sCxProjectTeamName) > 0 and \
        #       len(sCxProjectTeamName) > self.dictCxProjectDataCollectionStats["cWidthCxProjectTeamName"]:
        #
        #           self.dictCxProjectDataCollectionStats["cWidthCxProjectTeamName"] = len(sCxProjectTeamName);
        #
        #   sCxProjectTeamId = cxProjectData.getCxProjectTeamId();
        #
        #   if sCxProjectTeamId != None:
        #
        #       sCxProjectTeamId = sCxProjectTeamId.strip();
        #
        #   if sCxProjectTeamId != None   and \
        #       len(sCxProjectTeamId) > 0 and \
        #       len(sCxProjectTeamId) > self.dictCxProjectDataCollectionStats["cWidthCxProjectTeamId"]:
        #
        #           self.dictCxProjectDataCollectionStats["cWidthCxProjectTeamId"] = len(sCxProjectTeamId);
        #
        #   sCxProjectPresetName = cxProjectData.getCxProjectPresetName();
        #
        #   if sCxProjectPresetName != None:
        #
        #       sCxProjectPresetName = sCxProjectPresetName.strip();
        #
        #   if sCxProjectPresetName != None   and \
        #       len(sCxProjectPresetName) > 0 and \
        #       len(sCxProjectPresetName) > self.dictCxProjectDataCollectionStats["cWidthCxProjectPresetName"]:
        #
        #           self.dictCxProjectDataCollectionStats["cWidthCxProjectPresetName"] = len(sCxProjectPresetName);
        #
        #   sCxProjectPresetId = cxProjectData.getCxProjectPresetId();
        #
        #   if sCxProjectPresetId != None:
        #
        #       sCxProjectPresetId = sCxProjectPresetId.strip();
        #
        #   if sCxProjectPresetId != None   and \
        #       len(sCxProjectPresetId) > 0 and \
        #       len(sCxProjectPresetId) > self.dictCxProjectDataCollectionStats["cWidthCxProjectPresetId"]:
        #
        #           self.dictCxProjectDataCollectionStats["cWidthCxProjectPresetId"] = len(sCxProjectPresetId);
        #
        #   sCxProjectEngineConfigName = cxProjectData.getCxProjectEngineConfigName();
        #
        #   if sCxProjectEngineConfigName != None:
        #
        #       sCxProjectEngineConfigName = sCxProjectEngineConfigName.strip();
        #
        #   if sCxProjectEngineConfigName != None   and \
        #       len(sCxProjectEngineConfigName) > 0 and \
        #       len(sCxProjectEngineConfigName) > self.dictCxProjectDataCollectionStats["cWidthCxProjectEngineConfigName"]:
        #
        #           self.dictCxProjectDataCollectionStats["cWidthCxProjectEngineConfigName"] = len(sCxProjectEngineConfigName);
        #
        #   sCxProjectEngineConfigId = cxProjectData.getCxProjectEngineConfigId();
        #
        #   if sCxProjectEngineConfigId != None:
        #
        #       sCxProjectEngineConfigId = sCxProjectEngineConfigId.strip();
        #
        #   if sCxProjectEngineConfigId != None   and \
        #       len(sCxProjectEngineConfigId) > 0 and \
        #       len(sCxProjectEngineConfigId) > self.dictCxProjectDataCollectionStats["cWidthCxProjectEngineConfigId"]:
        #
        #           self.dictCxProjectDataCollectionStats["cWidthCxProjectEngineConfigId"] = len(sCxProjectEngineConfigId);

        except Exception as inst:

            print("%s 'gatherCxProjectDataStatistics()' - exception occured..." % (self.sClassDisp));
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

    def generateCxProjectDataCollectionScansDelta(self):
 
        bProcessingError = False;

        if self.dictCxProjectDataCollection == None or \
           len(self.dictCxProjectDataCollection) < 1:

            print("");
            print("%s NO Checkmarx CxProjectData(s) have been specified nor defined in the Checkmarx CxProjectData(s) Collection - at least 1 CxProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            cCxProjectDataCollection = 0;

            for sCxProjectName in list(self.dictCxProjectDataCollection.keys()):

                cCxProjectDataCollection += 1;

                cxProjectData = self.dictCxProjectDataCollection[sCxProjectName];

                if cxProjectData == None:

                    continue;

                bGenProjScansDeltaOk = self.generateCxProjectDataScansDelta(cxprojectdata=cxProjectData);

                if bGenProjScansDeltaOk == False:

                    print("");
                    print("%s 'generateCxProjectDataScansDelta()' API call failed - Warning!" % (self.sClassDisp));
                    print("");

                    return False;

        except Exception as inst:
 
            print("%s 'generateCxProjectDataCollectionScansDelta()' - exception occured..." % (self.sClassDisp));
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
 
    def resolveCxProjectIdsToNames(self, cxprojectdata=None):

    #   self.bTraceFlag = True;

        cxProjectData = cxprojectdata;

        if cxProjectData == None:

            print("");
            print("%s NO CxProjectData has been specified nor defined for the Checkmarx CxProjectData(s) Collection - one CxProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.dictCxAllTeams == None or \
            len(self.dictCxAllTeams) < 1:

            print("");
            print("%s The CxProject Team 'id' of [%s] can NOT be 'resolved' - the dictionary of ALL Team(s) is None or 'empty' - Error!" % (self.sClassDisp, sCxProjectTeamId));
            print("");

            return False;

        bProcessingError = False;

        try:

            # Convert the various Project Id(s) to Name(s):

            sCxProjectName = cxProjectData.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectData has a 'name' that is None or 'empty' - bypassing the IDs-to-Names 'resolution' of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            sCxProjectTeamId = cxProjectData.getCxProjectTeamId();

            if sCxProjectTeamId != None:

                sCxProjectTeamId = sCxProjectTeamId.strip();

            if sCxProjectTeamId == None or \
                len(sCxProjectTeamId) < 1:

                print("");
                print("%s The CxProject Team 'id' of [%s] in the CxProjectData object [%s] is 'invalid' - Error!" % (self.sClassDisp, sCxProjectTeamId, cxProjectData));
                print("");

                return False;

            for sCurrTeamName in self.dictCxAllTeams.keys():

                if sCurrTeamName == None:

                    continue;

                sCurrTeamId = self.dictCxAllTeams[sCurrTeamName];

                if sCurrTeamId == sCxProjectTeamId:

                    cxProjectData.setCxProjectTeam(cxprojectteam=sCurrTeamName);

        except Exception as inst:

            print("%s 'resolveCxProjectIdsToNames()' - exception occured..." % (self.sClassDisp));
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

    def generateCxProjectDataScansDelta(self, cxprojectdata=None):

    #   self.bTraceFlag = True;

        cxProjectData = cxprojectdata;

        if cxProjectData == None:

            print("");
            print("%s NO CxProjectData has been specified nor defined for the Checkmarx CxProjectData(s) Collection - one CxProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            sCxProjectName = cxProjectData.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectData has a 'name' that is None or 'empty' - bypassing the gathering of scans delta for this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            if len(sCxProjectName) > self.dictCxProjectDataCollectionStats["cWidthCxProjectName"]:

                self.dictCxProjectDataCollectionStats["cWidthCxProjectName"] = len(sCxProjectName);

            sCxProjectId = cxProjectData.getCxProjectId();

            if sCxProjectId == None or \
                len(sCxProjectId) < 1:

                print("");
                print("%s The CxProjectData has a 'name' of [%s] but an 'id' that is None or 'empty' - bypassing the gathering of scans delta for this object - Error!" % (self.sClassDisp, sCxProjectName));
                print("");

                return False;

            bGenerateScansDeltaOk = cxProjectData.generateCxProjectDataScansDelta();

            if bGenerateScansDeltaOk == False:

                print("");
                print("%s 'cxProjectData.generateCxProjectDataScansDelta()' API call failed - Warning!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'generateCxProjectDataScansDelta()' - exception occured..." % (self.sClassDisp));
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

    def generateCxProjectDataCollectionReport(self):
 
        bProcessingError = False;

        self.asCxProjectDataCollectionReport = None;
 
        if self.dictCxProjectDataCollection == None or \
           len(self.dictCxProjectDataCollection) < 1:

            print("");
            print("%s NO Checkmarx CxProjectData(s) have been specified nor defined in the Checkmarx CxProjectData(s) Collection - at least 1 CxProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            asCxProjectDataCollectionReportDebug = list();
            self.asCxProjectDataCollectionReport = list();

            self.asCxProjectDataCollectionReport.append("");
            self.asCxProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
            self.asCxProjectDataCollectionReport.append("%s Checkmarx CxProjectData(s) collection for (%d) element(s):" % \
                                                            (self.sClassDisp, len(self.dictCxProjectDataCollection)));
            self.asCxProjectDataCollectionReport.append("");

            asCxProjectDataCollectionReportDebug.append("");
            asCxProjectDataCollectionReportDebug.append("- - - - - - - - - - - - - - - - DEBUG - - - - - - - - - - - - - - - - - - - - - -");
            asCxProjectDataCollectionReportDebug.append("%s Checkmarx CxProjectData(s) collection for (%d) element(s):" % \
                                                       (self.sClassDisp, len(self.dictCxProjectDataCollection)));
            asCxProjectDataCollectionReportDebug.append("");

            cCxProjectDataCollection = 0;

            for sCxProjectName in list(self.dictCxProjectDataCollection.keys()):

                cCxProjectDataCollection += 1;

                cxProjectData = self.dictCxProjectDataCollection[sCxProjectName];

                if cxProjectData == None:

                    continue;

                self.asCxProjectDataCollectionReport.append("%s CxProjectData element (%3d) of (%3d):" % \
                                                                (self.sClassDisp, cCxProjectDataCollection, len(self.dictCxProjectDataCollection)));
                self.asCxProjectDataCollectionReport.append(cxProjectData.toPrettyStringWithWidths(dictcxprojectdatacollectionstats=self.dictCxProjectDataCollectionStats));

                if self.bTraceFlag == True:

                    asCxProjectDataCollectionReportDebug.append("%s CxProjectData element (named '%s')[(%d) of (%d)] is:" % \
                                                            (self.sClassDisp, sCxProjectName, cCxProjectDataCollection, len(self.dictCxProjectDataCollection)));
                    asCxProjectDataCollectionReportDebug.append(cxProjectData.toString());
                    asCxProjectDataCollectionReportDebug.append("");

            self.asCxProjectDataCollectionReport.append("");
            self.asCxProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
            self.asCxProjectDataCollectionReport.append("");

            if self.bTraceFlag == True:

                asCxProjectDataCollectionReportDebug.append("");
                asCxProjectDataCollectionReportDebug.append("- - - - - - - - - - - - - - - - DEBUG - - - - - - - - - - - - - - - - - - - - - -");
                asCxProjectDataCollectionReportDebug.append("");

                self.asCxProjectDataCollectionReport.extend(asCxProjectDataCollectionReportDebug);

        except Exception as inst:
 
            print("%s 'generateCxProjectDataCollectionReport()' - exception occured..." % (self.sClassDisp));
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
 
    def saveCxProjectDataCollectionReportToFile(self, outputprojectdatacollectionreportfile=None):

    #   self.bTraceFlag = True;

        sOutputCxProjectDataCollectionReportFile = outputprojectdatacollectionreportfile;

        if sOutputCxProjectDataCollectionReportFile != None:

            sOutputCxProjectDataCollectionReportFile = sOutputCxProjectDataCollectionReportFile.strip();

        if sOutputCxProjectDataCollectionReportFile == None or \
           len(sOutputCxProjectDataCollectionReportFile) < 1:

            print("%s Command received an (Output) CxProjectData Collection report filename that is 'null' or Empty - Error!" % (self.sClassDisp));

            return False;

        if self.asCxProjectDataCollectionReport == None or \
            len(self.asCxProjectDataCollectionReport) < 1:

            print("");
            print("%s The CxProjectData Collection 'report' is 'None' or Empty - Severe Error!" % (self.sClassDisp));
 
            return False;

        try:

            print("%s Command is generating the (Output) CxProjectData Collection 'report' into a file of [%s]..." % (self.sClassDisp, sOutputCxProjectDataCollectionReportFile));
            print("");

            fOutputCxProjectDataCollectionReport = open(sOutputCxProjectDataCollectionReportFile, "w");

            fOutputCxProjectDataCollectionReport.write('\n'.join(self.asCxProjectDataCollectionReport));
            fOutputCxProjectDataCollectionReport.close();

            print("%s Command generated the (Output) CxProjectData Collection 'report' into a file of [%s]..." % (self.sClassDisp, sOutputCxProjectDataCollectionReportFile));
            print("");

        except Exception as inst:

            print("%s 'saveCxProjectDataCollectionReportToFile()' - operational exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def generateCxProjectDataCollectionHtml(self):
 
        bProcessingError = False;

        self.asCxProjectDataCollectionHtml = None;
 
        if self.dictCxProjectDataCollection == None or \
           len(self.dictCxProjectDataCollection) < 1:

            print("");
            print("%s NO Checkmarx CxProjectData(s) have been specified nor defined in the Checkmarx CxProjectData(s) Collection - at least 1 CxProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            asCxProjectDataCollectionHtmlDebug = list();
            self.asCxProjectDataCollectionHtml = list();

            self.asCxProjectDataCollectionHtml.append("<html>");
            self.asCxProjectDataCollectionHtml.append("");
            self.asCxProjectDataCollectionHtml.append("<head>");
            self.asCxProjectDataCollectionHtml.append("    <title Checkmarx CxProjectData(s) Collection Html report [%s] ></title>" % (self.sClassDisp));
            self.asCxProjectDataCollectionHtml.append("    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/> ");
            self.asCxProjectDataCollectionHtml.append("    <script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js\"></script>");
            self.asCxProjectDataCollectionHtml.append("    <script language=\"JavaScript\" src=\"script.js\"></script>");
            self.asCxProjectDataCollectionHtml.append("    <script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>");
            self.asCxProjectDataCollectionHtml.append("    <style>");
            self.asCxProjectDataCollectionHtml.append("        .toggle        { display: none; }");
            self.asCxProjectDataCollectionHtml.append("        .toggle:target { display: table-row; }");
            self.asCxProjectDataCollectionHtml.append("");
            self.asCxProjectDataCollectionHtml.append("        div#links");
            self.asCxProjectDataCollectionHtml.append("        {");
            self.asCxProjectDataCollectionHtml.append("            position: relative;");
            self.asCxProjectDataCollectionHtml.append("            top: 0px;");
            self.asCxProjectDataCollectionHtml.append("            left: 0;");
        #   self.asCxProjectDataCollectionHtml.append("            font: 9px Verdana, sans-serif;");
            self.asCxProjectDataCollectionHtml.append("        }");
            self.asCxProjectDataCollectionHtml.append("");
            self.asCxProjectDataCollectionHtml.append("        /* Popup box BEGIN */");
            self.asCxProjectDataCollectionHtml.append("        .popupCloseButton {");
            self.asCxProjectDataCollectionHtml.append("            background-color: #fff;");
            self.asCxProjectDataCollectionHtml.append("            border: 3px solid #999;");
            self.asCxProjectDataCollectionHtml.append("            border-radius: 50px;");
            self.asCxProjectDataCollectionHtml.append("            cursor: pointer;");
            self.asCxProjectDataCollectionHtml.append("            display: inline-block;");
            self.asCxProjectDataCollectionHtml.append("            font-family: arial;");
            self.asCxProjectDataCollectionHtml.append("            font-weight: bold;");
            self.asCxProjectDataCollectionHtml.append("            position: absolute;");
            self.asCxProjectDataCollectionHtml.append("            top: -20px;");
            self.asCxProjectDataCollectionHtml.append("            right: -20px;");
            self.asCxProjectDataCollectionHtml.append("            font-size: 25px;");
            self.asCxProjectDataCollectionHtml.append("            line-height: 30px;");
            self.asCxProjectDataCollectionHtml.append("            width: 30px;");
            self.asCxProjectDataCollectionHtml.append("            height: 30px;");
            self.asCxProjectDataCollectionHtml.append("            text-align: center;");
            self.asCxProjectDataCollectionHtml.append("        }");
            self.asCxProjectDataCollectionHtml.append("        .popupCloseButton:hover {");
            self.asCxProjectDataCollectionHtml.append("            background-color: #ccc;");
            self.asCxProjectDataCollectionHtml.append("        }");
            self.asCxProjectDataCollectionHtml.append("        /* Popup box END */");
            self.asCxProjectDataCollectionHtml.append("");

            for sCxProjectName in list(self.dictCxProjectDataCollection.keys()):

                cxProjectData = self.dictCxProjectDataCollection[sCxProjectName];

                if cxProjectData == None:

                    continue;

                self.asCxProjectDataCollectionHtml.append("        div#cxDiv%s   { display: none; } " % (cxProjectData.getCxProjectId())); 
                self.asCxProjectDataCollectionHtml.append("");
                self.asCxProjectDataCollectionHtml.append("        .hover_bkgr_lang%s{" % (cxProjectData.getCxProjectId()));
                self.asCxProjectDataCollectionHtml.append("            background:rgba(0,0,0,.4);");
                self.asCxProjectDataCollectionHtml.append("            cursor:pointer;");
                self.asCxProjectDataCollectionHtml.append("            display:none;");
                self.asCxProjectDataCollectionHtml.append("            height:80%;");
                self.asCxProjectDataCollectionHtml.append("            position:fixed;");
                self.asCxProjectDataCollectionHtml.append("            text-align:center;");
                self.asCxProjectDataCollectionHtml.append("            top:0;");
                self.asCxProjectDataCollectionHtml.append("            width:100%;");
                self.asCxProjectDataCollectionHtml.append("            z-index:10000;");
                self.asCxProjectDataCollectionHtml.append("        }");
                self.asCxProjectDataCollectionHtml.append("        .hover_bkgr_lang%s .helper{" % (cxProjectData.getCxProjectId()));
                self.asCxProjectDataCollectionHtml.append("            display:inline-block;");
                self.asCxProjectDataCollectionHtml.append("            height:80%;");
                self.asCxProjectDataCollectionHtml.append("            vertical-align:middle;");
                self.asCxProjectDataCollectionHtml.append("        }");
                self.asCxProjectDataCollectionHtml.append("        .hover_bkgr_lang%s > div {" % (cxProjectData.getCxProjectId()));
                self.asCxProjectDataCollectionHtml.append("            background-color: #fff;");
                self.asCxProjectDataCollectionHtml.append("            box-shadow: 8px 8px 15px #555;");
                self.asCxProjectDataCollectionHtml.append("            display: inline-block;");
                self.asCxProjectDataCollectionHtml.append("            height: auto;");
                self.asCxProjectDataCollectionHtml.append("            max-width: 650px;");
                self.asCxProjectDataCollectionHtml.append("            min-height: 4px;");
                self.asCxProjectDataCollectionHtml.append("            vertical-align: middle;");
                self.asCxProjectDataCollectionHtml.append("            width: 60%;");
                self.asCxProjectDataCollectionHtml.append("            position: relative;");
                self.asCxProjectDataCollectionHtml.append("            border-radius: 3px;");
                self.asCxProjectDataCollectionHtml.append("            padding: 4px 5%;");
                self.asCxProjectDataCollectionHtml.append("        }");
                self.asCxProjectDataCollectionHtml.append("        .trigger_popup_lang%s {" % (cxProjectData.getCxProjectId()));
                self.asCxProjectDataCollectionHtml.append("            cursor: pointer;");
                self.asCxProjectDataCollectionHtml.append("            font-size: 20px;");
                self.asCxProjectDataCollectionHtml.append("            margin: 8px;");
                self.asCxProjectDataCollectionHtml.append("            display: inline-block;");
                self.asCxProjectDataCollectionHtml.append("            font-weight: bold;");
                self.asCxProjectDataCollectionHtml.append("        }");
                self.asCxProjectDataCollectionHtml.append("");

            self.asCxProjectDataCollectionHtml.append("    </style>");
            self.asCxProjectDataCollectionHtml.append("    <script>");
            self.asCxProjectDataCollectionHtml.append("        function drcToggleSection(divId) {");
            self.asCxProjectDataCollectionHtml.append("            var x = document.getElementById(divId);");
            self.asCxProjectDataCollectionHtml.append("            console.log(\"drcToggleSection called for 'divId' of [%s] 'x.style.display' of [%s]...\", divId, x.style.display);");
            self.asCxProjectDataCollectionHtml.append("            if (x.style.display === \"none\") {");
            self.asCxProjectDataCollectionHtml.append("                x.style.display = \"block\";");
            self.asCxProjectDataCollectionHtml.append("            } else {");
            self.asCxProjectDataCollectionHtml.append("                x.style.display = \"none\";");
            self.asCxProjectDataCollectionHtml.append("            }");
            self.asCxProjectDataCollectionHtml.append("        }");
            self.asCxProjectDataCollectionHtml.append("");
            self.asCxProjectDataCollectionHtml.append("        $(window).load(function () {");

            for sCxProjectName in list(self.dictCxProjectDataCollection.keys()):

                cxProjectData = self.dictCxProjectDataCollection[sCxProjectName];

                if cxProjectData == None:

                    continue;

                self.asCxProjectDataCollectionHtml.append("            $(\".trigger_popup_lang%s\").click(function(){" % (cxProjectData.getCxProjectId()));
                self.asCxProjectDataCollectionHtml.append("               $('.hover_bkgr_lang%s').show();" % (cxProjectData.getCxProjectId()));
                self.asCxProjectDataCollectionHtml.append("            });");
                self.asCxProjectDataCollectionHtml.append("            $('.hover_bkgr_lang%s').click(function(){" % (cxProjectData.getCxProjectId()));
                self.asCxProjectDataCollectionHtml.append("                $('.hover_bkgr_lang%s').hide();" % (cxProjectData.getCxProjectId()));
                self.asCxProjectDataCollectionHtml.append("            });");
                self.asCxProjectDataCollectionHtml.append("            $('.popupCloseButton').click(function(){");
                self.asCxProjectDataCollectionHtml.append("                $('.hover_bkgr_lang%s').hide();" % (cxProjectData.getCxProjectId()));
                self.asCxProjectDataCollectionHtml.append("            });");

            self.asCxProjectDataCollectionHtml.append("        });");
            self.asCxProjectDataCollectionHtml.append("    </script>");
            self.asCxProjectDataCollectionHtml.append("</head>");
            self.asCxProjectDataCollectionHtml.append("");

            sPythonVers = ("v%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro));
            sServerNode = platform.node();
            dtNow       = datetime.now();
            sDTNowStamp = dtNow.strftime("%m/%d/%Y at %H:%M:%S");

            self.asCxProjectDataCollectionHtml.append("<body>");
            self.asCxProjectDataCollectionHtml.append("");
            self.asCxProjectDataCollectionHtml.append("<h1><center><b>Checkmarx collection for (%d) Project(s)</b></center></h1>" % \
                                                         (len(self.dictCxProjectDataCollection)));
            self.asCxProjectDataCollectionHtml.append("<h4><center>...Executed from Machine [%s] on [%s] under Python [%s]...</center></h4>" % \
                                                         (sServerNode, sDTNowStamp, sPythonVers));
            self.asCxProjectDataCollectionHtml.append("<br>");

            asCxProjectDataCollectionHtmlDebug.append("<br>");
            asCxProjectDataCollectionHtmlDebug.append("<div>");
            asCxProjectDataCollectionHtmlDebug.append("<h1><center><b>Checkmarx CxProjectData(s) collection for (%d) element(s)</b></center></h1>" % \
                                                         (len(self.dictCxProjectDataCollection)));
            asCxProjectDataCollectionHtmlDebug.append("<br>");

            self.asCxProjectDataCollectionHtml.append("<table border=\"2\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">");
            asCxProjectDataCollectionHtmlDebug.append("<table border=\"2\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">");

            sStyleWidth1 = "style=\"width:6%\"";
            sStyleWidth2 = "style=\"width:27%\"";
            sStyleWidth3 = "style=\"width:25%\"";

            self.asCxProjectDataCollectionHtml.append("<tr align=\"center\" bgcolor=\"deepskyblue\">");
            self.asCxProjectDataCollectionHtml.append("<td %s>Project</td>" % (sStyleWidth1));
            self.asCxProjectDataCollectionHtml.append("<td %s>Project Name</td>" % (sStyleWidth2));
            self.asCxProjectDataCollectionHtml.append("<td %s>Id</td>" % (sStyleWidth1));
            self.asCxProjectDataCollectionHtml.append("<td %s>Public?</td>" % (sStyleWidth1));
            self.asCxProjectDataCollectionHtml.append("<td %s>CxLang</td>" % (sStyleWidth1));
            self.asCxProjectDataCollectionHtml.append("<td %s>Risk Sev</td>" % (sStyleWidth1));
            self.asCxProjectDataCollectionHtml.append("<td %s>Risk Trend</td>" % (sStyleWidth1));
            self.asCxProjectDataCollectionHtml.append("<td %s>Team Id</td>" % (sStyleWidth3));
            self.asCxProjectDataCollectionHtml.append("<td %s>Total Number of Scans</td>" % (sStyleWidth1));
            self.asCxProjectDataCollectionHtml.append("<td %s></td>" % (sStyleWidth1));
            self.asCxProjectDataCollectionHtml.append("</tr>");

            cCxProjectDataCollection = 0;

            for sCxProjectName in list(self.dictCxProjectDataCollection.keys()):

                cCxProjectDataCollection += 1;

                cxProjectData = self.dictCxProjectDataCollection[sCxProjectName];

                if cxProjectData == None:

                    continue;

                sProjectTag = "#(%4d)" % (cCxProjectDataCollection); 

                self.asCxProjectDataCollectionHtml.append(cxProjectData.toPrettyStringForHtml(projecttag=sProjectTag));

                if self.bTraceFlag == True:

                    asCxProjectDataCollectionHtmlDebug.append("<tr bgcolor=\"deepskyblue\">");
                    asCxProjectDataCollectionHtmlDebug.append("<td>");
                    asCxProjectDataCollectionHtmlDebug.append("<center><b>CxProjectData element (named '%s')[(%d) of (%d)]</b></td></center>" % \
                                                                 (sCxProjectName, cCxProjectDataCollection, len(self.dictCxProjectDataCollection)));
                    asCxProjectDataCollectionHtmlDebug.append("</tr>");
                    asCxProjectDataCollectionHtmlDebug.append("<tr bgcolor=\"snow\">");
                    asCxProjectDataCollectionHtmlDebug.append("<td>");
                    asCxProjectDataCollectionHtmlDebug.append(cxProjectData.toString());
                    asCxProjectDataCollectionHtmlDebug.append("</td>");
                    asCxProjectDataCollectionHtmlDebug.append("</tr>");

            self.asCxProjectDataCollectionHtml.append("</table>");
            self.asCxProjectDataCollectionHtml.append("");

            if self.bTraceFlag == True:

                asCxProjectDataCollectionHtmlDebug.append("</table>");
                asCxProjectDataCollectionHtmlDebug.append("");
                asCxProjectDataCollectionHtmlDebug.append("</div>");
                asCxProjectDataCollectionHtmlDebug.append("");

                self.asCxProjectDataCollectionHtml.extend(asCxProjectDataCollectionHtmlDebug);

            self.asCxProjectDataCollectionHtml.append("");
            self.asCxProjectDataCollectionHtml.append("</body>");
            self.asCxProjectDataCollectionHtml.append("");
            self.asCxProjectDataCollectionHtml.append("</html>");
            self.asCxProjectDataCollectionHtml.append("");

        except Exception as inst:
 
            print("%s 'generateCxProjectDataCollectionHtml()' - exception occured..." % (self.sClassDisp));
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
 
    def saveCxProjectDataCollectionHtmlToFile(self, outputprojectdatacollectionhtmlfile=None):

    #   self.bTraceFlag = True;

        sOutputCxProjectDataCollectionHtmlFile = outputprojectdatacollectionhtmlfile;

        if sOutputCxProjectDataCollectionHtmlFile != None:

            sOutputCxProjectDataCollectionHtmlFile = sOutputCxProjectDataCollectionHtmlFile.strip();

        if sOutputCxProjectDataCollectionHtmlFile == None or \
           len(sOutputCxProjectDataCollectionHtmlFile) < 1:

            print("%s Command received an (Output) CxProjectData Collection Html filename that is 'null' or Empty - Error!" % (self.sClassDisp));

            return False;

        if self.asCxProjectDataCollectionHtml == None or \
            len(self.asCxProjectDataCollectionHtml) < 1:

            print("");
            print("%s The CxProjectData Collection 'Html' is 'None' or Empty - Severe Error!" % (self.sClassDisp));
 
            return False;

        try:

            print("%s Command is generating the (Output) CxProjectData Collection 'Html' into a file of [%s]..." % (self.sClassDisp, sOutputCxProjectDataCollectionHtmlFile));
            print("");

            fOutputCxProjectDataCollectionHtml = open(sOutputCxProjectDataCollectionHtmlFile, "w");

            fOutputCxProjectDataCollectionHtml.write('\n'.join(self.asCxProjectDataCollectionHtml));
            fOutputCxProjectDataCollectionHtml.close();

            print("%s Command generated the (Output) CxProjectData Collection 'Html' into a file of [%s]..." % (self.sClassDisp, sOutputCxProjectDataCollectionHtmlFile));
            print("");

        except Exception as inst:

            print("%s 'saveCxProjectDataCollectionHtmlToFile()' - operational exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

