""" 
========================================================================

MERGE TEAM LEVEL QUERIES TO PROJECT OR APPLICATION

antonio.silva@checkmarx.com
PS-EMEA
24-08-2023

========================================================================
"""


import re
from datetime import datetime
from enum import Enum


STATUS_OK           = 0         # All good
STATUS_REMERGE	    = 1         # Detected query code merged before, this is dangerous and must be reported or logged
STATUS_EMPTY        = 8			# No queries to process
STATUS_INVALID 	    = 9			# Invalid content for processing


class cxquerylevel(Enum) :
    querycorp           = 1
    queryteam           = 2
    queryproj           = 3


# Query record
class cxquery(object) :

    def __init__(self, 
                sourcecode: str,
                queryid: int,
                queryname: str,
                language: str,
                packageid: int,
                packagename: str,
                severity: int,
                level: cxquerylevel,
                teamorprojid: int,
                teamorprojname: str ) :
        # External props        
        self.sourcecode         = sourcecode
        self.queryid            = queryid
        self.queryname          = queryname.strip()
        self.language           = language.strip()
        self.packageid          = packageid
        self.packagename        = packagename.strip()
        self.severity           = severity
        self.level              = level
        # self.isproject          = isproject
        self.teamorprojid       = teamorprojid
        self.teamorprojname     = teamorprojname.strip()
        # Internal props
        self.tag: str           = ''
        self.callsbase: bool    = False
        self.issafe: bool       = True
        # Compose the tag
        # Severity
        qseverity = ''
        if self.severity == 0 :
            qseverity = '0 - Info'
        elif self.severity == 1 :
            qseverity = '1 - Low'
        elif self.severity == 2 :
            qseverity = '2 - Medium'
        elif self.severity == 3 :
            qseverity = '3 - High'
        else :
             qseverity = 'Invalid (' +  str(severity) + ')'
        qtag = '// ------------------------------------------------------\n'

        if level == cxquerylevel.querycorp :
            qtag = qtag + "// MERGED - CORPORATE LEVEL\n"
        elif level == cxquerylevel.queryteam :
            qtag = qtag + '// MERGED - TEAM LEVEL\n'
            qtag = qtag + '// TEAM: ' + str(self.teamorprojid) + ' - ' + self.teamorprojname + '\n'
        elif level == cxquerylevel.queryproj :
            qtag = qtag + '// MERGED - PROJECT LEVEL\n'
            qtag = qtag + '// PROJECT: ' + str(self.teamorprojid) + ' - ' + self.teamorprojname + '\n'
        qtag = qtag + '// QUERY: ' + str(self.queryid) + ' - ' + self.queryname + '\n'
        qtag = qtag + '// LANGUAGE: ' + self.language + '\n'
        qtag = qtag + '// PACKAGE: ' + str(self.packageid) + ' - ' + self.packagename + '\n'
        qtag = qtag + '// SEVERITY: ' + qseverity + '\n'
        qtag = qtag + '// TIMESTAMP: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '\n'
        qtag = qtag + "// ------------------------------------------------------\n"
        self.tag = qtag



