
import os;
import traceback;
import re;
import string;
import sys;
import collections;

class CxProjectDataCollectionDefaults:

    sClassMod  = __name__;
    sClassId   = "CxProjectDataCollectionDefaults";
    sClassVers = "(v1.0005)";
    sClassDisp = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag = False;

    # -------------------------------------------------------------------
    #
    # The following section contains the fields that may be customized
    # to support the CxProject 'data' collection:
    #
    #   1) ...
    #
    # -------------------------------------------------------------------

    # Project 'default' field(s):

    # Key 'cx-programming-language-name' : Value ['g'|'s'] (where 'g' indicates a 'gap' language and 's' a 'standard' language)...

    dictCxProjectLanguages = {"unknown"   :"s",
                              "csharp"    :"s",    
                              "java"      :"s",
                              "cpp"       :"s",
                              "javascript":"s",
                              "apex"      :"s",
                              "vbnet"     :"s",
                              "vbscript"  :"s",
                              "asp"       :"s",
                              "vb6"       :"s",
                              "php"       :"s",
                              "ruby"      :"s", 
                              "perl"      :"g",
                              "objc"      :"s",
                              "plsql"     :"s",
                              "python"    :"s",
                              "groovy"    :"g", 
                              "scala"     :"g",
                              "go"        :"g",
                              "typescript":"g",
                              "kotlin"    :"g",  
                              "common"    :"s"};

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

    def getDefaultCxProjectLanguages(self):

        return self.dictCxProjectLanguages;

    def resetCxProjectDataCollectionDefaults(self):

        self.dictCxProjectLanguages = {"unknown"   :"s",
                                       "csharp"    :"s",    
                                       "java"      :"s",
                                       "cpp"       :"s",
                                       "javascript":"s",
                                       "apex"      :"s",
                                       "vbnet"     :"s",
                                       "vbscript"  :"s",
                                       "asp"       :"s",
                                       "vb6"       :"s",
                                       "php"       :"s",
                                       "ruby"      :"s", 
                                       "perl"      :"g",
                                       "objc"      :"g",
                                       "plsql"     :"s",
                                       "python"    :"s",
                                       "groovy"    :"g", 
                                       "scala"     :"g",
                                       "go"        :"g",
                                       "typescript":"g",
                                       "kotlin"    :"s",  
                                       "common"    :"s"};

        return;

    # Project 'overrides' for various field(s):

    def getCxProjectLanguageType(self, cxprojectlanguage=None):

        if cxprojectlanguage == None:

            return None;

        sCxProjectLanguage = cxprojectlanguage;

        if sCxProjectLanguage != None:

            sCxProjectLanguage = sCxProjectLanguage.strip();

        if sCxProjectLanguage == None or \
            len(sCxProjectLanguage) < 1:

            return None;

        sCxProjectLanguageLow = sCxProjectLanguage.lower();

        if sCxProjectLanguageLow not in self.dictCxProjectLanguages.keys():

            return None;

        sCxProjectLanguageType = self.dictCxProjectLanguages[sCxProjectLanguageLow];

        return sCxProjectLanguageType;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'dictCxProjectLanguages' is [%s]..." % (self.sClassDisp, self.dictCxProjectLanguages));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'dictCxProjectLanguages' is [%s], " % (self.dictCxProjectLanguages));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

bMainVerbose = True;

def main():

    try:

        if bMainVerbose == True:

            cxProjectDataCollectionDefaults = CxProjectDataCollectionDefaults(trace=bMainVerbose);

            cxProjectDataCollectionDefaults.dump_fields();

            print("");

            asTestLanguages = ["java",
                               "apex",
                               "objc",
                               "scala",
                               "typescript",
                               "common",
                               "cobol",
                               "fortran"];

            for sTestLanguage in asTestLanguages:

                sTestLanguageType = cxProjectDataCollectionDefaults.getCxProjectLanguageType(cxprojectlanguage=sTestLanguage);

                print("A 'language' of [%s] has a type of [%s]..." % (sTestLanguage, sTestLanguageType));

            print("");

    except Exception as inst:

        print("%s 'main()' - exception occured..." % (CxProjectDataCollectionDefaults.sClassDisp));
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

        print("%s Exiting with a Return Code of (31)..." % (CxProjectDataCollectionDefaults.sClassDisp));

        sys.exit(31);

    print("%s Exiting with a Return Code of (0)..." % (CxProjectDataCollectionDefaults.sClassDisp));

    sys.exit(0);

