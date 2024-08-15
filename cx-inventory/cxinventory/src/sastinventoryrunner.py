""" 
========================================================================

SAST DATA EXTRACTOR INVENTORY PRODUCER

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
from cxglobfilters import globfilters
from baserunner import baserunner
from sastcache import sastcachetype
from sastdefaultpresets import sastdefaultpresets
from sastdefaultcategories import sastdefaultcategories


# MAX LOC REF
MAX_LOC                 = 9500000
MAX_LOC_TXT             = '9.5M'

# Sanity status
SOK                     = 0
SWARNING                = 1
SFATAL                  = 2
STATUS                  = ['OK', 'WARNING', 'DANGER']

# Preset query status
QOK                     = 0
QADDED                  = 1
QMISSING                = 2
QSTATUS                 = ['MATCH', 'QUERY-ADDED', 'QUERY-REMOVED']

# Preset types
PTYPE_OOB               = 'Checkmarx'
PTYPE_CUSTOM            = 'Customer'

# CSV output files
OUT_SUMMARY             = 'sast_inventorysummary.csv'
OUT_INVENTORY           = 'sast_inventory.csv'
OUT_PROJECTS            = 'sast_inventoryprojects.csv'
OUT_PRESETQUERIES       = 'sast_inventorypresets.csv'

# CSV file headers
CSV_SUMMARY             = ['STATUS', 'OBJ-TYPE', 'OBJ-COUNT', 'INFO']
CSV_INVENTORY           = ['STATUS', 'OBJ-TYPE', 'OBJ-ID', 'OBJ-NAME', 'PROJ-USING', 'INFO']
CSV_PROJECTS            = ['STATUS', 'ID', 'NAME', 'DUPLICATED', 'ISPUBLIC', 'CREATED', 'TEAM-ID', 'TEAM-NAME', 'PRESET', 'ENGINE-CONFIG', 
                           'CUSTOM-FIELDS', 'EMAIL-NOTIFICATIONS', 'ISSUE-TRACKER', 'EXCLUSIONS-FILES', 'EXCLUSIONS-FOLDERS', 'EXCLUSIONS-GLOB', 'SCHEDULED-SCANS', 
                           'PRE-SCAN-ACTION', 'POST-SCAN-ACTION', 'CUSTOM-CORP-QUERIES', 'CUSTOM-TEAM-QUERIES', 'CUSTOM-PROJ-QUERIES',
                           'REPOSITORY-TYPE', 'PLUGIN', 'ORIGIN', 'LAST-SCAN-ID', 'LAST-SCAN-DATE', 'LOC', 'LANGUAGES', 'TOTAL-SCANS', 
                           'TOTAL-RESULTS', 'HIGH', 'MEDIUM', 'LOW', 'INFO', 'TRIAGES', 'CUSTOM-STATES', 'INFO']
CSV_PRESETQUERIES       = ['STATUS','PRESET-ID','PRESET-NAME','PRESET-TYPE','QUERY-STATUS','QUERY-ID','QUERY-NAME','QUERY-LANGUAGE','QUERY-GROUP','QUERY-PACKAGE-TYPE']

# OBJECT TYPE
OBJ_SAST_INSTANCE       = 'SAST-INSTANCE'
OBJ_ENGINE_CONFIG       = 'ENGINE-CONFIG'
OBJ_ENGINE_SERVER       = 'ENGINE-SERVER'
OBJ_CUSTOM_FIELDS       = 'CUSTOM-FIELD'
OBJ_SMTP_SETTINGS       = 'SMTP-SETTINGS'
OBJ_ISSUE_TRACKER       = 'ISSUE-TRACKER'
OBJ_PRE_SCAN_ACTION     = 'PRE-SCAN-ACTION'
OBJ_POST_SCAN_ACTION    = 'POST-SCAN-ACTION'
OBJ_RESULT_STATES       = 'RESULT-STATE'
OBJ_AC_SAML             = 'AC-SAML-SETTINGS'
OBJ_AC_LDAP             = 'AC-LDAP-SETTINGS'
OBJ_AC_DOMAIN           = 'AC-DOMAIN-SETTINGS'
OBJ_AC_TEAMS            = 'AC-TEAMS'
OBJ_AC_ROLES            = 'AC-ROLES'
OBJ_AC_USERS_APP        = 'AC-USERS-APPLICATION'
OBJ_AC_USERS_OTHER      = 'AC-USERS-EXTERNAL'
OBJ_AC_USERS_EMAILS     = 'AC-USERS-EMAIL-DOMAINS'
OBJ_PRESETS             = 'PRESETS'
OBJ_QUERIES_CORP        = 'CUSTOM-QUERIES-CORP'
OBJ_QUERIES_TEAM        = 'CUSTOM-QUERIES-TEAM'
OBJ_QUERIES_PROJ        = 'CUSTOM-QUERIES-PROJ'
OBJ_QUERY_CATEGORIES    = 'CUSTOM-QUERY-CATEGORIES'
OBJ_PROJECTS            = 'PROJECTS'
OBJ_ORIGINS             = 'SCAN-ORIGINS'
OBJ_CONSTRAINTS         = 'CONSTRAINTS'




class sastinventory(baserunner) :

    def __init__(self):
        # Well known file for csv containing summary
        self.__sumryhandler = None
        self.__sumrywriter  = None
        # Well known file for csv containing inventory
        self.__datahandler  = None
        self.__datawriter   = None
        # Well known file for csv containing projects
        self.__projshandler = None
        self.__projswriter  = None
        # Well known file for csv containing preset queries
        self.__psetqhandler = None
        self.__psetqwriter  = None
        # Controlling caches
        self.__xpresets     = []    # list of detected customized or new presets
        self.__xcorpqry     = []    # list of projects affected by corp level queries
        self.__xteamqry     = []    # list of projects affected by team level queries
        self.__xprojqry     = []    # list of projects affected by proj level queries
        super().__init__



    def __init__(self, config: config, conn = None, caches = None, verbose = None, csvseparator = None) :
        # Well known file for csv containing summary
        self.__sumryhandler = None
        self.__sumrywriter  = None
        # Well known file for csv containing inventory
        self.__datahandler  = None
        self.__datawriter   = None
        # Well known file for csv containing projects
        self.__projshandler = None
        self.__projswriter  = None
        # Well known file for csv containing preset queries
        self.__psetqhandler = None
        self.__psetqwriter  = None
        # Controlling caches
        self.__xpresets     = []    # list of detected customized or new presets
        self.__xcorpqry     = []    # list of projects affected by corp level queries
        self.__xteamqry     = []    # list of projects affected by team level queries
        self.__xprojqry     = []    # list of projects affected by proj level queries
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
            # Well known file for csv containing inventory
            filename = self.datapath() + os.sep + OUT_INVENTORY
            if os.path.exists(filename) :
                os.remove(filename)
            self.__datahandler  = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
            self.__datawriter   = csv.writer(self.__datahandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            self.__datawriter.writerow(CSV_INVENTORY)
            # Well known file for csv containing projects
            filename = self.datapath() + os.sep + OUT_PROJECTS
            if os.path.exists(filename) :
                os.remove(filename)
            self.__projshandler = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
            self.__projswriter  = csv.writer(self.__projshandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            self.__projswriter.writerow(CSV_PROJECTS)
            # Well known file for csv containing preset queries
            filename = self.datapath() + os.sep + OUT_PRESETQUERIES
            if os.path.exists(filename) :
                os.remove(filename)
            self.__psetqhandler = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
            self.__psetqwriter  = csv.writer(self.__psetqhandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            self.__psetqwriter.writerow(CSV_PRESETQUERIES)
            # Done
            return True
        except Exception as e:
            self.closedatafiles()
            cxlogger.verbose( 'Unable to create output files with "' + str(e) + '"', True, False, True, e )    
            return False



    def closedatafiles(self) :
        if (self.__sumryhandler):
            self.__sumryhandler.close()
        if (self.__datahandler):
            self.__datahandler.close()
        if (self.__projshandler):
            self.__projshandler.close()
        if (self.__psetqhandler):
            self.__psetqhandler.close()




    def inventory_sastinstance(self) :
        errorcount = 0
        SOBJECT = OBJ_SAST_INSTANCE
        SSTATUS = SOK
        inventory_name = 'sast instance'
        sinfo = None
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try: 
            sastversion = None
            sastname = self.config.value('sast.url') + ', version ' + self.conn.versionstring
            sastverz = self.conn.version['version']
            if sastverz :
                sastverx = sastverz.split('.')
                if len(sastverx) >= 2 :
                    sastversion = float( sastverx[0] + '.' + sastverx[1] )
            # Is version below 9.5
            if sastversion and sastversion < 9.5 :
                SSTATUS = SFATAL
                sinfo = 'version is below 9.5'
            # Register inventory
            self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, None, sastname, None, sinfo ] )
            # Register SUMMARY
            if sinfo :
                sinfo = sastname + ', ' +  sinfo
            else :
                sinfo = sastname
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, 1, sinfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (1) ' + self.duration(dtini, True), False)
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount
    


    def inventory_engineconfigs(self) :
        cachedata = self.cache(sastcachetype.engine_configs)
        SOBJECT = OBJ_ENGINE_CONFIG
        SSTATUS = SOK
        ginfo = None
        inuse = 0
        errorcount = 0
        inventory_name = 'engine configurations'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                itemstatus = SOK
                # Is it used by projects ?
                projusing = list( filter( lambda el: item['id'] == el['engineConfigurationId'], self.cache(sastcachetype.projectsfull) ) )
                # Sanity check
                if item['IsCustom'] and len(projusing) > 0 :
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    inuse += 1
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], len(projusing), None ] )
            # Register index
            if inuse > 0 :
                ginfo = str(inuse) + ' custom configurations in use'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False)
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False,True, e )
        return errorcount



    def inventory_engineservers(self) :
        cachedata = self.cache(sastcachetype.engines_servers)
        SOBJECT = OBJ_ENGINE_SERVER
        SSTATUS = SOK
        errorcount = 0
        inventory_name = 'engine servers'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], None, 'Max Scans: ' + str(item['maxScans']) + ', range: ' + str(item['minLoc']) + ' to ' + str(item['maxLoc']) ] )
            # Register index
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), None ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(sastcachetype.engines_servers)
        return errorcount



    def inventory_customfields(self) :
        cachedata = self.cache(sastcachetype.custom_fields)
        SOBJECT = OBJ_CUSTOM_FIELDS
        SSTATUS = SOK
        ginfo = None
        inuse = 0
        errorcount = 0
        inventory_name = 'custom fields'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                # Is it used by projects ?
                projusing = list( filter( lambda el: item['name'] in el['customFieldsNames'], self.cache(sastcachetype.projectsfull) ) )
                # Sanity check
                if len(projusing) > 0 :
                    inuse += 1
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], len(projusing), None ] )
            # Register index
            if inuse > 0 :
                ginfo = str(inuse) + ' in use'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_smtpsettings(self) :
        cachedata = self.cache(sastcachetype.smtp_settings)
        SOBJECT = OBJ_SMTP_SETTINGS
        SSTATUS = SOK
        errorcount = 0
        inventory_name = 'smtp settings'
        ginfo = None
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Have we projects sending emails ?
            if len(cachedata) > 0 :
                projusing = list( filter( lambda el: el['emailNotifications'] > 0, self.cache(sastcachetype.projectsfull) ) )
            else :
                projusing = []
            # Register inventory
            for item in cachedata :
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, None, item['name'], len(projusing), None ] )
            # Register index
            if len(cachedata) > 0 and len(projusing) > 0 :
                ginfo = 'in use, not supported'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(sastcachetype.smtp_settings)
        return errorcount



    def inventory_issuetrackers(self) :
        cachedata = self.cache(sastcachetype.issue_trackers)
        SOBJECT = OBJ_ISSUE_TRACKER
        SSTATUS = SOK
        errorcount = 0
        inuse = 0
        ginfo = None
        inventory_name = 'issue trackers'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                itemstatus = SOK
                # Have projects using ?
                projusing = list( filter( lambda el: el['issueTrackingId'] == item['id'], self.cache(sastcachetype.projectsfull) ) )
                if len(projusing) > 0 :
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    inuse += 1
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], len(projusing), item['type'] + ': ' + item['url'] ] )
            # Register index
            if inuse > 0 :
                ginfo = str(inuse) + ' in use, not supported'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(sastcachetype.issue_trackers)
        return errorcount



    def inventory_prescanactions(self) :
        cachedata = list( filter( lambda el: el['type'] == 'SOURCE_CONTROL_COMMAND', self.cache(sastcachetype.scan_actions) ) )
        SOBJECT = OBJ_PRE_SCAN_ACTION
        SSTATUS = SOK
        errorcount = 0
        inuse = 0
        ginfo = None
        inventory_name = 'pre-scan actions'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                itemstatus = SOK
                # Have projects using ?
                projusing = list( filter( lambda el: el['preScanAction'] == item['id'], self.cache(sastcachetype.projectsfull) ) )
                if len(projusing) > 0 :
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    inuse += 1
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], len(projusing), item['data'] ] )
            # Register index
            if inuse > 0 :
                ginfo = str(inuse) + ' in use, not supported'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_postscanactions(self) :
        cachedata = list( filter( lambda el: el['type'] != 'SOURCE_CONTROL_COMMAND', self.cache(sastcachetype.scan_actions) ) )
        SOBJECT = OBJ_POST_SCAN_ACTION
        SSTATUS = SOK
        errorcount = 0
        inuse = 0
        ginfo = None
        inventory_name = 'post-scan actions'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                itemstatus = SOK
                # Have projects using ?
                projusing = list( filter( lambda el: el['postScanAction'] == item['id'], self.cache(sastcachetype.projectsfull) ) )
                if len(projusing) > 0 :
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    inuse += 1
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], len(projusing), item['data'] ] )
            # Register index
            if inuse > 0 :
                ginfo = str(inuse) + ' in use, not supported'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_resultstates(self) :
        cachedata = self.cache(sastcachetype.result_states)
        SOBJECT = OBJ_RESULT_STATES
        SSTATUS = SOK
        ginfo = None
        inuse = 0
        errorcount = 0
        inventory_name = 'result states'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                itemstatus = SOK
                sinfo = None
                # Is it custom ?
                if item['IsCustom'] :
                    sinfo = 'custom state'
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    inuse += 1
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['ResultID'], item['ResultName'], None, sinfo ] )
            # Register index
            if inuse > 0 :
                ginfo = str(inuse) + ' custom states exists, not supported'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_ac_samlsettings(self) :
        cachedata = self.cache(sastcachetype.ac_saml_settings)
        SOBJECT = OBJ_AC_SAML
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inventory_name = 'access-control saml settings'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            if len(cachedata) > 0 :
                SSTATUS = self.setstatus(SSTATUS, SWARNING )    
            # Register inventory
            for item in cachedata :
                # Get how many associated
                usercount = list( filter( lambda el: item['id'] == el['authenticationProviderId'], self.cache(sastcachetype.ac_users) ) )
                sinfo = 'issuer: ' + item['issuer'] + ' (' + str(len(usercount)) + ' users)'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], None, sinfo ] )
            # Register index
            if len(cachedata) > 0 :
                ginfo = 'Requires manual configuration'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata),  ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(sastcachetype.ac_saml_settings)
        return errorcount
    

    def inventory_ac_ldapsettings(self) :
        cachedata = self.cache(sastcachetype.ac_ldap_settings)
        SOBJECT = OBJ_AC_LDAP
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inventory_name = 'access-control ldap settings'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            if len(cachedata) > 0 :
                SSTATUS = self.setstatus(SSTATUS, SWARNING )    
            # Register inventory
            for item in cachedata :
                # Get how many associated
                usercount = list( filter( lambda el: item['id'] == el['authenticationProviderId'], self.cache(sastcachetype.ac_users) ) )
                sinfo = 'DN: ' + item['baseDn'] + ', Host: ' + item['host'] + ' (' + str(len(usercount)) + ' users)'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], None, sinfo ] )
            # Register index
            if len(cachedata) > 0 :
                ginfo = 'Requires manual configuration'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(sastcachetype.ac_ldap_settings)
        return errorcount



    def inventory_ac_domainsettings(self) :
        cachedata = self.cache(sastcachetype.ac_domain_settings)
        SOBJECT = OBJ_AC_DOMAIN
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inventory_name = 'access-control domain settings'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            if len(cachedata) > 0 :
                SSTATUS = self.setstatus(SSTATUS, SFATAL )    
            # Register inventory
            for item in cachedata :
                # Get how many associated
                usercount = len(list( filter( lambda el: item['id'] == el['authenticationProviderId'], self.cache(sastcachetype.ac_users) ) ))
                sinfo = 'FQDN: ' + item['fullyQualifiedName'] + ' (' + str(usercount) + ' users)'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], None, sinfo ] )
            # Register index
            if len(cachedata) > 0 :
                ginfo = 'Not supported'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(sastcachetype.ac_domain_settings)
        return errorcount



    def inventory_ac_teams(self) :
        cachedata = self.cache(sastcachetype.ac_teams)
        SOBJECT = OBJ_AC_TEAMS
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inventory_name = 'access-control teams'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                # Is it used by projects ?
                projusing = list( filter( lambda el: item['id'] == el['teamId'] > 0, self.cache(sastcachetype.projectsfull) ) )
                # Have users
                usercount = len(list( filter( lambda el: item['id'] in el['teamIds'], self.cache(sastcachetype.ac_users) ) ))
                sinfo = str(usercount) + ' user members'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['fullName'], len(projusing), sinfo ] )
            # Register index
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount
    


    def inventory_ac_roles(self) :
        cachedata = self.cache(sastcachetype.ac_roles)
        SOBJECT = OBJ_AC_ROLES
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        customroles = 0
        inventory_name = 'access-control roles'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                itemstatus = SOK
                # Have users
                usercount = len( list( filter( lambda el: item['id'] in el['roleIds'], self.cache(sastcachetype.ac_users) ) ) )
                if not item['isSystemRole'] :
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    sinfo = 'custom role ' + str(usercount) + ' users'
                    customroles += 1
                else :
                    sinfo = str(usercount) + ' users'
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], None, sinfo ] )
            # Register index
            if customroles > 0 :
                ginfo = str(customroles) + ' custom roles'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(sastcachetype.ac_roles)
        return errorcount
    


    def inventory_ac_users_application(self) :
        origproviders = self.conn.ac.get('/cxrestapi/auth/authenticationproviders')
        origprovider = next( filter( lambda el: el['providerType'] == 'Application', origproviders) )['id']
        cachedata = list( filter( lambda el: el['authenticationProviderId'] == origprovider, self.cache(sastcachetype.ac_users) ) )
        SOBJECT = OBJ_AC_USERS_APP
        SSTATUS = SOK
        ginfo = str(len(cachedata)) + ' users to manual creation'
        errorcount = 0
        inventory_name = 'access-control application users'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            if len(cachedata) > 0 :
                SSTATUS = SWARNING
            # Register counts only
            self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, None, ginfo, len(cachedata), None ] )
            # # Register inventory
            # for item in cachedata :
            #     self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['userName'], None, item['email'] ] )
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount
    


    def inventory_ac_users_external(self) :
        origproviders = self.conn.ac.get('/cxrestapi/auth/authenticationproviders')
        origprovider = next( filter( lambda el: el['providerType'] == 'Application', origproviders) )['id']
        cachedata = list( filter( lambda el: el['authenticationProviderId'] != origprovider, self.cache(sastcachetype.ac_users) ) )
        SOBJECT = OBJ_AC_USERS_OTHER
        SSTATUS = SOK
        ginfo = str(len(cachedata)) + ' users for IdP integration'
        errorcount = 0
        inventory_name = 'access-control external users'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            if len(cachedata) > 0 :
                SSTATUS = SWARNING
            # Register counts only
            self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, None, ginfo, len(cachedata), None ] )
            # # Register inventory
            # for item in cachedata :
            #     self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['userName'], None, item['email'] ] )
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_ac_users_email_domains(self) :
        cachedata = self.cache(sastcachetype.ac_users)
        emails    = []
        SOBJECT = OBJ_AC_USERS_EMAILS
        SSTATUS = SOK
        errorcount = 0
        inventory_name = 'access-control users email domains'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Read-it
            for item in cachedata :
                email = item['email']
                if email :
                    p = email.find('@')
                    if p >= 0 :
                        email = email[p:].strip()
                if email :
                    emails.append(email)
            emails = list( dict.fromkeys(emails) )
            if len(emails) > 0 :
                SSTATUS = SWARNING
            for item in emails :
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, None, item, None, None ] )
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(emails), None ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(emails)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(sastcachetype.ac_users)
        return errorcount



    def inventory_presets(self) :
        cachedata = self.cache(sastcachetype.presets)
        defaultpresets = sastdefaultpresets(self.conn.version)
        SOBJECT = OBJ_PRESETS
        SSTATUS = SOK
        ginfo = None
        customized = 0
        errorcount = 0
        inventory_name = 'presets'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                itemstatus = SOK
                sinfo = None
                presetid   = item['id']
                presetname = item['name']
                # Projects using
                projusing = list( filter( lambda el: el['presetId'] == item['id'], self.cache(sastcachetype.projectsfull) ) )
                # Is it a custom preset or a changed out-of-the-box preset
                defpreset = next( filter( lambda el: el['name'] == presetname, defaultpresets ), None )
                isoriginal = defpreset
                iscustomized = not isoriginal
                # Check if original was modified
                if isoriginal :
                    pqrys = set( item['queryIds'] )
                    dqrys = set( defpreset['queryIds'] )
                    iscustomized = (len(list(pqrys - dqrys)) > 0) or (len(list(dqrys - pqrys)) > 0) 
                else :
                    pqrys = set( item['queryIds'] )
                    dqrys = set( [] )
                # Check
                if not isoriginal :
                    self.__xpresets.append(item['id'])
                    customized += 1
                    sinfo = 'custom preset'
                    if len(projusing) > 0 :
                        itemstatus = self.setstatus(itemstatus, SFATAL )
                        SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    else :
                        itemstatus = self.setstatus(itemstatus, SWARNING )
                        SSTATUS = self.setstatus(SSTATUS, SWARNING )
                elif iscustomized :
                    self.__xpresets.append(item['id'])
                    customized += 1
                    sinfo = 'modified original preset'
                    if len(projusing) > 0 :
                        itemstatus = self.setstatus(itemstatus, SFATAL )
                        SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    else :
                        itemstatus = self.setstatus(itemstatus, SWARNING )
                        SSTATUS = self.setstatus(SSTATUS, SWARNING )

                # Write preset query data
                if not isoriginal :
                    preset_type = PTYPE_CUSTOM
                else :
                    preset_type = PTYPE_OOB
                # Queries that are on the preset but not the defaults
                if iscustomized :
                    queryids = list(pqrys - dqrys)

                # Ordered query ids
                presetqueries = list(pqrys)

                # Write preset query data (all queries)                        
                for queryid in presetqueries :
                    query = next( filter( lambda el: el['QueryId'] == queryid, self.cache(sastcachetype.queries_all) ), None )
                    if query :
                        q_status  = SOK
                        qq_status = QOK
                        if iscustomized and queryid in queryids :
                            q_status  = SWARNING
                            qq_status = QADDED
                        self.__psetqwriter.writerow( [ 
                            STATUS[q_status],
                            presetid,
                            presetname,
                            preset_type,
                            QSTATUS[qq_status],
                            queryid,
                            query['Name'],
                            query['LanguageName'],
                            query['PackageName'],
                            query['PackageTypeName']
                        ] )
                # Queries that are on the preset but not the defaults
                if iscustomized :
                    queryids = list(dqrys - pqrys)
                    q_status  = SWARNING
                    qq_status = QMISSING
                    for queryid in queryids :
                        query = next( filter( lambda el: el['QueryId'] == queryid, self.cache(sastcachetype.queries_all) ), None )
                        if query :
                            self.__psetqwriter.writerow( [ 
                                STATUS[q_status],
                                presetid,
                                presetname,
                                preset_type,
                                QSTATUS[qq_status],
                                queryid,
                                query['Name'],
                                query['LanguageName'],
                                query['PackageName'],                                
                                query['PackageTypeName']
                            ] )

                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], len(projusing), sinfo ] )
            if customized > 0 :
                ginfo = str(customized) + ' customized or new presets exist'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_custom_queries_corp(self) :
        cachedata = list(filter(lambda el: el['PackageType'] == 'Corporate', self.cache(sastcachetype.queries_custom)))
        SOBJECT = OBJ_QUERIES_CORP
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inventory_name = 'custom queries corporate level'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                lang = item['LanguageName']
                projusing = list( filter( lambda el: lang in el['sortedlanguages'], self.cache(sastcachetype.projectsfull)) )
                sinfo = item['LanguageName'] + ' (' + item['PackageFullName'] + ')'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['QueryId'], item['Name'], len(projusing), sinfo ] )
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount
    


    def inventory_custom_queries_team(self) :
        cachedata = list(filter(lambda el: el['PackageType'] == 'Team', self.cache(sastcachetype.queries_custom)))
        SOBJECT = OBJ_QUERIES_TEAM
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inuse = 0
        inventory_name = 'custom queries team level'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            if len(cachedata) > 0 :
                SSTATUS = SWARNING
            # Register inventory
            for item in cachedata :
                itemstatus = SWARNING
                team = item['OwningTeamName']
                lang = item['LanguageName']
                # Get projects using (direct or indirect)
                projusing = list( filter( lambda el: lang in el['sortedlanguages'] and (el['teamFullName'] == team or el['teamFullName'].startswith(team + '/') ), self.cache(sastcachetype.projectsfull)) )
                if len(projusing) > 0 :
                    inuse += 1
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    for proj in projusing :
                        self.__xteamqry.append(proj['id'])
                # Count hierachy (upwards)
                xteams = team[1:].split('/')
                teams = []
                steam = ''
                for xteam in xteams :
                    steam = steam + '/' + xteam
                    teams.append(steam)
                teams = teams[:-1]
                parentqueries = list( filter( lambda el: el['LanguageName'] == lang and el['Name'] == item['Name'] and el['OwningTeamName'] in teams, cachedata ) )
                sinfo = item['LanguageName'] + ', team: [' + str(item['OwningTeam']) + '] ' + item['OwningTeamName'] + ', ' + str(len(parentqueries)) + ' parents (' + item['PackageFullName'] + ')'
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['QueryId'], item['Name'], len(projusing), sinfo ] )
            if inuse > 0 :
                ginfo = str(inuse) + ' in use, directly or indirectly'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_custom_queries_proj(self) :
        cachedata = list(filter(lambda el: el['PackageType'] == 'Project', self.cache(sastcachetype.queries_custom)))
        SOBJECT = OBJ_QUERIES_PROJ
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inuse = 0
        inventory_name = 'custom queries project level'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                itemstatus = SOK
                proj = item['ProjectId']
                lang = item['LanguageName']
                # Get projects using (direct or indirect)
                projusing = list( filter( lambda el: lang in el['sortedlanguages'] and el['id'] == proj, self.cache(sastcachetype.projectsfull)) )
                if len(projusing) < 1 :
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    sinfo = item['LanguageName'] + ', project orphan (' + item['PackageFullName'] + ')'
                    inuse += 1
                    for proj in projusing :
                        self.__xprojqry.append(proj['id'])
                else :
                    sinfo = item['LanguageName'] + ', project: [' + str(proj) + '] ' + projusing[0]['name'] + ' (' + item['PackageFullName'] + ')'
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['QueryId'], item['Name'], len(projusing), sinfo ] )
            if inuse > 0 :
                ginfo = str(inuse) + ' orphan queries'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount
    


    def inventory_custom_categories(self) :
        cachedata = self.cache(sastcachetype.query_categories)
        defaultcategories = sastdefaultcategories(self.conn.version)
        SOBJECT = OBJ_QUERY_CATEGORIES
        SSTATUS = SOK
        ginfo = None
        inuse = 0
        errorcount = 0
        inventory_name = 'query categories'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                itemstatus = SOK
                sinfo = None
                default = next( filter( lambda el: el['CategoryName'] == item['CategoryName'] and el['CategoryType']['Name'] == item['CategoryType']['Name'], defaultcategories ), None )
                # Check if original was modified
                if not default :
                    inuse += 1
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    sinfo = 'Custom category found'
                    self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['Id'], item['CategoryName'], None, sinfo ] )
            if inuse > 0 :
                ginfo = str(inuse) + ' custom query categories exist'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, inuse, ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_projects(self) :
        cachedata = self.cache(sastcachetype.projectsfull)
        SOBJECT = OBJ_PROJECTS
        SSTATUS = SOK
        ginfo = None
        projcount = 0
        errorcount = 0
        inventory_name = 'projects'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )

        # Arrange helper caches
        self.__xpresets = list(set(self.__xpresets))
        self.__xcorpqry = list(set(self.__xcorpqry))
        self.__xteamqry = list(set(self.__xteamqry))
        self.__xprojqry = list(set(self.__xprojqry))

        # Origins detected
        origins = []
        def __incorigin( ostatus, oname ) :
            oc = next( filter(lambda el: el['info'] == oname, origins), None )
            if oc :
                oc['count'] = oc['count'] + 1
            else :
                origins.append( { 'status': ostatus, 'info': oname, 'count': 1 } )

        # Constraints detected
        constraints = []
        def __incconstraint( cstatus, cname ) :
            xc = next( filter(lambda el: el['info'] == cname, constraints), None )
            if xc :
                xc['count'] = xc['count'] + 1
            else :
                constraints.append( { 'status': cstatus, 'info': cname, 'count': 1 } )

        try :
            # Register inventory
            for item in cachedata :
                projcount += 1
                if (projcount % 100) == 0 :
                    cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(projcount) + ')', False )    
                sinfo = None
                itemstatus = SOK
                messages = []

                # Resolve duplicates project name
                pduplicated = None
                if next( filter( lambda el: el['id'] != item['id'] and el['name'].upper() == item['name'].upper(), cachedata), None ) :
                    pduplicated = True
                # Resolve origin
                porigin = item['lastScanOrigin']
                if porigin :
                    if porigin.upper().startswith('JENKINS') :
                        porigin = 'Jenkins'
                    elif porigin.upper().startswith('TFS') :
                        porigin = 'TFS'                        
                    elif porigin.upper().startswith('ADO') :
                        porigin = 'ADO'                        
                    elif porigin.upper().startswith('CXFLOW') :
                        porigin = 'CxFlow'                        
                    if porigin == 'CxFlow' :
                        __incorigin( SFATAL, porigin )
                    else :
                        __incorigin( SOK, porigin )

                # Check for problems
                # ------------------
                # duplicated project name
                if pduplicated :
                    messages.append('duplicated project name exists')
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    __incconstraint( SFATAL, 'duplicated project names' )
                # Project is private
                if not item['isPublic'] :
                    messages.append('project is private')
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    __incconstraint( SWARNING, 'private projects' )
                # Team is not resolved
                if not item['teamFullName'] :
                    messages.append('unresolved team name')
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    __incconstraint( SFATAL, 'unresolved team names' )
                # Preset is custom or customized
                if item['presetId'] in self.__xpresets :
                    messages.append('preset is custom or customized')
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    __incconstraint( SFATAL, 'custom or customized presets' )
                # Engine configuration is custom
                if next( filter( lambda el: el['id'] == item['engineConfigurationId'] and el['IsCustom'], self.cache(sastcachetype.engine_configs) ), None ) :
                    messages.append('engine configuration is custom')
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    __incconstraint( SFATAL, 'custom engine configurations' )
                # Email notifications
                if item['emailNotifications'] > 0 :
                    messages.append('e-mail notifications exist')
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    __incconstraint( SWARNING, 'projects with email notifications' )
                # Issue trackers
                if item['issueTrackingId'] :
                    messages.append('issue tracking sesstings exist')
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    __incconstraint( SWARNING, 'projects with issue tracking' )
                # Scheduled scans
                if item['ScheduledScans'] :
                    messages.append('scheduled scans are configured')
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    __incconstraint( SWARNING, 'projects with scheduled scans' )
                # Pre-scan action
                if item['preScanAction'] :
                    messages.append('pre-scan action is used')
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    __incconstraint( SFATAL, 'projects with pre-scan action' )
                # Post-scan action
                if item['postScanAction'] :
                    messages.append('post-scan action is used')
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    __incconstraint( SWARNING, 'projects with post-scan action' )
                # Check unsupported repository location
                if item['sourceSettingsType'] and item['sourceSettingsType'] not in ['local', 'custom', 'git'] :
                    messages.append('usupported repository type ' + item['sourceSettingsType'])
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    __incconstraint( SFATAL, 'projects with usupported repository type' )
                # Custom team queries
                if item['id'] in self.__xteamqry :
                    messages.append('project uses team level queries')
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    __incconstraint( SFATAL, 'projects using team level queries' )
                # Check a full scan was found
                if not item['lastScanId'] :
                    messages.append('full scan not found in the last 100 scans')
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    __incconstraint( SWARNING, 'projects without a full scan' )
                # Origin uses CxFlow
                if porigin == 'CxFlow' :
                    messages.append('scan done with CxFlow, usupported')
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    __incconstraint( SWARNING, 'projects using CxFlow' )
                # Triages custom states
                if item['triagesCustomState'] and item['triagesCustomState'] > 0 :
                    messages.append('triages with custom states exist')
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    __incconstraint( SFATAL, 'projects with triages with custom states' )
                # Max LOC passed
                if item['lastScanLOC'] and item['lastScanLOC'] > MAX_LOC :
                    messages.append('size above ' + MAX_LOC_TXT + ' line of code')
                    itemstatus = self.setstatus(itemstatus, SFATAL )
                    SSTATUS = self.setstatus(SSTATUS, SFATAL )
                    __incconstraint( SFATAL, 'projects with size above ' + MAX_LOC_TXT + ' line of code')

                # Join messages
                if len(messages) > 0 :
                    sinfo = '\n'.join(messages)

                if 'pathFilter' in item.keys() :
                    gfilters = item['pathFilter'] 
                else :
                    gfilters = globfilters.getfilters(item['excludedFiles'], item['excludedFolders'])

                # Write project data
                self.__projswriter.writerow( [
                        STATUS[itemstatus], 
                        item['id'], 
                        item['name'], 
                        pduplicated,
                        item['isPublic'],
                        item['createdDate'],
                        item['teamId'],
                        item['teamFullName'],
                        item['presetName'], 
                        item['engineConfigurationName'], 
                        len(item['customFieldsNames']) if len(item['customFieldsNames']) > 0 else None,
                        item['emailNotifications'] if item['emailNotifications'] > 0 else None,
                        True if item['issueTrackingId'] else None,
                        item['excludedFiles'],
                        item['excludedFolders'],
                        gfilters,
                        True if item['ScheduledScans'] else None,
                        True if item['preScanAction'] else None,
                        True if item['postScanAction'] else None,
                        True if item['id'] in self.__xcorpqry else None,
                        True if item['id'] in self.__xteamqry else None,
                        True if item['id'] in self.__xprojqry else None,
                        item['sourceSettingsType'],
                        porigin, 
                        item['lastScanOrigin'],
                        item['lastScanId'],
                        item['lastScanRequestedOn'],
                        item['lastScanLOC'],
                        ', '.join(item['languages']), 
                        item['TotalScans'],

                        item['TotalVulnerabilities'],
                        item['High'],
                        item['Medium'],
                        item['Low'],
                        item['Info'],

                        item['triagesCount'],
                        item['triagesCustomState'],
                        sinfo ] )
                # Write inventory data
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], 1, sinfo ] )
            # The final status
            if SSTATUS != SOK :
                ginfo = str(len(messages)) + ' problems detected'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Write origins to summary
            for origin in origins :
                self.__sumrywriter.writerow( [ STATUS[origin['status']], OBJ_ORIGINS, origin['count'], origin['info'] ] )
            # Write constraints to summary
            for constraint in constraints :
                self.__sumrywriter.writerow( [ STATUS[constraint['status']], OBJ_CONSTRAINTS, constraint['count'], constraint['info'] ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(projcount) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def execute(self) :
        errorcount = 0
        dtini = datetime.now()
        # Prepare the data files
        if not self.preparedatafiles() :
            exit(1)
        try :
            cxlogger.verbose( '============================================================' )
            cxlogger.verbose( 'Extracting full inventory from SAST' )
            cxlogger.verbose( 'Extraction started: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Processing sast inventory')
            # Config section
            errorcount += self.inventory_sastinstance() if errorcount == 0 else 0
            errorcount += self.inventory_engineconfigs() if errorcount == 0 else 0
            errorcount += self.inventory_engineservers() if errorcount == 0 else 0
            errorcount += self.inventory_customfields() if errorcount == 0 else 0
            errorcount += self.inventory_smtpsettings() if errorcount == 0 else 0
            errorcount += self.inventory_issuetrackers() if errorcount == 0 else 0
            errorcount += self.inventory_prescanactions() if errorcount == 0 else 0
            errorcount += self.inventory_postscanactions() if errorcount == 0 else 0
            errorcount += self.inventory_resultstates() if errorcount == 0 else 0
            # Access control section
            errorcount += self.inventory_ac_samlsettings() if errorcount == 0 else 0
            errorcount += self.inventory_ac_ldapsettings() if errorcount == 0 else 0
            errorcount += self.inventory_ac_domainsettings() if errorcount == 0 else 0
            errorcount += self.inventory_ac_teams() if errorcount == 0 else 0
            errorcount += self.inventory_ac_roles() if errorcount == 0 else 0
            errorcount += self.inventory_ac_users_application() if errorcount == 0 else 0
            errorcount += self.inventory_ac_users_external() if errorcount == 0 else 0
            errorcount += self.inventory_ac_users_email_domains() if errorcount == 0 else 0
            # Queries and presets section
            errorcount += self.inventory_presets() if errorcount == 0 else 0
            errorcount += self.inventory_custom_queries_corp() if errorcount == 0 else 0
            errorcount += self.inventory_custom_queries_team() if errorcount == 0 else 0
            errorcount += self.inventory_custom_queries_proj() if errorcount == 0 else 0
            errorcount += self.inventory_custom_categories() if errorcount == 0 else 0
            # Projects 
            errorcount += self.inventory_projects() if errorcount == 0 else 0
            # Done
            cxlogger.verbose( 'Sast inventory processed' )
        finally :
            dtend = datetime.now()
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Extraction ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            self.closedatafiles()
