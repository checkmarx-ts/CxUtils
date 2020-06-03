
import os;
import traceback;
import re;
import string;
import sys;
import collections;

class CxGitLabProjectData(object):

    sClassMod                      = __name__;
    sClassId                       = "CxGitLabProjectData";
    sClassVers                     = "(v1.0212)";
    sClassDisp                     = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                     = False;

    sCxGitLabProjectId             = None;
    sCxGitLabProjectName           = None;
    sCxGitLabProjectGroupName      = None;
    sCxGitLabProjectRepoBranchName = None;
    sCxGitLabProjectRepoHttpURL    = None;
    sCxGitLabProjectRepoSshURL     = None;

    def __init__(self, trace=False, cxgitlabprojectid=0, cxgitlabprojectname=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxGitLabProjectId(cxgitlabprojectid=cxgitlabprojectid);
            self.setCxGitLabProjectName(cxgitlabprojectname=cxgitlabprojectname);

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

    def getCxGitLabProjectId(self):

        return self.sCxGitLabProjectId;

    def setCxGitLabProjectId(self, cxgitlabprojectid=None):

        if cxgitlabprojectid == None:

            return;

        if type(cxgitlabprojectid) == str:

            self.sCxGitLabProjectId = cxgitlabprojectid;

            if self.sCxGitLabProjectId != None:

                self.sCxGitLabProjectId = self.sCxGitLabProjectId.strip();

            if self.sCxGitLabProjectId == None or \
               len(self.sCxGitLabProjectId) < 1:

                self.sCxGitLabProjectId = "";

        else:

            iCxGitLabProjectId = cxgitlabprojectid;

            if iCxGitLabProjectId < 0:

                self.sCxGitLabProjectId = "";

            else:

                self.sCxGitLabProjectId = ("%d" % iCxGitLabProjectId);

    def getCxGitLabProjectName(self):

        return self.sCxGitLabProjectName;

    def setCxGitLabProjectName(self, cxgitlabprojectname=None):

        self.sCxGitLabProjectName = cxgitlabprojectname;

        if self.sCxGitLabProjectName == None or \
           len(self.sCxGitLabProjectName) < 1:

            self.sCxGitLabProjectName = None;

    def getCxGitLabProjectGroupName(self):

        return self.sCxGitLabProjectGroupName;

    def setCxGitLabProjectGroupName(self, cxgitlabprojectgroupname=None):

        self.sCxGitLabProjectGroupName = cxgitlabprojectgroupname;

        if self.sCxGitLabProjectGroupName == None or \
           len(self.sCxGitLabProjectGroupName) < 1:

            self.sCxGitLabProjectGroupName = None;

    def getCxGitLabProjectRepoBranchName(self):

        return self.sCxGitLabProjectRepoBranchName;

    def setCxGitLabProjectRepoBranchName(self, cxgitlabprojectrepobranchname=None):

        self.sCxGitLabProjectRepoBranchName = cxgitlabprojectrepobranchname;

        if self.sCxGitLabProjectRepoBranchName == None or \
           len(self.sCxGitLabProjectRepoBranchName) < 1:

            self.sCxGitLabProjectRepoBranchName = None;

    def getCxGitLabProjectRepoHttpUrl(self):

        return self.sCxGitLabProjectRepoHttpURL;

    def setCxGitLabProjectRepoHttpUrl(self, cxgitlabprojectrepohttpurl=None):

        self.sCxGitLabProjectRepoHttpURL = cxgitlabprojectrepohttpurl;

        if self.sCxGitLabProjectRepoHttpURL == None or \
           len(self.sCxGitLabProjectRepoHttpURL) < 1:

            self.sCxGitLabProjectRepoHttpURL = None;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'sCxGitLabProjectId' is [%s]..." % (self.sClassDisp, self.sCxGitLabProjectId));
            print("%s The contents of 'sCxGitLabProjectName' is [%s]..." % (self.sClassDisp, self.sCxGitLabProjectName));
            print("%s The contents of 'sCxGitLabProjectGroupName' is [%s]..." % (self.sClassDisp, self.sCxGitLabProjectGroupName));
            print("%s The contents of 'sCxGitLabProjectRepoBranchName' is [%s]..." % (self.sClassDisp, self.sCxGitLabProjectRepoBranchName));
            print("%s The contents of 'sCxGitLabProjectRepoHttpURL' is [%s]..." % (self.sClassDisp, self.sCxGitLabProjectRepoHttpURL));
            print("%s The contents of 'sCxGitLabProjectRepoSshURL' is [%s]..." % (self.sClassDisp, self.sCxGitLabProjectRepoSshURL));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'sCxGitLabProjectId' is [%s], " % (self.sCxGitLabProjectId));
        asObjDetail.append("'sCxGitLabProjectName' is [%s], " % (self.sCxGitLabProjectName));
        asObjDetail.append("'sCxGitLabProjectGroupName' is [%s], " % (self.sCxGitLabProjectGroupName));
        asObjDetail.append("'sCxGitLabProjectRepoBranchName' is [%s], " % (self.sCxGitLabProjectRepoBranchName));
        asObjDetail.append("'sCxGitLabProjectRepoHttpURL' is [%s], " % (self.sCxGitLabProjectRepoHttpURL));
        asObjDetail.append("'sCxGitLabProjectRepoSshURL' is [%s]. " % (self.sCxGitLabProjectRepoSshURL));

        return ''.join(asObjDetail);

    def toPrettyString(self):

        asObjDetail = list();

        asObjDetail.append("Project (Repo) ");
        asObjDetail.append("'Id' [%-s], "          % (self.sCxGitLabProjectId));
        asObjDetail.append("'Name' [%s], "         % (self.sCxGitLabProjectName));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Group' [%s], "        % (self.sCxGitLabProjectGroupName));
        asObjDetail.append("'Repo Branch' [%s], "  % (self.sCxGitLabProjectRepoBranchName));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Repo URL' [%s], "     % (self.sCxGitLabProjectRepoHttpURL));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Repo SSH URL' [%s], " % (self.sCxGitLabProjectRepoSshURL));
        asObjDetail.append("\n");
        asObjDetail.append("........");

        return ''.join(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def populateCxGitLabProjectDataFromJsonDictionary(self, dictcxgitlabprojectdata=None):
 
        bProcessingError = False;

        if dictcxgitlabprojectdata == None:

            return False;

        dictCxGitLabProjectData = dictcxgitlabprojectdata;

        if dictCxGitLabProjectData == None or \
            len(dictCxGitLabProjectData) < 1:

            print("");
            print("%s NO Checkmarx CxGitLabProjectData dictionary object has been supplied - at CxGitLabProjectData dictionary MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            # --------------------------------------------------------------------------------------------------
            # {
            #     "id": 1,
            #     "description": "",
            #     "name": "JWS_App-Project_GitLab_1",
            #     "name_with_namespace": "JWebsoftwareDev / JWS_App-Project_GitLab_1",
            #     "path": "jws_app-project_gitlab_1",
            #     "path_with_namespace": "jwebsoftwaredev/jws_app-project_gitlab_1",
            #     "created_at": "2019-10-25T02:09:08.776Z",
            #     "default_branch": "master",
            #     "tag_list": [],
            #     "ssh_url_to_repo": "git@10.211.55.50:jwebsoftwaredev/jws_app-project_gitlab_1.git",
            #     "http_url_to_repo": "http://10.211.55.50/jwebsoftwaredev/jws_app-project_gitlab_1.git",
            #     "web_url": "http://10.211.55.50/jwebsoftwaredev/jws_app-project_gitlab_1",
            #     "readme_url": "http://10.211.55.50/jwebsoftwaredev/jws_app-project_gitlab_1/blob/master/README.md",
            #     "avatar_url": null,
            #     "star_count": 0,
            #     "forks_count": 0,
            #     "last_activity_at": "2019-10-25T02:09:08.776Z",
            #     "namespace": {
            #         "id": 2,
            #         "name": "JWebsoftwareDev",
            #         "path": "jwebsoftwaredev",
            #         "kind": "group",
            #         "full_path": "jwebsoftwaredev",
            #         "parent_id": null,
            #         "avatar_url": null,
            #         "web_url": "http://10.211.55.50/groups/jwebsoftwaredev"
            #     }
            # }
            # --------------------------------------------------------------------------------------------------

            sGitLabProjectId          = ("%s" % (dictCxGitLabProjectData["id"]));
            sGitLabProjectName        = dictCxGitLabProjectData["name"];
            sGitLabProjectGroupName   = "";
            sGitLabPathWithNamespace  = dictCxGitLabProjectData["path_with_namespace"];
            asGitLabPathWithNamespace = sGitLabPathWithNamespace.partition("/");

            if asGitLabPathWithNamespace != None and \
                len(asGitLabPathWithNamespace) > 0:

                sGitLabProjectGroupName = asGitLabPathWithNamespace[0];

            if sGitLabProjectGroupName != None:

                sGitLabProjectGroupName = sGitLabProjectGroupName.strip();

            if sGitLabProjectGroupName == None or \
                len(sGitLabProjectGroupName) < 1:

                sGitLabProjectGroupName = "";

            sGitLabProjectRepoBranchName = dictCxGitLabProjectData["default_branch"]; 
            sGitLabProjectRepoHttpURL    = dictCxGitLabProjectData["http_url_to_repo"]; 
            sGitLabProjectRepoSshURL     = dictCxGitLabProjectData["ssh_url_to_repo"]; 

            if sGitLabProjectId != None:

                sGitLabProjectId = sGitLabProjectId.strip();

            if sGitLabProjectId == None or \
                len(sGitLabProjectId) < 1:

                self.sCxGitLabProjectId = None;

            else:

                self.sCxGitLabProjectId = sGitLabProjectId;
            
            if sGitLabProjectName != None:

                sGitLabProjectName = sGitLabProjectName.strip();

            if sGitLabProjectName == None or \
                len(sGitLabProjectName) < 1:

                self.sCxGitLabProjectName = None;

            else:

                self.sCxGitLabProjectName = sGitLabProjectName;

            if sGitLabProjectGroupName != None:

                sGitLabProjectGroupName = sGitLabProjectGroupName.strip();

            if sGitLabProjectGroupName == None or \
                len(sGitLabProjectGroupName) < 1:

                self.sCxGitLabProjectGroupName = None;

            else:

                self.sCxGitLabProjectGroupName = sGitLabProjectGroupName;

            if sGitLabProjectRepoBranchName != None:

                sGitLabProjectRepoBranchName = sGitLabProjectRepoBranchName.strip();

            if sGitLabProjectRepoBranchName == None or \
                len(sGitLabProjectRepoBranchName) < 1:

                self.sCxGitLabProjectRepoBranchName = None;

            else:

                self.sCxGitLabProjectRepoBranchName = sGitLabProjectRepoBranchName;

            if sGitLabProjectRepoHttpURL != None:

                sGitLabProjectRepoHttpURL = sGitLabProjectRepoHttpURL.strip();

            if sGitLabProjectRepoHttpURL == None or \
                len(sGitLabProjectRepoHttpURL) < 1:

                self.sCxGitLabProjectRepoHttpURL = None;

            else:

                self.sCxGitLabProjectRepoHttpURL = sGitLabProjectRepoHttpURL;

            if sGitLabProjectRepoSshURL != None:

                sGitLabProjectRepoSshURL = sGitLabProjectRepoSshURL.strip();

            if sGitLabProjectRepoSshURL == None or \
                len(sGitLabProjectRepoSshURL) < 1:

                self.sCxGitLabProjectRepoSshURL = None;

            else:

                self.sCxGitLabProjectRepoSshURL = sGitLabProjectRepoSshURL;

        except Exception as inst:
 
            print("%s 'populateCxGitLabProjectDataFromJsonDictionary()' - exception occured..." % (self.sClassDisp));
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
 
    def generateCxGitLabProjectDataAsDirectory(self):

        bProcessingError        = False;
        dictCxGitLabProjectRepo = {}; 

        try:

            # Generate the (Output) 'plist' Repo Dictionary:
        
            listCxGitLabProjectRepoBranches = [];
            dictCxGitLabProjectRepoBranch   = {};
        
            dictCxGitLabProjectRepoBranch["BranchIsActive"] = "true";
            dictCxGitLabProjectRepoBranch["BranchName"]     = self.sCxGitLabProjectRepoBranchName;
        
            listCxGitLabProjectRepoBranches.append(dictCxGitLabProjectRepoBranch);
        
            dictCxGitLabProjectRepo["RepoTitle"]     = self.sCxGitLabProjectName
            dictCxGitLabProjectRepo["RepoIsActive"]  = "true";
            dictCxGitLabProjectRepo["RepoURL"]       = self.sCxGitLabProjectRepoHttpURL;
            dictCxGitLabProjectRepo["RepoRemoteURL"] = self.sCxGitLabProjectRepoHttpURL;
            dictCxGitLabProjectRepo["RepoSshURL"]    = self.sCxGitLabProjectRepoSshURL;
            dictCxGitLabProjectRepo["RepoBranches"]  = listCxGitLabProjectRepoBranches;

        except Exception as inst:
 
            print("%s 'generateCxGitLabProjectDataAsDirectory()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);
 
            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);
 
            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");
 
            return None;
 
        if bProcessingError == True:
 
            return None;
 
        return dictCxGitLabProjectRepo;
 
