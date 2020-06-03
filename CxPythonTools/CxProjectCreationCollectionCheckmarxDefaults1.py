
import os;
import traceback;
import re;
import string;
import sys;
import collections;
import zope.interface;

import CxProjectCreation1;

from zope.interface import implementer;
from CxProjectCreationCollectionInterfaceDefaults1 import CxProjectCreationCollectionInterfaceDefaults;

# ass CxProjectCreationCollectionCheckmarxDefaults(interface.implements(CxProjectCreationCollectionInterfaceDefaults)):
@implementer(CxProjectCreationCollectionInterfaceDefaults)
class CxProjectCreationCollectionCheckmarxDefaults(object):

    # pe.interface.implements(CxProjectCreationCollectionInterfaceDefaults);

    sClassMod  = __name__;
    sClassId   = "CxProjectCreationCollectionCheckmarxDefaults";
    sClassVers = "(v1.0305)";
    sClassDisp = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag = False;

    # -------------------------------------------------------------------
    #
    # The following section contains the fields that may be customized
    # to support the CxProject 'creation' collection:
    #
    #   1) 'default' Project TeamName
    #   2) 'default' Project PresetName
    #   3) 'default' Project Mobile PresetName
    #
    # -------------------------------------------------------------------

    # Project 'default' field(s):

    sDefaultCxProjectTeamName         = "\\CxServer\\SP\\Company\\Users";
    sDefaultCxProjectPresetName       = "Checkmarx Default";
    sDefaultCxProjectMobilePresetName = "Mobile";

    def __init__(self, trace=False):

        try:

            self.setTraceFlag(trace=trace);

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

    def getDefaultCxProjectTeamName(self):
 
        return self.sDefaultCxProjectTeamName;
 
    def getDefaultCxProjectPresetName(self):
 
        return self.sDefaultCxProjectPresetName;
 
    def getDefaultCxProjectMobilePresetName(self):
 
        return self.sDefaultCxProjectMobilePresetName;
 
    def resetCxProjectCreationCollectionDefaultsDefaults(self):
 
        self.sDefaultCxProjectTeamName         = "\\CxServer\\SP\\Company\\Users";
        self.sDefaultCxProjectPresetName       = "Checkmarx Default";             
        self.sDefaultCxProjectMobilePresetName = "Mobile";                        
 
        return;

    # Project 'overrides' for various field(s) (for the 'Checkmarx' version - everything defaults to the 'super' class):

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'sDefaultCxProjectTeamName' is [%s]..." % (self.sClassDisp, self.getDefaultCxProjectTeamName()));
            print("%s The contents of 'sDefaultCxProjectPresetName' is [%s]..." % (self.sClassDisp, self.getDefaultCxProjectPresetName()));
            print("%s The contents of 'sDefaultCxProjectMobilePresetName' is [%s]..." % (self.sClassDisp, self.getDefaultCxProjectMobilePresetName()));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'sDefaultCxProjectTeamName' is [%s], " % (self.getDefaultCxProjectTeamName()));
        asObjDetail.append("'sDefaultCxProjectPresetName' is [%s], " % (self.getDefaultCxProjectPresetName()));
        asObjDetail.append("'sDefaultCxProjectMobilePresetName' is [%s]. " % (self.getDefaultCxProjectMobilePresetName()));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

bMainVerbose = True;

