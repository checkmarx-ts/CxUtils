""" 
========================================================================

SCA DATA EXTRACTOR TRIAGE COUNTER PRODUCER

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
from scacache import scacachetype



# CSV output files
OUT_TRIAGES             = 'sca_triagescount.csv'

# CSV file headers
CSV_TRIAGES             = ['PROJ-ID', 'PROJ-NAME', 
                           'DIRECT-PACKAGES', 'TOTAL-PACKAGES', 'OUTDATED-PACKAGES', 'HIGH', 'MEDIUM', 'LOW', 'IGNORED',                           
                           'TO-VERIFY', 'NOT-EXPLOITABLE', 'CONFIRMED', 'URGENT', 'PROPOSED-NOT-EXPLOITABLE']



class scacounttriages(baserunner) :

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
            self.__triagwriter.writerow(CSV_TRIAGES)
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
        cachedata = self.cache(scacachetype.projects)
        try :
            for project in cachedata :
                lcount          = 0
                projid          = project['id'] 
                projname        = project['name']
                cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname )
                # toverify        = 0
                # notexploitable  = 0
                # confirmed       = 0
                # urgent          = 0
                # proposed        = 0
                counts = {}
                counts['ToVerify']                = 0
                counts['NotExploitable']          = 0
                counts['Confirmed']               = 0
                counts['Urgent']                  = 0
                counts['ProposedNotExploitable']  = 0

                triages = self.conn.sca.get('/risk-management/risk-state/' + projid )
                for triage in triages :
                    lcount += 1
                    for triage in triages :
                        state = triage['state']
                        counts[state] = counts[state] + 1

                # Write triagged result
                self.__triagwriter.writerow( [
                    projid,
                    projname,
                    project['directPackages'] if project['directPackages'] else None,
                    project['totalPackages'] if project['totalPackages'] else None,
                    project['totalOutdatedPackages'] if project['totalOutdatedPackages'] else None,
                    project['highVulnerabilityCount'] if project['highVulnerabilityCount'] else None,
                    project['mediumVulnerabilityCount'] if project['mediumVulnerabilityCount'] else None,
                    project['lowVulnerabilityCount'] if project['lowVulnerabilityCount'] else None,
                    project['ignoredVulnerabilityCount'] if project['ignoredVulnerabilityCount'] else None,
                    counts['ToVerify'] if counts['ToVerify'] else None,
                    counts['NotExploitable'] if counts['NotExploitable'] else None,
                    counts['Confirmed'] if counts['Confirmed'] else None,
                    counts['Urgent'] if counts['Urgent'] else None,
                    counts['ProposedNotExploitable'] if counts['ProposedNotExploitable'] else None
                    ] )                  

                cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname + ' (' + str(lcount) + ')', False)
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
            cxlogger.verbose( 'Extracting triage counts from SCA' )
            cxlogger.verbose( 'Extraction started: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Processing sca triage counts')
            # Extracts triage counts
            errorcount += self.triages_extractdata() if errorcount == 0 else 0
            # Done
            cxlogger.verbose( 'Sca triage counts processed' )
        finally :
            dtend = datetime.now()
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Extraction ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            self.closedatafiles()
