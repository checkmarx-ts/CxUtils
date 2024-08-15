""" 
========================================================================

CXONE DATA EXTRACTOR ALL TRIAGES PRODUCER

joao.costa@checkmarx.com
PS-EMEA
22-06-2023

========================================================================
"""

import os
import csv
from datetime import datetime
from config import config
from cxloghandler import cxlogger
from baserunner import baserunner
from cxonecache import cxonecachetype



# CSV output files
OUT_SUMMARY             = 'cxone_alltriagessummary.csv'
OUT_TRIAGES             = 'cxone_alltriages.csv'

# CSV file headers
CSV_SUMMARY             = ['PROJ-ID', 'PROJ-NAME', 'TRIAGE-COUNT']
CSV_TRIAGES             = ['PROJ-ID', 'PROJ-NAME', 'SCAN-TYPE', 'RESULT-ID', 'SCAN-ID', 'SIMILARITY-ID', 'RESULT-STATUS', 'RESULT-STATE', 'RESULT-SEVERITY', 'CONFIDENCE-LEVEL',
                           'TRIAGE-DATE', 'FIRST-FOUND', 'QUERY-ID', 'QUERY-NAME', 'QUERY-GROUP', 'QUERY-LANGUAGE']


class cxonealltriages(baserunner) :

    def __init__(self):
        # Well known file for csv containing summary
        self.__sumryhandler = None
        self.__sumrywriter  = None
        # Well known file for csv containing triages
        self.__triaghandler = None
        self.__triagwriter  = None
        super().__init__



    def __init__(self, config: config, conn = None, caches = None, verbose = None, csvseparator = None) :
        # Well known file for csv containing summary
        self.__sumryhandler = None
        self.__sumrywriter  = None
        # Well known file for csv containing triages
        self.__triaghandler = None
        self.__triagwriter  = None
        super().__init__(config, conn, caches, verbose, csvseparator)



    def preparedatafiles(self) :
        try :
            # Well known file for csv containing summary
            filename = self.datapath() + os.sep + OUT_SUMMARY
            if os.path.exists(filename) :
                os.remove(filename)
            self.__sumryhandler = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
            self.__sumrywriter = csv.writer(self.__sumryhandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            self.__sumrywriter.writerow(CSV_SUMMARY)
            # Well known file for csv containing triages
            filename = self.datapath() + os.sep + OUT_TRIAGES
            if os.path.exists(filename) :
                os.remove(filename)
            self.__triaghandler = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
            self.__triagwriter  = csv.writer(self.__triaghandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            self.__triagwriter.writerow(CSV_TRIAGES)
            return True
        except Exception as e:
            cxlogger.verbose( 'Unable to create output files with "' + str(e) + '"', True, False, True, e )    
            self.closedatafiles()
            return False



    def closedatafiles(self) :
        if (self.__sumryhandler):
            self.__sumryhandler.close()
        if (self.__triaghandler):
            self.__triaghandler.close()



    def triages_extractalldata(self) :
        errorcount = 0
        cachedata = self.cache(cxonecachetype.projectsfull)
        try :
            lcount = 0
            for project in cachedata :
                lcount      = 0
                projid      = project['id'] 
                projname    = project['name']
                cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname )

                scanids = []
                if project['sastLastScan']['scanid'] :
                    scanids.append(project['sastLastScan']['scanid'])
                if project['scaLastScan']['scanid'] :
                    scanids.append(project['scaLastScan']['scanid'])
                if project['kicsLastScan']['scanid'] :
                    scanids.append(project['kicsLastScan']['scanid'])
                if project['apisecLastScan']['scanid'] :
                    scanids.append(project['apisecLastScan']['scanid'])
                scanids = set(scanids)

                for scanid in scanids :
                    lskip = 0
                    olist = self.conn.ast.get('/api/results?offset=' + str(lskip) + '&limit=100&scan-id=' + scanid )

                    while olist and olist['results'] and len(olist['results']) > 0 :

                        for triage in olist['results'] :
                            if triage['state'] != 'TO_VERIFY' :
                                lcount          += 1
                                cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname + ' (' + str(lcount) + ')', False)
                                queryId         = None
                                queryName       = None
                                querygroup      = None
                                querylanguage   = None

                                if triage['type'] == 'kics' :
                                    queryId         = triage['data']['queryId']
                                    queryName       = triage['data']['queryName']
                                    querygroup      = triage['data']['group']
                                    queryId         = queryId.replace('[Taken from query_id]', '').strip()
                                    querygroup      = querygroup.replace('[Taken from category]', '').strip()
                                elif triage['type'] == 'sca' :
                                    queryId         = triage['vulnerabilityDetails']['cweId']
                                    queryName       = triage['data']['packageIdentifier']
                                    if triage['vulnerabilityDetails']['cvss'] :
                                        querygroup  = triage['vulnerabilityDetails']['cvss']['attackVector']
                                else :
                                    queryId         = triage['data']['queryId']
                                    queryName       = triage['data']['queryName']
                                    querygroup      = triage['data']['group']
                                    querylanguage   = triage['data']['languageName']

                                self.__triagwriter.writerow( [
                                    projid,
                                    projname,
                                    triage['type'],
                                    triage['id'],
                                    scanid,
                                    triage['similarityId'],
                                    triage['status'],
                                    triage['state'],
                                    triage['severity'],
                                    triage['confidenceLevel'],
                                    triage['created'],
                                    triage['firstFoundAt'],
                                    # triage['comments'],     # Comments do not seem to come in payload
                                    queryId,
                                    queryName,
                                    querygroup,
                                    querylanguage
                                    ] )

                        lskip += 100
                        olist = self.conn.ast.get('/api/results?offset=' + str(lskip) + '&limit=100&scan-id=' + scanid )
                    cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname + ' (' + str(lcount) + ')', False)
                cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname + ' (' + str(lcount) + ')', False)
                self.__sumrywriter.writerow( [ projid, projname, lcount ] )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname + ' (' + str(lcount) + ') failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def execute(self) :
        errorcount = 0
        dtini = datetime.now()
        # Prepare the data files
        if not self.preparedatafiles() :
            exit(1)
        try :
            cxlogger.verbose( '============================================================' )
            cxlogger.verbose( 'Extracting all triages from CXONE' )            
            cxlogger.verbose( 'Extraction started: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Processing all cxone triages')
            # Extracts triage counts
            errorcount += self.triages_extractalldata() if errorcount == 0 else 0
            # Done
            cxlogger.verbose( 'Cxone all triages processed' )
        finally :
            dtend = datetime.now()
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Extraction ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            self.closedatafiles()



