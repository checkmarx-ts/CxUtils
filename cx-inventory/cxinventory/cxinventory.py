""" 
========================================================================

CHECKMARX DATA EXTRACTOR TOOLING
- SAST, SCA, CXONE

joao.costa@checkmarx.com
PS-EMEA
22-06-2023

========================================================================
"""


import os
import sys
if not getattr(sys, 'frozen', False) :
    sys.path.insert(1, os.path.abspath(os.path.dirname(__file__)) + os.sep + '..' + os.sep + 'shared')
from cxloghandler import cxlogger
from baserunner import baserunner
from datetime import datetime
from cxparamfilters import paramfilters
from cxparamfilters import ValidFilter
from src.cxinventoryconfigdefaults import cxinventoryconfiguration
from sastconn import sastconn
from sastcache import sastcache
from sastcache import sastcachetype
from src.sastinventoryrunner import sastinventory
from src.sastalltriagesrunner import sastalltriages
from src.sastcounttriagesrunner import sastcounttriages
from src.sastcustomqueriesrunner import sastcustomqueries
from scaconn import scaconn
from scacache import scacachetype
from scacache import scacache
from src.scainventoryrunner import scainventory
from src.scaalltriagesrunner import scaalltriages
from src.scacounttriagesrunner import scacounttriages
from cxoneconn import cxoneconn
from cxonecache import cxonecachetype
from cxonecache import cxonecache
from src.cxoneinventoryrunner import cxoneinventory
from src.cxonecounttriagesrunner import cxonecounttriages
from src.cxonealltriagesrunner import cxonealltriages



