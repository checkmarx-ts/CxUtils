
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
from requests_toolbelt import MultipartEncoder;

# port CxProjectCreationCollectionDefaults1;
import CxRestAPITokenAuthenticationBase1;
import CxRestAPIStatistics1;
import CxProjectCreation1;
import CxProjectData1;
import CxServerEndpoint1;

class CxRestAPIProjectCreationBase:

    sClassMod                   = __name__;
    sClassId                    = "CxRestAPIProjectCreationBase";
    sClassVers                  = "(v1.0563)";
    sClassDisp                  = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                  = False;
    cxServerEndpoint            = None;
    cxProjectCreationCollection = None;

    # Constructed objects:

    cxRestAPITokenAuth          = None;

    def __init__(self, trace=False, cxserverendpoint=None, cxprojectcreationcollection=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxServerEndpoint(cxserverendpoint=cxserverendpoint);
            self.setCxProjectCreationCollection(cxprojectcreationcollection=cxprojectcreationcollection);

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

    def getCxProjectCreationCollection(self):

        return self.cxProjectCreationCollection;

    def setCxProjectCreationCollection(self, cxprojectcreationcollection=None):

        self.cxProjectCreationCollection = cxprojectcreationcollection;

    def resetCxRestAPIProjectCreationBase(self):

        return;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'cxServerEndpoint' is [%s]..." % (self.sClassDisp, self.cxServerEndpoint));
            print("%s The contents of 'cxProjectCreationCollection' is [%s]..." % (self.sClassDisp, self.cxProjectCreationCollection));
            print("%s The contents of 'cxRestAPITokenAuth' is [%s]..." % (self.sClassDisp, self.cxRestAPITokenAuth));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'cxServerEndpoint' is [%s], " % (self.cxServerEndpoint));
        asObjDetail.append("'cxProjectCreationCollection' is [%s], " % (self.cxProjectCreationCollection));
        asObjDetail.append("'cxRestAPITokenAuth' is [%s]. " % (self.cxRestAPITokenAuth));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def getCxRestAPIProjectCreationMetaData(self):

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

        if self.cxProjectCreationCollection == None:

            print("");
            print("%s NO CxProjectCreationCollection has been specified nor defined - a CxProjectCreationCollection MUST be defined - Error!" % (self.sClassDisp));
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
                print("%s CxProjectCreationCollection (after 1st 'meta' data) is:" % (self.sClassDisp));
                print(self.cxProjectCreationCollection.toString());
                print("");
         
            bGetCxAllPresets = self.getCxRestAPIAllPresets();

            if bGetCxAllPresets == False:

                print("");
                print("%s Invocation of 'getCxRestAPIAllPresets()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxProjectCreationCollection (after 2nd 'meta' data) is:" % (self.sClassDisp));
                print(self.cxProjectCreationCollection.toString());
                print("");

            bGetCxAllEngineConfigurations = self.getCxRestAPIAllEngineConfigurations();

            if bGetCxAllEngineConfigurations == False:

                print("");
                print("%s Invocation of 'getCxRestAPIAllEngineConfigurations()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxProjectCreationCollection (after 3rd 'meta' data) is:" % (self.sClassDisp));
                print(self.cxProjectCreationCollection.toString());
                print("");

            bGetCxAllProjectDataOk = self.getCxRestAPIAllProjectData();

            if bGetCxAllProjectDataOk == False:

                print("");
                print("%s Invocation of 'getCxRestAPIAllProjectData()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'getCxRestAPIProjectCreationMetaData()' - exception occured..." % (self.sClassDisp));
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

                self.cxProjectCreationCollection.addCxProjectMetaDataAllTeams(cxteamfullname=sCxTeamFullName, cxteamid=sCxTeamId);

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

                self.cxProjectCreationCollection.addCxProjectMetaDataAllPresets(cxpresetname=sCxPresetName, cxpresetdict=dictCxPreset);

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

                self.cxProjectCreationCollection.addCxProjectMetaDataAllEngineConfigurations(cxengineconfigname=sCxEngineConfigName, cxengineconfigid=sCxEngineConfigId);

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

    def getCxRestAPIAllProjectData(self):

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

                self.cxProjectCreationCollection.addCxProjectMetaDataAllProjects(cxprojectdata=cxProjectData);

        except Exception as inst:

            print("%s 'getCxRestAPIAllProjectData()' - exception occured..." % (self.sClassDisp));
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

    def createCxRestAPIProjectAndBranches(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined - a CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxProjectCreationCollection == None:

            print("");
            print("%s NO CxProjectCreationCollection has been specified nor defined - a CxProjectCreationCollection MUST be defined - Error!" % (self.sClassDisp));
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
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the Project(s)/Branch(s) 'creation' of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            # NOTE: The Project Id field may be None or < 1. This indicates that we need to create the 'parent' Project before creating 'Branch(s)'.

            sCxProjectId = cxProjectCreation.getCxProjectId();

            if sCxProjectId != None:

                sCxProjectId = sCxProjectId.strip();

            if sCxProjectId == None or \
                len(sCxProjectId) < 1 or \
                int(sCxProjectId) < 1:

                print("%s For a CxProject 'name' of [%s] the CxProject  'id' of [%s] in the CxProjectCreation object [%s] is 'invalid' (meaning it doesn't exist) - creating this Project..." % (self.sClassDisp, sCxProjectName, sCxProjectId, cxProjectCreation));

                bCreateCxProject = self.createCxRestAPIProject(cxprojectcreation=cxProjectCreation);

                if bCreateCxProject == False:

                    print("");
                    print("%s Invocation of 'createCxRestAPIProject()' failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                sCxProjectId = cxProjectCreation.getCxProjectId();

                if sCxProjectId != None:

                    sCxProjectId = sCxProjectId.strip();

                if sCxProjectId == None or \
                    len(sCxProjectId) < 1 or \
                    int(sCxProjectId) < 1:

                    print("%s For a CxProject 'name' of [%s] the CxProject 'id' of [%s] in the CxProjectCreation object [%s] is 'invalid' - failed to create this Project - Error!" % (self.sClassDisp, sCxProjectName, sCxProjectId, cxProjectCreation));

                    return False;

                print("%s For a CxProject 'name' of [%s] created the Project with a CxProject 'id' of [%s]..." % (self.sClassDisp, sCxProjectName, sCxProjectId));
                print("");
                print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] defining the SAST Scan setting(s)..." % (self.sClassDisp, sCxProjectName, sCxProjectId));

                bDefineCxProjectSASTScanSettings = self.defineCxRestAPIProjectSASTScanSettings(cxprojectcreation=cxProjectCreation);

                if bDefineCxProjectSASTScanSettings == False:

                    print("");
                    print("%s Invocation of 'defineCxRestAPIProjectSASTScanSettings()' failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the SAST Scan setting(s) have been defined..." % (self.sClassDisp, sCxProjectName, sCxProjectId));

            else:

                print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project already 'exists' - creation of the 'main' Project was bypassed..." % (self.sClassDisp, sCxProjectName, sCxProjectId));

            # Create 'branch(s)'...

            sCxProjectId = cxProjectCreation.getCxProjectId();

            if sCxProjectId != None:

                sCxProjectId = sCxProjectId.strip();

            if sCxProjectId == None or \
                len(sCxProjectId) < 1 or \
                int(sCxProjectId) < 1:

                print("%s For a CxProject 'name' of [%s] the CxProject 'id' of [%s] in the CxProjectCreation object [%s] is 'invalid' - failed to create this Project - Error!" % (self.sClassDisp, sCxProjectName, sCxProjectId, cxProjectCreation));

                return False;

            asCxProjectBranchNames = cxProjectCreation.getCxProjectBranchNames();

            if asCxProjectBranchNames == None or \
                len(asCxProjectBranchNames) < 1:

                print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project has a Branch 'name(s)' array that is None or 'empty' - creation of the Project 'branch(s)' was bypassed..." % (self.sClassDisp, sCxProjectName, sCxProjectId));

                return True;

            sCxProjectBaseName = cxProjectCreation.getCxProjectBaseName();

            if sCxProjectBaseName != None:

                sCxProjectBaseName = sCxProjectBaseName.strip();

            if sCxProjectBaseName == None or \
                len(sCxProjectBaseName) < 1:

                sCxProjectBaseName = cxProjectCreation.getCxProjectName();

            dictCxAllProjects = self.cxProjectCreationCollection.getCxProjectMetaDataAllProjects();

            for sCxProjectBranchName in asCxProjectBranchNames:

                if sCxProjectBranchName != None:

                    sCxProjectBranchName = sCxProjectBranchName.strip();

                if sCxProjectBranchName == None or \
                    len(sCxProjectBranchName) < 1:

                    print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project has a Branch 'name' that is None or 'empty' - creation of the Project 'branch' was bypassed..." % (self.sClassDisp, sCxProjectName, sCxProjectId));

                    return True;

            #   sCxProjectBranchedName = "%s_BR_%s" % (sCxProjectBaseName, sCxProjectBranchName);
                sCxProjectBranchedName = self.cxProjectCreationCollection.cxProjectCreationCollectionDefaults.getCxProjectBranchedName(cxprojectcreation=cxProjectCreation, cxprojectbranchname=sCxProjectBranchName);
                sCxProjectBranchedId   = "";

                print("%s Returned a CxProject Branched 'name' of [%s] from a Branch 'name' of [%s] and a 'cxProjectCreation' object of [%s]..." % (self.sClassDisp, sCxProjectBranchedName, sCxProjectBranchName, cxProjectCreation));

                if sCxProjectBranchedName in list(dictCxAllProjects.keys()):

                    cxProjectData = dictCxAllProjects[sCxProjectBranchedName];

                    if cxProjectData != None:

                        sCxProjectBranchedId = cxProjectData.getCxProjectId();

                        if cxProjectCreation.dictCxProjectBranchedNames == None:

                            cxProjectCreation.dictCxProjectBranchedNames = collections.defaultdict(); 

                        cxProjectCreation.dictCxProjectBranchedNames[sCxProjectBranchedName] = sCxProjectBranchedId;

                        print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project has a Branched 'name' of [%s] and an 'id' of [%s] - creation of the Project 'branch' was bypassed..." % (self.sClassDisp, sCxProjectName, sCxProjectId, sCxProjectBranchedName, sCxProjectBranchedId));

                        continue;

                print("%s Failed to find the CxProject Branched 'name' of [%s] in key(s) of [%s] in dictionary of CxProjectCreationCollection 'dictCxAllProjects' of [%s] - creating the 'branch'..." % (self.sClassDisp, sCxProjectBranchedName, list(dictCxAllProjects.keys()), dictCxAllProjects));

                (bCreateCxProjectBranch, sCxProjectBranchedId) = self.createCxRestAPIProjectBranch(cxprojectcreation=cxProjectCreation, cxprojectbranchname=sCxProjectBranchedName);

                if bCreateCxProjectBranch == False:

                    print("");
                    print("%s Invocation of 'createCxRestAPIProjectBranch()' failed - Error!" % (self.sClassDisp));
                    print("");

                    bProcessingError = True;

                    continue;

                if sCxProjectBranchedId != None:

                    sCxProjectBranchedId = sCxProjectBranchedId.strip();

                if sCxProjectBranchedId == None or \
                    len(sCxProjectBranchedId) < 1 or \
                    int(sCxProjectBranchedId) < 1:

                    print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project has a Branch 'name' of [%s] but an 'id' of [%s] - creation of the Project 'branch' failed - Error!" % (self.sClassDisp, sCxProjectName, sCxProjectId, sCxProjectBranchedName, sCxProjectBranchedId));

                    bProcessingError = True;

                    continue;

                if cxProjectCreation.dictCxProjectBranchedNames == None:

                    cxProjectCreation.dictCxProjectBranchedNames = collections.defaultdict(); 

                cxProjectCreation.dictCxProjectBranchedNames[sCxProjectBranchedName] = sCxProjectBranchedId;

                print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project has a Branch 'name' of [%s] and an 'id' of [%s] - creation of the Project 'branch' was successful..." % (self.sClassDisp, sCxProjectName, sCxProjectId, sCxProjectBranchedName, sCxProjectBranchedId));

        except Exception as inst:

            print("%s 'createCxRestAPIProjectAndBranches()' - exception occured..." % (self.sClassDisp));
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

    def createCxRestAPIProject(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined - a CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/projects" % (self.cxServerEndpoint.getCxServerURL());
            cxReqPayload = "{'name':\"%s\", 'owningTeam':\"%s\", 'isPublic':%s}" % (cxProjectCreation.getCxProjectName(), cxProjectCreation.getCxProjectTeamId(), ("true" if (cxProjectCreation.getCxProjectIsPublic() == True) else "false"));
            cxReqHeaders = {
                'Content-Type':  "application/json;v=2.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cxOrigin':      "CxProjectCreator1.py",
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [201];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("POST", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                self.cxProjectCreationCollection.setCxProjectWasCreatedByRestAPIFlag(cxprojectwascreatedbyrestapiflag=True);

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
             
            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {Create (Main) Project} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {Create (Main) Project} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {Create (Main) Project} ===============");
                print(sReqResponseRaw);

            dictCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'dictionary' Response {Create (Main) Project} ===============");
                print((type(dictCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'dictionary' Response {Create (Main) Project} ===============");
                print((dir(dictCxReqResponseJson)));

                print("");
                print("=============== JSON 'dictionary' Response {Create (Main) Project} [RAW print] ===============");
                print(dictCxReqResponseJson);

                print("");
                print("=============== JSON 'dictionary' Response {Create (Main) Project} Enumerated ===============");

            cDictJsonItem = 0;

            for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                if dictCxReqResponseJsonKey == None:

                    continue;

                cDictJsonItem += 1;

                dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                if self.bTraceFlag == True:

                    print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                # --------------------------------------------------------------------------------------------------
                # Item #(1): 'id' [390107]...
                # Item #(2): 'link' [{'rel': 'self', 'uri': '/projects/390107'}]...
                # --------------------------------------------------------------------------------------------------

                if dictCxReqResponseJsonKey == "id":

                    cxProjectCreation.setCxProjectId(cxprojectid=dictCxReqResponseJsonItem);

        except Exception as inst:

            print("%s 'createCxRestAPIProject()' - exception occured..." % (self.sClassDisp));
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

    def defineCxRestAPIProjectSASTScanSettings(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined - a CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/sast/scanSettings" % (self.cxServerEndpoint.getCxServerURL());
            cxReqPayload = "{'projectId':%s, 'presetId':%s, 'engineConfigurationId':%s}" % (cxProjectCreation.getCxProjectId(), cxProjectCreation.getCxProjectPresetId(), cxProjectCreation.getCxProjectEngineConfigId());
            cxReqHeaders = {
                'Content-Type':  "application/json;v=1.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cxOrigin':      "CxProjectCreator1.py",
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [200];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("POST", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

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
                print("=============== TYPE JSON Response {Define (Main) Project SAST Scan Settings} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {Define (Main) Project SAST Scan Settings} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {Define (Main) Project SAST Scan Settings} ===============");
                print(sReqResponseRaw);

            dictCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'dictionary' Response {Define (Main) Project SAST Scan Settings} ===============");
                print((type(dictCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'dictionary' Response {Define (Main) Project SAST Scan Settings} ===============");
                print((dir(dictCxReqResponseJson)));

                print("");
                print("=============== JSON 'dictionary' Response {Define (Main) Project SAST Scan Settings} [RAW print] ===============");
                print(dictCxReqResponseJson);

                print("");
                print("=============== JSON 'dictionary' Response {Define (Main) Project SAST Scan Settings} Enumerated ===============");

            cDictJsonItem = 0;

            for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                if dictCxReqResponseJsonKey == None:

                    continue;

                cDictJsonItem += 1;

                dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                if self.bTraceFlag == True:

                    print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                # --------------------------------------------------------------------------------------------------
                # Item #(1): 'id' [390107]...
                # Item #(2): 'link' [{'rel': 'self', 'uri': '/sast/scanSettings/390107'}]...
                # --------------------------------------------------------------------------------------------------

        except Exception as inst:

            print("%s 'defineCxRestAPIProjectSASTScanSettings()' - exception occured..." % (self.sClassDisp));
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

    def createCxRestAPIProjectBranch(self, cxprojectcreation=None, cxprojectbranchname=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined - a CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return (False, "0");

        sCxProjectBranchName = cxprojectbranchname;

        if sCxProjectBranchName != None:

            sCxProjectBranchName = sCxProjectBranchName.strip();

        if sCxProjectBranchName == None or \
            len(sCxProjectBranchName) < 1:

            print("");
            print("%s CxProjectCreation contains NO 'Branch' name(s) - it MUST contain at least 1 'Branch' name - Error!" % (self.sClassDisp));
            print("");

            return (False, "0");

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/projects/%s/branch" % (self.cxServerEndpoint.getCxServerURL(), cxProjectCreation.getCxProjectId());
            cxReqPayload = "{'name':\"%s\"}" % (sCxProjectBranchName);
            cxReqHeaders = {
                'Content-Type':  "application/json;v=1.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cxOrigin':      "CxProjectCreator1.py",
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [201];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("POST", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                self.cxProjectCreationCollection.setCxProjectWasCreatedByRestAPIFlag(cxprojectwascreatedbyrestapiflag=True);

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
             
            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {Create (Branch) Project} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {Create (Branch) Project} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {Create (Branch) Project} ===============");
                print(sReqResponseRaw);

            dictCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'dictionary' Response {Create (Branch) Project} ===============");
                print((type(dictCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'dictionary' Response {Create (Branch) Project} ===============");
                print((dir(dictCxReqResponseJson)));

                print("");
                print("=============== JSON 'dictionary' Response {Create (Branch) Project} [RAW print] ===============");
                print(dictCxReqResponseJson);

                print("");
                print("=============== JSON 'dictionary' Response {Create (Branch) Project} Enumerated ===============");

            sCxProjectBranchId = "0";
            cDictJsonItem      = 0;

            for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                if dictCxReqResponseJsonKey == None:

                    continue;

                cDictJsonItem += 1;

                dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                if self.bTraceFlag == True:

                    print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                # --------------------------------------------------------------------------------------------------
                # Item #(1): 'id' [390108]...
                # Item #(2): 'link' [{'rel': 'self', 'uri': '/projects/390108'}]...
                # --------------------------------------------------------------------------------------------------

                if dictCxReqResponseJsonKey == "id":

                    sCxProjectBranchId = "%s" % (dictCxReqResponseJsonItem);

        except Exception as inst:

            print("%s 'createCxRestAPIProjectBranch()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return (False, "0");

        if bProcessingError == True:

            return (False, "0");

        return (True, sCxProjectBranchId);

    def deleteCxRestAPIProjectAndBranches(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined - a CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxProjectCreationCollection == None:

            print("");
            print("%s NO CxProjectCreationCollection has been specified nor defined - a CxProjectCreationCollection MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

        # Delete the 'main' Project:

            sCxProjectName = cxProjectCreation.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the Project(s)/Branch(s) 'deletion' of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            sCxProjectId = cxProjectCreation.getCxProjectId();
         
            if sCxProjectId != None:
         
                sCxProjectId = sCxProjectId.strip();
         
            if sCxProjectId == None or \
                len(sCxProjectId) < 1 or \
                int(sCxProjectId) < 1:
         
                print("%s For a CxProject 'name' of [%s] the CxProject 'id' of [%s] in the CxProjectCreation object [%s] is 'invalid' - cannot delete this Project - Error!" % (self.sClassDisp, sCxProjectName, sCxProjectId, cxProjectCreation));

                bProcessingError = True;

            else:

                bDeleteCxProject = self.deleteCxRestAPIProject(cxprojectid=sCxProjectId);

                if bDeleteCxProject == False:

                    print("");
                    print("%s Invocation of 'deleteCxRestAPIProject()' failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

        # Delete 'branch(s)'...

            asCxProjectBranchNames = cxProjectCreation.getCxProjectBranchNames();

            if asCxProjectBranchNames == None or \
                len(asCxProjectBranchNames) < 1:

                print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project has a Branch 'name(s)' array that is None or 'empty' - deletion of the Project 'branch(s)' was bypassed..." % (self.sClassDisp, sCxProjectName, sCxProjectId));

                return True;

            sCxProjectBaseName = cxProjectCreation.getCxProjectBaseName();

            if sCxProjectBaseName != None:

                sCxProjectBaseName = sCxProjectBaseName.strip();

            if sCxProjectBaseName == None or \
                len(sCxProjectBaseName) < 1:

                sCxProjectBaseName = cxProjectCreation.getCxProjectName();

            dictCxAllProjects = self.cxProjectCreationCollection.getCxProjectMetaDataAllProjects();

            for sCxProjectBranchName in asCxProjectBranchNames:

                if sCxProjectBranchName != None:

                    sCxProjectBranchName = sCxProjectBranchName.strip();

                if sCxProjectBranchName == None or \
                    len(sCxProjectBranchName) < 1:

                    print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project has a Branch 'name' that is None or 'empty' - deletion of the Project 'branch' was bypassed..." % (self.sClassDisp, sCxProjectName, sCxProjectId));

                    return True;

            #   sCxProjectBranchedName = "%s_BR_%s" % (sCxProjectBaseName, sCxProjectBranchName);
                sCxProjectBranchedName = self.cxProjectCreationCollection.cxProjectCreationCollectionDefaults.getCxProjectBranchedName(cxprojectcreation=cxProjectCreation, cxprojectbranchname=sCxProjectBranchName);
                sCxProjectBranchedId   = "";

                print("%s Returned a CxProject Branched 'name' of [%s] from a Branch 'name' of [%s] and a 'cxProjectCreation' object of [%s]..." % (self.sClassDisp, sCxProjectBranchedName, sCxProjectBranchName, cxProjectCreation));

                if sCxProjectBranchedName in list(dictCxAllProjects.keys()):

                    cxProjectData = dictCxAllProjects[sCxProjectBranchedName];

                    if cxProjectData != None:

                        sCxProjectBranchedId = cxProjectData.getCxProjectId();

                        if cxProjectCreation.dictCxProjectBranchedNames == None:

                            cxProjectCreation.dictCxProjectBranchedNames = collections.defaultdict(); 

                        cxProjectCreation.dictCxProjectBranchedNames[sCxProjectBranchedName] = sCxProjectBranchedId;

                        bDeleteCxProject = self.deleteCxRestAPIProject(cxprojectid=sCxProjectBranchedId);

                        if bDeleteCxProject == False:

                            print("");
                            print("%s Invocation of 'deleteCxRestAPIProject()' failed - Error!" % (self.sClassDisp));
                            print("");

                            return False;

                        print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project has a Branch 'name' of [%s] and an 'id' of [%s] - deletion of the Project 'branch' was successful..." % (self.sClassDisp, sCxProjectName, sCxProjectId, sCxProjectBranchedName, sCxProjectBranchedId));

                else:

                        print("%s For a CxProject 'name' of [%s] and an 'id' of [%s] the Project has a Branch 'name' of [%s] - Project 'branch' does NOT exist - deletion of the Project 'branch' was bypassed..." % (self.sClassDisp, sCxProjectName, sCxProjectId, sCxProjectBranchedName));

        except Exception as inst:

            print("%s 'deleteCxRestAPIProjectAndBranches()' - exception occured..." % (self.sClassDisp));
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

    def deleteCxRestAPIProject(self, cxprojectid=None):

    #   self.bTraceFlag = True;

        sCxProjectId = cxprojectid;

        if sCxProjectId != None:

            sCxProjectId = sCxProjectId.strip();

        if sCxProjectId == None or \
            len(sCxProjectId) < 1 or \
            int(sCxProjectId) < 1:

            print("%s The supplied CxProject 'id' of [%s] is 'invalid' - cannot delete this Project - Error!" % (self.sClassDisp, sCxProjectId));

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/projects/%s" % (self.cxServerEndpoint.getCxServerURL(), sCxProjectId);
            cxReqPayload = "{'deleteRunningScans':true}";
            cxReqHeaders = {
                'Content-Type':  "application/json;v=2.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cxOrigin':      "CxProjectCreator1.py",
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [202];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("DELETE", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

        except Exception as inst:

            print("%s 'deleteCxRestAPIProject()' - exception occured..." % (self.sClassDisp));
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

    def uploadCxRestAPIProjectZip(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined - a CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        sCxProjectSASTZipFile = cxProjectCreation.getCxProjectSASTZipFilespec();

        if sCxProjectSASTZipFile != None:

            sCxProjectSASTZipFile = sCxProjectSASTZipFile.strip();

        if sCxProjectSASTZipFile == None or \
            len(sCxProjectSASTZipFile) < 1:

            print("");
            print("%s The supplied CxProjectCreation has a 'sCxProjectSASTZipFile' that is None or Empty - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            sCxProjectSASTZipFilespec = os.path.realpath(sCxProjectSASTZipFile);
            bCxProjectSASTZipIsFile   = os.path.isfile(sCxProjectSASTZipFilespec);

            if bCxProjectSASTZipIsFile == False:

                print("");
                print("%s Command received a Project Creation SAST 'zip' filespec of [%s] that does NOT exist - Error!" % (self.sClassDisp, sCxProjectSASTZipFilespec));
                print("");

                return False;

            cCxProjectSASTZipFile                                     = os.path.getsize(sCxProjectSASTZipFilespec);
            (sCxProjectSASTZipPathName, sCxProjectSASTZipFilenameExt) = os.path.split(sCxProjectSASTZipFilespec);

            print("");
            print("%s Uploading the Project Creation SAST 'zip' file [%s] with a 'filename.ext' of [%s] containing (%d) bytes of data..." % (self.sClassDisp, sCxProjectSASTZipFilespec, sCxProjectSASTZipFilenameExt, cCxProjectSASTZipFile));
            print("");

            cxRequestURL   = "%s/cxrestapi/projects/%s/sourceCode/attachments" % (self.cxServerEndpoint.getCxServerURL(), cxProjectCreation.getCxProjectId());
            cxReqHeaders   = {
                'Content-Type':    "application/x-www-form-urlencoded",
                'Authorization':   ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cxOrigin':        "CxApplicationScanner1.py",
                'Accept':          "application/json;v1.0",
                'api-version':     "2.0", 
                'accept-encoding': "gzip, deflate",
                'cache-control':   "no-cache"
                };
            cxReqRespOk    = [204];
            cxZippedSource = {"zippedSource": (sCxProjectSASTZipFilenameExt, open(sCxProjectSASTZipFilespec, 'rb'), "application/zip")};
            cxZipMultipart = MultipartEncoder(fields=cxZippedSource);

            cxReqHeaders.update({"Content-Type": cxZipMultipart.content_type});

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with Header(s) of [%s] and Data of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqHeaders, cxZipMultipart));

            cxReqResponse = requests.request("POST", cxRequestURL, headers=cxReqHeaders, data=cxZipMultipart, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                self.cxProjectCreationCollection.setCxProjectWasCreatedByRestAPIFlag(cxprojectwascreatedbyrestapiflag=True);

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

                jsonReqResponse = cxReqResponse.json();

                if jsonReqResponse != None:

                    sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
                     
                    if self.bTraceFlag == True:
                 
                        print("");
                        print("=============== TYPE JSON Response {Upload (Application) Project Zipfile} ===============");
                        print((type(sReqResponseRaw)));
                 
                        print("");
                        print("=============== DIR JSON Response {Upload (Application) Project Zipfile} ===============");
                        print((dir(sReqResponseRaw)));
                 
                        print("");
                        print("=============== JSON 'string' Response {Upload (Application) Project Zipfile} ===============");
                        print(sReqResponseRaw);
                 
                    dictCxReqResponseJson = json.loads(sReqResponseRaw);
                 
                    if self.bTraceFlag == True:
                 
                        print("");
                        print("=============== TYPE JSON 'dictionary' Response {Upload (Application) Project Zipfile} ===============");
                        print((type(dictCxReqResponseJson)));
                 
                        print("");
                        print("=============== DIR JSON 'dictionary' Response {Upload (Application) Project Zipfile} ===============");
                        print((dir(dictCxReqResponseJson)));
                 
                        print("");
                        print("=============== JSON 'dictionary' Response {Upload (Application) Project Zipfile} [RAW print] ===============");
                        print(dictCxReqResponseJson);
                 
                        print("");
                        print("=============== JSON 'dictionary' Response {Upload (Application) Project Zipfile} Enumerated ===============");
                 
                    cDictJsonItem = 0;
                 
                    for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):
                 
                        if dictCxReqResponseJsonKey == None:
                 
                            continue;
                 
                        cDictJsonItem += 1;
                 
                        dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];
                 
                        if self.bTraceFlag == True:
                 
                            print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

        except Exception as inst:

            print("%s 'uploadCxRestAPIProjectZip()' - exception occured..." % (self.sClassDisp));
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

    def scanCxRestAPIProject(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined - a CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/sast/scans" % (self.cxServerEndpoint.getCxServerURL());
            cxReqPayload = "{'projectId':\"%s\", 'isIncremental':\"false\", 'isPublic':\"%s\", 'forceScan':\"true\"}" % (cxProjectCreation.getCxProjectId(), ("true" if (cxProjectCreation.getCxProjectIsPublic() == True) else "false"));
            cxReqHeaders = {
                'Content-Type':  "application/json;v=1.0",
                'Authorization': ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cxOrigin':      "CxApplicationScanner1.py",
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [201];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Payload of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("POST", cxRequestURL, data=cxReqPayload, headers=cxReqHeaders, verify=False);

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                self.cxProjectCreationCollection.setCxProjectWasCreatedByRestAPIFlag(cxprojectwascreatedbyrestapiflag=True);

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
             
            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {Scan (Application) Project} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {Scan (Application) Project} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {Scan (Application) Project} ===============");
                print(sReqResponseRaw);

            dictCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'dictionary' Response {Scan (Application) Project} ===============");
                print((type(dictCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'dictionary' Response {Scan (Application) Project} ===============");
                print((dir(dictCxReqResponseJson)));

                print("");
                print("=============== JSON 'dictionary' Response {Scan (Application) Project} [RAW print] ===============");
                print(dictCxReqResponseJson);

                print("");
                print("=============== JSON 'dictionary' Response {Scan (Application) Project} Enumerated ===============");

            cDictJsonItem = 0;

            for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                if dictCxReqResponseJsonKey == None:

                    continue;

                cDictJsonItem += 1;

                dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                if self.bTraceFlag == True:

                    print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                # --------------------------------------------------------------------------------------------------
                # Item #(1): 'id' [390107]...
                # Item #(2): 'link' [{'rel': 'self', 'uri': '/projects/390107'}]...
                # --------------------------------------------------------------------------------------------------
             
                if dictCxReqResponseJsonKey == "id":

                    dictCxScanData = {"Action":"Scan", "id":("%s" % (dictCxReqResponseJsonItem))};
             
                    cxProjectCreation.setCxProjectExtraField3(cxprojectextrafield3=dictCxScanData);
                #   cxProjectCreation.setCxProjectExtraField2(cxprojectextrafield2=dictCxScanData);
                #   cxProjectCreation.setCxProjectId(cxprojectid=dictCxReqResponseJsonItem);

        except Exception as inst:

            print("%s 'scanCxRestAPIProject()' - exception occured..." % (self.sClassDisp));
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

    def scanOsaCxRestAPIProject(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined - a CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        sCxProjectOSAZipFile = cxProjectCreation.getCxProjectOSAZipFilespec();

        if sCxProjectOSAZipFile != None:

            sCxProjectOSAZipFile = sCxProjectOSAZipFile.strip();

        if sCxProjectOSAZipFile == None or \
            len(sCxProjectOSAZipFile) < 1:

            print("");
            print("%s The supplied CxProjectCreation has a 'sCxProjectOSAZipFile' that is None or Empty - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            sCxProjectOSAZipFilespec = os.path.realpath(sCxProjectOSAZipFile);
            bCxProjectOSAZipIsFile   = os.path.isfile(sCxProjectOSAZipFilespec);

            if bCxProjectOSAZipIsFile == False:

                print("");
                print("%s Command received a Project Creation OSA 'zip' filespec of [%s] that does NOT exist - Error!" % (self.sClassDisp, sCxProjectOSAZipFilespec));
                print("");

                return False;

            cCxProjectOSAZipFile                                    = os.path.getsize(sCxProjectOSAZipFilespec);
            (sCxProjectOSAZipPathName, sCxProjectOSAZipFilenameExt) = os.path.split(sCxProjectOSAZipFilespec);

            print("");
            print("%s Uploading the Project Creation OSA 'zip' file [%s] with a 'filename.ext' of [%s] containing (%d) bytes of data..." % (self.sClassDisp, sCxProjectOSAZipFilespec, sCxProjectOSAZipFilenameExt, cCxProjectOSAZipFile));
            print("");

            cxRequestURL   = "%s/cxrestapi/osa/scans" % (self.cxServerEndpoint.getCxServerURL());
            cxReqHeaders   = {
        #       'Content-Type':    "application/x-www-form-urlencoded",
                'Content-Type':    "application/json;v=1.0/2.0",
                'Authorization':   ("%s %s" % (self.cxServerEndpoint.getCxTokenType(), self.cxServerEndpoint.getCxAccessToken())),
                'cxOrigin':        "CxApplicationScanner1.py",
                'Accept':          "application/json;v1.0",
                'api-version':     "2.0", 
                'accept-encoding': "gzip, deflate",
                'cache-control':   "no-cache"
                };
            cxReqRespOk    = [202];
            cxZippedSource = {
                'projectId':    ("%s" % (cxProjectCreation.getCxProjectId())),
                'origin':       "Portal",
                "zippedSource": (sCxProjectOSAZipFilenameExt, open(sCxProjectOSAZipFilespec, 'rb'), "application/zip")
                };
            cxZipMultipart = MultipartEncoder(fields=cxZippedSource);

            cxReqHeaders.update({"Content-Type": cxZipMultipart.content_type});

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with Header(s) of [%s] and Data of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqHeaders, cxZipMultipart));

            cxReqResponse = requests.request("POST", cxRequestURL, headers=cxReqHeaders, data=cxZipMultipart, verify=False);

        #   url = "http://192.168.2.190:8080/cxrestapi/osa/scans"
        #   payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"projectId\"\r\n\r\n390238\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"origin\"\r\n\r\nPortal\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"zippedSource\"; filename=\"PHPMailer-master.zip\"\r\nContent-Type: application/zip\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        #   headers = {
        #       'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        #       'Content-Type': "application/json;v=1.0/2.0",
        #       'cxOrigin': "DrcPostman1",
        #       'cache-control': "no-cache"
        #       } 
        #   response = requests.request("POST", url, data=payload, headers=headers, verify=False)

            if self.bTraceFlag == True:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            if cxReqResponse.status_code in cxReqRespOk:

                self.cxProjectCreationCollection.setCxProjectWasCreatedByRestAPIFlag(cxprojectwascreatedbyrestapiflag=True);

                if self.bTraceFlag == True:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));

            else:

                bProcessingError = True;

                print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));

            sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON Response {Scan OSA (Application) Project} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {Scan OSA (Application) Project} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {Scan OSA (Application) Project} ===============");
                print(sReqResponseRaw);

            dictCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'dictionary' Response {Scan OSA (Application) Project} ===============");
                print((type(dictCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'dictionary' Response {Scan OSA (Application) Project} ===============");
                print((dir(dictCxReqResponseJson)));

                print("");
                print("=============== JSON 'dictionary' Response {Scan OSA (Application) Project} [RAW print] ===============");
                print(dictCxReqResponseJson);

                print("");
                print("=============== JSON 'dictionary' Response {Scan OSA (Application) Project} Enumerated ===============");

            cDictJsonItem = 0;

            for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                if dictCxReqResponseJsonKey == None:

                    continue;

                cDictJsonItem += 1;

                dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                if self.bTraceFlag == True:

                    print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

            #   # --------------------------------------------------------------------------------------------------
            #   # Item #(1): 'id' [390107]...
            #   # Item #(2): 'link' [{'rel': 'self', 'uri': '/projects/390107'}]...
            #   # --------------------------------------------------------------------------------------------------
             
                if dictCxReqResponseJsonKey == "scanId":
             
                    dictCxOsaScanData = {"Action":"OSAScan", "id":("%s" % (dictCxReqResponseJsonItem))};
             
                    cxProjectCreation.setCxProjectExtraField4(cxprojectextrafield4=dictCxOsaScanData);
            #   #   cxProjectCreation.setCxProjectExtraField3(cxprojectextrafield3=dictCxScanData);
            #   #   cxProjectCreation.setCxProjectExtraField2(cxprojectextrafield2=dictCxScanData);
            #   #   cxProjectCreation.setCxProjectId(cxprojectid=dictCxReqResponseJsonItem);

        except Exception as inst:

            print("%s 'scanOSACxRestAPIProject()' - exception occured..." % (self.sClassDisp));
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

