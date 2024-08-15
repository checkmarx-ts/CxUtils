""" 
========================================================================

SCA DATA EXTRACTOR ALL TRIAGES PRODUCER

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
OUT_SUMMARY             = 'sca_alltriagessummary.csv'
OUT_TRIAGES             = 'sca_alltriages.csv'

# CSV file headers
CSV_SUMMARY             = ['PROJ-ID', 'PROJ-NAME', 'TRIAGE-COUNT']
CSV_TRIAGES             = ['PROJ-ID', 'PROJ-NAME', 'PACKAGE-ID', 'RESULT-ID', 'RESULT-STATE', 'DATE']



class scaalltriages(baserunner) :

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
        cachedata = self.cache(scacachetype.projects)
        try :
            for project in cachedata :
                lcount          = 0
                projid          = project['id'] 
                projname        = project['name']
                cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname )
                triages = self.conn.sca.get('/risk-management/risk-state/' + projid )
                for triage in triages :
                    lcount += 1
                    # Write triagged result
                    self.__triagwriter.writerow( [
                        projid,
                        projname,
                        triage['packageId'],
                        triage['vulnerabilityId'],
                        triage['state'],
                        triage['createdOn'] ] )
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
            cxlogger.verbose( 'Extracting all triages from SCA' ) 
            cxlogger.verbose( 'Extraction started: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Processing all sca triages')
            # Extracts triage counts
            errorcount += self.triages_extractalldata() if errorcount == 0 else 0
            # Done
            cxlogger.verbose( 'Sca all triages processed' )
        finally :
            dtend = datetime.now()
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Extraction ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            self.closedatafiles()