class querymerger(object) :

    def __init__(self) :
        self.__queries: list[cxquery] = []


    # Append a new query code to the queries list (slice) to be processed
    # All queries in the list must belong to the same vulnerability/language
    # They will be processed top-down
    def add( self, sourcecode: str, queryid: int, queryname: str, language: str, packageid: int, packagename: str, severity: int, level: cxquerylevel, teamorprojid: int, teamorprojname: str ) :
        # Compose the query element
        qqry = cxquery( sourcecode, queryid, queryname, language, packageid, packagename, severity, level, teamorprojid, teamorprojname )
        # Add the query to the list
        self.__queries.append(qqry)


    # Append a new query code to the queries list (slice) to be processed
    # All queries in the list must belong to the same vulnerability/language
    # They will be processed top-down
    def addquery( self, query: cxquery ) :
        # Add the query
        self.__queries.append(query)


    # Insert a new query at the top of the queries list (slice) to be processed
    # All queries in the list must belong to the same vulnerability/language
    # They will be processed top-down
    def insert(self, sourcecode: str, queryid: int, queryname: str, language: str, packageid: int, packagename: str, severity: int, level: cxquerylevel, teamorprojid: int, teamorprojname: str ) :
        # Compose the query element
        qqry = cxquery( sourcecode, queryid, queryname, language, packageid, packagename, severity, level, teamorprojid, teamorprojname )
        # Insert the query to the list
        if len(self.__queries) == 0 :
            self.__queries.append(qqry)
        else :
            self.__queries.insert(0, qqry)


    # Insert a new query at the top of the queries list (slice) to be processed
    # All queries in the list must belong to the same vulnerability/language
    # They will be processed top-down
    def insertquery(self, query: cxquery ) :
        # Ensure queryname and language matched
        if len(self.__queries) > 0 :
            unmatch = next( filter( lambda el: el.queryname != query.queryname, self.__queries), None )
            if unmatch :
                raise Exception("Query name does not match " + self.__queries[0].queryname)
            unmatch = next( filter( lambda el: el.language != query.language, self.__queries), None )
            if unmatch :
                raise Exception("Language does not match " + self.__queries[0].language)
        # Insert the query to the list
        if len(self.__queries) == 0 :
            self.__queries.append(query)
        else :
            self.__queries.insert(0, query)


    # Read from file and append a new query at the end of the list
    def addfromfile( self, sourcefilename: str, queryid: int, queryname: str, language: str, packageid: int, packagename: str, severity: int, level: cxquerylevel, teamorprojid: int, teamorprojname: str ) :
        with open( sourcefilename, 'r' ) as handle :
            sourcecode = handle.read()
        self.add( sourcecode, queryid, queryname, language, packageid, packagename, severity, level, teamorprojid, teamorprojname )


    # Read from file and insert a new query at the top of the list
    def insertfromfile( self, sourcefilename: str, queryid: int, queryname: str, language: str, packageid: int, packagename: str, severity: int, level: cxquerylevel, teamorprojid: int, teamorprojname: str ) :
        with open( sourcefilename, 'r' ) as handle :
            sourcecode = handle.read()
        self.insert( sourcecode, queryid, queryname, language, packageid, packagename, severity, level, teamorprojid, teamorprojname )


    # Clears the list
    def clear(self) :
        self.__time = datetime.now()
        self.__queries = []


    # Get number of queries in the list
    def count(self) :
        return len(self.__queries)
    

    # Removes the last query on the list
    def delete( self ) :
        if len(self.__queries) > 0 :
            self.__queries.pop()


    # Refrieves a query object from list
    def query( self, index: int ) :
        if index < 0 or index > self.count() - 1 :
            raise IndexError( 'Query index out of bounds.')
        return self.__queries[index]
    

    # Gets the last ververity or the highest severity from the queries list
    def severity(self, highest: bool = False) :
        severity = 0
        for qry in self.__queries :
            if (not highest) or (qry.severity > severity) :
                severity = qry.severity
        if severity < 0 or severity > 3 :
            raise IndexError( 'Severity value out of bounds.')
        return severity
    

    def __arrangecode( self, sourcecode: str, commented: bool ) :
        if not sourcecode.strip() :
            return ''
        else :
            xlines = sourcecode.strip(' \n').splitlines()
            data = ''
            for line in xlines :
                if commented :
                    data = data + '\t' + '//NO-BASE//\t ' + line + '\n'
                else :
                    data = data + '\t' + line + '\n'
            return data


    # Removes comments from code using regex
    # This code is safe, user imput is not in play here
    def __uncommentedcode( self, qcode ) :
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " " # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        return re.sub(pattern, replacer, qcode)


    # Find word in an array of words, private
    def __wordindex(self, words: list[str], word: str, prefixed: bool) :
        i = 0
        for w in words :
            if prefixed :
                if w.startswith(word) :
                    return i
            elif w == word :
                return i
            i += 1
        return -1


    # Check if the code calls base.<queryname> in a recongized way, private
    def __codecallsbase( self, sourcecode: str, qname: str) :
        callsbase       = False
        issafe          = True
        uncommented     = self.__uncommentedcode(sourcecode)
        thebase         = 'base.' + qname + '()'
        # Check base invocation
        callsbase = thebase in uncommented
        # Check for assignments that will indicate danger suggesting code needs fix or manual review
        # Such as assignement to a variable that is not "result"
        # The patterns recognized as VALID are:
        #   result = base.<queryname>
        #   result= base.<queryname>
        #   result =base.<queryname>
        #   result=base.<queryname>
        if callsbase :
            found = 'result=' + thebase in uncommented
            if not found :
                pos = uncommented.find(thebase) + len(thebase) + 10
                xtext = uncommented[0:pos]
                # Remove unwanted escaped chars
                xtext = xtext.replace( '\n', ' ' )
                xtext = xtext.replace( '\r', ' ' )
                xtext = xtext.replace( '\t', ' ' )
                xtext = xtext.replace( '\b', ' ' )
                words = xtext.split()
                pos = self.__wordindex(words, thebase, True)
                # Check for direct assignment
                found = ((pos >= 2) and (words[pos-2] == 'result') and (words[pos-1] == '=')) or ((pos >= 1) and (words[pos-1] == 'result='))
                if not found :
                    pos = 0
                    while pos < len(words) - 1 and not found :
                        found = words[pos] == 'result' and words[pos+1].startswith('=' + thebase)
                        pos += 1
            if not found :
                issafe = False
        return callsbase, issafe
    

    # Validate that query chain is correct
    def __validate_queries_struct(self) :
        status: int         = STATUS_OK
        message: str        = ''
        queryremerge: bool  = False
        queryname: str
        querylang: str
        queryteam: str

        # No queries to process
        if len(self.__queries) == 0 :
            message = 'Cannot process an empty set of queries'
            status = STATUS_EMPTY
            return status, message
        
        queryname = self.__queries[0].queryname
        querylang = self.__queries[0].language
        queryteam = self.__queries[0].teamorprojname

	    # Detect if this query is a remerge
        if ('// MERGED - CORPORATE LEVEL\n' in self.__queries[0].sourcecode) or ('// MERGED - TEAM LEVEL\n' in self.__queries[0].sourcecode) or ('// MERGED - PROJECT LEVEL\n' in self.__queries[0].sourcecode) :
            queryremerge = True

        # If only one query, we can go
        if len(self.__queries) == 1 :
            # Query severity must be between 0 and 3
            if self.__queries[0].severity < 0 or self.__queries[0].severity :
                return STATUS_INVALID, 'Query severity out of range'
            elif queryremerge :
                return STATUS_REMERGE, ''
            else :
                return STATUS_OK, ''
            
        # Verify the chain
        i = 0
        for query in self.__queries :
            i += 1
    		# Query name must be the same
            if not (query.queryname == queryname) :
                return STATUS_INVALID, 'Query name must be the same'
            # Query language must be the same
            if not (query.language == querylang) :
                return STATUS_INVALID, 'Query language must be the same'
            # Query severity must be between 0 and 3
            if query.severity < 0 or query.severity > 3 :
                return STATUS_INVALID, 'Query severity out of range'
            # Corp level queries can't be used in aggregation
            if query.level == cxquerylevel.querycorp :
                return STATUS_INVALID, 'Corp level queries cannot be merged'
    		# Project level query in aggregation must be unique and the last on the list	
            if query.level == cxquerylevel.queryproj and i < len(self.__queries) :
                return STATUS_INVALID, 'Project level query must be the last on the list'
            # Check team sequence
            if query.level == cxquerylevel.queryteam :
                if query.teamorprojname.startswith(queryteam) :
                    queryteam = query.teamorprojname
                else :
                    return STATUS_INVALID, 'Team level query not in same tree hierachy'

        if queryremerge :
            return STATUS_REMERGE, ''
        else :    
            return STATUS_OK, ''
        


    def __merge_queries( self, destqueryname: str = '') :
        status          = STATUS_OK
        statusmessage   = ''
        result          = ''
        xdestqueryname  = ''
        querycount      = 0
        index           = 0
        firstindex      = 0
        extratag        = ''
        querycode       = ''


        # Precheck status
        status, statusmessage = self.__validate_queries_struct()

        # Check we have some queries
        if len(self.__queries) == 0 :
            result = ''
            status = STATUS_EMPTY
            return result, status, statusmessage

        # Get query name from first query
        xqueryname = self.__queries[0].queryname
        xdestqueryname = destqueryname
        if destqueryname == '' :
            xdestqueryname = xqueryname

        # If only one query, aggegation and identation are not needed
        if len(self.__queries) == 1 :
            querycode = self.__queries[0].sourcecode
            # If query name changed, must ensure the right base.<newname> is being called/referred
            if not xqueryname == xdestqueryname :
                extratag = extratag + '// QUERY RENAMED FROM ' + xqueryname + ' TO ' + xdestqueryname + '\n'
                extratag = extratag + '// ------------------------------------------------------\n'
                querycode = querycode.replace('base.' + xqueryname + '()', 'base.' + xdestqueryname + '()')
            result = self.__queries[0].tag + extratag + "\n" + querycode +"\n"
            status = STATUS_OK
            return result, status, statusmessage

        # Analyse the code for
        # - Broken chain, base.<queryname> not called
        # - Unhandled code, base.<queryname> is not assigned to "result" directly
        index = 0
        for qry in self.__queries :
            qry.callsbase, qry.issafe = self.__codecallsbase(qry.sourcecode, qry.queryname)
            if not qry.callsbase :
                firstindex = index
            index += 1

        # Inject code fixes into the queries
        for qry in self.__queries :
            extratag    = ''
            querycode   = qry.sourcecode
            if not result == '' :
                result = result + '\n\n\n'
            # If query name changed, must ensure the right base.<newname> is being called/referred
            if not xqueryname == xdestqueryname :
                extratag = extratag + '// QUERY RENAMED FROM ' + xqueryname + ' TO ' + xdestqueryname + '\n'
                querycode = querycode.replace('base.' + xqueryname + '()', 'base.' + xdestqueryname + '()')
            # Fixes are not relevant for the first query in the chain. Only for the next
            if querycount >= firstindex :
                if not qry.callsbase :
                    extratag = "// BASE CALL CHAIN BROKEN - QUERY DOES NOT CALL BASE\n"
                elif not qry.issafe :
                    extratag = "// DIRECT RESULT ASSIGNMENT UNDETECTED - result = base.<x> \n"
            if not extratag == '' :
                extratag = extratag + '// ------------------------------------------------------\n'

            # Now check fixes
            if querycount > firstindex :
                if not qry.callsbase :
                    queryinject = '\n'
                    queryinject = queryinject + '// ---------- >> AUTO ADDED BY MERGE\n'
                    queryinject = queryinject + 'result.Clear();\n'
                    queryinject = queryinject + '// << ---------- AUTO ADDED BY MERGE\n\n'
                    querycode = queryinject + querycode
                elif not qry.issafe :
                    sbase = 'base.' + qry.xdestqueryname + '()'
                    xbase = '_merged_base_' + qry.xdestqueryname
                    xcounter = 0
                    xresult = xbase
                    while querycode.find(xresult) >= 0 :
                        xcounter += 1
                        xresult = xbase + str(xcounter)
                    # Inject the fix in the code ...
                    querycode = querycode.replace(sbase, xresult)
                    queryinject = '\n'
                    queryinject = queryinject + '// ---------- >> AUTO ADDED BY MERGE\n'
                    queryinject = queryinject + 'CxList ' + xresult + ' = result.Clone();\n'
                    queryinject = queryinject + 'result.Clear();\n'
                    queryinject = queryinject + '// << ---------- AUTO ADDED BY MERGE\n\n'
                    querycode = queryinject + querycode
                else :
                    sbase = 'base.' + xdestqueryname + '()'
                    querycode = querycode.replace(sbase, 'result')

            result = result + qry.tag + extratag + '{\n' + self.__arrangecode(querycode, (querycount < firstindex))  + '\n}'
            querycount += 1

        return result, status, statusmessage


    # Merge the list of queries int a singe code
    # Returns:
    # - qcode		the merged query code
    # - status		the status of the merged query 
    def merge(self, destqueryname: str = '') :
        xstatus         = STATUS_OK
        xstatusmessage  = ''
        xresult         = ''
        xresult, xstatus, xstatusmessage = self.__merge_queries( destqueryname )
        if xstatus > STATUS_REMERGE :
            raise Exception( xstatusmessage )
        return xresult, xstatus


    # Helper funtion to check the contents
    def checkstatus(self) :
        xstatus: int
        xstatusmessage: str
        xstatus, xstatusmessage = self.__validate_queries_struct()
        return xstatus, xstatusmessage


    # Helper funtion to get CxQL code without comments
    # It does not check for errors, just deliver the uncommented code
    def uncommentedcode(self) :
        xstatus         = STATUS_OK
        xstatusmessage  = ''
        xresult         = ''
        xresult, xstatus, xstatusmessage = self.__merge_queries( '' )
        if not xresult == '' :
            xresult = self.__uncommentedcode(xresult)
        return xresult
