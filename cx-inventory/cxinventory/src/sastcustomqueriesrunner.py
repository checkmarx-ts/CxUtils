""" 
========================================================================

SAST DATA EXTRACTOR CUSTOM QUERIES PRODUCER

joao.costa@checkmarx.com
PS-EMEA
03-07-2023

========================================================================
"""

import os
import csv
from datetime import datetime
from config import config
from cxloghandler import cxlogger
from baserunner import baserunner
from sastcache import sastcachetype



# Query types
OBJ_QUERIES_CORP        = 'CUSTOM-QUERIES-CORP'
OBJ_QUERIES_TEAM        = 'CUSTOM-QUERIES-TEAM'
OBJ_QUERIES_PROJ        = 'CUSTOM-QUERIES-PROJ'

# Max query text size for excel cells
MAX_QUERY_SIZE          = 32500  

# CSV output files
OUT_QUERIES             = 'sast_customqueries.csv'

# CSV file headers
CSV_QUERIES             = [ 'QUERY-TYPE', 'ID', 'KIND', 'ORIGINAL', 'NAME', 'LANGUAGE', 'GROUP', 'VERSION', 'SEVERITY', 
                           'CWE', 'CATEGORIES-COUNT', 'PROJECTS-AFFECTED', 'PRESETS-AFFECTED',
                           'PROJECT-ID', 'PROJECT-NAME',
                           'TEAM-ID', 'TEAM-NAME', 'PARENTS', 'DEPENDANTS', 'INDIRECT-PROJECTS',
                           'SOURCE-CODE' ]


