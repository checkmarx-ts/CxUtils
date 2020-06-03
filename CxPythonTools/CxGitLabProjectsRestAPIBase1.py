
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

import CxGitLabProjectData1;
import CxGitLabServerEndpoint1;
import CxGitLabRestAPITokenAuthenticationBase1;
import CxRestAPIStatistics1;

class CxGitLabProjectsRestAPIBase(object):

    sClassMod                     = __name__;
    sClassId                      = "CxGitLabProjectsRestAPIBase";
    sClassVers                    = "(v1.0212)";
    sClassDisp                    = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                    = False;
    cxGitLabServerEndpoint        = None;
    cxGitLabProjectDataCollection = None;

    # Constructed objects:

    sCxGitLabServerURL            = None;
    cxRestAPITokenAuth            = None;
    asCxGitLabRestResponses       = list();

    def __init__(self, trace=False, cxgitlabserverendpoint=None, cxgitlabprojectdatacollection=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxGitLabServerEndpoint(cxgitlabserverendpoint=cxgitlabserverendpoint);
            self.setCxGitLabProjectDataCollection(cxgitlabprojectdatacollection=cxgitlabprojectdatacollection);

            sPythonVers = ("v%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro));
            sServerNode = platform.node();
            dtNow       = datetime.now();
            sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S");

            sHeaderMsg = ("%s The Checkmarx GitLab 'Get-ALL-Projects' via Rest API #1 is starting execution from Server [%s] on [%s] under Python [%s]..." % (self.sClassDisp, sServerNode, sDTNowStamp, sPythonVers));

            self.asCxGitLabRestResponses.append("");
            self.asCxGitLabRestResponses.append(sHeaderMsg);
            self.asCxGitLabRestResponses.append("");

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

        return self.cxGitLabProjectDataCollection;

    def setCxGitLabProjectDataCollection(self, cxgitlabprojectdatacollection=None):

        self.cxGitLabProjectDataCollection = cxgitlabprojectdatacollection;

    def getCxGitLabRestResponses(self):

        return self.asCxGitLabRestResponses;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'cxGitLabServerEndpoint' is [%s]..." % (self.sClassDisp, self.cxGitLabServerEndpoint));
            print("%s The contents of 'cxGitLabProjectDataCollection' is [%s]..." % (self.sClassDisp, self.cxGitLabProjectDataCollection));
            print("%s The contents of 'sCxGitLabServerURL' is [%s]..." % (self.sClassDisp, self.sCxGitLabServerURL));
            print("%s The contents of 'cxRestAPITokenAuth' is [%s]..." % (self.sClassDisp, self.cxRestAPITokenAuth));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'cxGitLabServerEndpoint' is [%s], " % (self.cxGitLabServerEndpoint));
        asObjDetail.append("'cxGitLabProjectDataCollection' is [%s], " % (self.cxGitLabProjectDataCollection));
        asObjDetail.append("'sCxGitLabServerURL' is [%s], " % (self.sCxGitLabServerURL));
        asObjDetail.append("'cxRestAPITokenAuth' is [%s]. " % (self.cxRestAPITokenAuth));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def validateCxGitLabProjectRequiredFields(self):

        try:

            if self.cxGitLabProjectDataCollection == None:

                print("");
                print("%s NO CxGitLabProjectDataCollection has been specified nor defined - a CxGitLabProjectDataCollection MUST be defined - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.cxGitLabServerEndpoint == None:

                print("");
                print("%s NO CxGitLabServerEndpoint has been specified nor defined - a CxGitLabServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.cxGitLabServerEndpoint.getCxGitLabServerEndpointActiveFlag() == False:

                print("");
                print("%s The supplied CxGitLabServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.sCxGitLabServerURL != None:

                self.sCxGitLabServerURL = self.sCxGitLabServerURL.strip();

            if self.sCxGitLabServerURL == None or \
                len(self.sCxGitLabServerURL) < 1:

                self.sCxGitLabServerURL = self.cxGitLabServerEndpoint.getCxGitLabServerURL();

            if self.sCxGitLabServerURL != None:

                self.sCxGitLabServerURL = self.sCxGitLabServerURL.strip();

            if self.sCxGitLabServerURL == None or \
                len(self.sCxGitLabServerURL) < 1:

                print("");
                print("%s NO CxGitLab Server URL has been specified nor defined - 1 MUST be defined - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'validateCxGitLabProjectRequiredFields()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def getCxGitLabProjectsInitialDataViaRestAPI(self):

        bValidateReqFieldsOk = self.validateCxGitLabProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxGitLabProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            sCxAccessToken = self.cxGitLabServerEndpoint.getCxGitLabAccessToken();

            if sCxAccessToken != None:

                sCxAccessToken = sCxAccessToken.strip();

            if sCxAccessToken == None or \
                len(sCxAccessToken) < 1:

                bGetCxAuthTokenOk = self.__getCxGitLabRestAPIAuthToken();

                if bGetCxAuthTokenOk == False:

                    print("");
                    print("%s Invocation of '__getCxGitLabRestAPIAuthToken()' failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            bGetCxGitLabAllProjectsOk = self.getGitLabProjectsDataForAllProjects();

            if bGetCxGitLabAllProjectsOk == False:

                print("");
                print("%s Invocation of 'getGitLabProjectsDataForAllProjects()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.bTraceFlag == True:

                print("");
                print("%s CxGitLabProjectDataCollection (after 'Get-ALL-Project(s)') is:" % (self.sClassDisp));
                print(self.cxGitLabProjectDataCollection.toString());
                print("");

        except Exception as inst:

            print("%s 'getCxGitLabProjectsInitialDataViaRestAPI()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def __getCxGitLabRestAPIAuthToken(self):

        bValidateReqFieldsOk = self.validateCxGitLabProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxGitLabProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            self.cxRestAPITokenAuth = CxGitLabRestAPITokenAuthenticationBase1.CxGitLabRestAPITokenAuthenticationBase(trace=self.bTraceFlag, cxgitlabserverendpoint=self.cxGitLabServerEndpoint);

            bGetCxRestAPIAuthTokenOk = self.cxRestAPITokenAuth.getCxGitLabRestAPITokenAuthentication();

            if bGetCxRestAPIAuthTokenOk == False:

                print("");
                print("%s Invocation of 'cxRestAPITokenAuth.getCxGitLabRestAPITokenAuthentication()' failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s '__getCxGitLabRestAPIAuthToken()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def getGitLabProjectsDataForAllProjects(self):

        bProcessingError = False;

        bValidateReqFieldsOk = self.validateCxGitLabProjectRequiredFields();

        if bValidateReqFieldsOk == False:

            print("");
            print("%s CxGitLabProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            CxRestAPIStatistics1.cRestAPICallsMade += 1;

        #   url = "http://10.211.55.50:80/api/v4/groups/JwebsoftwareDev/projects"
        #   querystring = {"simple":"true"}
        #   headers = {
        #       'Content-Type': "application/json",
        #       'Authorization': "Bearer 6e2e8e80dc3215bf85e22106eeb683129de7023832a9f2e45056f857b603774a",
        #       'User-Agent': "PostmanRuntime/7.19.0",
        #       'Accept': "*/*",
        #       'Cache-Control': "no-cache",
        #       'Postman-Token': "12faa173-0735-4924-9717-bf392dc5686b,ea8d238a-77e4-49b2-93d6-df440e807812",
        #       'Host': "10.211.55.50:80",
        #       'Accept-Encoding': "gzip, deflate",
        #       'Cookie': "experimentation_subject_id=ImM3N2YxZGM5LWNhNWUtNDlmZC1iOWIxLWM1OTZmNWQ4YzY5OSI%3D--7d47e1783a5c171560b14a3c787158e8730900b5",
        #       'Connection': "keep-alive",
        #       'cache-control': "no-cache"
        #       }
        #   response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
                     
            cxRequestVerb  = "GET";
            cxRequestURL   = ("%s/api/v4/groups/%s/projects" % (self.sCxGitLabServerURL, self.cxGitLabServerEndpoint.getCxGitLabGroup()));
            cxReqPayload   = "simple=true";
            cxReqHeaders   = {
                'Authorization':             ("%s %s" % (self.cxGitLabServerEndpoint.getCxGitLabTokenType(), self.cxGitLabServerEndpoint.getCxGitLabAccessToken())),
                'Accept-Encoding':           "gzip, deflate",
                'Accept':                    "*/*",
                'Connection':                "keep-alive",
                'Content-Type':              "application/json",
                'Cache-Control':             "no-cache",
                'cache-control':             "no-cache"
                };
            cxReqRespOk    = [200];
         
            sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Param(s) of [%s] and Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqPayload, cxReqHeaders));
         
            self.asCxGitLabRestResponses.append("");
            self.asCxGitLabRestResponses.append(sOutputMsg);
         
            if self.bTraceFlag == True:
         
                print(sOutputMsg);
         
            cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, params=cxReqPayload, headers=cxReqHeaders, verify=False);
         
            sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));
         
            self.asCxGitLabRestResponses.append(sOutputMsg);
         
            if self.bTraceFlag == True:
         
                print(sOutputMsg);
            #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));
         
            if cxReqResponse.status_code in cxReqRespOk:
         
                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));
         
                self.asCxGitLabRestResponses.append(sOutputMsg);
         
                if self.bTraceFlag == True:
         
                    print(sOutputMsg);
         
            else:
         
                bProcessingError = True;
         
                sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));
         
                self.asCxGitLabRestResponses.append(sOutputMsg);
         
                print(sOutputMsg);
         
            jsonReqResponse = cxReqResponse.json();
         
            if jsonReqResponse != None:
         
                sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
                 
                if self.bTraceFlag == True:
         
                    print("");
                    print("=============== TYPE JSON Response {GitLab Group Get-ALL-Projects} ===============");
                    print((type(sReqResponseRaw)));
         
                    print("");
                    print("=============== DIR JSON Response {GitLab Group Get-ALL-Projects} ===============");
                    print((dir(sReqResponseRaw)));
         
                    print("");
                    print("=============== JSON 'string' Response {GitLab Group Get-ALL-Projects} ===============");
                    print(sReqResponseRaw);
         
                if type(sReqResponseRaw) == str:
         
                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));
         
                else:
         
                    sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));
         
                self.asCxGitLabRestResponses.append("");
                self.asCxGitLabRestResponses.append("=============== JSON 'string' Response {GitLab Group Get-ALL-Projects} ===============");
                self.asCxGitLabRestResponses.append(sOutputMsg);
                self.asCxGitLabRestResponses.append("");
                self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxGitLabRestResponses.append(sReqResponseRaw);
                self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
                self.asCxGitLabRestResponses.append("");
         
                listCxReqResponseJson = json.loads(sReqResponseRaw);
         
                if self.bTraceFlag == True:

                    print("");
                    print("=============== TYPE JSON 'list' Response {GitLab Group Get-ALL-Projects} ===============");
                    print((type(listCxReqResponseJson)));

                    print("");
                    print("=============== DIR JSON 'list' Response {GitLab Group Get-ALL-Projects} ===============");
                    print((dir(listCxReqResponseJson)));

                    print("");
                    print("=============== JSON 'list' Response {GitLab Group Get-ALL-Projects} [RAW print] ===============");
                    print(listCxReqResponseJson);

                    print("");
                    print("=============== JSON 'list' Response {GitLab Group Get-ALL-Projects} Enumerated ===============");
         
                # --------------------------------------------------------------------------------------------------
                # [
                #     {
                #         "id": 1,
                #         "description": "",
                #         "name": "JWS_App-Project_GitLab_1",
                #         "name_with_namespace": "JWebsoftwareDev / JWS_App-Project_GitLab_1",
                #         "path": "jws_app-project_gitlab_1",
                #         "path_with_namespace": "jwebsoftwaredev/jws_app-project_gitlab_1",
                #         "created_at": "2019-10-25T02:09:08.776Z",
                #         "default_branch": "master",
                #         "tag_list": [],
                #         "ssh_url_to_repo": "git@10.211.55.50:jwebsoftwaredev/jws_app-project_gitlab_1.git",
                #         "http_url_to_repo": "http://10.211.55.50/jwebsoftwaredev/jws_app-project_gitlab_1.git",
                #         "web_url": "http://10.211.55.50/jwebsoftwaredev/jws_app-project_gitlab_1",
                #         "readme_url": "http://10.211.55.50/jwebsoftwaredev/jws_app-project_gitlab_1/blob/master/README.md",
                #         "avatar_url": null,
                #         "star_count": 0,
                #         "forks_count": 0,
                #         "last_activity_at": "2019-10-25T02:09:08.776Z",
                #         "namespace": {
                #             "id": 2,
                #             "name": "JWebsoftwareDev",
                #             "path": "jwebsoftwaredev",
                #             "kind": "group",
                #             "full_path": "jwebsoftwaredev",
                #             "parent_id": null,
                #             "avatar_url": null,
                #             "web_url": "http://10.211.55.50/groups/jwebsoftwaredev"
                #         }
                #     }
                # ]
                # --------------------------------------------------------------------------------------------------
         
                if type(listCxReqResponseJson) != list:
         
                    print("");
                    print("%s JSON List response object is NOT type(list) - Error!" % (self.sClassDisp));
                    print("");
         
                    return False;
                 
                cListDictItem = 0;
             
                for dictCxReqResponseListItem in listCxReqResponseJson:
             
                    if dictCxReqResponseListItem == None:
             
                        continue;
             
                    cListDictItem += 1;
             
                    if self.bTraceFlag == True:
             
                        print(("  List Item #(%d): <raw> {%s} [%s]..." % (cListDictItem, type(dictCxReqResponseListItem), dictCxReqResponseListItem)));
             
                    cxGitLabProjectData = CxGitLabProjectData1.CxGitLabProjectData(trace=self.bTraceFlag);
     
                    bCxGitLabProjectDataPopulatedOk = cxGitLabProjectData.populateCxGitLabProjectDataFromJsonDictionary(dictcxgitlabprojectdata=dictCxReqResponseListItem);
                 
                    if bCxGitLabProjectDataPopulatedOk == True:
                 
                        self.cxGitLabProjectDataCollection.addCxGitLabProjectDataToCxGitLabProjectDataCollection(cxgitlabprojectdata=cxGitLabProjectData);

        except Exception as inst:

            print("%s 'getGitLabProjectsDataForAllProjects()' - exception occured..." % (self.sClassDisp));
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

