
import os;
import traceback;
import re;
import string;
import sys;

class CxServerEndpoint(object):

    sClassMod               = __name__;
    sClassId                = "CxServerEndpoint";
    sClassVers              = "(v1.0502)";
    sClassDisp              = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag              = False;
    bCxServerEndpointActive = False;
    sCxServerURL            = None;
    sCxAuthUserID           = None;
    sCxAuthPassword         = None;

    # --- Fields set via Rest API call(s) ---

    sCxTokenType            = "";
    sCxAccessToken          = "";
    sCxAccessTokenExpiresIn = "";

    def __init__(self, trace=False, cxserverendpointactive=False, cxserverurl=None, cxauthuserid=None, cxauthpassword=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxServerEndpointActiveFlag(cxserverendpointactive=cxserverendpointactive);
            self.setCxServerURL(cxserverurl=cxserverurl);
            self.setCxAuthUserID(cxauthuserid=cxauthuserid);
            self.setCxAuthPassword(cxauthpassword=cxauthpassword);

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

    def getCxServerEndpointActiveFlag(self):

        return self.bCxServerEndpointActive;

    def setCxServerEndpointActiveFlag(self, cxserverendpointactive=False):

        self.bCxServerEndpointActive = cxserverendpointactive;

    def getCxServerURL(self):

        return self.sCxServerURL;

    def setCxServerURL(self, cxserverurl=None):

        self.sCxServerURL = cxserverurl;

        if self.sCxServerURL != None:

            self.sCxServerURL = self.sCxServerURL.strip();

        if self.sCxServerURL == None or \
           len(self.sCxServerURL) < 1:

            self.sCxServerURL = None;

        else:

            sCxServerURLLow = self.sCxServerURL.lower();

            if sCxServerURLLow.startswith("http://")  == False and \
               sCxServerURLLow.startswith("https://") == False:

                self.sCxServerURL = None;

        if self.sCxServerURL != None and \
            len(self.sCxServerURL) > 0:

            if self.sCxServerURL.endswith("/") == True:

                self.sCxServerURL = self.sCxServerURL[:(len(self.sCxServerURL) - 1)];

    def getCxAuthUserID(self):

        return self.sCxAuthUserID;

    def setCxAuthUserID(self, cxauthuserid=None):

        self.sCxAuthUserID = cxauthuserid;

        if self.sCxAuthUserID != None:

            self.sCxAuthUserID = self.sCxAuthUserID.strip();

        if self.sCxAuthUserID == None or \
           len(self.sCxAuthUserID) < 1:

            self.sCxAuthUserID = None;

        return;

    def getCxAuthPassword(self):

        return self.sCxAuthPassword;

    def setCxAuthPassword(self, cxauthpassword=None):

        self.sCxAuthPassword = cxauthpassword;

        if self.sCxAuthPassword != None:

            self.sCxAuthPassword = self.sCxAuthPassword.strip();

        if self.sCxAuthPassword == None or \
           len(self.sCxAuthPassword) < 1:

            self.sCxAuthPassword = "";

        return;

    def resetCxServerEndpointAuthTokenDetails(self):

        self.sCxTokenType            = "";
        self.sCxAccessToken          = "";
        self.sCxAccessTokenExpiresIn = "";

        return;

    def getCxTokenType(self):

        return self.sCxTokenType;

    def setCxTokenType(self, cxtokentype=None):

        self.sCxTokenType = cxtokentype;

        if self.sCxTokenType != None:

            self.sCxTokenType = self.sCxTokenType.strip();

        if self.sCxTokenType == None or \
           len(self.sCxTokenType) < 1:

            self.sCxTokenType = "";

        return;

    def getCxAccessToken(self):

        return self.sCxAccessToken;

    def setCxAccessToken(self, cxaccesstoken=None):

        self.sCxAccessToken = cxaccesstoken;

        if self.sCxAccessToken != None:

            self.sCxAccessToken = self.sCxAccessToken.strip();

        if self.sCxAccessToken == None or \
           len(self.sCxAccessToken) < 1:

            self.sCxAccessToken = "";

        return;

    def getCxAccessTokenExpiresIn(self):

        return self.sCxAccessTokenExpiresIn;

    def setCxAccessTokenExpiresIn(self, cxaccesstokenexpiresin=None):

        if type(cxaccesstokenexpiresin) == str:

            self.sCxAccessTokenExpiresIn = cxaccesstokenexpiresin;

        else:

            self.sCxAccessTokenExpiresIn = ("%d" % cxaccesstokenexpiresin);

        if self.sCxAccessTokenExpiresIn != None:

            self.sCxAccessTokenExpiresIn = self.sCxAccessTokenExpiresIn.strip();

        if self.sCxAccessTokenExpiresIn == None or \
           len(self.sCxAccessTokenExpiresIn) < 1:

            self.sCxAccessTokenExpiresIn = "";

        return;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The 'bCxServerEndpointActive' boolean is [%s]..." % (self.sClassDisp, self.bCxServerEndpointActive));
            print("%s The contents of 'sCxServerURL' is [%s]..." % (self.sClassDisp, self.sCxServerURL));
            print("%s The contents of 'sCxAuthUserID' is [%s]..." % (self.sClassDisp, self.sCxAuthUserID));
            print("%s The contents of 'sCxAuthPassword' is [%s]..." % (self.sClassDisp, self.sCxAuthPassword));
            print("%s The contents of 'sCxTokenType' is [%s]..." % (self.sClassDisp, self.sCxTokenType));
            print("%s The contents of 'sCxAccessToken' is [%s]..." % (self.sClassDisp, self.sCxAccessToken));
            print("%s The contents of 'sCxAccessTokenExpiresIn' is [%s]..." % (self.sClassDisp, self.sCxAccessTokenExpiresIn));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'bCxServerEndpointActive' is [%s], " % (self.bCxServerEndpointActive));
        asObjDetail.append("'sCxServerURL' is [%s], " % (self.sCxServerURL));
        asObjDetail.append("'sCxAuthUserID' is [%s], " % (self.sCxAuthUserID));
        asObjDetail.append("'sCxAuthPassword' is [%s], " % (self.sCxAuthPassword));
        asObjDetail.append("'sCxTokenType' is [%s], " % (self.sCxTokenType));
        asObjDetail.append("'sCxAccessToken' is [%s], " % (self.sCxAccessToken));
        asObjDetail.append("'sCxAccessTokenExpiresIn' is [%s]. " % (self.sCxAccessTokenExpiresIn));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