class sastcustomqueries(baserunner) :

    def __init__(self):
        # Well known file for csv containing queries
        self.__queryhandler = None
        self.__queryswriter = None
        super().__init__



    def __init__(self, config: config, conn = None, caches = None, verbose = None, csvseparator = None) :
        # Well known file for csv containing queries
        self.__queryhandler = None
        self.__queryswriter = None
        super().__init__(config, conn, caches, verbose, csvseparator)    



    def preparedatafiles(self) :
        try :
            filename = self.datapath() + os.sep + OUT_QUERIES
            if os.path.exists(filename) :
                os.remove(filename)
            self.__queryshandler = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
            self.__queryswriter = csv.writer(self.__queryshandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            self.__queryswriter.writerow(CSV_QUERIES)
            return True
        except Exception as e:
            cxlogger.verbose( 'Unable to create output files with "' + str(e) + '"', True, False, True, e )    
            self.closedatafiles()
            return False



    def closedatafiles(self) :
        if (self.__queryshandler):
            self.__queryshandler.close()



    def extract_custom_queries_corp(self) :
        cachedata = list(filter(lambda el: el['PackageType'] == 'Corporate', self.cache(sastcachetype.queries_custom)))
        allqueries = self.cache(sastcachetype.queries_all)
        SOBJECT = OBJ_QUERIES_CORP
        errorcount = 0
        inventory_name = 'custom queries corporate level'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            for item in cachedata :
                overriden = True
                queryid = item['QueryId']
                lang = item['LanguageName']
                # Find original query
                oqry = next( filter( lambda el: el['Name'] == item['Name'] and el['LanguageName'] == item['LanguageName'] and el['PackageType'] not in ['Corporate', 'Team', 'Project'], allqueries ), None )
                if oqry :
                    basequery = oqry['QueryId']
                else :
                    basequery = queryid
                    overriden = False
                # Presets using
                presetids = []
                presetusing = list( filter( lambda el: basequery in el['queryIds'], self.cache(sastcachetype.presets) ) )
                for preset in presetusing :
                    presetids.append( preset['id'])
                # Projects using                
                projusing   = list( filter( lambda el: lang in el['sortedlanguages'] and el['presetId'] in presetids, self.cacheoneof([sastcachetype.projectssimple, sastcachetype.projectsfull])) )

                # Excel cell text max size control, 32767 chars per cell
                xsource: str = item['Source']
                if len(xsource) > MAX_QUERY_SIZE :
                    xsource = xsource[:MAX_QUERY_SIZE] + ' ... '   

                self.__queryswriter.writerow( [
                    SOBJECT,
                    queryid,
                    'Override' if overriden else 'New',
                    basequery if overriden else None,
                    item['Name'],
                    item['LanguageName'],
                    item['GroupName'],
                    item['QueryVersionCode'],
                    item['Severity'],
                    item['Cwe'],
                    len(item['Categories']) if item['Categories'] else None,
                    len(projusing) if len(projusing) > 0 else None,                 # Direct project count
                    len(presetusing) if len(presetusing) > 0 else None,           # Direct preset count
                    None,                       # Project-id
                    None,                       # Project-name
                    None,                       # Team-id
                    None,                       # Team-name
                    None,                       # Teams-in-chain
                    None,                       # Teams-dependant
                    None,                       # Indirect projects affected
                    xsource
                ] )

            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount
    


    def extract_custom_queries_team(self) :
        cachedata = list(filter(lambda el: el['PackageType'] == 'Team', self.cache(sastcachetype.queries_custom)))
        allqueries = self.cache(sastcachetype.queries_all)
        SOBJECT = OBJ_QUERIES_TEAM
        errorcount = 0
        inventory_name = 'custom queries team level'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )
        try :
            for item in cachedata :
                overriden = True
                queryid = item['QueryId']
                lang = item['LanguageName']
                # Find original query
                oqry = next( filter( lambda el: el['Name'] == item['Name'] and el['LanguageName'] == item['LanguageName'] and el['PackageType'] not in ['Corporate', 'Team', 'Project'], allqueries ), None )
                if oqry :
                    basequery = oqry['QueryId']
                else :
                    basequery = queryid
                    overriden = False
                # Resolve team
                teamid = item['OwningTeam']
                teamname = ''
                team = next(filter(lambda el: el['id'] == teamid, self.cache(sastcachetype.ac_teams)), None)
                if team :
                    teamname = team['fullName']

                # Resolve parent teams (upwards)
                parents = []
                par_teams = []
                if teamname :
                    xteams = teamname[1:].split('/')
                    xteams = xteams[:-1]
                    steam = ''
                    teams = []
                    for xteam in xteams :
                        steam = steam + '/' + xteam
                        teams.append(steam)
                        xparteams = list( filter( lambda el: el['LanguageName'] == lang and el['Name'] == item['Name'] and el['OwningTeamName'] in teams, cachedata ) )
                        for xparteam in xparteams :
                            par_teams.append(xparteam['OwningTeam'])
                    parents = list( filter( lambda el: el['LanguageName'] == lang and el['Name'] == item['Name'] and el['OwningTeam'] in par_teams, cachedata ) )
                    
                # Resolve dependant teams (downwards)
                dependants = []
                sub_teams = []
                if teamname :
                    xsubteams = list(filter(lambda el: el['fullName'].startswith(teamname + '/'), self.cache(sastcachetype.ac_teams) ))
                    for xsubteam in xsubteams :
                        sub_teams.append(xsubteam['id'])
                    dependants = list( filter( lambda el: el['LanguageName'] == lang and el['Name'] == item['Name'] and el['OwningTeam'] in sub_teams, cachedata ) )

                # Presets using
                presetids = []
                presetusing = list( filter( lambda el: basequery in el['queryIds'], self.cache(sastcachetype.presets) ) )
                for preset in presetusing :
                    presetids.append( preset['id'])
                # Projects using direcly
                projusing   = list( filter( lambda el: lang in el['sortedlanguages'] and el['teamId'] == teamid and el['presetId'] in presetids, self.cacheoneof([sastcachetype.projectssimple, sastcachetype.projectsfull])) )
                # Projects using indirectly
                projindirect  = list( filter( lambda el: lang in el['sortedlanguages'] and el['teamId'] in sub_teams and el['presetId'] in presetids, self.cacheoneof([sastcachetype.projectssimple, sastcachetype.projectsfull])) )

                # Excel cell text max size control, 32767 chars per cell
                xsource: str = item['Source']
                if len(xsource) > MAX_QUERY_SIZE :
                    xsource = xsource[:MAX_QUERY_SIZE] + ' ... '                   

                self.__queryswriter.writerow( [
                    SOBJECT,
                    queryid,
                    'Override' if overriden else 'New',
                    basequery if overriden else None,
                    item['Name'],
                    item['LanguageName'],
                    item['GroupName'],
                    item['QueryVersionCode'],
                    item['Severity'],
                    item['Cwe'],
                    len(item['Categories']) if item['Categories'] else None,
                    len(projusing) if len(projusing) > 0 else None,             # Direct project count
                    len(presetusing) if len(presetusing) > 0 else None,           # Direct preset count
                    None,                       # Project-id
                    None,                       # Project-name
                    teamid,                     # Team-id
                    teamname,                   # Team-name
                    len(parents) if len(parents) > 0 else None,               # Teams-in-chain
                    len(dependants) if len(dependants) > 0 else None,            # Teams-dependant
                    len(projindirect) if len(projindirect) > 0 else None,          # Indirect projects affected
                    xsource
                ] )

            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
        except Exception as e:
            errorcount += 1
            cxlogger.verbose( '  - Processing ' + inventory_name + ' failed with "' + str(e) + '"', True, False, True, e )
        return errorcount



    def extract_custom_queries_proj(self) :
        cachedata = list(filter(lambda el: el['PackageType'] == 'Project', self.cache(sastcachetype.queries_custom)))
        allqueries = self.cache(sastcachetype.queries_all)
        SOBJECT = OBJ_QUERIES_PROJ
        errorcount = 0
        inventory_name = 'custom queries project level'
        dtini = datetime.now()
        cxlogger.verbose( '  - Processing ' + inventory_name )

        try :
            for item in cachedata :
                overriden = True
                queryid = item['QueryId']
                lang = item['LanguageName']
                projid = item['ProjectId']
                projname = None
                # Find original query
                oqry = next( filter( lambda el: el['Name'] == item['Name'] and el['LanguageName'] == item['LanguageName'] and el['PackageType'] not in ['Corporate', 'Team', 'Project'], allqueries ), None )
                if oqry :
                    basequery = oqry['QueryId']
                else :
                    basequery = queryid
                    overriden = False
                # Presets using
                presetids = []
                presetusing = list( filter( lambda el: basequery in el['queryIds'], self.cache(sastcachetype.presets) ) )
                for preset in presetusing :
                    presetids.append( preset['id'])
                # Projects using   
                projusing   = list( filter( lambda el: lang in el['sortedlanguages'] and el['id'] == projid and el['presetId'] in presetids, self.cacheoneof([sastcachetype.projectssimple, sastcachetype.projectsfull])) )
                if len(projusing) > 0 :
                    projname = projusing[0]['name']

                # Excel cell text max size control, 32767 chars per cell
                xsource: str = item['Source']
                if len(xsource) > MAX_QUERY_SIZE :
                    xsource = xsource[:MAX_QUERY_SIZE] + ' ... '                    

                self.__queryswriter.writerow( [
                    SOBJECT,
                    queryid,
                    'Override' if overriden else 'New',
                    basequery if overriden else None,
                    item['Name'],
                    item['LanguageName'],
                    item['GroupName'],
                    item['QueryVersionCode'],
                    item['Severity'],
                    item['Cwe'],
                    len(item['Categories']) if item['Categories'] else None,
                    len(projusing) if len(projusing) > 0 else None,             # Direct project count
                    len(presetusing) if len(presetusing) > 0 else None,           # Direct preset count
                    projid,                     # Project-id
                    projname,                   # Project-name
                    None,                       # Team-id
                    None,                       # Team-name
                    None,                       # Teams-in-chain
                    None,                       # Teams-dependant
                    None,                       # Indirect projects affected
                    xsource
                ] )

            # Close
            cxlogger.verbose('  - Processed ' + inventory_name + ' (' + str(len(cachedata)) + ') ' + self.duration(dtini, True), False )
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
            cxlogger.verbose( 'Extracting custom queries from SAST' )            
            cxlogger.verbose( 'Extraction started: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Processing all sast custom queries')    
            # Custom queries
            errorcount += self.extract_custom_queries_corp() if errorcount == 0 else 0
            errorcount += self.extract_custom_queries_team() if errorcount == 0 else 0
            errorcount += self.extract_custom_queries_proj() if errorcount == 0 else 0
            # Done
            cxlogger.verbose( 'Sast custom queries processed' )
        finally :
            dtend = datetime.now()
            cxlogger.verbose( '------------------------------------------------------------' )
            cxlogger.verbose( 'Extraction ended: ' + dtend.strftime('%d-%m-%Y %H:%M:%S') )
            cxlogger.verbose( 'Total duration: ' + self.duration(dtini, False) )
            if errorcount > 0 :
                cxlogger.verbose( str(errorcount) + ' errors were found.' )    
            self.closedatafiles()