#   def getCxGitLabProjectDetailsDataViaRestAPI(self, cxgitlabprojectdata=None):
#
#   #   self.bTraceFlag = True;
#
#       cxGitLabProjectData = cxgitlabprojectdata;
#
#       if cxGitLabProjectData == None:
#
#           print("");
#           print("%s NO CxGitLabProjectData has been specified nor defined for this request - one CxGitLabProjectData MUST be defined - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bValidateReqFieldsOk = self.validateCxGitLabProjectRequiredFields();
#
#       if bValidateReqFieldsOk == False:
#
#           print("");
#           print("%s CxGitLabProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       try:
#
#           bGetCxGitLabProjectDetailsOk = self.getGitLabProjectDetailsDataForProject(cxgitlabprojectdata=cxGitLabProjectData);
#
#           if bGetCxGitLabProjectDetailsOk == False:
#
#               print("");
#               print("%s Invocation of 'getGitLabProjectDetailsDataForProject()' failed - Error!" % (self.sClassDisp));
#               print("");
#
#               return False;
#
#           if self.bTraceFlag == True:
#
#               print("");
#               print("%s CxGitLabProjectData (after 'Get-Unique-Project-Details(s)') is:" % (self.sClassDisp));
#               print(cxGitLabProjectData.toString());
#               print("");
#
#           bGetCxGitLabProjectCollectionOk = self.getGitLabProjectCollectionDataForProject(cxgitlabprojectdata=cxGitLabProjectData);
#
#           if bGetCxGitLabProjectCollectionOk == False:
#
#               print("");
#               print("%s Invocation of 'getGitLabProjectCollectionDataForProject()' failed - Warning!" % (self.sClassDisp));
#               print("");
#
#           #   return False;
#
#           if self.bTraceFlag == True:
#
#               print("");
#               print("%s CxGitLabProjectData (after 'Get-Unique-Project-Collection') is:" % (self.sClassDisp));
#               print(cxGitLabProjectData.toString());
#               print("");
#
#           bGetCxGitLabProjectTeamOk = self.getGitLabProjectTeamDataForProject(cxgitlabprojectdata=cxGitLabProjectData);
#
#           if bGetCxGitLabProjectTeamOk == False:
#
#               print("");
#               print("%s Invocation of 'getGitLabProjectTeamDataForProject()' failed - Error!" % (self.sClassDisp));
#               print("");
#
#               return False;
#
#           if self.bTraceFlag == True:
#
#               print("");
#               print("%s CxGitLabProjectData (after 'Get-Unique-Project-Team') is:" % (self.sClassDisp));
#               print(cxGitLabProjectData.toString());
#               print("");
#
#           bGetCxGitLabProjectTeamIdentityOk = self.getGitLabProjectTeamIdentityDataForProject(cxgitlabprojectdata=cxGitLabProjectData);
#
#           if bGetCxGitLabProjectTeamIdentityOk == False:
#
#               print("");
#               print("%s Invocation of 'getGitLabProjectTeamIdentityDataForProject()' failed - Error!" % (self.sClassDisp));
#               print("");
#
#               return False;
#
#           if self.bTraceFlag == True:
#
#               print("");
#               print("%s CxGitLabProjectData (after 'Get-Unique-Project-Team-Identity') is:" % (self.sClassDisp));
#               print(cxGitLabProjectData.toString());
#               print("");
#
#           bGetCxGitLabProjectReposOk = self.getGitLabProjectReposDataForProject(cxgitlabprojectdata=cxGitLabProjectData);
#
#           if bGetCxGitLabProjectReposOk == False:
#
#               print("");
#               print("%s Invocation of 'getGitLabProjectReposDataForProject()' failed - Error!" % (self.sClassDisp));
#               print("");
#
#               return False;
#
#           if self.bTraceFlag == True:
#
#               print("");
#               print("%s CxGitLabProjectData (after 'Get-Unique-Project-(Git)-Repo(s)') is:" % (self.sClassDisp));
#               print(cxGitLabProjectData.toString());
#               print("");
#
#       except Exception as inst:
#
#           print("%s 'getCxGitLabProjectsInitialDataViaRestAPI()' - exception occured..." % (self.sClassDisp));
#           print(type(inst));
#           print(inst);
#
#           excType, excValue, excTraceback = sys.exc_info();
#           asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);
#
#           print("- - - ");
#           print('\n'.join(asTracebackLines));
#           print("- - - ");
#
#           return False;
#
#       return True;
#
#   def getGitLabProjectDetailsDataForProject(self, cxgitlabprojectdata=None):
#
#       cxGitLabProjectData = cxgitlabprojectdata;
#
#       if cxGitLabProjectData == None:
#
#           print("");
#           print("%s NO CxGitLabProjectData has been specified nor defined for this request - one CxGitLabProjectData MUST be defined - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bValidateReqFieldsOk = self.validateCxGitLabProjectRequiredFields();
#
#       if bValidateReqFieldsOk == False:
#
#           print("");
#           print("%s CxGitLabProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bProcessingError = False;
#
#       try:
#
#           CxRestAPIStatistics1.cRestAPICallsMade += 1;
#
#           cxRequestVerb  = "GET";
#           cxRequestURL   = cxGitLabProjectData.getCxProjectDetailsURL();
#           cxReqHeaders   = {
#               'Authorization':             ("Basic %s" % (self.sCxGitLabBase64UserAndPAT)),
#               'Accept-Encoding':           "gzip, deflate",
#               'Accept':                    "application/json;api-version=4.1",
#               'Connection':                "keep-alive",
#               'Content-Type':              "application/json; charset=utf-8",
#               'Cache-Control':             "no-cache",
#               'cache-control':             "no-cache"
#           #   'X-VSS-ForceMsaPassThrough': "true",
#               };
#           cxReqRespOk    = [200];
#
#           sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));
#
#           self.asCxGitLabRestResponses.append("");
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#
#           cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);
#
#           sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#           #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));
#
#           if cxReqResponse.status_code in cxReqRespOk:
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               if self.bTraceFlag == True:
#
#                   print(sOutputMsg);
#
#           else:
#
#               bProcessingError = True;
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               print(sOutputMsg);
#
#           jsonReqResponse = cxReqResponse.json();
#
#           if jsonReqResponse != None:
#
#               sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
#
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON Response {GitLab Get-Unique-Project-Details} ===============");
#                   print((type(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== DIR JSON Response {GitLab Get-Unique-Project-Details} ===============");
#                   print((dir(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== JSON 'string' Response {GitLab Get-Unique-Project-Details} ===============");
#                   print(sReqResponseRaw);
#
#               if type(sReqResponseRaw) == str:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));
#
#               else:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));
#
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append("=============== JSON 'string' Response {GitLab Get-Unique-Project-Details} ===============");
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append(sReqResponseRaw);
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append("");
#
#               dictCxReqResponseJson = json.loads(sReqResponseRaw);
#
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON 'dictionary' Response {GitLab Get-Unique-Project-Details} ===============");
#                   print((type(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== DIR JSON 'dictionary' Response {GitLab Get-Unique-Project-Details} ===============");
#                   print((dir(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Details} [RAW print] ===============");
#                   print(dictCxReqResponseJson);
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Details} Enumerated ===============");
#
#               # --------------------------------------------------------------------------------------------------
#               # {
#               #  "id": "705ff45a-11cf-406d-8e04-823aff3b3ab6",
#               #  "name": "GitLabSampleProject1",
#               #  "url": "http://10.211.55.50:80/gitlab/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6",
#               #  "state": "wellFormed",
#               #  "revision": 8,
#               #  "_links": {
#               #   "self": {
#               #    "href": "http://10.211.55.50:80/gitlab/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6"
#               #   },
#               #   "collection": {
#               #    "href": "http://10.211.55.50:80/gitlab/_apis/projectCollections/1ea0178e-6700-4742-9ff8-a4f77af995bf"
#               #   },
#               #   "web": {
#               #    "href": "http://darylc-laptop:80/gitlab/DefaultCollection/GitLabSampleProject1"
#               #   }
#               #  },
#               #  "visibility": "private",
#               #  "defaultTeam": {
#               #    "id": "ec3de804-b8b2-463f-a963-27453ce09273",
#               #    "name": "GitLabSampleProject1 Team",
#               #    "url": "http://10.211.55.50:80/gitlab/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6/teams/ec3de804-b8b2-463f-a963-27453ce09273"
#               #  }
#               # }
#               # --------------------------------------------------------------------------------------------------
#
#               if type(dictCxReqResponseJson) != dict:
#
#                   print("");
#                   print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
#                   print("");
#
#                   return False;
#
#               cDictJsonItem = 0;
#
#               for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):
#
#                   if dictCxReqResponseJsonKey == None:
#
#                       continue;
#
#                   cDictJsonItem += 1;
#
#                   dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];
#
#                   if self.bTraceFlag == True:
#
#                       print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));
#
#                       if type(dictCxReqResponseJsonItem) == dict:
#
#                           dictSubItem  = dictCxReqResponseJsonItem;
#                           cDictSubItem = 0;
#
#                           for sDictItemKey in dictSubItem.keys():
#
#                               cDictSubItem += 1;
#
#                               objDictItemValue = dictSubItem[sDictItemKey];
#
#                               print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));
#
#                       else:
#
#                           if type(dictCxReqResponseJsonItem) == list:
#
#                               listSubItems = dictCxReqResponseJsonItem;
#                               cListSubItem = 0;
#
#                               for objListSubItem in listSubItems:
#
#                                   cListSubItem += 1;
#
#                                   print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));
#
#                   if dictCxReqResponseJsonKey != "_links" and \
#                      dictCxReqResponseJsonKey != "defaultTeam":
#
#                       continue;
#
#                   dictCxReqResponseDetails = dictCxReqResponseJsonItem;
#
#                   if self.bTraceFlag == True:
#
#                       print("");
#                       print("=============== TYPE JSON 'dict' Response {GitLab Get-Unique-Project-Details} ===============");
#                       print((type(dictCxReqResponseDetails)));
#
#                       print("");
#                       print("=============== DIR JSON 'dict' Response {GitLab Get-Unique-Project-Details} ===============");
#                       print((dir(dictCxReqResponseDetails)));
#
#                       print("");
#                       print("=============== JSON 'dict' Response {GitLab Get-Unique-Project-Details} [RAW print] ===============");
#                       print(dictCxReqResponseDetails);
#
#                       print("");
#                       print("=============== JSON 'dict' Response {GitLab Get-Unique-Project-Details} Enumerated ===============");
#
#                   if dictCxReqResponseJsonKey != "_links":
#
#                       cxGitLabProjectData.setCxProjectLinks(cxprojectlinks=dictCxReqResponseDetails);
#
#                   if dictCxReqResponseJsonKey != "defaultTeam":
#
#                       cxGitLabProjectData.setCxProjectDefaultTeam(cxprojectdefaultteam=dictCxReqResponseDetails);
#
#                   cDictItemDetails = 0;
#
#                   for dictCxReqResponseDetailsItem in dictCxReqResponseDetails:
#
#                       if dictCxReqResponseDetailsItem == None:
#
#                           continue;
#
#                       cDictItemDetails += 1;
#
#                       if self.bTraceFlag == True:
#
#                           print(("  Dict Item #(%d): <raw> {%s} [%s]..." % (cDictItemDetails, type(dictCxReqResponseDetailsItem), dictCxReqResponseDetailsItem)));
#
#                       if dictCxReqResponseJsonKey == "_links":
#
#                           if dictCxReqResponseDetailsItem == "collection":
#
#                               dictProjDetailsCollection = dictCxReqResponseDetails["collection"];
#
#                               cxGitLabProjectData.setCxProjectGroupURL(cxprojectcollectionurl=dictProjDetailsCollection["href"]);
#
#                       if dictCxReqResponseJsonKey == "defaultTeam":
#
#                           if dictCxReqResponseDetailsItem == "id":
#
#                               sProjDefaultTeamId = dictCxReqResponseDetails["id"];
#
#                               cxGitLabProjectData.setCxProjectTeamId(cxprojectteamid=sProjDefaultTeamId);
#
#                           if dictCxReqResponseDetailsItem == "name":
#
#                               sProjDefaultTeamName = dictCxReqResponseDetails["name"];
#
#                               cxGitLabProjectData.setCxProjectTeamName(cxprojectteamname=sProjDefaultTeamName);
#
#                           if dictCxReqResponseDetailsItem == "url":
#
#                               sProjDefaultTeamURL = dictCxReqResponseDetails["url"];
#
#                               cxGitLabProjectData.setCxProjectTeamURL(cxprojectteamurl=sProjDefaultTeamURL);
#
#       except Exception as inst:
#
#           print("%s 'getGitLabProjectDetailsDataForProject()' - exception occured..." % (self.sClassDisp));
#           print(type(inst));
#           print(inst);
#
#           excType, excValue, excTraceback = sys.exc_info();
#           asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);
#
#           print("- - - ");
#           print('\n'.join(asTracebackLines));
#           print("- - - ");
#
#           return False;
#
#       if bProcessingError == True:
#
#           return False;
#
#       return True;
#
#   def getGitLabProjectCollectionDataForProject(self, cxgitlabprojectdata=None):
#
#       cxGitLabProjectData = cxgitlabprojectdata;
#
#       if cxGitLabProjectData == None:
#
#           print("");
#           print("%s NO CxGitLabProjectData has been specified nor defined for this request - one CxGitLabProjectData MUST be defined - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bValidateReqFieldsOk = self.validateCxGitLabProjectRequiredFields();
#
#       if bValidateReqFieldsOk == False:
#
#           print("");
#           print("%s CxGitLabProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bProcessingError = False;
#
#       try:
#
#           CxRestAPIStatistics1.cRestAPICallsMade += 1;
#
#           cxRequestVerb  = "GET";
#           cxRequestURL   = cxGitLabProjectData.getCxProjectGroupURL();
#           cxReqHeaders   = {
#               'Authorization':             ("Basic %s" % (self.sCxGitLabBase64UserAndPAT)),
#               'Accept-Encoding':           "gzip, deflate",
#               'Accept':                    "application/json;api-version=4.1",
#               'Connection':                "keep-alive",
#               'Content-Type':              "application/json; charset=utf-8",
#               'Cache-Control':             "no-cache",
#               'cache-control':             "no-cache"
#           #   'X-VSS-ForceMsaPassThrough': "true",
#               };
#           cxReqRespOk    = [200];
#
#           sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));
#
#           self.asCxGitLabRestResponses.append("");
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#
#           cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);
#
#           sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#           #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));
#
#           if cxReqResponse.status_code in cxReqRespOk:
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               if self.bTraceFlag == True:
#
#                   print(sOutputMsg);
#
#           else:
#
#               bProcessingError = True;
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               print(sOutputMsg);
#
#           jsonReqResponse = cxReqResponse.json();
#
#           if jsonReqResponse != None:
#
#               sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
#
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON Response {GitLab Get-Unique-Project-Collection} ===============");
#                   print((type(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== DIR JSON Response {GitLab Get-Unique-Project-Collection} ===============");
#                   print((dir(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== JSON 'string' Response {GitLab Get-Unique-Project-Collection} ===============");
#                   print(sReqResponseRaw);
#
#               if type(sReqResponseRaw) == str:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));
#
#               else:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));
#
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append("=============== JSON 'string' Response {GitLab Get-Unique-Project-Collection} ===============");
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append(sReqResponseRaw);
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append("");
#
#               dictCxReqResponseJson = json.loads(sReqResponseRaw);
#
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON 'dictionary' Response {GitLab Get-Unique-Project-Collection} ===============");
#                   print((type(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== DIR JSON 'dictionary' Response {GitLab Get-Unique-Project-Collection} ===============");
#                   print((dir(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Collection} [RAW print] ===============");
#                   print(dictCxReqResponseJson);
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Collection} Enumerated ===============");
#
#               # --------------------------------------------------------------------------------------------------
#               # {
#               #  "id": "1ea0178e-6700-4742-9ff8-a4f77af995bf",
#               #  "name": "DefaultCollection",
#               #  "url": "http://10.211.55.50:80/gitlab/_apis/projectCollections/1ea0178e-6700-4742-9ff8-a4f77af995bf",
#               #  "state": "Started",
#               #  "_links": {
#               #   "self": {
#               #    "href": "http://10.211.55.50:80/gitlab/_apis/projectCollections/1ea0178e-6700-4742-9ff8-a4f77af995bf"
#               #   },
#               #   "web": {
#               #    "href": "http://darylc-laptop:80/gitlab/DefaultCollection/"
#               #   }
#               #  }
#               # }
#               # --------------------------------------------------------------------------------------------------
#
#               if type(dictCxReqResponseJson) != dict:
#
#                   print("");
#                   print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
#                   print("");
#
#                   return False;
#
#               cxGitLabProjectData.setCxProjectCollection(cxprojectcollection=dictCxReqResponseJson);
#
#               cDictJsonItem = 0;
#
#               for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):
#
#                   if dictCxReqResponseJsonKey == None:
#
#                       continue;
#
#                   cDictJsonItem += 1;
#
#                   dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];
#
#                   if self.bTraceFlag == True:
#
#                       print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));
#
#                       if type(dictCxReqResponseJsonItem) == dict:
#
#                           dictSubItem  = dictCxReqResponseJsonItem;
#                           cDictSubItem = 0;
#
#                           for sDictItemKey in dictSubItem.keys():
#
#                               cDictSubItem += 1;
#
#                               objDictItemValue = dictSubItem[sDictItemKey];
#
#                               print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));
#
#                       else:
#
#                           if type(dictCxReqResponseJsonItem) == list:
#
#                               listSubItems = dictCxReqResponseJsonItem;
#                               cListSubItem = 0;
#
#                               for objListSubItem in listSubItems:
#
#                                   cListSubItem += 1;
#
#                                   print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));
#
#       except Exception as inst:
#
#           print("%s 'getGitLabProjectCollectionDataForProject()' - exception occured..." % (self.sClassDisp));
#           print(type(inst));
#           print(inst);
#
#           excType, excValue, excTraceback = sys.exc_info();
#           asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);
#
#           print("- - - ");
#           print('\n'.join(asTracebackLines));
#           print("- - - ");
#
#           return False;
#
#       if bProcessingError == True:
#
#           return False;
#
#       return True;
#
#   def getGitLabProjectTeamDataForProject(self, cxgitlabprojectdata=None):
#
#       cxGitLabProjectData = cxgitlabprojectdata;
#
#       if cxGitLabProjectData == None:
#
#           print("");
#           print("%s NO CxGitLabProjectData has been specified nor defined for this request - one CxGitLabProjectData MUST be defined - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bValidateReqFieldsOk = self.validateCxGitLabProjectRequiredFields();
#
#       if bValidateReqFieldsOk == False:
#
#           print("");
#           print("%s CxGitLabProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bProcessingError = False;
#
#       try:
#
#           CxRestAPIStatistics1.cRestAPICallsMade += 1;
#
#           cxRequestVerb  = "GET";
#           cxRequestURL   = cxGitLabProjectData.getCxProjectTeamURL();
#           cxReqHeaders   = {
#               'Authorization':             ("Basic %s" % (self.sCxGitLabBase64UserAndPAT)),
#               'Accept-Encoding':           "gzip, deflate",
#               'Accept':                    "application/json;api-version=4.1",
#               'Connection':                "keep-alive",
#               'Content-Type':              "application/json; charset=utf-8",
#               'Cache-Control':             "no-cache",
#               'cache-control':             "no-cache"
#           #   'X-VSS-ForceMsaPassThrough': "true",
#               };
#           cxReqRespOk    = [200];
#
#           sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));
#
#           self.asCxGitLabRestResponses.append("");
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#
#           cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);
#
#           sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#           #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));
#
#           if cxReqResponse.status_code in cxReqRespOk:
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               if self.bTraceFlag == True:
#
#                   print(sOutputMsg);
#
#           else:
#
#               bProcessingError = True;
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               print(sOutputMsg);
#
#           jsonReqResponse = cxReqResponse.json();
#
#           if jsonReqResponse != None:
#
#               sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
#
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON Response {GitLab Get-Unique-Project-Team} ===============");
#                   print((type(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== DIR JSON Response {GitLab Get-Unique-Project-Team} ===============");
#                   print((dir(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== JSON 'string' Response {GitLab Get-Unique-Project-Team} ===============");
#                   print(sReqResponseRaw);
#
#               if type(sReqResponseRaw) == str:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));
#
#               else:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));
#
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append("=============== JSON 'string' Response {GitLab Get-Unique-Project-Team} ===============");
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append(sReqResponseRaw);
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append("");
#
#               dictCxReqResponseJson = json.loads(sReqResponseRaw);
#
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON 'dictionary' Response {GitLab Get-Unique-Project-Team} ===============");
#                   print((type(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== DIR JSON 'dictionary' Response {GitLab Get-Unique-Project-Team} ===============");
#                   print((dir(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Team} [RAW print] ===============");
#                   print(dictCxReqResponseJson);
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Team} Enumerated ===============");
#
#               # --------------------------------------------------------------------------------------------------
#               # {
#               #  "id": "ec3de804-b8b2-463f-a963-27453ce09273",
#               #  "name": "GitLabSampleProject1 Team",
#               #  "url": "http://10.211.55.50:80/gitlab/DefaultCollection/_apis/projects/705ff45a-11cf-406d-8e04-823aff3b3ab6/teams/ec3de804-b8b2-463f-a963-27453ce09273",
#               #  "description": "The default project team.",
#               #  "identityUrl": "http://10.211.55.50:80/gitlab/DefaultCollection/_apis/Identities/ec3de804-b8b2-463f-a963-27453ce09273",
#               #  "projectName": "GitLabSampleProject1",
#               #  "projectId": "705ff45a-11cf-406d-8e04-823aff3b3ab6"
#               # }
#               # --------------------------------------------------------------------------------------------------
#
#               if type(dictCxReqResponseJson) != dict:
#
#                   print("");
#                   print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
#                   print("");
#
#                   return False;
#
#               cxGitLabProjectData.setCxProjectTeam(cxprojectteam=dictCxReqResponseJson);
#
#               cDictJsonItem = 0;
#
#               for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):
#
#                   if dictCxReqResponseJsonKey == None:
#
#                       continue;
#
#                   cDictJsonItem += 1;
#
#                   dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];
#
#                   if self.bTraceFlag == True:
#
#                       print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));
#
#                       if type(dictCxReqResponseJsonItem) == dict:
#
#                           dictSubItem  = dictCxReqResponseJsonItem;
#                           cDictSubItem = 0;
#
#                           for sDictItemKey in dictSubItem.keys():
#
#                               cDictSubItem += 1;
#
#                               objDictItemValue = dictSubItem[sDictItemKey];
#
#                               print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));
#
#                       else:
#
#                           if type(dictCxReqResponseJsonItem) == list:
#
#                               listSubItems = dictCxReqResponseJsonItem;
#                               cListSubItem = 0;
#
#                               for objListSubItem in listSubItems:
#
#                                   cListSubItem += 1;
#
#                                   print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));
#
#                   if dictCxReqResponseJsonKey == "description":
#
#                       cxGitLabProjectData.setCxProjectTeamDescription(cxprojectteamdescription=dictCxReqResponseJsonItem);
#
#                   if dictCxReqResponseJsonKey == "identityUrl":
#
#                       cxGitLabProjectData.setCxProjectTeamIdentityURL(cxprojectteamidentityurl=dictCxReqResponseJsonItem);
#
#                   if dictCxReqResponseJsonKey == "projectName":
#
#                       cxGitLabProjectData.setCxProjectTeamProjectName(cxprojectteamprojectname=dictCxReqResponseJsonItem);
#
#                   if dictCxReqResponseJsonKey == "projectId":
#
#                       cxGitLabProjectData.setCxProjectTeamProjectId(cxprojectteamprojectid=dictCxReqResponseJsonItem);
#
#       except Exception as inst:
#
#           print("%s 'getGitLabProjectTeamDataForProject()' - exception occured..." % (self.sClassDisp));
#           print(type(inst));
#           print(inst);
#
#           excType, excValue, excTraceback = sys.exc_info();
#           asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);
#
#           print("- - - ");
#           print('\n'.join(asTracebackLines));
#           print("- - - ");
#
#           return False;
#
#       if bProcessingError == True:
#
#           return False;
#
#       return True;
#
#   def getGitLabProjectTeamIdentityDataForProject(self, cxgitlabprojectdata=None):
#
#       cxGitLabProjectData = cxgitlabprojectdata;
#
#       if cxGitLabProjectData == None:
#
#           print("");
#           print("%s NO CxGitLabProjectData has been specified nor defined for this request - one CxGitLabProjectData MUST be defined - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bValidateReqFieldsOk = self.validateCxGitLabProjectRequiredFields();
#
#       if bValidateReqFieldsOk == False:
#
#           print("");
#           print("%s CxGitLabProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bProcessingError = False;
#
#       try:
#
#           CxRestAPIStatistics1.cRestAPICallsMade += 1;
#
#           cxRequestVerb  = "GET";
#           cxRequestURL   = cxGitLabProjectData.getCxProjectTeamIdentityURL();
#           cxReqHeaders   = {
#               'Authorization':             ("Basic %s" % (self.sCxGitLabBase64UserAndPAT)),
#               'Accept-Encoding':           "gzip, deflate",
#               'Accept':                    "application/json;api-version=4.1",
#               'Connection':                "keep-alive",
#               'Content-Type':              "application/json; charset=utf-8",
#               'Cache-Control':             "no-cache",
#               'cache-control':             "no-cache"
#           #   'X-VSS-ForceMsaPassThrough': "true",
#               };
#           cxReqRespOk    = [200];
#
#           sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));
#
#           self.asCxGitLabRestResponses.append("");
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#
#           cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);
#
#           sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#           #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));
#
#           if cxReqResponse.status_code in cxReqRespOk:
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               if self.bTraceFlag == True:
#
#                   print(sOutputMsg);
#
#           else:
#
#               bProcessingError = True;
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               print(sOutputMsg);
#
#           jsonReqResponse = cxReqResponse.json();
#
#           if jsonReqResponse != None:
#
#               sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
#
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON Response {GitLab Get-Unique-Project-Team-Identity} ===============");
#                   print((type(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== DIR JSON Response {GitLab Get-Unique-Project-Team-Identity} ===============");
#                   print((dir(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== JSON 'string' Response {GitLab Get-Unique-Project-Team-Identity} ===============");
#                   print(sReqResponseRaw);
#
#               if type(sReqResponseRaw) == str:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));
#
#               else:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));
#
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append("=============== JSON 'string' Response {GitLab Get-Unique-Project-Team-Identity} ===============");
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append(sReqResponseRaw);
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append("");
#
#               dictCxReqResponseJson = json.loads(sReqResponseRaw);
#
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON 'dictionary' Response {GitLab Get-Unique-Project-Team-Identity} ===============");
#                   print((type(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== DIR JSON 'dictionary' Response {GitLab Get-Unique-Project-Team-Identity} ===============");
#                   print((dir(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Team-Identity} [RAW print] ===============");
#                   print(dictCxReqResponseJson);
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Team-Identity} Enumerated ===============");
#
#               # --------------------------------------------------------------------------------------------------
#               # {
#               #     "id": "ec3de804-b8b2-463f-a963-27453ce09273",
#               #     "descriptor": "Microsoft.TeamFoundation.Identity;S-1-9-1551374245-4263824929-2983495753-2170576692-487292674-1-192998105-199977285-2515143924-823569469",
#               #     "providerDisplayName": "[GitLabSampleProject1]\\GitLabSampleProject1 Team",
#               #     "isActive": true,
#               #     "isContainer": true,
#               #     "members": [],
#               #     "memberOf": [],
#               #     "memberIds": [],
#               #     "masterId": "ffffffff-ffff-ffff-ffff-ffffffffffff",
#               #     "properties": {
#               #         "SchemaClassName": {
#               #             "$type": "System.String",
#               #             "$value": "Group"
#               #         },
#               #         "Description": {
#               #             "$type": "System.String",
#               #             "$value": "The default project team."
#               #         },
#               #         "Domain": {
#               #             "$type": "System.String",
#               #             "$value": "vsgitlab:///Classification/TeamProject/705ff45a-11cf-406d-8e04-823aff3b3ab6"
#               #         },
#               #         "Account": {
#               #             "$type": "System.String",
#               #             "$value": "GitLabSampleProject1 Team"
#               #         },
#               #         "SecurityGroup": {
#               #             "$type": "System.String",
#               #             "$value": "SecurityGroup"
#               #         },
#               #         "SpecialType": {
#               #             "$type": "System.String",
#               #             "$value": "Generic"
#               #         },
#               #         "ScopeId": {
#               #             "$type": "System.Guid",
#               #             "$value": "21ce24fe-d4b1-4988-8160-5f341d0b7f02"
#               #         },
#               #         "ScopeType": {
#               #             "$type": "System.String",
#               #             "$value": "TeamProject"
#               #         },
#               #         "LocalScopeId": {
#               #             "$type": "System.Guid",
#               #             "$value": "705ff45a-11cf-406d-8e04-823aff3b3ab6"
#               #         },
#               #         "SecuringHostId": {
#               #             "$type": "System.Guid",
#               #             "$value": "1ea0178e-6700-4742-9ff8-a4f77af995bf"
#               #         },
#               #         "ScopeName": {
#               #             "$type": "System.String",
#               #             "$value": "GitLabSampleProject1"
#               #         },
#               #         "VirtualPlugin": {
#               #             "$type": "System.String",
#               #             "$value": ""
#               #         }
#               #     },
#               #     "resourceVersion": 2,
#               #     "metaTypeId": 255
#               # }
#               # --------------------------------------------------------------------------------------------------
#
#               if type(dictCxReqResponseJson) != dict:
#
#                   print("");
#                   print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
#                   print("");
#
#                   return False;
#
#               cxGitLabProjectData.setCxProjectTeamIdentity(cxprojectteamidentity=dictCxReqResponseJson);
#
#               cDictJsonItem = 0;
#
#               for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):
#
#                   if dictCxReqResponseJsonKey == None:
#
#                       continue;
#
#                   cDictJsonItem += 1;
#
#                   dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];
#
#                   if self.bTraceFlag == True:
#
#                       print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));
#
#                       if type(dictCxReqResponseJsonItem) == dict:
#
#                           dictSubItem  = dictCxReqResponseJsonItem;
#                           cDictSubItem = 0;
#
#                           for sDictItemKey in dictSubItem.keys():
#
#                               cDictSubItem += 1;
#
#                               objDictItemValue = dictSubItem[sDictItemKey];
#
#                               print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));
#
#                       else:
#
#                           if type(dictCxReqResponseJsonItem) == list:
#
#                               listSubItems = dictCxReqResponseJsonItem;
#                               cListSubItem = 0;
#
#                               for objListSubItem in listSubItems:
#
#                                   cListSubItem += 1;
#
#                                   print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));
#
#       except Exception as inst:
#
#           print("%s 'getGitLabProjectTeamIdentityDataForProject()' - exception occured..." % (self.sClassDisp));
#           print(type(inst));
#           print(inst);
#
#           excType, excValue, excTraceback = sys.exc_info();
#           asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);
#
#           print("- - - ");
#           print('\n'.join(asTracebackLines));
#           print("- - - ");
#
#           return False;
#
#       if bProcessingError == True:
#
#           return False;
#
#       return True;
#
#   def getGitLabProjectReposDataForProject(self, cxgitlabprojectdata=None):
#
#       cxGitLabProjectData = cxgitlabprojectdata;
#
#       if cxGitLabProjectData == None:
#
#           print("");
#           print("%s NO CxGitLabProjectData has been specified nor defined for this request - one CxGitLabProjectData MUST be defined - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       bProcessingError = False;
#
#       bValidateReqFieldsOk = self.validateCxGitLabProjectRequiredFields();
#
#       if bValidateReqFieldsOk == False:
#
#           print("");
#           print("%s CxGitLabProject 'required' field(s) failed to 'validate' - Error!" % (self.sClassDisp));
#           print("");
#
#           return False;
#
#       try:
#
#           CxRestAPIStatistics1.cRestAPICallsMade += 1;
#
#           cxRequestVerb  = "GET";
#           cxRequestURL = ("%s/gitlab/%s/%s/_apis/git/repositories?api-version=1" % (self.sCxGitLabServerURL, self.cxGitLabProjectDataCollection.getCxGitLabCollectionName(), cxGitLabProjectData.getCxProjectName()));
#           cxReqHeaders   = {
#               'Authorization':             ("Basic %s" % (self.sCxGitLabBase64UserAndPAT)),
#               'Accept-Encoding':           "gzip, deflate",
#               'Accept':                    "application/json;api-version=1",
#               'Connection':                "keep-alive",
#               'Content-Type':              "application/json; charset=utf-8",
#               'Cache-Control':             "no-cache",
#               'cache-control':             "no-cache"
#           #   'X-VSS-ForceMsaPassThrough': "true",
#               };
#           cxReqRespOk    = [200];
#
#           sOutputMsg = ("%s Issuing Request #(%d) for a [%s] of URL [%s] with Header(s) of [%s]..." % (self.sClassDisp, CxRestAPIStatistics1.cRestAPICallsMade, cxRequestVerb, cxRequestURL, cxReqHeaders));
#
#           self.asCxGitLabRestResponses.append("");
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#
#           cxReqResponse = requests.request(cxRequestVerb, cxRequestURL, headers=cxReqHeaders, verify=False);
#
#           sOutputMsg = ("%s The URL [%s] Request returned a 'status' code of [%s] Type [%s]..." % (self.sClassDisp, cxRequestVerb, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#           self.asCxGitLabRestResponses.append(sOutputMsg);
#
#           if self.bTraceFlag == True:
#
#               print(sOutputMsg);
#           #   print("%s The URL Response is [%s]..." % (cxReqResponse.text));
#
#           if cxReqResponse.status_code in cxReqRespOk:
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code)));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               if self.bTraceFlag == True:
#
#                   print(sOutputMsg);
#
#           else:
#
#               bProcessingError = True;
#
#               sOutputMsg = ("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.sClassDisp, cxReqResponse.status_code, type(cxReqResponse.status_code), cxReqRespOk));
#
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#
#               print(sOutputMsg);
#
#           jsonReqResponse = cxReqResponse.json();
#
#           if jsonReqResponse != None:
#
#               sReqResponseRaw = json.dumps(cxReqResponse.json(), indent=4);
#                
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON Response {GitLab Get-Unique-Project-Repos} ===============");
#                   print((type(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== DIR JSON Response {GitLab Get-Unique-Project-Repos} ===============");
#                   print((dir(sReqResponseRaw)));
#
#                   print("");
#                   print("=============== JSON 'string' Response {GitLab Get-Unique-Project-Repos} ===============");
#                   print(sReqResponseRaw);
#
#               if type(sReqResponseRaw) == str:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw)));
#
#               else:
#
#                   sOutputMsg = ("%s The JSON Response: LEN (%d) - TYPE [%s] - DIR [%s]..." % (self.sClassDisp, len(sReqResponseRaw), type(sReqResponseRaw), dir(sReqResponseRaw)));
#
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append("=============== JSON 'string' Response {GitLab Get-Unique-Project-Repos} ===============");
#               self.asCxGitLabRestResponses.append(sOutputMsg);
#               self.asCxGitLabRestResponses.append("");
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append(sReqResponseRaw);
#               self.asCxGitLabRestResponses.append(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
#               self.asCxGitLabRestResponses.append("");
#
#               dictCxReqResponseJson = json.loads(sReqResponseRaw);
#
#               if self.bTraceFlag == True:
#
#                   print("");
#                   print("=============== TYPE JSON 'dictionary' Response {GitLab Get-Unique-Project-Repos} ===============");
#                   print((type(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== DIR JSON 'dictionary' Response {GitLab Get-Unique-Project-Repos} ===============");
#                   print((dir(dictCxReqResponseJson)));
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Repos} [RAW print] ===============");
#                   print(dictCxReqResponseJson);
#
#                   print("");
#                   print("=============== JSON 'dictionary' Response {GitLab Get-Unique-Project-Repos} Enumerated ===============");
#
#               # --------------------------------------------------------------------------------------------------
#               # {
#               #     "value": [
#               #         {
#               #             "id": "6f23a004-735a-4df6-909b-17571d9f06b1",
#               #             "name": "JWS_App-Project_1",
#               #             "url": "http://10.211.55.50:80/gitlab/JWebsoftwareDev/_apis/git/repositories/6f23a004-735a-4df6-909b-17571d9f06b1",
#               #             "project": {
#               #                 "id": "dc408339-e04f-4582-9b50-65e9182fcb3a",
#               #                 "name": "JWS_App-Project_1",
#               #                 "description": "JWS_App-Project_1 description",
#               #                 "url": "http://10.211.55.50:80/gitlab/JWebsoftwareDev/_apis/projects/dc408339-e04f-4582-9b50-65e9182fcb3a",
#               #                 "state": "wellFormed",
#               #                 "revision": 9,
#               #                 "visibility": "private"
#               #             },
#               #             "defaultBranch": "refs/heads/master",
#               #             "remoteUrl": "http://darylc-laptop:80/gitlab/JWebsoftwareDev/_git/JWS_App-Project_1",
#               #             "sshUrl": "ssh://darylc-laptop:22/gitlab/JWebsoftwareDev/_git/JWS_App-Project_1"
#               #         }
#               #     ],
#               #     "count": 1
#               # }
#               # --------------------------------------------------------------------------------------------------
#
#               if type(dictCxReqResponseJson) != dict:
#
#                   print("");
#                   print("%s JSON Dictionary response object is NOT type(dict) - Error!" % (self.sClassDisp));
#                   print("");
#
#                   return False;
#
#               cDictJsonItem = 0;
#
#               for dictCxReqResponseJsonKey in list(dictCxReqResponseJson.keys()):
#
#                   if dictCxReqResponseJsonKey == None:
#
#                       continue;
#
#                   cDictJsonItem += 1;
#
#                   dictCxReqResponseJsonItem = dictCxReqResponseJson[dictCxReqResponseJsonKey];
#
#                   if self.bTraceFlag == True:
#
#                       print(("  Item #(%d): '%s' [%s]..." % (cDictJsonItem, dictCxReqResponseJsonKey, dictCxReqResponseJsonItem)));
#
#                       if type(dictCxReqResponseJsonItem) == dict:
#
#                           dictSubItem  = dictCxReqResponseJsonItem;
#                           cDictSubItem = 0;
#
#                           for sDictItemKey in dictSubItem.keys():
#
#                               cDictSubItem += 1;
#
#                               objDictItemValue = dictSubItem[sDictItemKey];
#
#                               print("    DICT Item #(%d) of (%d) 'sDictItemKey' Type [%s] is [%s] 'objDictItemValue' Type [%s] is [%s]:" % (cDictSubItem, len(dictSubItem), type(sDictItemKey), sDictItemKey, type(objDictItemValue), objDictItemValue));
#
#                       else:
#
#                           if type(dictCxReqResponseJsonItem) == list:
#
#                               listSubItems = dictCxReqResponseJsonItem;
#                               cListSubItem = 0;
#
#                               for objListSubItem in listSubItems:
#
#                                   cListSubItem += 1;
#
#                                   print("    LIST Item #(%d) of (%d) 'objListSubItem' Type [%s] is [%s]..." % (cListSubItem, len(listSubItems), type(objListSubItem), objListSubItem));
#
#                   if dictCxReqResponseJsonKey != "value":
#
#                       continue;
#
#                   listCxReqResponseJson = dictCxReqResponseJsonItem;
#                
#                   if self.bTraceFlag == True:
#                
#                       print("");
#                       print("=============== TYPE JSON 'list' Response {GitLab Get-Unique-Project-Repos} ===============");
#                       print((type(listCxReqResponseJson)));
#                
#                       print("");
#                       print("=============== DIR JSON 'list' Response {GitLab Get-Unique-Project-Repos} ===============");
#                       print((dir(listCxReqResponseJson)));
#                
#                       print("");
#                       print("=============== JSON 'list' Response {GitLab Get-Unique-Project-Repos} [RAW print] ===============");
#                       print(listCxReqResponseJson);
#                
#                       print("");
#                       print("=============== JSON 'list' Response {GitLab Get-Unique-Project-Repos} Enumerated ===============");
#
#                   cxGitLabProjectData.setCxProjectRepos(cxprojectrepos=listCxReqResponseJson);
#                
#                   cListDictItem = 0;
#                
#                   for dictCxReqResponseListItem in listCxReqResponseJson:
#                
#                       if dictCxReqResponseListItem == None:
#                
#                           continue;
#                
#                       cListDictItem += 1;
#                
#                       if self.bTraceFlag == True:
#                
#                           print(("  List Item #(%d): <raw> {%s} [%s]..." % (cListDictItem, type(dictCxReqResponseListItem), dictCxReqResponseListItem)));
#                
#       except Exception as inst:
#
#           print("%s 'getGitLabProjectReposDataForProject()' - exception occured..." % (self.sClassDisp));
#           print(type(inst));
#           print(inst);
#
#           excType, excValue, excTraceback = sys.exc_info();
#           asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);
#
#           print("- - - ");
#           print('\n'.join(asTracebackLines));
#           print("- - - ");
#
#           return False;
#
#       if bProcessingError == True:
#
#           return False;
#
#       return True;
#
