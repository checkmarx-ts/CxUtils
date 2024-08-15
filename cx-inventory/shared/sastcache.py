""" 
========================================================================

SIMPLE CLASS TO CACHE SAST DATA
Supports v8.8 and up

joao.costa@checkmarx.com
PS-EMEA
22-06-2023

========================================================================
"""

import os
import json
import traceback
from enum import Enum
from copy import deepcopy
from datetime import datetime
from cxloghandler import cxlogger
from sastconn import sastconn
from cxparamfilters import paramfilters



class sastcachetype(Enum) :
    # Config section
    engine_configs      = 1                      
    engines_servers     = 2
    custom_fields       = 3
    smtp_settings       = 4
    issue_trackers      = 5
    scan_actions        = 6
    result_states       = 7
    #Access control setting
    ac_saml_settings    = 10
    ac_ldap_settings    = 11
    ac_domain_settings  = 12
    ac_teams            = 13
    ac_roles            = 14
    ac_users            = 15
    # Queries and presets
    presets             = 20
    presetssimple       = 21
    queries_custom      = 22
    queries_all         = 23
    query_categories    = 24
    # Projects
    projectsfull        = 30
    projectssimple      = 31
    projectstiny        = 32
    # Empty spots
    aux1                = 91
    aux2                = 92
    aux3                = 93
    aux4                = 94
    aux5                = 95
    aux6                = 96
    aux7                = 97
    aux8                = 98
    aux9                = 99



