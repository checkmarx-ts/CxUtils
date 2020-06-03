
import os;
import traceback;
import platform;
import re;
import string;
import sys;
import collections;
import plistlib;

from datetime import datetime;

import CxGitLabProjectData1;
import CxGitLabServerEndpoint1;
import CxGitLabProjectsRestAPIBase1;

class CxGitLabProjectDataCollection(object):

    sClassMod                             = __name__;
    sClassId                              = "CxGitLabProjectDataCollection";
    sClassVers                            = "(v1.0209)";
    sClassDisp                            = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                            = False;
    cxGitLabServerEndpoint                = None;
    dictCxGitLabProjectDataCollection     = None;
    asCxGitLabProjectDataCollectionReport = None;

    # CxRestAPI object(s):

    cxGitLabProjectsRestAPI               = None;

    # Misc. variables:

    sPlatform                             = None;
    bPlatformIsWindows                    = False;

    def __init__(self, trace=False, cxgitlabserverendpoint=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxGitLabServerEndpoint(cxgitlabserverendpoint=cxgitlabserverendpoint);

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

    def getCxGitLabServerEndpoint(self):

        return self.cxGitLabServerEndpoint;

    def setCxGitLabServerEndpoint(self, cxgitlabserverendpoint=None):

        self.cxGitLabServerEndpoint = cxgitlabserverendpoint;

    def getCxGitLabProjectDataCollection(self):

        return self.dictCxGitLabProjectDataCollection;

    def setCxGitLabProjectDataCollection(self, cxgitlabprojectdatacollection=None):

        self.dictCxGitLabProjectDataCollection = cxgitlabprojectdatacollection;

    def getCxGitLabProjectDataCollectionReportAsList(self):

        return self.asCxGitLabProjectDataCollectionReport;

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

            if self.cxGitLabServerEndpoint == None:

                print("%s The 'cxGitLabServerEndpoint' has NOT been set..." % (self.sClassDisp));

            else:

                print("%s The 'cxGitLabServerEndpoint' is [%s]..." % (self.sClassDisp, self.cxGitLabServerEndpoint));

            if self.dictCxGitLabProjectDataCollection == None:

                print("%s The 'dictCxGitLabProjectDataCollection' has NOT been set..." % (self.sClassDisp));

            else:

                print("%s The 'dictCxGitLabProjectDataCollection' is [%s]..." % (self.sClassDisp, self.dictCxGitLabProjectDataCollection));

            print("%s The contents of 'asCxGitLabProjectDataCollectionReport' is [%s]..." % (self.sClassDisp, self.asCxGitLabProjectDataCollectionReport));
            print("%s The contents of 'sPlatform' is [%s]..." % (self.sClassDisp, self.sPlatform));
            print("%s The contents of 'bPlatformIsWindows' is [%s]..." % (self.sClassDisp, self.bPlatformIsWindows));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'cxGitLabServerEndpoint' is [%s], " % (self.cxGitLabServerEndpoint));
        asObjDetail.append("'dictCxGitLabProjectDataCollection' is [%s], " % (self.dictCxGitLabProjectDataCollection));
        asObjDetail.append("'asCxGitLabProjectDataCollectionReport' is [%s], " % (self.asCxGitLabProjectDataCollectionReport));
        asObjDetail.append("'sPlatform' is [%s], " % (self.sPlatform));
        asObjDetail.append("'bPlatformIsWindows' is [%s]. " % (self.bPlatformIsWindows));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def addCxGitLabProjectDataToCxGitLabProjectDataCollection(self, cxgitlabprojectdata=None):

    #   self.bTraceFlag = True;

        cxGitLabProjectData = cxgitlabprojectdata;

        if cxGitLabProjectData == None:

            print("");
            print("%s NO CxGitLabProjectData has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxGitLabProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.dictCxGitLabProjectDataCollection == None:

            if self.bTraceFlag == True:

                print("%s The object 'dictCxGitLabProjectDataCollection' has NOT been set - creating an internal instance..." % (self.sClassDisp));

            self.dictCxGitLabProjectDataCollection = collections.defaultdict(); 

        bProcessingError = False;

        try:

            sCxGitLabProjectName = cxGitLabProjectData.getCxGitLabProjectName();

            if sCxGitLabProjectName != None:

                sCxGitLabProjectName = sCxGitLabProjectName.strip();

            if sCxGitLabProjectName == None or \
                len(sCxGitLabProjectName) < 1:

                print("");
                print("%s The CxGitLabProjectData has a 'name' that is None or 'empty' - bypassing the addition of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            self.dictCxGitLabProjectDataCollection[sCxGitLabProjectName] = cxGitLabProjectData;

            if self.bTraceFlag == True:

                print("%s CxGitLabProjectData named [%s] of [%s] added to the CxGitLabProjectDataCollection..." % (self.sClassDisp, sCxGitLabProjectName, cxGitLabProjectData));

        except Exception as inst:

            print("%s 'addCxGitLabProjectDataToCxGitLabProjectDataCollection()' - exception occured..." % (self.sClassDisp));
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

    def loadCxGitLabProjectDataInitialDataToCollectionFromRestAPI(self):

    #   self.bTraceFlag = True;

        if self.cxGitLabServerEndpoint == None:

            print("");
            print("%s NO CxGitLabServerEndpoint has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxGitLabServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxGitLabServerEndpoint.getCxGitLabServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxGitLabServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            if self.cxGitLabProjectsRestAPI == None:

                self.cxGitLabProjectsRestAPI = CxGitLabProjectsRestAPIBase1.CxGitLabProjectsRestAPIBase(trace=self.bTraceFlag, cxgitlabserverendpoint=self.cxGitLabServerEndpoint, cxgitlabprojectdatacollection=self);

                if self.cxGitLabProjectsRestAPI == None:

                    print("");
                    print("%s Failed to create a CxGitLabProjectsRestAPIBase object - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            bGetProjInitialDataOk = self.cxGitLabProjectsRestAPI.getCxGitLabProjectsInitialDataViaRestAPI();

            if bGetProjInitialDataOk == False:

                print("");
                print("%s 'cxGitLabProjectsRestAPI.getCxGitLabProjectsInitialDataViaRestAPI()' API call failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'loadCxGitLabProjectDataInitialDataToCollectionFromRestAPI()' - exception occured..." % (self.sClassDisp));
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

    def generateCxGitLabProjectDataCollectionReport(self):
 
        bProcessingError = False;

        try:

            asCxGitLabProjectDataCollectionReportDebug = list();
            self.asCxGitLabProjectDataCollectionReport = list();

            if self.dictCxGitLabProjectDataCollection == None or \
               len(self.dictCxGitLabProjectDataCollection) < 1:

                print("");
                print("%s NO Checkmarx CxGitLabProjectData(s) have been specified nor defined in the Checkmarx CxGitLabProjectData(s) Collection - at least 1 CxGitLabProjectData MUST be defined - Warning!" % (self.sClassDisp));
                print("");

                self.asCxGitLabProjectDataCollectionReport.append("");
                self.asCxGitLabProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                self.asCxGitLabProjectDataCollectionReport.append("%s Checkmarx CxGitLabProjectData(s) collection is 'empty'..." % \
                                                                (self.sClassDisp));
                self.asCxGitLabProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                self.asCxGitLabProjectDataCollectionReport.append("");

            else:

                self.asCxGitLabProjectDataCollectionReport.append("");
                self.asCxGitLabProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                self.asCxGitLabProjectDataCollectionReport.append("%s Checkmarx CxGitLabProjectData(s) collection for (%d) element(s):" % \
                                                                (self.sClassDisp, len(self.dictCxGitLabProjectDataCollection)));
                self.asCxGitLabProjectDataCollectionReport.append("");

                asCxGitLabProjectDataCollectionReportDebug.append("");
                asCxGitLabProjectDataCollectionReportDebug.append("- - - - - - - - - - - - - - - - DEBUG - - - - - - - - - - - - - - - - - - - - - -");
                asCxGitLabProjectDataCollectionReportDebug.append("%s Checkmarx CxGitLabProjectData(s) collection for (%d) element(s):" % \
                                                           (self.sClassDisp, len(self.dictCxGitLabProjectDataCollection)));
                asCxGitLabProjectDataCollectionReportDebug.append("");

                cCxGitLabProjectDataCollection = 0;

                for sCxProjectName in list(self.dictCxGitLabProjectDataCollection.keys()):

                    cCxGitLabProjectDataCollection += 1;

                    cxGitLabProjectData = self.dictCxGitLabProjectDataCollection[sCxProjectName];

                    if cxGitLabProjectData == None:

                        continue;

                    self.asCxGitLabProjectDataCollectionReport.append("%s CxGitLabProjectData element (%3d) of (%3d):" % \
                                                                    (self.sClassDisp, cCxGitLabProjectDataCollection, len(self.dictCxGitLabProjectDataCollection)));
                    self.asCxGitLabProjectDataCollectionReport.append(cxGitLabProjectData.toPrettyString());

                    if self.bTraceFlag == True:

                        asCxGitLabProjectDataCollectionReportDebug.append("%s CxGitLabProjectData element (named '%s') [(%d) of (%d)] is:" % \
                                                                (self.sClassDisp, sCxProjectName, cCxGitLabProjectDataCollection, len(self.dictCxGitLabProjectDataCollection)));
                        asCxGitLabProjectDataCollectionReportDebug.append(cxGitLabProjectData.toString());
                        asCxGitLabProjectDataCollectionReportDebug.append("");

                self.asCxGitLabProjectDataCollectionReport.append("");
                self.asCxGitLabProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                self.asCxGitLabProjectDataCollectionReport.append("");

                if self.bTraceFlag == True:

                    asCxGitLabProjectDataCollectionReportDebug.append("");
                    asCxGitLabProjectDataCollectionReportDebug.append("- - - - - - - - - - - - - - - - DEBUG - - - - - - - - - - - - - - - - - - - - - -");
                    asCxGitLabProjectDataCollectionReportDebug.append("");

                    self.asCxGitLabProjectDataCollectionReport.extend(asCxGitLabProjectDataCollectionReportDebug);

            if self.cxGitLabProjectsRestAPI != None:

                asCxGitLabRestResponses = self.cxGitLabProjectsRestAPI.getCxGitLabRestResponses();

                if asCxGitLabRestResponses != None and \
                   len(asCxGitLabRestResponses) > 0:

                    self.asCxGitLabProjectDataCollectionReport.append("");
                    self.asCxGitLabProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - Rest API Json response(s) - - - - - - - - - - - -");
                    self.asCxGitLabProjectDataCollectionReport.append("");
                    self.asCxGitLabProjectDataCollectionReport.append('\n'.join(asCxGitLabRestResponses));
                    self.asCxGitLabProjectDataCollectionReport.append("");
                    self.asCxGitLabProjectDataCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
                    self.asCxGitLabProjectDataCollectionReport.append("");

        except Exception as inst:
 
            print("%s 'generateCxGitLabProjectDataCollectionReport()' - exception occured..." % (self.sClassDisp));
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
 
    def saveCxGitLabProjectDataCollectionReportToFile(self, outputprojectdatacollectionreportfile=None):

    #   self.bTraceFlag = True;

        sOutputCxGitLabProjectDataCollectionReportFile = outputprojectdatacollectionreportfile;

        if sOutputCxGitLabProjectDataCollectionReportFile != None:

            sOutputCxGitLabProjectDataCollectionReportFile = sOutputCxGitLabProjectDataCollectionReportFile.strip();

        if sOutputCxGitLabProjectDataCollectionReportFile == None or \
           len(sOutputCxGitLabProjectDataCollectionReportFile) < 1:

            print("%s Command received an (Output) CxGitLabProjectData Collection report filename that is 'null' or Empty - Error!" % (self.sClassDisp));

            return False;

        if self.asCxGitLabProjectDataCollectionReport == None or \
           len(self.asCxGitLabProjectDataCollectionReport) < 1:

            print("");
            print("%s The CxGitLabProjectData Collection 'report' is 'None' or Empty - Severe Error!" % (self.sClassDisp));
 
            return False;

        try:

            print("%s Command is generating the (Output) CxGitLabProjectData Collection 'report' into a file of [%s]..." % (self.sClassDisp, sOutputCxGitLabProjectDataCollectionReportFile));

            fOutputCxGitLabProjectDataCollectionReport = open(sOutputCxGitLabProjectDataCollectionReportFile, "w");

            fOutputCxGitLabProjectDataCollectionReport.write('\n'.join(self.asCxGitLabProjectDataCollectionReport));
            fOutputCxGitLabProjectDataCollectionReport.close();

            print("%s Command generated the (Output) CxGitLabProjectData Collection 'report' into a file of [%s]..." % (self.sClassDisp, sOutputCxGitLabProjectDataCollectionReportFile));
            print("");

        except Exception as inst:

            print("%s 'saveCxGitLabProjectDataCollectionReportToFile()' - operational exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def saveCxGitLabProjectDataCollectionAsPlistToDirectory(self, outputprojectdatacollectionplistsdir=None):

        sOutputProjectDataCollectionPlistsDirspec = outputprojectdatacollectionplistsdir;

        if sOutputProjectDataCollectionPlistsDirspec != None:

            sOutputProjectDataCollectionPlistsDirspec = sOutputProjectDataCollectionPlistsDirspec.strip();

        if sOutputProjectDataCollectionPlistsDirspec == None or \
            len(sOutputProjectDataCollectionPlistsDirspec) < 1:

            print("");
            print("%s The supplied (Output) 'plists' directory is None or Empty - this MUST be supplied - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxGitLabServerEndpoint == None:

            print("");
            print("%s NO CxGitLabServerEndpoint has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxGitLabServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxGitLabServerEndpoint.getCxGitLabServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxGitLabServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            if self.dictCxGitLabProjectDataCollection == None or \
               len(self.dictCxGitLabProjectDataCollection) < 1:

                print("");
                print("%s NO Checkmarx CxGitLabProjectData(s) have been specified nor defined in the Checkmarx CxGitLabProjectData(s) Collection - at least 1 CxGitLabProjectData MUST be defined - Warning!" % (self.sClassDisp));
                print("");

                return False;

            print("%s Command is generating the (Output) CxGitLabProjectData 'plist' into a directory of [%s]..." % (self.sClassDisp, sOutputProjectDataCollectionPlistsDirspec));

            # Generate the (Output) 'plist' Dictionary:
            
            dictOutputCxGitLabProjectPlist    = {};
            listOutputCxGitLabProjectAppRepos = [];
            
            dictOutputCxGitLabProjectPlist["AppName"]      = self.cxGitLabServerEndpoint.getCxGitLabGroup();
            dictOutputCxGitLabProjectPlist["AppIsActive"]  = "true";
            dictOutputCxGitLabProjectPlist["AppGroupName"] = self.cxGitLabServerEndpoint.getCxGitLabGroup(); 
            dictOutputCxGitLabProjectPlist["AppProjectId"] = "0";
            dictOutputCxGitLabProjectPlist["AppScanType"]  = "both";
            
            for sCxGitLabProjectName in list(self.dictCxGitLabProjectDataCollection.keys()):

                cxGitLabProjectData = self.dictCxGitLabProjectDataCollection[sCxGitLabProjectName];

                if cxGitLabProjectData == None:

                    continue;

                dictCxGitLabProjectData = cxGitLabProjectData.generateCxGitLabProjectDataAsDirectory();

                if dictCxGitLabProjectData == None:

                    print("");
                    print("%s The CxGitLabProjectData named [%s] for a GitLab Collection failed to generate to a Dictionary object - Error!" % (self.sClassDisp, sCxGitLabProjectName));
                    print("");

                    bProcessingError = True;

                if self.bTraceFlag == True:

                    print("%s Returned 'dictCxGitLabProjectData' is [%s]..." % (self.sClassDisp, dictCxGitLabProjectData));

                listOutputCxGitLabProjectAppRepos.append(dictCxGitLabProjectData);

            dictOutputCxGitLabProjectPlist["AppRepos"] = listOutputCxGitLabProjectAppRepos;

            if self.bTraceFlag == True:

                print("%s Generated 'dictOutputCxGitLabProjectPlist' is [%s]..." % (self.sClassDisp, dictOutputCxGitLabProjectPlist));

            # Generate the (Output) 'plist' file from the Dictionary:

            sOutputCxGitLabProjectFile = os.path.join(sOutputProjectDataCollectionPlistsDirspec, ("%s.plist" % (self.cxGitLabServerEndpoint.getCxGitLabGroup())));
         
            print("%s Generating the (Output) 'plist' file of [%s]..." % (self.sClassDisp, sOutputCxGitLabProjectFile));
         
            plistlib.writePlist(dictOutputCxGitLabProjectPlist, sOutputCxGitLabProjectFile);
         
            print("%s Generated the (Output) 'plist' file of [%s] into a directory of [%s]..." % (self.sClassDisp, sOutputCxGitLabProjectFile, sOutputProjectDataCollectionPlistsDirspec));
            print("");

        except Exception as inst:
 
            print("%s 'saveCxGitLabProjectDataCollectionAsPlistToDirectory()' - exception occured..." % (self.sClassDisp));
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
 