def main():

    try:

        if bMainVerbose == True:

            cxProjectCreationCollectionDefaults = CxProjectCreationCollectionCheckmarxDefaults(trace=bMainVerbose);

            cxProjectCreationCollectionDefaults.dump_fields();

            print("");

            cxProjectCreation1 = CxProjectCreation1.CxProjectCreation(trace=bMainVerbose, cxprojectispublic=True, cxprojectteamname=cxProjectCreationCollectionDefaults.getDefaultCxProjectTeamName(), cxprojectpresetname=cxProjectCreationCollectionDefaults.getDefaultCxProjectPresetName(), cxprojectengineconfigname="Default Configuration");

        #   cxProjectCreation1.setCxProjectBaseName(cxprojectbasename="CxProjBase");
            cxProjectCreation1.setCxProjectName(cxprojectname="CxProjName"); 
            cxProjectCreation1.setCxProjectBranchNames(cxprojectbranchnames=["CxBranch0"]);  
            cxProjectCreation1.setCxProjectTeamName(cxprojectteamname=None);  

            print("");
            print("'cxProjectCreation1' (before exit) is [%s]..." % (cxProjectCreation1.toString()));
            print("");

            print("Calling 'default' setCxProjectBaseName()...");

            cxProjectCreation1.setCxProjectBaseName(cxprojectbasename=cxProjectCreationCollectionDefaults.getCxProjectBaseName(cxprojectcreation=cxProjectCreation1, dictprojectcreationproperties=None));

            print("Calling 'default' setCxProjectName()...");

            cxProjectCreation1.setCxProjectName(cxprojectname=cxProjectCreationCollectionDefaults.getCxProjectName(cxprojectcreation=cxProjectCreation1, dictprojectcreationproperties=None)); 

            print("Calling 'default' setCxProjectBranchNames()...");

            cxProjectCreation1.setCxProjectBranchNames(cxprojectbranchnames=cxProjectCreationCollectionDefaults.getExtraCxProjectBranchNames(cxprojectcreation=cxProjectCreation1, dictprojectcreationproperties=None));  
        #   cxProjectCreation1.setCxProjectBranchNames(cxprojectbranchnames="CxBranch1");  

            print("Calling 'default' setCxProjectTeamName()...");

            cxProjectCreation1.setCxProjectTeamName(cxprojectteamname=cxProjectCreationCollectionDefaults.getCxProjectTeamName(cxprojectcreation=cxProjectCreation1, dictprojectcreationproperties=None));  

            print("Called all of the 'default' method(s)..."); 

            print("");
            print("Generated 'CxProjectBaseName'    is [%s]..." % (cxProjectCreation1.getCxProjectBaseName()));
            print("Generated 'CxProjectName'        is [%s]..." % (cxProjectCreation1.getCxProjectName()));
            print("Generated 'CxProjectBranchNames' is [%s]..." % (cxProjectCreation1.getCxProjectBranchNames()));
            print("Generated 'CxProjectTeamName'    is [%s]..." % (cxProjectCreation1.getCxProjectTeamName()));
            print("");
            print("'cxProjectCreation1' (after exit) is [%s]..." % (cxProjectCreation1.toString()));
            print("");

            asCxProjectBranchNames = cxProjectCreation1.getCxProjectBranchNames();
            cCxProjectBranchedName = 0;

            if asCxProjectBranchNames != None and \
               len(asCxProjectBranchNames) > 0:

                for sCxProjectBranchName in asCxProjectBranchNames:

                    if sCxProjectBranchName != None:

                        sCxProjectBranchName = sCxProjectBranchName.strip();

                    if sCxProjectBranchName == None or \
                        len(sCxProjectBranchName) < 1:

                        continue;

                    cCxProjectBranchedName += 1;

                    sCxProjectBranchedName = cxProjectCreationCollectionDefaults.getCxProjectBranchedName(cxprojectcreation=cxProjectCreation1, cxprojectbranchname=sCxProjectBranchName);

                    print("#(%d) of (%d): 'sCxProjectBranchName' is [%s] and 'sCxProjectBranchedName' is [%s]..." % (cCxProjectBranchedName, len(asCxProjectBranchNames), sCxProjectBranchName, sCxProjectBranchedName));

            print("");

    except Exception as inst:

        print("%s 'main()' - exception occured..." % (CxProjectCreationCollectionCheckmarxDefaults.sClassDisp));
        print(type(inst));
        print(inst);

        excType, excValue, excTraceback = sys.exc_info();
        asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

        print("- - - ");
        print('\n'.join(asTracebackLines));
        print("- - - ");

        return False;

    return True;

if __name__ == '__main__':

    bCmdExecOk = main();

    if bCmdExecOk == False:

        print("%s Exiting with a Return Code of (31)..." % (CxProjectCreationCollectionCheckmarxDefaults.sClassDisp));

        sys.exit(31);

    print("%s Exiting with a Return Code of (0)..." % (CxProjectCreationCollectionCheckmarxDefaults.sClassDisp));

    sys.exit(0);

