
import os;
import traceback;
import platform;
import re;
import string;
import sys;
import collections;

from datetime import datetime;

import CxTFSProjectData1;
import CxTFSServerEndpoint1;
import CxTFSProjectsRestAPIBase1;

class CxTFSProjectDataCollection(object):

    sClassMod                          = __name__;
    sClassId                           = "CxTFSProjectDataCollection";
    sClassVers                         = "(v1.0306)";
    sClassDisp                         = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                         = False;
    cxTFSServerEndpoint                = None;
    sCxTFSCollectionName               = None;
    dictCxTFSProjectDataCollection     = None;
    asCxTFSProjectDataCollectionReport = None;

    # CxRestAPI object(s):

    cxTFSProjectsRestAPI               = None;

    # Misc. variables:

    sPlatform                          = None;
    bPlatformIsWindows                 = False;

    def __init__(self, trace=False, cxtfsserverendpoint=None, cxtfscollection=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxTFSServerEndpoint(cxtfsserverendpoint=cxtfsserverendpoint);
            self.setCxTFSCollectionName(cxtfscollection=cxtfscollection);

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

    def getCxTFSServerEndpoint(self):

        return self.cxTFSServerEndpoint;

    def setCxTFSServerEndpoint(self, cxtfsserverendpoint=None):

        self.cxTFSServerEndpoint = cxtfsserverendpoint;

    def getCxTFSCollectionName(self):

        return self.sCxTFSCollectionName;

    def setCxTFSCollectionName(self, cxtfscollection=None):

        self.sCxTFSCollectionName = cxtfscollection;

    def getCxTFSProjectDataCollection(self):

        return self.dictCxTFSProjectDataCollection;

    def setCxTFSProjectDataCollection(self, cxtfsprojectdatacollection=None):

        self.dictCxTFSProjectDataCollection = cxtfsprojectdatacollection;

    def getCxTFSProjectDataCollectionReportAsList(self):

        return self.asCxTFSProjectDataCollectionReport;

    def getCxProjectInitialDataAllTeams(self):

        return self.dictCxAllTeams;

    def addCxProjectInitialDataAllTeams(self, cxteamfullname=None, cxteamid=None):

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

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));

            if self.cxTFSServerEndpoint == None:

                print("%s The 'cxTFSServerEndpoint' has NOT been set..." % (self.sClassDisp));

            else:

                print("%s The 'cxTFSServerEndpoint' is [%s]..." % (self.sClassDisp, self.cxTFSServerEndpoint));

            print("%s The 'sCxTFSCollectionName' boolean is [%s]..." % (self.sClassDisp, self.sCxTFSCollectionName));

            if self.dictCxTFSProjectDataCollection == None:

                print("%s The 'dictCxTFSProjectDataCollection' has NOT been set..." % (self.sClassDisp));

            else:

                print("%s The 'dictCxTFSProjectDataCollection' is [%s]..." % (self.sClassDisp, self.dictCxTFSProjectDataCollection));

            print("%s The contents of 'asCxTFSProjectDataCollectionReport' is [%s]..." % (self.sClassDisp, self.asCxTFSProjectDataCollectionReport));
            print("%s The contents of 'sPlatform' is [%s]..." % (self.sClassDisp, self.sPlatform));
            print("%s The contents of 'bPlatformIsWindows' is [%s]..." % (self.sClassDisp, self.bPlatformIsWindows));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'cxTFSServerEndpoint' is [%s], " % (self.cxTFSServerEndpoint));
        asObjDetail.append("'sCxTFSCollectionName' is [%s], " % (self.sCxTFSCollectionName));
        asObjDetail.append("'dictCxTFSProjectDataCollection' is [%s], " % (self.dictCxTFSProjectDataCollection));
        asObjDetail.append("'asCxTFSProjectDataCollectionReport' is [%s], " % (self.asCxTFSProjectDataCollectionReport));
        asObjDetail.append("'sPlatform' is [%s], " % (self.sPlatform));
        asObjDetail.append("'bPlatformIsWindows' is [%s]. " % (self.bPlatformIsWindows));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def addCxTFSProjectDataToCxTFSProjectDataCollection(self, cxtfsprojectdata=None):

    #   self.bTraceFlag = True;

        cxTFSProjectData = cxtfsprojectdata;

        if cxTFSProjectData == None:

            print("");
            print("%s NO CxTFSProjectData has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxTFSProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.dictCxTFSProjectDataCollection == None:

            if self.bTraceFlag == True:

                print("%s The object 'dictCxTFSProjectDataCollection' has NOT been set - creating an internal instance..." % (self.sClassDisp));

            self.dictCxTFSProjectDataCollection = collections.defaultdict(); 

        bProcessingError = False;

        try:

            sCxProjectName = cxTFSProjectData.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxTFSProjectData has a 'name' that is None or 'empty' - bypassing the addition of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            self.dictCxTFSProjectDataCollection[sCxProjectName] = cxTFSProjectData;

            if self.bTraceFlag == True:

                print("%s CxTFSProjectData named [%s] of [%s] added to the CxTFSProjectDataCollection..." % (self.sClassDisp, sCxProjectName, cxTFSProjectData));

        except Exception as inst:

            print("%s 'addCxTFSProjectDataToCxTFSProjectDataCollection()' - exception occured..." % (self.sClassDisp));
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

    def loadCxTFSProjectDataInitialDataToCollectionFromRestAPI(self):

    #   self.bTraceFlag = True;

        if self.cxTFSServerEndpoint == None:

            print("");
            print("%s NO CxTFSServerEndpoint has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxTFSServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxTFSServerEndpoint.getCxTFSServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxTFSServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            if self.cxTFSProjectsRestAPI == None:

                self.cxTFSProjectsRestAPI = CxTFSProjectsRestAPIBase1.CxTFSProjectsRestAPIBase(trace=self.bTraceFlag, cxtfsserverendpoint=self.cxTFSServerEndpoint, cxtfsprojectdatacollection=self);

                if self.cxTFSProjectsRestAPI == None:

                    print("");
                    print("%s Failed to create a CxTFSProjectsRestAPIBase object - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            bGetProjInitialDataOk = self.cxTFSProjectsRestAPI.getCxTFSProjectsInitialDataViaRestAPI();

            if bGetProjInitialDataOk == False:

                print("");
                print("%s 'cxTFSProjectsRestAPI.getCxTFSProjectsInitialDataViaRestAPI()' API call failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.dictCxTFSProjectDataCollection != None and \
               len(self.dictCxTFSProjectDataCollection) > 0:

                bGetProjDetailsCollectionTeamDataOk = self.loadCxTFSProjectsDetailCollectionTeamData();

                if bGetProjDetailsCollectionTeamDataOk == False:

                    print("");
                    print("%s 'loadCxTFSProjectsDetailCollectionTeamData()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

        except Exception as inst:

            print("%s 'loadCxTFSProjectDataInitialDataToCollectionFromRestAPI()' - exception occured..." % (self.sClassDisp));
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

    def loadCxTFSProjectsDetailCollectionTeamData(self):

        if self.cxTFSServerEndpoint == None:

            print("");
            print("%s NO CxTFSServerEndpoint has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxTFSServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxTFSServerEndpoint.getCxTFSServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxTFSServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.dictCxTFSProjectDataCollection == None or \
           len(self.dictCxTFSProjectDataCollection) < 1:

            print("");
            print("%s NO Checkmarx CxTFSProjectData(s) have been specified nor defined in the Checkmarx CxTFSProjectData(s) Collection - at least 1 CxTFSProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            if self.cxTFSProjectsRestAPI == None:

                self.cxTFSProjectsRestAPI = CxTFSProjectsRestAPIBase1.CxTFSProjectsRestAPIBase(trace=self.bTraceFlag, cxtfsserverendpoint=self.cxTFSServerEndpoint, cxtfsprojectdatacollection=self);

                if self.cxTFSProjectsRestAPI == None:

                    print("");
                    print("%s Failed to create a CxTFSProjectsRestAPIBase object - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            cCxTFSProjectDataCollection = 0;
         
            for sCxProjectName in list(self.dictCxTFSProjectDataCollection.keys()):
         
                cCxTFSProjectDataCollection += 1;
         
                cxTFSProjectData = self.dictCxTFSProjectDataCollection[sCxProjectName];
         
                if cxTFSProjectData == None:
         
                    continue;
         
                bGetProjDetailsDataOk = self.cxTFSProjectsRestAPI.getCxTFSProjectDetailsDataViaRestAPI(cxtfsprojectdata=cxTFSProjectData);

                if bGetProjDetailsDataOk == False:

                    print("");
                    print("%s 'cxTFSProjectsRestAPI.getCxTFSProjectDetailsDataViaRestAPI()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

        except Exception as inst:
 
            print("%s 'loadCxTFSProjectsDetailCollectionTeamData()' - exception occured..." % (self.sClassDisp));
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
 
    def generateCxTFSProjectDataCollectionReport(self):
 
        bProcessingError = False;

        try:

            asCxTFSProjectDataCollectionReportDebug = list();
            self.asCxTFSProjectDataCollectionReport = list();

            if self.dictCxTFSProjectDataCollection == None or \
               len(self.dictCxTFSProjectDataCollection) < 1:

                print("");
                print("%s NO Checkmarx CxTFSProjectData(s) have been specified nor defined in the Checkmarx CxTFSProjectData(s) Collection - at least 1 CxTFSProjectData MUST be defined - Warning!" % (self.sClassDisp));
                print("");

                self.asCxTFSProjectDataCollectionReport.append("");
                self.asCxTFSProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                self.asCxTFSProjectDataCollectionReport.append("%s Checkmarx CxTFSProjectData(s) collection is 'empty'..." % \
                                                                (self.sClassDisp));
                self.asCxTFSProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                self.asCxTFSProjectDataCollectionReport.append("");

            else:

                self.asCxTFSProjectDataCollectionReport.append("");
                self.asCxTFSProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                self.asCxTFSProjectDataCollectionReport.append("%s Checkmarx CxTFSProjectData(s) collection for (%d) element(s):" % \
                                                                (self.sClassDisp, len(self.dictCxTFSProjectDataCollection)));
                self.asCxTFSProjectDataCollectionReport.append("");

                asCxTFSProjectDataCollectionReportDebug.append("");
                asCxTFSProjectDataCollectionReportDebug.append("- - - - - - - - - - - - - - - - DEBUG - - - - - - - - - - - - - - - - - - - - - -");
                asCxTFSProjectDataCollectionReportDebug.append("%s Checkmarx CxTFSProjectData(s) collection for (%d) element(s):" % \
                                                           (self.sClassDisp, len(self.dictCxTFSProjectDataCollection)));
                asCxTFSProjectDataCollectionReportDebug.append("");

                cCxTFSProjectDataCollection = 0;

                for sCxProjectName in list(self.dictCxTFSProjectDataCollection.keys()):

                    cCxTFSProjectDataCollection += 1;

                    cxTFSProjectData = self.dictCxTFSProjectDataCollection[sCxProjectName];

                    if cxTFSProjectData == None:

                        continue;

                    self.asCxTFSProjectDataCollectionReport.append("%s CxTFSProjectData element (%3d) of (%3d):" % \
                                                                    (self.sClassDisp, cCxTFSProjectDataCollection, len(self.dictCxTFSProjectDataCollection)));
                    self.asCxTFSProjectDataCollectionReport.append(cxTFSProjectData.toPrettyString());

                    if self.bTraceFlag == True:

                        asCxTFSProjectDataCollectionReportDebug.append("%s CxTFSProjectData element (named '%s') [(%d) of (%d)] is:" % \
                                                                (self.sClassDisp, sCxProjectName, cCxTFSProjectDataCollection, len(self.dictCxTFSProjectDataCollection)));
                        asCxTFSProjectDataCollectionReportDebug.append(cxTFSProjectData.toString());
                        asCxTFSProjectDataCollectionReportDebug.append("");

                self.asCxTFSProjectDataCollectionReport.append("");
                self.asCxTFSProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                self.asCxTFSProjectDataCollectionReport.append("");

                if self.bTraceFlag == True:

                    asCxTFSProjectDataCollectionReportDebug.append("");
                    asCxTFSProjectDataCollectionReportDebug.append("- - - - - - - - - - - - - - - - DEBUG - - - - - - - - - - - - - - - - - - - - - -");
                    asCxTFSProjectDataCollectionReportDebug.append("");

                    self.asCxTFSProjectDataCollectionReport.extend(asCxTFSProjectDataCollectionReportDebug);

            if self.cxTFSProjectsRestAPI != None:

                asCxTFSRestResponses = self.cxTFSProjectsRestAPI.getCxTFSRestResponses();

                if asCxTFSRestResponses != None and \
                   len(asCxTFSRestResponses) > 0:

                    self.asCxTFSProjectDataCollectionReport.append("");
                    self.asCxTFSProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - Rest API Json response(s) - - - - - - - - - - - -");
                    self.asCxTFSProjectDataCollectionReport.append("");
                    self.asCxTFSProjectDataCollectionReport.append('\n'.join(asCxTFSRestResponses));
                    self.asCxTFSProjectDataCollectionReport.append("");
                    self.asCxTFSProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                    self.asCxTFSProjectDataCollectionReport.append("");

        except Exception as inst:
 
            print("%s 'generateCxTFSProjectDataCollectionReport()' - exception occured..." % (self.sClassDisp));
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
 
    def saveCxTFSProjectDataCollectionReportToFile(self, outputprojectdatacollectionreportfile=None):

    #   self.bTraceFlag = True;

        sOutputCxTFSProjectDataCollectionReportFile = outputprojectdatacollectionreportfile;

        if sOutputCxTFSProjectDataCollectionReportFile != None:

            sOutputCxTFSProjectDataCollectionReportFile = sOutputCxTFSProjectDataCollectionReportFile.strip();

        if sOutputCxTFSProjectDataCollectionReportFile == None or \
           len(sOutputCxTFSProjectDataCollectionReportFile) < 1:

            print("%s Command received an (Output) CxTFSProjectData Collection report filename that is 'null' or Empty - Error!" % (self.sClassDisp));

            return False;

        if self.asCxTFSProjectDataCollectionReport == None or \
           len(self.asCxTFSProjectDataCollectionReport) < 1:

            print("");
            print("%s The CxTFSProjectData Collection 'report' is 'None' or Empty - Severe Error!" % (self.sClassDisp));
 
            return False;

        try:

            print("%s Command is generating the (Output) CxTFSProjectData Collection 'report' into a file of [%s]..." % (self.sClassDisp, sOutputCxTFSProjectDataCollectionReportFile));

            fOutputCxTFSProjectDataCollectionReport = open(sOutputCxTFSProjectDataCollectionReportFile, "w");

            fOutputCxTFSProjectDataCollectionReport.write('\n'.join(self.asCxTFSProjectDataCollectionReport));
            fOutputCxTFSProjectDataCollectionReport.close();

            print("%s Command generated the (Output) CxTFSProjectData Collection 'report' into a file of [%s]..." % (self.sClassDisp, sOutputCxTFSProjectDataCollectionReportFile));
            print("");

        except Exception as inst:

            print("%s 'saveCxTFSProjectDataCollectionReportToFile()' - operational exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def saveCxTFSProjectDataCollectionAsPlistsToDirectory(self, outputprojectdatacollectionplistsdir=None):

        sOutputProjectDataCollectionPlistsDirspec = outputprojectdatacollectionplistsdir;

        if sOutputProjectDataCollectionPlistsDirspec != None:

            sOutputProjectDataCollectionPlistsDirspec = sOutputProjectDataCollectionPlistsDirspec.strip();

        if sOutputProjectDataCollectionPlistsDirspec == None or \
            len(sOutputProjectDataCollectionPlistsDirspec) < 1:

            print("");
            print("%s The supplied (Output) 'plists' directory is None or Empty - this MUST be supplied - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            if self.dictCxTFSProjectDataCollection == None or \
               len(self.dictCxTFSProjectDataCollection) < 1:

                print("");
                print("%s NO Checkmarx CxTFSProjectData(s) have been specified nor defined in the Checkmarx CxTFSProjectData(s) Collection - at least 1 CxTFSProjectData MUST be defined - Warning!" % (self.sClassDisp));
                print("");

                return False;

            print("%s Command is generating the (Output) CxTFSProjectData Collection named [%s] 'plist(s)' into a directory of [%s]..." % (self.sClassDisp, self.sCxTFSCollectionName, sOutputProjectDataCollectionPlistsDirspec));

            for sCxProjectName in list(self.dictCxTFSProjectDataCollection.keys()):

                cxTFSProjectData = self.dictCxTFSProjectDataCollection[sCxProjectName];

                if cxTFSProjectData == None:

                    continue;

                bSaveCxTFSProjectDataToPlistOk = cxTFSProjectData.saveCxTFSProjectDataAsPlistToDirectory(outputprojectdataplistdir=sOutputProjectDataCollectionPlistsDirspec, cxtfscollection=self.sCxTFSCollectionName);

                if bSaveCxTFSProjectDataToPlistOk == False:

                    print("");
                    print("%s The CxTFSProjectData named [%s] for a TFS Collection named [%s] 'plist' failed to save to the directory [%s] - Error!" % (self.sClassDisp, cxTFSProjectData.getCxProjectName(), self.sCxTFSCollectionName, sOutputProjectDataCollectionPlistsDirspec));
                    print("");

                    bProcessingError = True;

            print("%s Command is generated the (Output) CxTFSProjectData Collection named [%s] 'plist(s)' into a directory of [%s]..." % (self.sClassDisp, self.sCxTFSCollectionName, sOutputProjectDataCollectionPlistsDirspec));
            print("");

        except Exception as inst:
 
            print("%s 'saveCxTFSProjectDataCollectionAsPlistsToDirectory()' - exception occured..." % (self.sClassDisp));
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
 
