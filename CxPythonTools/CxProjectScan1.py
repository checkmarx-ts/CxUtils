
import os;
import traceback;
import re;
import string;
import sys;
import collections;

import CxProjectData1;

class CxProjectScan(object):

    sClassMod                = __name__;
    sClassId                 = "CxProjectScan";
    sClassVers               = "(v1.0506)";
    sClassDisp               = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag               = False;
    cxProjectData            = None;            # Parent object...

    # --------------------------------------------------------------------------------------------------
    # Item #(1):
    #   Item #(1.1):  'status' <type 'dict'> [{u'details': 
    #                                          {u'step': u'', 
    #                                           u'stage': u''}, 
    #                                          u'name': u'Finished',
    #                                          u'id': 7}]...
    #   Item #(1.2):  'comment' <type 'unicode'> [Scan from CheckmarxXcodePlugin1]...
    #   Item #(1.3):  'resultsStatistics' <type 'dict'> [{u'link': None}]...
    #   Item #(1.4):  'scanType' <type 'dict'> [{u'id': 1, 
    #                                            u'value': u'Regular'}]...
    #   Item #(1.5):  'owningTeamId' <type 'unicode'> [00000000-1111-1111-b111-989c9070eb11]...
    #   Item #(1.6):  'dateAndTime' <type 'dict'> [{u'startedOn': u'2019-04-06T16:57:12.393', 
    #                                               u'finishedOn': u'2019-04-06T16:59:44.563', 
    #                                               u'engineStartedOn': u'2019-04-06T16:57:12.393', 
    #                                               u'engineFinishedOn': u'2019-04-06T16:59:44.54'}]...
    #   Item #(1.7):  'partialScanReasons' <type 'NoneType'> [None]...
    #   Item #(1.8):  'id' <type 'int'> [1450378]...
    #   Item #(1.9):  'scanState' <type 'dict'> [{u'languageStateCollection': 
    #                                            [{u'stateCreationDate': u'2018-08-29T20:05:16.59',
    #                                              u'languageID': 1073741824, 
    #                                              u'languageHash': u'0206692917308612', 
    #                                              u'languageName': u'Common'}, 
    #                                             {u'stateCreationDate': u'2018-08-29T20:05:16.59',
    #                                              u'languageID': 8, 
    #                                              u'languageHash': u'3602822811217894', 
    #                                              u'languageName': u'JavaScript'}, 
    #                                             {u'stateCreationDate': u'2018-08-29T20:05:16.59', 
    #                                              u'languageID': 4096,
    #                                              u'languageHash': u'0118406991696123', 
    #                                              u'languageName': u'Objc'}, 
    #                                             {u'stateCreationDate': u'2018-08-29T20:05:16.59', 
    #                                              u'languageID': 262144, 
    #                                              u'languageHash': u'1939975091058023', 
    #                                              u'languageName': u'Typescript'}, 
    #                                             {u'stateCreationDate': u'2017-11-15T13:45:50.393', 
    #                                              u'languageID': 64,
    #                                              u'languageHash': u'1349101913133594',
    #                                              u'languageName': u'VbScript'}],
    #                                             u'failedLinesOfCode': 0, 
    #                                             u'cxVersion': u'8.8.0.72 HF4',
    #                                             u'sourceId': u'0000000037_000836296494_00-689512115',
    #                                             u'filesCount': 37, 
    #                                             u'path': u' N/A (Zip File)',
    #                                             u'linesOfCode': 13341}]...
    #   Item #(1.10): 'isLocked' <type 'bool'> [False]...
    #   Item #(1.11): 'isIncremental' <type 'bool'> [True]...
    #   Item #(1.12): 'project' <type 'dict'> [{u'link': None,
    #                                           u'id': 390093, 
    #                                           u'name': u'CheckmarxXcodePlugin1'}]...
    #   Item #(1.13): 'origin' <type 'unicode'> [CheckmarxXcodePlugin1]...
    #   Item #(1.14): 'scanRisk' <type 'int'> [35]...
    #   Item #(1.15): 'initiatorName' <type 'unicode'> [admin admin]...
    #   Item #(1.16): 'scanRiskSeverity' <type 'int'> [19]...
    #   Item #(1.17): 'engineServer' <type 'dict'> [{u'link': None, 
    #                                                u'id': 1, 
    #                                                u'name': u'Localhost'}]...
    #   Item #(1.18): 'owner' <type 'unicode'> [dcox]...
    #   Item #(1.19): 'finishedScanStatus' <type 'dict'> [{u'id': 0, 
    #                                                      u'value': u'None'}]...
    #   Item #(1.20): 'isPublic' <type 'bool'> [True]...
    # --------------------------------------------------------------------------------------------------

    sCxScanId                = "-undefined-";
    iCxScanId                = 0;
    bCxScanIsPublic          = False;
    bCxScanIsIncremental     = False;           # New...
    sCxScanOwningTeamId      = None;
    sCxScanOrigin            = None;            # New...
    sCxScanRisk              = None;            # New...
    sCxScanRiskSeverity      = None;            # New...
    dictCxScanStatus         = [];
    dictCxScanStatusFinished = [];
    dictCxScanResultsStats   = [];
    dictCxScanState          = [];              # New...

    def __init__(self, trace=False, cxprojectdata=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxProjectData(cxprojectdata=cxprojectdata);

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

    def getCxProjectData(self):

        return self.cxProjectData;

    def setCxProjectData(self, cxprojectdata=None):

        self.cxProjectData = cxprojectdata;

    def getCxScanId(self):

        return self.sCxScanId;

    def setCxScanId(self, cxscanid=None):

        if type(cxscanid) == str:

            self.sCxScanId = cxscanid;

            if self.sCxScanId != None:

                self.sCxScanId = self.sCxScanId.strip();

            if self.sCxScanId == None or \
               len(self.sCxScanId) < 1:

                self.sCxScanId = "";
                self.iCxScanId = -1;

            else:

                self.iCxScanId = int(self.sCxScanId);

        else:

            self.iCxScanId = cxscanid;

            if self.iCxScanId < 0:

                self.sCxScanId = "";
                self.iCxScanId = -1;

            else:

                self.sCxScanId = ("%d" % self.iCxScanId);

    def getCxScanIsPublic(self):

        return self.bCxScanIsPublic;

    def setCxScanIsPublic(self, cxscanispublic=False):

        self.bCxScanIsPublic = cxscanispublic;

    def getCxScanIsIncremental(self):

        return self.bCxScanIsIncremental;

    def setCxScanIsIncremental(self, cxscanisincremental=False):

        self.bCxScanIsIncremental = cxscanisincremental;

    def getCxScanOwningTeamId(self):

        return self.sCxScanOwningTeamId;

    def setCxScanOwningTeamId(self, cxscanowningteamid=None):

        if cxscanowningteamid == None:

            return;

        if type(cxscanowningteamid) == str:

            self.sCxScanOwningTeamId = cxscanowningteamid;

            if self.sCxScanOwningTeamId != None:

                self.sCxScanOwningTeamId = self.sCxScanOwningTeamId.strip();

            if self.sCxScanOwningTeamId == None or \
               len(self.sCxScanOwningTeamId) < 1:

                self.sCxScanOwningTeamId = "0";

        else:

            self.iCxScanOwningTeamId = cxscanowningteamid;

            if self.iCxScanOwningTeamId < 0:

                self.sCxScanOwningTeamId = "0";

            else:

                self.sCxScanOwningTeamId = ("%d" % self.iCxScanOwningTeamId);
         
    def getCxScanOrigin(self):

        return self.sCxScanOrigin;

    def setCxScanOrigin(self, cxscanorigin=None):

        self.sCxScanOrigin = cxscanorigin;

        if self.sCxScanOrigin == None or \
           len(self.sCxScanOrigin) < 1:

            self.sCxScanOrigin = None;

    def getCxScanRisk(self):

        return self.sCxScanRisk;

    def setCxScanRisk(self, cxscanrisk=None):

        if type(cxscanrisk) == str:

            self.sCxScanRisk = cxscanrisk;

            if self.sCxScanRisk != None:

                self.sCxScanRisk = self.sCxScanRisk.strip();

            if self.sCxScanRisk == None or \
               len(self.sCxScanRisk) < 1:

                self.sCxScanRisk = None;

        else:

            if cxscanrisk < 0:

                self.sCxScanRisk = None;

            else:

                self.sCxScanRisk = ("%d" % cxscanrisk);

    def getCxScanRiskSeverity(self):

        return self.sCxScanRiskSeverity;

    def setCxScanRiskSeverity(self, cxscanriskseverity=None):

        if type(cxscanriskseverity) == str:

            self.sCxScanRiskSeverity = cxscanriskseverity;

            if self.sCxScanRiskSeverity != None:

                self.sCxScanRiskSeverity = self.sCxScanRiskSeverity.strip();

            if self.sCxScanRiskSeverity == None or \
               len(self.sCxScanRiskSeverity) < 1:

                self.sCxScanRiskSeverity = None;

        else:

            if cxscanriskseverity < 0:

                self.sCxScanRiskSeverity = None;

            else:

                self.sCxScanRiskSeverity = ("%d" % cxscanriskseverity);

    def getCxScanStatus(self):

        return self.dictCxScanStatus;

    def setCxScanStatus(self, cxscanstatus=None):

        self.dictCxScanStatus = cxscanstatus;

    def getCxScanStatusFinished(self):

        return self.dictCxScanStatusFinished;

    def setCxScanStatusFinished(self, cxscanstatusfinished=None):

        self.dictCxScanStatusFinished = cxscanstatusfinished;

    def getCxScanResultsStats(self):

        return self.dictCxScanResultsStats;

    def setCxScanResultsStats(self, cxscanresultsstats=None):

        self.dictCxScanResultsStats = cxscanresultsstats;

    def getCxScanState(self):

        return self.dictCxScanState;

    def setCxScanState(self, cxscanstate=None):

        self.dictCxScanState = cxscanstate;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'sCxScanId' is [%s]..." % (self.sClassDisp, self.sCxScanId));
            print("%s The contents of 'iCxScanId' is (%d)..." % (self.sClassDisp, self.iCxScanId));
            print("%s The contents of 'bCxScanIsPublic' is [%s]..." % (self.sClassDisp, self.bCxScanIsPublic));
            print("%s The contents of 'bCxScanIsIncremental' is [%s]..." % (self.sClassDisp, self.bCxScanIsIncremental));
            print("%s The contents of 'sCxScanOwningTeamId' is [%s]..." % (self.sClassDisp, self.sCxScanOwningTeamId));
            print("%s The contents of 'sCxScanOrigin' is [%s]..." % (self.sClassDisp, self.sCxScanOrigin));
            print("%s The contents of 'sCxScanRisk' is [%s]..." % (self.sClassDisp, self.sCxScanRisk));
            print("%s The contents of 'sCxScanRiskSeverity' is [%s]..." % (self.sClassDisp, self.sCxScanRiskSeverity));
            print("%s The contents of 'dictCxScanStatus' is [%s]..." % (self.sClassDisp, self.dictCxScanStatus));
            print("%s The contents of 'dictCxScanStatusFinished' is [%s]..." % (self.sClassDisp, self.dictCxScanStatusFinished));
            print("%s The contents of 'dictCxScanResultsStats' is [%s]..." % (self.sClassDisp, self.dictCxScanResultsStats));
            print("%s The contents of 'dictCxScanState' is [%s]..." % (self.sClassDisp, self.dictCxScanState));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'sCxScanId' is [%s], " % (self.sCxScanId));
        asObjDetail.append("'iCxScanId' is (%d), " % (self.iCxScanId));
        asObjDetail.append("'bCxScanIsPublic' is [%s], " % (self.bCxScanIsPublic));
        asObjDetail.append("'bCxScanIsIncremental' is [%s], " % (self.bCxScanIsIncremental));
        asObjDetail.append("'sCxScanOwningTeamId' is [%s], " % (self.sCxScanOwningTeamId));
        asObjDetail.append("'sCxScanOrigin' is [%s], " % (self.sCxScanOrigin));
        asObjDetail.append("'sCxScanRisk' is [%s], " % (self.sCxScanRisk));
        asObjDetail.append("'sCxScanRiskSeverity' is [%s], " % (self.sCxScanRiskSeverity));
        asObjDetail.append("'dictCxScanStatus' is [%s], " % (self.dictCxScanStatus));
        asObjDetail.append("'dictCxScanStatusFinished' is [%s], " % (self.dictCxScanStatusFinished));
        asObjDetail.append("'dictCxScanResultsStats' is [%s], " % (self.dictCxScanResultsStats));
        asObjDetail.append("'dictCxScanState' is [%s]. " % (self.dictCxScanState));

        return ''.join(asObjDetail);

    def toPrettyString(self):

        return self.toPrettyStringWithWidths();

    def toPrettyStringWithWidths(self, cWidthId=6, cWidthStatus=3, cWidthStatusFinished=3, cWidthOwningTeamId=36, cWidthName=70):

        asObjDetail = list();

        asObjDetail.append("'Id' [%*s], " % (cWidthId, self.sCxScanId));
        asObjDetail.append("'Public?' [%5s], " % (self.bCxScanIsPublic));
        asObjDetail.append("'# Status field(s)' (%*d), " % (cWidthStatus, len(self.dictCxScanStatus)));
        asObjDetail.append("'# S. Finished field(s)' (%*d), " % (cWidthStatusFinished, len(self.dictCxScanStatusFinished)));
        asObjDetail.append("'# R. Stats field(s)' (%1d), " % (len(self.dictCxScanResultsStats)));
        asObjDetail.append("'O. TeamId' [%*s], " % (cWidthOwningTeamId, self.sCxScanOwningTeamId));

        sCxProjectName = self.cxProjectData.getCxProjectName();

        if sCxProjectName != None:

            sCxProjectName = sCxProjectName.strip();

        if sCxProjectName == None or \
            len(sCxProjectName) < 1:

            sCxProjectName = "-undefined-";
         
        asObjDetail.append("'Name' [%-*s], " % (cWidthName, sCxProjectName));

        return ''.join(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