class cxinventory(baserunner) :

    # Overriding
    def printhelp(self) :
        print( '============================================================' )
        print( 'Checkmarx Inventory Tool' )
        print( '© Checkmarx. All rights reserved.' )
        print( 'Version: ' + self.config.value('version') )
        print( '============================================================' )
        print( 'COMMANDS: ')
        print( '  sast                    To inventory a SAST instance (default)' )
        print( '  cxone                   To inventory a CXONE tenant' )
        print( '  sca                     To inventory a SCA tenant' )        
        print( 'EXECUTION OPTIONS:' )
        print( '  --inventory             Extract the full inventory data (default)' )
        print( '  --triages-count         Extract counts of triages per state from all projects' )
        print( '  --triages-all           Extract all triaged results from all projects (heavy, please avoid)' )
        print( '  --custom-queries        Extract custom queries along with their code (sast only)' )
        print( 'GENERAL OPTIONS:' )
        print( '  --help, -h              This help information' )
        print( '  --verbose, -v           Verbose the execution to the console' )
        print( 'FILTER OPTIONS:' )
        print( '  --filter.projects       Filter projects using: project id, array of ids [id1,id2,..], external file with ids "@filepath", sast range like > >= < <= project id' )
        print( 'SAST CONNECTION PARAMETERS:' )
        print( '  --sast.url              You SAST url, example: https//sast.url.net (mandatory for sast)' )
        print( '  --sast.username         User name to access your SAST (mandatory for sast)' )
        print( '  --sast.password         Password to access your SAST (mandatory for sast)' )
        print( '  --sast.proxy_url        Network proxy to use, optional')
        print( '  --sast.proxy_username   User name to pass the proxy, if needed' )
        print( '  --sast.proxy_password   Password to pass the proxy, if needed' )
        print( 'CXONE CONNECTION PARAMETERS:' )
        print( '  --cxone.url             Your CXONE api, example: https//eu.ast.checkmarx.com (mandatory for cxone)' )
        print( '  --cxone.acl             Your CXONE iam, example: https//eu.iam.checkmarx.com (mandatory for cxone)' )
        print( '  --cxone.tenant          Your CXONE tenant name (mandatory for cxone)' )
        print( '  --cxone.apikey          Api key to access your CXONE (mandatory for cxone)' )
        print( '  --cxone.clientid        Client id to access your CXONE' )
        print( '  --cxone.grattype        Grant type to access your CXONE')
        print( '  --cxone.proxy_url       Network proxy to use, optional')
        print( '  --cxone.proxy_username  User name to pass the proxy, if needed' )
        print( '  --cxone.proxy_password  Password to pass the proxy, if needed' )
        print( 'SCA CONNECTION PARAMETERS:' )
        print( '  --sca.url               Your SCA api, example: https//api-sca.checkmarx.com (mandatory for sca)' )
        print( '  --sca.acl               Your SCA platform, example: https//platform.checkmarx.com (mandatory for sca)' )
        print( '  --sca.tenant            Your SCA tenant name (mandatory for sca)' )
        print( '  --sca.username          Username to access your SCA (mandatory for sca)' )
        print( '  --sca.password          Password to access your SCA (mandatory for sca)' )
        print( '  --sca.proxy_url         Network proxy to use, optional')
        print( '  --sca.proxy_username    User name to pass the proxy, if needed' )
        print( '  --sca.proxy_password    Password to pass the proxy, if needed' )


    # Overriding
    def execute(self) :
        errorcount = 0
        # Load configurations           
        self.loadconfig( defaults = cxinventoryconfiguration )
        # Init log and verbose
        cxlogger.activate( verbose = self.verbose, logging = True, debug = False )
        # To compute duration
        dtini = datetime.now()

        try :

            # Verbose the header
            cxlogger.verbose( '' )
            cxlogger.verbose( '============================================================' )
            cxlogger.verbose( 'Checkmarx Inventory Tool' )
            cxlogger.verbose( '© Checkmarx. All rights reserved.' )
            cxlogger.verbose( 'Version: ' + self.config.value('version') )
            cxlogger.verbose( '============================================================' )
            cxlogger.verbose( 'Date: ' + dtini.strftime('%d-%m-%Y %H:%M:%S') )

            # Check where to go (commands: SAST, SCA, CXONE)
            commands = []
            command = ''
            if self.config.hascommand('sast') or self.config.hascommand('cxsast') :
                commands.append('sast')
            if self.config.hascommand('sca') or self.config.hascommand('cxsca') :
                commands.append('sca')
            if self.config.hascommand('cxone') or self.config.hascommand('cx1') :
                commands.append('cxone')
            # If none, assume SAST        
            if len(commands) == 0 :
                cxlogger.verbose( 'Target environment type not specified. Using sast.' )
                commands.append('sast')
            # Check it and report back if error
            if len(commands) == 0 :
                errorcount += 1
                raise Exception( 'A target environment must be selected. Please select one of:  sast, cxone, sca')
            if len(commands) > 1 :
                errorcount += 1
                raise Exception( 'A single environment must be selected. You selected: ' + ', '.join(commands))
            command = commands[0]

            # Check what to do
            actions = []
            action  = ''
            if self.config.haskey('inventory') :
                actions.append('inventory')
            if self.config.haskey('triages-all') :
                actions.append('triages-all')
            if self.config.haskey('triages-count') :
                actions.append('triages-count')
            if self.config.haskey('custom-queries') :
                if command != 'sast' :
                    errorcount += 1
                    raise Exception( 'Custom queries can only be retrived from sast, not from ' + command )
                actions.append('custom-queries')
            # Default is inventory
            if len(actions) == 0 :
                cxlogger.verbose( 'Execution action not specified. Using inventory.' )
                actions.append('inventory')

            # -----------------------------------------------------------------
            # SAST 
            # -----------------------------------------------------------------
            if command == 'sast' :

                # Connect to SAST instance
                cxsastconn = None
                try :
                    cxlogger.verbose( 'Connecting to SAST "' + self.config.value('sast.url') + '"' )
                    cxsastconn = sastconn( self.config.value('sast.url'), self.config.value('sast.username'), self.config.value('sast.password'), self.config.value('sast.proxy_url'), self.config.value('sast.proxy_username'), self.config.value('sast.proxy_password') )
                    cxsastconn.logon()
                    ver = cxsastconn.versionstring
                    if not ver or ver == '0' :
                        raise Exception( 'Cound not obtain sast version' )
                    cxlogger.verbose( 'Connected to SAST, version ' + ver )
                except Exception as e:
                    errorcount += 1
                    raise Exception( 'Failed connecting to SAST with "' + str(e) + '"', True, True, e )
                # Check if THIS user has the required permissions
                cxsastconn.checkpermissions( perm_sast = True, perm_accesscontrol = True, perm_odata = True, perm_audit = False, read_only = True )
                # Check projects filter
                projectsfilter = self.config.value('filter.projects')
                if projectsfilter :
                    cxlogger.verbose( '============================================================' )
                    cxlogger.verbose( 'filter.projects: ' + str(projectsfilter) )
                    projectsfilter = paramfilters.idsfromfilter( projectsfilter, ValidFilter.NumericOdataIds, 'filter.projects' )
                # Create the caches for SAST
                cxlogger.verbose( '============================================================' )
                cxlogger.verbose( 'Creating SAST caches')
                cxsastcaches = sastcache( cxsastconn ) 
                cacheerrorcount = 0
                # Cache class avoids creating duplicated caches, so safe to use
                if 'inventory' in actions :
                    cacheerrorcount += cxsastcaches.createallcaches(projectsfilter = projectsfilter) if cacheerrorcount == 0 else 0
                if 'custom-queries' in actions :
                    cacheerrorcount += cxsastcaches.createcache( sastcachetype.presets ) if cacheerrorcount == 0 else 0 
                    cacheerrorcount += cxsastcaches.createcache( sastcachetype.ac_teams ) if cacheerrorcount == 0 else 0 
                    cacheerrorcount += cxsastcaches.createcache( sastcachetype.queries_all ) if cacheerrorcount == 0 else 0 
                    cacheerrorcount += cxsastcaches.createcache( sastcachetype.queries_custom ) if cacheerrorcount == 0 else 0 
                if 'triages-count' in actions :
                    cacheerrorcount += cxsastcaches.createcache(sastcachetype.result_states) if cacheerrorcount == 0 else 0 
                if 'triages-all' in actions :
                    cacheerrorcount += cxsastcaches.createcache( sastcachetype.queries_all ) if cacheerrorcount == 0 else 0 
                # A projects cache is always needed, so ensure we have at least the simple cache
                if not cxsastcaches.hascache(sastcachetype.projectsfull) :
                    cacheerrorcount += cxsastcaches.createcache( sastcachetype.projectssimple, projectsfilter ) if cacheerrorcount == 0 else 0 
                if cacheerrorcount > 0 :
                    errorcount += cacheerrorcount
                    raise Exception( 'Errors found creating SAST caches' )
                cxlogger.verbose( 'SAST caches created')

                # Dispose of filter after caching, to release resourced
                projectsfilter = None

                # Let's go
                if 'inventory' in actions :
                    runner = sastinventory( self.config, cxsastconn, cxsastcaches )
                    runner.execute()    
                if 'custom-queries' in actions :
                    runner = sastcustomqueries( self.config, cxsastconn, cxsastcaches )
                    runner.execute()
                if 'triages-count' in actions :
                    runner = sastcounttriages( self.config, cxsastconn, cxsastcaches )
                    runner.execute()
                if 'triages-all' in actions :
                    runner = sastalltriages( self.config, cxsastconn, cxsastcaches )
                    runner.execute()

            # -----------------------------------------------------------------
            # CXONE
            # -----------------------------------------------------------------
            if command == 'cxone' :

                # Connect to CXONE instance
                cxsastconn = None
                try :
                    cxlogger.verbose( 'Connecting to CXONE "' + self.config.value('cxone.url') + '"' )
                    cxxoneconn = cxoneconn( self.config.value('cxone.url'), self.config.value('cxone.tenant'), self.config.value('cxone.apikey'), 
                                            self.config.value('cxone.acl'), self.config.value('cxone.clientid'), self.config.value('cxone.granttype'), 
                                            self.config.value('cxone.proxy_url'), self.config.value('cxone.proxy_username'), self.config.value('cxone.proxy_password') )
                    cxxoneconn.logon()
                    ver = cxxoneconn.versionstring
                    if not ver or ver == '0' :
                        raise Exception( 'Cound not obtain cxone version' )
                    cxlogger.verbose( 'Connected to CXONE, version ' + ver )
                except Exception as e:
                    errorcount += 1
                    raise Exception( 'Failed connecting to CXONE with "' + str(e) + '"', True, True, e )
                # Check if THIS user has the required permissions
                cxxoneconn.checkpermissions( perm_cxone = True, perm_accesscontrol = True )
                # Check projects filter
                projectsfilter = self.config.value('filter.projects')
                if projectsfilter :
                    cxlogger.verbose( '============================================================' )
                    cxlogger.verbose( 'filter.projects: ' + str(projectsfilter) )
                    projectsfilter = paramfilters.idsfromfilter( projectsfilter, ValidFilter.StringIds, 'filter.projects' )
                # Create the caches for CXONE
                cxlogger.verbose( '============================================================' )
                cxlogger.verbose( 'Creating CXONE caches')
                cxonecaches = cxonecache( cxxoneconn ) 
                cacheerrorcount = 0
                # Cache class avoids creating duplicated caches, so safe to use
                if 'inventory' in actions :
                    cacheerrorcount += cxonecaches.createallcaches(projectsfilter = projectsfilter) if cacheerrorcount == 0 else 0
                else :
                    cacheerrorcount += cxonecaches.createcache( cxonecachetype.projectsfull, projectsfilter )
                if cacheerrorcount > 0 :
                    errorcount += cacheerrorcount
                    raise Exception( 'Errors found creating CXONE caches' )
                cxlogger.verbose( 'CXONE caches created')

                # Dispose of filter after caching, to release resourced
                projectsfilter = None

                # Lets go
                if 'inventory' in actions :
                    runner = cxoneinventory( self.config, cxxoneconn, cxonecaches )
                    runner.execute()    
                if 'triages-count' in actions :
                    runner = cxonecounttriages( self.config, cxxoneconn, cxonecaches )
                    runner.execute()    
                if 'triages-all' in actions :
                    runner = cxonealltriages( self.config, cxxoneconn, cxonecaches )
                    runner.execute()    

            # -----------------------------------------------------------------
            # SCA
            # -----------------------------------------------------------------
            if command == 'sca' :

                # Connect to SCA instance
                cxscaconn = None
                try :
                    cxlogger.verbose( 'Connecting to SCA "' + self.config.value('sca.url') + '"' )
                    cxscaconn = scaconn( self.config.value('sca.url'), self.config.value('sca.acl'), self.config.value('sca.tenant'), self.config.value('sca.username'), self.config.value('sca.password'), self.config.value('sca.proxy_url'), self.config.value('sca.proxy_username'), self.config.value('sca.proxy_password') )
                    cxscaconn.logon()
                    cxlogger.verbose( 'Connected to SCA' )
                except Exception as e:
                    errorcount += 1
                    raise Exception( 'Failed connecting to SCA with "' + str(e) + '"', True, True, e )
                # Check if THIS user has the required permissions
                cxscaconn.checkpermissions( perm_sca = True, perm_accesscontrol = True )
                # Check projects filter
                projectsfilter = self.config.value('filter.projects')
                if projectsfilter :
                    cxlogger.verbose( '============================================================' )
                    cxlogger.verbose( 'filter.projects: ' + str(projectsfilter) )
                    projectsfilter = paramfilters.idsfromfilter( projectsfilter, ValidFilter.StringIds, 'filter.projects' )
                # Create the caches for SAST
                cxlogger.verbose( '============================================================' )
                cxlogger.verbose( 'Creating SCA caches')
                cxscacaches = scacache( cxscaconn ) 
                cacheerrorcount = 0
                # Cache class avoids creating duplicated caches, so safe to use
                if 'inventory' in actions :
                    cacheerrorcount += cxscacaches.createallcaches(projectsfilter = projectsfilter) if cacheerrorcount == 0 else 0
                else :
                    cacheerrorcount += cxscacaches.createcache( scacachetype.projects, projectsfilter ) if cacheerrorcount == 0 else 0
                if cacheerrorcount > 0 :
                    errorcount += cacheerrorcount
                    raise Exception( 'Errors found creating SCA caches' )
                cxlogger.verbose( 'SCA caches created')

                # Dispose of filter after caching, to release resourced
                projectsfilter = None

                # Lets go
                if 'inventory' in actions :
                    runner = scainventory( self.config, cxscaconn, cxscacaches )
                    runner.execute()    
                if 'triages-count' in actions :
                    runner = scacounttriages( self.config, cxscaconn, cxscacaches )
                    runner.execute()
                if 'triages-all' in actions :
                    runner = scaalltriages( self.config, cxscaconn, cxscacaches )
                    runner.execute()

        except Exception as e:
            cxlogger.verbose( str(e), True, False, True, e )
        finally :
            # Verbose the footer
            dtend = datetime.now()
            cxlogger.verbose( '============================================================' )
            cxlogger.verbose( 'Ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            cxlogger.verbose( '============================================================' )
            cxlogger.verbose( '' )
        

if __name__ == '__main__' :
    application = cxinventory()
    application.execute()

