
import os;
import traceback;
import re;
import string;
import sys;
import collections;

import CxProjectScan1;
import CxProjectDataCollectionDefaults1;

class CxProjectData(object):

    sClassMod                       = __name__;
    sClassId                        = "CxProjectData";
    sClassVers                      = "(v1.0577)";
    sClassDisp                      = sClassMod+"."+sClassId+" "+sClassVers+": ";

    bTraceFlag                      = False;

    # --------------------------------------------------------------------------------------------------
    # Item #(14): 
    #   Item #(14.1): 'name' <type 'unicode'> [TestCLI3]...
    #   Item #(14.2): 'links' <type 'list'> 
    #                     [[{u'uri': u'/projects/390094', u'rel': u'self'},
    #                       {u'uri': u'/auth/teams/', u'rel': u'teams'}, 
    #                       {u'uri': u'/sast/scans?projectId=390094&last=1', u'rel': u'latestscan'},
    #                       {u'uri': u'/sast/scans?projectId=390094', u'rel': u'allscans'}, 
    #                       {u'uri': u'/sast/scanSettings/390094', u'rel': u'scansettings'}, 
    #                       {u'type': u'local', u'uri': None, u'rel': u'source'}]]...
    #   Item #(14.3): 'isPublic' <type 'bool'> [True]...
    #   Item #(14.4): 'teamId' <type 'unicode'> [22222222-2222-448d-b029-989c9070eb23]...
    #   Item #(14.5): 'customFields' <type 'list'> [[]]...
    #   Item #(14.6): 'id' <type 'int'> [390094]...
    # --------------------------------------------------------------------------------------------------

    sCxProjectName                  = None;
    sCxProjectId                    = "-undefined-";
    iCxProjectId                    = 0;
    bCxProjectIsPublic              = False;
    sCxProjectTeamId                = None;
    asCxProjectLinks                = [];
    asCxProjectCustomFields         = [];

    dictCxProjectScans              = None;

    cxProjectDataCollectionDefaults = None;     # New...

    # Fields that are determined by 'lookup' or Rest API response:

    sCxProjectTeam                  = None;

    # Generated Project 'stats':

    asCxProjectScanLanguagesGap     = None;     # New...
    asCxProjectScanLanguagesStd     = None;     # New...

    sCxProjectRiskSeverity          = None;
    sCxProjectRiskTrend             = None;

    sCxScanIdBaseline               = None;
    sCxScanIdLatest                 = None;

    cxProjectScanBaseline           = None;
    cxProjectScanLatest             = None;

    dictScanResultsBaseline         = None;
    dictScanResultsLatest           = None;
    dictScanResultsDelta            = None;

    def __init__(self, trace=False, cxprojectname=None, cxprojectid=0):

        try:

            self.setTraceFlag(trace=trace);
            self.setCxProjectName(cxprojectname=cxprojectname);
            self.setCxProjectId(cxprojectid=cxprojectid);

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

    def getCxProjectName(self):

        return self.sCxProjectName;

    def setCxProjectName(self, cxprojectname=None):

        self.sCxProjectName = cxprojectname;

        if self.sCxProjectName == None or \
           len(self.sCxProjectName) < 1:
         
            self.sCxProjectName = None;
         
    def getCxProjectId(self):

        return self.sCxProjectId;

    def setCxProjectId(self, cxprojectid=None):

    #   print("%s TYPE 'cxprojectid' is [%s]..." % (self.sClassDisp, type(cxprojectid)));

        if cxprojectid == None:

            return;

        if type(cxprojectid) == str:

            self.sCxProjectId = cxprojectid;

            if self.sCxProjectId != None:

                self.sCxProjectId = self.sCxProjectId.strip();

            if self.sCxProjectId == None or \
               len(self.sCxProjectId) < 1:

                self.sCxProjectId = "";
                self.iCxProjectId = -1;

            else:

                self.iCxProjectId = int(self.sCxProjectId);

        else:

            self.iCxProjectId = cxprojectid;

            if self.iCxProjectId < 0:

                self.sCxProjectId = "";
                self.iCxProjectId = -1;

            else:

                self.sCxProjectId = ("%d" % self.iCxProjectId);

    def getCxProjectIsPublic(self):

        return self.bCxProjectIsPublic;

    def setCxProjectIsPublic(self, cxprojectispublic=False):

        self.bCxProjectIsPublic = cxprojectispublic;

    def getCxProjectTeamId(self):

        return self.sCxProjectTeamId;

    def setCxProjectTeamId(self, cxprojectteamid=None):

        if cxprojectteamid == None:

            return;

        if type(cxprojectteamid) == str:

            self.sCxProjectTeamId = cxprojectteamid;

            if self.sCxProjectTeamId != None:

                self.sCxProjectTeamId = self.sCxProjectTeamId.strip();

            if self.sCxProjectTeamId == None or \
               len(self.sCxProjectTeamId) < 1:

                self.sCxProjectTeamId = "0";

        else:

            self.iCxProjectTeamId = cxprojectteamid;

            if self.iCxProjectTeamId < 0:

                self.sCxProjectTeamId = "0";

            else:

                self.sCxProjectTeamId = ("%d" % self.iCxProjectTeamId);
         
    def getCxProjectLinks(self):

        return self.asCxProjectLinks;

    def setCxProjectLinks(self, cxprojectlinks=None):

        self.asCxProjectLinks = cxprojectlinks;

    def getCxProjectCustomFields(self):

        return self.asCxProjectCustomFields;

    def setCxProjectCustomFields(self, cxprojectcustomfields=None):

        self.asCxProjectCustomFields = cxprojectcustomfields;

    def getCxProjectScans(self):

        return self.dictCxProjectScans;

    def getCxProjectTeam(self):

        return self.sCxProjectTeam;

    def setCxProjectTeam(self, cxprojectteam=None):

        self.sCxProjectTeam = cxprojectteam;

        if self.sCxProjectTeam != None:

            self.sCxProjectTeam = self.sCxProjectTeam.strip();

        if self.sCxProjectTeam == None or \
           len(self.sCxProjectTeam) < 1:

            self.sCxProjectTeam = None;

    def addCxProjectScanLanguageToGapList(self, cxprojectscanlanguage=None):

        if cxprojectscanlanguage == None:

            return;

        sCxProjectScanLanguage = cxprojectscanlanguage;

        if sCxProjectScanLanguage != None:

            sCxProjectScanLanguage = sCxProjectScanLanguage.strip();

        if sCxProjectScanLanguage == None or \
            len(sCxProjectScanLanguage) < 1:

            return;

        sCxProjectScanLanguageLow = sCxProjectScanLanguage.lower();

        if self.asCxProjectScanLanguagesGap == None:

            self.asCxProjectScanLanguagesGap = list();

        if sCxProjectScanLanguageLow not in self.asCxProjectScanLanguagesGap:

            self.asCxProjectScanLanguagesGap.append(sCxProjectScanLanguageLow);

    def addCxProjectScanLanguageToStdList(self, cxprojectscanlanguage=None):

        if cxprojectscanlanguage == None:

            return;

        sCxProjectScanLanguage = cxprojectscanlanguage;

        if sCxProjectScanLanguage != None:

            sCxProjectScanLanguage = sCxProjectScanLanguage.strip();

        if sCxProjectScanLanguage == None or \
            len(sCxProjectScanLanguage) < 1:

            return;

        sCxProjectScanLanguageLow = sCxProjectScanLanguage.lower();

        if self.asCxProjectScanLanguagesStd == None:

            self.asCxProjectScanLanguagesStd = list();

        if sCxProjectScanLanguageLow not in self.asCxProjectScanLanguagesStd:

            self.asCxProjectScanLanguagesStd.append(sCxProjectScanLanguageLow);

    def dump_fields(self):

        if self.bTraceFlag == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp));
            print("%s The 'bTraceFlag' boolean is [%s]..." % (self.sClassDisp, self.bTraceFlag));
            print("%s The contents of 'sCxProjectName' is [%s]..." % (self.sClassDisp, self.sCxProjectName));
            print("%s The contents of 'sCxProjectId' is [%s]..." % (self.sClassDisp, self.sCxProjectId));
            print("%s The contents of 'iCxProjectId' is (%d)..." % (self.sClassDisp, self.iCxProjectId));
            print("%s The contents of 'bCxProjectIsPublic' is [%s]..." % (self.sClassDisp, self.bCxProjectIsPublic));
            print("%s The contents of 'sCxProjectTeamId' is [%s]..." % (self.sClassDisp, self.sCxProjectTeamId));
            print("%s The contents of 'asCxProjectLinks' is [%s]..." % (self.sClassDisp, self.asCxProjectLinks));
            print("%s The contents of 'asCxProjectCustomFields' is [%s]..." % (self.sClassDisp, self.asCxProjectCustomFields));
            print("%s The contents of 'dictCxProjectScans' is [%s]..." % (self.sClassDisp, self.dictCxProjectScans));
            print("%s The contents of 'cxProjectDataCollectionDefaults' is [%s]..." % (self.sClassDisp, self.cxProjectDataCollectionDefaults));
            print("%s The contents of 'sCxProjectTeam' is [%s]..." % (self.sClassDisp, self.sCxProjectTeam));
            print("%s The contents of 'asCxProjectScanLanguagesGap' is [%s]..." % (self.sClassDisp, self.asCxProjectScanLanguagesGap));
            print("%s The contents of 'asCxProjectScanLanguagesStd' is [%s]..." % (self.sClassDisp, self.asCxProjectScanLanguagesStd));
            print("%s The contents of 'sCxProjectRiskSeverity' is [%s]..." % (self.sClassDisp, self.sCxProjectRiskSeverity));
            print("%s The contents of 'sCxProjectRiskTrend' is [%s]..." % (self.sClassDisp, self.sCxProjectRiskTrend));
            print("%s The contents of 'sCxScanIdBaseline' is [%s]..." % (self.sClassDisp, self.sCxScanIdBaseline));
            print("%s The contents of 'sCxScanIdLatest' is [%s]..." % (self.sClassDisp, self.sCxScanIdLatest));
            print("%s The contents of 'cxProjectScanBaseline' is [%s]..." % (self.sClassDisp, self.cxProjectScanBaseline));
            print("%s The contents of 'cxProjectScanLatest' is [%s]..." % (self.sClassDisp, self.cxProjectScanLatest));
            print("%s The contents of 'dictScanResultsBaseline' is [%s]..." % (self.sClassDisp, self.dictScanResultsBaseline));
            print("%s The contents of 'dictScanResultsLatest' is [%s]..." % (self.sClassDisp, self.dictScanResultsLatest));
            print("%s The contents of 'dictScanResultsDelta' is [%s]..." % (self.sClassDisp, self.dictScanResultsDelta));

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp));
        asObjDetail.append("'bTraceFlag' is [%s], " % (self.bTraceFlag));
        asObjDetail.append("'sCxProjectName' is [%s], " % (self.sCxProjectName));
        asObjDetail.append("'sCxProjectId' is [%s], " % (self.sCxProjectId));
        asObjDetail.append("'iCxProjectId' is (%d), " % (self.iCxProjectId));
        asObjDetail.append("'bCxProjectIsPublic' is [%s], " % (self.bCxProjectIsPublic));
        asObjDetail.append("'sCxProjectTeamId' is [%s], " % (self.sCxProjectTeamId));
        asObjDetail.append("'asCxProjectLinks' is [%s], " % (self.asCxProjectLinks));
        asObjDetail.append("'asCxProjectCustomFields' is [%s], " % (self.asCxProjectCustomFields));
        asObjDetail.append("'dictCxProjectScans' is [%s], " % (self.dictCxProjectScans));
        asObjDetail.append("'cxProjectDataCollectionDefaults' is [%s], " % (self.cxProjectDataCollectionDefaults));
        asObjDetail.append("'sCxProjectTeam' is [%s], " % (self.sCxProjectTeam));
        asObjDetail.append("'asCxProjectScanLanguagesGap' is [%s], " % (self.asCxProjectScanLanguagesGap));
        asObjDetail.append("'asCxProjectScanLanguagesStd' is [%s], " % (self.asCxProjectScanLanguagesStd));
        asObjDetail.append("'sCxProjectRiskSeverity' is [%s], " % (self.sCxProjectRiskSeverity));
        asObjDetail.append("'sCxProjectRiskTrend' is [%s], " % (self.sCxProjectRiskTrend));
        asObjDetail.append("'sCxScanIdBaseline' is [%s], " % (self.sCxScanIdBaseline));
        asObjDetail.append("'sCxScanIdLatest' is [%s], " % (self.sCxScanIdLatest));
        asObjDetail.append("'cxProjectScanBaseline' is [%s], " % (self.cxProjectScanBaseline));
        asObjDetail.append("'cxProjectScanLatest' is [%s], " % (self.cxProjectScanLatest));
        asObjDetail.append("'dictScanResultsBaseline' is [%s], " % (self.dictScanResultsBaseline));
        asObjDetail.append("'dictScanResultsLatest' is [%s], " % (self.dictScanResultsLatest));
        asObjDetail.append("'dictScanResultsDelta' is [%s]. " % (self.dictScanResultsDelta));

        return ''.join(asObjDetail);

    def toPrettyString(self):

        return self.toPrettyStringWithWidths();

    def toPrettyStringWithWidths(self, dictcxprojectdatacollectionstats=None):

    #   dictCxProjectDataCollectionStats = None;
    #
    #   if dictcxprojectdatacollectionstats != None:
    #
    #       if self.bTraceFlag == True:
    #
    #           print("%s 'dictcxprojectdatacollectionstats' Type is [%s]..." % (self.sClassDisp, type(dictcxprojectdatacollectionstats)));
    #
    #       if type(dictcxprojectdatacollectionstats) == dict or \
    #           type(dictcxprojectdatacollectionstats) == collections.defaultdict:
    #
    #           dictCxProjectDataCollectionStats = dictcxprojectdatacollectionstats;
    #
    #       else:
    #
    #           dictCxProjectDataCollectionStats = collections.defaultdict(int);
    #
    #   else:
    #
    #       dictCxProjectDataCollectionStats = collections.defaultdict(int);
    #
    #   # Dictionary collection of 'width' counters...
    #   # Keys: "cWidthCxProjectName",
    #   #       "cWidthCxProjectId",
    #   #       "cWidthCxProjectTeamName",
    #   #       "cWidthCxProjectTeamId",
    #   #       "cWidthCxProjectPresetName",
    #   #       "cWidthCxProjectPresetId",
    #   #       "cWidthCxProjectEngineConfigName",
    #   #       "cWidthCxProjectEngineConfigId".
    #   # Note: ALL Key(s) are initialized to 0 (Zero).
    #
    #   dictCxProjectDataCollectionStats.setdefault("cWidthCxProjectName",             70);
    #   dictCxProjectDataCollectionStats.setdefault("cWidthCxProjectId",               8);
    #   dictCxProjectDataCollectionStats.setdefault("cWidthCxProjectTeamName",         48);
    #   dictCxProjectDataCollectionStats.setdefault("cWidthCxProjectTeamId",           36);
    #   dictCxProjectDataCollectionStats.setdefault("cWidthCxProjectPresetName",       48);
    #   dictCxProjectDataCollectionStats.setdefault("cWidthCxProjectPresetId",         36);
    #   dictCxProjectDataCollectionStats.setdefault("cWidthCxProjectEngineConfigName", 24);
    #   dictCxProjectDataCollectionStats.setdefault("cWidthCxProjectEngineConfigId",   2);
    #
    #   cWidthCxProjectName             = dictCxProjectDataCollectionStats["cWidthCxProjectName"];    
    #   cWidthCxProjectId               = dictCxProjectDataCollectionStats["cWidthCxProjectId"];    
    #   cWidthCxProjectTeamName         = dictCxProjectDataCollectionStats["cWidthCxProjectTeamName"];    
    #   cWidthCxProjectTeamId           = dictCxProjectDataCollectionStats["cWidthCxProjectTeamId"];    
    #   cWidthCxProjectPresetName       = dictCxProjectDataCollectionStats["cWidthCxProjectPresetName"];    
    #   cWidthCxProjectPresetId         = dictCxProjectDataCollectionStats["cWidthCxProjectPresetId"];    
    #   cWidthCxProjectEngineConfigName = dictCxProjectDataCollectionStats["cWidthCxProjectEngineConfigName"];    
    #   cWidthCxProjectEngineConfigId   = dictCxProjectDataCollectionStats["cWidthCxProjectEngineConfigId"];    
    #
    #   if self.bTraceFlag == True:
    #
    #       print(" = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ");
    #       print("%s 'dictcxprojectdatacollectionstats' is [%s]..." % (self.sClassDisp, dictcxprojectdatacollectionstats));
    #       print("%s 'dictCxProjectDataCollectionStats' is [%s]..." % (self.sClassDisp, dictCxProjectDataCollectionStats));
    #       print("%s 'cWidthCxProjectName' is [%d]..." % (self.sClassDisp, cWidthCxProjectName));
    #       print("%s 'cWidthCxProjectId' is [%d]..." % (self.sClassDisp, cWidthCxProjectId));
    #       print("%s 'cWidthCxProjectTeamName' is [%d]..." % (self.sClassDisp, cWidthCxProjectTeamName));
    #       print("%s 'cWidthCxProjectTeamId' is [%d]..." % (self.sClassDisp, cWidthCxProjectTeamId));
    #       print("%s 'cWidthCxProjectPresetName' is [%d]..." % (self.sClassDisp, cWidthCxProjectPresetName));
    #       print("%s 'cWidthCxProjectPresetId' is [%d]..." % (self.sClassDisp, cWidthCxProjectPresetId));
    #       print("%s 'cWidthCxProjectEngineConfigName' is [%d]..." % (self.sClassDisp, cWidthCxProjectEngineConfigName));
    #       print("%s 'cWidthCxProjectEngineConfigId' is [%d]..." % (self.sClassDisp, cWidthCxProjectEngineConfigId));
    #       print(" = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ");
    #       print("");

        asObjDetail = list();

        asObjDetail.append("Project ");
        asObjDetail.append("'Name' [%s], "               % (self.sCxProjectName));
        asObjDetail.append("'Id' [%-s], "                % (self.sCxProjectId));
        asObjDetail.append("'Is Public?' [%5s], "        % (self.bCxProjectIsPublic));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Team Name' [%s], "          % (self.sCxProjectTeam));
        asObjDetail.append("'Team Id' [%s], "            % (self.sCxProjectTeamId));
        asObjDetail.append("\n");
        asObjDetail.append("........");

        if self.dictCxProjectScans == None or \
            len(self.dictCxProjectScans) < 1:

            asObjDetail.append("(   0) Scan(s): ");

        else:

            asObjDetail.append("(%4d) Scan(s): "         % (len(self.dictCxProjectScans)));

        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Scan Id (baseline)' [%s], " % (self.sCxScanIdBaseline));
        asObjDetail.append("'Scan Results (baseline)' [%s], " % (self.dictScanResultsBaseline));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("'Scan Id (latest)' [%s], "   % (self.sCxScanIdLatest));
        asObjDetail.append("'Scan Results (latest)' [%s], " % (self.dictScanResultsLatest));
        asObjDetail.append("\n");
        asObjDetail.append("........");
        asObjDetail.append("....'Scan Results (delta)' [%s]. " % (self.dictScanResultsDelta));
        asObjDetail.append("\n");

    #   for sCxProjectBranchedName in self.dictCxProjectBranchedNames.keys():
    #
    #       if sCxProjectBranchedName == None:
    #
    #           continue;
    #
    #       sCxProjectBranchedId = self.dictCxProjectBranchedNames[sCxProjectBranchedName];
    #
    #       asObjDetail.append("............");
    #       asObjDetail.append("Branched Project ");
    #       asObjDetail.append("'Name' [%*s], " % (cWidthCxProjectName, sCxProjectBranchedName));
    #       asObjDetail.append("'Id' [%*s]. "   % (cWidthCxProjectId, sCxProjectBranchedId));
    #       asObjDetail.append("\n");

        return ''.join(asObjDetail);

    def toPrettyStringForHtml(self, projecttag=None):

        sProjectTag = projecttag;

        if sProjectTag != None:

            sProjectTag = sProjectTag.strip();

        if sProjectTag == None or \
            len(sProjectTag) < 1:

            sProjectTag = "-N/A-"

        sStyleWidth1 = "style=\"width:6%\"";
        sStyleWidth2 = "style=\"width:27%\"";
        sStyleWidth3 = "style=\"width:25%\"";

        asObjDetail = list();

        if self.sCxProjectRiskSeverity != None:

            self.sCxProjectRiskSeverity = self.sCxProjectRiskSeverity.strip();

        if self.sCxProjectRiskSeverity == None or \
            len(self.sCxProjectRiskSeverity) < 1:

            self.sCxProjectRiskSeverity = "0";

        iValueProjRiskSev = int(self.sCxProjectRiskSeverity);
        sColorProjRiskSev = "red";

        if iValueProjRiskSev < 41:

            sColorProjRiskSev = "lime";

        else:

            if iValueProjRiskSev > 40 and \
                iValueProjRiskSev < 61:

                sColorProjRiskSev = "yellow";

        if self.sCxProjectRiskTrend != None:

            self.sCxProjectRiskTrend = self.sCxProjectRiskTrend.strip();

        if self.sCxProjectRiskTrend == None:

            self.sCxProjectRiskTrend = "0";

        iValueProjRiskTrend = int(self.sCxProjectRiskTrend);
        sColorProjRiskTrend = "red";

        if iValueProjRiskTrend < 0:

            sColorProjRiskTrend = "lime";

        else:

            if iValueProjRiskTrend == 0:

                sColorProjRiskTrend = sColorProjRiskSev;
            #   sColorProjRiskTrend = "yellow";

        cCxProjectScanLanguages  = 0;
        sColorProjScanLanguages  = "lightgrey";
        bProjScanHasGapLanguage  = False;
        sProjScanLanguageDisplay = False;
        sProjScanLanguagesGap    = "None";
        sProjScanLanguagesStd    = "None";

        if self.asCxProjectScanLanguagesGap != None and \
            len(self.asCxProjectScanLanguagesGap) > 0:

            cCxProjectScanLanguages += len(self.asCxProjectScanLanguagesGap);
            sColorProjScanLanguages  = "lime";
            bProjScanHasGapLanguage  = True;
            sProjScanLanguagesGap    = ', '.join(self.asCxProjectScanLanguagesGap);

        if self.asCxProjectScanLanguagesStd != None and \
            len(self.asCxProjectScanLanguagesStd) > 0:

            cCxProjectScanLanguages += len(self.asCxProjectScanLanguagesStd);
            sProjScanLanguagesStd    = ', '.join(self.asCxProjectScanLanguagesStd);

        if bProjScanHasGapLanguage == True:

            sProjScanLanguageDisplay = "<a class=\"trigger_popup_lang%s\"><b><u>%2d</u></b></a>" % (self.sCxProjectId, cCxProjectScanLanguages);

        else:

            sProjScanLanguageDisplay = "<a class=\"trigger_popup_lang%s\">%2d</a>" % (self.sCxProjectId, cCxProjectScanLanguages);

        asObjDetail.append("<div id=\"links\">");
        asObjDetail.append("\n");

        asObjDetail.append("<tr colspan=\"10\" align=\"center\" bgcolor=\"lightgrey\">");
        asObjDetail.append("<td %s>%s</td>" % (sStyleWidth1, sProjectTag));
        asObjDetail.append("<td %s>%s</td>" % (sStyleWidth2, self.sCxProjectName));
        asObjDetail.append("<td %s>%s</td>" % (sStyleWidth1, self.sCxProjectId));
        asObjDetail.append("<td %s>%s</td>" % (sStyleWidth1, self.bCxProjectIsPublic));
        asObjDetail.append("<td %s bgcolor=\"%s\">%s</td>" % (sStyleWidth1, sColorProjScanLanguages, sProjScanLanguageDisplay));
        asObjDetail.append("<td %s bgcolor=\"%s\">%s</td>" % (sStyleWidth1, sColorProjRiskSev, self.sCxProjectRiskSeverity));
        asObjDetail.append("<td %s bgcolor=\"%s\">%s</td>" % (sStyleWidth1, sColorProjRiskTrend, self.sCxProjectRiskTrend));

        if self.sCxProjectTeam != None:

            self.sCxProjectTeam = self.sCxProjectTeam.strip();

        if self.sCxProjectTeam != None and \
            len(self.sCxProjectTeam) > 0:

            asObjDetail.append("<td %s>%s</td>" % (sStyleWidth3, self.sCxProjectTeam));

        else:

            asObjDetail.append("<td %s>%s</td>" % (sStyleWidth3, self.sCxProjectTeamId));

        if self.dictCxProjectScans == None or \
            len(self.dictCxProjectScans) < 1:

            asObjDetail.append("<td %s>0</td>" % (sStyleWidth1));
            asObjDetail.append("<td %s></td>" % (sStyleWidth1));

        else:

            asObjDetail.append("<td %s>%d</td>" % (sStyleWidth1, len(self.dictCxProjectScans)));
            asObjDetail.append("<td %s><a href=\"#tr%s\" onClick=\"drcToggleSection('cxDiv%s')\">Details</a></td>" % (sStyleWidth1, self.sCxProjectId, self.sCxProjectId));

        asObjDetail.append("</tr>");
        asObjDetail.append("\n");

        asObjDetail.append("</div>");
        asObjDetail.append("\n");

        # --------------------------------------------------------------------------------------------------
        # Item #(1):
        #   Item #(1.1):  'status' <type 'dict'> [{u'details': 
        #                                          {u'step': u'', 
        #                                           u'stage': u''}, 
        #                                          u'name': u'Finished',
        #                                          u'id': 7}]...
        #   Item #(1.2):  'comment' <type 'unicode'> [Scan from CheckmarxXcodePlugin1]...
        #   Item #(1.3):  'resultsStatistics' <type 'dict'> [{u'link': None}]...
        #   Item #(1.4):  'scanType' <type 'dict'> [{u'id': 1, 
        #                                            u'value': u'Regular'}]...
        #   Item #(1.5):  'owningTeamId' <type 'unicode'> [00000000-1111-1111-b111-989c9070eb11]...
        #   Item #(1.6):  'dateAndTime' <type 'dict'> [{u'startedOn': u'2019-04-06T16:57:12.393', 
        #                                               u'finishedOn': u'2019-04-06T16:59:44.563', 
        #                                               u'engineStartedOn': u'2019-04-06T16:57:12.393', 
        #                                               u'engineFinishedOn': u'2019-04-06T16:59:44.54'}]...
        #   Item #(1.7):  'partialScanReasons' <type 'NoneType'> [None]...
        #   Item #(1.8):  'id' <type 'int'> [1450378]...
        #   Item #(1.9):  'scanState' <type 'dict'> [{u'languageStateCollection': 
        #                                            [{u'stateCreationDate': u'2018-08-29T20:05:16.59',
        #                                              u'languageID': 1073741824, 
        #                                              u'languageHash': u'0206692917308612', 
        #                                              u'languageName': u'Common'}, 
        #                                             {u'stateCreationDate': u'2018-08-29T20:05:16.59',
        #                                              u'languageID': 8, 
        #                                              u'languageHash': u'3602822811217894', 
        #                                              u'languageName': u'JavaScript'}, 
        #                                             {u'stateCreationDate': u'2018-08-29T20:05:16.59', 
        #                                              u'languageID': 4096,
        #                                              u'languageHash': u'0118406991696123', 
        #                                              u'languageName': u'Objc'}, 
        #                                             {u'stateCreationDate': u'2018-08-29T20:05:16.59', 
        #                                              u'languageID': 262144, 
        #                                              u'languageHash': u'1939975091058023', 
        #                                              u'languageName': u'Typescript'}, 
        #                                             {u'stateCreationDate': u'2017-11-15T13:45:50.393', 
        #                                              u'languageID': 64,
        #                                              u'languageHash': u'1349101913133594',
        #                                              u'languageName': u'VbScript'}],
        #                                             u'failedLinesOfCode': 0, 
        #                                             u'cxVersion': u'8.8.0.72 HF4',
        #                                             u'sourceId': u'0000000037_000836296494_00-689512115',
        #                                             u'filesCount': 37, 
        #                                             u'path': u' N/A (Zip File)',
        #                                             u'linesOfCode': 13341}]...
        #   Item #(1.10): 'isLocked' <type 'bool'> [False]...
        #   Item #(1.11): 'isIncremental' <type 'bool'> [True]...
        #   Item #(1.12): 'project' <type 'dict'> [{u'link': None,
        #                                           u'id': 390093, 
        #                                           u'name': u'CheckmarxXcodePlugin1'}]...
        #   Item #(1.13): 'origin' <type 'unicode'> [CheckmarxXcodePlugin1]...
        #   Item #(1.14): 'scanRisk' <type 'int'> [35]...
        #   Item #(1.15): 'initiatorName' <type 'unicode'> [admin admin]...
        #   Item #(1.16): 'scanRiskSeverity' <type 'int'> [19]...
        #   Item #(1.17): 'engineServer' <type 'dict'> [{u'link': None, 
        #                                                u'id': 1, 
        #                                                u'name': u'Localhost'}]...
        #   Item #(1.18): 'owner' <type 'unicode'> [dcox]...
        #   Item #(1.19): 'finishedScanStatus' <type 'dict'> [{u'id': 0, 
        #                                                      u'value': u'None'}]...
        #   Item #(1.20): 'isPublic' <type 'bool'> [True]...
        # --------------------------------------------------------------------------------------------------

        if self.dictCxProjectScans != None and \
            len(self.dictCxProjectScans) > 0 and \
            self.sCxScanIdBaseline != None:

            asObjDetail.append("<div id=\"cxDiv%s\">" % (self.sCxProjectId));
            asObjDetail.append("\n");

            asObjDetail.append("<tr colspan=\"10\" id=\"tr%s\" class=\"toggle\"><td colspan=\"10\">" % (self.sCxProjectId));
            asObjDetail.append("\n");

            asObjDetail.append("<table bgcolor=\"cyan\" border=\"0\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">");
            asObjDetail.append("\n");

            asObjDetail.append("<tr align=\"center\" bgcolor=\"cyan\">");
            asObjDetail.append("<td colspan=\"10\">Scan</td>");
            asObjDetail.append("<td colspan=\"4\">Results</td>");
            asObjDetail.append("</tr>");
            asObjDetail.append("\n");

            asObjDetail.append("<tr align=\"center\" bgcolor=\"cyan\">");
            asObjDetail.append("<td>Position</td>");
            asObjDetail.append("<td>Id</td>");
            asObjDetail.append("<td>Inc?</td>");
            asObjDetail.append("<td>Languages</td>");
            asObjDetail.append("<td>Files</td>");
            asObjDetail.append("<td>Loc</td>");
            asObjDetail.append("<td>Failed Loc</td>");
            asObjDetail.append("<td>Origin</td>");
            asObjDetail.append("<td>Risk</td>");
            asObjDetail.append("<td>RiskSev</td>");
            asObjDetail.append("<td>'High'</td>");
            asObjDetail.append("<td>'Medium'</td>");
            asObjDetail.append("<td>'Low'</td>");
            asObjDetail.append("<td>'Info'</td>");
            asObjDetail.append("</tr>");
            asObjDetail.append("\n");

            if self.sCxScanIdLatest != None:

                if (len(self.dictCxProjectScans)) == 1 or \
                    self.cxProjectScanLatest == None or \
                    self.dictScanResultsLatest == None:

                    asObjDetail.append("<tr align=\"center\" bgcolor=\"silver\">");
                    asObjDetail.append("<td><i>%s</i></td>" % ("latest"));
                    asObjDetail.append("<td>%s</td>" % (self.sCxScanIdLatest));
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("<td></td>");
                    asObjDetail.append("</tr>");
                    asObjDetail.append("\n");

                else:

                    asObjDetail.append("<tr align=\"center\" bgcolor=\"silver\">");
                    asObjDetail.append("<td><i>%s</i></td>" % ("latest"));
                    asObjDetail.append("<td>%s</td>" % (self.sCxScanIdLatest));
                    asObjDetail.append("<td>%s</td>" % (self.cxProjectScanLatest.bCxScanIsIncremental));
                    asObjDetail.append("<td>%s</td>" % (len(self.cxProjectScanLatest.dictCxScanState["languageStateCollection"])));
                    asObjDetail.append("<td>%s</td>" % (self.cxProjectScanLatest.dictCxScanState["filesCount"]));
                    asObjDetail.append("<td>%s</td>" % (self.cxProjectScanLatest.dictCxScanState["linesOfCode"]));
                    asObjDetail.append("<td>%s</td>" % (self.cxProjectScanLatest.dictCxScanState["failedLinesOfCode"]));
                    asObjDetail.append("<td>%s</td>" % (self.cxProjectScanLatest.sCxScanOrigin));
                    asObjDetail.append("<td>%s</td>" % (self.cxProjectScanLatest.sCxScanRisk));
                    asObjDetail.append("<td>%s</td>" % (self.cxProjectScanLatest.sCxScanRiskSeverity));
                    asObjDetail.append("<td>%d</td>" % (self.dictScanResultsLatest["highSeverity"]));
                    asObjDetail.append("<td>%d</td>" % (self.dictScanResultsLatest["mediumSeverity"]));
                    asObjDetail.append("<td>%d</td>" % (self.dictScanResultsLatest["lowSeverity"]));
                    asObjDetail.append("<td>%d</td>" % (self.dictScanResultsLatest["infoSeverity"]));
                    asObjDetail.append("</tr>");
                    asObjDetail.append("\n");

            else: 

                asObjDetail.append("<tr align=\"center\" bgcolor=\"silver\">");
                asObjDetail.append("<td><i>%s</i></td>" % ("latest"));
                asObjDetail.append("<td>%s</td>" % (self.sCxScanIdLatest));
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("</tr>");
                asObjDetail.append("\n");

            if self.cxProjectScanBaseline == None or \
                self.dictScanResultsBaseline == None:

                asObjDetail.append("<tr align=\"center\" bgcolor=\"gainsboro\">");
                asObjDetail.append("<td><i>%s</i></td>" % ("baseline"));
                asObjDetail.append("<td>%s</td>" % (self.sCxScanIdBaseline));
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("<td></td>");
                asObjDetail.append("</tr>");
                asObjDetail.append("\n");

            else:

                asObjDetail.append("<tr align=\"center\" bgcolor=\"gainsboro\">");
                asObjDetail.append("<td><i>%s</i></td>" % ("baseline"));
                asObjDetail.append("<td>%s</td>" % (self.sCxScanIdBaseline));
                asObjDetail.append("<td>%s</td>" % (self.cxProjectScanBaseline.bCxScanIsIncremental));          
                asObjDetail.append("<td>%s</td>" % (len(self.cxProjectScanBaseline.dictCxScanState["languageStateCollection"])));
                asObjDetail.append("<td>%s</td>" % (self.cxProjectScanBaseline.dictCxScanState["filesCount"])); 
                asObjDetail.append("<td>%s</td>" % (self.cxProjectScanBaseline.dictCxScanState["linesOfCode"]));
                asObjDetail.append("<td>%s</td>" % (self.cxProjectScanBaseline.dictCxScanState["failedLinesOfCode"]));
                asObjDetail.append("<td>%s</td>" % (self.cxProjectScanBaseline.sCxScanOrigin));                 
                asObjDetail.append("<td>%s</td>" % (self.cxProjectScanBaseline.sCxScanRisk));                   
                asObjDetail.append("<td>%s</td>" % (self.cxProjectScanBaseline.sCxScanRiskSeverity));           
                asObjDetail.append("<td>%d</td>" % (self.dictScanResultsBaseline["highSeverity"]));
                asObjDetail.append("<td>%d</td>" % (self.dictScanResultsBaseline["mediumSeverity"]));
                asObjDetail.append("<td>%d</td>" % (self.dictScanResultsBaseline["lowSeverity"]));
                asObjDetail.append("<td>%d</td>" % (self.dictScanResultsBaseline["infoSeverity"]));
                asObjDetail.append("</tr>");
                asObjDetail.append("\n");

            if self.dictScanResultsDelta != None and \
                len(self.dictScanResultsDelta) > 0:

                iValueDeltaHigh = self.dictScanResultsDelta["highSeverity"];
                sColorDeltaHigh = "red";

                if iValueDeltaHigh < 0:

                    sColorDeltaHigh = "lime";

                else:

                    if iValueDeltaHigh == 0:

                        sColorDeltaHigh = "yellow";

                iValueDeltaMedium = self.dictScanResultsDelta["mediumSeverity"];
                sColorDeltaMedium = "red";

                if iValueDeltaMedium < 0:

                    sColorDeltaMedium = "lime";

                else:

                    if iValueDeltaMedium == 0:

                        sColorDeltaMedium = "yellow";

                iValueDeltaLow = self.dictScanResultsDelta["lowSeverity"];
                sColorDeltaLow = "red";

                if iValueDeltaLow < 0:

                    sColorDeltaLow = "lime";

                else:

                    if iValueDeltaLow == 0:

                        sColorDeltaLow = "yellow";

                iValueDeltaInfo = self.dictScanResultsDelta["infoSeverity"];
                sColorDeltaInfo = "red";

                if iValueDeltaInfo < 0:

                    sColorDeltaInfo = "lime";

                else:

                    if iValueDeltaInfo == 0:

                        sColorDeltaInfo = "yellow";

                asObjDetail.append("<tr align=\"center\" bgcolor=\"lavender\">");
                asObjDetail.append("<td><i>%s</i></td>" % ("calculated delta"));
                asObjDetail.append("<td>-------</td>");
                asObjDetail.append("<td colspan=\"8\"></td>");
                asObjDetail.append("<td bgcolor=\"%s\">%d</td>" % (sColorDeltaHigh,   self.dictScanResultsDelta["highSeverity"]));
                asObjDetail.append("<td bgcolor=\"%s\">%d</td>" % (sColorDeltaMedium, self.dictScanResultsDelta["mediumSeverity"]));
                asObjDetail.append("<td bgcolor=\"%s\">%d</td>" % (sColorDeltaLow,    self.dictScanResultsDelta["lowSeverity"]));
                asObjDetail.append("<td bgcolor=\"%s\">%d</td>" % (sColorDeltaInfo,   self.dictScanResultsDelta["infoSeverity"]));
                asObjDetail.append("</tr>");
                asObjDetail.append("\n");

            asObjDetail.append("</table>");
            asObjDetail.append("\n");

            asObjDetail.append("</td></tr>");
            asObjDetail.append("\n");

            asObjDetail.append("</div>");
            asObjDetail.append("\n");

            if sProjScanLanguagesGap != None:

                sProjScanLanguagesGap = sProjScanLanguagesGap.strip();

            if sProjScanLanguagesStd != None:

                sProjScanLanguagesStd = sProjScanLanguagesStd.strip();

            if sProjScanLanguagesGap != None and \
                len(sProjScanLanguagesGap) > 0 or \
                sProjScanLanguagesStd != None and \
                len(sProjScanLanguagesStd) > 0:

                asObjDetail.append("<div class=\"hover_bkgr_lang%s\">" % (self.sCxProjectId));
                asObjDetail.append("\n");
                asObjDetail.append("    <span class=\"helper\"></span>");
                asObjDetail.append("\n");
                asObjDetail.append("    <div>");
                asObjDetail.append("\n");
                asObjDetail.append("        <div class=\"popupCloseButton\">X</div>");
                asObjDetail.append("\n");
                asObjDetail.append("        <p><b>Gap Languages: %s</b><br>Standard Languages: %s</p>" % (sProjScanLanguagesGap, sProjScanLanguagesStd));
                asObjDetail.append("\n");
                asObjDetail.append("    </div>");
                asObjDetail.append("\n");
                asObjDetail.append("</div>");
                asObjDetail.append("\n");

        return ''.join(asObjDetail);

    def __str__(self):

        return self.toString();

    def __repr__(self):

        return self.toString();

    def addCxProjectScanToCxProjectData(self, cxprojectscan=None):

    #   self.bTraceFlag = True;

        cxProjectScan = cxprojectscan;

        if cxProjectScan == None:

            print("");
            print("%s NO CxProjectScan object has been specified nor defined - a CxProjectScan object MUST be defined - Error!" % (self.sClassDisp));
            print("");

            return False;

        if self.dictCxProjectScans == None:

            if self.bTraceFlag == True:

                print("%s The object 'dictCxProjectScans' has NOT been set - creating an internal instance..." % (self.sClassDisp));

            self.dictCxProjectScans = collections.defaultdict(); 

        bProcessingError = False;

        try:

            sCxProjectScanId = cxProjectScan.getCxScanId();

            if sCxProjectScanId != None:

                sCxProjectScanId = sCxProjectScanId.strip();

            if sCxProjectScanId == None or \
                len(sCxProjectScanId) < 1:

                print("");
                print("%s The CxProjectScan has an 'id' that is None or 'empty' - bypassing the addition of this object - Error!" % (self.sClassDisp));
                print("");

                return False;

            self.dictCxProjectScans[sCxProjectScanId] = cxProjectScan;

            if self.bTraceFlag == True:

                print("%s <Debug> CxProjectScan 'id' of [%s] object of [%s] added to the CxProjectData..." % (self.sClassDisp, sCxProjectScanId, cxProjectScan.toString()));

            # --------------------------------------------------------------------------------------------------
            # 'dictCxScanStatus' is [{'id': 7, 'name': 'Finished', 'details': {'stage': '', 'step': ''}}], 
            # 'dictCxScanStatusFinished' is [{'id': 0, 'value': 'None'}], 
            # 'dictCxScanState' is [{'path': ' N/A (Zip File)', 'sourceId': '0000000062_000420154832_000071834169',
            #                        'filesCount': 62, 'linesOfCode': 11416, 'failedLinesOfCode': 14, 
            #                        'cxVersion': '8.8.0.72 HF4',
            #                        'languageStateCollection': 
            #                            [{'languageID': 1073741824, 'languageName': 'Common', 
            #                              'languageHash': '0206692917308612', 'stateCreationDate': '2018-08-29T20:05:16.59'},
            #                             {'languageID': 8, 'languageName': 'JavaScript', 
            #                              'languageHash': '3602822811217894', 'stateCreationDate': '2018-08-29T20:05:16.59'},
            #                             {'languageID': 512, 'languageName': 'PHP', 
            #                              'languageHash': '1085264088171134', 'stateCreationDate': '2018-08-29T20:05:16.59'}, 
            #                             {'languageID': 262144, 'languageName': 'Typescript', 
            #                              'languageHash': '1939975091058023', 'stateCreationDate': '2018-08-29T20:05:16.59'}, 
            #                             {'languageID': 64, 'languageName': 'VbScript', 
            #                              'languageHash': '1349101913133594', 'stateCreationDate': '2017-11-15T13:45:50.393'}]
            # --------------------------------------------------------------------------------------------------

            # Check that the Scan is 'Finished' 'Ok' before using for Stats update:
            
            iCxScanStatus         = cxProjectScan.dictCxScanStatus["id"];
            iCxScanStatusFinished = cxProjectScan.dictCxScanStatusFinished["id"];

            if self.bTraceFlag == True:

                print("%s <Debug> CxProjectScan 'id' of [%s] has 'iCxScanStatus' of [%s] and 'iCxScanStatusFinished' of [%s]..." % (self.sClassDisp, sCxProjectScanId, iCxScanStatus, iCxScanStatusFinished));

        #   if iCxScanStatus == 7:
            if iCxScanStatus == 7 and \
                iCxScanStatusFinished == 0:

                if self.sCxScanIdBaseline == None:

                    self.sCxScanIdBaseline = sCxProjectScanId;

                else:

                    if int(sCxProjectScanId) < int(self.sCxScanIdBaseline):

                        self.sCxScanIdBaseline = sCxProjectScanId;

                if self.sCxScanIdLatest == None:

                    self.sCxScanIdLatest = sCxProjectScanId;

                else:

                    if int(sCxProjectScanId) > int(self.sCxScanIdLatest):

                        self.sCxScanIdLatest = sCxProjectScanId;

            # Collect ALL of the 'scan' languages for this Project:

            if cxProjectScan.dictCxScanState != None and \
                len(cxProjectScan.dictCxScanState) > 0:

                listLanguageStateCollection = cxProjectScan.dictCxScanState["languageStateCollection"];

                if listLanguageStateCollection != None and \
                    len(listLanguageStateCollection) > 0:

                    for dictLanguageState in listLanguageStateCollection:

                        if dictLanguageState == None or \
                            len(dictLanguageState) < 1:

                            continue;

                        sCxProjectScanLanguage = dictLanguageState["languageName"];

                        if sCxProjectScanLanguage != None:

                            sCxProjectScanLanguage = sCxProjectScanLanguage.strip();

                        if sCxProjectScanLanguage == None or \
                            len(sCxProjectScanLanguage) < 1:

                            continue;

                        if self.cxProjectDataCollectionDefaults == None:

                            self.cxProjectDataCollectionDefaults = CxProjectDataCollectionDefaults1.CxProjectDataCollectionDefaults(trace=self.bTraceFlag);

                        sCxProjectScanLanguageType = self.cxProjectDataCollectionDefaults.getCxProjectLanguageType(cxprojectlanguage=sCxProjectScanLanguage);

                        if sCxProjectScanLanguageType != None:

                            sCxProjectScanLanguageType = sCxProjectScanLanguageType.strip();

                        if sCxProjectScanLanguageType == None or \
                            len(sCxProjectScanLanguageType) < 1:

                            continue;

                        if sCxProjectScanLanguageType == "g":

                            self.addCxProjectScanLanguageToGapList(cxprojectscanlanguage=sCxProjectScanLanguage);

                        if sCxProjectScanLanguageType == "s":

                            self.addCxProjectScanLanguageToStdList(cxprojectscanlanguage=sCxProjectScanLanguage);

        except Exception as inst:

            print("%s 'addCxProjectScanToCxProjectData()' - exception occured..." % (self.sClassDisp));
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

    def generateCxProjectDataScansDelta(self):

    #   self.bTraceFlag = True;

        if self.dictCxProjectScans == None or \
            len(self.dictCxProjectScans) < 1:

            print("");
            print("%s NO CxProjectScan object has been specified nor defined - a CxProjectScan object MUST be defined - Warning!" % (self.sClassDisp));
            print("");

            return True;

        if self.sCxScanIdBaseline == None:

            print("");
            print("%s For the Project named [%s] the 'Baseline' Scan Id [%s] is None - there are NO Scan(s) to compare -  Warning!" % (self.sClassDisp, self.sCxProjectName, self.sCxScanIdBaseline));
            print("");

            return True;

        bProcessingError = False;

        try:

            if self.bTraceFlag == True:

                print("%s <Debug> Generating the Scans 'delta' for the Project named [%s] with 'sCxScanIdBaseline' of [%s] and 'sCxScanIdLatest' of [%s]..." % (self.sClassDisp, self.sCxProjectName, self.sCxScanIdBaseline, self.sCxScanIdLatest));

            self.sCxProjectRiskSeverity = "0";
            self.sCxProjectRiskTrend    = "0";
            self.cxProjectScanBaseline  = self.dictCxProjectScans[self.sCxScanIdBaseline];

            if self.cxProjectScanBaseline == None:

                print("");
                print("%s For the Project named [%s] with 'Baseline' Scan Id [%s] the CxProjectScan object is None - Error!" % (self.sClassDisp, self.sCxProjectName, self.sCxScanIdBaseline));
                print("");

                return False;

            self.sCxProjectRiskSeverity  = self.cxProjectScanBaseline.sCxScanRiskSeverity;
            self.sCxProjectRiskTrend     = "0";
            self.dictScanResultsBaseline = self.cxProjectScanBaseline.dictCxScanResultsStats;

            if self.dictScanResultsBaseline == None or \
                len(self.dictScanResultsBaseline) < 1:

                print("");
                print("%s For the Project named [%s] the 'Baseline' Scan Id [%s] CxProjectScan object contains a Scan results dictionary object is None or 'empty' - Error!" % (self.sClassDisp, self.sCxProjectName, self.sCxScanIdBaseline));
                print("");

                return False;

            if self.sCxScanIdLatest == self.sCxScanIdBaseline:

                self.dictScanResultsDelta = collections.defaultdict(int);

                self.dictScanResultsDelta["highSeverity"]   = self.dictScanResultsBaseline["highSeverity"];  
                self.dictScanResultsDelta["mediumSeverity"] = self.dictScanResultsBaseline["mediumSeverity"];
                self.dictScanResultsDelta["lowSeverity"]    = self.dictScanResultsBaseline["lowSeverity"];   
                self.dictScanResultsDelta["infoSeverity"]   = self.dictScanResultsBaseline["infoSeverity"];  

                return True;

            self.cxProjectScanLatest = self.dictCxProjectScans[self.sCxScanIdLatest];

            if self.cxProjectScanLatest == None:

                print("");
                print("%s For the Project named [%s] the 'Latest' Scan Id [%s] the CxProjectScan object is None - Error!" % (self.sClassDisp, self.sCxProjectName, self.sCxScanIdLatest));
                print("");

                return False;

            self.sCxProjectRiskSeverity = self.cxProjectScanLatest.sCxScanRiskSeverity;
            self.sCxProjectRiskTrend    = "0";
            self.dictScanResultsLatest  = self.cxProjectScanLatest.dictCxScanResultsStats;

            if self.dictScanResultsLatest == None or \
                len(self.dictScanResultsLatest) < 1:

                print("");
                print("%s For the Project named [%s] the 'Latest' Scan Id [%s] CxProjectScan contains a Scan results dictionary object is None or 'empty' - Error!" % (self.sClassDisp, self.sCxProjectName, self.sCxScanIdLatest));
                print("");

                return False;

            # --------------------------------------------------------------------------------------------------
            # 'sCxScanIdBaseline' is [1450342], 'sCxScanIdLatest' is [1450378]. 
            #
            #     'sCxScanId' is [1450378], 
            #     'dictCxScanResultsStats' is [
            #         {'highSeverity': 0, 
            #         'mediumSeverity': 6,
            #         'lowSeverity': 27, 
            #         'infoSeverity': 0, 
            #         'statisticsCalculationDate': '2019-04-06T16:59:44.84'}]
            #
            #     'sCxScanId' is [1450342], 
            #     'dictCxScanResultsStats' is [
            #         {'highSeverity': 0, 
            #         'mediumSeverity': 0,
            #         'lowSeverity': 22,
            #         'infoSeverity': 0, 
            #         'statisticsCalculationDate': '2019-03-20T13:13:12.383'}]
            # --------------------------------------------------------------------------------------------------

            self.dictScanResultsDelta = collections.defaultdict(int);

            iScanResultHighDelta   = (self.dictScanResultsLatest["highSeverity"]   - self.dictScanResultsBaseline["highSeverity"]);
            iScanResultMediumDelta = (self.dictScanResultsLatest["mediumSeverity"] - self.dictScanResultsBaseline["mediumSeverity"]);
            iScanResultLowDelta    = (self.dictScanResultsLatest["lowSeverity"]    - self.dictScanResultsBaseline["lowSeverity"]);
            iScanResultInfoDelta   = (self.dictScanResultsLatest["infoSeverity"]   - self.dictScanResultsBaseline["infoSeverity"]);

            self.dictScanResultsDelta["highSeverity"]   = iScanResultHighDelta;
            self.dictScanResultsDelta["mediumSeverity"] = iScanResultMediumDelta;
            self.dictScanResultsDelta["lowSeverity"]    = iScanResultLowDelta;
            self.dictScanResultsDelta["infoSeverity"]   = iScanResultInfoDelta;

            iCxProjectRiskTrend      = ((iScanResultHighDelta * 4) + (iScanResultMediumDelta * 3) + (iScanResultLowDelta * 2) + (iScanResultInfoDelta * 1));
            self.sCxProjectRiskTrend = ("%d" % (iCxProjectRiskTrend));

        except Exception as inst:

            print("%s 'generateCxProjectDataScansDelta()' - exception occured..." % (self.sClassDisp));
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

