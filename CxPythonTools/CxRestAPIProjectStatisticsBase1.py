
import os;
import traceback;
import platform;
import re;
import string;
import sys;
import collections;
import requests;
import json;

from datetime import datetime;

import CxProjectData1;
import CxProjectScan1;
import CxServerEndpoint1;
import CxRestAPIStatistics1;
import CxRestAPITokenAuthenticationBase1;

class CxRestAPIProjectStatisticsBase(object):

    sClassMod               = __name__;
    sClassId                = "CxRestAPIProjectStatisticsBase";
    sClassVers              = "(v1.0515)";
    sClassDisp              = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag              = False;
    cxServerEndpoint        = None;
    cxProjectDataCollection = None;

    # Constructed objects:

    cxRestAPITokenAuth      = None;

    def __init__(self, trace=False, cxserverendpoint=None, cxprojectdatacollection=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxServerEndpoint(cxserverendpoint=cxserverendpoint);
            self.setCxProjectDataCollection(cxprojectdatacollection=cxprojectdatacollection);

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

        return self.cxProjectDataCollection;

    def setCxProjectDataCollection(self, cxprojectdatacollection=None):

        self.cxProjectDataCollection = cxprojectdatacollection;

    def resetCxRestAPIProjectStatisticsBase(self):

        return;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'cxServerEndpoint' is [%s]..." % (self.sClassDisp, self.cxServerEndpoint));
            print("%s The contents of 'cxProjectDataCollection' is [%s]..." % (self.sClassDisp, self.cxProjectDataCollection));
            print("%s The contents of 'cxRestAPITokenAuth' is [%s]..." % (self.sClassDisp, self.cxRestAPITokenAuth));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'cxServerEndpoint' is [%s], " % (self.cxServerEndpoint));
        asObjDetail.append("'cxProjectDataCollection' is [%s], " % (self.cxProjectDataCollection));
        asObjDetail.append("'cxRestAPITokenAuth' is [%s]. " % (self.cxRestAPITokenAuth));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def getCxRestAPIProjectDataMetaData(self):

        if self.cxServerEndpoint == None:

            print("");
            print("%s NO CxServerEndpoint has been specified nor defined - a CxServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxServerEndpoint.getCxServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxProjectDataCollection == None:

            print("");
            print("%s NO CxProjectDataCollection has been specified nor defined - a CxProjectDataCollection MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            sCxAccessToken = self.cxServerEndpoint.getCxAccessToken();

            if sCxAccessToken != None:

                sCxAccessToken = sCxAccessToken.strip();

            if sCxAccessToken == None or \
                len(sCxAccessToken) < 1:

                bGetCxAuthTokenOk = self.getCxRestAPIAuthToken();

                if bGetCxAuthTokenOk == False:

                    print("");
                    print("%s Invocation of 'getCxRestAPIAuthToken()' failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            bGetCxAllTeams = self.getCxRestAPIAllTeams();

            if bGetCxAllTeams == False:

                print("");
                print("%s Invocation of 'getCxRestAPIAllTeams()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxProjectDataCollection (after 1st 'meta' data) is:" % (self.sClassDisp));
                print(self.cxProjectDataCollection.toString());
                print("");

            bGetCxAllPresets = self.getCxRestAPIAllPresets();

            if bGetCxAllPresets == False:

                print("");
                print("%s Invocation of 'getCxRestAPIAllPresets()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxProjectDataCollection (after 2nd 'meta' data) is:" % (self.sClassDisp));
                print(self.cxProjectDataCollection.toString());
                print("");

            bGetCxAllEngineConfigurations = self.getCxRestAPIAllEngineConfigurations();

            if bGetCxAllEngineConfigurations == False:

                print("");
                print("%s Invocation of 'getCxRestAPIAllEngineConfigurations()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxProjectDataCollection (after 3rd 'meta' data) is:" % (self.sClassDisp));
                print(self.cxProjectDataCollection.toString());
                print("");

        except Exception as inst:

            print("%s 'getCxRestAPIProjectDataMetaData()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def getCxRestAPIProjectStatistics(self):

        if self.cxServerEndpoint == None:

            print("");
            print("%s NO CxServerEndpoint has been specified nor defined - a CxServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxServerEndpoint.getCxServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxProjectDataCollection == None:

            print("");
            print("%s NO CxProjectDataCollection has been specified nor defined - a CxProjectDataCollection MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            sCxAccessToken = self.cxServerEndpoint.getCxAccessToken();

            if sCxAccessToken != None:

                sCxAccessToken = sCxAccessToken.strip();

            if sCxAccessToken == None or \
                len(sCxAccessToken) < 1:

                bGetCxAuthTokenOk = self.getCxRestAPIAuthToken();

                if bGetCxAuthTokenOk == False:

                    print("");
                    print("%s Invocation of 'getCxRestAPIAuthToken()' failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            bGetCxProjectDataOk = self.getCxRestAPIProjectData();

            if bGetCxProjectDataOk == False:

                print("");
                print("%s Invocation of 'getCxRestAPIProjectData()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.cxProjectDataCollection.dictCxProjectDataCollection == None or \
               len(self.cxProjectDataCollection.dictCxProjectDataCollection) < 1:

                print("");
                print("%s NO Checkmarx CxProjectData(s) have been specified nor defined in the Checkmarx CxProjectData(s) Collection - at least 1 CxProjectData MUST be defined - Error!" % (self.sClassDisp));
                print("");

                return False;

            cCxProject = 0;

            for sCxProjectName in list(self.cxProjectDataCollection.dictCxProjectDataCollection.keys()):

                cCxProject += 1;

                cxProjectData = self.cxProjectDataCollection.dictCxProjectDataCollection[sCxProjectName];

                if cxProjectData == None:

                    continue;

                bGetCxProjectScansOk = self.getCxRestAPIProjectScans(cxprojectdata=cxProjectData);

                if bGetCxProjectScansOk == False:

                    print("");
                    print("%s Invocation of 'getCxRestAPIProjectScans()' failed - Error!" % (self.sClassDisp));
                    print("");

        except Exception as inst:

            print("%s 'getCxRestAPIProjectStatistics()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def getCxRestAPIAuthToken(self):

        if self.cxServerEndpoint == None:

            print("");
            print("%s NO CxServerEndpoint has been specified nor defined - a CxServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxServerEndpoint.getCxServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            self.cxRestAPITokenAuth = CxRestAPITokenAuthenticationBase1.CxRestAPITokenAuthenticationBase(trace=self.bTraceFlag, cxserverendpoint=self.cxServerEndpoint);

            bGetCxRestAPIAuthTokenOk = self.cxRestAPITokenAuth.getCxRestAPITokenAuthentication();

            if bGetCxRestAPIAuthTokenOk == False:

                print("");
                print("%s Invocation of 'cxRestAPITokenAuth.getCxRestAPITokenAuthentication()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'getCxRestAPIAuthToken()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def getCxRestAPIProjectData(self):

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/projects" % (self.cxServerEndpoint.getCxServerURL());
            cxReqPayload = "";
            cxReqHeaders = {
                'Content-Type':  "application/json;v=1.0 / 2.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [200];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("GET", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
             
            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {ALL Project(s)} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {ALL Project(s)} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {ALL Project(s)} ===============");
                print(sReqResponseRaw);

            listCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'list' Response {ALL Project(s)} ===============");
                print((type(listCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'list' Response {ALL Project(s)} ===============");
                print((dir(listCxReqResponseJson)));

                print("");
                print("=============== JSON 'list' Response {ALL Project(s)} [RAW print] ===============");
                print(listCxReqResponseJson);

                print("");
                print("=============== JSON 'list' Response {ALL Project(s)} Enumerated ===============");

            cListJsonItem = 0;

            for listCxReqResponseJsonItem in listCxReqResponseJson:

                if listCxReqResponseJsonItem == None:

                    continue;

                cListJsonItem += 1;

                if self.bTraceFlag == True:

                    print(("  Item #(%d): <raw> {%s} [%s]..." % (cListJsonItem, type(listCxReqResponseJsonItem), listCxReqResponseJsonItem)));

                dictCxReqResponseJson = listCxReqResponseJsonItem;

                cDictJsonItem = 0;
                cxProjectData = CxProjectData1.CxProjectData(trace=self.bTraceFlag);

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("    Item #(%d.%d): '%s' %s [%s]..." % (cListJsonItem, cDictJsonItem, dictCxReqResponseJsonKey, type(dictCxReqResponseJsonItem), dictCxReqResponseJsonItem)));

                    # --------------------------------------------------------------------------------------------------
                    # Item #(13):
                    #   Item #(13.1): 'name' [CheckmarxXcodePlugin1]...
                    #   Item #(13.2): 'links' [[{u'uri': u'/projects/390093', u'rel': u'self'}, 
                    #                           {u'uri': u'/auth/teams/', u'rel': u'teams'}, 
                    #                           {u'uri': u'/sast/scans?projectId=390093&last=1', u'rel': u'latestscan'}, 
                    #                           {u'uri': u'/sast/scans?projectId=390093', u'rel': u'allscans'}, 
                    #                           {u'uri': u'/sast/scanSettings/390093', u'rel': u'scansettings'}, 
                    #                           {u'type': u'local', u'uri': None, u'rel': u'source'}]]...
                    #   Item #(13.3): 'isPublic' [True]...
                    #   Item #(13.4): 'teamId' [00000000-1111-1111-b111-989c9070eb11]...
                    #   Item #(13.5): 'customFields' [[]]...
                    #   Item #(13.6): 'id' [390093]...
                    # --------------------------------------------------------------------------------------------------

                    if dictCxReqResponseJsonKey == "name":

                        cxProjectData.setCxProjectName(cxprojectname=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "id":

                        cxProjectData.setCxProjectId(cxprojectid=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "isPublic":

                        cxProjectData.setCxProjectIsPublic(cxprojectispublic=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "teamId":

                        cxProjectData.setCxProjectTeamId(cxprojectteamid=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "links":

                        cxProjectData.setCxProjectLinks(cxprojectlinks=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "customFields":

                        cxProjectData.setCxProjectCustomFields(cxprojectcustomfields=dictCxReqResponseJsonItem);

                self.cxProjectDataCollection.addCxProjectDataToCxProjectDataCollection(cxprojectdata=cxProjectData);

        except Exception as inst:

            print("%s 'getCxRestAPIProjectData()' - exception occured..." % (self.sClassDisp));
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

    def getCxRestAPIProjectScans(self, cxprojectdata=None):

        cxProjectData = cxprojectdata;

        if cxProjectData == None:

            print("");
            print("%s NO CxProjectData has been specified nor defined for the request - a CxProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/sast/scans?projectId=%s" % (self.cxServerEndpoint.getCxServerURL(), cxProjectData.getCxProjectId());
            cxReqPayload = "";
            cxReqHeaders = {
                'Content-Type':  "application/json;v=1.0 / 2.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [200];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("GET", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
             
            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {ALL Project Scan(s)} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {ALL Project Scan(s)} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {ALL Project Scan(s)} ===============");
                print(sReqResponseRaw);

            listCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'list' Response {ALL Project Scan(s)} ===============");
                print((type(listCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'list' Response {ALL Project Scan(s)} ===============");
                print((dir(listCxReqResponseJson)));

                print("");
                print("=============== JSON 'list' Response {ALL Project Scan(s)} [RAW print] ===============");
                print(listCxReqResponseJson);

                print("");
                print("=============== JSON 'list' Response {ALL Project Scan(s)} Enumerated ===============");

            cListJsonItem = 0;

            for listCxReqResponseJsonItem in listCxReqResponseJson:

                if listCxReqResponseJsonItem == None:

                    continue;

                cListJsonItem += 1;

                if self.bTraceFlag == True:

                    print(("  Item #(%d): <raw> {%s} [%s]..." % (cListJsonItem, type(listCxReqResponseJsonItem), listCxReqResponseJsonItem)));

                dictCxReqResponseJson = listCxReqResponseJsonItem;

                cDictJsonItem = 0;
                cxProjectScan = CxProjectScan1.CxProjectScan(trace=self.bTraceFlag, cxprojectdata=cxProjectData);

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("    Item #(%d.%d): '%s' %s [%s]..." % (cListJsonItem, cDictJsonItem, dictCxReqResponseJsonKey, type(dictCxReqResponseJsonItem), dictCxReqResponseJsonItem)));

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

                    if dictCxReqResponseJsonKey == "id":
             
                        cxProjectScan.setCxScanId(cxscanid=dictCxReqResponseJsonItem);
             
                    if dictCxReqResponseJsonKey == "isPublic":
             
                        cxProjectScan.setCxScanIsPublic(cxscanispublic=dictCxReqResponseJsonItem);
             
                    if dictCxReqResponseJsonKey == "owningTeamId":
             
                        cxProjectScan.setCxScanOwningTeamId(cxscanowningteamid=dictCxReqResponseJsonItem);
             
                    if dictCxReqResponseJsonKey == "status":
             
                        cxProjectScan.setCxScanStatus(cxscanstatus=dictCxReqResponseJsonItem);
             
                    if dictCxReqResponseJsonKey == "finishedScanStatus":
             
                        cxProjectScan.setCxScanStatusFinished(cxscanstatusfinished=dictCxReqResponseJsonItem);

                        if self.bTraceFlag == True:

                            print(("    <Debug> Set CxProjectScan field of 'finishedScanStatus' to [%s] from [%s]..." % (cxProjectScan.dictCxScanStatusFinished, dictCxReqResponseJsonItem)));
             
                    # NEW field(s):
                    #
                    # cxProjectScan.bCxScanIsIncremental     = False; # New...
                    # cxProjectScan.sCxScanOrigin            = None;  # New...
                    # cxProjectScan.sCxScanRisk              = None;  # New...
                    # cxProjectScan.sCxScanRiskSeverity      = None;  # New...
                    # cxProjectScan.dictCxScanState          = [];    # New...

                    if dictCxReqResponseJsonKey == "isIncremental":
             
                        cxProjectScan.setCxScanIsIncremental(cxscanisincremental=dictCxReqResponseJsonItem);
             
                    if dictCxReqResponseJsonKey == "origin":

                        cxProjectScan.setCxScanOrigin(cxscanorigin=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "scanRisk":

                        cxProjectScan.setCxScanRisk(cxscanrisk=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "scanRiskSeverity":

                        cxProjectScan.setCxScanRiskSeverity(cxscanriskseverity=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "scanState":
             
                        cxProjectScan.setCxScanState(cxscanstate=dictCxReqResponseJsonItem);

                if self.bTraceFlag == True:

                    print(("    Adding a CxProjectScan object of [%s] to the CxProjectData..." % (cxProjectScan.toString())));

                cxProjectData.addCxProjectScanToCxProjectData(cxprojectscan=cxProjectScan);

                self.getCxRestAPIProjectScanResultsStats(cxprojectscan=cxProjectScan);

                if self.bTraceFlag == True:

                    print(("    Added a CxProjectScan object of [%s] to the CxProjectData of [%s]..." % (cxProjectScan.toString(), cxProjectData.toString())));

        except Exception as inst:

            print("%s 'getCxRestAPIProjectScans()' - exception occured..." % (self.sClassDisp));
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

    def getCxRestAPIProjectScanResultsStats(self, cxprojectscan=None):

        cxProjectScan = cxprojectscan;

        if cxProjectScan == None:

            print("");
            print("%s NO CxProjectScan has been specified nor defined for the request - a CxProjectScan MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/sast/scans/%s/resultsStatistics?id=%s" % (self.cxServerEndpoint.getCxServerURL(), cxProjectScan.getCxScanId(), cxProjectScan.getCxScanId());
            cxReqPayload = "";
            cxReqHeaders = {
                'Content-Type':  "application/json;v=1.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [200, 404];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("GET", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
             
            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {Project Scan Results Stats} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {Project Scan Results Stats} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {Project Scan Results Stats} ===============");
                print(sReqResponseRaw);

            dictCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'dict' Response {Project Scan Results Stats} ===============");
                print((type(dictCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'dict' Response {Project Scan Results Stats} ===============");
                print((dir(dictCxReqResponseJson)));

                print("");
                print("=============== JSON 'dict' Response {Project Scan Results Stats} [RAW print] ===============");
                print(dictCxReqResponseJson);

                print("");
                print("=============== JSON 'dict' Response {Project Scan Results Stats} Enumerated ===============");

            cDictJsonItem = 0;

            for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                if dictCxReqResponseJsonKey == None:

                    continue;

                cDictJsonItem += 1;

                dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                if self.bTraceFlag == True:

                    print(("    Item #(%d): '%s' %s [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, type(dictCxReqResponseJsonItem), dictCxReqResponseJsonItem)));

                # --------------------------------------------------------------------------------------------------
                # Item #(1): 'infoSeverity' <type 'int'> [0]...
                # Item #(2): 'lowSeverity' <type 'int'> [27]...
                # Item #(3): 'statisticsCalculationDate' <type 'unicode'> [2019-04-06T16:59:44.84]...
                # Item #(4): 'mediumSeverity' <type 'int'> [6]...
                # Item #(5): 'highSeverity' <type 'int'> [0]...
                # --------------------------------------------------------------------------------------------------

            if self.bTraceFlag == True:

                print(("    Adding a 'dictCxReqResponseJson' object of [%s] to the CxProjectScan..." % (dictCxReqResponseJson)));

            cxProjectScan.setCxScanResultsStats(cxscanresultsstats=dictCxReqResponseJson);

        except Exception as inst:

            print("%s 'getCxRestAPIProjectScanResultsStats()' - exception occured..." % (self.sClassDisp));
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

    def getCxRestAPIAllTeams(self):

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/auth/teams" % (self.cxServerEndpoint.getCxServerURL());
            cxReqPayload = "";
            cxReqHeaders = {
                'Content-Type':  "application/json;v=1.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [200];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("GET", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
             
            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {ALL Team(s)} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {ALL Team(s)} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {ALL Team(s)} ===============");
                print(sReqResponseRaw);

            listCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'list' Response {ALL Team(s)} ===============");
                print((type(listCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'list' Response {ALL Team(s)} ===============");
                print((dir(listCxReqResponseJson)));

                print("");
                print("=============== JSON 'list' Response {ALL Team(s)} [RAW print] ===============");
                print(listCxReqResponseJson);

                print("");
                print("=============== JSON 'list' Response {ALL Team(s)} Enumerated ===============");

            cListJsonItem = 0;

            for listCxReqResponseJsonItem in listCxReqResponseJson:

                if listCxReqResponseJsonItem == None:

                    continue;

                cListJsonItem += 1;

                if self.bTraceFlag == True:

                    print(("  Item #(%d): <raw> {%s} [%s]..." % (cListJsonItem, type(listCxReqResponseJsonItem), listCxReqResponseJsonItem)));

                dictCxReqResponseJson = listCxReqResponseJsonItem;

                cDictJsonItem   = 0;
                sCxTeamFullName = "";
                sCxTeamId       = "";

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("    Item #(%d.%d): '%s' %s [%s]..." % (cListJsonItem, cDictJsonItem, dictCxReqResponseJsonKey, type(dictCxReqResponseJsonItem), dictCxReqResponseJsonItem)));

                    # --------------------------------------------------------------------------------------------------
                    # Item #(1): <raw> {<type 'dict'>} [{u'fullName': u'\\CxServer', u'id': u'00000000-1111-1111-b111-989c9070eb11'}]...
                    #   Item #(1.1): 'fullName' <type 'unicode'> [\CxServer]...
                    #   Item #(1.2): 'id' <type 'unicode'> [00000000-1111-1111-b111-989c9070eb11]...
                    # --------------------------------------------------------------------------------------------------

                    if dictCxReqResponseJsonKey == "fullName":

                        if type(dictCxReqResponseJsonItem) == str:

                            sCxTeamFullName = dictCxReqResponseJsonItem.encode('ascii', 'ignore');

                        else:

                            sCxTeamFullName = dictCxReqResponseJsonItem;

                    if dictCxReqResponseJsonKey == "id":

                        sCxTeamId = dictCxReqResponseJsonItem;

                self.cxProjectDataCollection.addCxProjectMetaDataAllTeams(cxteamfullname=sCxTeamFullName, cxteamid=sCxTeamId);

        except Exception as inst:

            print("%s 'getCxRestAPIAllTeams()' - exception occured..." % (self.sClassDisp));
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

    def getCxRestAPIAllPresets(self):

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/sast/presets" % (self.cxServerEndpoint.getCxServerURL());
            cxReqPayload = "";
            cxReqHeaders = {
                'Content-Type':  "application/json;v=1.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [200];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("GET", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
             
            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {All Preset(s)} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {All Preset(s)} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {All Preset(s)} ===============");
                print(sReqResponseRaw);

            listCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'list' Response {All Preset(s)} ===============");
                print((type(listCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'list' Response {All Preset(s)} ===============");
                print((dir(listCxReqResponseJson)));

                print("");
                print("=============== JSON 'list' Response {All Preset(s)} [RAW print] ===============");
                print(listCxReqResponseJson);

                print("");
                print("=============== JSON 'list' Response {All Preset(s)} Enumerated ===============");

            cListJsonItem = 0;

            for listCxReqResponseJsonItem in listCxReqResponseJson:

                if listCxReqResponseJsonItem == None:

                    continue;

                cListJsonItem += 1;

                if self.bTraceFlag == True:

                    print(("  Item #(%d): <raw> {%s} [%s]..." % (cListJsonItem, type(listCxReqResponseJsonItem), listCxReqResponseJsonItem)));

                dictCxReqResponseJson = listCxReqResponseJsonItem;

                cDictJsonItem      = 0;
                sCxPresetName      = "";
                sCxPresetOwnerName = "";
                sCxPresetId        = "";

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("    Item #(%d.%d): '%s' %s [%s]..." % (cListJsonItem, cDictJsonItem, dictCxReqResponseJsonKey, type(dictCxReqResponseJsonItem), dictCxReqResponseJsonItem)));

                    # --------------------------------------------------------------------------------------------------
                    # Item #(1): <raw> {<type 'dict'>} [{u'fullName': u'\\CxServer', u'id': u'00000000-1111-1111-b111-989c9070eb11'}]...
                    #   Item #(1.1): 'fullName' <type 'unicode'> [\CxServer]...
                    #   Item #(1.2): 'id' <type 'unicode'> [00000000-1111-1111-b111-989c9070eb11]...
                    # --------------------------------------------------------------------------------------------------

                    if dictCxReqResponseJsonKey == "name":

                        if type(dictCxReqResponseJsonItem) == str:

                            sCxPresetName = dictCxReqResponseJsonItem.encode('ascii', 'ignore');

                        else:

                            sCxPresetName = dictCxReqResponseJsonItem;

                    if dictCxReqResponseJsonKey == "ownerName":

                        if type(dictCxReqResponseJsonItem) == str:

                            sCxPresetOwnerName = dictCxReqResponseJsonItem.encode('ascii', 'ignore');

                        else:

                            sCxPresetOwnerName = dictCxReqResponseJsonItem;

                    if dictCxReqResponseJsonKey == "id":

                        sCxPresetId = "%d" % (dictCxReqResponseJsonItem);

                dictCxPreset = collections.defaultdict();

                dictCxPreset["name"]      = sCxPresetName;
                dictCxPreset["ownerName"] = sCxPresetOwnerName;
                dictCxPreset["id"]        = sCxPresetId;

                self.cxProjectDataCollection.addCxProjectMetaDataAllPresets(cxpresetname=sCxPresetName, cxpresetdict=dictCxPreset);

        except Exception as inst:

            print("%s 'getCxRestAPIAllPresets()' - exception occured..." % (self.sClassDisp));
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

    def getCxRestAPIAllEngineConfigurations(self):

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/sast/engineConfigurations" % (self.cxServerEndpoint.getCxServerURL());
            cxReqPayload = "";
            cxReqHeaders = {
                'Content-Type':  "application/json;v=1.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [200];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("GET", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
             
            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {ALL EngineConfiguration(s)} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {ALL EngineConfiguration(s)} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {ALL EngineConfiguration(s)} ===============");
                print(sReqResponseRaw);

            listCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'list' Response {ALL EngineConfiguration(s)} ===============");
                print((type(listCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'list' Response {ALL EngineConfiguration(s)} ===============");
                print((dir(listCxReqResponseJson)));

                print("");
                print("=============== JSON 'list' Response {ALL EngineConfiguration(s)} [RAW print] ===============");
                print(listCxReqResponseJson);

                print("");
                print("=============== JSON 'list' Response {ALL EngineConfiguration(s)} Enumerated ===============");

            cListJsonItem = 0;

            for listCxReqResponseJsonItem in listCxReqResponseJson:

                if listCxReqResponseJsonItem == None:

                    continue;

                cListJsonItem += 1;

                if self.bTraceFlag == True:

                    print(("  Item #(%d): <raw> {%s} [%s]..." % (cListJsonItem, type(listCxReqResponseJsonItem), listCxReqResponseJsonItem)));

                dictCxReqResponseJson = listCxReqResponseJsonItem;

                cDictJsonItem       = 0;
                sCxEngineConfigName = "";
                sCxEngineConfigId   = "";

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("    Item #(%d.%d): '%s' %s [%s]..." % (cListJsonItem, cDictJsonItem, dictCxReqResponseJsonKey, type(dictCxReqResponseJsonItem), dictCxReqResponseJsonItem)));

                    # --------------------------------------------------------------------------------------------------
                    # Item #(4): <raw> {<type 'dict'>} [{u'id': 5, u'name': u'Multi-language Scan'}]...
                    #   Item #(4.1): 'id' <type 'int'> [5]...
                    #   Item #(4.2): 'name' <type 'unicode'> [Multi-language Scan]...
                    # --------------------------------------------------------------------------------------------------

                    if dictCxReqResponseJsonKey == "name":

                        if type(dictCxReqResponseJsonItem) == str:

                            sCxEngineConfigName = dictCxReqResponseJsonItem.encode('ascii', 'ignore');

                        else:

                            sCxEngineConfigName = dictCxReqResponseJsonItem;

                    if dictCxReqResponseJsonKey == "id":

                        sCxEngineConfigId = "%d" % (dictCxReqResponseJsonItem);

                self.cxProjectDataCollection.addCxProjectMetaDataAllEngineConfigurations(cxengineconfigname=sCxEngineConfigName, cxengineconfigid=sCxEngineConfigId);

        except Exception as inst:

            print("%s 'getCxRestAPIAllEngineConfigurations()' - exception occured..." % (self.sClassDisp));
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

