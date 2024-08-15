""" 
========================================================================

SIMPLE CLASS TO CACHE SCA DATA

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
from scaconn import scaconn
from cxparamfilters import paramfilters



class scacachetype(Enum) :
    # Access control setting
    ac_saml_settings    = 10
    ac_master_settings  = 11
    ac_teams            = 12
    ac_roles            = 13
    ac_users            = 14
    # Projects
    projects            = 30
    projectstiny        = 31
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



class scacache(object) :

    def __init__(self) :
        self.__conn         = None
        self.__caches       = {}    


    def __init__(self, conn: scaconn ) :
        self.__conn         = conn
        self.__caches       = {}    


    @property
    def conn(self) :
        return self.__conn
    

    @property
    def caches(self) :
        return self.__caches
    

    def cache(self, cachetype: scacachetype ) :
        if self.hascache(cachetype) :
            return self.__caches[cachetype]
        else :
            return None


    def cacheoneof(self, cachetypes: list[scacachetype] ) :   
        for cachetype in cachetypes :
            if self.hascache(cachetype) :
                return self.__caches[cachetype]
        return None
    

    def uncache(self, cachetype: scacachetype ) :
        if self.hascache(cachetype) :
            self.__caches[cachetype] = None
            self.__caches.pop(cachetype, None)


    def hascache(self, cachetype: scacachetype ) :
        return cachetype in self.__caches.keys()
    

    def copycache( self, sourcetype: scacachetype, desttype: scacachetype ) :
        if not self.hascache(sourcetype) :
            raise Exception( 'Source type is void.')
        self.__caches[desttype] = deepcopy(self.__caches[sourcetype])


    def putcache( self, cachetype: scacachetype, cachedata: None ) :
        if not cachetype in [scacachetype.aux1, scacachetype.aux2, scacachetype.aux3, scacachetype.aux4, scacachetype.aux5, scacachetype.aux6, scacachetype.aux7, scacachetype.aux8, scacachetype.aux9] :
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


    def __internalprocessproject( self, project ) :
        data = {}
        data['id']                          = project['id']
        data['name']                        = project['name']
        data['createdOn']                   = project['createdOn']
        data['lastUpdate']                  = project['lastUpdate']
        data['enableExploitablePath']       = project['enableExploitablePath']
        data['lastSastScanTime']            = project['lastSastScanTime']
        data['branch']                      = project['branch']
        data['isManaged']                   = project['isManaged']
        data['lastSuccessfulScanId']        = project['lastSuccessfulScanId']
        data['latestScanId']                = project['latestScanId']
        data['canonicalName']               = project['canonicalName']
        data['tenantId']                    = project['tenantId']
        if project['riskReportSummary'] :
            data['riskReportSummary']           = project['riskReportSummary']['id']
            data['riskReportCreatedOn']         = project['riskReportSummary']['createdOn']
            data['riskReportLastUpdate']        = project['riskReportSummary']['lastUpdate']
            data['directPackages']              = project['riskReportSummary']['directPackages']
            data['totalPackages']               = project['riskReportSummary']['totalPackages']
            data['totalOutdatedPackages']       = project['riskReportSummary']['totalOutdatedPackages']
            data['highVulnerabilityCount']      = project['riskReportSummary']['highVulnerabilityCount']
            data['mediumVulnerabilityCount']    = project['riskReportSummary']['mediumVulnerabilityCount']
            data['lowVulnerabilityCount']       = project['riskReportSummary']['lowVulnerabilityCount']
            data['ignoredVulnerabilityCount']   = project['riskReportSummary']['ignoredVulnerabilityCount']
            data['lastScanned']                 = project['riskReportSummary']['lastScanned']
            data['severity']                    = project['riskReportSummary']['severity']
            data['isViolated']                  = project['riskReportSummary']['isViolated']
            data['isPrivatePackage']            = project['riskReportSummary']['isPrivatePackage']
        else :
            data['riskReportSummary']           = ''
            data['riskReportCreatedOn']         = ''
            data['riskReportLastUpdate']        = ''
            data['directPackages']              = 0
            data['totalPackages']               = 0
            data['totalOutdatedPackages']       = 0
            data['highVulnerabilityCount']      = 0
            data['mediumVulnerabilityCount']    = 0
            data['lowVulnerabilityCount']       = 0
            data['ignoredVulnerabilityCount']   = 0
            data['lastScanned']                 = ''
            data['severity']                    = ''
            data['isViolated']                  = False
            data['isPrivatePackage']            = False
        data['tags']                        = project['tags']
        data['assignedTeams']               = project['assignedTeams']
        # if not simple :
        #     data['ToVerify']                = 0
        #     data['NotExploitable']          = 0
        #     data['Confirmed']               = 0
        #     data['Urgent']                  = 0
        #     data['ProposedNotExploitable']  = 0
        #     triages = self.conn.sca.get('/risk-management/risk-state/' + project['id'] )
        #     for triage in triages :
        #         state = triage['state']
        #         data[state] = data[state] + 1
        return data


    def __internalprojectsfilter( self, projectsfilter ) :
        pfilter = ''
        pfilterlist = False
        if projectsfilter :
            if isinstance(projectsfilter, list):
                pfilterlist = True
            elif isinstance(projectsfilter, str) :
                projectsfilter = projectsfilter.strip()
                if projectsfilter.startswith('=') :
                    pfilter = '&$filter=Id eq ' + projectsfilter[1:]
                elif projectsfilter.startswith('==') :
                    pfilter = '&$filter=Id eq ' + projectsfilter[2:]
                else :
                    pfilter = str('&$filter=Id eq ') + projectsfilter
            elif isinstance(projectsfilter, int) :
                pfilter = str('&$filter=Id eq ') + str(projectsfilter)
        return pfilter, pfilterlist


    def __internalteamsfilter( self, teamsfilter, allteams ) :
        tfilter = []
        pfilter = paramfilters.processfilter( teamsfilter, True )
        if pfilter :
            pnames  = []
            for team in allteams :
                if (team['id'] in pfilter) or (team['fullName'] in pfilter) :
                    pnames.append(team)
            for name in pnames :
                team = next( filter( lambda el: el['fullName'] == name or el['fullName'].startwith( name + '/'), allteams ), None )
                if team :
                    tfilter.append(team['id'])
            tfilter = list(set(tfilter))
        if len(tfilter) > 0 :
            return tfilter
        else :
            return None


    def __internalcacheprojects( self, projectsfilter = None, tiny = False, silent: bool = False, updatinglist: list = None ) :    
        cache_name = 'sca projects'
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
        pfilter, pfilterlist = self.__internalprojectsfilter(projectsfilter)
        if pfilterlist :
            for filtervalue in projectsfilter :
                # Check if the filter is a uuid or a name
                try:
                    uuid.UUID(str(filtervalue))
                    pfilter = '&$filter=Id eq ' + str(filtervalue)
                except ValueError:
                    pfilter = '&$filter=name eq %27' + parse.quote(str(filtervalue), safe = '') + '%27'
                olist = self.conn.sca.get('/risk-management/projectsriskreportsummary?$expand=riskReportSummary,tags,assignedTeams($filter=isDirectlyAssigned eq true)&$top=1&$skip=0' + pfilter)
                lcount += len(olist)
                for proj in olist :
                    prjid = proj['id']
                    if updating :
                        existing = next( filter( lambda el: el['id'] == prjid, plist), None )
                        if existing :
                            if tiny :
                                existing = deepcopy(proj)
                            else :
                                existing = self.__internalprocessproject( deepcopy(proj) )
                        else :
                            if tiny :
                                plist.append( proj )    
                            else :
                                plist.append( self.__internalprocessproject( proj ) )
                    else :
                        if tiny :
                            plist.append( proj )
                        else :
                            plist.append( self.__internalprocessproject( proj ) )
                    if tiny :
                        plist.append( proj )
                    else :
                        plist.append( self.__internalprocessproject( proj ) )
                if not silent and lcount % 100 == 0 :
                    cxlogger.verbose( signal + cache_name + ' (' + str(lcount) + ')', False)
        else :
            olist = self.conn.sca.get('/risk-management/projectsriskreportsummary?$expand=riskReportSummary,tags,assignedTeams($filter=isDirectlyAssigned eq true)&$top=100&$skip='  + str(lskip) + pfilter)
            while len(olist) > 0 :
                lcount += len(olist)
                if not silent :
                    cxlogger.verbose( signal + cache_name + ' (' + str(lcount) + ')', False)
                for proj in olist :
                    prjid = proj['id']
                    if updating :
                        existing = next( filter( lambda el: el['id'] == prjid, plist), None )
                        if existing :
                            if tiny :
                                existing = deepcopy(proj)
                            else :
                                existing = self.__internalprocessproject( deepcopy(proj) )
                        else :
                            if tiny :
                                plist.append( proj )    
                            else :
                                plist.append( self.__internalprocessproject( proj ) )
                    else :
                        if tiny :
                            plist.append( proj )
                        else :
                            plist.append( self.__internalprocessproject( proj ) )
                    if tiny :
                        plist.append( proj )
                    else :
                        plist.append( self.__internalprocessproject( proj ) )
                lskip += 100
                olist = self.conn.sca.get('/risk-management/projectsriskreportsummary?$expand=riskReportSummary,tags,assignedTeams($filter=isDirectlyAssigned eq true)&$top=100&$skip='  + str(lskip) + pfilter)
        return plist


    def createcache( self, cachetype: scacachetype, contentfilter = None, silent: bool = False, forupdate: bool = False ) :
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
            # Access control section
            if cachetype == scacachetype.ac_saml_settings :
                cache_name = 'sca saml settings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                samldata = []
                samllist = self.conn.ac.get('/samlidentityproviders')
                samlproviders = self.conn.ac.get('/authenticationproviders')
                samlactive = list( filter( lambda el: el['active'], samllist ) )
                for saml in samlactive :    
                    provid  = next(filter(lambda el: el['providerId'] == saml['id'] and el['providerType'] == 'SAML', samlproviders), None)['id']
                    samldata.append( { "id": provid, "name": saml['name'], "issuer": saml['issuer'] })
                self.__caches[scacachetype.ac_saml_settings] = samldata
                lcount = len(self.__caches[scacachetype.ac_saml_settings])
            elif cachetype == scacachetype.ac_master_settings :
                cache_name = 'sca master ac settings'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                masterdata = []
                masterlist = self.conn.ac.get('/primaryaccesscontrol')
                masterproviders = self.conn.ac.get('/authenticationproviders')
                if masterlist and masterlist['isActive'] :
                    provid  = next(filter(lambda el: el['name'] == masterlist['name'] and el['providerType'] == 'MasterAccessControl', masterproviders), None)['id']
                    masterdata.append( { "id": provid, "name": masterlist['name'], "issuer": masterlist['issuer'] })
                self.__caches[scacachetype.ac_master_settings] = masterdata
                lcount = len(self.__caches[scacachetype.ac_master_settings])
            elif cachetype == scacachetype.ac_teams :
                cache_name = 'sca teams'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                teamsaux = []
                teams = self.conn.ac.get('/teams')
                teamsfilter = self.__internalteamsfilter( contentfilter, teams )
                if teamsfilter :
                    for team in teams :
                        if (team['id'] in teamsfilter) :
                            teamsaux.append(team)
                    self.__caches[scacachetype.ac_teams] = teamsaux
                else :
                    self.__caches[scacachetype.ac_teams] = teams
                lcount = len(self.__caches[scacachetype.ac_teams])
            elif cachetype == scacachetype.ac_roles :
                cache_name = 'sca roles'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                rolesfilter = paramfilters.processfilter( contentfilter, True )
                rolesaux = []
                roles = self.conn.ac.get('/roles')
                if rolesfilter :
                    for role in roles :
                        if (role['id'] in rolesfilter) or (role['name'] in rolesfilter) :
                            rolesaux.append(role)
                    self.__caches[scacachetype.ac_roles] = rolesaux
                else :
                    self.__caches[scacachetype.ac_roles] = roles
                lcount = len(self.__caches[scacachetype.ac_roles])
            elif cachetype == scacachetype.ac_users :
                cache_name = 'sca users'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                self.__caches[scacachetype.ac_users] = self.conn.ac.get('/users')
                lcount = len(self.__caches[scacachetype.ac_users])
            # Projects section
            elif cachetype == scacachetype.projects :
                cache_name = 'sca projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( contentfilter, False, silent )
                self.__caches[scacachetype.projects] = plist
                lcount = len(plist)
            # Projects section
            elif cachetype == scacachetype.projectstiny :
                cache_name = 'sca projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( contentfilter, True, silent )
                self.__caches[scacachetype.projectstiny] = plist
                lcount = len(plist)
            # Done
            if not silent :    
                cxlogger.verbose( signalsuccess + cache_name + filtered + ' (' + str(lcount) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            if not silent :
                cxlogger.verbose( signalerrors + cache_name + filtered + ' (' + str(lcount) + ') failed with "' + str(e) + '"', True, False, True, e )

        return errorcount
    

    def updatecache( self, cachetype: scacachetype, contentfilter = None, silent: bool = False, forupdate: bool = False ) :
        errorcount = 0
        lcount = 0
        dtini = datetime.now()

        if not ( cachetype in [scacachetype.projects, scacachetype.projectstiny] ) :
            self.uncache( cachetype )
            return self.createcache( cachetype, contentfilter, silent, True )
        
        try :
            signal = '  - Updating cache '
            # Filtered indicator
            filtered = ''
            if contentfilter :
                filtered = ' filtered'

            # Projects section
            if cachetype == scacachetype.projects :
                cache_name = 'sca projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( contentfilter, False, silent, self.cache(scacachetype.projects) )
                self.__caches[scacachetype.projects] = plist
                lcount = len(plist)
            # Projects section
            elif cachetype == scacachetype.projectstiny :
                cache_name = 'sca projects'
                if not silent :
                    cxlogger.verbose( signal + cache_name + filtered )
                plist = self.__internalcacheprojects( contentfilter, True, silent, self.cache(scacachetype.projectstiny) )
                self.__caches[scacachetype.projectstiny] = plist
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
        # Access control section
        errorcount += self.createcache( scacachetype.ac_saml_settings ) if errorcount == 0 else 0
        errorcount += self.createcache( scacachetype.ac_master_settings ) if errorcount == 0 else 0
        errorcount += self.createcache( scacachetype.ac_teams, teamsfilter ) if errorcount == 0 else 0
        errorcount += self.createcache( scacachetype.ac_roles ) if errorcount == 0 else 0
        errorcount += self.createcache( scacachetype.ac_users ) if errorcount == 0 else 0
        # Projects section
        errorcount += self.createcache( scacachetype.projects, projectsfilter ) if errorcount == 0 else 0
        return errorcount

