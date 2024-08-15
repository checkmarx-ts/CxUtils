""" 
========================================================================

SCA DATA EXTRACTOR INVENTORY PRODUCER

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


# Sanity status
SOK                     = 0
SWARNING                = 1
SFATAL                  = 2
STATUS                  = ['OK', 'WARNING', 'DANGER']

# CSV output files
OUT_SUMMARY             = 'sca_inventorysummary.csv'
OUT_INVENTORY           = 'sca_inventory.csv'
OUT_PROJECTS            = 'sca_inventoryprojects.csv'

# CSV file headers
CSV_SUMMARY             = ['STATUS', 'OBJ-TYPE', 'OBJ-COUNT', 'INFO']
CSV_INVENTORY           = ['STATUS', 'OBJ-TYPE', 'OBJ-ID', 'OBJ-NAME', 'PROJ-USING', 'INFO']
CSV_PROJECTS            = ['STATUS', 'ID', 'NAME', 'CREATED-ON', 'UPDATED-ON', 'EXPLOITABLE-PATH', 'LAST-SAST-SCAN', 'BRANCH', 'IS-MANAGED',
                           'LAST-FULL-SCAN', 'LATEST-SCAN', 'RISK-REPORT-ID', 'RISK-REPORT-CREATED', 'RISK-REPORT-UPDATED',
                           'DIRECT-PACKAGES', 'TOTAL-PACKAGES', 'OUTDATED-PACKAGES', 'HIGH', 'MEDIUM', 'LOW', 'IGNORED',
                           'LAST-SCANNED', 'SEVERITY', 'IS-VIOLATED', 'IS-PRIVATE', 'TEAMS', 'TAGS' ]


# OBJECT TYPE
OBJ_AC_SAML             = 'AC-SAML-SETTINGS'
OBJ_AC_MASTER_AC        = 'AC-MASTER-ACCESS'
OBJ_AC_TEAMS            = 'AC-TEAMS'
OBJ_AC_ROLES            = 'AC-ROLES'
OBJ_AC_USERS_APP        = 'AC-USERS-APPLICATION'
OBJ_AC_USERS_OTHER      = 'AC-USERS-EXTERNAL'
OBJ_AC_USERS_EMAILS     = 'AC-USERS-EMAIL-DOMAINS'
OBJ_PROJECTS            = 'PROJECTS'



class scainventory(baserunner) :

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
            return True
        except Exception as e:
            cxlogger.verbose( 'Unable to create output files with "' + str(e) + '"', True, False, True, e )    
            self.__closedatafiles()
            return False



    def closedatafiles(self) :
        if (self.__sumryhandler):
            self.__sumryhandler.close()
        if (self.__datahandler):
            self.__datahandler.close()
        if (self.__projshandler):
            self.__projshandler.close()



    def inventory_ac_samlsettings(self) :
        cachedata = self.cache(scacachetype.ac_saml_settings)
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
                usercount = list( filter( lambda el: item['id'] == el['authenticationProviderId'], self.cache(scacachetype.ac_users) ) )
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
        self.caches.uncache(scacachetype.ac_saml_settings)
        return errorcount



    def inventory_ac_mastersettings(self) :
        cachedata = self.cache(scacachetype.ac_master_settings)
        SOBJECT = OBJ_AC_MASTER_AC
        SSTATUS = SOK
        ginfo = None
        errorcount = 0
        inventory_name = 'access-control master settings'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            if len(cachedata) > 0 :
                SSTATUS = self.setstatus(SSTATUS, SFATAL )    
            # Register inventory
            for item in cachedata :
                # Get how many associated
                usercount = list( filter( lambda el: item['id'] == el['authenticationProviderId'], self.cache(scacachetype.ac_users) ) )
                sinfo = 'issuer: ' + item['issuer'] + ' (' + str(len(usercount)) + ' users)'
                self.__datawriter.writerow( [STATUS[SSTATUS], SOBJECT, item['id'], item['name'], None, sinfo ] )
            # Register index
            if len(cachedata) > 0 :
                ginfo = 'Not supported'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata),  ginfo ] )
            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        # Cache not needed anymore
        self.caches.uncache(scacachetype.ac_master_settings)
        return errorcount



    def inventory_ac_teams(self) :
        cachedata = self.cache(scacachetype.ac_teams)
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

                # next( filter( lambda tl: item['id'] == tl['id'], el['assignedTeams'] ), None )
                # projusing = list( filter( lambda el: len(el['assignedTeams']) > 0 and item['id'] in el['teamIds'] > 0, self.cache(scacachetype.projects) ) )

                projusing = list( filter( lambda el: len(el['assignedTeams']) > 0 and next( filter( lambda tl: item['id'] == tl['id'], el['assignedTeams'] ), None ), self.cache(scacachetype.projects) ) )

                # Have users
                usercount = len(list( filter( lambda el: item['id'] in el['teamIds'], self.cache(scacachetype.ac_users) ) ))
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
        cachedata = self.cache(scacachetype.ac_roles)
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
                usercount = len( list( filter( lambda el: item['id'] in el['roleIds'], self.cache(scacachetype.ac_users) ) ) )
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
        self.caches.uncache(scacachetype.ac_roles)
        return errorcount
    


    def inventory_ac_users_application(self) :
        origproviders = self.conn.ac.get('/authenticationproviders')
        origprovider = next( filter( lambda el: el['providerType'] == 'Application', origproviders) )['id']
        cachedata = list( filter( lambda el: el['authenticationProviderId'] == origprovider, self.cache(scacachetype.ac_users) ) )
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
        origproviders = self.conn.ac.get('/authenticationproviders')
        origprovider = next( filter( lambda el: el['providerType'] == 'Application', origproviders) )['id']
        cachedata = list( filter( lambda el: el['authenticationProviderId'] != origprovider, self.cache(scacachetype.ac_users) ) )
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
        cachedata = self.cache(scacachetype.ac_users)
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
        self.caches.uncache(scacachetype.ac_users)
        return errorcount



    def inventory_projects(self) :
        cachedata = self.cache(scacachetype.projects)
        SOBJECT = OBJ_PROJECTS
        SSTATUS = SOK
        ginfo = None
        projcount = 0
        errorcount = 0
        inuse = 0
        inventory_name = 'projects'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )

        try :
            # Register inventory
            for item in cachedata :
                projcount += 1
                if (projcount % 100) == 0 :
                    cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(projcount) + ')', False)    
                sinfo = None
                itemstatus = SOK
                messages = []

                # Join messages
                if len(messages) > 0 :
                    sinfo = '\n'.join(messages)                

                pteams = None
                if len(item['assignedTeams']) > 0 :
                    pteams = item['assignedTeams'][0]['teamPath']
                    if len(item['assignedTeams']) > 1 :
                        pteams = pteams + ' (+' + str(len(item['assignedTeams']) - 1) + ')'

                ptags = None
                if len(item['tags']) > 0 :
                    if item['tags'][0]['key'] :
                        ptags = item['tags'][0]['key']
                    if item['tags'][0]['value'] :
                        if ptags :
                            ptags = ptags + ': ' + item['tags'][0]['value']
                        else :
                            ptags = item['tags'][0]['value']
                    if len(item['tags']) > 1 :
                        ptags = ptags + ' (+' + str(len(item['tags']) - 1) + ')'

                    len(item['assignedTeams']) if len(item['assignedTeams']) > 0 else None,
                    len(item['tags']) if len(item['tags']) > 0 else None,

                # Write project data
                self.__projswriter.writerow( [
                    STATUS[itemstatus],                         
                    item['id'],
                    item['name'],
                    item['createdOn'],
                    item['lastUpdate'],
                    item['enableExploitablePath'],
                    item['lastSastScanTime'] if item['lastSastScanTime'] else None,
                    item['branch'],
                    item['isManaged'],
                    item['lastSuccessfulScanId'],
                    item['latestScanId'],
                    # item['canonicalName'],
                    # item['tenantId'],
                    item['riskReportSummary'],
                    item['riskReportCreatedOn'],
                    item['riskReportLastUpdate'],
                    item['directPackages'] if item['directPackages'] else None,
                    item['totalPackages'] if item['totalPackages'] else None,
                    item['totalOutdatedPackages'] if item['totalOutdatedPackages'] else None,
                    item['highVulnerabilityCount'] if item['highVulnerabilityCount'] else None,
                    item['mediumVulnerabilityCount'] if item['mediumVulnerabilityCount'] else None,
                    item['lowVulnerabilityCount'] if item['lowVulnerabilityCount'] else None,
                    item['ignoredVulnerabilityCount'] if item['ignoredVulnerabilityCount'] else None,
                    item['lastScanned'] if item['lastScanned'] else None,
                    item['severity'],
                    item['isViolated'],
                    item['isPrivatePackage'],
                    pteams,
                    ptags
                ] )
                # Write inventory data
                self.__datawriter.writerow( [STATUS[itemstatus], SOBJECT, item['id'], item['name'], 1, sinfo ] )

            # The final status
            if SSTATUS != SOK :
                ginfo = str(len(messages)) + ' problems detected'
            self.__sumrywriter.writerow( [STATUS[SSTATUS], SOBJECT, len(cachedata), ginfo ] )
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
            cxlogger.verbose( 'Extracting full inventory from SCA' )
            cxlogger.verbose( 'Extraction started: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Processing sca inventory')
            # Access control section
            errorcount += self.inventory_ac_samlsettings() if errorcount == 0 else 0
            errorcount += self.inventory_ac_mastersettings() if errorcount == 0 else 0
            errorcount += self.inventory_ac_teams() if errorcount == 0 else 0
            errorcount += self.inventory_ac_roles() if errorcount == 0 else 0
            errorcount += self.inventory_ac_users_application() if errorcount == 0 else 0
            errorcount += self.inventory_ac_users_external() if errorcount == 0 else 0
            errorcount += self.inventory_ac_users_email_domains() if errorcount == 0 else 0
            # Projects and triages
            errorcount += self.inventory_projects() if errorcount == 0 else 0
            # Done
            cxlogger.verbose( 'Sca inventory processed' )
        finally :
            dtend = datetime.now()
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Extraction ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            self.closedatafiles()
