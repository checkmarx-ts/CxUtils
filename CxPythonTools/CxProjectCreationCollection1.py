
import os;
import traceback;
import platform;
import re;
import string;
import sys;
import collections;
import plistlib;

from datetime import datetime;

import DrcDirectoryFileSearch1;

# port CxProjectCreationCollectionDefaults1;
import CxProjectCreation1;
import CxRestAPIProjectCreationBase1;
import CxProjectData1;
import CxServerEndpoint1;

class CxProjectCreationCollection:

    sClassMod                            = __name__;
    sClassId                             = "CxProjectCreationCollection";
    sClassVers                           = "(v1.0581)";
    sClassDisp                           = sClassMod+"."+sClassId+" "+sClassVers+": ";

    # Project 'instance' field(s):

    bTraceFlag                           = False;
    bSearchRecursiveFlag                 = False;
    bSearchCaseSensitive                 = False;
    sSearchDirectory                     = None;
    sSearchFilePatterns                  = None;
    listProjectCreationPropertiesFiles   = None;
    listProjectCreationPlistFiles        = None;
    cxServerEndpoint                     = None;
    dictCxProjectCreationCollection      = None;

    asCxProjectCreationCollectionReport  = None;

    bCxProjectWasCreatedByRestAPIFlag    = False;   # Flag used by the Rest API to indicate whether or not any Project was actually created...

    # Project Collection 'meta' data:

    dictCxAllTeams                       = None;
    dictCxAllPresets                     = None;
    dictCxAllEngineConfigurations        = None;
    dictCxAllProjects                    = None;

    # Cx Application and/or Project object(s):

    cxProjCreationBase                   = None;
    cxApplicationZipper                  = None;

    # Project Collection stats:

    dictCxProjectCreationCollectionStats = collections.defaultdict(int);
                                           # Dictionary collection of 'width' counters...
                                           # Keys: "cWidthCxProjectName",
                                           #       "cWidthCxProjectId",
                                           #       "cWidthCxProjectTeamName",
                                           #       "cWidthCxProjectTeamId",
                                           #       "cWidthCxProjectPresetName",
                                           #       "cWidthCxProjectPresetId",
                                           #       "cWidthCxProjectEngineConfigName",
                                           #       "cWidthCxProjectEngineConfigId".
                                           # Note: ALL Key(s) are initialized to 0 (Zero).

    # Project Collection stats 'key(s)':

    listProjectCreationPropertiesKeys    = ["project.name",
                                            "project.team",
                                            "project.version",
                                            "project.tier",
                                            "project.visibility",
                                            "project.language.list",
                                            "project.cx.branches",
                                            "project.cx.teamname",
                                            "project.cx.presetname",
                                            "vast.id"];

    # Project Collection default(s):

    cxProjectCreationCollectionDefaults  = None;

    def __init__(self, trace=False, searchrecursive=False, searchcasesensitive=False, searchdirectory=None, searchfilepatterns=None, cxserverendpoint=None, cxprojectcreationcollectiondefaults=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setSearchRecursiveFlag(searchrecursive=searchrecursive);
            self.setSearchCaseSensitiveFlag(searchcasesensitive=searchcasesensitive);
            self.setSearchDirectory(searchdirectory=searchdirectory);
            self.setSearchFilePatterns(searchfilepatterns=searchfilepatterns);
            self.setCxServerEndpoint(cxserverendpoint=cxserverendpoint);

            self.setCxProjectCreationCollectionDefaults(cxprojectcreationcollectiondefaults=cxprojectcreationcollectiondefaults);
        #   self.cxProjectCreationCollectionDefaults = CxProjectCreationCollectionDefaults1.CxProjectCreationCollectionDefaults(trace=self.bTraceFlag);

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

    def getSearchRecursiveFlag(self):

        return self.bSearchRecursiveFlag;

    def setSearchRecursiveFlag(self, searchrecursive=False):

        self.bSearchRecursiveFlag = searchrecursive;

    def getSearchCaseSensitiveFlag(self):

        return self.bSearchCaseSensitive;

    def setSearchCaseSensitiveFlag(self, searchcasesensitive=False):

        self.bSearchCaseSensitive = searchcasesensitive;

    def getSearchDirectory(self):

        return self.sSearchDirectory;

    def setSearchDirectory(self, searchdirectory=None):

        self.sSearchDirectory = searchdirectory;

    def getSearchFilePatterns(self):

        return self.sSearchFilePatterns;

    def setSearchFilePatterns(self, searchfilepatterns=None):

        self.sSearchFilePatterns = searchfilepatterns;

    def getCxServerEndpoint(self):

        return self.cxServerEndpoint;

    def setCxServerEndpoint(self, cxserverendpoint=None):

        self.cxServerEndpoint = cxserverendpoint;

    def getCxProjectCreationCollectionDefaults(self):

        return self.cxProjectCreationCollectionDefaults;

    def setCxProjectCreationCollectionDefaults(self, cxprojectcreationcollectiondefaults=None):

        self.cxProjectCreationCollectionDefaults = cxprojectcreationcollectiondefaults;

    def getCxProjectCreationCollection(self):

        return self.dictCxProjectCreationCollection;

    def setCxProjectCreationCollection(self, cxprojectcreationcollection=None):

        self.dictCxProjectCreationCollection = cxprojectcreationcollection;

    def getCxProjectCreationCollectionReportAsList(self):

        return self.asCxProjectCreationCollectionReport;

    def getCxProjectWasCreatedByRestAPIFlag(self):

        return self.bCxProjectWasCreatedByRestAPIFlag;

    def setCxProjectWasCreatedByRestAPIFlag(self, cxprojectwascreatedbyrestapiflag=False):

        self.bCxProjectWasCreatedByRestAPIFlag = cxprojectwascreatedbyrestapiflag;

    def getCxProjectMetaDataAllTeams(self):

        return self.dictCxAllTeams;

    def addCxProjectMetaDataAllTeams(self, cxteamfullname=None, cxteamid=None):

        sCxTeamFullName = cxteamfullname;

        if sCxTeamFullName != None and \
            type(sCxTeamFullName) == bytes:

            sCxTeamFullName = sCxTeamFullName.decode("utf-8");

        if sCxTeamFullName != None:

            sCxTeamFullName = sCxTeamFullName.strip();

        if sCxTeamFullName == None or \
            len(sCxTeamFullName) < 1:

            return;

        sCxTeamId = cxteamid;

        if sCxTeamId != None:

            sCxTeamId = sCxTeamId.strip();

        if sCxTeamId == None or \
            len(sCxTeamId) < 1:

            sCxTeamId = "";

        if self.dictCxAllTeams == None:

            self.dictCxAllTeams = collections.defaultdict();

        self.dictCxAllTeams[sCxTeamFullName] = sCxTeamId;

    def getCxProjectMetaDataAllPresets(self):

        return self.dictCxAllPresets;

    def addCxProjectMetaDataAllPresets(self, cxpresetname=None, cxpresetdict=None):

        sCxPresetName = cxpresetname;

        if sCxPresetName != None and \
            type(sCxPresetName) == bytes:

            sCxPresetName = sCxPresetName.decode("utf-8");

        if sCxPresetName != None:

            sCxPresetName = sCxPresetName.strip();

        if sCxPresetName == None or \
            len(sCxPresetName) < 1:

            return;

        dictCxPreset = cxpresetdict;

        if dictCxPreset == None or \
            len(dictCxPreset) < 1:

            return;

        if self.dictCxAllPresets == None:

            self.dictCxAllPresets = collections.defaultdict();

        self.dictCxAllPresets[sCxPresetName] = dictCxPreset;

    def getCxProjectMetaDataAllEngineConfigurations(self):

        return self.dictCxAllEngineConfigurations;

    def addCxProjectMetaDataAllEngineConfigurations(self, cxengineconfigname=None, cxengineconfigid=None):

        sCxEngineConfigName = cxengineconfigname;

        if sCxEngineConfigName != None and \
            type(sCxEngineConfigName) == bytes:

            sCxEngineConfigName = sCxEngineConfigName.decode("utf-8");

        if sCxEngineConfigName != None:

            sCxEngineConfigName = sCxEngineConfigName.strip();

        if sCxEngineConfigName == None or \
            len(sCxEngineConfigName) < 1:

            return;

        sCxEngineConfigId = cxengineconfigid;

        if sCxEngineConfigId != None:

            sCxEngineConfigId = sCxEngineConfigId.strip();

        if sCxEngineConfigId == None or \
            len(sCxEngineConfigId) < 1:

            sCxEngineConfigId = "";

        if self.dictCxAllEngineConfigurations == None:

            self.dictCxAllEngineConfigurations = collections.defaultdict();

        self.dictCxAllEngineConfigurations[sCxEngineConfigName] = sCxEngineConfigId;

    def getCxProjectMetaDataAllProjects(self):

        return self.dictCxAllProjects;

    def addCxProjectMetaDataAllProjects(self, cxprojectdata=None):

        cxProjectData = cxprojectdata;

        if cxProjectData == None:

            return;

        sCxProjectDataName = cxProjectData.getCxProjectName();

        if sCxProjectDataName != None:

            sCxProjectDataName = sCxProjectDataName.strip();

        if sCxProjectDataName == None or \
            len(sCxProjectDataName) < 1:

            return;

        if self.dictCxAllProjects == None:

            self.dictCxAllProjects = collections.defaultdict();

        self.dictCxAllProjects[sCxProjectDataName] = cxProjectData;

    def getCxApplicationZipper(self):

        return self.cxApplicationZipper;

    def setCxApplicationZipper(self, cxapplicationzipper=None):

        self.cxApplicationZipper = cxapplicationzipper;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The 'bSearchRecursiveFlag' boolean is [%s]..." % (self.sClassDisp, self.bSearchRecursiveFlag));
            print("%s The 'bSearchCaseSensitive' boolean is [%s]..." % (self.sClassDisp, self.bSearchCaseSensitive));
            print("%s The contents of 'sSearchDirectory' is [%s]..." % (self.sClassDisp, self.sSearchDirectory));
            print("%s The contents of 'sSearchFilePatterns' is [%s]..." % (self.sClassDisp, self.sSearchFilePatterns));
            print("%s The contents of 'listProjectCreationPropertiesFiles' is [%s]..." % (self.sClassDisp, self.listProjectCreationPropertiesFiles));
            print("%s The contents of 'listProjectCreationPlistFiles' is [%s]..." % (self.sClassDisp, self.listProjectCreationPlistFiles));

            if self.cxServerEndpoint == None:

                print("%s The 'cxServerEndpoint' has NOT been set..." % (self.sClassDisp));

            else:

                print("%s The 'cxServerEndpoint' is [%s]..." % (self.sClassDisp, self.cxServerEndpoint));

            if self.dictCxProjectCreationCollection == None:

                print("%s The 'dictCxProjectCreationCollection' has NOT been set..." % (self.sClassDisp));

            else:

                print("%s The 'dictCxProjectCreationCollection' is [%s]..." % (self.sClassDisp, self.dictCxProjectCreationCollection));

            print("%s The contents of 'asCxProjectCreationCollectionReport' is [%s]..." % (self.sClassDisp, self.asCxProjectCreationCollectionReport));
            print("%s The contents of 'bCxProjectWasCreatedByRestAPIFlag' is [%s]..." % (self.sClassDisp, self.bCxProjectWasCreatedByRestAPIFlag));
            print("%s The contents of 'dictCxAllTeams' is [%s]..." % (self.sClassDisp, self.dictCxAllTeams));
            print("%s The contents of 'dictCxAllPresets' is [%s]..." % (self.sClassDisp, self.dictCxAllPresets));
            print("%s The contents of 'dictCxAllEngineConfigurations' is [%s]..." % (self.sClassDisp, self.dictCxAllEngineConfigurations));
            print("%s The contents of 'dictCxAllProjects' is [%s]..." % (self.sClassDisp, self.dictCxAllProjects));
            print("%s The contents of 'cxApplicationZipper' is [%s]..." % (self.sClassDisp, self.cxApplicationZipper));
            print("%s The contents of 'dictCxProjectCreationCollectionStats' is [%s]..." % (self.sClassDisp, self.dictCxProjectCreationCollectionStats));
            print("%s The contents of 'listProjectCreationPropertiesKeys' is [%s]..." % (self.sClassDisp, self.listProjectCreationPropertiesKeys));
            print("%s The contents of 'cxProjectCreationCollectionDefaults' is [%s]..." % (self.sClassDisp, self.cxProjectCreationCollectionDefaults));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'bSearchRecursiveFlag' is [%s], " % (self.bSearchRecursiveFlag));
        asObjDetail.append("'bSearchCaseSensitive' is [%s], " % (self.bSearchCaseSensitive));
        asObjDetail.append("'sSearchDirectory' is [%s], " % (self.sSearchDirectory));
        asObjDetail.append("'sSearchFilePatterns' is [%s], " % (self.sSearchFilePatterns));
        asObjDetail.append("'listProjectCreationPropertiesFiles' is [%s], " % (self.listProjectCreationPropertiesFiles));
        asObjDetail.append("'listProjectCreationPlistFiles' is [%s], " % (self.listProjectCreationPlistFiles));
        asObjDetail.append("'cxServerEndpoint' is [%s], " % (self.cxServerEndpoint));
        asObjDetail.append("'dictCxProjectCreationCollection' is [%s], " % (self.dictCxProjectCreationCollection));
        asObjDetail.append("'asCxProjectCreationCollectionReport' is [%s], " % (self.asCxProjectCreationCollectionReport));
        asObjDetail.append("'bCxProjectWasCreatedByRestAPIFlag' is [%s], " % (self.bCxProjectWasCreatedByRestAPIFlag));
        asObjDetail.append("'dictCxAllTeams' is [%s], " % (self.dictCxAllTeams));
        asObjDetail.append("'dictCxAllPresets' is [%s], " % (self.dictCxAllPresets));
        asObjDetail.append("'dictCxAllEngineConfigurations' is [%s], " % (self.dictCxAllEngineConfigurations));
        asObjDetail.append("'dictCxAllProjects' is [%s], " % (self.dictCxAllProjects));
        asObjDetail.append("'cxApplicationZipper' is [%s], " % (self.cxApplicationZipper));
        asObjDetail.append("'dictCxProjectCreationCollectionStats' is [%s], " % (self.dictCxProjectCreationCollectionStats));
        asObjDetail.append("'listProjectCreationPropertiesKeys' is [%s], " % (self.listProjectCreationPropertiesKeys));
        asObjDetail.append("'cxProjectCreationCollectionDefaults' is [%s]. " % (self.cxProjectCreationCollectionDefaults));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def dumpCxProjectCreationCollectionDefaultsFromSuppliedObject(self):
 
    #   self.bTraceFlag = True;
 
        if self.cxProjectCreationCollectionDefaults == None:
 
            print("");
            print("%s NO CxProjectCreationCollectionDefaults object has been specified nor defined for this Checkmarx CxProject(s) Collection - one MUST be defined - Error!" % (self.sClassDisp));
            print("");
 
            return False;
 
        bProcessingError = False;
 
        try:

            print("");
            print(" = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =");
            print("");
            print("%s cxProjectCreationCollectionDefaults.getTraceFlag() returned [%s]..." % (self.sClassDisp, self.cxProjectCreationCollectionDefaults.getTraceFlag()));
            print("%s cxProjectCreationCollectionDefaults.getDefaultCxProjectTeamName() returned [%s]..." % (self.sClassDisp, self.cxProjectCreationCollectionDefaults.getDefaultCxProjectTeamName()));
            print("%s cxProjectCreationCollectionDefaults.getDefaultCxProjectPresetName() returned [%s]..." % (self.sClassDisp, self.cxProjectCreationCollectionDefaults.getDefaultCxProjectPresetName()));
            print("%s cxProjectCreationCollectionDefaults.getDefaultCxProjectMobilePresetName() returned [%s]..." % (self.sClassDisp, self.cxProjectCreationCollectionDefaults.getDefaultCxProjectMobilePresetName()));
            print("");
            print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
            print("");
        #   print("%s cxProjectCreationCollectionDefaults.() returned [%s]..." % (self.sClassDisp, self.cxProjectCreationCollectionDefaults.()));
        #   print("");
            print(" = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =");
            print("");
 
        except Exception as inst:
 
            print("%s 'dumpCxProjectCreationCollectionDefaultsFromSuppliedObject()' - exception occured..." % (self.sClassDisp));
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

    def loadCxProjectCreationCollectionFromPropertiesFiles(self):

    #   self.bTraceFlag = True;

        if self.cxServerEndpoint == None:

            print("");
            print("%s NO CxServerEndpoint has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxServerEndpoint.getCxServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.sSearchDirectory == None or \
           len(self.sSearchDirectory) < 1:

            print("");
            print("%s The supplied 'search' Directory (to be input from) 'sSearchDirectory' is None or Empty - Severe Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.sSearchFilePatterns == None or \
           len(self.sSearchFilePatterns) < 1:

            print("");
            print("%s The supplied 'search' File Patterns to be scanned for 'sSearchFilePatterns' is None or Empty - defaulting to '*.properties' - Warning!" % (self.sClassDisp));
            print("");

            self.setSearchFilePatterns(searchfilepatterns="*.properties");

        else:

            print("");
            print("%s The supplied 'search' File Patterns to be scanned for 'sSearchFilePatterns' is [%s]..." % (self.sClassDisp, self.sSearchFilePatterns));
            print("");

        self.listProjectCreationPropertiesFiles = None;

        bProcessingError = False;

        try:

            drcDirSearch = DrcDirectoryFileSearch1.DrcDirectoryFileSearcher(trace=self.bTraceFlag, searchrecursive=self.bSearchRecursiveFlag, searchcasesensitive=self.bSearchCaseSensitive, searchdirectories=self.sSearchDirectory, searchfilepatterns=self.sSearchFilePatterns);

            drcDirSearch.searchDirectoriesForFiles();

            if self.bTraceFlag == True:

                print("%s 'drcDirSearch' (after search) is [%s]..." % (self.sClassDisp, drcDirSearch.toString()));
                print("");

            asFileSearchResults = drcDirSearch.renderDictSearchResultsAsList();

            if self.bTraceFlag == True:

                print("%s 'asFileSearchResults' [list] (after search) is:" % (self.sClassDisp));
                print(asFileSearchResults);
                print("");

            if asFileSearchResults == None or \
               len(asFileSearchResults) < 1:

                print("%s Directory search produced a File(s) listing array that is 'null' or Empty - Error!" % (self.sClassDisp));

                return False;

            print("%s Directory search produced a File(s) listing array with (%d) elements..." % (self.sClassDisp, len(asFileSearchResults)));
            print("");

            idProjectCreationPropertiesFile = 0;

            for sProjectCreationPropertiesFile in asFileSearchResults:

                sProjectCreationPropertiesFilespec = os.path.realpath(sProjectCreationPropertiesFile);
                bProjectCreationPropertiesIsFile   = os.path.isfile(sProjectCreationPropertiesFilespec);

                if bProjectCreationPropertiesIsFile == False:

                    print("%s Command received a Project Creation 'properties' filespec of [%s] that does NOT exist - Error!" % (self.sClassDisp, sProjectCreationPropertiesFilespec));

                    continue;

                idProjectCreationPropertiesFile += 1;

                if self.bTraceFlag == True:

                    print("%s Command is adding a Project Creation 'properties' filespec #(%d) of [%s]..." % (self.sClassDisp, idProjectCreationPropertiesFile, sProjectCreationPropertiesFilespec));
                    print("");

                if self.listProjectCreationPropertiesFiles == None:

                    self.listProjectCreationPropertiesFiles = list();

                self.listProjectCreationPropertiesFiles.append(sProjectCreationPropertiesFilespec);

                print("%s Command added a Project Creation 'properties' filespec #(%d) of [%s]..." % (self.sClassDisp, idProjectCreationPropertiesFile, sProjectCreationPropertiesFilespec));

            bLoadPropFilesOk = self.loadProjectCreationPropertiesFilesToCollection();

            if bLoadPropFilesOk == None:
         
                print("");
                print("%s 'loadProjectCreationPropertiesFilesToCollection()' API call failed - Error!" % (self.sClassDisp));
                print("");
         
                return False;

        except Exception as inst:

            print("%s 'loadCxProjectCreationCollectionFromPropertiesFiles()' - exception occured..." % (self.sClassDisp));
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

    def loadProjectCreationPropertiesFilesToCollection(self):

    #   self.bTraceFlag = True;

        if self.listProjectCreationPropertiesFiles == None or \
           len(self.listProjectCreationPropertiesFiles) < 1:

            print("%s The generated Project Creation 'properties' file(s) 'search' List is None or Empty - Severe Error!" % (self.sClassDisp));

            return False;

        bProcessingError = False;

        try:

            idProjectCreationPropertiesFile = 0;

            for sProjectCreationPropertiesFile in self.listProjectCreationPropertiesFiles:

                idProjectCreationPropertiesFile += 1;

                if sProjectCreationPropertiesFile != None:

                    sProjectCreationPropertiesFile = sProjectCreationPropertiesFile.strip();

                if sProjectCreationPropertiesFile == None or \
                   len(sProjectCreationPropertiesFile) < 1:

                    if self.bTraceFlag == True:

                        print("%s The Project Creation 'properties' file #(%d) has a name that is None or Empty - bypassing the entry..." % (self.sClassDisp, idProjectCreationPropertiesFile));
                        print("");

                    continue;

                sProjectCreationPropertiesFilespec = os.path.realpath(sProjectCreationPropertiesFile);
                bProjectCreationPropertiesIsFile   = os.path.isfile(sProjectCreationPropertiesFilespec);

                if bProjectCreationPropertiesIsFile == False:

                    print("%s Command received a Project Creation 'properties' #(%d) filespec of [%s] that does NOT exist - bypassing the entry - Error!" % (self.sClassDisp, idProjectCreationPropertiesFile, sProjectCreationPropertiesFilespec));

                    continue;

                cProjectCreationPropertiesFile = os.path.getsize(sProjectCreationPropertiesFilespec);

                if self.bTraceFlag == True:

                    print("%s Loading a Project Creation 'properties' #(%d) filespec of [%s] containing (%d) bytes..." % (self.sClassDisp, idProjectCreationPropertiesFile, sProjectCreationPropertiesFilespec, cProjectCreationPropertiesFile));
                    print("");

                bLoadProjectCreationPropertiesFileOk = self.loadProjectCreationPropertiesFile(projectcreationpropertiesfile=sProjectCreationPropertiesFilespec);

                if bLoadProjectCreationPropertiesFileOk == None:

                    print("");
                    print("%s 'loadProjectCreationPropertiesFile()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                print("%s Loaded a Project Creation 'properties' #(%d) filespec of [%s] containing (%d) bytes..." % (self.sClassDisp, idProjectCreationPropertiesFile, sProjectCreationPropertiesFilespec, cProjectCreationPropertiesFile));

        except Exception as inst:

            print("%s 'loadProjectCreationPropertiesFilesToCollection()' - exception occured..." % (self.sClassDisp));
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

    def loadProjectCreationPropertiesFile(self, projectcreationpropertiesfile=None):

    #   self.bTraceFlag = True;

        sProjectCreationPropertiesFile = projectcreationpropertiesfile;

        if sProjectCreationPropertiesFile != None:
         
            sProjectCreationPropertiesFile = sProjectCreationPropertiesFile.strip();
         
        if sProjectCreationPropertiesFile == None or \
           len(sProjectCreationPropertiesFile) < 1:
         
            print("");
            print("%s The supplied Project Creation 'properties' file is 'None' or Empty - Severe Error!" % (self.sClassDisp));

            return False;

        bProjectCreationPropertiesIsFile = os.path.isfile(sProjectCreationPropertiesFile);

        if bProjectCreationPropertiesIsFile == False:

            print("");
            print("%s The supplied Project Creation 'properties' file [%s] does NOT exist - bypassing the file - Warning!" % (self.sClassDisp, sProjectCreationPropertiesFile));

            return False;

        cProjectCreationPropertiesFile = os.path.getsize(sProjectCreationPropertiesFile);

        print("");
        print("%s Loading the supplied Project Creation 'properties' from the file [%s] containing (%d) bytes of data..." % (self.sClassDisp, sProjectCreationPropertiesFile, cProjectCreationPropertiesFile));
        print("");

        sFieldProjectName   = None;
        sFieldProjectTier   = None;
        sFieldProjectVastId = None;
        cxProjectCreation1  = None;

        try:

            asProjectCreationProperties = list();
            fProjectCreationProperties  = open(sProjectCreationPropertiesFile, "r");
            asProjectCreationProperties = fProjectCreationProperties.readlines();

            fProjectCreationProperties.close();

            if len(asProjectCreationProperties) < 1:

                print("%s Command has processed a Project Creation 'properties' filespec of [%s] with (0) input lines - Warning!" % (self.sClassDisp, sProjectCreationPropertiesFile));

                return False;

            idProjectCreationPropertiesLine = 0;
            dictProjectCreationProperties   = None;

            for sProjectCreationPropertiesLine in asProjectCreationProperties:

                idProjectCreationPropertiesLine += 1;

                sProjectCreationPropertiesLine = sProjectCreationPropertiesLine.strip();

                if sProjectCreationPropertiesLine == None or \
                   len(sProjectCreationPropertiesLine) < 1:

                    continue;

                if self.bTraceFlag == True:

                    print("%s Reading a Project Creation 'properties' text line #(%d) of (%d) as [%s]..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine));

                if sProjectCreationPropertiesLine.startswith('#') == True:

                    if self.bTraceFlag == True:

                        print("%s Bypassing Project Creation 'properties' text line #(%d) of (%d) as [%s] is a 'comment'..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine));

                    continue;

                if self.bTraceFlag == True:

                    print("%s Processing a Project Creation 'properties' text line #(%d) of (%d) as [%s]..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine));

                # --------------------------------------------------------------------------------------------------
                # #REQUIRED FIELDS
                # #VERIZON
                # #this is a label for the project for reporting purposes
                # project.name=Black Duck
                #
                # #this is the repoversion of the project for reporting purposes... alphanumeric, max length 255
                # project.version=2019-10-31
                #
                # #options: alphanumeric 255
                # project.team=ACSS
                #
                # #options:public/department/private/adom_group [*SDLC_<role_name>]
                # project.visibility=public
                #
                # #REQUIRED FIELDS
                # #CHECKMARX (-None-)
                #
                # #OPTIONAL FIELDS
                # #VERIZON
                # project.language.list=java,c,scala
                #
                # vast.id=24436
                #
                # #OPTIONAL FIELDS
                # #CHECKMARX
                # project.cx.teamname=\CxServer\SP\Company\Users
                # project.cx.presetname=Checkmarx Default
                # project.cx.branches=Branch1,Branch2,Branch3,Branch4
                #
                # #NOT CURRENTLY USED FIELDS (but could be)
                # #options: prod/nonprod/sit/uat/qa/dev
                # project.tier=prod
                # --------------------------------------------------------------------------------------------------

                asProjectCreationPropertiesFields = sProjectCreationPropertiesLine.partition("=");

                if asProjectCreationPropertiesFields == None or \
                    len(asProjectCreationPropertiesFields) < 1:

                    if self.bTraceFlag == True:

                        print("%s Bypassing Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list that is None or 'empty'..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine));

                    continue;

                if len(asProjectCreationPropertiesFields) < 3:

                    if self.bTraceFlag == True:

                        print("%s Bypassing Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) that is less than 3..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields)));

                    continue;

                sProjectCreationPropertiesKey = asProjectCreationPropertiesFields[0];

                if sProjectCreationPropertiesKey != None:

                    sProjectCreationPropertiesKey = sProjectCreationPropertiesKey.strip();

                if sProjectCreationPropertiesKey == None or \
                    len(sProjectCreationPropertiesKey) < 1:

                    if self.bTraceFlag == True:

                        print("%s Bypassing Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) but the 'key' (1st field) is None or 'empty'..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields)));

                    continue;

                sProjectCreationPropertiesKeyLow = sProjectCreationPropertiesKey.lower();
                sProjectCreationPropertiesValue  = asProjectCreationPropertiesFields[2];

                if sProjectCreationPropertiesValue != None:

                    sProjectCreationPropertiesValue = sProjectCreationPropertiesValue.strip();

                if sProjectCreationPropertiesValue == None or \
                    len(sProjectCreationPropertiesValue) < 1:

                    if self.bTraceFlag == True:

                        print("%s The Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] but the 'value' (2nd field) is None or 'empty' - bypassing the line..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow));

                    continue;

                print("%s Verifying the Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] and a 'value' (2nd field) of [%s]..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow, sProjectCreationPropertiesValue));

                # --------------------------------------------------------------------------------------------------
                # listProjectCreationPropertiesKeys = ["project.name",
                #                                      "project.team",
                #                                      "project.version",
                #                                      "project.tier",
                #                                      "project.visibility",
                #                                      "project.language.list",
                #                                      "project.cx.branches",
                #                                      "project.cx.teamname"
                #                                      "project.cx.presetname"
                #                                      "vast.id"];
                # --------------------------------------------------------------------------------------------------

                if sProjectCreationPropertiesKeyLow not in self.listProjectCreationPropertiesKeys:

                    if self.bTraceFlag == True:

                        print("%s Bypassing Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] and a 'value' (2nd field) of [%s] is NOT a processable 'key'..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow, sProjectCreationPropertiesValue));

                    continue;

                print("%s Turning the Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] and a 'value' (2nd field) of [%s] into a CxProjectCreation object field..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow, sProjectCreationPropertiesValue));

                if dictProjectCreationProperties == None:

                    dictProjectCreationProperties = collections.defaultdict(); 

                dictProjectCreationProperties[sProjectCreationPropertiesKeyLow] = sProjectCreationPropertiesValue;

                if cxProjectCreation1 == None:

                    cxProjectCreation1 = CxProjectCreation1.CxProjectCreation(trace=self.bTraceFlag, cxprojectispublic=True, cxprojectteamname=self.cxProjectCreationCollectionDefaults.getDefaultCxProjectTeamName(), cxprojectpresetname=self.cxProjectCreationCollectionDefaults.getDefaultCxProjectPresetName(), cxprojectengineconfigname="Default Configuration");

                    if cxProjectCreation1 == None:

                        print("");
                        print("%s Failed to create a CxProjectCreation object - Error!" % (self.sClassDisp));
                        print("");

                        return False;

                if sProjectCreationPropertiesKeyLow == "project.name":

                    sFieldProjectName = sProjectCreationPropertiesValue.replace(' ', '-');

                if sProjectCreationPropertiesKeyLow == "project.team":

                    cxProjectCreation1.setCxProjectTeam(cxprojectteam=sProjectCreationPropertiesValue); 

                if sProjectCreationPropertiesKeyLow == "project.version":

                    cxProjectCreation1.setCxProjectVersion(cxprojectversion=sProjectCreationPropertiesValue); 

                if sProjectCreationPropertiesKeyLow == "project.tier":        

                    sFieldProjectTier = sProjectCreationPropertiesValue;

                if sProjectCreationPropertiesKeyLow == "project.visibility":

                    sProjectCreationPropertiesValueLow = sProjectCreationPropertiesValue.lower();

                    if sProjectCreationPropertiesValueLow == "private":

                        cxProjectCreation1.setCxProjectIsPublic(cxprojectispublic=False); 

                    else:

                        cxProjectCreation1.setCxProjectIsPublic(cxprojectispublic=True); 

                if sProjectCreationPropertiesKeyLow == "project.language.list":

                    sProjectCreationPropertiesValueLow = sProjectCreationPropertiesValue.lower();
                    asSetProjectLangList               = sProjectCreationPropertiesValueLow.split(',');

                    if self.bTraceFlag == True:

                        print("%s <Debug> Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] and a 'value' (2nd field) of [%s] produces a 'value' list of #(%d) item(s) of [%s]..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow, sProjectCreationPropertiesValue, len(asSetProjectLangList), asSetProjectLangList));

                    if asSetProjectLangList == None or \
                        len(asSetProjectLangList) < 2:

                        cxProjectCreation1.setCxProjectEngineConfigName(cxprojectengineconfigname="Default Configuration"); 

                        if self.bTraceFlag == True:

                            print("%s <Debug> Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] and a 'value' (2nd field) of [%s] produces a 'value' list of #(%d) item(s) of [%s] and set 'EngineConfig' to \"Default Configuration\"..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow, sProjectCreationPropertiesValue, len(asSetProjectLangList), asSetProjectLangList));

                    else:

                        cxProjectCreation1.setCxProjectEngineConfigName(cxprojectengineconfigname="Multi-language Scan"); 

                        if self.bTraceFlag == True:

                            print("%s <Debug> Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] and a 'value' (2nd field) of [%s] produces a 'value' list of #(%d) item(s) of [%s] and set 'EngineConfig' to \"Multi-language Scan\"..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow, sProjectCreationPropertiesValue, len(asSetProjectLangList), asSetProjectLangList));

                    if "android" in asSetProjectLangList or \
                        "swift"  in asSetProjectLangList or \
                        "objc"   in asSetProjectLangList or \
                        "obj-c"  in asSetProjectLangList:

                        cxProjectCreation1.setCxProjectPresetName(cxprojectpresetname=self.cxProjectCreationCollectionDefaults.getDefaultCxProjectMobilePresetName());

                if sProjectCreationPropertiesKeyLow == "project.cx.branches":

                    if self.bTraceFlag == True:

                        print("%s <Debug> Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] and a 'value' (2nd field) of [%s]..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow, sProjectCreationPropertiesValue));

                    asSetProjectBranchesList = sProjectCreationPropertiesValue.split(',');

                    if self.bTraceFlag == True:

                        print("%s <Debug> Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] and a 'value' (2nd field) of [%s] produces a 'value' list of #(%d) item(s) of [%s]..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow, sProjectCreationPropertiesValue, len(asSetProjectBranchesList), asSetProjectBranchesList));

                    cxProjectCreation1.setCxProjectBranchNames(cxprojectbranchnames=asSetProjectBranchesList);

                    if self.bTraceFlag == True:

                        print("%s <Debug> Project Creation 'properties' text line #(%d) of (%d) as [%s] parsed into a 'field(s)' list of #(%d) field(s) with a 'key' (1st field) of [%s] and a 'value' (2nd field) of [%s] and set the Project 'branches' to [%s]..." % (self.sClassDisp, idProjectCreationPropertiesLine, len(asProjectCreationProperties), sProjectCreationPropertiesLine, len(asProjectCreationPropertiesFields), sProjectCreationPropertiesKeyLow, sProjectCreationPropertiesValue, asSetProjectBranchesList));

                if sProjectCreationPropertiesKeyLow == "project.cx.teamname":

                    cxProjectCreation1.setCxProjectTeamName(cxprojectteamname=sProjectCreationPropertiesValue); 

                if sProjectCreationPropertiesKeyLow == "project.cx.presetname":

                    cxProjectCreation1.setCxProjectPresetName(cxprojectpresetname=sProjectCreationPropertiesValue); 

                if sProjectCreationPropertiesKeyLow == "vast.id": 

                    sFieldProjectVastId = sProjectCreationPropertiesValue;

            if cxProjectCreation1 != None:

                cxProjectCreation1.setCxProjectBaseName(cxprojectbasename=self.cxProjectCreationCollectionDefaults.getCxProjectBaseName(cxprojectcreation=cxProjectCreation1, dictprojectcreationproperties=dictProjectCreationProperties));
                cxProjectCreation1.setCxProjectName(cxprojectname=self.cxProjectCreationCollectionDefaults.getCxProjectName(cxprojectcreation=cxProjectCreation1, dictprojectcreationproperties=dictProjectCreationProperties)); 
                cxProjectCreation1.setCxProjectScanType(cxprojectscantype="sast");
                cxProjectCreation1.setCxProjectBranchNames(cxprojectbranchnames=self.cxProjectCreationCollectionDefaults.getExtraCxProjectBranchNames(cxprojectcreation=cxProjectCreation1, dictprojectcreationproperties=dictProjectCreationProperties));  
                cxProjectCreation1.setCxProjectTeamName(cxprojectteamname=self.cxProjectCreationCollectionDefaults.getCxProjectTeamName(cxprojectcreation=cxProjectCreation1, dictprojectcreationproperties=dictProjectCreationProperties));  

                bAddProjCreationToCollectionOk = self.addCxProjectCreationToCxProjectCreationCollection(cxprojectcreation=cxProjectCreation1);

                if bAddProjCreationToCollectionOk == False:

                    print("");
                    print("%s The 'addCxProjectCreationToCxProjectCreationCollection()' call failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                dictProjectCreationProperties = None;
                cxProjectCreation1            = None;

        # --------------------------------------------------------------------------------------------------
        #
        # Replaced by the new 'exit' logic in CxProjectCreationCollectionDefaults1.py:
        #
        #       sGeneratedProjectName = "";
        #
        #       if sFieldProjectVastId != None:
        #
        #           sFieldProjectVastId = sFieldProjectVastId.strip();
        #
        #       if sFieldProjectVastId != None and \
        #           len(sFieldProjectVastId) > 0:
        #
        #           sGeneratedProjectName = sFieldProjectVastId;
        #
        #       if sFieldProjectName != None:
        #
        #           sFieldProjectName = sFieldProjectName.strip();
        #
        #       if sFieldProjectName != None and \
        #           len(sFieldProjectName) > 0:
        #
        #           if sGeneratedProjectName != None:
        #
        #               sGeneratedProjectName = sGeneratedProjectName.strip();
        #
        #           if sGeneratedProjectName == None or \
        #               len(sGeneratedProjectName) < 1:
        #
        #               sGeneratedProjectName = sFieldProjectName;
        #
        #           else:
        #
        #               sGeneratedProjectName = "%s-%s" % (sGeneratedProjectName, sFieldProjectName);
        #
        #       cxProjectCreation1.setCxProjectBaseName(cxprojectbasename=sGeneratedProjectName); 
        #
        #       sGeneratedProjectName = "%s_Main" % (sGeneratedProjectName);
        #
        #   #   if sFieldProjectTier != None:
        #   #
        #   #       sFieldProjectTier = sFieldProjectTier.strip();
        #   #
        #   #   if sFieldProjectTier != None and \
        #   #       len(sFieldProjectTier) > 0:
        #   #
        #   #       if sGeneratedProjectName != None:
        #   #
        #   #           sGeneratedProjectName = sGeneratedProjectName.strip();
        #   #
        #   #       if sGeneratedProjectName == None or \
        #   #           len(sGeneratedProjectName) < 1:
        #   #
        #   #           sGeneratedProjectName = sFieldProjectTier;
        #   #
        #   #       else:
        #   #
        #   #           sGeneratedProjectName = "%s_%s" % (sGeneratedProjectName, sFieldProjectTier);
        #
        #       cxProjectCreation1.setCxProjectName(cxprojectname=sGeneratedProjectName); 
        #
        #       sFieldProjectTeam = cxProjectCreation1.getCxProjectTeam();
        #
        #       if sFieldProjectTeam != None:
        #
        #           sFieldProjectTeam = sFieldProjectTeam.strip();
        #
        #       if sFieldProjectTeam != None and \
        #           len(sFieldProjectTeam) > 0:
        #
        #           if cxProjectCreation1.asCxProjectBranchNames == None:
        #
        #               cxProjectCreation1.asCxProjectBranchNames = [];
        #
        #           cxProjectCreation1.asCxProjectBranchNames.append(sFieldProjectTeam);
        #
        #       if sFieldProjectName != None:
        #
        #           sFieldProjectName = sFieldProjectName.strip();
        #
        #       if sFieldProjectName != None and \
        #           len(sFieldProjectName) > 0:
        #
        #           sCxProjectTeamName = cxProjectCreation1.getCxProjectTeamName();
        #
        #           if sCxProjectTeamName != None:
        #
        #               sCxProjectTeamName = sCxProjectTeamName.strip();
        #
        #           if sCxProjectTeamName != None and \
        #               len(sCxProjectTeamName) > 0:
        #
        #               if sCxProjectTeamName.endswith(sFieldProjectName) == False:
        #
        #                   cxProjectCreation1.setCxProjectTeamName(cxprojectteamname=("%s\\%s" % (sCxProjectTeamName, sFieldProjectName)));
        #
        #           else:
        #
        #               cxProjectCreation1.setCxProjectTeamName(cxprojectteamname=("%s\\%s" % (self.cxProjectCreationCollectionDefaults.getDefaultCxProjectTeamName(), sFieldProjectName)));
        #
        # --------------------------------------------------------------------------------------------------

        except Exception as inst:

            print("%s 'loadProjectCreationPropertiesFile()' - load of the Project Creation 'properties' file [%s] - operational exception occured..." % (self.sClassDisp, sProjectCreationPropertiesFile));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def loadCxProjectCreationCollectionFromPlistFiles(self):

    #   self.bTraceFlag = True;

        if self.cxServerEndpoint == None:

            print("");
            print("%s NO CxServerEndpoint has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxServerEndpoint.getCxServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.sSearchDirectory == None or \
           len(self.sSearchDirectory) < 1:

            print("");
            print("%s The supplied 'search' Directory (to be input from) 'sSearchDirectory' is None or Empty - Severe Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.sSearchFilePatterns == None or \
           len(self.sSearchFilePatterns) < 1:

            print("");
            print("%s The supplied 'search' File Patterns to be scanned for 'sSearchFilePatterns' is None or Empty - defaulting to '*.plist' - Warning!" % (self.sClassDisp));
            print("");

            self.setSearchFilePatterns(searchfilepatterns="*.plist");

        else:

            print("");
            print("%s The supplied 'search' File Patterns to be scanned for 'sSearchFilePatterns' is [%s]..." % (self.sClassDisp, self.sSearchFilePatterns));
            print("");

        self.listProjectCreationPlistFiles = None;

        bProcessingError = False;

        try:

            drcDirSearch = DrcDirectoryFileSearch1.DrcDirectoryFileSearcher(trace=self.bTraceFlag, searchrecursive=self.bSearchRecursiveFlag, searchcasesensitive=self.bSearchCaseSensitive, searchdirectories=self.sSearchDirectory, searchfilepatterns=self.sSearchFilePatterns);

            drcDirSearch.searchDirectoriesForFiles();

            if self.bTraceFlag == True:

                print("%s 'drcDirSearch' (after search) is [%s]..." % (self.sClassDisp, drcDirSearch.toString()));
                print("");

            asFileSearchResults = drcDirSearch.renderDictSearchResultsAsList();

            if self.bTraceFlag == True:

                print("%s 'asFileSearchResults' [list] (after search) is:" % (self.sClassDisp));
                print(asFileSearchResults);
                print("");

            if asFileSearchResults == None or \
               len(asFileSearchResults) < 1:

                print("%s Directory search produced a File(s) listing array that is 'null' or Empty - Error!" % (self.sClassDisp));

                return False;

            print("%s Directory search produced a File(s) listing array with (%d) elements..." % (self.sClassDisp, len(asFileSearchResults)));
            print("");

            idProjectCreationPlistFile = 0;

            for sProjectCreationPlistFile in asFileSearchResults:

                sProjectCreationPlistFilespec = os.path.realpath(sProjectCreationPlistFile);
                bProjectCreationPlistIsFile   = os.path.isfile(sProjectCreationPlistFilespec);

                if bProjectCreationPlistIsFile == False:

                    print("%s Command received a Project Creation 'plist' filespec of [%s] that does NOT exist - Error!" % (self.sClassDisp, sProjectCreationPlistFilespec));

                    continue;

                idProjectCreationPlistFile += 1;

                if self.bTraceFlag == True:

                    print("%s Command is adding a Project Creation 'plist' filespec #(%d) of [%s]..." % (self.sClassDisp, idProjectCreationPlistFile, sProjectCreationPlistFilespec));
                    print("");

                if self.listProjectCreationPlistFiles == None:

                    self.listProjectCreationPlistFiles = list();

                self.listProjectCreationPlistFiles.append(sProjectCreationPlistFilespec);

                print("%s Command added a Project Creation 'plist' filespec #(%d) of [%s]..." % (self.sClassDisp, idProjectCreationPlistFile, sProjectCreationPlistFilespec));

            bLoadPlistFilesOk = self.loadProjectCreationPlistFilesToCollection();

            if bLoadPlistFilesOk == None:
         
                print("");
                print("%s 'loadProjectCreationPlistFilesToCollection()' API call failed - Error!" % (self.sClassDisp));
                print("");
         
                return False;

        except Exception as inst:

            print("%s 'loadCxProjectCreationCollectionFromPlistFiles()' - exception occured..." % (self.sClassDisp));
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

    def loadProjectCreationPlistFilesToCollection(self):

    #   self.bTraceFlag = True;

        if self.listProjectCreationPlistFiles == None or \
           len(self.listProjectCreationPlistFiles) < 1:

            print("%s The generated Project Creation 'plist' file(s) 'search' List is None or Empty - Severe Error!" % (self.sClassDisp));

            return False;

        bProcessingError = False;

        try:

            idProjectCreationPlistFile = 0;

            for sProjectCreationPlistFile in self.listProjectCreationPlistFiles:

                idProjectCreationPlistFile += 1;

                if sProjectCreationPlistFile != None:

                    sProjectCreationPlistFile = sProjectCreationPlistFile.strip();

                if sProjectCreationPlistFile == None or \
                   len(sProjectCreationPlistFile) < 1:

                    if self.bTraceFlag == True:

                        print("%s The Project Creation 'plist' file #(%d) has a name that is None or Empty - bypassing the entry..." % (self.sClassDisp, idProjectCreationPlistFile));
                        print("");

                    continue;

                sProjectCreationPlistFilespec = os.path.realpath(sProjectCreationPlistFile);
                bProjectCreationPlistIsFile   = os.path.isfile(sProjectCreationPlistFilespec);

                if bProjectCreationPlistIsFile == False:

                    print("%s Command received a Project Creation 'plist' #(%d) filespec of [%s] that does NOT exist - bypassing the entry - Error!" % (self.sClassDisp, idProjectCreationPlistFile, sProjectCreationPlistFilespec));

                    continue;

                cProjectCreationPlistFile = os.path.getsize(sProjectCreationPlistFilespec);

                if self.bTraceFlag == True:

                    print("%s Loading a Project Creation 'plist' #(%d) filespec of [%s] containing (%d) bytes..." % (self.sClassDisp, idProjectCreationPlistFile, sProjectCreationPlistFilespec, cProjectCreationPlistFile));
                    print("");

                bLoadProjectCreationPlistFileOk = self.loadProjectCreationPlistFile(projectcreationplistfile=sProjectCreationPlistFilespec);

                if bLoadProjectCreationPlistFileOk == None:

                    print("");
                    print("%s 'loadProjectCreationPlistFile()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                print("%s Loaded a Project Creation 'plist' #(%d) filespec of [%s] containing (%d) bytes..." % (self.sClassDisp, idProjectCreationPlistFile, sProjectCreationPlistFilespec, cProjectCreationPlistFile));

        except Exception as inst:

            print("%s 'loadProjectCreationPlistFilesToCollection()' - exception occured..." % (self.sClassDisp));
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

    def loadProjectCreationPlistFile(self, projectcreationplistfile=None):

    #   self.bTraceFlag = True;

        sProjectCreationPlistFile = projectcreationplistfile;

        if sProjectCreationPlistFile != None:
         
            sProjectCreationPlistFile = sProjectCreationPlistFile.strip();
         
        if sProjectCreationPlistFile == None or \
           len(sProjectCreationPlistFile) < 1:
         
            print("");
            print("%s The supplied Project Creation 'plist' file is 'None' or Empty - Severe Error!" % (self.sClassDisp));

            return False;

        bProjectCreationPlistIsFile = os.path.isfile(sProjectCreationPlistFile);

        if bProjectCreationPlistIsFile == False:

            print("");
            print("%s The supplied Project Creation 'plist' file [%s] does NOT exist - bypassing the file - Warning!" % (self.sClassDisp, sProjectCreationPlistFile));

            return False;

        cProjectCreationPlistFile = os.path.getsize(sProjectCreationPlistFile);

        print("");
        print("%s Loading the supplied Project Creation 'plist' from the file [%s] containing (%d) bytes of data..." % (self.sClassDisp, sProjectCreationPlistFile, cProjectCreationPlistFile));
        print("");

        cxProjectCreation1 = None;

        try:

            asProjectCreationPlist = list();

            with open(sProjectCreationPlistFile, 'rb') as fProjectCreationPlist:

                dictProjectCreationPlist = plistlib.load(fProjectCreationPlist);

            print("%s Command read the (Input) 'plist' file of [%s] into 'dictProjectCreationPlist'..." % (self.sClassDisp, cProjectCreationPlistFile));
            print("%s The OBJECT 'dictProjectCreationPlist' Type [%s] is [%s]..." % (self.sClassDisp, type(dictProjectCreationPlist), dictProjectCreationPlist));

            if type(dictProjectCreationPlist) != dict:

                print("%s Command has processed a Project Creation 'plist' filespec of [%s] producing a 'dictProjectCreationPlist' object that is NOT of type(dict) - Error!" % (self.sClassDisp, sProjectCreationPlistFile));

                return False;

            if dictProjectCreationPlist == None or \
               len(dictProjectCreationPlist) < 1:

                print("%s Command has processed a Project Creation 'plist' filespec of [%s] producing a 'dictProjectCreationPlist' that is None or Empty - Error!" % (self.sClassDisp, sProjectCreationPlistFile));

                return False;

            # --------------------------------------------------------------------------------------------------
            # <dict>
            #     <key>AppCollectionName</key>
            #     <string>JWebsoftwareDev</string>
            #     <key>AppIsActive</key>
            #     <string>true</string>
            #     <key>AppName</key>
            #     <string>JWS_App-Project_1</string>
            #     <key>AppProjectId</key>
            #     <string>dc408339-e04f-4582-9b50-65e9182fcb3a</string>
            #     <key>AppScanType</key>
            #     <string>both</string>
            #     <key>AppRepos</key>
            #     <array>
            #         <dict>
            #             <key>RepoBranches</key>
            #             <array>
            #                 <dict>
            #                     <key>BranchIsActive</key>
            #                     <string>true</string>
            #                     <key>BranchName</key>
            #                     <string>refs/heads/master</string>
            #                 </dict>
            #             </array>
            #             <key>RepoIsActive</key>
            #             <string>true</string>
            #             <key>RepoRemoteURL</key>
            #             <string>http://darylc-laptop:9080/tfs/JWebsoftwareDev/_git/JWS_App-Project_1</string>
            #             <key>RepoSshURL</key>
            #             <string>ssh://darylc-laptop:22/tfs/JWebsoftwareDev/_git/JWS_App-Project_1</string>
            #             <key>RepoTitle</key>
            #             <string>JWS_App-Project_1</string>
            #             <key>RepoURL</key>
            #             <string>http://192.168.2.190:9080/tfs/JWebsoftwareDev/_apis/git/repositories/6f23a004-735a-4df6-909b-17571d9f06b1</string>
            #         </dict>
            #     </array>
            # </dict>
            # --------------------------------------------------------------------------------------------------

            sCxProjectName = dictProjectCreationPlist["AppName"];

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                sCxProjectName = None;

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the Project(s)/Branch(s) 'creation' of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            sCxProjectIsActive = dictProjectCreationPlist["AppIsActive"]; 

            if sCxProjectIsActive != None:

                sCxProjectIsActive = sCxProjectIsActive.strip();

            if sCxProjectIsActive == None or \
                len(sCxProjectIsActive) < 1:

                sCxProjectIsActive = "false";

            sCxProjectIsActiveLow = sCxProjectIsActive.lower();

            if sCxProjectIsActiveLow == "false":

                print("");
                print("%s The CxProjectCreation named [%s] is marked NOT 'active' - bypassing the Project(s)/Branch(s) 'creation' of this object - Error!" % (self.sClassDisp, sCxProjectName));
                print("");

                return False;

            if cxProjectCreation1 == None:

                cxProjectCreation1 = CxProjectCreation1.CxProjectCreation(trace=self.bTraceFlag, cxprojectispublic=True, cxprojectteamname=self.cxProjectCreationCollectionDefaults.getDefaultCxProjectTeamName(), cxprojectpresetname=self.cxProjectCreationCollectionDefaults.getDefaultCxProjectPresetName(), cxprojectengineconfigname="Default Configuration");

                if cxProjectCreation1 == None:

                    print("");
                    print("%s Failed to create a CxProjectCreation object - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            cxProjectCreation1.setCxProjectBaseName(cxprojectbasename=sCxProjectName);
            cxProjectCreation1.setCxProjectName(cxprojectname=sCxProjectName);

            if "AppScanType" in dictProjectCreationPlist.keys():

                cxProjectCreation1.setCxProjectScanType(cxprojectscantype=dictProjectCreationPlist["AppScanType"]);

            else:

                cxProjectCreation1.setCxProjectScanType(cxprojectscantype="both");

            cxProjectCreation1.setCxProjectEngineConfigName(cxprojectengineconfigname="Multi-language Scan");

            if "AppCollectionName" in dictProjectCreationPlist.keys():

                cxProjectCreation1.setCxProjectExtraField1(cxprojectextrafield1=dictProjectCreationPlist["AppCollectionName"]);

            else:

                if "AppGroupName" in dictProjectCreationPlist.keys():

                    cxProjectCreation1.setCxProjectExtraField1(cxprojectextrafield1=dictProjectCreationPlist["AppGroupName"]);

                else:

                    cxProjectCreation1.setCxProjectExtraField1(cxprojectextrafield1="Default");

            cxProjectCreation1.setCxProjectExtraField2(cxprojectextrafield2=dictProjectCreationPlist["AppRepos"]);

            if "AppCreateBranches" in dictProjectCreationPlist.keys():

                sAppCreateBranches = dictProjectCreationPlist["AppCreateBranches"];

                if sAppCreateBranches != None:

                    sAppCreateBranches = sAppCreateBranches.strip();

                if sAppCreateBranches == None or \
                    len(sAppCreateBranches) < 1:

                    sAppCreateBranches = "false";

                sAppCreateBranchesLow = sAppCreateBranches.lower();

                if sAppCreateBranchesLow == "true":

                    listAppRepos = dictProjectCreationPlist["AppRepos"];

                    if listAppRepos != None and \
                        len(listAppRepos) > 0:

                        asAppRepoBranches = [];

                        for dictAppRepo in listAppRepos:

                            if dictAppRepo == None:

                                continue;

                            listAppRepoBranches = dictAppRepo["RepoBranches"];

                            if listAppRepoBranches != None and \
                                len(listAppRepoBranches) > 0:

                                for dictAppRepoBranch in listAppRepoBranches:

                                    if dictAppRepoBranch == None:

                                        continue;

                                    sAppRepoBranchName   = dictAppRepoBranch["BranchName"];
                                    sAppRepoBranchActive = dictAppRepoBranch["BranchIsActive"];

                                    if sAppRepoBranchActive != None:

                                        sAppRepoBranchActive = sAppRepoBranchActive.strip();

                                    if sAppRepoBranchActive == None or \
                                        len(sAppRepoBranchActive) < 1:

                                        sAppRepoBranchActive = "false";

                                    sAppRepoBranchActiveLow = sAppRepoBranchActive.lower();

                                    if sAppRepoBranchActiveLow == "true":

                                        asAppRepoBranches.append(sAppRepoBranchName);

                        if asAppRepoBranches != None and \
                            len(asAppRepoBranches) > 0:

                            cxProjectCreation1.setCxProjectBranchNames(cxprojectbranchnames=asAppRepoBranches);

            bAddProjCreationToCollectionOk = self.addCxProjectCreationToCxProjectCreationCollection(cxprojectcreation=cxProjectCreation1);

            if bAddProjCreationToCollectionOk == False:

                print("");
                print("%s The 'addCxProjectCreationToCxProjectCreationCollection()' call failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            dictProjectCreationPlist = None;
            cxProjectCreation1       = None;

        except Exception as inst:

            print("%s 'loadProjectCreationPlistFile()' - load of the Project Creation 'plist' file [%s] - operational exception occured..." % (self.sClassDisp, sProjectCreationPlistFile));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def loadCxProjectCreationMetaDataToCollectionFromRestAPI(self):

    #   self.bTraceFlag = True;

        if self.cxServerEndpoint == None:

            print("");
            print("%s NO CxServerEndpoint has been specified nor defined for the Checkmarx CxProject(s) Collection - one CxServerEndpoint MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxServerEndpoint.getCxServerEndpointActiveFlag() == False:

            print("");
            print("%s The supplied CxServerEndpoint is NOT marked 'active' - it MUST be marked 'active' to be used - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        self.dictCxAllTeams                = None;
        self.dictCxAllPresets              = None;
        self.dictCxAllEngineConfigurations = None;
        self.dictCxAllProjects             = None;

        try:

            self.cxProjCreationBase = CxRestAPIProjectCreationBase1.CxRestAPIProjectCreationBase(trace=self.bTraceFlag, cxserverendpoint=self.cxServerEndpoint, cxprojectcreationcollection=self);

            if self.cxProjCreationBase == None:

                print("");
                print("%s Failed to create a CxRestAPIProjectCreationBase object - Error!" % (self.sClassDisp));
                print("");

                return False;

            bGetProjMetaOk = self.cxProjCreationBase.getCxRestAPIProjectCreationMetaData();

            if bGetProjMetaOk == False:

                print("");
                print("%s 'cxProjCreationBase.getCxRestAPIProjectCreationMetaData()' API call failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'loadCxProjectCreationMetaDataToCollectionFromRestAPI()' - exception occured..." % (self.sClassDisp));
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

    def addCxProjectCreationToCxProjectCreationCollection(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined for the Checkmarx CxProjectCreation(s) Collection - one CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.dictCxProjectCreationCollection == None:

            if self.bTraceFlag == True:

                print("%s The object 'dictCxProjectCreationCollection' has NOT been set - creating an internal instance..." % (self.sClassDisp));

            self.dictCxProjectCreationCollection = collections.defaultdict(); 

        bProcessingError = False;

        try:

            sCxProjectName = cxProjectCreation.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the addition of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            self.dictCxProjectCreationCollection[sCxProjectName] = cxProjectCreation;

            if self.bTraceFlag == True:

                print("%s CxProjectCreation named [%s] added to the CxProjectCreationCollection..." % (self.sClassDisp, sCxProjectName));

        except Exception as inst:

            print("%s 'addCxProjectCreationToCxProjectCreationCollection()' - exception occured..." % (self.sClassDisp));
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

    def createCxProjectsAndBranchesFromCxProjectCreationCollection(self):

    #   self.bTraceFlag = True;

        if self.dictCxProjectCreationCollection == None or \
            len(self.dictCxProjectCreationCollection) < 1:

            if self.bTraceFlag == True:

                print("%s The object 'dictCxProjectCreationCollection' is None or 'empty' - NO Cx Project(s) and/or Branch(s) to create - Warning..." % (self.sClassDisp));

            return True;

        bProcessingError = False;

        try:

            print("");
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
            print("%s Creating Cx Project(s) and/or Branch(s) for a CxProjectCreation(s) collection of (%d) element(s):" % (self.sClassDisp, len(self.dictCxProjectCreationCollection)));
            print("");

            cCxProjectCreation = 0;

            for sCxProjectName in list(self.dictCxProjectCreationCollection.keys()):

                cCxProjectCreation += 1;

                cxProjectCreation = self.dictCxProjectCreationCollection[sCxProjectName];

                if cxProjectCreation == None:

                    continue;

                sCxProjectName = cxProjectCreation.getCxProjectName();

                if sCxProjectName != None:

                    sCxProjectName = sCxProjectName.strip();

                if sCxProjectName == None or \
                    len(sCxProjectName) < 1:

                    print("");
                    print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the creation of this object [%s] - Error!" % (self.sClassDisp, cxProjectCreation));
                    print("");

                    bProcessingError = True;

                    continue;

                if self.bTraceFlag == True:

                    print("%s CxProjectCreation (%d) of (%d) named [%s] of [%s] is being 'created'..." % (self.sClassDisp, cCxProjectCreation, len(self.dictCxProjectCreationCollection), sCxProjectName, cxProjectCreation));

                bResolveNamesToIdsOk = self.resolveCxProjectNamesToIds(cxprojectcreation=cxProjectCreation);

                if bResolveNamesToIdsOk == False:

                    if self.dictCxAllProjects != None and \
                        len(self.dictCxAllProjects) > 0:

                        print("");
                        print("%s 'resolveCxProjectNamesToIds()' API call failed - Error!" % (self.sClassDisp));
                        print("");

                        bProcessingError = True;

                        continue;

                if self.bTraceFlag == True:

                    print("%s CxProjectCreation (%d) of (%d) named [%s] of [%s] after Names-to-IDs 'resolution'..." % (self.sClassDisp, cCxProjectCreation, len(self.dictCxProjectCreationCollection), sCxProjectName, cxProjectCreation));

                bCreateProjectsAndBranchesOk = self.createCxProjectsAndBranches(cxprojectcreation=cxProjectCreation);

                if bCreateProjectsAndBranchesOk == False:

                    print("");
                    print("%s 'createCxProjectsAndBranches()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    bProcessingError = True;

                    continue;

                if self.bTraceFlag == True:

                    print("%s CxProjectCreation (%d) of (%d) named [%s] of [%s] after Project(s)/Branch(s) 'creation'..." % (self.sClassDisp, cCxProjectCreation, len(self.dictCxProjectCreationCollection), sCxProjectName, cxProjectCreation));

        except Exception as inst:

            print("%s 'createCxProjectsAndBranchesFromCxProjectCreationCollection()' - exception occured..." % (self.sClassDisp));
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

    def resolveCxProjectNamesToIds(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined for the Checkmarx CxProjectCreation(s) Collection - one CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            # Set the various Project Id(s):

            sCxProjectName = cxProjectCreation.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the Names-to-IDs 'resolution' for this Project name - Warning!" % (self.sClassDisp));
                print("");

            else:

                bCxProjectNameFound = False;

                if self.dictCxAllProjects != None and \
                    len(self.dictCxAllProjects) > 0:

                    if sCxProjectName in list(self.dictCxAllProjects.keys()):

                        bCxProjectNameFound = True;

                        cxProjectData = self.dictCxAllProjects[sCxProjectName];

                        if cxProjectData != None:

                            cxProjectCreation.setCxProjectId(cxprojectid=cxProjectData.getCxProjectId());

                if bCxProjectNameFound == False:

                    if self.bTraceFlag == True:

                        print("%s Failed to find the CxProject 'name' of [%s] in key(s) of [%s] in dictionary of 'self.dictCxAllProjects' of [%s]..." % (self.sClassDisp, sCxProjectName, list(self.dictCxAllProjects.keys()), self.dictCxAllProjects));

            sCxProjectTeamName = cxProjectCreation.getCxProjectTeamName();

            if sCxProjectTeamName != None:

                sCxProjectTeamName = sCxProjectTeamName.strip();

            if sCxProjectTeamName != None and \
                len(sCxProjectTeamName) > 0:

                bCxProjectTeamNameFound = False;

                if self.dictCxAllTeams != None and \
                    len(self.dictCxAllTeams) > 0:

                    if sCxProjectTeamName in list(self.dictCxAllTeams.keys()):

                        bCxProjectTeamNameFound = True;

                        cxProjectCreation.setCxProjectTeamId(cxprojectteamid=self.dictCxAllTeams[sCxProjectTeamName]);

                if bCxProjectTeamNameFound == False:

                    if self.bTraceFlag == True:

                        print("%s Failed to find the CxProject Team 'name' of [%s] in key(s) of [%s] in dictionary of 'self.dictCxAllTeams' of [%s]..." % (self.sClassDisp, sCxProjectTeamName, list(self.dictCxAllTeams.keys()), self.dictCxAllTeams));

            sCxProjectPresetName = cxProjectCreation.getCxProjectPresetName();

            if sCxProjectPresetName != None:

                sCxProjectPresetName = sCxProjectPresetName.strip();

            if sCxProjectPresetName != None and \
                len(sCxProjectPresetName) > 0:

                bCxProjectPresetNameFound = False;

                if self.dictCxAllPresets != None and \
                    len(self.dictCxAllPresets) > 0:

                    if sCxProjectPresetName in list(self.dictCxAllPresets.keys()):

                        bCxProjectPresetNameFound = True;

                        dictProjectPreset = self.dictCxAllPresets[sCxProjectPresetName];

                        if dictProjectPreset != None:

                            cxProjectCreation.setCxProjectPresetId(cxprojectpresetid=dictProjectPreset["id"]);

                if bCxProjectPresetNameFound == False:

                    if self.bTraceFlag == True:

                        print("%s Failed to find the CxProject Preset 'name' of [%s] in key(s) of [%s] in dictionary of 'self.dictCxAllPresets' of [%s]..." % (self.sClassDisp, sCxProjectPresetName, list(self.dictCxAllPresets.keys()), self.dictCxAllPresets));

            sCxProjectEngineConfigName = cxProjectCreation.getCxProjectEngineConfigName();

            if sCxProjectEngineConfigName != None:

                sCxProjectEngineConfigName = sCxProjectEngineConfigName.strip();

            if sCxProjectEngineConfigName != None and \
                len(sCxProjectEngineConfigName) > 0:

                bCxProjectEngineConfigNameFound = False;

                if self.dictCxAllEngineConfigurations != None and \
                    len(self.dictCxAllEngineConfigurations) > 0:

                    if sCxProjectEngineConfigName in list(self.dictCxAllEngineConfigurations.keys()):

                        bCxProjectEngineConfigNameFound = True;

                        cxProjectCreation.setCxProjectEngineConfigId(cxprojectengineconfigid=self.dictCxAllEngineConfigurations[sCxProjectEngineConfigName]);

                if bCxProjectEngineConfigNameFound == False:

                    if self.bTraceFlag == True:

                        print("%s Failed to find the CxProject EngineConfiguration 'name' of [%s] in key(s) of [%s] in dictionary of 'self.dictCxAllEngineConfigurations' of [%s]..." % (self.sClassDisp, sCxProjectEngineConfigName, list(self.dictCxAllEngineConfigurations.keys()), self.dictCxAllEngineConfigurations));

            # Validate the 'required' Project Id(s).
            #
            # NOTE: The Project Id field may be None or < 1. This indicates that we need to create the 'parent' Project before creating 'Branch(s)'.

            sCxProjectTeamId = cxProjectCreation.getCxProjectTeamId();

            if sCxProjectTeamId != None:

                sCxProjectTeamId = sCxProjectTeamId.strip();

            if sCxProjectTeamId == None or \
                len(sCxProjectTeamId) < 1:

                print("%s The CxProject Team 'id' of [%s] in the CxProjectCreation object [%s] is 'invalid' - Warning!" % (self.sClassDisp, sCxProjectTeamId, cxProjectCreation));

                bProcessingError = True;

            sCxProjectPresetId = cxProjectCreation.getCxProjectPresetId();

            if sCxProjectPresetId != None:

                sCxProjectPresetId = sCxProjectPresetId.strip();

            if sCxProjectPresetId == None or \
                len(sCxProjectPresetId) < 1 or \
                int(sCxProjectPresetId) < 1:

                print("%s The CxProject Preset 'id' of [%s] in the CxProjectCreation object [%s] is 'invalid' - Warning!" % (self.sClassDisp, sCxProjectPresetId, cxProjectCreation));

                bProcessingError = True;

            sCxProjectEngineConfigId = cxProjectCreation.getCxProjectEngineConfigId();

            if sCxProjectEngineConfigId != None:

                sCxProjectEngineConfigId = sCxProjectEngineConfigId.strip();

            if sCxProjectEngineConfigId == None or \
                len(sCxProjectEngineConfigId) < 1 or \
                int(sCxProjectEngineConfigId) < 1:

                print("%s The CxProject EngineConfiguration 'id' of [%s] in the CxProjectCreation object [%s] is 'invalid' - Warning!" % (self.sClassDisp, sCxProjectEngineConfigId, cxProjectCreation));

                bProcessingError = True;

        except Exception as inst:

            print("%s 'resolveCxProjectNamesToIds()' - exception occured..." % (self.sClassDisp));
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

    def createCxProjectsAndBranches(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined for the Checkmarx CxProjectCreation(s) Collection - one CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            sCxProjectName = cxProjectCreation.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the Project(s)/Branch(s) 'creation' of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.cxProjCreationBase == None:

                self.cxProjCreationBase = CxRestAPIProjectCreationBase1.CxRestAPIProjectCreationBase(trace=self.bTraceFlag, cxserverendpoint=self.cxServerEndpoint, cxprojectcreationcollection=self);

                if self.cxProjCreationBase == None:

                    print("");
                    print("%s Failed to create a CxRestAPIProjectCreationBase object - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            bCreateProjAndBranchesOk = self.cxProjCreationBase.createCxRestAPIProjectAndBranches(cxprojectcreation=cxProjectCreation);

            if bCreateProjAndBranchesOk == False:

                print("");
                print("%s 'cxProjCreationBase.createCxRestAPIProjectAndBranches()' API call failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            bGatherProjStats = self.gatherCxProjectCreationStatistics(cxprojectcreation=cxProjectCreation);

            if bGatherProjStats == False:

                print("");
                print("%s 'gatherCxProjectCreationStatistics()' API call failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'createCxProjectsAndBranches()' - exception occured..." % (self.sClassDisp));
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

    def gatherCxProjectCreationStatistics(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined for the Checkmarx CxProjectCreation(s) Collection - one CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            # Gather 'longest' field 'width' stats:

            sCxProjectName = cxProjectCreation.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the gathering of stats for this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            if len(sCxProjectName) > self.dictCxProjectCreationCollectionStats["cWidthCxProjectName"]:

                self.dictCxProjectCreationCollectionStats["cWidthCxProjectName"] = len(sCxProjectName);

            sCxProjectId = cxProjectCreation.getCxProjectId();

            if sCxProjectId != None:

                sCxProjectId = sCxProjectId.strip();

            if sCxProjectId != None   and \
                len(sCxProjectId) > 0 and \
                len(sCxProjectId) > self.dictCxProjectCreationCollectionStats["cWidthCxProjectId"]:

                    self.dictCxProjectCreationCollectionStats["cWidthCxProjectId"] = len(sCxProjectId);

            sCxProjectTeamName = cxProjectCreation.getCxProjectTeamName();

            if sCxProjectTeamName != None:

                sCxProjectTeamName = sCxProjectTeamName.strip();

            if sCxProjectTeamName != None   and \
                len(sCxProjectTeamName) > 0 and \
                len(sCxProjectTeamName) > self.dictCxProjectCreationCollectionStats["cWidthCxProjectTeamName"]:

                    self.dictCxProjectCreationCollectionStats["cWidthCxProjectTeamName"] = len(sCxProjectTeamName);

            sCxProjectTeamId = cxProjectCreation.getCxProjectTeamId();

            if sCxProjectTeamId != None:

                sCxProjectTeamId = sCxProjectTeamId.strip();

            if sCxProjectTeamId != None   and \
                len(sCxProjectTeamId) > 0 and \
                len(sCxProjectTeamId) > self.dictCxProjectCreationCollectionStats["cWidthCxProjectTeamId"]:

                    self.dictCxProjectCreationCollectionStats["cWidthCxProjectTeamId"] = len(sCxProjectTeamId);

            sCxProjectPresetName = cxProjectCreation.getCxProjectPresetName();

            if sCxProjectPresetName != None:

                sCxProjectPresetName = sCxProjectPresetName.strip();

            if sCxProjectPresetName != None   and \
                len(sCxProjectPresetName) > 0 and \
                len(sCxProjectPresetName) > self.dictCxProjectCreationCollectionStats["cWidthCxProjectPresetName"]:

                    self.dictCxProjectCreationCollectionStats["cWidthCxProjectPresetName"] = len(sCxProjectPresetName);

            sCxProjectPresetId = cxProjectCreation.getCxProjectPresetId();

            if sCxProjectPresetId != None:

                sCxProjectPresetId = sCxProjectPresetId.strip();

            if sCxProjectPresetId != None   and \
                len(sCxProjectPresetId) > 0 and \
                len(sCxProjectPresetId) > self.dictCxProjectCreationCollectionStats["cWidthCxProjectPresetId"]:

                    self.dictCxProjectCreationCollectionStats["cWidthCxProjectPresetId"] = len(sCxProjectPresetId);

            sCxProjectEngineConfigName = cxProjectCreation.getCxProjectEngineConfigName();

            if sCxProjectEngineConfigName != None:

                sCxProjectEngineConfigName = sCxProjectEngineConfigName.strip();

            if sCxProjectEngineConfigName != None   and \
                len(sCxProjectEngineConfigName) > 0 and \
                len(sCxProjectEngineConfigName) > self.dictCxProjectCreationCollectionStats["cWidthCxProjectEngineConfigName"]:

                    self.dictCxProjectCreationCollectionStats["cWidthCxProjectEngineConfigName"] = len(sCxProjectEngineConfigName);

            sCxProjectEngineConfigId = cxProjectCreation.getCxProjectEngineConfigId();

            if sCxProjectEngineConfigId != None:

                sCxProjectEngineConfigId = sCxProjectEngineConfigId.strip();

            if sCxProjectEngineConfigId != None   and \
                len(sCxProjectEngineConfigId) > 0 and \
                len(sCxProjectEngineConfigId) > self.dictCxProjectCreationCollectionStats["cWidthCxProjectEngineConfigId"]:

                    self.dictCxProjectCreationCollectionStats["cWidthCxProjectEngineConfigId"] = len(sCxProjectEngineConfigId);

        except Exception as inst:

            print("%s 'gatherCxProjectCreationStatistics()' - exception occured..." % (self.sClassDisp));
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

    def deleteCxProjectsAndBranchesFromCxProjectCreationCollection(self):

    #   self.bTraceFlag = True;

        if self.dictCxProjectCreationCollection == None or \
            len(self.dictCxProjectCreationCollection) < 1:

            if self.bTraceFlag == True:

                print("%s The object 'dictCxProjectCreationCollection' is None or 'empty' - NO Cx Project(s) and/or Branch(s) to delete - Warning..." % (self.sClassDisp));

            return True;

        bProcessingError = False;

        try:

            print("");
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
            print("%s Deleting Cx Project(s) and/or Branch(s) for a CxProjectCreation(s) collection of (%d) element(s):" % (self.sClassDisp, len(self.dictCxProjectCreationCollection)));
            print("");

            cCxProjectDeletion = 0;

            for sCxProjectName in list(self.dictCxProjectCreationCollection.keys()):

                cCxProjectDeletion += 1;

                cxProjectCreation = self.dictCxProjectCreationCollection[sCxProjectName];

                if cxProjectCreation == None:

                    continue;

                sCxProjectName = cxProjectCreation.getCxProjectName();

                if sCxProjectName != None:

                    sCxProjectName = sCxProjectName.strip();

                if sCxProjectName == None or \
                    len(sCxProjectName) < 1:

                    print("");
                    print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the deletion of this object [%s] - Error!" % (self.sClassDisp, cxProjectCreation));
                    print("");

                    bProcessingError = True;

                    continue;

                if self.bTraceFlag == True:

                    print("%s CxProjectCreation (%d) of (%d) named [%s] of [%s] is being 'deleted'..." % (self.sClassDisp, cCxProjectDeletion, len(self.dictCxProjectCreationCollection), sCxProjectName, cxProjectCreation));

                bResolveNamesToIdsOk = self.resolveCxProjectNamesToIds(cxprojectcreation=cxProjectCreation);

                if bResolveNamesToIdsOk == False:

                    if self.dictCxAllProjects != None and \
                        len(self.dictCxAllProjects) > 0:

                        print("");
                        print("%s 'resolveCxProjectNamesToIds()' API call failed - Error!" % (self.sClassDisp));
                        print("");

                        bProcessingError = True;

                        continue;

                if self.bTraceFlag == True:

                    print("%s CxProjectCreation (%d) of (%d) named [%s] of [%s] after Names-to-IDs 'resolution'..." % (self.sClassDisp, cCxProjectDeletion, len(self.dictCxProjectCreationCollection), sCxProjectName, cxProjectCreation));

                bDeleteProjectsAndBranchesOk = self.deleteCxProjectsAndBranches(cxprojectcreation=cxProjectCreation);

                if bDeleteProjectsAndBranchesOk == False:

                    print("");
                    print("%s 'deleteCxProjectsAndBranches()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    bProcessingError = True;

                    continue;

                if self.bTraceFlag == True:

                    print("%s CxProjectCreation (%d) of (%d) named [%s] of [%s] after Project(s)/Branch(s) 'deletion'..." % (self.sClassDisp, cCxProjectDeletion, len(self.dictCxProjectCreationCollection), sCxProjectName, cxProjectCreation));

        except Exception as inst:

            print("%s 'deleteCxProjectsAndBranchesFromCxProjectCreationCollection()' - exception occured..." % (self.sClassDisp));
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

    def deleteCxProjectsAndBranches(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined for the Checkmarx CxProjectCreation(s) Collection - one CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            sCxProjectName = cxProjectCreation.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the Project(s)/Branch(s) 'deletion' of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.cxProjCreationBase == None:

                self.cxProjCreationBase = CxRestAPIProjectCreationBase1.CxRestAPIProjectCreationBase(trace=self.bTraceFlag, cxserverendpoint=self.cxServerEndpoint, cxprojectcreationcollection=self);

                if self.cxProjCreationBase == None:

                    print("");
                    print("%s Failed to create a CxRestAPIProjectCreationBase object - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            bDeleteProjAndBranchesOk = self.cxProjCreationBase.deleteCxRestAPIProjectAndBranches(cxprojectcreation=cxProjectCreation);

            if bDeleteProjAndBranchesOk == False:

                print("");
                print("%s 'cxProjCreationBase.deleteCxRestAPIProjectAndBranches()' API call failed - Error!" % (self.sClassDisp));
                print("");

                return False;

            bGatherProjStats = self.gatherCxProjectCreationStatistics(cxprojectcreation=cxProjectCreation);

            if bGatherProjStats == False:

                print("");
                print("%s 'gatherCxProjectCreationStatistics()' API call failed - Error!" % (self.sClassDisp));
                print("");

                return False;

        except Exception as inst:

            print("%s 'deleteCxProjectsAndBranches()' - exception occured..." % (self.sClassDisp));
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

    def generateCxProjectCreationCollectionReport(self):
 
        bProcessingError = False;

        self.asCxProjectCreationCollectionReport = None;
 
        if self.dictCxProjectCreationCollection == None or \
           len(self.dictCxProjectCreationCollection) < 1:

            print("");
            print("%s NO Checkmarx CxProjectCreation(s) have been specified nor defined in the Checkmarx CxProjectCreation(s) Collection - at least 1 CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        try:

            asCxProjectCreationCollectionReportDebug = list();
            self.asCxProjectCreationCollectionReport = list();

            self.asCxProjectCreationCollectionReport.append("");
            self.asCxProjectCreationCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
            self.asCxProjectCreationCollectionReport.append("%s Checkmarx CxProjectCreation(s) collection for (%d) element(s):" % \
                                                            (self.sClassDisp, len(self.dictCxProjectCreationCollection)));
            self.asCxProjectCreationCollectionReport.append("");

            asCxProjectCreationCollectionReportDebug.append("");
            asCxProjectCreationCollectionReportDebug.append("- - - - - - - - - - - - - - - - DEBUG - - - - - - - - - - - - - - - - - - - - - -");
            asCxProjectCreationCollectionReportDebug.append("%s Checkmarx CxProjectCreation(s) collection for (%d) element(s):" % \
                                                       (self.sClassDisp, len(self.dictCxProjectCreationCollection)));
            asCxProjectCreationCollectionReportDebug.append("");

            cCxProjectCreationCollection = 0;

            for sCxProjectName in list(self.dictCxProjectCreationCollection.keys()):

                cCxProjectCreationCollection += 1;

                cxProjectCreation = self.dictCxProjectCreationCollection[sCxProjectName];

                if cxProjectCreation == None:

                    continue;

                self.asCxProjectCreationCollectionReport.append("%s CxProjectCreation element (%3d) of (%3d):" % \
                                                                (self.sClassDisp, cCxProjectCreationCollection, len(self.dictCxProjectCreationCollection)));
                self.asCxProjectCreationCollectionReport.append(cxProjectCreation.toPrettyStringWithWidths(dictcxprojectcreationcollectionstats=self.dictCxProjectCreationCollectionStats));

                if self.bTraceFlag == True:

                    asCxProjectCreationCollectionReportDebug.append("%s CxProjectCreation element (named '%s')[(%d) of (%d)] is:" % \
                                                            (self.sClassDisp, sCxProjectName, cCxProjectCreationCollection, len(self.dictCxProjectCreationCollection)));
                    asCxProjectCreationCollectionReportDebug.append(cxProjectCreation.toString());
                    asCxProjectCreationCollectionReportDebug.append("");

            self.asCxProjectCreationCollectionReport.append("");
            self.asCxProjectCreationCollectionReport.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
            self.asCxProjectCreationCollectionReport.append("");

            if self.bTraceFlag == True:

                asCxProjectCreationCollectionReportDebug.append("");
                asCxProjectCreationCollectionReportDebug.append("- - - - - - - - - - - - - - - - DEBUG - - - - - - - - - - - - - - - - - - - - - -");
                asCxProjectCreationCollectionReportDebug.append("");

                self.asCxProjectCreationCollectionReport.extend(asCxProjectCreationCollectionReportDebug);

        except Exception as inst:
 
            print("%s 'generateCxProjectCreationCollectionReport()' - exception occured..." % (self.sClassDisp));
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
 
    def saveCxProjectCreationCollectionReportToFile(self, outputprojectcreationcollectionfile=None):

    #   self.bTraceFlag = True;

        sOutputCxProjectCreationCollectionFile = outputprojectcreationcollectionfile;

        if sOutputCxProjectCreationCollectionFile != None:

            sOutputCxProjectCreationCollectionFile = sOutputCxProjectCreationCollectionFile.strip();

        if sOutputCxProjectCreationCollectionFile == None or \
           len(sOutputCxProjectCreationCollectionFile) < 1:

            print("%s Command received an (Output) CxProjectCreation Collection filename that is 'null' or Empty - Error!" % (self.sClassDisp));

            return False;

        if self.asCxProjectCreationCollectionReport == None or \
            len(self.asCxProjectCreationCollectionReport) < 1:

            print("");
            print("%s The CxProjectCreation Collection 'report' is 'None' or Empty - Severe Error!" % (self.sClassDisp));
 
            return False;

        try:

            print("%s Command is generating the (Output) CxProjectCreation Collection 'report' into a file of [%s]..." % (self.sClassDisp, sOutputCxProjectCreationCollectionFile));
            print("");

            fOutputCxProjectCreationCollection = open(sOutputCxProjectCreationCollectionFile, "w");

            fOutputCxProjectCreationCollection.write('\n'.join(self.asCxProjectCreationCollectionReport));
            fOutputCxProjectCreationCollection.close();

            print("%s Command generated the (Output) CxProjectCreation Collection 'report' into a file of [%s]..." % (self.sClassDisp, sOutputCxProjectCreationCollectionFile));
            print("");

        except Exception as inst:

            print("%s 'saveCxProjectCreationCollectionReportToFile()' - operational exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            excType, excValue, excTraceback = sys.exc_info();
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

            print("- - - ");
            print('\n'.join(asTracebackLines));
            print("- - - ");

            return False;

        return True;

    def scanCxProjectsViaPlistFromCollection(self):

    #   self.bTraceFlag = True;

        if self.dictCxProjectCreationCollection == None or \
            len(self.dictCxProjectCreationCollection) < 1:

            if self.bTraceFlag == True:

                print("%s The object 'dictCxProjectCreationCollection' is None or 'empty' - NO Cx Project(s) to scan - Warning..." % (self.sClassDisp));

            return True;

        bProcessingError = False;

        try:

            print("");
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
            print("%s Scanning Cx Project(s) for a CxProjectCreation(s) collection of (%d) element(s):" % (self.sClassDisp, len(self.dictCxProjectCreationCollection)));
            print("");

            cCxProjectCreation = 0;

            for sCxProjectName in list(self.dictCxProjectCreationCollection.keys()):

                cCxProjectCreation += 1;

                cxProjectCreation = self.dictCxProjectCreationCollection[sCxProjectName];

                if cxProjectCreation == None:

                    continue;

                sCxProjectName = cxProjectCreation.getCxProjectName();

                if sCxProjectName != None:

                    sCxProjectName = sCxProjectName.strip();

                if sCxProjectName == None or \
                    len(sCxProjectName) < 1:

                    print("");
                    print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the scanning of this object [%s] - Error!" % (self.sClassDisp, cxProjectCreation));
                    print("");

                    bProcessingError = True;

                    continue;

                if self.bTraceFlag == True:

                    print("%s CxProjectCreation (%d) of (%d) named [%s] of [%s] is being 'scanned'..." % (self.sClassDisp, cCxProjectCreation, len(self.dictCxProjectCreationCollection), sCxProjectName, cxProjectCreation));

                bResolveNamesToIdsOk = self.resolveCxProjectNamesToIds(cxprojectcreation=cxProjectCreation);

                if bResolveNamesToIdsOk == False:

                    if self.dictCxAllProjects != None and \
                        len(self.dictCxAllProjects) > 0:

                        print("");
                        print("%s 'resolveCxProjectNamesToIds()' API call failed - Error!" % (self.sClassDisp));
                        print("");

                        bProcessingError = True;

                        continue;

                if self.bTraceFlag == True:

                    print("%s CxProjectCreation (%d) of (%d) named [%s] of [%s] after Names-to-IDs 'resolution'..." % (self.sClassDisp, cCxProjectCreation, len(self.dictCxProjectCreationCollection), sCxProjectName, cxProjectCreation));

                bScanCxProjectOk = self.scanCxProjectFromCollection(cxprojectcreation=cxProjectCreation);

                if bScanCxProjectOk == False:

                    print("");
                    print("%s 'scanCxProjectFromCollection()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    bProcessingError = True;

                    continue;

                if self.bTraceFlag == True:

                    print("%s CxProjectCreation (%d) of (%d) named [%s] of [%s] after Project 'scan'..." % (self.sClassDisp, cCxProjectCreation, len(self.dictCxProjectCreationCollection), sCxProjectName, cxProjectCreation));

        except Exception as inst:

            print("%s 'scanCxProjectsViaPlistFromCollection()' - exception occured..." % (self.sClassDisp));
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

    def scanCxProjectFromCollection(self, cxprojectcreation=None):

    #   self.bTraceFlag = True;

        cxProjectCreation = cxprojectcreation;

        if cxProjectCreation == None:

            print("");
            print("%s NO CxProjectCreation has been specified nor defined for the Checkmarx CxProjectCreation(s) Collection - one CxProjectCreation MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.cxApplicationZipper == None:

            print("");
            print("%s NO CxApplicationZipper has been specified nor defined for the Checkmarx CxProjectCreation(s) Collection - one CxApplicationzipper MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        bProcessingError = False;

        try:

            sCxProjectName = cxProjectCreation.getCxProjectName();

            if sCxProjectName != None:

                sCxProjectName = sCxProjectName.strip();

            if sCxProjectName == None or \
                len(sCxProjectName) < 1:

                print("");
                print("%s The CxProjectCreation has a 'name' that is None or 'empty' - bypassing the Project 'scanning' of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            if self.cxProjCreationBase == None:

                self.cxProjCreationBase = CxRestAPIProjectCreationBase1.CxRestAPIProjectCreationBase(trace=self.bTraceFlag, cxserverendpoint=self.cxServerEndpoint, cxprojectcreationcollection=self);

                if self.cxProjCreationBase == None:

                    print("");
                    print("%s Failed to create a CxRestAPIProjectCreationBase object - Error!" % (self.sClassDisp));
                    print("");

                    return False;

            sCxProjectScanType = cxProjectCreation.getCxProjectScanType();

            if sCxProjectScanType != None:

                sCxProjectScanType = sCxProjectScanType.strip();

            if sCxProjectScanType == None or \
                len(sCxProjectScanType) < 1:

                sCxProjectScanType = "sast";

            if sCxProjectScanType == "both" or \
               sCxProjectScanType == "sast":

            # TEMP - replace with actual .zip file creation:
            #
            #   cxProjectCreation.setCxProjectSASTZipFilespec(cxprojectsastzipfilespec="/CheckMarx_Resources/CheckMarx.Demo/SQLInjectionSample_base/SQLInjectionSample.zip");
            #
            # TEMP - ...above...

                bGeneratedCxAppSASTZipOk = self.cxApplicationZipper.generateCxApplicationSASTZip(cxprojectcreation=cxProjectCreation);

                if bGeneratedCxAppSASTZipOk == False:

                    print("");
                    print("%s 'cxApplicationZipper.generateCxApplicationZip()' (SAST) API call failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                cxProjectCreation.setCxProjectSASTZipFilespec(cxprojectsastzipfilespec=self.cxApplicationZipper.getCxApplicationZip());

                bUploadCxProjectOk = self.cxProjCreationBase.uploadCxRestAPIProjectZip(cxprojectcreation=cxProjectCreation);

                if bUploadCxProjectOk == False:

                    print("");
                    print("%s 'cxProjCreationBase.uploadCxRestAPIProjectZip()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    bProcessingError = True;
                #   return False;

                else:

                    bScanCxProjectOk = self.cxProjCreationBase.scanCxRestAPIProject(cxprojectcreation=cxProjectCreation);

                    if bScanCxProjectOk == False:

                        print("");
                        print("%s 'cxProjCreationBase.scanCxRestAPIProject()' API call failed - Error!" % (self.sClassDisp));
                        print("");

                        bProcessingError = True;
                    #   return False;

            if sCxProjectScanType == "both" or \
               sCxProjectScanType == "osa":

            # TEMP - replace with actual .zip file creation:
            #
            #   cxProjectCreation.setCxProjectOSAZipFilespec(cxprojectosazipfilespec="/CheckMarx_Resources/CheckMarx.Demo/PHPMailer-master.zip");
            #
            # TEMP - ...above...

                bGeneratedCxAppOSAZipOk = self.cxApplicationZipper.generateCxApplicationOSAZip(cxprojectcreation=cxProjectCreation);

                if bGeneratedCxAppOSAZipOk == False:

                    print("");
                    print("%s 'cxApplicationZipper.generateCxApplicationZip()' (OSA) API call failed - Error!" % (self.sClassDisp));
                    print("");

                    return False;

                cxProjectCreation.setCxProjectOSAZipFilespec(cxprojectosazipfilespec=self.cxApplicationZipper.getCxApplicationZip());

                bScanOsaCxProjectOk = self.cxProjCreationBase.scanOsaCxRestAPIProject(cxprojectcreation=cxProjectCreation);

                if bScanOsaCxProjectOk == False:

                    print("");
                    print("%s 'cxProjCreationBase.scanOsaCxRestAPIProject()' API call failed - Error!" % (self.sClassDisp));
                    print("");

                    bProcessingError = True;
                #   return False;

        except Exception as inst:

            print("%s 'scanCxProjectFromCollection()' - exception occured..." % (self.sClassDisp));
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

