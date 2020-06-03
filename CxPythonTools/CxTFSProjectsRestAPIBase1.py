
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

import CxTFSProjectData1;
import CxTFSServerEndpoint1;
import CxRestAPIStatistics1;

class CxTFSProjectsRestAPIBase(object):

    sClassMod                  = __name__;
    sClassId                   = "CxTFSProjectsRestAPIBase";
    sClassVers                 = "(v1.0306)";
    sClassDisp                 = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                 = False;
    cxTFSServerEndpoint        = None;
    cxTFSProjectDataCollection = None;

    # Constructed objects:

    sCxTFSBase64UserAndPAT     = None;
    sCxTFSServerURL            = None;
    asCxTFSRestResponses       = list();

    def __init__(self, trace=False, cxtfsserverendpoint=None, cxtfsprojectdatacollection=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxTFSServerEndpoint(cxtfsserverendpoint=cxtfsserverendpoint);
            self.setCxTFSProjectDataCollection(cxtfsprojectdatacollection=cxtfsprojectdatacollection);

            sPythonVers = ("v%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro));
            sServerNode = platform.node();
            dtNow       = datetime.now();
            sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

            sHeaderMsg = ("%s The Checkmarx TFS 'Get-ALL-Projects' via Rest API #1 is starting execution from Server [%s] on [%s] under Python [%s]..." % (self.sClassDisp, sServerNode, sDTNowStamp, sPythonVers));

            self.asCxTFSRestResponses.append("");
            self.asCxTFSRestResponses.append(sHeaderMsg);
            self.asCxTFSRestResponses.append("");

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

    def getCxTFSProjectDataCollection(self):

        return self.cxTFSProjectDataCollection;

    def setCxTFSProjectDataCollection(self, cxtfsprojectdatacollection=None):

        self.cxTFSProjectDataCollection = cxtfsprojectdatacollection;

    def getCxTFSRestResponses(self):

        return self.asCxTFSRestResponses;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'cxTFSServerEndpoint' is [%s]..." % (self.sClassDisp, self.cxTFSServerEndpoint));
            print("%s The contents of 'cxTFSProjectDataCollection' is [%s]..." % (self.sClassDisp, self.cxTFSProjectDataCollection));
            print("%s The contents of 'sCxTFSBase64UserAndPAT' is [%s]..." % (self.sClassDisp, self.sCxTFSBase64UserAndPAT));
            print("%s The contents of 'sCxTFSServerURL' is [%s]..." % (self.sClassDisp, self.sCxTFSServerURL));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'cxTFSServerEndpoint' is [%s], " % (self.cxTFSServerEndpoint));
        asObjDetail.append("'cxTFSProjectDataCollection' is [%s], " % (self.cxTFSProjectDataCollection));
        asObjDetail.append("'sCxTFSBase64UserAndPAT' is [%s] " % (self.sCxTFSBase64UserAndPAT));
        asObjDetail.append("'sCxTFSServerURL' is [%s]. " % (self.sCxTFSServerURL));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def validateCxTFSProjectRequiredFields(self):

        try:

            if self.cxTFSProjectDataCollection == None:

                print("");
                print("%s NO CxTFSProjectDataCollection has been specified nor defined - a CxTFSProjectDataCollection MUST be defined - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.cxTFSServerEndpoint == None:

                print("");
                print("%s NO CxTFSServerEndpoint has been specified nor defined - a CxTFSServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.cxTFSServerEndpoint.getCxTFSServerEndpointActiveFlag() == False:

                print("");
                print("%s The supplied CxTFSServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.sCxTFSBase64UserAndPAT != None:

                self.sCxTFSBase64UserAndPAT = self.sCxTFSBase64UserAndPAT.strip();

            if self.sCxTFSBase64UserAndPAT == None or \
                len(self.sCxTFSBase64UserAndPAT) < 1:

                self.sCxTFSBase64UserAndPAT = self.cxTFSServerEndpoint.getBase64UserPAT();

            if self.sCxTFSBase64UserAndPAT != None:

                self.sCxTFSBase64UserAndPAT = self.sCxTFSBase64UserAndPAT.strip();

            if self.sCxTFSBase64UserAndPAT == None or \
                len(self.sCxTFSBase64UserAndPAT) < 1:

                self.cxTFSServerEndpoint.generateCxTFSProjectBase64Fields();

                self.sCxTFSBase64UserAndPAT = self.cxTFSServerEndpoint.getBase64UserPAT();

            if self.sCxTFSBase64UserAndPAT != None:

                self.sCxTFSBase64UserAndPAT = self.sCxTFSBase64UserAndPAT.strip();

            if self.sCxTFSBase64UserAndPAT == None or \
                len(self.sCxTFSBase64UserAndPAT) < 1:

                print("");
                print("%s NO CxTFS Base64 UserAndPAT has been specified nor generated - 1 MUST be defined - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.sCxTFSServerURL != None:

                self.sCxTFSServerURL = self.sCxTFSServerURL.strip();

            if self.sCxTFSServerURL == None or \
                len(self.sCxTFSServerURL) < 1:

                self.sCxTFSServerURL = self.cxTFSServerEndpoint.getCxTFSServerURL();

            if self.sCxTFSServerURL != None:

                self.sCxTFSServerURL = self.sCxTFSServerURL.strip();

            if self.sCxTFSServerURL == None or \
                len(self.sCxTFSServerURL) < 1:

                print("");
                print("%s NO CxTFS Server URL has been specified nor defined - 1 MUST be defined - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'validateCxTFSProjectRequiredFields()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def getCxTFSProjectsInitialDataViaRestAPI(self):

        bValidateReqFieldsOk = self.validateCxTFSProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxTFSProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            bGetCxTFSAllProjectsOk = self.getTFSProjectsDataForAllProjects();

            if bGetCxTFSAllProjectsOk == False:

                print("");
                print("%s Invocation of 'getTFSProjectsDataForAllProjects()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxTFSProjectDataCollection (after 'Get-ALL-Project(s)') is:" % (self.sClassDisp));
                print(self.cxTFSProjectDataCollection.toString());
                print("");

        except Exception as inst:

            print("%s 'getCxTFSProjectsInitialDataViaRestAPI()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def getTFSProjectsDataForAllProjects(self):

        bProcessingError = False;

        bValidateReqFieldsOk = self.validateCxTFSProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxTFSProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestVerb  = "GET";
        #   cxRequestURL   = ("%s/tfs/DefaultCollection/_apis/projects" % (self.sCxTFSServerURL));
            cxRequestURL = ("%s/tfs/%s/_apis/projects" % (self.sCxTFSServerURL, self.cxTFSProjectDataCollection.getCxTFSCollectionName()));
            cxReqHeaders   = {
                'Authorization':             ("Basic %s" % (self.sCxTFSBase64UserAndPAT)),
                'Accept-Encoding':           "gzip, deflate",
                'Accept':                    "application/json;api-version=4.1",
                'Connection':                "keep-alive",
                'Content-Type':              "application/json; charset=utf-8",
                'Cache-Control':             "no-cache",
                'cache-control':             "no-cache"
            #   'X-VSS-ForceMsaPassThrough': "true",
                };
            cxReqRespOk    = [200];

            sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));

            self.asCxTFSRestResponses.append("");
            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);

            cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);

            sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);
            #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));

            if cxReqResponse.status_code in cxReqRespOk:

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

                self.asCxTFSRestResponses.append(sOutputMsg);

                if self.bTraceFlag == True:

                    print(sOutputMsg);

            else:

                bProcessingError = True;

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

                self.asCxTFSRestResponses.append(sOutputMsg);

                print(sOutputMsg);

            jsonReqResponse = cxReqResponse.json();

            if jsonReqResponse != None:

                sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
                 
                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON Response {TFS Get-ALL-Projects} ===============");
                    print((type(sReqResponseRaw)));

                    print("");
                    print("=============== DIR JSON Response {TFS Get-ALL-Projects} ===============");
                    print((dir(sReqResponseRaw)));

                    print("");
                    print("=============== JSON 'string' Response {TFS Get-ALL-Projects} ===============");
                    print(sReqResponseRaw);

                if type(sReqResponseRaw) == str:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));

                else:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));

                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append("=============== JSON 'string' Response {TFS Get-ALL-Projects} ===============");
                self.asCxTFSRestResponses.append(sOutputMsg);
                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append(sReqResponseRaw);
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append("");

                dictCxReqResponseJson = json.loads(sReqResponseRaw);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON 'dictionary' Response {TFS Get-ALL-Projects} ===============");
                    print((type(dictCxReqResponseJson)));

                    print("");
                    print("=============== DIR JSON 'dictionary' Response {TFS Get-ALL-Projects} ===============");
                    print((dir(dictCxReqResponseJson)));

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-ALL-Projects} [RAW print] ===============");
                    print(dictCxReqResponseJson);

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-ALL-Projects} Enumerated ===============");

                # --------------------------------------------------------------------------------------------------
                # {
                #  "count": 1,
                #  "value": [
                #   {
                #    "id": "705ff45a-11cf-406d-8e04-823aff3b3ab6",
                #    "name": "TFSSampleProject1",
                #    "url": "http://192.168.2.190:9080/tfs/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6",
                #    "state": "wellFormed",
                #    "revision": 8,
                #    "visibility": "private"
                #   }
                #  ]
                # }
                # --------------------------------------------------------------------------------------------------

                if type(dictCxReqResponseJson) != dict:

                    print("");
                    print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                cDictJsonItem = 0;

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                        if type(dictCxReqResponseJsonItem) == dict:

                            dictSubItem  = dictCxReqResponseJsonItem;
                            cDictSubItem = 0;

                            for sDictItemKey in dictSubItem.keys():

                                cDictSubItem += 1;

                                objDictItemValue = dictSubItem[sDictItemKey];

                                print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));

                        else:

                            if type(dictCxReqResponseJsonItem) == list:

                                listSubItems = dictCxReqResponseJsonItem;
                                cListSubItem = 0;

                                for objListSubItem in listSubItems:

                                    cListSubItem += 1;

                                    print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));

                    if dictCxReqResponseJsonKey != "value":

                        continue;

                    listCxReqResponseJson = dictCxReqResponseJsonItem;
                 
                    if self.bTraceFlag == True:
                 
                        print("");
                        print("=============== TYPE JSON 'list' Response {TFS Get-ALL-Projects} ===============");
                        print((type(listCxReqResponseJson)));
                 
                        print("");
                        print("=============== DIR JSON 'list' Response {TFS Get-ALL-Projects} ===============");
                        print((dir(listCxReqResponseJson)));
                 
                        print("");
                        print("=============== JSON 'list' Response {TFS Get-ALL-Projects} [RAW print] ===============");
                        print(listCxReqResponseJson);
                 
                        print("");
                        print("=============== JSON 'list' Response {TFS Get-ALL-Projects} Enumerated ===============");
                 
                    cListDictItem = 0;
                 
                    for dictCxReqResponseListItem in listCxReqResponseJson:
                 
                        if dictCxReqResponseListItem == None:
                 
                            continue;
                 
                        cListDictItem += 1;
                 
                        if self.bTraceFlag == True:
                 
                            print(("  List Item #(%d): <raw> {%s} [%s]..." % (cListDictItem, type(dictCxReqResponseListItem), dictCxReqResponseListItem)));
                 
                        cxTFSProjectData = CxTFSProjectData1.CxTFSProjectData(trace=self.bTraceFlag);

                        bCxTFSProjectDataPopulatedOk = cxTFSProjectData.populateCxTFSProjectDataFromJsonDictionary(dictcxtfsprojectdata=dictCxReqResponseListItem);

                        if bCxTFSProjectDataPopulatedOk == True:

                            self.cxTFSProjectDataCollection.addCxTFSProjectDataToCxTFSProjectDataCollection(cxtfsprojectdata=cxTFSProjectData);

        except Exception as inst:

            print("%s 'getTFSProjectsDataForAllProjects()' - exception occured..." % (self.sClassDisp));
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

    def getCxTFSProjectDetailsDataViaRestAPI(self, cxtfsprojectdata=None):

    #   self.bTraceFlag = True;

        cxTFSProjectData = cxtfsprojectdata;

        if cxTFSProjectData == None:

            print("");
            print("%s NO CxTFSProjectData has been specified nor defined for this request - one CxTFSProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bValidateReqFieldsOk = self.validateCxTFSProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxTFSProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            bGetCxTFSProjectDetailsOk = self.getTFSProjectDetailsDataForProject(cxtfsprojectdata=cxTFSProjectData);

            if bGetCxTFSProjectDetailsOk == False:

                print("");
                print("%s Invocation of 'getTFSProjectDetailsDataForProject()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxTFSProjectData (after 'Get-Unique-Project-Details(s)') is:" % (self.sClassDisp));
                print(cxTFSProjectData.toString());
                print("");

            bGetCxTFSProjectCollectionOk = self.getTFSProjectCollectionDataForProject(cxtfsprojectdata=cxTFSProjectData);

            if bGetCxTFSProjectCollectionOk == False:

                print("");
                print("%s Invocation of 'getTFSProjectCollectionDataForProject()' failed - Warning!" % (self.sClassDisp));
                print("");

            #   return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxTFSProjectData (after 'Get-Unique-Project-Collection') is:" % (self.sClassDisp));
                print(cxTFSProjectData.toString());
                print("");

            bGetCxTFSProjectTeamOk = self.getTFSProjectTeamDataForProject(cxtfsprojectdata=cxTFSProjectData);

            if bGetCxTFSProjectTeamOk == False:

                print("");
                print("%s Invocation of 'getTFSProjectTeamDataForProject()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxTFSProjectData (after 'Get-Unique-Project-Team') is:" % (self.sClassDisp));
                print(cxTFSProjectData.toString());
                print("");

            bGetCxTFSProjectTeamIdentityOk = self.getTFSProjectTeamIdentityDataForProject(cxtfsprojectdata=cxTFSProjectData);

            if bGetCxTFSProjectTeamIdentityOk == False:

                print("");
                print("%s Invocation of 'getTFSProjectTeamIdentityDataForProject()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxTFSProjectData (after 'Get-Unique-Project-Team-Identity') is:" % (self.sClassDisp));
                print(cxTFSProjectData.toString());
                print("");

            bGetCxTFSProjectReposOk = self.getTFSProjectReposDataForProject(cxtfsprojectdata=cxTFSProjectData);

            if bGetCxTFSProjectReposOk == False:

                print("");
                print("%s Invocation of 'getTFSProjectReposDataForProject()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxTFSProjectData (after 'Get-Unique-Project-(Git)-Repo(s)') is:" % (self.sClassDisp));
                print(cxTFSProjectData.toString());
                print("");

        except Exception as inst:

            print("%s 'getCxTFSProjectsInitialDataViaRestAPI()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def getTFSProjectDetailsDataForProject(self, cxtfsprojectdata=None):

        cxTFSProjectData = cxtfsprojectdata;

        if cxTFSProjectData == None:

            print("");
            print("%s NO CxTFSProjectData has been specified nor defined for this request - one CxTFSProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bValidateReqFieldsOk = self.validateCxTFSProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxTFSProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestVerb  = "GET";
            cxRequestURL   = cxTFSProjectData.getCxProjectDetailsURL();
            cxReqHeaders   = {
                'Authorization':             ("Basic %s" % (self.sCxTFSBase64UserAndPAT)),
                'Accept-Encoding':           "gzip, deflate",
                'Accept':                    "application/json;api-version=4.1",
                'Connection':                "keep-alive",
                'Content-Type':              "application/json; charset=utf-8",
                'Cache-Control':             "no-cache",
                'cache-control':             "no-cache"
            #   'X-VSS-ForceMsaPassThrough': "true",
                };
            cxReqRespOk    = [200];

            sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));

            self.asCxTFSRestResponses.append("");
            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);

            cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);

            sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);
            #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));

            if cxReqResponse.status_code in cxReqRespOk:

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

                self.asCxTFSRestResponses.append(sOutputMsg);

                if self.bTraceFlag == True:

                    print(sOutputMsg);

            else:

                bProcessingError = True;

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

                self.asCxTFSRestResponses.append(sOutputMsg);

                print(sOutputMsg);

            jsonReqResponse = cxReqResponse.json();

            if jsonReqResponse != None:

                sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON Response {TFS Get-Unique-Project-Details} ===============");
                    print((type(sReqResponseRaw)));

                    print("");
                    print("=============== DIR JSON Response {TFS Get-Unique-Project-Details} ===============");
                    print((dir(sReqResponseRaw)));

                    print("");
                    print("=============== JSON 'string' Response {TFS Get-Unique-Project-Details} ===============");
                    print(sReqResponseRaw);

                if type(sReqResponseRaw) == str:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));

                else:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));

                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append("=============== JSON 'string' Response {TFS Get-Unique-Project-Details} ===============");
                self.asCxTFSRestResponses.append(sOutputMsg);
                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append(sReqResponseRaw);
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append("");

                dictCxReqResponseJson = json.loads(sReqResponseRaw);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON 'dictionary' Response {TFS Get-Unique-Project-Details} ===============");
                    print((type(dictCxReqResponseJson)));

                    print("");
                    print("=============== DIR JSON 'dictionary' Response {TFS Get-Unique-Project-Details} ===============");
                    print((dir(dictCxReqResponseJson)));

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Details} [RAW print] ===============");
                    print(dictCxReqResponseJson);

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Details} Enumerated ===============");

                # --------------------------------------------------------------------------------------------------
                # {
                #  "id": "705ff45a-11cf-406d-8e04-823aff3b3ab6",
                #  "name": "TFSSampleProject1",
                #  "url": "http://192.168.2.190:9080/tfs/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6",
                #  "state": "wellFormed",
                #  "revision": 8,
                #  "_links": {
                #   "self": {
                #    "href": "http://192.168.2.190:9080/tfs/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6"
                #   },
                #   "collection": {
                #    "href": "http://192.168.2.190:9080/tfs/_apis/projectCollections/1ea0178e-6700-4742-9ff8-a4f77af995bf"
                #   },
                #   "web": {
                #    "href": "http://darylc-laptop:9080/tfs/DefaultCollection/TFSSampleProject1"
                #   }
                #  },
                #  "visibility": "private",
                #  "defaultTeam": {
                #    "id": "ec3de804-b8b2-463f-a963-27453ce09273",
                #    "name": "TFSSampleProject1 Team",
                #    "url": "http://192.168.2.190:9080/tfs/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6/teams/ec3de804-b8b2-463f-a963-27453ce09273"
                #  }
                # }
                # --------------------------------------------------------------------------------------------------

                if type(dictCxReqResponseJson) != dict:

                    print("");
                    print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                cDictJsonItem = 0;

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                        if type(dictCxReqResponseJsonItem) == dict:

                            dictSubItem  = dictCxReqResponseJsonItem;
                            cDictSubItem = 0;

                            for sDictItemKey in dictSubItem.keys():

                                cDictSubItem += 1;

                                objDictItemValue = dictSubItem[sDictItemKey];

                                print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));

                        else:

                            if type(dictCxReqResponseJsonItem) == list:

                                listSubItems = dictCxReqResponseJsonItem;
                                cListSubItem = 0;

                                for objListSubItem in listSubItems:

                                    cListSubItem += 1;

                                    print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));

                    if dictCxReqResponseJsonKey != "_links" and \
                       dictCxReqResponseJsonKey != "defaultTeam":

                        continue;

                    dictCxReqResponseDetails = dictCxReqResponseJsonItem;

                    if self.bTraceFlag == True:

                        print("");
                        print("=============== TYPE JSON 'dict' Response {TFS Get-Unique-Project-Details} ===============");
                        print((type(dictCxReqResponseDetails)));

                        print("");
                        print("=============== DIR JSON 'dict' Response {TFS Get-Unique-Project-Details} ===============");
                        print((dir(dictCxReqResponseDetails)));

                        print("");
                        print("=============== JSON 'dict' Response {TFS Get-Unique-Project-Details} [RAW print] ===============");
                        print(dictCxReqResponseDetails);

                        print("");
                        print("=============== JSON 'dict' Response {TFS Get-Unique-Project-Details} Enumerated ===============");

                    if dictCxReqResponseJsonKey != "_links":

                        cxTFSProjectData.setCxProjectLinks(cxprojectlinks=dictCxReqResponseDetails);

                    if dictCxReqResponseJsonKey != "defaultTeam":

                        cxTFSProjectData.setCxProjectDefaultTeam(cxprojectdefaultteam=dictCxReqResponseDetails);

                    cDictItemDetails = 0;

                    for dictCxReqResponseDetailsItem in dictCxReqResponseDetails:

                        if dictCxReqResponseDetailsItem == None:

                            continue;

                        cDictItemDetails += 1;

                        if self.bTraceFlag == True:

                            print(("  Dict Item #(%d): <raw> {%s} [%s]..." % (cDictItemDetails, type(dictCxReqResponseDetailsItem), dictCxReqResponseDetailsItem)));

                        if dictCxReqResponseJsonKey == "_links":

                            if dictCxReqResponseDetailsItem == "collection":

                                dictProjDetailsCollection = dictCxReqResponseDetails["collection"];

                                cxTFSProjectData.setCxProjectCollectionURL(cxprojectcollectionurl=dictProjDetailsCollection["href"]);

                        if dictCxReqResponseJsonKey == "defaultTeam":

                            if dictCxReqResponseDetailsItem == "id":

                                sProjDefaultTeamId = dictCxReqResponseDetails["id"];

                                cxTFSProjectData.setCxProjectTeamId(cxprojectteamid=sProjDefaultTeamId);

                            if dictCxReqResponseDetailsItem == "name":

                                sProjDefaultTeamName = dictCxReqResponseDetails["name"];

                                cxTFSProjectData.setCxProjectTeamName(cxprojectteamname=sProjDefaultTeamName);

                            if dictCxReqResponseDetailsItem == "url":

                                sProjDefaultTeamURL = dictCxReqResponseDetails["url"];

                                cxTFSProjectData.setCxProjectTeamURL(cxprojectteamurl=sProjDefaultTeamURL);

        except Exception as inst:

            print("%s 'getTFSProjectDetailsDataForProject()' - exception occured..." % (self.sClassDisp));
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

    def getTFSProjectCollectionDataForProject(self, cxtfsprojectdata=None):

        cxTFSProjectData = cxtfsprojectdata;

        if cxTFSProjectData == None:

            print("");
            print("%s NO CxTFSProjectData has been specified nor defined for this request - one CxTFSProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bValidateReqFieldsOk = self.validateCxTFSProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxTFSProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestVerb  = "GET";
            cxRequestURL   = cxTFSProjectData.getCxProjectCollectionURL();
            cxReqHeaders   = {
                'Authorization':             ("Basic %s" % (self.sCxTFSBase64UserAndPAT)),
                'Accept-Encoding':           "gzip, deflate",
                'Accept':                    "application/json;api-version=4.1",
                'Connection':                "keep-alive",
                'Content-Type':              "application/json; charset=utf-8",
                'Cache-Control':             "no-cache",
                'cache-control':             "no-cache"
            #   'X-VSS-ForceMsaPassThrough': "true",
                };
            cxReqRespOk    = [200];

            sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));

            self.asCxTFSRestResponses.append("");
            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);

            cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);

            sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);
            #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));

            if cxReqResponse.status_code in cxReqRespOk:

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

                self.asCxTFSRestResponses.append(sOutputMsg);

                if self.bTraceFlag == True:

                    print(sOutputMsg);

            else:

                bProcessingError = True;

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

                self.asCxTFSRestResponses.append(sOutputMsg);

                print(sOutputMsg);

            jsonReqResponse = cxReqResponse.json();

            if jsonReqResponse != None:

                sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON Response {TFS Get-Unique-Project-Collection} ===============");
                    print((type(sReqResponseRaw)));

                    print("");
                    print("=============== DIR JSON Response {TFS Get-Unique-Project-Collection} ===============");
                    print((dir(sReqResponseRaw)));

                    print("");
                    print("=============== JSON 'string' Response {TFS Get-Unique-Project-Collection} ===============");
                    print(sReqResponseRaw);

                if type(sReqResponseRaw) == str:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));

                else:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));

                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append("=============== JSON 'string' Response {TFS Get-Unique-Project-Collection} ===============");
                self.asCxTFSRestResponses.append(sOutputMsg);
                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append(sReqResponseRaw);
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append("");

                dictCxReqResponseJson = json.loads(sReqResponseRaw);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON 'dictionary' Response {TFS Get-Unique-Project-Collection} ===============");
                    print((type(dictCxReqResponseJson)));

                    print("");
                    print("=============== DIR JSON 'dictionary' Response {TFS Get-Unique-Project-Collection} ===============");
                    print((dir(dictCxReqResponseJson)));

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Collection} [RAW print] ===============");
                    print(dictCxReqResponseJson);

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Collection} Enumerated ===============");

                # --------------------------------------------------------------------------------------------------
                # {
                #  "id": "1ea0178e-6700-4742-9ff8-a4f77af995bf",
                #  "name": "DefaultCollection",
                #  "url": "http://192.168.2.190:9080/tfs/_apis/projectCollections/1ea0178e-6700-4742-9ff8-a4f77af995bf",
                #  "state": "Started",
                #  "_links": {
                #   "self": {
                #    "href": "http://192.168.2.190:9080/tfs/_apis/projectCollections/1ea0178e-6700-4742-9ff8-a4f77af995bf"
                #   },
                #   "web": {
                #    "href": "http://darylc-laptop:9080/tfs/DefaultCollection/"
                #   }
                #  }
                # }
                # --------------------------------------------------------------------------------------------------

                if type(dictCxReqResponseJson) != dict:

                    print("");
                    print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                cxTFSProjectData.setCxProjectCollection(cxprojectcollection=dictCxReqResponseJson);

                cDictJsonItem = 0;

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                        if type(dictCxReqResponseJsonItem) == dict:

                            dictSubItem  = dictCxReqResponseJsonItem;
                            cDictSubItem = 0;

                            for sDictItemKey in dictSubItem.keys():

                                cDictSubItem += 1;

                                objDictItemValue = dictSubItem[sDictItemKey];

                                print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));

                        else:

                            if type(dictCxReqResponseJsonItem) == list:

                                listSubItems = dictCxReqResponseJsonItem;
                                cListSubItem = 0;

                                for objListSubItem in listSubItems:

                                    cListSubItem += 1;

                                    print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));

        except Exception as inst:

            print("%s 'getTFSProjectCollectionDataForProject()' - exception occured..." % (self.sClassDisp));
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

    def getTFSProjectTeamDataForProject(self, cxtfsprojectdata=None):

        cxTFSProjectData = cxtfsprojectdata;

        if cxTFSProjectData == None:

            print("");
            print("%s NO CxTFSProjectData has been specified nor defined for this request - one CxTFSProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bValidateReqFieldsOk = self.validateCxTFSProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxTFSProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestVerb  = "GET";
            cxRequestURL   = cxTFSProjectData.getCxProjectTeamURL();
            cxReqHeaders   = {
                'Authorization':             ("Basic %s" % (self.sCxTFSBase64UserAndPAT)),
                'Accept-Encoding':           "gzip, deflate",
                'Accept':                    "application/json;api-version=4.1",
                'Connection':                "keep-alive",
                'Content-Type':              "application/json; charset=utf-8",
                'Cache-Control':             "no-cache",
                'cache-control':             "no-cache"
            #   'X-VSS-ForceMsaPassThrough': "true",
                };
            cxReqRespOk    = [200];

            sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));

            self.asCxTFSRestResponses.append("");
            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);

            cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);

            sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);
            #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));

            if cxReqResponse.status_code in cxReqRespOk:

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

                self.asCxTFSRestResponses.append(sOutputMsg);

                if self.bTraceFlag == True:

                    print(sOutputMsg);

            else:

                bProcessingError = True;

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

                self.asCxTFSRestResponses.append(sOutputMsg);

                print(sOutputMsg);

            jsonReqResponse = cxReqResponse.json();

            if jsonReqResponse != None:

                sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON Response {TFS Get-Unique-Project-Team} ===============");
                    print((type(sReqResponseRaw)));

                    print("");
                    print("=============== DIR JSON Response {TFS Get-Unique-Project-Team} ===============");
                    print((dir(sReqResponseRaw)));

                    print("");
                    print("=============== JSON 'string' Response {TFS Get-Unique-Project-Team} ===============");
                    print(sReqResponseRaw);

                if type(sReqResponseRaw) == str:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));

                else:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));

                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append("=============== JSON 'string' Response {TFS Get-Unique-Project-Team} ===============");
                self.asCxTFSRestResponses.append(sOutputMsg);
                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append(sReqResponseRaw);
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append("");

                dictCxReqResponseJson = json.loads(sReqResponseRaw);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON 'dictionary' Response {TFS Get-Unique-Project-Team} ===============");
                    print((type(dictCxReqResponseJson)));

                    print("");
                    print("=============== DIR JSON 'dictionary' Response {TFS Get-Unique-Project-Team} ===============");
                    print((dir(dictCxReqResponseJson)));

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Team} [RAW print] ===============");
                    print(dictCxReqResponseJson);

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Team} Enumerated ===============");

                # --------------------------------------------------------------------------------------------------
                # {
                #  "id": "ec3de804-b8b2-463f-a963-27453ce09273",
                #  "name": "TFSSampleProject1 Team",
                #  "url": "http://192.168.2.190:9080/tfs/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6/teams/ec3de804-b8b2-463f-a963-27453ce09273",
                #  "description": "The default project team.",
                #  "identityUrl": "http://192.168.2.190:9080/tfs/DefaultCollection/_apis/Identities/ec3de804-b8b2-463f-a963-27453ce09273",
                #  "projectName": "TFSSampleProject1",
                #  "projectId": "705ff45a-11cf-406d-8e04-823aff3b3ab6"
                # }
                # --------------------------------------------------------------------------------------------------

                if type(dictCxReqResponseJson) != dict:

                    print("");
                    print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                cxTFSProjectData.setCxProjectTeam(cxprojectteam=dictCxReqResponseJson);

                cDictJsonItem = 0;

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                        if type(dictCxReqResponseJsonItem) == dict:

                            dictSubItem  = dictCxReqResponseJsonItem;
                            cDictSubItem = 0;

                            for sDictItemKey in dictSubItem.keys():

                                cDictSubItem += 1;

                                objDictItemValue = dictSubItem[sDictItemKey];

                                print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));

                        else:

                            if type(dictCxReqResponseJsonItem) == list:

                                listSubItems = dictCxReqResponseJsonItem;
                                cListSubItem = 0;

                                for objListSubItem in listSubItems:

                                    cListSubItem += 1;

                                    print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));

                    if dictCxReqResponseJsonKey == "description":

                        cxTFSProjectData.setCxProjectTeamDescription(cxprojectteamdescription=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "identityUrl":

                        cxTFSProjectData.setCxProjectTeamIdentityURL(cxprojectteamidentityurl=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "projectName":

                        cxTFSProjectData.setCxProjectTeamProjectName(cxprojectteamprojectname=dictCxReqResponseJsonItem);

                    if dictCxReqResponseJsonKey == "projectId":

                        cxTFSProjectData.setCxProjectTeamProjectId(cxprojectteamprojectid=dictCxReqResponseJsonItem);

        except Exception as inst:

            print("%s 'getTFSProjectTeamDataForProject()' - exception occured..." % (self.sClassDisp));
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

    def getTFSProjectTeamIdentityDataForProject(self, cxtfsprojectdata=None):

        cxTFSProjectData = cxtfsprojectdata;

        if cxTFSProjectData == None:

            print("");
            print("%s NO CxTFSProjectData has been specified nor defined for this request - one CxTFSProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bValidateReqFieldsOk = self.validateCxTFSProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxTFSProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestVerb  = "GET";
            cxRequestURL   = cxTFSProjectData.getCxProjectTeamIdentityURL();
            cxReqHeaders   = {
                'Authorization':             ("Basic %s" % (self.sCxTFSBase64UserAndPAT)),
                'Accept-Encoding':           "gzip, deflate",
                'Accept':                    "application/json;api-version=4.1",
                'Connection':                "keep-alive",
                'Content-Type':              "application/json; charset=utf-8",
                'Cache-Control':             "no-cache",
                'cache-control':             "no-cache"
            #   'X-VSS-ForceMsaPassThrough': "true",
                };
            cxReqRespOk    = [200];

            sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));

            self.asCxTFSRestResponses.append("");
            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);

            cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);

            sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);
            #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));

            if cxReqResponse.status_code in cxReqRespOk:

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

                self.asCxTFSRestResponses.append(sOutputMsg);

                if self.bTraceFlag == True:

                    print(sOutputMsg);

            else:

                bProcessingError = True;

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

                self.asCxTFSRestResponses.append(sOutputMsg);

                print(sOutputMsg);

            jsonReqResponse = cxReqResponse.json();

            if jsonReqResponse != None:

                sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON Response {TFS Get-Unique-Project-Team-Identity} ===============");
                    print((type(sReqResponseRaw)));

                    print("");
                    print("=============== DIR JSON Response {TFS Get-Unique-Project-Team-Identity} ===============");
                    print((dir(sReqResponseRaw)));

                    print("");
                    print("=============== JSON 'string' Response {TFS Get-Unique-Project-Team-Identity} ===============");
                    print(sReqResponseRaw);

                if type(sReqResponseRaw) == str:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));

                else:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));

                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append("=============== JSON 'string' Response {TFS Get-Unique-Project-Team-Identity} ===============");
                self.asCxTFSRestResponses.append(sOutputMsg);
                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append(sReqResponseRaw);
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append("");

                dictCxReqResponseJson = json.loads(sReqResponseRaw);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON 'dictionary' Response {TFS Get-Unique-Project-Team-Identity} ===============");
                    print((type(dictCxReqResponseJson)));

                    print("");
                    print("=============== DIR JSON 'dictionary' Response {TFS Get-Unique-Project-Team-Identity} ===============");
                    print((dir(dictCxReqResponseJson)));

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Team-Identity} [RAW print] ===============");
                    print(dictCxReqResponseJson);

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Team-Identity} Enumerated ===============");

                # --------------------------------------------------------------------------------------------------
                # {
                #     "id": "ec3de804-b8b2-463f-a963-27453ce09273",
                #     "descriptor": "Microsoft.TeamFoundation.Identity;S-1-9-1551374245-4263824929-2983495753-2170576692-487292674-1-192998105-199977285-2515143924-823569469",
                #     "providerDisplayName": "[TFSSampleProject1]\\TFSSampleProject1 Team",
                #     "isActive": true,
                #     "isContainer": true,
                #     "members": [],
                #     "memberOf": [],
                #     "memberIds": [],
                #     "masterId": "ffffffff-ffff-ffff-ffff-ffffffffffff",
                #     "properties": {
                #         "SchemaClassName": {
                #             "$type": "System.String",
                #             "$value": "Group"
                #         },
                #         "Description": {
                #             "$type": "System.String",
                #             "$value": "The default project team."
                #         },
                #         "Domain": {
                #             "$type": "System.String",
                #             "$value": "vstfs:///Classification/TeamProject/705ff45a-11cf-406d-8e04-823aff3b3ab6"
                #         },
                #         "Account": {
                #             "$type": "System.String",
                #             "$value": "TFSSampleProject1 Team"
                #         },
                #         "SecurityGroup": {
                #             "$type": "System.String",
                #             "$value": "SecurityGroup"
                #         },
                #         "SpecialType": {
                #             "$type": "System.String",
                #             "$value": "Generic"
                #         },
                #         "ScopeId": {
                #             "$type": "System.Guid",
                #             "$value": "21ce24fe-d4b1-4988-8160-5f341d0b7f02"
                #         },
                #         "ScopeType": {
                #             "$type": "System.String",
                #             "$value": "TeamProject"
                #         },
                #         "LocalScopeId": {
                #             "$type": "System.Guid",
                #             "$value": "705ff45a-11cf-406d-8e04-823aff3b3ab6"
                #         },
                #         "SecuringHostId": {
                #             "$type": "System.Guid",
                #             "$value": "1ea0178e-6700-4742-9ff8-a4f77af995bf"
                #         },
                #         "ScopeName": {
                #             "$type": "System.String",
                #             "$value": "TFSSampleProject1"
                #         },
                #         "VirtualPlugin": {
                #             "$type": "System.String",
                #             "$value": ""
                #         }
                #     },
                #     "resourceVersion": 2,
                #     "metaTypeId": 255
                # }
                # --------------------------------------------------------------------------------------------------

                if type(dictCxReqResponseJson) != dict:

                    print("");
                    print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                cxTFSProjectData.setCxProjectTeamIdentity(cxprojectteamidentity=dictCxReqResponseJson);

                cDictJsonItem = 0;

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                        if type(dictCxReqResponseJsonItem) == dict:

                            dictSubItem  = dictCxReqResponseJsonItem;
                            cDictSubItem = 0;

                            for sDictItemKey in dictSubItem.keys():

                                cDictSubItem += 1;

                                objDictItemValue = dictSubItem[sDictItemKey];

                                print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));

                        else:

                            if type(dictCxReqResponseJsonItem) == list:

                                listSubItems = dictCxReqResponseJsonItem;
                                cListSubItem = 0;

                                for objListSubItem in listSubItems:

                                    cListSubItem += 1;

                                    print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));

        except Exception as inst:

            print("%s 'getTFSProjectTeamIdentityDataForProject()' - exception occured..." % (self.sClassDisp));
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

    def getTFSProjectReposDataForProject(self, cxtfsprojectdata=None):

        cxTFSProjectData = cxtfsprojectdata;

        if cxTFSProjectData == None:

            print("");
            print("%s NO CxTFSProjectData has been specified nor defined for this request - one CxTFSProjectData MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        bValidateReqFieldsOk = self.validateCxTFSProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxTFSProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestVerb  = "GET";
            cxRequestURL = ("%s/tfs/%s/%s/_apis/git/repositories?api-version=1" % (self.sCxTFSServerURL, self.cxTFSProjectDataCollection.getCxTFSCollectionName(), cxTFSProjectData.getCxProjectName()));
            cxReqHeaders   = {
                'Authorization':             ("Basic %s" % (self.sCxTFSBase64UserAndPAT)),
                'Accept-Encoding':           "gzip, deflate",
                'Accept':                    "application/json;api-version=1",
                'Connection':                "keep-alive",
                'Content-Type':              "application/json; charset=utf-8",
                'Cache-Control':             "no-cache",
                'cache-control':             "no-cache"
            #   'X-VSS-ForceMsaPassThrough': "true",
                };
            cxReqRespOk    = [200];

            sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));

            self.asCxTFSRestResponses.append("");
            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);

            cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);

            sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            self.asCxTFSRestResponses.append(sOutputMsg);

            if self.bTraceFlag == True:

                print(sOutputMsg);
            #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));

            if cxReqResponse.status_code in cxReqRespOk:

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

                self.asCxTFSRestResponses.append(sOutputMsg);

                if self.bTraceFlag == True:

                    print(sOutputMsg);

            else:

                bProcessingError = True;

                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

                self.asCxTFSRestResponses.append(sOutputMsg);

                print(sOutputMsg);

            jsonReqResponse = cxReqResponse.json();

            if jsonReqResponse != None:

                sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
                 
                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON Response {TFS Get-Unique-Project-Repos} ===============");
                    print((type(sReqResponseRaw)));

                    print("");
                    print("=============== DIR JSON Response {TFS Get-Unique-Project-Repos} ===============");
                    print((dir(sReqResponseRaw)));

                    print("");
                    print("=============== JSON 'string' Response {TFS Get-Unique-Project-Repos} ===============");
                    print(sReqResponseRaw);

                if type(sReqResponseRaw) == str:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));

                else:

                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));

                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append("=============== JSON 'string' Response {TFS Get-Unique-Project-Repos} ===============");
                self.asCxTFSRestResponses.append(sOutputMsg);
                self.asCxTFSRestResponses.append("");
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append(sReqResponseRaw);
                self.asCxTFSRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxTFSRestResponses.append("");

                dictCxReqResponseJson = json.loads(sReqResponseRaw);

                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON 'dictionary' Response {TFS Get-Unique-Project-Repos} ===============");
                    print((type(dictCxReqResponseJson)));

                    print("");
                    print("=============== DIR JSON 'dictionary' Response {TFS Get-Unique-Project-Repos} ===============");
                    print((dir(dictCxReqResponseJson)));

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Repos} [RAW print] ===============");
                    print(dictCxReqResponseJson);

                    print("");
                    print("=============== JSON 'dictionary' Response {TFS Get-Unique-Project-Repos} Enumerated ===============");

                # --------------------------------------------------------------------------------------------------
                # {
                #     "value": [
                #         {
                #             "id": "6f23a004-735a-4df6-909b-17571d9f06b1",
                #             "name": "JWS_App-Project_1",
                #             "url": "http://192.168.2.190:9080/tfs/JWebsoftwareDev/_apis/git/repositories/6f23a004-735a-4df6-909b-17571d9f06b1",
                #             "project": {
                #                 "id": "dc408339-e04f-4582-9b50-65e9182fcb3a",
                #                 "name": "JWS_App-Project_1",
                #                 "description": "JWS_App-Project_1 description",
                #                 "url": "http://192.168.2.190:9080/tfs/JWebsoftwareDev/_apis/projects/dc408339-e04f-4582-9b50-65e9182fcb3a",
                #                 "state": "wellFormed",
                #                 "revision": 9,
                #                 "visibility": "private"
                #             },
                #             "defaultBranch": "refs/heads/master",
                #             "remoteUrl": "http://darylc-laptop:9080/tfs/JWebsoftwareDev/_git/JWS_App-Project_1",
                #             "sshUrl": "ssh://darylc-laptop:22/tfs/JWebsoftwareDev/_git/JWS_App-Project_1"
                #         }
                #     ],
                #     "count": 1
                # }
                # --------------------------------------------------------------------------------------------------

                if type(dictCxReqResponseJson) != dict:

                    print("");
                    print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                cDictJsonItem = 0;

                for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                    if dictCxReqResponseJsonKey == None:

                        continue;

                    cDictJsonItem += 1;

                    dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                    if self.bTraceFlag == True:

                        print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                        if type(dictCxReqResponseJsonItem) == dict:

                            dictSubItem  = dictCxReqResponseJsonItem;
                            cDictSubItem = 0;

                            for sDictItemKey in dictSubItem.keys():

                                cDictSubItem += 1;

                                objDictItemValue = dictSubItem[sDictItemKey];

                                print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));

                        else:

                            if type(dictCxReqResponseJsonItem) == list:

                                listSubItems = dictCxReqResponseJsonItem;
                                cListSubItem = 0;

                                for objListSubItem in listSubItems:

                                    cListSubItem += 1;

                                    print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));

                    if dictCxReqResponseJsonKey != "value":

                        continue;

                    listCxReqResponseJson = dictCxReqResponseJsonItem;
                 
                    if self.bTraceFlag == True:
                 
                        print("");
                        print("=============== TYPE JSON 'list' Response {TFS Get-Unique-Project-Repos} ===============");
                        print((type(listCxReqResponseJson)));
                 
                        print("");
                        print("=============== DIR JSON 'list' Response {TFS Get-Unique-Project-Repos} ===============");
                        print((dir(listCxReqResponseJson)));
                 
                        print("");
                        print("=============== JSON 'list' Response {TFS Get-Unique-Project-Repos} [RAW print] ===============");
                        print(listCxReqResponseJson);
                 
                        print("");
                        print("=============== JSON 'list' Response {TFS Get-Unique-Project-Repos} Enumerated ===============");

                    cxTFSProjectData.setCxProjectRepos(cxprojectrepos=listCxReqResponseJson);
                 
                    cListDictItem = 0;
                 
                    for dictCxReqResponseListItem in listCxReqResponseJson:
                 
                        if dictCxReqResponseListItem == None:
                 
                            continue;
                 
                        cListDictItem += 1;
                 
                        if self.bTraceFlag == True:
                 
                            print(("  List Item #(%d): <raw> {%s} [%s]..." % (cListDictItem, type(dictCxReqResponseListItem), dictCxReqResponseListItem)));
                 
        except Exception as inst:

            print("%s 'getTFSProjectReposDataForProject()' - exception occured..." % (self.sClassDisp));
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

