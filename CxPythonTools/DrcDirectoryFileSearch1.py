
import os;
import re;
import string;
import sys;
import collections;
import fnmatch;

class DrcDirectoryFileSearcher:

    sClassMod            = __name__;
    sClassId             = "DrcDirectoryFileSearcher";
    sClassVers           = "(v1.0501)";
    sClassDisp           = sClassMod+"."+sClassId+" "+sClassVers+":";

    bTraceFlag           = False;
    bSearchRecursiveFlag = False;
    bSearchCaseSensitive = False;

    sSearchDirectories   = None;
    sSearchFilePatterns  = None;

    ssSearchDirectories  = None;
    ssSearchFilePatterns = None;

    dictSearchResults    = None;

    def __init__(self, trace=False, searchrecursive=False, searchcasesensitive=False, searchdirectories=None, searchfilepatterns=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setSearchRecursiveFlag(searchrecursive=searchrecursive);
            self.setSearchCaseSensitiveFlag(searchcasesensitive=searchcasesensitive);
            self.setSearchDirectories(searchdirectories=searchdirectories);
            self.setSearchFilePatterns(searchfilepatterns=searchfilepatterns);

        except Exception as inst:

            print("%s '__init__()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

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

    def getSearchDirectories(self):

        return self.sSearchDirectories;

    def setSearchDirectories(self, searchdirectories=None):

        self.sSearchDirectories = searchdirectories;

        if self.sSearchDirectories == None or \
           len(self.sSearchDirectories) < 1:

            return;

        self.addSearchDirectories(searchdirectories=self.sSearchDirectories);

    def addSearchDirectories(self, searchdirectories=None):

        sSetSearchDirectories = searchdirectories;

        if sSetSearchDirectories == None or \
           len(sSetSearchDirectories) < 1:

            return;

        sSetSearchDirectories  = sSetSearchDirectories.strip();
        asSetSearchDirectories = sSetSearchDirectories.split(';');

        if asSetSearchDirectories == None or \
           len(asSetSearchDirectories) < 1:

            return;

        for sSetSearchDirectory in asSetSearchDirectories:

            sSetSearchDirectory = sSetSearchDirectory.strip();

            if sSetSearchDirectory == None or \
               len(sSetSearchDirectory) < 1:

                continue;

            self.addSearchDirectory(searchdirectory=sSetSearchDirectory);

    def addSearchDirectory(self, searchdirectory=None):

        sSearchDirectory = searchdirectory;

        if sSearchDirectory == None or \
           len(sSearchDirectory) < 1:

            return;

        sSearchDirectory = sSearchDirectory.strip();

        if self.ssSearchDirectories == None:

            self.ssSearchDirectories = set();

        self.ssSearchDirectories.add(sSearchDirectory);

    def getSSSearchDirectories(self):

        return self.ssSearchDirectories;

    def getSearchFilePatterns(self):

        return self.sSearchFilePatterns;

    def setSearchFilePatterns(self, searchfilepatterns=None):

        self.sSearchFilePatterns = searchfilepatterns;

        if self.sSearchFilePatterns == None or \
           len(self.sSearchFilePatterns) < 1:

            return;

        self.addSearchFilePatterns(searchfilepatterns=self.sSearchFilePatterns);

    def addSearchFilePatterns(self, searchfilepatterns=None):

        sSetSearchFilePatterns = searchfilepatterns;

        if sSetSearchFilePatterns == None or \
           len(sSetSearchFilePatterns) < 1:

            return;

        sSetSearchFilePatterns  = sSetSearchFilePatterns.strip();
        asSetSearchFilePatterns = sSetSearchFilePatterns.split(';');

        if asSetSearchFilePatterns == None or \
           len(asSetSearchFilePatterns) < 1:

            return;

        for sSetSearchFilePattern in asSetSearchFilePatterns:

            sSetSearchFilePattern = sSetSearchFilePattern.strip();

            if sSetSearchFilePattern == None or \
               len(sSetSearchFilePattern) < 1:

                continue;

            self.addSearchFilePattern(searchfilepattern=sSetSearchFilePattern);

    def addSearchFilePattern(self, searchfilepattern=None):

        sSearchFilePattern = searchfilepattern;

        if sSearchFilePattern == None or \
           len(sSearchFilePattern) < 1:

            return;

        sSearchFilePattern = sSearchFilePattern.strip();

        if self.ssSearchFilePatterns == None:

            self.ssSearchFilePatterns = set();

        self.ssSearchFilePatterns.add(sSearchFilePattern);

    def getSSSearchFilePatterns(self):

        return self.ssSearchFilePatterns;

    def getDictSearchResults(self):

        return self.dictSearchResults;

    def renderDictSearchResultsAsList(self):

        asSearchResultsList = list();

        if self.dictSearchResults == None or \
           len(self.dictSearchResults) < 1:

            return asSearchResultsList;

        if self.bTraceFlag == True:

            print("%s Processing the (%d) 'root' paths found..." % (self.sClassDisp, len(self.dictSearchResults)));

        for sRootPath in list(self.dictSearchResults.keys()):

            if sRootPath == None or \
               len(sRootPath) < 1:

                continue;

            if self.bTraceFlag == True:

                print("%s Processing the 'root' path of [%s]..." % (self.sClassDisp, sRootPath));

            asDirFiles = self.dictSearchResults[sRootPath];

            if asDirFiles == None or \
               len(asDirFiles) < 1:

                continue;

            if self.bTraceFlag == True:

                print("%s Processing the (%d) files in the 'root' path of [%s]..." % (self.sClassDisp, len(asDirFiles), sRootPath));

            for sDirFile in asDirFiles:

                if sDirFile == None or \
                   len(sDirFile) < 1:

                    continue;

                sFullyQualifiedFilename = os.path.join(sRootPath, sDirFile);

                if self.bTraceFlag == True:

                    print("%s Adding the fully-qualified Filename [%s] to the list..." % (self.sClassDisp, sFullyQualifiedFilename));

                asSearchResultsList.append(sFullyQualifiedFilename);

        return asSearchResultsList;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The 'bSearchRecursiveFlag' boolean is [%s]..." % (self.sClassDisp, self.bSearchRecursiveFlag));
            print("%s The 'bSearchCaseSensitive' boolean is [%s]..." % (self.sClassDisp, self.bSearchCaseSensitive));
            print("%s The contents of 'sSearchDirectories' is [%s]..." % (self.sClassDisp, self.sSearchDirectories));
            print("%s The contents of 'sSearchFilePatterns' is [%s]..." % (self.sClassDisp, self.sSearchFilePatterns));
            print("%s The contents of 'ssSearchDirectories' is [%s]..." % (self.sClassDisp, self.ssSearchDirectories));
            print("%s The contents of 'ssSearchFilePatterns' is [%s]..." % (self.sClassDisp, self.ssSearchFilePatterns));
            print("%s The contents of 'dictSearchResults' is [%s]..." % (self.sClassDisp, self.dictSearchResults));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'bSearchRecursiveFlag' is [%s], " % (self.bSearchRecursiveFlag));
        asObjDetail.append("'bSearchCaseSensitive' is [%s], " % (self.bSearchCaseSensitive));
        asObjDetail.append("'sSearchDirectories' is [%s], " % (self.sSearchDirectories));
        asObjDetail.append("'sSearchFilePatterns' is [%s], " % (self.sSearchFilePatterns));
        asObjDetail.append("'ssSearchDirectories' is [%s], " % (self.ssSearchDirectories));
        asObjDetail.append("'ssSearchFilePatterns' is [%s], " % (self.ssSearchFilePatterns));
        asObjDetail.append("'dictSearchResults' is [%s]." % (self.dictSearchResults));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def searchDirectoriesForFiles(self):

        if self.ssSearchDirectories == None or \
           len(self.ssSearchDirectories) < 1:

            print("%s The set of supplied Directories to be searched 'ssSearchDirectories' is None or Empty - Severe Error!" % (self.sClassDisp));

            return False;

        if self.ssSearchFilePatterns == None or \
           len(self.ssSearchFilePatterns) < 1:

            print("%s The set of supplied File(name) 'search' pattern(s) 'ssSearchFilePatterns' is None or Empty - Severe Error!" % (self.sClassDisp));

            return False;

        try:

            cSubDirs = 0;

            for sSearchDirectory in self.ssSearchDirectories:

                cSubDirs    += 1;
                sSearchPath  = os.path.realpath(sSearchDirectory);

                if self.bTraceFlag == True:

                    print("%s Element #(%d) - search Directory is [%s] - search 'real' Path is [%s]..." % (self.sClassDisp, cSubDirs, sSearchDirectory, sSearchPath));
                    print("");

                if self.bSearchRecursiveFlag == False:

                    asDirFiles = None;

                    for sDirFileName in os.listdir(sSearchPath):

                        sDirFilePath = os.path.join(sSearchPath, sDirFileName);

                        if not os.path.isfile(sDirFilePath):

                            continue;

                        if asDirFiles == None:

                            asDirFiles = list();

                        asDirFiles.append(sDirFileName);

                    if asDirFiles != None and \
                       len(asDirFiles) > 0:

                        self.filterFilesAgainstPatterns(rootpath=sSearchPath, dirfiles=asDirFiles);

                else:

                    for sRootPath, asSubDirs, asDirFiles in os.walk(sSearchPath):

                        if sRootPath == None or \
                           len(sRootPath) < 1:

                            continue;

                        sRootPath = sRootPath.strip();

                        if asDirFiles == None or \
                           len(asDirFiles) < 1:

                            continue;

                        self.filterFilesAgainstPatterns(rootpath=sRootPath, dirfiles=asDirFiles);

        except Exception as inst:

            print("%s 'searchDirectoriesForFiles()' - operational exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            return False;

        return True;

    def filterFilesAgainstPatterns(self, rootpath=None, dirfiles=None):

        sRootPath = rootpath;

        if sRootPath == None or \
           len(sRootPath) < 1:

            return;

        sRootPath  = sRootPath.strip();
        asDirFiles = dirfiles;

        if asDirFiles == None or \
           len(asDirFiles) < 1:

            return;

        if self.ssSearchFilePatterns == None or \
           len(self.ssSearchFilePatterns) < 1:

            return;

        for sDirFile in asDirFiles:

            sDirFile = sDirFile.strip();

            if sDirFile == None or \
               len(sDirFile) < 1:

                continue;

            for sSearchFilePattern in self.ssSearchFilePatterns:

                if sSearchFilePattern == None or \
                   len(sSearchFilePattern) < 1:

                    continue;

                bFileMatchesPattern = False;

                if self.bSearchCaseSensitive == False:

                    bFileMatchesPattern = fnmatch.fnmatch(sDirFile, sSearchFilePattern);

                else:

                    bFileMatchesPattern = fnmatch.fnmatchcase(sDirFile, sSearchFilePattern);

                if bFileMatchesPattern == False:

                    continue;

                if self.dictSearchResults == None:

                    self.dictSearchResults = collections.defaultdict(list);

                self.dictSearchResults[sRootPath].append(sDirFile);

        return;

class DrcDirectorySearcher:

    sClassMod            = __name__;
    sClassId             = "DrcDirectorySearcher";
    sClassVers           = "(v1.0101)";
    sClassDisp           = sClassMod+"."+sClassId+" "+sClassVers+":";

    bTraceFlag           = False;
    bSearchRecursiveFlag = False;
    bSearchCaseSensitive = False;

    sSearchDirectories   = None;
    sSearchNamePatterns  = None;

    ssSearchDirectories  = None;
    ssSearchNamePatterns = None;

    dictSearchResults    = None;

    def __init__(self, trace=False, searchrecursive=False, searchcasesensitive=False, searchdirectories=None, searchnamepatterns=None):

        try:

            self.setTraceFlag(trace=trace);
            self.setSearchRecursiveFlag(searchrecursive=searchrecursive);
            self.setSearchCaseSensitiveFlag(searchcasesensitive=searchcasesensitive);
            self.setSearchDirectories(searchdirectories=searchdirectories);
            self.setSearchNamePatterns(searchnamepatterns=searchnamepatterns);

        except Exception as inst:

            print("%s '__init__()' - exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

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

    def getSearchDirectories(self):

        return self.sSearchDirectories;

    def setSearchDirectories(self, searchdirectories=None):

        self.sSearchDirectories = searchdirectories;

        if self.sSearchDirectories == None or \
           len(self.sSearchDirectories) < 1:

            return;

        self.addSearchDirectories(searchdirectories=self.sSearchDirectories);

    def addSearchDirectories(self, searchdirectories=None):

        sSetSearchDirectories = searchdirectories;

        if sSetSearchDirectories == None or \
           len(sSetSearchDirectories) < 1:

            return;

        sSetSearchDirectories  = sSetSearchDirectories.strip();
        asSetSearchDirectories = sSetSearchDirectories.split(';');

        if asSetSearchDirectories == None or \
           len(asSetSearchDirectories) < 1:

            return;

        for sSetSearchDirectory in asSetSearchDirectories:

            sSetSearchDirectory = sSetSearchDirectory.strip();

            if sSetSearchDirectory == None or \
               len(sSetSearchDirectory) < 1:

                return;

            self.addSearchDirectory(searchdirectory=sSetSearchDirectory);

    def addSearchDirectory(self, searchdirectory=None):

        sSearchDirectory = searchdirectory;

        if sSearchDirectory == None or \
           len(sSearchDirectory) < 1:

            return;

        sSearchDirectory = sSearchDirectory.strip();

        if self.ssSearchDirectories == None:

            self.ssSearchDirectories = set();

        self.ssSearchDirectories.add(sSearchDirectory);

    def getSSSearchDirectories(self):

        return self.ssSearchDirectories;

    def getSearchNamePatterns(self):

        return self.sSearchNamePatterns;

    def setSearchNamePatterns(self, searchnamepatterns=None):

        self.sSearchNamePatterns = searchnamepatterns;

        if self.sSearchNamePatterns == None or \
           len(self.sSearchNamePatterns) < 1:

            return;

        self.addSearchNamePatterns(searchnamepatterns=self.sSearchNamePatterns);

    def addSearchNamePatterns(self, searchnamepatterns=None):

        sSetSearchNamePatterns = searchnamepatterns;

        if sSetSearchNamePatterns == None or \
           len(sSetSearchNamePatterns) < 1:

            return;

        sSetSearchNamePatterns  = sSetSearchNamePatterns.strip();
        asSetSearchNamePatterns = sSetSearchNamePatterns.split(';');

        if asSetSearchNamePatterns == None or \
           len(asSetSearchNamePatterns) < 1:

            return;

        for sSetSearchNamePattern in asSetSearchNamePatterns:

            sSetSearchNamePattern = sSetSearchNamePattern.strip();

            if sSetSearchNamePattern == None or \
               len(sSetSearchNamePattern) < 1:

                return;

            self.addSearchNamePattern(searchnamepattern=sSetSearchNamePattern);

    def addSearchNamePattern(self, searchnamepattern=None):

        sSearchNamePattern = searchnamepattern;

        if sSearchNamePattern == None or \
           len(sSearchNamePattern) < 1:

            return;

        sSearchNamePattern = sSearchNamePattern.strip();

        if self.ssSearchNamePatterns == None:

            self.ssSearchNamePatterns = set();

        self.ssSearchNamePatterns.add(sSearchNamePattern);

    def getSSSearchNamePatterns(self):

        return self.ssSearchNamePatterns;

    def getDictSearchResults(self):

        return self.dictSearchResults;

    def renderDictSearchResultsAsList(self):

        asSearchResultsList = list();

        if self.dictSearchResults == None or \
           len(self.dictSearchResults) < 1:

            return asSearchResultsList;

        if self.bTraceFlag == True:

            print("%s Processing the (%d) 'root' paths found..." % (self.sClassDisp, len(self.dictSearchResults)));

        for sRootPath in list(self.dictSearchResults.keys()):

            if sRootPath == None or \
               len(sRootPath) < 1:

                continue;

            if self.bTraceFlag == True:

                print("%s Processing the 'root' path of [%s]..." % (self.sClassDisp, sRootPath));

            asDirNames = self.dictSearchResults[sRootPath];

            if asDirNames == None or \
               len(asDirNames) < 1:

                continue;

            if self.bTraceFlag == True:

                print("%s Processing the (%d) Directory names in the 'root' path of [%s]..." % (self.sClassDisp, len(asDirNames), sRootPath));

            for sDirName in asDirNames:

                if sDirName == None or \
                   len(sDirName) < 1:

                    continue;

                sFullyQualifiedDirName = os.path.join(sRootPath, sDirName);

                if self.bTraceFlag == True:

                    print("%s Adding the fully-qualified Directory name [%s] to the list..." % (self.sClassDisp, sFullyQualifiedDirName));

                asSearchResultsList.append(sFullyQualifiedDirName);

        return asSearchResultsList;

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The 'bSearchRecursiveFlag' boolean is [%s]..." % (self.sClassDisp, self.bSearchRecursiveFlag));
            print("%s The 'bSearchCaseSensitive' boolean is [%s]..." % (self.sClassDisp, self.bSearchCaseSensitive));
            print("%s The contents of 'sSearchDirectories' is [%s]..." % (self.sClassDisp, self.sSearchDirectories));
            print("%s The contents of 'sSearchNamePatterns' is [%s]..." % (self.sClassDisp, self.sSearchNamePatterns));
            print("%s The contents of 'ssSearchDirectories' is [%s]..." % (self.sClassDisp, self.ssSearchDirectories));
            print("%s The contents of 'ssSearchNamePatterns' is [%s]..." % (self.sClassDisp, self.ssSearchNamePatterns));
            print("%s The contents of 'dictSearchResults' is [%s]..." % (self.sClassDisp, self.dictSearchResults));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'bSearchRecursiveFlag' is [%s], " % (self.bSearchRecursiveFlag));
        asObjDetail.append("'bSearchCaseSensitive' is [%s], " % (self.bSearchCaseSensitive));
        asObjDetail.append("'sSearchDirectories' is [%s], " % (self.sSearchDirectories));
        asObjDetail.append("'sSearchNamePatterns' is [%s], " % (self.sSearchNamePatterns));
        asObjDetail.append("'ssSearchDirectories' is [%s], " % (self.ssSearchDirectories));
        asObjDetail.append("'ssSearchNamePatterns' is [%s], " % (self.ssSearchNamePatterns));
        asObjDetail.append("'dictSearchResults' is [%s]." % (self.dictSearchResults));

        return str(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def searchDirectoriesForNames(self):

        if self.ssSearchDirectories == None or \
           len(self.ssSearchDirectories) < 1:

            print("%s The set of supplied Directories to be searched 'ssSearchDirectories' is None or Empty - Severe Error!" % (self.sClassDisp));

            return False;

        if self.ssSearchNamePatterns == None or \
           len(self.ssSearchNamePatterns) < 1:

            print("%s The set of supplied (Directory) Name 'search' pattern(s) 'ssSearchNamePatterns' is None or Empty - Severe Error!" % (self.sClassDisp));

            return False;

        try:

            cSubDirs = 0;

            for sSearchDirectory in self.ssSearchDirectories:

                cSubDirs    += 1;
                sSearchPath  = os.path.realpath(sSearchDirectory);

                if self.bTraceFlag == True:

                    print("%s Element #(%d) - search Directory is [%s] - search 'real' Path is [%s]..." % (self.sClassDisp, cSubDirs, sSearchDirectory, sSearchPath));
                    print("");

                if self.bSearchRecursiveFlag == False:

                    asDirNames = None;

                    for sDirName in os.listdir(sSearchPath):

                        sDirPath = os.path.join(sSearchPath, sDirName);

                        if not os.path.isdir(sDirPath):

                            continue;

                        if asDirNames == None:

                            asDirNames = list();

                        asDirNames.append(sDirName);

                    if asDirNames != None and \
                       len(asDirNames) > 0:

                        self.filterNamesAgainstPatterns(rootpath=sSearchPath, dirnames=asDirNames);

                else:

                    for sRootPath, asSubDirs, asDirFiles in os.walk(sSearchPath):

                        if sRootPath == None or \
                           len(sRootPath) < 1:

                            continue;

                        sRootPath = sRootPath.strip();

                        if asSubDirs == None or \
                           len(asSubDirs) < 1:

                            continue;

                        self.filterNamesAgainstPatterns(rootpath=sRootPath, dirnames=asSubDirs);

        except Exception as inst:

            print("%s 'searchDirectoriesForNames()' - operational exception occured..." % (self.sClassDisp));
            print(type(inst));
            print(inst);

            return False;

        return True;

    def filterNamesAgainstPatterns(self, rootpath=None, dirnames=None):

        sRootPath = rootpath;

        if sRootPath == None or \
           len(sRootPath) < 1:

            return;

        sRootPath  = sRootPath.strip();
        asDirNames = dirnames;

        if asDirNames == None or \
           len(asDirNames) < 1:

            return;

        if self.ssSearchNamePatterns == None or \
           len(self.ssSearchNamePatterns) < 1:

            return;

        for sDirName in asDirNames:

            sDirName = sDirName.strip();

            if sDirName == None or \
               len(sDirName) < 1:

                continue;

            for sSearchNamePattern in self.ssSearchNamePatterns:

                if sSearchNamePattern == None or \
                   len(sSearchNamePattern) < 1:

                    continue;

                bFileMatchesPattern = False;

                if self.bSearchCaseSensitive == False:

                    bFileMatchesPattern = fnmatch.fnmatch(sDirName, sSearchNamePattern);

                else:

                    bFileMatchesPattern = fnmatch.fnmatchcase(sDirName, sSearchNamePattern);

                if bFileMatchesPattern == False:

                    continue;

                if self.dictSearchResults == None:

                    self.dictSearchResults = collections.defaultdict(list);

                self.dictSearchResults[sRootPath].append(sDirName);

        return;

