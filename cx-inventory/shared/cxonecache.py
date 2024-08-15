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
import uuid
import traceback
from urllib import parse
from enum import Enum
from copy import deepcopy
from datetime import datetime
from cxloghandler import cxlogger
from cxoneconn import cxoneconn
from cxparamfilters import paramfilters



class cxonecachetype(Enum) :
    # Config section
    tenant_defaults     = 1                     
    engine_configs      = 2     
    # Access control setting
    ac_saml_settings    = 10
    ac_oidc_settings    = 11
    ac_ldap_settings    = 12
    ac_groups           = 13
    ac_roles            = 14
    ac_users            = 15
    # Queries and presets
    presets             = 20
    presetssimple       = 21
    queries_custom      = 22
    queries_all         = 23
    queries_sast_maps   = 24
    # Projects and application
    applications        = 30
    projectsfull        = 31
    projectssimple      = 32
    projectstiny        = 33
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



class cxonecache(object) :

    def __init__(self) :
        self.__conn         = None
        self.__tenant_id    = None
        self.__ast_app      = None
        self.__cb_app       = None
        self.__caches       = {} 
        self.__prjkeys      = None 
        self.__appkeys      = None


    def __init__(self, conn: cxoneconn ) :
        self.__conn         = conn
        self.__tenant_id    = None
        self.__ast_app      = None
        self.__cb_app       = None
        self.__caches       = {}
        self.__prjkeys      = None
        self.__appkeys      = None


    @property
    def __tenantid(self) :
        if not self.__tenant_id :
            tenantinfo = self.conn.keycloak.get('')
            self.__tenant_id = tenantinfo['id']
        return self.__tenant_id


    @property
    def conn(self) :
        return self.__conn
    

    @property
    def caches(self) :
        return self.__caches


    def cache(self, cachetype: cxonecachetype ) :
        if self.hascache(cachetype) :
            return self.__caches[cachetype]
        else :
            return None


    def cacheoneof(self, cachetypes: list[cxonecachetype] ) :   
        for cachetype in cachetypes :
            if self.hascache(cachetype) :
                return self.__caches[cachetype]
        return None


    def uncache(self, cachetype: cxonecachetype ) :
        if self.hascache(cachetype) :
            self.__caches[cachetype] = None
            self.__caches.pop(cachetype, None)


    def hascache(self, cachetype: cxonecachetype ) :
        return cachetype in self.__caches.keys()
    

    def copycache( self, sourcetype: cxonecachetype, desttype: cxonecachetype ) :
        if not self.hascache(sourcetype) :
            raise Exception( 'Source type is void.')
        self.__caches[desttype] = deepcopy(self.__caches[sourcetype])


    def putcache( self, cachetype: cxonecachetype, cachedata: None ) :
        if not cachetype in [cxonecachetype.aux1, cxonecachetype.aux2, cxonecachetype.aux3, cxonecachetype.aux4, cxonecachetype.aux5, cxonecachetype.aux6, cxonecachetype.aux7, cxonecachetype.aux8, cxonecachetype.aux9] :
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


    def __internal_get_keycloak_clientids( self ) :
        # Resolve keycloak client ids for "ast-app" and "cb-app", relevant for roles and premissions
        if not self.__ast_app or not self.__cb_app :
            clients = self.conn.keycloak.get('/clients')
            if not self.__ast_app :
                client = next( filter( lambda el: el['clientId'] == 'ast-app', clients ), None )
                if client :
                    self.__ast_app = client['id']
            if not self.__cb_app :
                client = next( filter( lambda el: el['clientId'] == 'cb-app', clients ), None )
                if client :
                    self.__cb_app = client['id']


    def __internal_flatten_groups( self, groups, parentid, groupslist ) :
        for group in groups :
            data = {}
            data['id'] = group['id']
            data['name'] = group['name']
            data['path'] = group['path']
            data['parentid'] = parentid
            groupslist.append(data)
            subgroups = group['subGroups']
            if len(subgroups) > 0 :
                groupslist = self.__internal_flatten_groups( subgroups, group['id'], groupslist )
        return groupslist


    def __internal_processusers( self, users ) :
        userslist = []
        for user in users :
            userid = user['id']
            if user['enabled'] :
                xuser = self.conn.keycloak.get('/users/' + userid)
                if not ('federatedIdentities' in xuser.keys()) :
                    xuser['federatedIdentities'] = []
                userslist.append( xuser )
        return userslist


    def __internal_processpresets( self, presets ) :
        for preset in presets :
            presetid = preset['id']
            xqueries = self.conn.ast.get('/api/presets/' + str(presetid))
            preset.update(xqueries)                
        return presets


    def __internalprocessproject( self, project, simple = False, silent = False ) :
        cache_name = 'cxone projects'

        # Get the first available completed scan for a project
        def __cxone_getprojectlastscan( projid, sast, sca, kics, apisec ) :
            # Only go for a 50 page. if not found, return None
            scan = None
            if sast :
                scan = self.conn.ast.get( '/api/projects/last-scan?project-ids=' + projid + '&sast-status=completed&limit=50' )
            elif sca :
                scan = self.conn.ast.get( '/api/projects/last-scan?project-ids=' + projid + '&sca-status=completed&limit=50' )
            elif kics :
                scan = self.conn.ast.get( '/api/projects/last-scan?project-ids=' + projid + '&kics-status=completed&limit=50' )
            elif apisec :
                scan = self.conn.ast.get( '/api/projects/last-scan?project-ids=' + projid + '&apisec-status=completed&limit=50' )
            if scan :
                return scan[projid]

        projid = project['id']

        # Check for SCM data
        if not 'repoId' in project.keys() :
            project['repoId']       = None
        if not 'scmRepoId' in project.keys() :
            project['scmRepoId']    = None
            project['scmBranches']  = None
        else :
            project['scmBranches']  = None
            projdata = self.conn.ast.get('/api/projects/branches?project-id=' + projid)
            if projdata and len(projdata) > 0 :
                project['scmBranches'] = ','.join(projdata)


        # Get associated applications
        projdata = self.conn.ast.get('/api/projects/' + projid)
        project['applicationIds'] = projdata['applicationIds']

        # Get configurations for project
        projdata = self.conn.ast.get('/api/configuration/project?project-id=' + projid)
        # Get SAST configuration
        xvalue = next( filter( lambda el: el['key'] == 'scan.config.sast.languageMode' and el['originLevel'] == 'Project' and el['value'], projdata ), None )
        if xvalue :
            project['sastLanguageMode'] = xvalue['value'] if xvalue['value'] else None
        else :
            project['sastLanguageMode'] = None
        # Get SAST preset
        xvalue = next( filter( lambda el: el['key'] == 'scan.config.sast.presetName' and el['originLevel'] == 'Project' and el['value'], projdata ), None )
        if xvalue :
            project['sastPresetName'] = xvalue['value'] if xvalue['value'] else None
        else :
            project['sastPresetName'] = None
        # Get SAST filters (exclusions)
        xvalue = next( filter( lambda el: el['key'] == 'scan.config.sast.filter' and el['originLevel'] == 'Project' and el['value'], projdata ), None )
        if xvalue :
            project['sastFilter'] = xvalue['value'] if xvalue['value'] else None
        else :
            project['sastFilter'] = None
        # Get KICS platforms
        xvalue = next( filter( lambda el: el['key'] == 'scan.config.kics.platforms' and el['originLevel'] == 'Project' and el['value'], projdata ), None )
        if xvalue :
            project['kicsPlatforms'] = xvalue['value'] if xvalue['value'] else None
        else :
            project['kicsPlatforms'] = None
        # Get KICS filters (exclusions)
        xvalue = next( filter( lambda el: el['key'] == 'scan.config.kics.filter' and el['originLevel'] == 'Project' and el['value'], projdata ), None )
        if xvalue :
            project['kicsFilter'] = xvalue['value'] if xvalue['value'] else None
        else :
            project['kicsFilter'] = None
        # Get SCA exploitable path
        xvalue = next( filter( lambda el: el['key'] == 'scan.config.sca.ExploitablePath' and el['originLevel'] == 'Project' and el['value'], projdata ), None )
        if xvalue :
            project['scaExploitablePath'] = xvalue['value'] if xvalue['value'] else None
        else :
            project['scaExploitablePath'] = None
        # Get SCA last sast scan time path
        xvalue = next( filter( lambda el: el['key'] == 'scan.config.sca.LastSastScanTime' and el['originLevel'] == 'Project' and el['value'], projdata ), None )
        if xvalue :
            project['scaLastSastScanTime'] = xvalue['value'] if xvalue['value'] else None
        else :
            project['scaLastSastScanTime'] = None
        # Get SCA filters (exclusions)
        xvalue = next( filter( lambda el: el['key'] == 'scan.config.sca.filter' and el['originLevel'] == 'Project' and el['value'], projdata ), None )
        if xvalue :
            project['scaFilter'] = xvalue['value'] if xvalue['value'] else None
        else :
            project['scaFilter'] = None

        if not simple :
            project['isConsistent']     = True            
            # Add scanners data
            project['languages']        = []
            project['scanners']         = []
            scanids = []
            project['sastLastScan']     = {}
            project['scaLastScan']      = {}
            project['kicsLastScan']     = {}
            project['apisecLastScan']   = {}

            # Get SAST last completed scan
            project['sastLastScan']['scanid']           = None
            project['sastLastScan']['created']          = None
            project['sastLastScan']['useragent']        = None
            project['sastLastScan']['initiator']        = None
            project['sastLastScan']['sourcetype']       = None
            project['sastLastScan']['sourceorigin']     = None
            project['sastLastScan']['branch']           = None
            project['sastLastScan']['engines']          = None
            project['sastLastScan']['languages']        = None
            project['sastLastScan']['high']             = None            
            project['sastLastScan']['medium']           = None
            project['sastLastScan']['low']              = None
            project['sastLastScan']['info']             = None
            project['sastLastScan']['otherseverity']    = None
            project['sastLastScan']['toverify']                 = None
            project['sastLastScan']['notexploitable']           = None
            project['sastLastScan']['confirmed']                = None
            project['sastLastScan']['urgent']                   = None
            project['sastLastScan']['proposednotexploitable']   = None
            project['sastLastScan']['otherstate']               = None
            projdata = __cxone_getprojectlastscan( projid, True, False, False, False )
            if projdata :
                project['scanners'].append('sast')
                scanids.append(projdata['id'])
                project['sastLastScan']['scanid']           = projdata['id']
                project['sastLastScan']['created']          = projdata['createdAt']
                project['sastLastScan']['useragent']        = projdata['userAgent']
                project['sastLastScan']['initiator']        = projdata['initiator']
                project['sastLastScan']['sourcetype']       = projdata['sourceType']
                project['sastLastScan']['sourceorigin']     = projdata['sourceOrigin']
                project['sastLastScan']['branch']           = projdata['branch']
                project['sastLastScan']['engines']          = projdata['engines']
            # Get SCA last completed scan
            project['scaLastScan']['scanid']           = None
            project['scaLastScan']['created']          = None
            project['scaLastScan']['useragent']        = None
            project['scaLastScan']['initiator']        = None
            project['scaLastScan']['sourcetype']       = None
            project['scaLastScan']['sourceorigin']     = None
            project['scaLastScan']['branch']           = None
            project['scaLastScan']['engines']          = None
            project['scaLastScan']['high']             = None            
            project['scaLastScan']['medium']           = None
            project['scaLastScan']['low']              = None
            project['scaLastScan']['info']             = None
            project['scaLastScan']['otherseverity']    = None
            project['scaLastScan']['toverify']                 = None
            project['scaLastScan']['notexploitable']           = None
            project['scaLastScan']['confirmed']                = None
            project['scaLastScan']['urgent']                   = None
            project['scaLastScan']['proposednotexploitable']   = None
            project['scaLastScan']['otherstate']               = None
            projdata = __cxone_getprojectlastscan( projid, False, True, False, False )
            if projdata :
                project['scanners'].append('sca')
                scanids.append(projdata['id'])
                project['scaLastScan']['scanid']           = projdata['id']
                project['scaLastScan']['created']          = projdata['createdAt']
                project['scaLastScan']['useragent']        = projdata['userAgent']
                project['scaLastScan']['initiator']        = projdata['initiator']
                project['scaLastScan']['sourcetype']       = projdata['sourceType']
                project['scaLastScan']['sourceorigin']     = projdata['sourceOrigin']
                project['scaLastScan']['branch']           = projdata['branch']
                project['scaLastScan']['engines']          = projdata['engines']
            # Get KICS last completed scan
            project['kicsLastScan']['scanid']           = None
            project['kicsLastScan']['created']          = None
            project['kicsLastScan']['useragent']        = None
            project['kicsLastScan']['initiator']        = None
            project['kicsLastScan']['sourcetype']       = None
            project['kicsLastScan']['sourceorigin']     = None
            project['kicsLastScan']['branch']           = None
            project['kicsLastScan']['engines']          = None
            project['kicsLastScan']['high']             = None            
            project['kicsLastScan']['medium']           = None
            project['kicsLastScan']['low']              = None
            project['kicsLastScan']['info']             = None
            project['kicsLastScan']['otherseverity']    = None
            project['kicsLastScan']['toverify']                 = None
            project['kicsLastScan']['notexploitable']           = None
            project['kicsLastScan']['confirmed']                = None
            project['kicsLastScan']['urgent']                   = None
            project['kicsLastScan']['proposednotexploitable']   = None
            project['kicsLastScan']['otherstate']               = None
            projdata = __cxone_getprojectlastscan( projid, False, False, True, False )
            if projdata :
                project['scanners'].append('kics')
                scanids.append(projdata['id'])
                project['kicsLastScan']['scanid']           = projdata['id']
                project['kicsLastScan']['created']          = projdata['createdAt']
                project['kicsLastScan']['useragent']        = projdata['userAgent']
                project['kicsLastScan']['initiator']        = projdata['initiator']
                project['kicsLastScan']['sourcetype']       = projdata['sourceType']
                project['kicsLastScan']['sourceorigin']     = projdata['sourceOrigin']
                project['kicsLastScan']['branch']           = projdata['branch']
                project['kicsLastScan']['engines']          = projdata['engines']
            # Get API-SEC last completed scan
            project['apisecLastScan']['scanid']           = None
            project['apisecLastScan']['created']          = None
            project['apisecLastScan']['useragent']        = None
            project['apisecLastScan']['initiator']        = None
            project['apisecLastScan']['sourcetype']       = None
            project['apisecLastScan']['sourceorigin']     = None
            project['apisecLastScan']['branch']           = None
            project['apisecLastScan']['engines']          = None
            project['apisecLastScan']['high']             = None            
            project['apisecLastScan']['medium']           = None
            project['apisecLastScan']['low']              = None
            project['apisecLastScan']['info']             = None
            project['apisecLastScan']['otherseverity']    = None
            project['apisecLastScan']['toverify']                 = None
            project['apisecLastScan']['notexploitable']           = None
            project['apisecLastScan']['confirmed']                = None
            project['apisecLastScan']['urgent']                   = None
            project['apisecLastScan']['proposednotexploitable']   = None
            project['apisecLastScan']['otherstate']               = None
            projdata = __cxone_getprojectlastscan( projid, False, False, False, True )
            if projdata :
                project['scanners'].append('api-sec')
                scanids.append(projdata['id'])
                project['apisecLastScan']['scanid']           = projdata['id']
                project['apisecLastScan']['created']          = projdata['createdAt']
                project['apisecLastScan']['useragent']        = projdata['userAgent']
                project['apisecLastScan']['initiator']        = projdata['initiator']
                project['apisecLastScan']['sourcetype']       = projdata['sourceType']
                project['apisecLastScan']['sourceorigin']     = projdata['sourceOrigin']
                project['apisecLastScan']['branch']           = projdata['branch']
                project['apisecLastScan']['engines']          = projdata['engines']
            # Get summary data
            if len(scanids) > 0 :
                scanids = list(set(scanids))
                xfilter = ','.join(scanids)
                # This may fail for empty unfinished scans
                try :
                    summarydatas = self.conn.ast.get('/api/scan-summary?scan-ids=' + xfilter + '&include-queries=false&include-status-counters=false&include-files=false' )
                except Exception as e: 
                    project['isConsistent']     = False                       
                    summarydatas = None
                    pass
                # Process SAST data
                if summarydatas :
                    summary = next( filter( lambda el: el['scanId'] == project['sastLastScan']['scanid'], summarydatas['scansSummaries']), None )
                    if summary :
                        if len(project['languages']) == 0 :
                            for language in summary['sastCounters']['languageCounters'] :
                                project['languages'].append(language['language'])
                        # Severities
                        for severity in summary['sastCounters']['severityCounters'] :
                            if severity['severity'] == 'HIGH' :
                                project['sastLastScan']['high'] = severity['counter']
                            elif severity['severity'] == 'MEDIUM' :
                                project['sastLastScan']['medium'] = severity['counter']
                            elif severity['severity'] == 'LOW' :
                                project['sastLastScan']['low'] = severity['counter']
                            elif severity['severity'] == 'INFO' :
                                project['sastLastScan']['info'] = severity['counter']
                            else :
                                if not project['sastLastScan']['otherseverity'] :
                                    project['sastLastScan']['otherseverity'] = severity['counter']
                                else :
                                    project['sastLastScan']['otherseverity'] += severity['counter']
                        # States
                        for state in summary['sastCounters']['stateCounters'] :
                            if state['state'] == 'TO_VERIFY' :
                                project['sastLastScan']['toverify'] = state['counter']
                            elif state['state'] == 'NOT_EXPLOITABLE' :
                                project['sastLastScan']['notexploitable'] = state['counter']
                            elif state['state'] == 'CONFIRMED' :
                                project['sastLastScan']['confirmed'] = state['counter']
                            elif state['state'] == 'URGENT' :
                                project['sastLastScan']['urgent'] = state['counter']
                            elif state['state'] == 'PROPOSED_NOT_EXPLOITABLE' :
                                project['sastLastScan']['proposednotexploitable'] = state['counter']
                            else :
                                if not project['sastLastScan']['otherstate'] :
                                    project['sastLastScan']['otherstate'] = state['counter']
                                else :
                                    project['sastLastScan']['otherstate'] += state['counter']
                    # Process SCA data
                    summary = next( filter( lambda el: el['scanId'] == project['scaLastScan']['scanid'], summarydatas['scansSummaries']), None )
                    if summary :
                        # Severities
                        for severity in summary['scaCounters']['severityCounters'] :
                            if severity['severity'] == 'HIGH' :
                                project['scaLastScan']['high'] = severity['counter']
                            elif severity['severity'] == 'MEDIUM' :
                                project['scaLastScan']['medium'] = severity['counter']
                            elif severity['severity'] == 'LOW' :
                                project['scaLastScan']['low'] = severity['counter']
                            elif severity['severity'] == 'INFO' :
                                project['scaLastScan']['info'] = severity['counter']
                            else :
                                if not project['scaLastScan']['otherseverity'] :
                                    project['scaLastScan']['otherseverity'] = severity['counter']
                                else :
                                    project['scaLastScan']['otherseverity'] += severity['counter']
                        # States
                        for state in summary['scaCounters']['stateCounters'] :
                            if state['state'] == 'TO_VERIFY' :
                                project['scaLastScan']['toverify'] = state['counter']
                            elif state['state'] == 'NOT_EXPLOITABLE' :
                                project['scaLastScan']['notexploitable'] = state['counter']
                            elif state['state'] == 'CONFIRMED' :
                                project['scaLastScan']['confirmed'] = state['counter']
                            elif state['state'] == 'URGENT' :
                                project['scaLastScan']['urgent'] = state['counter']
                            elif state['state'] == 'PROPOSED_NOT_EXPLOITABLE' :
                                project['scaLastScan']['proposednotexploitable'] = state['counter']
                            else :
                                if not project['scaLastScan']['otherstate'] :
                                    project['scaLastScan']['otherstate'] = state['counter']
                                else :
                                    project['scaLastScan']['otherstate'] += state['counter']
                    # Process KICK data
                    summary = next( filter( lambda el: el['scanId'] == project['kicsLastScan']['scanid'], summarydatas['scansSummaries']), None )
                    if summary :
                        # Severities
                        for severity in summary['kicsCounters']['severityCounters'] :
                            if severity['severity'] == 'HIGH' :
                                project['kicsLastScan']['high'] = severity['counter']
                            elif severity['severity'] == 'MEDIUM' :
                                project['kicsLastScan']['medium'] = severity['counter']
                            elif severity['severity'] == 'LOW' :
                                project['kicsLastScan']['low'] = severity['counter']
                            elif severity['severity'] == 'INFO' :
                                project['kicsLastScan']['info'] = severity['counter']
                            else :
                                if not project['kicsLastScan']['otherseverity'] :
                                    project['kicsLastScan']['otherseverity'] = severity['counter']
                                else :
                                    project['kicsLastScan']['otherseverity'] += severity['counter']
                        # States
                        for state in summary['kicsCounters']['stateCounters'] :
                            if state['state'] == 'TO_VERIFY' :
                                project['kicsLastScan']['toverify'] = state['counter']
                            elif state['state'] == 'NOT_EXPLOITABLE' :
                                project['kicsLastScan']['notexploitable'] = state['counter']
                            elif state['state'] == 'CONFIRMED' :
                                project['kicsLastScan']['confirmed'] = state['counter']
                            elif state['state'] == 'URGENT' :
                                project['kicsLastScan']['urgent'] = state['counter']
                            elif state['state'] == 'PROPOSED_NOT_EXPLOITABLE' :
                                project['kicsLastScan']['proposednotexploitable'] = state['counter']
                            else :
                                if not project['kicsLastScan']['otherstate'] :
                                    project['kicsLastScan']['otherstate'] = state['counter']
                                else :
                                    project['kicsLastScan']['otherstate'] += state['counter']
                    # Process API-SEC data
                    summary = next( filter( lambda el: el['scanId'] == project['apisecLastScan']['scanid'], summarydatas['scansSummaries']), None )
                    if summary :
                        # Severities
                        for severity in summary['apiSecCounters']['severityCounters'] :
                            if severity['severity'] == 'HIGH' :
                                project['apisecLastScan']['high'] = severity['counter']
                            elif severity['severity'] == 'MEDIUM' :
                                project['apisecLastScan']['medium'] = severity['counter']
                            elif severity['severity'] == 'LOW' :
                                project['apisecLastScan']['low'] = severity['counter']
                            elif severity['severity'] == 'INFO' :
                                project['apisecLastScan']['info'] = severity['counter']
                            else :
                                if not project['apisecLastScan']['otherseverity'] :
                                    project['apisecLastScan']['otherseverity'] = severity['counter']
                                else :
                                    project['apisecLastScan']['otherseverity'] += severity['counter']
                        # States
                        for state in summary['apiSecCounters']['stateCounters'] :
                            if state['state'] == 'TO_VERIFY' :
                                project['apisecLastScan']['toverify'] = state['counter']
                            elif state['state'] == 'NOT_EXPLOITABLE' :
                                project['apisecLastScan']['notexploitable'] = state['counter']
                            elif state['state'] == 'CONFIRMED' :
                                project['apisecLastScan']['confirmed'] = state['counter']
                            elif state['state'] == 'URGENT' :
                                project['apisecLastScan']['urgent'] = state['counter']
                            elif state['state'] == 'PROPOSED_NOT_EXPLOITABLE' :
                                project['apisecLastScan']['proposednotexploitable'] = state['counter']
                            else :
                                if not project['apisecLastScan']['otherstate'] :
                                    project['apisecLastScan']['otherstate'] = state['counter']
                                else :
                                    project['apisecLastScan']['otherstate'] += state['counter']
        return project
    

    def __internalprojectsfilter( self, projectsfilter ) :
        pfilter = []
        if projectsfilter :
            if isinstance(projectsfilter, list):
                pfilter = projectsfilter
            elif isinstance(projectsfilter, str) :
                projectsfilter = projectsfilter.strip()
                if projectsfilter.startswith('=') :
                    pfilter = [projectsfilter[1:]]
                elif projectsfilter.startswith('==') :
                    pfilter = [projectsfilter[2:]]
                else :
                    pfilter = [projectsfilter]
        return pfilter


    def __internalgroupsfilter( self, groupsfilter, allgroups ) :
        tfilter = []
        pfilter = paramfilters.processfilter( groupsfilter, True )
        if pfilter :
            pnames  = []
            for group in allgroups :
                if (group['id'] in pfilter) or (group['path'] in pfilter) :        
                    pnames.append(group)
            for name in pnames :
                group = next( filter( lambda el: el['path'] == name or el['path'].startwith( name + '/'), allgroups ), None )
                if group :
                    tfilter.append(group['id'])
            tfilter = list(set(tfilter))
        if len(tfilter) > 0 :
            return tfilter
        else :
            return None


    def __internalcacheprojects( self, projectsfilter = None, simple: bool = False, tiny = False, silent: bool = False, updatinglist: list = None ) :    
        cache_name = 'cxone projects'
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
        signal = '  - Caching '
        pfilter = self.__internalprojectsfilter(projectsfilter)
        prjid = None
        prjname = None
        try :
            if len(pfilter) > 0 :
                for filtervalue in pfilter :
                    # Check if the filter is a uuid or a name
                    ffield = 'ids'
                    fvalue = filtervalue
                    try:
                        uuid.UUID(str(filtervalue))
                    except ValueError:
                        ffield = 'names'
                        fvalue = parse.quote(str(filtervalue), safe = '')
                    olist = self.conn.ast.get('/api/projects?' + ffield + '=' + fvalue + '&offset=0&limit=1')
                    if olist and olist['projects'] :
                        lcount += len(olist['projects'])
                        for proj in olist['projects'] :
                            prjid   = proj['id']
                            prjname = proj['name']
                            if updating :
                                existing = next( filter( lambda el: el['id'] == prjid, plist), None )
                                if existing :
                                    if tiny :
                                        existing = deepcopy(proj)
                                    else :
                                        existing = self.__internalprocessproject( deepcopy(proj), simple, silent )
                                else :
                                    if tiny :
                                        plist.append( proj )    
                                    else :
                                        plist.append( self.__internalprocessproject( proj, simple, silent ) )
                            else :
                                if tiny :
                                    plist.append( proj )
                                else :
                                    plist.append( self.__internalprocessproject( proj, simple, silent ) )
                        if not silent and lcount % 100 == 0 :
                            cxlogger.verbose( signal + cache_name + ' (' + str(lcount) + ')', False)
            else :
                olist = self.conn.ast.get('/api/projects?offset=' + str(lskip) + '&limit=100')
                while olist and olist['projects'] and len(olist['projects']) > 0 :
                    lcount += len(olist['projects'])
                    if not silent :
                        cxlogger.verbose( signal + cache_name + ' (' + str(lcount) + ')', False)
                    for proj in olist['projects'] :
                        prjid   = proj['id']
                        prjname = proj['name']
                        if updating :
                            existing = next( filter( lambda el: el['id'] == prjid, plist), None )
                            if existing :
                                if tiny :
                                    existing = deepcopy(proj)
                                else :
                                    existing = self.__internalprocessproject( deepcopy(proj), simple, silent )
                            else :
                                if tiny :
                                    plist.append( proj )    
                                else :
                                    plist.append( self.__internalprocessproject( proj, simple, silent ) )
                        else :
                            if tiny :
                                plist.append( proj )
                            else :
                                plist.append( self.__internalprocessproject( proj, simple, silent ) )
                    lskip += 100
                    olist = self.conn.ast.get('/api/projects?offset=' + str(lskip) + '&limit=100')
        except Exception as e:            
            if not silent :
                cxlogger.verbose( signal + cache_name + ' [' + str(prjid) + '] ' + str(prjname) + ' failed with "' + str(e) + '"', True, False, True )
            raise
        return plist


    def __internalcacheprojectkeys( self ) :    
        plist = []
        lskip = 0
        olist = self.conn.ast.get('/api/projects?offset=' + str(lskip) + '&limit=100')
        while olist and olist['projects'] and len(olist['projects']) > 0 :
            for proj in olist['projects'] :
                plist.append( { 'id': proj['id'], 'name': proj['name'] } )
            lskip += 100
            olist = self.conn.ast.get('/api/projects?offset=' + str(lskip) + '&limit=100')
        return plist


    def __internalcacheapplicationkeys( self ) :    
        plist = []
        lskip = 0
        olist = self.conn.ast.get('/api/applications?offset=' + str(lskip) + '&limit=100')
        while olist and olist['applications'] and len(olist['applications']) > 0 :
            for app in olist['applications'] :
                plist.append( { 'id': app['id'], 'name': app['name'] } )
            lskip += 100
            olist = self.conn.ast.get('/api/applications?offset=' + str(lskip) + '&limit=100')
        return plist


    def __internal_cachequeries( self, customonly: bool = False, includecode: bool = False ) :
        # Curent api implementation does not have paging. Allqueries came at once.
        # Project level queries are retrieved by project, repeating all Cx and Corp ones again.
        # That's why we have to obtain the projects list first.
        # Very inneficient, specially with many projects!!!
        if not self.__prjkeys :
            self.__prjkeys = self.__internalcacheprojectkeys()
        if not self.__appkeys :
            self.__appkeys = self.__internalcacheapplicationkeys()
        queries = []
        # Get all queries cx and corp
        xqueries = self.conn.ast.get('/api/cx-audit/queries')
        for xquery in xqueries :
            addquery = False
            xdata = xquery.copy()
            xdata['qtype']              = 'Original'
            xdata['projectid']          = None
            xdata['projectname']        = None
            xdata['applicationid']      = None
            xdata['applicationname']    = None
            if xdata['level'] == 'Cx' and not customonly :
                addquery = True
            elif xdata['level'] != 'Cx' :
                parent = next( filter( lambda el: el['name'] == xdata['name'] and el['lang'] == xdata['lang'] and el['level'] == 'Cx', xqueries), None )
                if parent :
                    xdata['qtype']      = 'Override'
                else :
                    xdata['qtype']      = 'Custom'
                addquery = True
            if addquery :
                if includecode :
                    xqpath = '/api/cx-audit/queries/' + xdata['level'] + '/'
                    xqpath = xqpath + parse.quote(xdata['path'], safe = '')
                    xqcode = self.conn.ast.get(xqpath)
                    xdata.update(xqcode)
                queries.append(xdata)

        # Now go for the projects
        for proj in self.__prjkeys :
            projqueries = self.conn.ast.get('/api/cx-audit/queries?projectId=' + proj['id'] )
            xqueries = list( filter( lambda el: el['level'] == 'Project', projqueries) )
            for xquery in xqueries :
                addquery = False
                xdata = xquery.copy()
                xdata['qtype']              = 'Override'
                xdata['projectid']          = proj['id']
                xdata['projectname']        = proj['name']
                xdata['applicationid']      = None
                xdata['applicationname']    = None
                parent = next( filter( lambda el: el['name'] == xdata['name'] and el['lang'] == xdata['lang'] and el['level'] == 'Cx', xqueries), None )
                if not parent :
                    xdata['qtype']      = 'Custom'
                if includecode :
                    xqpath = '/api/cx-audit/queries/' + proj['id'] + '/'
                    xqpath = xqpath + parse.quote(xdata['path'], safe = '')                
                    xqcode = self.conn.ast.get(xqpath)
                    xdata.update(xqcode)
                queries.append(xdata)

        # Now go for the applications
        for app in self.__appkeys :
            appqueries = self.conn.ast.get('/api/cx-audit/queries?applicationId=' + app['id'] )
            xqueries = list( filter( lambda el: el['level'] == 'Application', appqueries) )
            for xquery in xqueries :
                addquery = False
                xdata = xquery.copy()
                xdata['qtype']              = 'Override'
                xdata['projectid']          = None
                xdata['projectname']        = None
                xdata['applicationid']      = app['id']
                xdata['applicationname']    = app['name']
                parent = next( filter( lambda el: el['name'] == xdata['name'] and el['lang'] == xdata['lang'] and el['level'] == 'Cx', xqueries), None )
                if not parent :
                    xdata['qtype']      = 'Custom'
                if includecode :
                    xqpath = '/api/cx-audit/queries/' + app['id'] + '/'
                    xqpath = xqpath + parse.quote(xdata['path'], safe = '')                
                    xqcode = self.conn.ast.get(xqpath)
                    xdata.update(xqcode)
                queries.append(xdata)

        return queries


    def createcache( self, cachetype: cxonecachetype, contentfilter = None, silent: bool = False, forupdate: bool = False ) :
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
            # Configurations section
            if cachetype == cxonecachetype.tenant_defaults :
                cache_name = 'cxone tenant defaults'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                value = []
                xdata = self.conn.cxone.get( '/api/configuration/tenant' )
                if xdata :
                    # Default language mode (engine config)
                    data = next( filter( lambda el: el['key'] == 'scan.config.sast.languageMode', xdata), None )
                    if data :
                        xvalue = { 'Category': data['category'], 'Name': data['name'], 'Value': data['value'], 'AllowOverride': data['allowOverride']}
                        value.append(xvalue)
                    # Default preset
                    data = next( filter( lambda el: el['key'] == 'scan.config.sast.presetName', xdata), None )
                    if data :
                        xvalue = { 'Category': data['category'], 'Name': data['name'], 'Value': data['value'], 'AllowOverride': data['allowOverride']}
                        value.append(xvalue)
                    # Default incremental
                    data = next( filter( lambda el: el['key'] == 'scan.config.sast.incremental', xdata), None )
                    if data :
                        xvalue = { 'Category': data['category'], 'Name': data['name'], 'Value': data['value'], 'AllowOverride': data['allowOverride']}
                        value.append(xvalue)
                    # Default engine verbose
                    data = next( filter( lambda el: el['key'] == 'scan.config.sast.engineVerbose', xdata), None )
                    if data :
                        xvalue = { 'Category': data['category'], 'Name': data['name'], 'Value': data['value'], 'AllowOverride': data['allowOverride']}
                        value.append(xvalue)
                    # SCA Exploitable path
                    data = next( filter( lambda el: el['key'] == 'scan.config.sca.ExploitablePath', xdata), None )
                    if data :
                        xvalue = { 'Category': data['category'], 'Name': data['name'], 'Value': data['value'], 'AllowOverride': data['allowOverride']}
                        value.append(xvalue)
                    # KICS Platforms
                    data = next( filter( lambda el: el['key'] == 'scan.config.kics.platforms', xdata), None )
                    if data :
                        xvalue = { 'Category': data['category'], 'Name': 'kics_platforms', 'Value': data['value'], 'AllowOverride': data['allowOverride']}
                        value.append(xvalue)
                    # Default SAST filters
                    data = next( filter( lambda el: el['key'] == 'scan.config.sast.filter', xdata), None )
                    if data :
                        xvalue = { 'Category': data['category'], 'Name': 'sast_filter', 'Value': data['value'], 'AllowOverride': data['allowOverride']}
                        value.append(xvalue)
                    # Default SCA filters
                    data = next( filter( lambda el: el['key'] == 'scan.config.sca.filter', xdata), None )
                    if data :
                        xvalue = { 'Category': data['category'], 'Name': 'sca_filter', 'Value': data['value'], 'AllowOverride': data['allowOverride']}
                        value.append(xvalue)
                    # Default KICS filters
                    data = next( filter( lambda el: el['key'] == 'scan.config.kics.filter', xdata), None )
                    if data :
                        xvalue = { 'Category': data['category'], 'Name': 'kics_filter', 'Value': data['value'], 'AllowOverride': data['allowOverride']}
                        value.append(xvalue)
                self.__caches[cxonecachetype.tenant_defaults] = value
                lcount = len(self.__caches[cxonecachetype.tenant_defaults])
            elif cachetype == cxonecachetype.engine_configs :
                cache_name = 'cxone engine configurations'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                value = []
                xdata = self.conn.cxone.get( '/api/configuration/tenant' )
                if xdata :
                    data = next( filter( lambda el: el['key'] == 'scan.config.sast.languageMode', xdata), None )
                    if data :
                        xvalues = data['valuetypeparams'].split(',')
                        value = [s.strip() for s in xvalues]
                self.__caches[cxonecachetype.engine_configs] = value
                lcount = len(self.__caches[cxonecachetype.engine_configs])
            # Access control section
            elif cachetype == cxonecachetype.ac_saml_settings :
                cache_name = 'cxone saml settings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                samldata = []
                aux = self.conn.keycloak.get('/identity-provider/instances')
                if aux :
                    origlist = list( filter( lambda el: el['providerId'] == 'saml' and el['enabled'], aux) )
                    for saml in origlist :
                        samldata.append( { "id": saml['internalId'], "name": saml['alias'], "displayname": saml['displayName'], "issuer": saml['config']['singleSignOnServiceUrl'] })
                self.__caches[cxonecachetype.ac_saml_settings] = samldata
                lcount = len(self.__caches[cxonecachetype.ac_saml_settings])
            elif cachetype == cxonecachetype.ac_oidc_settings :
                cache_name = 'cxone oidc settings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                oidcdata = []
                aux = self.conn.keycloak.get('/identity-provider/instances')
                if aux :
                    origlist = list( filter( lambda el: el['providerId'] == 'oidc' and el['enabled'], aux) )
                    for oidc in origlist :
                        oidcdata.append( { "id": oidc['internalId'], "name": oidc['alias'], "displayname": oidc['displayName'], "issuer": oidc['config']['authorizationUrl'] })
                self.__caches[cxonecachetype.ac_oidc_settings] = oidcdata
                lcount = len(self.__caches[cxonecachetype.ac_oidc_settings])
            elif cachetype == cxonecachetype.ac_ldap_settings :
                cache_name = 'cxone ldap settings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                ldapdata = []
                aux = self.conn.keycloak.get('/components?parent=' + self.__tenantid + '&type=org.keycloak.storage.UserStorageProvider')
                if aux :
                    origlist = list( filter( lambda el: el['providerId'] == 'ldap', aux) )
                    for ldap in origlist :
                        if ldap['config'] and ldap['config']['enabled'] :
                            ldapdata.append( {"id": ldap['id'], "name": ldap['name'], "vendor": ', '.join(ldap['config']['vendor']), "issuer": ', '.join(ldap['config']['connectionUrl']) })
                self.__caches[cxonecachetype.ac_ldap_settings] = ldapdata
                lcount = len(self.__caches[cxonecachetype.ac_ldap_settings])
            elif cachetype == cxonecachetype.ac_groups :
                cache_name = 'cxone groups'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                groupdata = []
                groups = []
                lskip = 0
                # Get paged
                xgroups = self.conn.keycloak.get('/groups?first=' + str(lskip) + '&max=100')
                while len(xgroups) > 0 :
                    groups  = groups + xgroups
                    lskip   += 100
                    xgroups = self.conn.keycloak.get('/groups?first=' + str(lskip) + '&max=100')
                # Process - flatten
                self.__internal_flatten_groups( groups, None, groupdata )
                groupsaux = []
                groupsfilter = self.__internalgroupsfilter( contentfilter, groupdata )
                if groupsfilter :
                    for group in groupdata :
                        if (group['id'] in groupsfilter) :
                            groupsaux.append(group)
                    self.__caches[cxonecachetype.ac_groups] = groupsaux
                else :
                    self.__caches[cxonecachetype.ac_groups] = groupdata
                lcount = len(self.__caches[cxonecachetype.ac_groups])
            elif cachetype == cxonecachetype.ac_roles :
                cache_name = 'cxone roles'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__internal_get_keycloak_clientids()
                roles = []
                lskip = 0
                # shall be paged
                xroles = self.conn.keycloak.get('/clients/' + self.__ast_app + '/roles?first=' + str(lskip) + '&max=100' )
                while len(xroles) > 0 :
                    roles   = roles + xroles
                    lskip   += 100
                    xroles = self.conn.keycloak.get('/clients/' + self.__ast_app + '/roles?first=' + str(lskip) + '&max=100' )
                # Get the composite ones for root
                xroles = list( filter( lambda el: el['composite'] == True and el['clientRole'] == True, roles) )
                # Identify custom roles
                roles = []
                for xrole in xroles :
                    customrole = False
                    # Get role details to check if it is custom, may fail for incomplete role definition
                    try :
                        xroledata = self.conn.keycloak.get( '/clients/' + self.__ast_app + '/roles/' + parse.quote(xrole['name'], safe = '') )
                    except :
                        xroledata = None
                        pass
                    if xroledata :
                        xattributes = xroledata.get('attributes')
                        if xattributes :
                            xcreator = xattributes.get('creator')
                            if xcreator :
                                if not 'Checkmarx' in xcreator :
                                    customrole = True
                        xrole['isSystemRole'] = not customrole
                        roles.append(xrole)
                rolesfilter = paramfilters.processfilter( contentfilter, True )
                rolessaux = []
                if rolesfilter :
                    for role in roles :
                        if (role['id'] in rolesfilter) or (role['name'] in rolesfilter) :
                            rolessaux.append(group)
                    self.__caches[cxonecachetype.ac_roles] = rolessaux
                else :
                    self.__caches[cxonecachetype.ac_roles] = roles
                lcount = len(self.__caches[cxonecachetype.ac_roles])
            elif cachetype == cxonecachetype.ac_users :
                cache_name = 'cxone users'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                users = []
                lskip = 0
                # Get paged
                xusers = self.conn.keycloak.get('/users?first=' + str(lskip) + '&max=100')
                while len(xusers) > 0 :
                    users   = users + xusers
                    lskip   += 100
                    xusers  = self.conn.keycloak.get('/users?first=' + str(lskip) + '&max=100')
                self.__caches[cxonecachetype.ac_users] = self.__internal_processusers( users )
                lcount = len(self.__caches[cxonecachetype.ac_users])
            # Queries and presets section
            elif cachetype == cxonecachetype.presets :
                cache_name = 'cxone presets'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                presets = []
                lskip = 0
                xpresets = self.conn.ast.get('/api/presets?offset=' + str(lskip) + '&limit=100')
                xtotal = xpresets['totalCount']
                while len(xpresets) > 0 and xpresets['presets'] and len(presets) < xtotal :
                    presets = presets + xpresets['presets']
                    lskip += 100
                    xpresets = self.conn.ast.get('/api/presets?offset=' + str(lskip) + '&limit=100')
                self.__caches[cxonecachetype.presets] = self.__internal_processpresets( presets )
                lcount = len(self.__caches[cxonecachetype.presets])
            elif cachetype == cxonecachetype.presetssimple :
                cache_name = 'cxone presets'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                presets = []
                lskip = 0
                xpresets = self.conn.ast.get('/api/presets?offset=' + str(lskip) + '&limit=100')
                xtotal = xpresets['totalCount']
                while len(xpresets) > 0 and xpresets['presets'] and len(presets) < xtotal :
                    presets = presets + xpresets['presets']
                    lskip += 100
                    xpresets = self.conn.ast.get('/api/presets?offset=' + str(lskip) + '&limit=100')
                self.__caches[cxonecachetype.presetssimple] = presets
                lcount = len(self.__caches[cxonecachetype.presetssimple])
            elif cachetype == cxonecachetype.queries_custom :
                cache_name = 'cxone custom queries'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[cxonecachetype.queries_custom] = self.__internal_cachequeries( True, True )
                lcount = len(self.__caches[cxonecachetype.queries_custom])
            elif cachetype == cxonecachetype.queries_all :
                cache_name = 'cxone all queries'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[cxonecachetype.queries_all] = self.__internal_cachequeries( False, False )
                lcount = len(self.__caches[cxonecachetype.queries_all])
            elif cachetype == cxonecachetype.queries_sast_maps :
                cache_name = 'cxone query sast mappings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                mappings = self.conn.ast.get('/api/queries/mappings')
                self.__caches[cxonecachetype.queries_sast_maps] = mappings['mappings']
                lcount = len(self.__caches[cxonecachetype.queries_sast_maps])
            # Projects section
            elif cachetype == cxonecachetype.applications :
                cache_name = 'cxone applications'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                applications = []
                lskip = 0
                xapplications = self.conn.ast.get('/api/applications?offset=' + str(lskip) + '&limit=100')
                xtotal = xapplications['totalCount']
                while len(xapplications) > 0 and xapplications['applications'] and len(applications) < xtotal :
                    applications = applications + xapplications['applications']
                    lskip += 100
                    xapplications = self.conn.ast.get('/api/applications?offset=' + str(lskip) + '&limit=100')
                appsfilter = paramfilters.processfilter( contentfilter, True )
                appsaux = []
                if appsfilter :
                    for app in applications :
                        if (app['id'] in appsfilter) or (app['name'] in appsfilter) :
                            appsaux.append(app)
                    self.__caches[cxonecachetype.applications] = appsaux
                else :
                    self.__caches[cxonecachetype.applications] = applications
                lcount = len(self.__caches[cxonecachetype.applications])
            elif cachetype == cxonecachetype.projectsfull :
                cache_name = 'cxone projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[cxonecachetype.projectsfull] = self.__internalcacheprojects( contentfilter, False, False, silent )
                lcount = len(self.__caches[cxonecachetype.projectsfull])
            elif cachetype == cxonecachetype.projectssimple :
                cache_name = 'cxone projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[cxonecachetype.projectssimple] = self.__internalcacheprojects( contentfilter, True, False, silent )
                lcount = len(self.__caches[cxonecachetype.projectssimple])
            elif cachetype == cxonecachetype.projectstiny :
                cache_name = 'cxone projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[cxonecachetype.projectstiny] = self.__internalcacheprojects( contentfilter, True, True, silent )
                lcount = len(self.__caches[cxonecachetype.projectstiny])
            # Done
            if not silent :    
                cxlogger.verbose( signalsuccess + cache_name + filtered + ' (' + str(lcount) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            if not silent :
                cxlogger.verbose( signalerrors + cache_name + filtered + ' (' + str(lcount) + ') failed with "' + str(e) + '"', True, False, True, e )

        return errorcount
    

    def updatecache( self, cachetype: cxonecachetype, contentfilter = None, silent: bool = False ) :
        errorcount = 0
        lcount = 0
        dtini = datetime.now()

        if not ( cachetype in [cxonecachetype.projectsfull, cxonecachetype.projectssimple, cxonecachetype.projectstiny] ) :
            self.uncache( cachetype )
            return self.createcache( cachetype, contentfilter, silent, True )

        try :
            signal = '  - Updating cache '
            # Filtered indicator
            filtered = ''
            if contentfilter :
                filtered = ' filtered'
            if cachetype == cxonecachetype.projectsfull :
                cache_name = 'cxone projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered)
                self.__caches[cxonecachetype.projectsfull] = self.__internalcacheprojects( contentfilter, False, False, silent, self.cache(cxonecachetype.projectsfull) )
                lcount = len(self.__caches[cxonecachetype.projectsfull])
            elif cachetype == cxonecachetype.projectssimple :
                cache_name = 'cxone projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[cxonecachetype.projectssimple] = self.__internalcacheprojects( contentfilter, True, False, silent, self.cache(cxonecachetype.projectssimple) )
                lcount = len(self.__caches[cxonecachetype.projectssimple])
            elif cachetype == cxonecachetype.projectstiny :
                cache_name = 'cxone projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[cxonecachetype.projectstiny] = self.__internalcacheprojects( contentfilter, True, True, silent, self.cache(cxonecachetype.projectstiny) )
                lcount = len(self.__caches[cxonecachetype.projectstiny])
            # Done
            if not silent :    
                cxlogger.verbose( '  - Cache updated ' + cache_name + filtered + ' (' + str(lcount) + ') ' + self.duration(dtini, True), False)
        except Exception as e:
            errorcount += 1
            if not silent :
                cxlogger.verbose( '  - Cache updating ' + cache_name + filtered + ' (' + str(lcount) + ') failed with "' + str(e) + '"', True, False, True, e )

        return errorcount



    def createallcaches(self, projectsfilter = None, applicationsfilter = None, groupsfilter = None ) :
        errorcount = 0
        # Configuartions section
        errorcount += self.createcache( cxonecachetype.tenant_defaults ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.engine_configs ) if errorcount == 0 else 0
        # Access control section
        errorcount += self.createcache( cxonecachetype.ac_saml_settings ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.ac_oidc_settings ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.ac_ldap_settings ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.ac_groups, groupsfilter ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.ac_roles ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.ac_users ) if errorcount == 0 else 0
        # # Presets and queries
        errorcount += self.createcache( cxonecachetype.presets ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.queries_all ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.queries_custom ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.queries_sast_maps ) if errorcount == 0 else 0
        # # Projects section
        errorcount += self.createcache( cxonecachetype.applications, applicationsfilter ) if errorcount == 0 else 0
        errorcount += self.createcache( cxonecachetype.projectsfull, projectsfilter ) if errorcount == 0 else 0
        return errorcount
