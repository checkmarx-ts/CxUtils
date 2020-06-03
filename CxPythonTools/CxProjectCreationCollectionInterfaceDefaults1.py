
import os;
import traceback;
import re;
import string;
import sys;
import collections;
import zope.interface;

import CxProjectCreation1;

class CxProjectCreationCollectionInterfaceDefaults(zope.interface.Interface):

#   sClassMod  = __name__;
#   sClassId   = "CxProjectCreationCollectionInterfaceDefaults";
#   sClassVers = "(v1.0204)";
#   sClassDisp = sClassMod+"."+sClassId+" "+sClassVers+": ";

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

#   sDefaultCxProjectTeamName         = "\\CxServer\\SP\\Company\\Users";
#   sDefaultCxProjectPresetName       = "Checkmarx Default";
#   sDefaultCxProjectMobilePresetName = "Mobile";

    # @interface.default
    def getDefaultCxProjectTeamName(self):

    #   return self.sDefaultCxProjectTeamName;
        return "\\CxServer\\SP\\Company\\Users";

    # @interface.default
    def getDefaultCxProjectPresetName(self):

    #   return self.sDefaultCxProjectPresetName;
        return "Checkmarx Default"; 

    # @interface.default
    def getDefaultCxProjectMobilePresetName(self):

    #   return self.sDefaultCxProjectMobilePresetName;
        return "Mobile"; 

    def resetCxProjectCreationCollectionDefaultsDefaults(self):

        pass;

    # Project 'overrides' for various field(s) (in the 'interface' dictprojectcreationproperties is NOT used):

    # @interface.default
    def getCxProjectBaseName(self, cxprojectcreation=None, dictprojectcreationproperties=None):

        if cxprojectcreation == None:

            return None;

        cxProjectCreation = cxprojectcreation;

        sCxProjectBaseName = cxProjectCreation.getCxProjectBaseName();

        if sCxProjectBaseName != None:

            sCxProjectBaseName = sCxProjectBaseName.strip();

        if sCxProjectBaseName == None or \
            len(sCxProjectBaseName) < 1:

            sCxProjectBaseName = cxProjectCreation.getCxProjectName();

            cxProjectCreation.setCxProjectBaseName(cxprojectbasename=sCxProjectBaseName);

        return sCxProjectBaseName;

    # @interface.default
    def getCxProjectName(self, cxprojectcreation=None, dictprojectcreationproperties=None):

        if cxprojectcreation == None:

            return None;

        cxProjectCreation = cxprojectcreation;

        return cxProjectCreation.getCxProjectName();

    # @interface.default
    def getExtraCxProjectBranchNames(self, cxprojectcreation=None, dictprojectcreationproperties=None):

        if cxprojectcreation == None:

            return None;

        return None;

    # @interface.default
    def getCxProjectTeamName(self, cxprojectcreation=None, dictprojectcreationproperties=None):

        if cxprojectcreation == None:

            return None;

        cxProjectCreation  = cxprojectcreation;
        sCxProjectTeamName = cxProjectCreation.getCxProjectTeam();

        if sCxProjectTeamName != None:
        
            sCxProjectTeamName = sCxProjectTeamName.strip();
        
        if sCxProjectTeamName != None and \
            len(sCxProjectTeamName) > 0:

            return sCxProjectTeamName;
        
    #   return self.sDefaultCxProjectTeamName;
        return self.getDefaultCxProjectTeamName();

    # @interface.default
    def getCxProjectBranchedName(self, cxprojectcreation=None, cxprojectbranchname=None):

        if cxprojectcreation == None:

            return None;

        cxProjectCreation = cxprojectcreation;

        if cxprojectbranchname == None:

            return None;

        sCxProjectBranchName = cxprojectbranchname;

        if sCxProjectBranchName != None:

            sCxProjectBranchName = sCxProjectBranchName.strip();

        if sCxProjectBranchName == None or \
            len(sCxProjectBranchName) < 1:

            return None;

        sCxProjectBaseName = cxProjectCreation.getCxProjectBaseName();

        if sCxProjectBaseName != None:

            sCxProjectBaseName = sCxProjectBaseName.strip();

        if sCxProjectBaseName == None or \
            len(sCxProjectBaseName) < 1:

            sCxProjectBaseName = cxProjectCreation.getCxProjectName();

            cxProjectCreation.setCxProjectBaseName(cxprojectbasename=sCxProjectBaseName);

        #   return sCxProjectBranchName;

        sGeneratedProjectBranchedName = "%s_BR_%s" % (sCxProjectBaseName, sCxProjectBranchName); 

        return sGeneratedProjectBranchedName;

#   def dump_fields(self):
#
#       if self.bTraceFlag == True:
#
#           print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
#           print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
#           print("%s The contents of 'sDefaultCxProjectTeamName' is [%s]..." % (self.sClassDisp, self.sDefaultCxProjectTeamName));
#           print("%s The contents of 'sDefaultCxProjectPresetName' is [%s]..." % (self.sClassDisp, self.sDefaultCxProjectPresetName));
#           print("%s The contents of 'sDefaultCxProjectMobilePresetName' is [%s]..." % (self.sClassDisp, self.sDefaultCxProjectMobilePresetName));
#
#   def toString(self):
#
#       asObjDetail = list();
#
#       asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
#       asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
#       asObjDetail.append("'sDefaultCxProjectTeamName' is [%s], " % (self.sDefaultCxProjectTeamName));
#       asObjDetail.append("'sDefaultCxProjectPresetName' is [%s], " % (self.sDefaultCxProjectPresetName));
#       asObjDetail.append("'sDefaultCxProjectMobilePresetName' is [%s]. " % (self.sDefaultCxProjectMobilePresetName));
#
#       return str(asObjDetail);
#
#   def __str__(self):
#
#       return self.toString();
#
#   def __repr__(self):
#
#       return self.toString();