class sastcache(object) :

    def __init__(self) :
        self.__conn         = None
        self.__version      = None
        self.__customstate  = None
        self.__caches       = {}    


    def __init__(self, conn: sastconn ) :
        self.__conn         = conn
        self.__version      = None
        self.__customstate  = None
        self.__caches       = {}    


    @property
    def conn(self) :
        return self.__conn
    

    @property
    def caches(self) :
        return self.__caches
    

    def cache(self, cachetype: sastcachetype ) :
        if self.hascache(cachetype) :
            return self.__caches[cachetype]
        else :
            return None
        

    def cacheoneof(self, cachetypes: list[sastcachetype] ) :   
        for cachetype in cachetypes :
            if self.hascache(cachetype) :
                return self.__caches[cachetype]
        return None


    def uncache(self, cachetype: sastcachetype ) :
        if self.hascache(cachetype) :
            self.__caches[cachetype] = None
            self.__caches.pop(cachetype, None)


    def hascache(self, cachetype: sastcachetype ) :
        return cachetype in self.__caches.keys()
    

    def copycache( self, sourcetype: sastcachetype, desttype: sastcachetype ) :
        if not self.hascache(sourcetype) :
            raise Exception( 'Source type is void.')
        self.__caches[desttype] = deepcopy(self.__caches[sourcetype])


    def putcache( self, cachetype: sastcachetype, cachedata: None ) :
        if not cachetype in [sastcachetype.aux1, sastcachetype.aux2, sastcachetype.aux3, sastcachetype.aux4, sastcachetype.aux5, sastcachetype.aux6, sastcachetype.aux7, sastcachetype.aux8, sastcachetype.aux9] :
            raise Exception( 'Can only put data into aux types.')
        if not cachedata :
            self.uncache(cachetype) 
        else:
            self.__caches[cachetype] = cachedata


    # Helper: compute duration in time
    def duration(self, dtini, formated = False ) :
        dtend   = datetime.now()
        dtdiff  = dtend - dtini
        minutes = divmod(dtdiff.total_seconds(), 60) 
        hrs = 0
        min = minutes[0]
        sec = minutes[1]
        if min > 60 :
            hours = divmod(min, 60) 
            hrs = hours[0]
            min = hours[1]
        if formated :
            return '... (' + str(round(hrs)) + ':' + str(round(min)) + ':' + str(round(sec,4)) + ')'
        else :
            return str(round(hrs)) + ':' + str(round(min)) + ':' + str(round(sec,4))


    def __internalprocessproject( self, project, simple = False, tiny = False ) :
        # Get last valid scan details

        def __lastvalidscan(projectid, projectispublic) :
            # Use ODATA to control the volume
            lskip = 0
            lscan = None
            olist = self.conn.odata.get('/Cxwebinterface/odata/v1/Scans?$top=10&$skip=' + str(lskip) + '&$filter=ProjectId eq ' + str(projectid) + '&$expand=ScannedLanguages' )
            while (len(olist) > 0) and (not lscan) and (lskip < 100) :
                for xscan in olist :
                    if ((not projectispublic) or (projectispublic and xscan['IsPublic'])) and (xscan['ScannedLanguages']) and (len(xscan['ScannedLanguages']) > 0) :
                        lscan = xscan
                        return xscan
                lskip += 10
                olist = self.conn.odata.get('/Cxwebinterface/odata/v1/Scans?$top=10&$skip=' + str(lskip) + '&$filter=ProjectId eq ' + str(projectid) + '&$expand=ScannedLanguages' )
            return lscan
        
        data = {}
        # Identification
        data['id']                          = project['Id']
        data['name']                        = project['Name']
        data['teamId']                      = project['OwningTeamId']
        data['isPublic']                    = project['IsPublic']

        # In tiny mode, only go for a small set of data
        if tiny :
            data['teamFullName']                = None
            if data['teamId'] and data['teamId'] > 0 :
                data['teamFullName']            = project['OwningTeam']['FullName'].replace('\\','/')
            data['engineConfigurationId']       = project['EngineConfigurationId']
            data['presetId']                    = project['PresetId']
            data['presetName']                  = project['Preset']['Name']
            data['lastScanId']                  = project['LastScanId']
            return data
        
        if not simple :
            data['isConsistent']            = True
        data['description']                 = project['Description']
        data['createdDate']                 = project['CreatedDate']
        # Team
        data['teamName']                    = None
        data['teamFullName']                = None
        if data['teamId'] and data['teamId'] > 0 :
            team = next( filter(lambda el: el['id'] == data['teamId'], self.__caches[sastcachetype.ac_teams] ), None )
            if team :
                data['teamName']                = team['name']
                data['teamFullName']            = team['fullName']
        # Owner        
        data['ownerId']                     = project['OwnerId']
        # Preset
        data['presetId']                    = project['PresetId']
        data['presetName']                  = project['Preset']['Name']
        # Engine configuration
        data['engineConfigurationId']       = project['EngineConfigurationId']
        data['engineConfigurationName']     = [ el['name'] for el in self.__caches[sastcachetype.engine_configs] if el['id'] == data['engineConfigurationId'] ][0]
        if not simple :
            # Issue tracking
            if (project['IssueTrackingSettings']) :
                aux                             = json.loads(project['IssueTrackingSettings'])
                data['issueTrackingSettings']   = aux
                if (aux) and (aux['TrackingSystemID']) and (aux['TrackingSystemID'] > 0):
                    data['issueTrackingId']     = aux['TrackingSystemID']
                else :
                    data['issueTrackingId']     = None
            else :
                data['issueTrackingSettings']   = None
                data['issueTrackingId']         = None
        if 'PathFilter' in project.keys() :
            # Exclusions, 9.6.1 up
            pathfilter = project['PathFilter']
            # Workaround for case #00187800
            if not pathfilter :
                try :
                    auxdata = self.conn.sast.get('/cxrestapi/projects/' + str(data['id']) + '/sourcecode/pathfilter', None, '5.0' )
                    if auxdata :
                        pathfilter = auxdata['pathFilter']
                except :
                    pass
            data['pathFilter']                  = pathfilter
            data['excludedFiles']               = None
            data['excludedFolders']             = None
        else :
            # Exclusions, up to 9.5.5
            data['excludedFiles']               = project['ExcludedFiles']
            data['excludedFolders']             = project['ExcludedFolders']
        # Custom fields
        data['customFields']                = project['CustomFields']
        data['customFieldsNames']           = list( field['FieldName'] for field in project['CustomFields'] ) 
        # References
        data['SourcePath']                  = project['SourcePath']
        data['ScheduledScans']              = project['SchedulingExpression'] != None
        data['TotalScans']                  = project['TotalProjectScanCount']
        # Last scan check
        data['lastScanId']                  = project['LastScanId']
        data['languages']                   = []
        data['sortedlanguages']             = []
        # Resolve the last scan. If project is public, lastscan must be public as well.
        if (data['lastScanId']) :
            if ((not data['isPublic']) or (data['isPublic'] and project['LastScan']['IsPublic'])) and (project['LastScan']['ScannedLanguages']) and (len(project['LastScan']['ScannedLanguages']) > 0 ) :
                data['lastScanOrigin']          = project['LastScan']['Origin']
                data['lastScanSourceId']        = project['LastScan']['SourceId']
                data['lastScanIncremental']     = project['LastScan']['IsIncremental']
                data['lastScanLOC']             = project['LastScan']['LOC']
                data['lastScanInitiator']       = project['LastScan']['InitiatorName']
                data['lastScanIsPublic']        = project['LastScan']['IsPublic']
                data['lastScanProductVersion']  = project['LastScan']['ProductVersion']
                data['lastScanRequestedOn']     = project['LastScan']['ScanRequestedOn']
                aux2 = []
                for language in project['LastScan']['ScannedLanguages'] :
                    data['languages'].append( language['LanguageName'] )
                    aux2.append(language['LanguageName'])
                aux2.sort()
                data['sortedlanguages'] = aux2
                data['TotalVulnerabilities']    = project['LastScan']['TotalVulnerabilities']
                data['High']                    = project['LastScan']['High']
                data['Medium']                  = project['LastScan']['Medium']
                data['Low']                     = project['LastScan']['Low']
                data['Info']                    = project['LastScan']['Info']
            else:
                data['lastScanId'] = None
                lastscan = __lastvalidscan(project['Id'], data['isPublic'])
                if (lastscan) :
                    data['lastScanId'] = lastscan['Id']
                    data['lastScanOrigin']          = lastscan['Origin']
                    data['lastScanSourceId']        = lastscan['SourceId']
                    data['lastScanIncremental']     = lastscan['IsIncremental']
                    data['lastScanLOC']             = lastscan['LOC']
                    data['lastScanInitiator']       = lastscan['InitiatorName']
                    data['lastScanIsPublic']        = lastscan['IsPublic']
                    data['lastScanProductVersion']  = lastscan['ProductVersion']
                    data['lastScanRequestedOn']     = lastscan['ScanRequestedOn']
                    aux2 = []
                    for language in lastscan['ScannedLanguages'] :
                        data['languages'].append( language['LanguageName'] )
                        aux2.append(language['LanguageName'])
                    aux2.sort()
                    data['sortedlanguages'] = aux2                  
                    data['TotalVulnerabilities']    = lastscan['TotalVulnerabilities']
                    data['High']                    = lastscan['High']
                    data['Medium']                  = lastscan['Medium']
                    data['Low']                     = lastscan['Low']
                    data['Info']                    = lastscan['Info']
        if (not data['lastScanId']) :
            data['lastScanOrigin']          = ''
            data['lastScanSourceId']        = ''
            data['lastScanIncremental']     = False
            data['lastScanLOC']             = 0
            data['lastScanInitiator']       = ''
            data['lastScanIsPublic']        = True
            data['lastScanProductVersion']  = ''
            data['lastScanRequestedOn']     = ''
            data['TotalVulnerabilities']    = 0
            data['High']                    = 0
            data['Medium']                  = 0
            data['Low']                     = 0
            data['Info']                    = 0
            if not simple :
                data['triagesCount']            = None
                data['triagesCustomState']      = None
        elif not simple :
            data['triagesCount']            = None
            data['triagesCustomState']      = None
            # Get triages per state
            triagecount  = self.conn.odata.get('/Cxwebinterface/odata/v1/Scans(' + str(data['lastScanId']) + ')/Results/$count?$filter=StateId gt 0' )
            if triagecount :
                data['triagesCount'] = int(triagecount)
            if self.__customstate :
                triagescustom = self.conn.odata.get('/Cxwebinterface/odata/v1/Scans(' + str(data['lastScanId']) + ')/Results/$count?$filter=StateId ge ' + str(self.__customstate) )
                if triagescustom :
                    data['triagesCustomState'] = int(triagescustom)
        if not simple :
            # Some data not available if project is private
            data['sourceSettingsType']          = 'IDE Plugin' if not data['isPublic'] else None
            data['projectQueueSettings']        = None
            data['sourceSettingsLink']          = None
            data['preScanAction']               = None
            data['postScanAction']              = None
            data['emailNotifications']          = 0
            # Getit if it's public only
            if data['isPublic'] :
                # Queue settings available if version is v9.4 or higher
                if self.__version >= 9.4 :
                    try :
                        auxdata = self.conn.sast.get('/cxrestapi/projects/' + str(data['id']), None, '2.1' )
                        data['projectQueueSettings'] = auxdata['projectQueueSettings']
                    except :
                        pass
                # To get the source code location
                try :
                    auxdata = self.conn.sast.get('/cxrestapi/projects/' + str(data['id']) )
                    data['sourceSettingsType']      = auxdata['sourceSettingsLink']['type']
                    data['sourceSettingsLink']      = auxdata['sourceSettingsLink']['uri']
                    if (data['sourceSettingsType'] == 'custom') :
                        data['preScanAction']       = self.conn.sast.get('/cxrestapi' + data['sourceSettingsLink']['uri'] )['pullingCommandId']
                    # To get scan configurations                
                    auxdata = self.conn.sast.get('/cxrestapi/sast/scansettings/' + str(data['id']) )
                    # Postscan action
                    if auxdata['postScanAction'] :
                        data['postScanAction']      = auxdata['postScanAction']['id']
                    # Emails
                    data['emailNotifications']      = len(auxdata['emailNotifications']['failedScan']) + len(auxdata['emailNotifications']['beforeScan']) + len(auxdata['emailNotifications']['afterScan'])
                except :
                    data['isConsistent'] = False
                    pass
        return data


    def __internalteamsfilter( self, teamsfilter, allteams ) :
        tfilter = []
        pfilter = paramfilters.processfilter( teamsfilter, True )
        if pfilter :
            pnames  = []
            for team in allteams :
                if (team['id'] in pfilter) or (team['fullName'] in pfilter) :
                    pnames.append(team)
            for pname in pnames :
                team = next( filter( lambda el: el['fullName'] == pname['fullName'] or el['fullName'].startswith( pname['fullName'] + '/'), allteams ), None )
                if team :
                    tfilter.append(team['id'])
            tfilter = list(set(tfilter))
        if len(tfilter) > 0 :
            return tfilter
        else :
            return None


    def __internalcacheprojects( self, simple = False, tiny = False, projectsfilter = None, silent: bool = False, updatinglist: list = None ) :
        cache_name = 'sast projects'
        lcount = 0
        signal = '  - Caching '
        updating = False
        if projectsfilter and updatinglist and len(updatinglist) > 0:
            plist = updatinglist
            updating = True
            signal = '  - Updating cache '
        else :
            plist = []
        lskip = 0
        pfilter, pfilterlist = paramfilters.processodatafilter( projectsfilter, 'Id' )
        if pfilterlist :
            for projectid in projectsfilter :
                pfilter = '&$filter=Id eq ' + str(projectid)
                if tiny :
                    olist = self.conn.odata.get('/Cxwebinterface/odata/v1/Projects?$top=1&$skip=0&$select=Id,Name,IsPublic,OwningTeamId,EngineConfigurationId,PresetId,LastScanId' + pfilter + '&$expand=Preset,OwningTeam' )
                else :
                    olist = self.conn.odata.get('/Cxwebinterface/odata/v1/Projects?$top=1&$skip=0' + pfilter + '&$expand=Preset,CustomFields,OwningTeam,LastScan($expand=ScannedLanguages)')    
                lcount += len(olist)
                for proj in olist :
                    # Projects with missing teams are orphan
                    if proj['OwningTeamId'] and proj['OwningTeamId'] > 0 :
                        pdata = self.__internalprocessproject( proj, simple, tiny )
                        if updating :
                            existing = next( filter( lambda el: el['id'] == pdata['id'], plist), None )
                            if existing :
                                existing = deepcopy(pdata)
                            else :
                                plist.append( pdata )    
                        else :
                            plist.append( pdata )
                if not silent and lcount % 100 == 0 :
                    cxlogger.verbose( signal + cache_name + ' (' + str(lcount) + ')', False)
        else :
            if tiny :
                olist = self.conn.odata.get('/Cxwebinterface/odata/v1/Projects?$top=100&$skip=' + str(lskip) + '&$select=Id,Name,IsPublic,OwningTeamId,EngineConfigurationId,PresetId,LastScanId' + pfilter + '&$expand=Preset,OwningTeam' )
            else :
                olist = self.conn.odata.get('/Cxwebinterface/odata/v1/Projects?$top=100&$skip=' + str(lskip) + pfilter + '&$expand=Preset,CustomFields,OwningTeam,LastScan($expand=ScannedLanguages)')
            while len(olist) > 0 :
                lcount += len(olist)
                if not silent :
                    cxlogger.verbose( signal + cache_name + ' (' + str(lcount) + ')', False)
                for proj in olist :
                    # Projects with missing teams are orphan
                    if proj['OwningTeamId'] and proj['OwningTeamId'] > 0 :
                        pdata = self.__internalprocessproject( proj, simple, tiny )
                        if updating :
                            existing = next( filter( lambda el: el['id'] == pdata['id'], plist), None )
                            if existing :
                                existing = deepcopy(pdata)
                            else :
                                plist.append( pdata )    
                        else :
                            plist.append( pdata )
                lskip += 100
                if tiny :
                    olist = self.conn.odata.get('/Cxwebinterface/odata/v1/Projects?$top=100&$skip=' + str(lskip) + '&$select=Id,Name,IsPublic,OwningTeamId,EngineConfigurationId,PresetId,LastScanId' + pfilter + '&$expand=Preset,OwningTeam' )
                else :
                    olist = self.conn.odata.get('/Cxwebinterface/odata/v1/Projects?$top=100&$skip=' + str(lskip) + pfilter +'&$expand=Preset,CustomFields,OwningTeam,LastScan($expand=ScannedLanguages)')    
        return plist


    def createcache( self, cachetype: sastcachetype, contentfilter = None, silent: bool = False, forupdate: bool = False ) :
        errorcount = 0
        lcount = 0
        dtini = datetime.now()
        try :
            signal          = '  - Caching '
            signalsuccess   = '  - Cached '
            signalerrors    = '  - Caching '
            if forupdate :
                signal          = '  - Updating cache '
                signalsuccess   = '  - Cache updated '
                signalerrors    = '  - Cache updating '
            # Filtered indicator
            filtered = ''
            if contentfilter :
                filtered = ' filtered'
            # Avoid reacreationg the cache if it already exists
            if self.hascache(cachetype) :
                return 0
            # Resolve version
            if not self.__version :
                ver = self.conn.version['version']
                pos = ver.find('.', ver.find('.') + 1)
                if pos > 0 :
                    ver = ver[0:pos]
                try:
                    self.__version = float(ver)
                except:
                    self.__version = 9.0
            # Configurations section
            if cachetype == sastcachetype.engine_configs :
                cache_name = 'sast engine configurations'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                gconfigs = self.conn.sast.get('/cxrestapi/sast/engineconfigurations') 
                for config in gconfigs :
                    config['IsCustom'] = config['name'] not in ['Default Configuration', 'Japanese (Shift-JIS)', 'Korean', 'Multi-language Scan', 'Improved Scan Flow']
                self.__caches[sastcachetype.engine_configs] = gconfigs
                lcount = len(self.__caches[sastcachetype.engine_configs])
            elif cachetype == sastcachetype.engines_servers :
                cache_name = 'sast engines servers'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[sastcachetype.engines_servers] = self.conn.sast.get('/cxrestapi/sast/engineServers') 
                lcount = len(self.__caches[sastcachetype.engines_servers])
            elif cachetype == sastcachetype.custom_fields :
                cache_name = 'sast custom fields'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[sastcachetype.custom_fields] = self.conn.sast.get('/cxrestapi/customfields') 
                lcount = len(self.__caches[sastcachetype.custom_fields])
            elif cachetype == sastcachetype.smtp_settings :
                cache_name = 'sast smtp settings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                smtpdata = []
                gsettings = self.conn.sast.get('/cxrestapi/configurationsextended/systemsettings')
                ssettings = list( filter( lambda el: el['key'] == 'SMTPHost', gsettings ) )[0]['value']
                if ssettings :
                    smtpdata.append( { "name": ssettings } )
                self.__caches[sastcachetype.smtp_settings] = smtpdata
                lcount = len(self.__caches[sastcachetype.smtp_settings])
            elif cachetype == sastcachetype.issue_trackers :
                cache_name = 'sast issue trackers'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[sastcachetype.issue_trackers] = self.conn.sast.get('/cxrestapi/issuetrackingsystems') 
                lcount = len(self.__caches[sastcachetype.issue_trackers])
            elif cachetype == sastcachetype.scan_actions :
                cache_name = 'sast scan actions'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[sastcachetype.scan_actions] = self.conn.sast.get('/cxrestapi/customtasks') 
                lcount = len(self.__caches[sastcachetype.scan_actions])
            elif cachetype == sastcachetype.result_states :
                cache_name = 'sast result states'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                gstates = self.conn.soap.getresultstates()
                for state in gstates :
                    state['IsCustom'] = state['ResultName'] not in ['To Verify', 'Not Exploitable', 'Confirmed', 'Urgent', 'Proposed Not Exploitable']
                    if state['IsCustom'] and not self.__customstate :
                        self.__customstate = state['ResultID']
                self.__caches[sastcachetype.result_states] = gstates
                lcount = len(self.__caches[sastcachetype.result_states])
            # Access control section
            elif cachetype == sastcachetype.ac_saml_settings :
                cache_name = 'sast saml settings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                samldata = []
                samllist = self.conn.ac.get('/cxrestapi/auth/samlidentityproviders')
                samlproviders = self.conn.ac.get('/cxrestapi/auth/authenticationproviders')
                samlactive = list( filter( lambda el: el['active'], samllist ) )
                for saml in samlactive :    
                    provid  = next(filter(lambda el: el['providerId'] == saml['id'] and el['providerType'] == 'SAML', samlproviders), None)['id']
                    samldata.append( { "id": provid, "name": saml['name'], "issuer": saml['issuer'] })
                self.__caches[sastcachetype.ac_saml_settings] = samldata
                lcount = len(self.__caches[sastcachetype.ac_saml_settings])
            elif cachetype == sastcachetype.ac_ldap_settings :
                cache_name = 'sast ldap settings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                ldapdata = []
                ldaplist = self.conn.ac.get('/cxrestapi/auth/ldapservers')
                ldapproviders = self.conn.ac.get('/cxrestapi/auth/authenticationproviders')
                ldapactive = list( filter( lambda el: el['active'], ldaplist ) )
                for ldap in ldapactive :    
                    provid  = next(filter(lambda el: el['providerId'] == ldap['id'] and el['providerType'] == 'LDAP', ldapproviders), None)['id']
                    ldapdata.append( { "id": provid, "name": ldap['name'], "host": ldap['host'], "baseDn": ldap['baseDn'] })
                self.__caches[sastcachetype.ac_ldap_settings] = ldapdata
                lcount = len(self.__caches[sastcachetype.ac_ldap_settings])
            elif cachetype == sastcachetype.ac_domain_settings :
                cache_name = 'sast domain settings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                domaindata = []    
                domainlist = self.conn.ac.get('/cxrestapi/auth/windowsdomains')
                domainproviders = self.conn.ac.get('/cxrestapi/auth/authenticationproviders')
                for domain in domainlist :    
                    provid  = next(filter(lambda el: el['providerId'] == domain['id'] and el['providerType'] == 'Domain', domainproviders), None)['id']            
                    domaindata.append( { "id": provid, "name": domain['name'], "fullyQualifiedName": domain['fullyQualifiedName'] })
                self.__caches[sastcachetype.ac_domain_settings] = domaindata
                lcount = len(self.__caches[sastcachetype.ac_domain_settings])
            elif cachetype == sastcachetype.ac_teams :
                cache_name = 'sast teams'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                teamsaux = []
                teams = self.conn.ac.get('/cxrestapi/auth/teams')
                teamsfilter = self.__internalteamsfilter( contentfilter, teams )
                if teamsfilter :
                    for team in teams :
                        if (team['id'] in teamsfilter) :
                            teamsaux.append(team)
                    self.__caches[sastcachetype.ac_teams] = teamsaux
                else :
                    self.__caches[sastcachetype.ac_teams] = teams
                lcount = len(self.__caches[sastcachetype.ac_teams])
            elif cachetype == sastcachetype.ac_roles :
                cache_name = 'sast roles'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                rolesfilter = paramfilters.processfilter( contentfilter, True )
                rolesaux = []
                roles = self.conn.ac.get('/cxrestapi/auth/roles')
                if rolesfilter :
                    for role in roles :
                        if (role['id'] in rolesfilter) or (role['name'] in rolesfilter) :
                            rolesaux.append(role)
                    self.__caches[sastcachetype.ac_roles] = rolesaux
                else :
                    self.__caches[sastcachetype.ac_roles] = roles
                lcount = len(self.__caches[sastcachetype.ac_roles])
            elif cachetype == sastcachetype.ac_users :
                cache_name = 'sast users'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[sastcachetype.ac_users] = self.conn.ac.get('/cxrestapi/auth/users')
                lcount = len(self.__caches[sastcachetype.ac_users])
            # Queries and presets section
            elif cachetype == sastcachetype.presets :
                cache_name = 'sast presets'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                auxlist = self.conn.sast.get('/cxrestapi/sast/presets')
                for pset in auxlist :
                    pset['queryIds'] = self.conn.sast.get('/cxrestapi/sast/presets/' + str(pset['id']))['queryIds']
                self.__caches[sastcachetype.presets] = auxlist
                lcount = len(self.__caches[sastcachetype.presets])
            elif cachetype == sastcachetype.presetssimple :
                cache_name = 'sast presets'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[sastcachetype.presetssimple] = self.conn.sast.get('/cxrestapi/sast/presets')
                lcount = len(self.__caches[sastcachetype.presetssimple])
            elif cachetype == sastcachetype.queries_custom :
                # Teams cache is also required, because they are referenced
                if not self.cache(sastcachetype.ac_teams) :
                    self.createcache( sastcachetype.ac_teams, silent )
                cache_name = 'sast custom queries'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[sastcachetype.queries_custom] = self.conn.soap.getcustomqueries()
                # Resolve the query team path
                for query in self.__caches[sastcachetype.queries_custom] :
                    if query['OwningTeam'] :
                        team = next(filter( lambda el: el['id'] == query['OwningTeam'], self.__caches[sastcachetype.ac_teams]), None)
                        if team :
                            query['OwningTeamName'] = team['fullName']
                        else :
                            query['OwningTeamName'] = ''
                    else :
                        query['OwningTeamName'] = None                
                lcount = len(self.__caches[sastcachetype.queries_custom])
            elif cachetype == sastcachetype.queries_all :
                cache_name = 'sast all queries'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[sastcachetype.queries_all] = self.conn.soap.getallqueries()
                lcount = len(self.__caches[sastcachetype.queries_all])
            elif cachetype == sastcachetype.query_categories :
                cache_name = 'sast query categories'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[sastcachetype.query_categories] = self.conn.soap.getquerycategories()
                lcount = len(self.__caches[sastcachetype.query_categories])
            # Projects section
            elif cachetype == sastcachetype.projectsfull :
                # Teams, engineconfigs, and result states, caches are also required, because they are referenced
                if not self.cache(sastcachetype.ac_teams) :
                    self.createcache( sastcachetype.ac_teams, silent )
                if not self.cache(sastcachetype.engine_configs) :
                    self.createcache( sastcachetype.engine_configs, silent )
                cache_name = 'sast projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( False, False, contentfilter, silent )
                self.__caches[sastcachetype.projectsfull] = plist
                lcount = len(plist)
            elif cachetype == sastcachetype.projectssimple :
                # Teams, engineconfigs, and result states, caches are also required, because they are referenced
                if not self.cache(sastcachetype.ac_teams) :
                    self.createcache( sastcachetype.ac_teams, silent )
                if not self.cache(sastcachetype.engine_configs) :
                    self.createcache( sastcachetype.engine_configs, silent )
                cache_name = 'sast projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( True, False, contentfilter, silent )
                self.__caches[sastcachetype.projectssimple] = plist
                lcount = len(plist)
            elif cachetype == sastcachetype.projectstiny :
                cache_name = 'sast projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( True, True, contentfilter, silent )
                self.__caches[sastcachetype.projectstiny] = plist
                lcount = len(plist)
            # Done
            if not silent :    
                cxlogger.verbose( signalsuccess + cache_name + filtered + ' (' + str(lcount) + ') ' + self.duration(dtini, True), False)
        except Exception as e:
            errorcount += 1
            if not silent :
                cxlogger.verbose( signalerrors + cache_name + filtered + ' (' + str(lcount) + ') failed with "' + str(e) + '"', True, False, True, e )
        return errorcount
    

    def updatecache( self, cachetype: sastcachetype, contentfilter = None, silent: bool = False ) :
        errorcount = 0
        lcount = 0
        dtini = datetime.now()

        if not ( cachetype in [sastcachetype.projectsfull, sastcachetype.projectssimple, sastcachetype.projectstiny] ) :
            self.uncache( cachetype )
            return self.createcache( cachetype, contentfilter, silent, True )

        try :
            signal = '  - Updating cache '
            # Filtered indicator
            filtered = ''
            if contentfilter :
                filtered = ' filtered'
            if cachetype == sastcachetype.projectsfull :
                cache_name = 'sast projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( False, False, contentfilter, silent, self.cache(sastcachetype.projectsfull) )
                self.__caches[sastcachetype.projectsfull] = plist
                lcount = len(plist)
            elif cachetype == sastcachetype.projectssimple :
                cache_name = 'sast projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( True, False, contentfilter, silent, self.cache(sastcachetype.projectssimple) )
                self.__caches[sastcachetype.projectssimple] = plist
                lcount = len(plist)
            elif cachetype == sastcachetype.projectstiny :
                cache_name = 'sast projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( True, True, contentfilter, silent, self.cache(sastcachetype.projectstiny) )
                self.__caches[sastcachetype.projectstiny] = plist
                lcount = len(plist)
            # Done
            if not silent :    
                cxlogger.verbose( '  - Cache updated ' + cache_name + filtered + ' (' + str(lcount) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            if not silent :
                cxlogger.verbose( '  - Cache updating ' + cache_name + filtered + ' (' + str(lcount) + ') failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def createallcaches(self, projectsfilter = None, teamsfilter = None ) :
        errorcount = 0
        # Config section
        errorcount += self.createcache( sastcachetype.engine_configs ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.engines_servers ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.custom_fields ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.smtp_settings ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.issue_trackers ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.scan_actions ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.result_states ) if errorcount == 0 else 0
        # Access control section
        errorcount += self.createcache( sastcachetype.ac_saml_settings ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.ac_ldap_settings ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.ac_domain_settings ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.ac_teams, teamsfilter ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.ac_roles ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.ac_users ) if errorcount == 0 else 0
        # Queries and presets section
        errorcount += self.createcache( sastcachetype.presets ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.queries_all ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.queries_custom ) if errorcount == 0 else 0
        errorcount += self.createcache( sastcachetype.query_categories ) if errorcount == 0 else 0
        # Projects section
        errorcount += self.createcache( sastcachetype.projectsfull, projectsfilter ) if errorcount == 0 else 0
        return errorcount
