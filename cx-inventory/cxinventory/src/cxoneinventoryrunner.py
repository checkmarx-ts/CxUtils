""" 
========================================================================

CXONE DATA EXTRACTOR INVENTORY PRODUCER

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
from sastdefaultpresets import sastdefaultpresets



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
OUT_SUMMARY             = 'cxone_inventorysummary.csv'
OUT_INVENTORY           = 'cxone_inventory.csv'
OUT_PROJECTS            = 'cxone_inventoryprojects.csv'
OUT_PRESETQUERIES       = 'cxone_inventorypresets.csv'
OUT_QUERYMAPPER         = 'cxone_inventoryqueriesmapsast.csv'

# CSV file headers
CSV_SUMMARY             = ['STATUS', 'OBJ-TYPE', 'OBJ-COUNT', 'INFO']
CSV_INVENTORY           = ['STATUS', 'OBJ-TYPE', 'OBJ-ID', 'OBJ-NAME', 'PROJ-USING', 'INFO']
CSV_PROJECTS            = ['STATUS', 'ID', 'NAME', 'CREATED-ON', 'UPDATED-ON', 'LANGUAGE-MODE', 'SAST-PRESET', 'BRANCH', 'REPO', 
                           'SCM_REPONAME', 'SCM-REPOID', 'SCM-BRANCHES', 'CRITICALITY',
                           'APPLICATIONS', 'GROUPS', 'TAGS', 'SAST-FILTER', 'KICS-PLATFORMS', 'KICS-FILTER', 'SCA-EXPLOITABLE-PATH', 'SCA-FILTER',
                           'LANGUAGES', 'SCANNERS', 
                           'SAST-LASTSCAN-ID', 'SAST-LASTSCAN-CREATED', 'SAST-LASTSCAN-ORIGIN', 'SAST-LASTSCAN-RESULTS', 'SAST-LASTSCAN-TRIAGES', 
                           'SCA-LASTSCAN-ID', 'SCA-LASTSCAN-CREATED', 'SCA-LASTSCAN-ORIGIN', 'SCA-LASTSCAN-RESULTS', 'SCA-LASTSCAN-TRIAGES', 
                           'KICS-LASTSCAN-ID', 'KICS-LASTSCAN-CREATED', 'KICS-LASTSCAN-ORIGIN', 'KICS-LASTSCAN-RESULTS', 'KICS-LASTSCAN-TRIAGES', 
                           'APISEC-LASTSCAN-ID', 'APISEC-LASTSCAN-CREATED', 'APISEC-LASTSCAN-ORIGIN', 'APISEC-LASTSCAN-RESULTS', 'APISEC-LASTSCAN-TRIAGES']
CSV_PRESETQUERIES       = ['STATUS','PRESET-ID','PRESET-NAME','PRESET-TYPE','QUERY-STATUS','QUERY-ID','QUERY-NAME','QUERY-LANGUAGE','QUERY-GROUP','QUERY-LEVEL','SAST-QUERY-ID']
CSV_QUERYMAPPER         = ['QUERY-ID','QUERY-NAME','SAST-ID']


# OBJECT TYPE
OBJ_TENANT_DEFAULTS     = 'TENANT-DEFAULTS'
OBJ_ENGINE_CONFIG       = 'ENGINE-CONFIG'
OBJ_AC_SAML             = 'AC-SAML-SETTINGS'
OBJ_AC_OIDC             = 'AC-OIDC-SETTINGS'
OBJ_AC_LDAP             = 'AC-LDAP-SETTINGS'
OBJ_AC_TEAMS            = 'AC-TEAMS'
OBJ_AC_ROLES            = 'AC-ROLES'
OBJ_AC_USERS_APP        = 'AC-USERS-APPLICATION'
OBJ_AC_USERS_OTHER      = 'AC-USERS-EXTERNAL'
OBJ_AC_USERS_EMAILS     = 'AC-USERS-EMAIL-DOMAINS'
OBJ_PRESETS             = 'PRESETS'
OBJ_QUERIES_CORP        = 'CUSTOM-QUERIES-CORP'
OBJ_QUERIES_PROJ        = 'CUSTOM-QUERIES-PROJ'
OBJ_APPLICATIONS        = 'APPLICATIONS'
OBJ_PROJECTS            = 'PROJECTS'
OBJ_ORIGINS             = 'SCAN-ORIGINS'



class cxoneinventory(baserunner) :

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
        # Tenant defaults
        self.__defpreset    = None
        self.__defconfig    = None
        # Well known file for csv containing preset queries
        self.__psetqhandler = None
        self.__psetqwriter  = None
        # Well known file for csv containing cxone to sast query maps
        self.__qrmaphandler = None
        self.__qrmapwriter  = None
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
        # Tenant defaults
        self.__defpreset    = None
        self.__defconfig    = None
        # Well known file for csv containing preset queries
        self.__psetqhandler = None
        self.__psetqwriter  = None
        # Well known file for csv containing cxone to sast query maps
        self.__qrmaphandler = None
        self.__qrmapwriter  = None
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
            # Well known file for csv containing presets
            filename = self.datapath() + os.sep + OUT_PRESETQUERIES
            if os.path.exists(filename) :
                os.remove(filename)
            self.__psetqhandler = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
            self.__psetqwriter  = csv.writer(self.__psetqhandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            self.__psetqwriter.writerow(CSV_PRESETQUERIES)
            # Well known file for csv containing cxone to sast query maps
            filename = self.datapath() + os.sep + OUT_QUERYMAPPER
            if os.path.exists(filename) :
                os.remove(filename)
            self.__qrmaphandler = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
            self.__qrmapwriter  = csv.writer(self.__qrmaphandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            self.__qrmapwriter.writerow(CSV_QUERYMAPPER)
            # Done
            return True
        except Exception as e:
            cxlogger.verbose( 'Unable to create output files with "' + str(e) + '"', True, False, True, e )    
            self.closedatafiles()
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
        if (self.__qrmaphandler):
            self.__qrmaphandler.close()



    def inventory_tenantdefaults(self) :
        cachedata = self.cache(cxonecachetype.tenant_defaults)
        SOBJECT = OBJ_TENANT_DEFAULTS
        SSTATUS = SOK
        errorcount = 0
        inventory_name = 'tenant defaults'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['Name'], item['Value'], None, 'Category: ' + item['Category'] + 'AllowOverride: ' + str(item['AllowOverride']) ] )
                if item['Name'] == 'presetName' :
                    self.__defpreset = item['Value']
                if item['Name'] == 'languageMode' :
                    self.__defconfig = item['Value']
            # Register index
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), None ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_engineconfigs(self) :
        cachedata = self.cache(cxonecachetype.engine_configs)
        SOBJECT = OBJ_ENGINE_CONFIG
        SSTATUS = SOK
        errorcount = 0
        inventory_name = 'engine configurations'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                # Is it used by projects ?
                languagemode = item
                projusing = list( filter( lambda el: el['sastLanguageMode'] == languagemode or (el['sastLanguageMode'] == None and languagemode == self.__defconfig), self.cache(cxonecachetype.projectsfull) ) )
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item, item, len(projusing), None ] )
            # Register index
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), None ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_ac_samlsettings(self) :
        cachedata = self.cache(cxonecachetype.ac_saml_settings)
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
                usercount = list( filter( lambda el: next( filter( lambda fi: fi['identityProvider'] == item['name'], el['federatedIdentities']), None ), self.cache(cxonecachetype.ac_users) ) )
                sinfo = 'issuer: ' + item['issuer'] + ' (' + str(len(usercount)) + ' users)'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], None, sinfo ] )
            # Register index
            if len(cachedata) > 0 :
                ginfo = 'Involves manual configuration'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata),  ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(cxonecachetype.ac_saml_settings)
        return errorcount



    def inventory_ac_oidcsettings(self) :
        cachedata = self.cache(cxonecachetype.ac_oidc_settings)
        SOBJECT = OBJ_AC_OIDC
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inventory_name = 'access-control oidc settings'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            if len(cachedata) > 0 :
                SSTATUS = self.setstatus(SSTATUS, SWARNING )    
            # Register inventory
            for item in cachedata :
                # Get how many associated
                usercount = list( filter( lambda el: next( filter( lambda fi: fi['identityProvider'] == item['name'], el['federatedIdentities']), None ), self.cache(cxonecachetype.ac_users) ) )
                sinfo = 'issuer: ' + item['issuer'] + ' (' + str(len(usercount)) + ' users)'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], None, sinfo ] )
            # Register index
            if len(cachedata) > 0 :
                ginfo = 'Involves manual configuration'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata),  ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(cxonecachetype.ac_oidc_settings)
        return errorcount



    def inventory_ac_ldapsettings(self) :
        cachedata = self.cache(cxonecachetype.ac_ldap_settings)
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
                usercount = list( filter( lambda el: next( filter( lambda fi: fi['identityProvider'] == item['name'], el['federatedIdentities']), None ), self.cache(cxonecachetype.ac_users) ) )
                sinfo = 'vendor: ' + item['vendor'] + ', issuer: ' + item['issuer'] + ' (' + str(len(usercount)) + ' users)'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], None, sinfo ] )
            # Register index
            if len(cachedata) > 0 :
                ginfo = 'Involves manual configuration'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata),  ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(cxonecachetype.ac_ldap_settings)
        return errorcount



    def inventory_ac_groups(self) :
        cachedata = self.cache(cxonecachetype.ac_groups)
        SOBJECT = OBJ_AC_TEAMS
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inventory_name = 'access-control groups'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                # Is it used by projects ?
                projusing = list( filter( lambda el: item['id'] in el['groups'], self.cache(cxonecachetype.projectsfull) ) )
                # Have users
                # usercount = len(list( filter( lambda el: item['id'] in el['teamIds'], self.cache(cxonecachetype.ac_users) ) ))
                # sinfo = str(usercount) + ' user members'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['path'], len(projusing), None ] )
            # Register index
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_ac_roles(self) :
        cachedata = self.cache(cxonecachetype.ac_roles)
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
                sinfo = None
                itemstatus = SOK
                # # Have users
                # usercount = len( list( filter( lambda el: item['id'] in el['roleIds'], self.cache(cxonecachetype.ac_users) ) ) )
                if not item['isSystemRole'] :
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    sinfo = 'custom role'
                    customroles += 1
                # else :
                #     sinfo = str(usercount) + ' users'
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
        self.caches.uncache(cxonecachetype.ac_roles)
        return errorcount



    def inventory_ac_users_application(self) :
        cachedata = list( filter( lambda el: len(el['federatedIdentities']) == 0, self.cache(cxonecachetype.ac_users) ) )
        SOBJECT = OBJ_AC_USERS_APP
        SSTATUS = SOK
        errorcount = 0
        inventory_name = 'access-control application users'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register counts only
            self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, None, 'application users', len(cachedata), None ] )
            # # Register inventory
            # for item in cachedata :
            #     self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['username'], None, item['email'] ] )
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), None ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_ac_users_external(self) :
        cachedata = list( filter( lambda el: len(el['federatedIdentities']) > 0, self.cache(cxonecachetype.ac_users) ) )
        SOBJECT = OBJ_AC_USERS_OTHER
        SSTATUS = SOK
        errorcount = 0
        inventory_name = 'access-control external users'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register counts only
            self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, None, 'external IdP users', len(cachedata), None ] )
            # # Register inventory
            # for item in cachedata :
            #     self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['username'], None, item['email'] ] )
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), None ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_ac_users_email_domains(self) :
        cachedata = self.cache(cxonecachetype.ac_users)
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
        self.caches.uncache(cxonecachetype.ac_users)
        return errorcount



    def inventory_presets(self) :
        cachedata = self.cache(cxonecachetype.presets )
        defaultpresets = sastdefaultpresets(None)
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
                presetid    = item['id']
                presetname  = item['name']
                # Projects using
                projusing = list( filter( lambda el: el['sastPresetName'] == presetname or (el['sastPresetName'] == None and presetname == self.__defpreset), self.cache(cxonecachetype.projectsfull) ) )
                # Is it a custom preset
                defpreset = next( filter( lambda el: el['name'] == item['name'], defaultpresets ), None )
                isoriginal = defpreset
                # Check
                if not isoriginal :
                    customized += 1
                    sinfo = 'custom preset'
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )                    

                # Write preset data
                if not isoriginal :
                    preset_type = PTYPE_CUSTOM
                else :
                    preset_type = PTYPE_OOB

                # Ordered query ids
                presetqueries = list(set(item['queryIds']))

                for queryid in presetqueries :
                    query = next( filter( lambda el: el['Id'] == queryid, self.cache(cxonecachetype.queries_all) ), None )
                    if query :
                        sastqueryid = None
                        sastquery = next( filter( lambda el: el['astId'] == queryid, self.cache(cxonecachetype.queries_sast_maps) ), None )
                        if sastquery :
                            sastqueryid = sastquery['sastId']                                         
                        q_status  = SOK
                        qq_status = QOK
                        self.__psetqwriter.writerow( [ 
                            STATUS[q_status],
                            presetid,
                            presetname,
                            preset_type,
                            QSTATUS[qq_status],
                            queryid,
                            query['name'],
                            query['lang'],
                            query['group'],
                            query['level'],
                            sastqueryid
                        ] )

                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], len(projusing), sinfo ] )
            if customized > 0 :
                ginfo = str(customized) + ' new presets exist'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_sast_queries_map(self) :
        cachedata = self.cache(cxonecachetype.queries_sast_maps)
        errorcount = 0
        inventory_name = 'query sast mappings'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                queryid = item['astId']
                queryname = None
                query = next( filter( lambda el: el['Id'] == queryid, self.cache(cxonecachetype.queries_all) ), None )
                if query :
                    queryname = query['lang'] + ': ' + query['name']
                self.__qrmapwriter.writerow( [ queryid, queryname, item['sastId']  ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_custom_queries_corp(self) :
        cachedata = list(filter(lambda el: el['level'] == 'Corp', self.cache(cxonecachetype.queries_custom)))
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
                lang = item['lang']
                projusing = list( filter( lambda el: el['languages'] and lang in el['languages'], self.cache(cxonecachetype.projectsfull)) )
                sinfo = item['lang'] + ' (' + item['group'] + ')'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['Id'], item['name'], len(projusing), sinfo ] )
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_custom_queries_proj(self) :
        cachedata = list(filter(lambda el: el['level'] == 'Project', self.cache(cxonecachetype.queries_custom)))
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
                proj = item['projectid']
                lang = item['lang']
                projusing = list( filter( lambda el: el['languages'] and lang in el['languages'] and el['id'] == proj, self.cache(cxonecachetype.projectsfull)) )
                if len(projusing) < 1 :
                    itemstatus = self.setstatus(itemstatus, SWARNING )
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    sinfo = item['lang'] + ', project orphan (' + item['group'] + ')'
                    inuse += 1
                else :
                    sinfo = item['lang'] + ', project: [' + str(proj) + '] ' + projusing[0]['name'] + ' (' + item['group'] + ')'
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['Id'], item['name'], len(projusing), sinfo ] )
            if inuse > 0 :
                ginfo = str(inuse) + ' orphan queries'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_applications(self) :
        cachedata = self.cache(cxonecachetype.applications)
        SOBJECT = OBJ_APPLICATIONS
        SSTATUS = SOK
        errorcount = 0
        inventory_name = 'applications'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            # Register inventory
            for item in cachedata :
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], len(item['projectIds']), None ] )
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), None ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def inventory_projects(self) :
        cachedata = self.cache(cxonecachetype.projectsfull)
        SOBJECT = OBJ_PROJECTS
        SSTATUS = SOK
        ginfo = None
        projcount = 0
        errorcount = 0
        inventory_name = 'projects'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )

        origins = []
        def __incorigin( oname ) :
            if oname :
                oc = next( filter(lambda el: el['name'] == oname, origins), None )
                if oc :
                    oc['count'] = oc['count'] + 1
                else :
                    origins.append( { 'name': oname, 'count': 1 } )

        try :
            # Register inventory
            for item in cachedata :
                projcount += 1
                if (projcount % 100) == 0 :
                    cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(projcount) + ')', False )    
                sinfo = None
                itemstatus = SOK

                if not item['isConsistent'] :
                    SSTATUS = self.setstatus(SSTATUS, SWARNING )
                    itemstatus = self.setstatus(SSTATUS, SWARNING )
                    sinfo = 'project with inconsistent data'
                    ginfo = 'inconsistent projects'

                __incorigin( item['sastLastScan']['sourceorigin'] )
                __incorigin( item['scaLastScan']['sourceorigin'] )
                __incorigin( item['kicsLastScan']['sourceorigin'] )
                __incorigin( item['apisecLastScan']['sourceorigin'] )

                # Resolve language mode
                languagemode = item['sastLanguageMode']
                if not languagemode and self.__defconfig :
                    languagemode = self.__defconfig
                # Resolve preset
                presetname = item['sastPresetName']
                if not presetname and self.__defpreset :
                    presetname = self.__defpreset
                # Resolve groups
                groupname = None
                if item['groups'] and len(item['groups']) > 0 :
                    group = next( filter( lambda el: el['id'] == item['groups'][0], self.cache(cxonecachetype.ac_groups) ), None)
                    if group :
                        groupname = group['path']
                        if len(item['groups']) > 1 :
                            groupname = groupname + ' (+' + str(len(item['groups'])-1) + ')'
                # Resolve applications
                applicationname = None
                if item['applicationIds'] and len(item['applicationIds']) > 0 :
                    app = next( filter( lambda el: el['id'] == item['applicationIds'][0], self.cache(cxonecachetype.applications) ), None)
                    if app :
                        applicationname = app['name']
                        if len(item['applicationIds']) > 1 :
                            applicationname = applicationname + ' (+' + str(len(item['applicationIds'])-1) + ')'
                # Resolve tags
                tagname = None
                alltags = item['tags']
                tagkeys = list(alltags.keys())
                if tagkeys and len(tagkeys) > 0 :                
                    tagname = tagkeys[0]
                    tagvalue = alltags[tagkeys[0]]
                    if tagvalue :
                        tagname = tagname + ': ' + tagvalue
                    if len(tagkeys) > 1 :
                        tagname = tagname + ' (+' + str(len(tagkeys)-1) + ')'

                # Resolve sast counters
                sastresults     = 0
                sastresults     += item['sastLastScan']['high'] if item['sastLastScan']['high'] else 0
                sastresults     += item['sastLastScan']['medium'] if item['sastLastScan']['medium'] else 0
                sastresults     += item['sastLastScan']['low'] if item['sastLastScan']['low'] else 0
                sastresults     += item['sastLastScan']['info'] if item['sastLastScan']['info'] else 0
                sastresults     += item['sastLastScan']['otherseverity'] if item['sastLastScan']['otherseverity'] else 0
                sasttriages     = 0
                sasttriages     += item['sastLastScan']['notexploitable'] if item['sastLastScan']['notexploitable'] else 0
                sasttriages     += item['sastLastScan']['confirmed'] if item['sastLastScan']['confirmed'] else 0
                sasttriages     += item['sastLastScan']['urgent'] if item['sastLastScan']['urgent'] else 0
                sasttriages     += item['sastLastScan']['proposednotexploitable'] if item['sastLastScan']['proposednotexploitable'] else 0
                sasttriages     += item['sastLastScan']['otherstate'] if item['sastLastScan']['otherstate'] else 0
                # Resolve sca counters
                scaresults      = 0
                scaresults      += item['scaLastScan']['high'] if item['scaLastScan']['high'] else 0
                scaresults      += item['scaLastScan']['medium'] if item['scaLastScan']['medium'] else 0
                scaresults      += item['scaLastScan']['low'] if item['scaLastScan']['low'] else 0
                scaresults      += item['scaLastScan']['info'] if item['scaLastScan']['info'] else 0
                scaresults      += item['scaLastScan']['otherseverity'] if item['scaLastScan']['otherseverity'] else 0
                scatriages      = 0
                scatriages      += item['scaLastScan']['notexploitable'] if item['scaLastScan']['notexploitable'] else 0
                scatriages      += item['scaLastScan']['confirmed'] if item['scaLastScan']['confirmed'] else 0
                scatriages      += item['scaLastScan']['urgent'] if item['scaLastScan']['urgent'] else 0
                scatriages      += item['scaLastScan']['proposednotexploitable'] if item['scaLastScan']['proposednotexploitable'] else 0
                scatriages      += item['scaLastScan']['otherstate'] if item['scaLastScan']['otherstate'] else 0
                # Resolve kics counters
                kicsresults     = 0
                kicsresults     += item['kicsLastScan']['high'] if item['kicsLastScan']['high'] else 0
                kicsresults     += item['kicsLastScan']['medium'] if item['kicsLastScan']['medium'] else 0
                kicsresults     += item['kicsLastScan']['low'] if item['kicsLastScan']['low'] else 0
                kicsresults     += item['kicsLastScan']['info'] if item['kicsLastScan']['info'] else 0
                kicsresults     += item['kicsLastScan']['otherseverity'] if item['kicsLastScan']['otherseverity'] else 0
                kicstriages     = 0
                kicstriages     += item['kicsLastScan']['notexploitable'] if item['kicsLastScan']['notexploitable'] else 0
                kicstriages     += item['kicsLastScan']['confirmed'] if item['kicsLastScan']['confirmed'] else 0
                kicstriages     += item['kicsLastScan']['urgent'] if item['kicsLastScan']['urgent'] else 0
                kicstriages     += item['kicsLastScan']['proposednotexploitable'] if item['kicsLastScan']['proposednotexploitable'] else 0
                kicstriages     += item['kicsLastScan']['otherstate'] if item['kicsLastScan']['otherstate'] else 0
                # Resolve apisec counters
                apisecresults   = 0
                apisecresults   += item['apisecLastScan']['high'] if item['apisecLastScan']['high'] else 0
                apisecresults   += item['apisecLastScan']['medium'] if item['apisecLastScan']['medium'] else 0
                apisecresults   += item['apisecLastScan']['low'] if item['apisecLastScan']['low'] else 0
                apisecresults   += item['apisecLastScan']['info'] if item['apisecLastScan']['info'] else 0
                apisecresults   += item['apisecLastScan']['otherseverity'] if item['apisecLastScan']['otherseverity'] else 0
                apicestriages   = 0
                apicestriages   += item['apisecLastScan']['notexploitable'] if item['apisecLastScan']['notexploitable'] else 0
                apicestriages   += item['apisecLastScan']['confirmed'] if item['apisecLastScan']['confirmed'] else 0
                apicestriages   += item['apisecLastScan']['urgent'] if item['apisecLastScan']['urgent'] else 0
                apicestriages   += item['apisecLastScan']['proposednotexploitable'] if item['apisecLastScan']['proposednotexploitable'] else 0
                apicestriages   += item['apisecLastScan']['otherstate'] if item['apisecLastScan']['otherstate'] else 0

                # Write project data
                self.__projswriter.writerow( [
                    STATUS[itemstatus],                     
                    item['id'],
                    item['name'],
                    item['createdAt'],
                    item['updatedAt'],
                    languagemode,
                    presetname, 
                    item['mainBranch'],
                    item['repoUrl'],
                    item['scmRepoId'],
                    item['repoId'],
                    item['scmBranches'],
                    item['criticality'],  
                    applicationname,
                    groupname,
                    tagname,
                    item['sastFilter'],
                    item['kicsPlatforms'],
                    item['kicsFilter'],
                    item['scaExploitablePath'],
                    item['scaFilter'],
                    ','.join(item['languages']) if len(item['languages']) > 0 else None,
                    ','.join(item['scanners']) if len(item['scanners']) > 0 else None,
                    # Sast scan
                    item['sastLastScan']['scanid'] if item['sastLastScan']['scanid'] else None,
                    item['sastLastScan']['created'] if item['sastLastScan']['created'] else None,
                    item['sastLastScan']['sourceorigin'] if item['sastLastScan']['sourceorigin'] else None,
                    sastresults if sastresults > 0 else None,
                    sasttriages if sasttriages > 0 else None,
                    # Sca scan
                    item['scaLastScan']['scanid'] if item['scaLastScan']['scanid'] else None,
                    item['scaLastScan']['created'] if item['scaLastScan']['created'] else None,
                    item['scaLastScan']['sourceorigin'] if item['scaLastScan']['sourceorigin'] else None,
                    scaresults if scaresults > 0 else None,
                    scatriages if scatriages > 0 else None,
                    # Kics scan
                    item['kicsLastScan']['scanid'] if item['kicsLastScan']['scanid'] else None,
                    item['kicsLastScan']['created'] if item['kicsLastScan']['created'] else None,
                    item['kicsLastScan']['sourceorigin'] if item['kicsLastScan']['sourceorigin'] else None,
                    kicsresults if kicsresults > 0 else None,
                    kicstriages if kicstriages > 0 else None,
                    # Api security counters
                    item['apisecLastScan']['scanid'] if item['apisecLastScan']['scanid'] else None,
                    item['apisecLastScan']['created'] if item['apisecLastScan']['created'] else None,
                    item['apisecLastScan']['sourceorigin'] if item['apisecLastScan']['sourceorigin'] else None,
                    apisecresults if apisecresults > 0 else None,
                    apicestriages if apicestriages > 0 else None
                ] )

                # Write inventory data
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], 1, sinfo ] )
            # The final status
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )

            # Write origins to summary
            for origin in origins :
                self.__sumrywriter.writerow( [ STATUS[SOK], OBJ_ORIGINS, origin['count'], origin['name'] ] )
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
            cxlogger.verbose( 'Extracting full inventory from CXONE' )
            cxlogger.verbose( 'Extraction started: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Processing cxone inventory')
            # Config section
            errorcount += self.inventory_tenantdefaults() if errorcount == 0 else 0
            errorcount += self.inventory_engineconfigs() if errorcount == 0 else 0
            # Access control section
            errorcount += self.inventory_ac_samlsettings() if errorcount == 0 else 0
            errorcount += self.inventory_ac_oidcsettings() if errorcount == 0 else 0
            errorcount += self.inventory_ac_ldapsettings() if errorcount == 0 else 0
            errorcount += self.inventory_ac_groups() if errorcount == 0 else 0
            errorcount += self.inventory_ac_roles() if errorcount == 0 else 0
            errorcount += self.inventory_ac_users_application() if errorcount == 0 else 0
            errorcount += self.inventory_ac_users_external() if errorcount == 0 else 0
            errorcount += self.inventory_ac_users_email_domains() if errorcount == 0 else 0
            # Queries and presets section
            errorcount += self.inventory_presets() if errorcount == 0 else 0
            errorcount += self.inventory_sast_queries_map() if errorcount == 0 else 0
            errorcount += self.inventory_custom_queries_corp() if errorcount == 0 else 0
            errorcount += self.inventory_custom_queries_proj() if errorcount == 0 else 0
            # Projects and applications
            errorcount += self.inventory_applications() if errorcount == 0 else 0
            errorcount += self.inventory_projects() if errorcount == 0 else 0
            # Done
            cxlogger.verbose( 'Cxone inventory processed' )
        finally :
            dtend = datetime.now()
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Extraction ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            self.closedatafiles()
