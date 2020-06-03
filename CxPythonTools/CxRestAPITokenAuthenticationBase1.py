
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

import CxServerEndpoint1;
import CxRestAPIStatistics1;

class CxRestAPITokenAuthenticationBase(object):

    sClassMod           = __name__;
    sClassId            = "CxRestAPITokenAuthenticationBase";
    sClassVers          = "(v1.0509)";
    sClassDisp          = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag          = False;
    cxServerEndpoint    = None;

    def __init__(self, trace=False, cxserverendpoint=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxServerEndpoint(cxserverendpoint=cxserverendpoint);

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

    def resetCxRestAPITokenAuthenticationBaseObject(self):

        return;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'cxServerEndpoint' is [%s]..." % (self.sClassDisp, self.cxServerEndpoint));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'cxServerEndpoint' is [%s]. " % (self.cxServerEndpoint));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def getCxRestAPITokenAuthentication(self):

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

        try:

            bGetCxAuthTokenOk = self.getCxRestAPIAuthToken();

            if bGetCxAuthTokenOk == False:

                print("");
                print("%s Invocation of 'getCxRestAPIAuthToken()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'getCxRestAPITokenAuthentication()' - exception occured..." % (self.sClassDisp));
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

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/cxrestapi/auth/identity/connect/token" % (self.cxServerEndpoint.getCxServerURL());
            cxReqPayload = "username=%s&password=%s&grant_type=password&scope=sast_rest_api&client_id=resource_owner_client&client_secret=014DF517-39D1-4453-B7B3-9930C563627C" % (self.cxServerEndpoint.getCxAuthUserID(), self.cxServerEndpoint.getCxAuthPassword());
            cxReqHeaders = {
                'Content-Type': "application/x-www-form-urlencoded",
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
                print("=============== TYPE JSON Response {Auth/Token} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {Auth/Token} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {Auth/Token} ===============");
                print(sReqResponseRaw);

            dictCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'dictionary' Response {Auth/Token} ===============");
                print((type(dictCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'dictionary' Response {Auth/Token} ===============");
                print((dir(dictCxReqResponseJson)));

                print("");
                print("=============== JSON 'dictionary' Response {Auth/Token} [RAW print] ===============");
                print(dictCxReqResponseJson);

                print("");
                print("=============== JSON 'dictionary' Response {Auth/Token} Enumerated ===============");

            self.cxServerEndpoint.resetCxServerEndpointAuthTokenDetails();

            cDictJsonItem = 0;

            for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                if dictCxReqResponseJsonKey == None:

                    continue;

                cDictJsonItem += 1;

                dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                if self.bTraceFlag == True:

                    print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                # --------------------------------------------------------------------------------------------------
                #  Item #(1): 'access_token' [eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlNIcDNRNXZ...Gx38_OWA]...
                #  Item #(2): 'token_type' [Bearer]...
                #  Item #(3): 'expires_in' [86400]...
                # --------------------------------------------------------------------------------------------------
                      
                if dictCxReqResponseJsonKey == "token_type":

                    self.cxServerEndpoint.setCxTokenType(cxtokentype=dictCxReqResponseJsonItem);

                if dictCxReqResponseJsonKey == "access_token":

                    self.cxServerEndpoint.setCxAccessToken(cxaccesstoken=dictCxReqResponseJsonItem);

                if dictCxReqResponseJsonKey == "expires_in":

                    self.cxServerEndpoint.setCxAccessTokenExpiresIn(cxaccesstokenexpiresin=dictCxReqResponseJsonItem);

            if len(self.cxServerEndpoint.getCxAccessToken()) < 1:

                print("%s Checkmarx 'sCxAccessToken' is 'empty' - Error!" % (self.sClassDisp));

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

        if bProcessingError == True:

            return False;

        return True;

