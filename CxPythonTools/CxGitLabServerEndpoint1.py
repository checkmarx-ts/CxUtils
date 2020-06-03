
import os;
import traceback;
import re;
import string;
import sys;
import base64;

class CxGitLabServerEndpoint(object):

    sClassMod                     = __name__;
    sClassId                      = "CxGitLabServerEndpoint";
    sClassVers                    = "(v1.0206)";
    sClassDisp                    = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                    = False;
    bCxGitLabServerEndpointActive = False;
    sCxGitLabServerURL            = None;
    sCxGitLabGroup                = None;
    sCxGitLabUserId               = None;
    sCxGitLabPassword             = None;

    # --- Fields set via Rest API call(s) ---

    sCxGitLabTokenType            = "";
    sCxGitLabAccessToken          = "";

    def __init__(self, trace=False, cxgitlabserverendpointactive=False, cxgitlabserverurl=None, cxgitlabgroup=None, cxgitlabuserid=None, cxgitlabpassword=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxGitLabServerEndpointActiveFlag(cxgitlabserverendpointactive=cxgitlabserverendpointactive);
            self.setCxGitLabServerURL(cxgitlabserverurl=cxgitlabserverurl);
            self.setCxGitLabGroup(cxgitlabgroup=cxgitlabgroup);
            self.setCxGitLabUserId(cxgitlabuserid=cxgitlabuserid);
            self.setCxGitLabPassword(cxgitlabpassword=cxgitlabpassword);

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

    def getCxGitLabServerEndpointActiveFlag(self):

        return self.bCxGitLabServerEndpointActive;

    def setCxGitLabServerEndpointActiveFlag(self, cxgitlabserverendpointactive=False):

        self.bCxGitLabServerEndpointActive = cxgitlabserverendpointactive;

    def getCxGitLabServerURL(self):

        return self.sCxGitLabServerURL;

    def setCxGitLabServerURL(self, cxgitlabserverurl=None):

        self.sCxGitLabServerURL = cxgitlabserverurl;

        if self.sCxGitLabServerURL != None:

            self.sCxGitLabServerURL = self.sCxGitLabServerURL.strip();

        if self.sCxGitLabServerURL == None or \
           len(self.sCxGitLabServerURL) < 1:

            self.sCxGitLabServerURL = None;

        else:

            sCxGitLabServerURLLow = self.sCxGitLabServerURL.lower();

            if sCxGitLabServerURLLow.startswith("http://")  == False and \
               sCxGitLabServerURLLow.startswith("https://") == False and \
               sCxGitLabServerURLLow.startswith("ssh://")   == False:

                self.sCxGitLabServerURL = None;

        if self.sCxGitLabServerURL != None and \
            len(self.sCxGitLabServerURL) > 0:

            if self.sCxGitLabServerURL.endswith("/") == True:

                self.sCxGitLabServerURL = self.sCxGitLabServerURL[:(len(self.sCxGitLabServerURL) - 1)];

    def getCxGitLabUserId(self):

        return self.sCxGitLabUserId;

    def setCxGitLabUserId(self, cxgitlabuserid=None):

        self.sCxGitLabUserId = cxgitlabuserid;

        if self.sCxGitLabUserId != None:

            self.sCxGitLabUserId = self.sCxGitLabUserId.strip();

        if self.sCxGitLabUserId == None or \
           len(self.sCxGitLabUserId) < 1:

            self.sCxGitLabUserId = None;

        return;

    def getCxGitLabGroup(self):

        return self.sCxGitLabGroup;

    def setCxGitLabGroup(self, cxgitlabgroup=None):

        self.sCxGitLabGroup = cxgitlabgroup;

        if self.sCxGitLabGroup != None:

            self.sCxGitLabGroup = self.sCxGitLabGroup.strip();

        if self.sCxGitLabGroup == None or \
           len(self.sCxGitLabGroup) < 1:

            self.sCxGitLabGroup = None;

        return;

    def getCxGitLabPassword(self):

        return self.sCxGitLabPassword;

    def setCxGitLabPassword(self, cxgitlabpassword=None):

        self.sCxGitLabPassword = cxgitlabpassword;

        if self.sCxGitLabPassword != None:

            self.sCxGitLabPassword = self.sCxGitLabPassword.strip();

        if self.sCxGitLabPassword == None or \
           len(self.sCxGitLabPassword) < 1:

            self.sCxGitLabPassword = "";

        return;

    def resetCxGitLabServerEndpointAuthTokenDetails(self):

        self.sCxGitLabTokenType   = "";
        self.sCxGitLabAccessToken = "";

    def getCxGitLabTokenType(self):

        return self.sCxGitLabTokenType;

    def setCxGitLabTokenType(self, cxgitlabtokentype=None):

        self.sCxGitLabTokenType = cxgitlabtokentype;

        if self.sCxGitLabTokenType != None:

            self.sCxGitLabTokenType = self.sCxGitLabTokenType.strip();

        if self.sCxGitLabTokenType == None or \
           len(self.sCxGitLabTokenType) < 1:

            self.sCxGitLabTokenType = "";

        return;

    def getCxGitLabAccessToken(self):

        return self.sCxGitLabAccessToken;

    def setCxGitLabAccessToken(self, cxgitlabaccesstoken=None):

        self.sCxGitLabAccessToken = cxgitlabaccesstoken;

        if self.sCxGitLabAccessToken != None:

            self.sCxGitLabAccessToken = self.sCxGitLabAccessToken.strip();

        if self.sCxGitLabAccessToken == None or \
           len(self.sCxGitLabAccessToken) < 1:

            self.sCxGitLabAccessToken = "";

        return;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The 'bCxGitLabServerEndpointActive' boolean is [%s]..." % (self.sClassDisp, self.bCxGitLabServerEndpointActive));
            print("%s The contents of 'sCxGitLabServerURL' is [%s]..." % (self.sClassDisp, self.sCxGitLabServerURL));
            print("%s The contents of 'sCxGitLabGroup' is [%s]..." % (self.sClassDisp, self.sCxGitLabGroup));
            print("%s The contents of 'sCxGitLabUserId' is [%s]..." % (self.sClassDisp, self.sCxGitLabUserId));
            print("%s The contents of 'sCxGitLabPassword' is [%s]..." % (self.sClassDisp, self.sCxGitLabPassword));
            print("%s The contents of 'sCxGitLabTokenType' is [%s]..." % (self.sClassDisp, self.sCxGitLabTokenType));
            print("%s The contents of 'sCxGitLabAccessToken' is [%s]..." % (self.sClassDisp, self.sCxGitLabAccessToken));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'bCxGitLabServerEndpointActive' is [%s], " % (self.bCxGitLabServerEndpointActive));
        asObjDetail.append("'sCxGitLabServerURL' is [%s], " % (self.sCxGitLabServerURL));
        asObjDetail.append("'sCxGitLabGroup' is [%s], " % (self.sCxGitLabGroup));
        asObjDetail.append("'sCxGitLabUserId' is [%s], " % (self.sCxGitLabUserId));
        asObjDetail.append("'sCxGitLabPassword' is [%s], " % (self.sCxGitLabPassword));
        asObjDetail.append("'sCxGitLabTokenType' is [%s], " % (self.sCxGitLabTokenType));
        asObjDetail.append("'sCxGitLabAccessToken' is [%s]. " % (self.sCxGitLabAccessToken));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();
 
