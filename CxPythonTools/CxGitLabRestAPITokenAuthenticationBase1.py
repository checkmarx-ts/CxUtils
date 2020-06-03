
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

import CxGitLabServerEndpoint1;
import CxRestAPIStatistics1;

class CxGitLabRestAPITokenAuthenticationBase(object):

    sClassMod              = __name__;
    sClassId               = "CxGitLabRestAPITokenAuthenticationBase";
    sClassVers             = "(v1.0205)";
    sClassDisp             = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag             = False;
    CxGitLabServerEndpoint = None;

    def __init__(self, trace=False, cxgitlabserverendpoint=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxGitLabServerEndpoint(cxgitlabserverendpoint=cxgitlabserverendpoint);

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

        return self.CxGitLabServerEndpoint;

    def setCxGitLabServerEndpoint(self, cxgitlabserverendpoint=None):

        self.CxGitLabServerEndpoint = cxgitlabserverendpoint;

    def resetCxGitLabRestAPITokenAuthenticationBaseObject(self):

        return;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'CxGitLabServerEndpoint' is [%s]..." % (self.sClassDisp, self.CxGitLabServerEndpoint));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'CxGitLabServerEndpoint' is [%s]. " % (self.CxGitLabServerEndpoint));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def getCxGitLabRestAPITokenAuthentication(self):

        if self.CxGitLabServerEndpoint == None:

            print("");
            print("%s NO CxGitLabServerEndpoint has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxGitLabServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.CxGitLabServerEndpoint.getCxGitLabServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxGitLabServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            bGetCxAuthTokenOk = self.__getCxRestAPIAuthToken();

            if bGetCxAuthTokenOk == False:

                print("");
                print("%s Invocation of '__getCxRestAPIAuthToken()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'getCxGitLabRestAPITokenAuthentication()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def __getCxRestAPIAuthToken(self):

        bProcessingError = False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

            cxRequestURL = "%s/oauth/token" % (self.CxGitLabServerEndpoint.getCxGitLabServerURL());
            cxReqPayload = "username=%s&password=%s&grant_type=password" % (self.CxGitLabServerEndpoint.getCxGitLabUserId(), self.CxGitLabServerEndpoint.getCxGitLabPassword());
            cxReqHeaders = {
            #   'Content-Type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache"
                };
            cxReqRespOk  = [200];

            if self.bTraceFlag == True:

                print("%s Issuing Request #(%d) of URL [%s] with a Params of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestURL, cxReqPayload, cxReqHeaders));

            cxReqResponse = requests.request("POST", cxRequestURL, params=cxReqPayload, headers=cxReqHeaders, verify=False);

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
                print("=============== TYPE JSON Response {OAuth/Token} ===============");
                print((type(sReqResponseRaw)));

                print("");
                print("=============== DIR JSON Response {OAuth/Token} ===============");
                print((dir(sReqResponseRaw)));

                print("");
                print("=============== JSON 'string' Response {OAuth/Token} ===============");
                print(sReqResponseRaw);

            dictCxReqResponseJson = json.loads(sReqResponseRaw);

            if self.bTraceFlag == True:

                print("");
                print("=============== TYPE JSON 'dictionary' Response {OAuth/Token} ===============");
                print((type(dictCxReqResponseJson)));

                print("");
                print("=============== DIR JSON 'dictionary' Response {OAuth/Token} ===============");
                print((dir(dictCxReqResponseJson)));

                print("");
                print("=============== JSON 'dictionary' Response {OAuth/Token} [RAW print] ===============");
                print(dictCxReqResponseJson);

                print("");
                print("=============== JSON 'dictionary' Response {OAuth/Token} Enumerated ===============");

            self.CxGitLabServerEndpoint.resetCxGitLabServerEndpointAuthTokenDetails();

            cDictJsonItem = 0;

            for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):

                if dictCxReqResponseJsonKey == None:

                    continue;

                cDictJsonItem += 1;

                dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];

                if self.bTraceFlag == True:

                    print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));

                # --------------------------------------------------------------------------------------------------
                #  Item #(1): 'access_token' [6e2e8e80dc3215bf85e22106eeb683129de7023832a9f2e45056f857b603774a]...
                #  Item #(2): 'token_type' [bearer]...
                #  Item #(3): 'refresh_token' [27c3a203b8f372f575156fa8fba671d5fdbbcaabdd0a88fde656eaf47aaf4648]...
                #  Item #(4): 'scope' [api]...
                #  Item #(5): 'created_at' [1572034525]...
                # --------------------------------------------------------------------------------------------------
                      
                if dictCxReqResponseJsonKey == "token_type":

                    self.CxGitLabServerEndpoint.setCxGitLabTokenType(cxgitlabtokentype=dictCxReqResponseJsonItem);

                if dictCxReqResponseJsonKey == "access_token":

                    self.CxGitLabServerEndpoint.setCxGitLabAccessToken(cxgitlabaccesstoken=dictCxReqResponseJsonItem);

            if len(self.CxGitLabServerEndpoint.getCxGitLabAccessToken()) < 1:

                print("%s Checkmarx 'sCxGitLabAccessToken' is 'empty' - Error!" % (self.sClassDisp));

                return False;

        except Exception as inst:

            print("%s '__getCxRestAPIAuthToken()' - exception occured..." % (self.sClassDisp));
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

