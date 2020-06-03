
import os;
import traceback;
import re;
import string;
import sys;
import collections;
import zope.interface;

import CxProjectCreation1;

class CxApplicationScannerInterfaceZipper(zope.interface.Interface):

#   sClassMod  = __name__;
#   sClassId   = "CxApplicationScannerInterfaceZipper";
#   sClassVers = "(v1.0103)";
#   sClassDisp = sClassMod+"."+sClassId+" "+sClassVers+": ";

    # -------------------------------------------------------------------
    #
    # The following section contains the fields that may be customized
    # to support the CxProject 'application' collection:
    #
    #   1) Application 'work' directory.
    #   2) 'generated' Application Zip (filename).
    #
    # -------------------------------------------------------------------

    # @interface.default
    def getCxApplicationWorkDir(self):

        pass;

    # @interface.default
    def setCxApplicationWorkDir(self, cxapplicationworkdir=None):

        pass;

    # @interface.default
    def getCxApplicationZip(self):

        pass;

    # @interface.default
    def setCxApplicationZip(self, cxapplicationzip=None):

        pass;

    # Project 'overrides' for various field(s):

    # @interface.default
    def generateCxApplicationZip(self, cxprojectcreation=None):

        pass;

