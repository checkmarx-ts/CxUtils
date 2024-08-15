""" 
========================================================================

SAST DATA EXTRACTOR TRIAGE COUNTER PRODUCER

joao.costa@checkmarx.com
PS-EMEA
01-07-2023

========================================================================
"""


import os
import csv
from datetime import datetime
from cxloghandler import cxlogger
from config import config
from baserunner import baserunner
from sastcache import sastcachetype



# CSV output files
OUT_TRIAGES             = 'sast_triagescount.csv'
CSV_HEADER              = ['PROJ-ID', 'PROJ-NAME', 'TEAM-NAME', 'SCAN-ID', 'SCAN-REQUESTED', 'TOTAL-RESULTS', 'HIGH', 'MEDIUM', 'LOW', 'INFO' ]


class sastcounttriages(baserunner) :

    def __init__(self):
        # Well known file for csv containing triages
        self.__triaghandler = None
        self.__triagwriter  = None
        super().__init__



    def __init__(self, config: config, conn = None, caches = None, verbose = None, csvseparator = None) :
        # Well known file for csv containing triages
        self.__triaghandler = None
        self.__triagwriter  = None
        super().__init__(config, conn, caches, verbose, csvseparator)



    def preparedatafiles(self) :
        try :
            filename = self.datapath() + os.sep + OUT_TRIAGES
            if os.path.exists(filename) :
                os.remove(filename)
            self.__triaghandler = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
            self.__triagwriter  = csv.writer(self.__triaghandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            return True
        except Exception as e:
            cxlogger.verbose( 'Unable to create output files with "' + str(e) + '"', True, False, True, e )    
            self.closedatafiles()
            return False
        


    def closedatafiles(self) :
        if (self.__triaghandler):
            self.__triaghandler.close()



    def triages_extractdata(self) :
        errorcount = 0
        cachedata = self.cacheoneof([sastcachetype.projectssimple, sastcachetype.projectsfull])
        try :
            for state in self.cache(sastcachetype.result_states) :
                if not state['ResultName'] == 'To Verify' :
                    CSV_HEADER.append(state['ResultName'].upper())
            self.__triagwriter.writerow(CSV_HEADER)

            for project in cachedata :

                projid          = project['id'] 
                projname        = project['name']
                projteam        = project['teamFullName']
                scanid          = project['lastScanId']
                cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname )

                if projid and scanid :

                    # Compose the row
                    row = [ projid,
                            projname,
                            projteam,
                            scanid,
                            project['lastScanRequestedOn'],
                            project['TotalVulnerabilities'],
                            project['High'],
                            project['Medium'],
                            project['Low'],
                            project['Info'] ]

                    # Count by state
                    for state in self.cache(sastcachetype.result_states) :
                        if not state['ResultName'] == 'To Verify' :
                            try :
                                xcount = self.conn.odata.get('/Cxwebinterface/odata/v1/Scans(' + str(scanid) + ')/Results/$count?$filter=StateId eq ' + str(state['ResultID']) )
                                if xcount :
                                    scount = int(xcount)
                                else :
                                    scount = 0
                            except :
                                scount = 0
                            if scount <= 0 :
                                scount = None
                            row.append(scount)
                    self.__triagwriter.writerow(row)

        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def execute(self) :
        errorcount = 0
        dtini = datetime.now()
        # Prepare the data files
        if not self.preparedatafiles() :
            exit(1)
        try :
            cxlogger.verbose( '============================================================' )
            cxlogger.verbose( 'Extracting triage counts from SAST' )            
            cxlogger.verbose( 'Extraction started: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Processing sast triage counts')
            # Extracts triage counts
            errorcount += self.triages_extractdata() if errorcount == 0 else 0
            # Done
            cxlogger.verbose( 'Sast triage counts processed' )
        finally :
            dtend = datetime.now()
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Extraction ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            self.closedatafiles()
