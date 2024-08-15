""" 
========================================================================

CXONE DATA EXTRACTOR TRIAGE COUNTER PRODUCER

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
OUT_TRIAGES             = 'cxone_triagescount.csv'

# CSV file headers
CSV_TRIAGES             = ['PROJECT-ID', 'PROJECT-NAME',
                           'SAST-SCAN-ID', 'SAST-SCAN-DATE', 'SAST-HIGH', 'SAST-MEDIUM', 'SAST-LOW', 'SAST-INFO', 'SAST-OTHER',
                           'SAST-TO-VERIFY', 'SAST-NOT-EXPLOITABLE', 'SAST-CONFIRMED', 'SAST-URGENT', 'SAST-PROPOSED-NOT-EXPLOITABLE', 'SAST-OTHER-STATE',
                           'SCA-SCAN-ID', 'SCA-SCAN-DATE', 'SCA-HIGH', 'SCA-MEDIUM', 'SCA-LOW', 'SCA-INFO', 'SCA-OTHER',
                           'SCA-TO-VERIFY', 'SCA-NOT-EXPLOITABLE', 'SCA-CONFIRMED', 'SCA-URGENT', 'SCA-PROPOSED-NOT-EXPLOITABLE', 'SCA-OTHER-STATE',
                           'IAC-SCAN-ID', 'IAC-SCAN-DATE', 'IAC-HIGH', 'IAC-MEDIUM', 'IAC-LOW', 'IAC-INFO', 'IAC-OTHER',
                           'IAC-TO-VERIFY', 'IAC-NOT-EXPLOITABLE', 'IAC-CONFIRMED', 'IAC-URGENT', 'IAC-PROPOSED-NOT-EXPLOITABLE', 'IAC-OTHER-STATE',
                           'APISEC-SCAN-ID', 'APISEC-SCAN-DATE', 'APISEC-HIGH', 'APISEC-MEDIUM', 'APISEC-LOW', 'APISEC-INFO', 'APISEC-OTHER',
                           'APISEC-TO-VERIFY', 'APISEC-NOT-EXPLOITABLE', 'APISEC-CONFIRMED', 'APISEC-URGENT', 'APISEC-PROPOSED-NOT-EXPLOITABLE', 'APISEC-OTHER-STATE']



class cxonecounttriages(baserunner) :

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
        if (self.__triaghandler):
            self.__triaghandler.close()



    def triages_extractdata(self) :
        errorcount = 0
        cachedata = self.cache(cxonecachetype.projectsfull)
        try :
            for project in cachedata :
                lcount          = 0
                projid          = project['id'] 
                projname        = project['name']
                cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname )

                lcount += project['sastLastScan']['notexploitable'] if project['sastLastScan']['notexploitable'] else 0
                lcount += project['sastLastScan']['confirmed'] if project['sastLastScan']['confirmed'] else 0
                lcount += project['sastLastScan']['urgent'] if project['sastLastScan']['urgent'] else 0
                lcount += project['sastLastScan']['proposednotexploitable'] if project['sastLastScan']['proposednotexploitable'] else 0
                lcount += project['sastLastScan']['otherstate'] if project['sastLastScan']['otherstate'] else 0

                lcount += project['scaLastScan']['notexploitable'] if project['scaLastScan']['notexploitable'] else 0
                lcount += project['scaLastScan']['confirmed'] if project['scaLastScan']['confirmed'] else 0
                lcount += project['scaLastScan']['urgent'] if project['scaLastScan']['urgent'] else 0
                lcount += project['scaLastScan']['proposednotexploitable'] if project['scaLastScan']['proposednotexploitable'] else 0
                lcount += project['scaLastScan']['otherstate'] if project['scaLastScan']['otherstate'] else 0

                lcount += project['kicsLastScan']['notexploitable'] if project['kicsLastScan']['notexploitable'] else 0
                lcount += project['kicsLastScan']['confirmed'] if project['kicsLastScan']['confirmed'] else 0
                lcount += project['kicsLastScan']['urgent'] if project['kicsLastScan']['urgent'] else 0
                lcount += project['kicsLastScan']['proposednotexploitable'] if project['kicsLastScan']['proposednotexploitable'] else 0
                lcount += project['kicsLastScan']['otherstate'] if project['kicsLastScan']['otherstate'] else 0

                lcount += project['apisecLastScan']['notexploitable'] if project['apisecLastScan']['notexploitable'] else 0
                lcount += project['apisecLastScan']['confirmed'] if project['apisecLastScan']['confirmed'] else 0
                lcount += project['apisecLastScan']['urgent'] if project['apisecLastScan']['urgent'] else 0
                lcount += project['apisecLastScan']['proposednotexploitable'] if project['apisecLastScan']['proposednotexploitable'] else 0
                lcount += project['apisecLastScan']['otherstate'] if project['apisecLastScan']['otherstate'] else 0

                # Write triage counts
                self.__triagwriter.writerow( [
                    projid,
                    projname,
                    # SAST
                    project['sastLastScan']['scanid'],
                    project['sastLastScan']['created'],
                    project['sastLastScan']['high'],
                    project['sastLastScan']['medium'],
                    project['sastLastScan']['low'],
                    project['sastLastScan']['info'],
                    project['sastLastScan']['otherseverity'],
                    project['sastLastScan']['toverify'],
                    project['sastLastScan']['notexploitable'],
                    project['sastLastScan']['confirmed'],
                    project['sastLastScan']['urgent'],
                    project['sastLastScan']['proposednotexploitable'],
                    project['sastLastScan']['otherstate'],
                    # SCA
                    project['scaLastScan']['scanid'],
                    project['scaLastScan']['created'],
                    project['scaLastScan']['high'],
                    project['scaLastScan']['medium'],
                    project['scaLastScan']['low'],
                    project['scaLastScan']['info'],
                    project['scaLastScan']['otherseverity'],
                    project['scaLastScan']['toverify'],
                    project['scaLastScan']['notexploitable'],
                    project['scaLastScan']['confirmed'],
                    project['scaLastScan']['urgent'],
                    project['scaLastScan']['proposednotexploitable'],
                    project['scaLastScan']['otherstate'],
                    # IAC
                    project['kicsLastScan']['scanid'],
                    project['kicsLastScan']['created'],
                    project['kicsLastScan']['high'],
                    project['kicsLastScan']['medium'],
                    project['kicsLastScan']['low'],
                    project['kicsLastScan']['info'],
                    project['kicsLastScan']['otherseverity'],
                    project['kicsLastScan']['toverify'],
                    project['kicsLastScan']['notexploitable'],
                    project['kicsLastScan']['confirmed'],
                    project['kicsLastScan']['urgent'],
                    project['kicsLastScan']['proposednotexploitable'],
                    project['kicsLastScan']['otherstate'],
                    # API-SEC
                    project['apisecLastScan']['scanid'],
                    project['apisecLastScan']['created'],
                    project['apisecLastScan']['high'],
                    project['apisecLastScan']['medium'],
                    project['apisecLastScan']['low'],
                    project['apisecLastScan']['info'],
                    project['apisecLastScan']['otherseverity'],
                    project['apisecLastScan']['toverify'],
                    project['apisecLastScan']['notexploitable'],
                    project['apisecLastScan']['confirmed'],
                    project['apisecLastScan']['urgent'],
                    project['apisecLastScan']['proposednotexploitable'],
                    project['apisecLastScan']['otherstate']
                    ] )

                cxlogger.verbose( '  - Triages for [' + str(projid) + '] ' + projname + ' (' + str(lcount) + ')', False )
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
            cxlogger.verbose( 'Extracting triage counts from CXONE' )            
            cxlogger.verbose( 'Extraction started: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Processing cxone triage counts')
            # Extracts triage counts
            errorcount += self.triages_extractdata() if errorcount == 0 else 0
            # Done
            cxlogger.verbose( 'Cxone triage counts processed' )
        finally :
            dtend = datetime.now()
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Extraction ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            self.closedatafiles()


