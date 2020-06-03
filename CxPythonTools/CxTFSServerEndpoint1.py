
import os;
import traceback;
import re;
import string;
import sys;
import base64;

class CxTFSServerEndpoint(object):

    sClassMod                  = __name__;
    sClassId                   = "CxTFSServerEndpoint";
    sClassVers                 = "(v1.0202)";
    sClassDisp                 = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                 = False;
    bCxTFSServerEndpointActive = False;
    sCxTFSServerURL            = None;
    sCxTFSUserId               = None;
    sCxTFSPAT                  = None;

    # Generated Base64 'user:PAT' field(s):

    sTFSUserAndPAT             = None;          # "%s:%s" % (self.sCxTFSUserId, self.sCxTFSPAT);
    sBase64UserPATb            = None;
    sBase64UserPAT             = None;

    def __init__(self, trace=False, cxtfsserverendpointactive=False, cxtfsserverurl=None, cxtfsuserid=None, cxtfspat=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxTFSServerEndpointActiveFlag(cxtfsserverendpointactive=cxtfsserverendpointactive);
            self.setCxTFSServerURL(cxtfsserverurl=cxtfsserverurl);
            self.setCxTFSUserId(cxtfsuserid=cxtfsuserid);
            self.setCxTFSPAT(cxtfspat=cxtfspat);

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

    def getCxTFSServerEndpointActiveFlag(self):

        return self.bCxTFSServerEndpointActive;

    def setCxTFSServerEndpointActiveFlag(self, cxtfsserverendpointactive=False):

        self.bCxTFSServerEndpointActive = cxtfsserverendpointactive;

    def getCxTFSServerURL(self):

        return self.sCxTFSServerURL;

    def setCxTFSServerURL(self, cxtfsserverurl=None):

        self.sCxTFSServerURL = cxtfsserverurl;

        if self.sCxTFSServerURL != None:

            self.sCxTFSServerURL = self.sCxTFSServerURL.strip();

        if self.sCxTFSServerURL == None or \
           len(self.sCxTFSServerURL) < 1:

            self.sCxTFSServerURL = None;

        else:

            sCxTFSServerURLLow = self.sCxTFSServerURL.lower();

            if sCxTFSServerURLLow.startswith("http://")  == False and \
               sCxTFSServerURLLow.startswith("https://") == False and \
               sCxTFSServerURLLow.startswith("ssh://")   == False:

                self.sCxTFSServerURL = None;

        if self.sCxTFSServerURL != None and \
            len(self.sCxTFSServerURL) > 0:

            if self.sCxTFSServerURL.endswith("/") == True:

                self.sCxTFSServerURL = self.sCxTFSServerURL[:(len(self.sCxTFSServerURL) - 1)];

    def getCxTFSUserId(self):

        return self.sCxTFSUserId;

    def setCxTFSUserId(self, cxtfsuserid=None):

        self.sCxTFSUserId = cxtfsuserid;

        if self.sCxTFSUserId != None:

            self.sCxTFSUserId = self.sCxTFSUserId.strip();

        if self.sCxTFSUserId == None or \
           len(self.sCxTFSUserId) < 1:

            self.sCxTFSUserId = None;

        return;

    def getCxTFSPAT(self):

        return self.sCxTFSPAT;

    def setCxTFSPAT(self, cxtfspat=None):

        self.sCxTFSPAT = cxtfspat;

        if self.sCxTFSPAT != None:

            self.sCxTFSPAT = self.sCxTFSPAT.strip();

        if self.sCxTFSPAT == None or \
           len(self.sCxTFSPAT) < 1:

            self.sCxTFSPAT = "";

        return;

    # Generated field(s):

    def getTFSUserAndPAT(self):

        return self.sTFSUserAndPAT;

    def getBase64UserPATb(self):

        return self.sBase64UserPATb;

    def getBase64UserPAT(self):

        return self.sBase64UserPAT;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The 'bCxTFSServerEndpointActive' boolean is [%s]..." % (self.sClassDisp, self.bCxTFSServerEndpointActive));
            print("%s The contents of 'sCxTFSServerURL' is [%s]..." % (self.sClassDisp, self.sCxTFSServerURL));
            print("%s The contents of 'sCxTFSUserId' is [%s]..." % (self.sClassDisp, self.sCxTFSUserId));
            print("%s The contents of 'sCxTFSPAT' is [%s]..." % (self.sClassDisp, self.sCxTFSPAT));
            print("%s The contents of 'sTFSUserAndPAT' is [%s]..." % (self.sClassDisp, self.sTFSUserAndPAT));
            print("%s The contents of 'sBase64UserPATb' is [%s]..." % (self.sClassDisp, self.sBase64UserPATb));
            print("%s The contents of 'sBase64UserPAT' is [%s]..." % (self.sClassDisp, self.sBase64UserPAT));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'bCxTFSServerEndpointActive' is [%s], " % (self.bCxTFSServerEndpointActive));
        asObjDetail.append("'sCxTFSServerURL' is [%s], " % (self.sCxTFSServerURL));
        asObjDetail.append("'sCxTFSUserId' is [%s], " % (self.sCxTFSUserId));
        asObjDetail.append("'sCxTFSPAT' is [%s], " % (self.sCxTFSPAT));
        asObjDetail.append("'sTFSUserAndPAT' is [%s], " % (self.sTFSUserAndPAT));
        asObjDetail.append("'sBase64UserPATb' is [%s], " % (self.sBase64UserPATb));
        asObjDetail.append("'sBase64UserPAT' is [%s], " % (self.sBase64UserPAT));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def generateCxTFSProjectBase64Fields(self):
 
        bProcessingError = False;

        if self.sCxTFSUserId != None:

            self.sCxTFSUserId = self.sCxTFSUserId.strip();

        if self.sCxTFSUserId == None or \
            len(self.sCxTFSUserId) < 1:

            print("");
            print("%s NO TFS User Id has been specified nor defined - 1 MUST be defined - Error!" % (self.sClassDisp));
            print("");
     
            return False;

        if self.sCxTFSPAT != None:

            self.sCxTFSPAT = self.sCxTFSPAT.strip();

        if self.sCxTFSPAT == None or \
            len(self.sCxTFSPAT) < 1:

            print("");
            print("%s NO TFS PAT (Personal Access Token) has been specified nor defined - 1 MUST be defined - Error!" % (self.sClassDisp));
            print("");
     
            return False;

        try:

            self.sTFSUserAndPAT  = "%s:%s" % (self.sCxTFSUserId, self.sCxTFSPAT);
            self.sBase64UserPATb = base64.b64encode(bytes(self.sTFSUserAndPAT, "utf-8"));
            self.sBase64UserPAT  = self.sBase64UserPATb.decode(encoding='UTF-8');

            if self.bTraceFlag == True:

                print("%s Base64: 'sBase64UserPATb' is [%s] and 'sBase64UserPAT' is [%s]..." % (self.sClassDisp, self.sBase64UserPATb, self.sBase64UserPAT));

        except Exception as inst:
 
            print("%s 'generateCxTFSProjectBase64Fields()' - exception occured..." % (self.sClassDisp));
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
 
