""" 
========================================================================

BASE CLASS FOR RUNNERS AND PRODUCERS

Contains base shared code

joao.costa@checkmarx.com
PS-EMEA
01-07-2023

========================================================================
"""



import os
import sys
import csv
import traceback
import locale
from datetime import datetime
from config import config
from cxloghandler import cxlogger
from version import version


# DATA/LOGS LOCATION SUB-FOLDERS
LOGS_FOLDER             = 'logs'
DATA_FOLDER             = 'data'


class baserunner(object) :

    def __init__(self) :
        self.__config       = None      # Configuration file
        self.__conn         = None      # Connection object
        self.__caches       = None      # Caches object
        self.__csvseparator = ','
        self.__verbose      = None
        # Internals
        self.__privatelogs  = False


    def __init__(self, config: config = None, conn = None, caches = None, verbose = None, csvseparator = None) :
        self.__config       = config
        self.__conn         = conn      
        self.__caches       = caches    
        self.__csvseparator = csvseparator
        self.__verbose      = verbose
        # Internals
        self.__privatelogs  = False


    @property
    def csvseparator(self) :
        # Detect csvseparator if not set, from locale and decimal separator
        if not self.__csvseparator :
            self.__csvseparator = ','
            loc = locale.getlocale()  # get current locale
            locale.setlocale(locale.LC_ALL, '')     # assign OS locale
            decsep = locale.localeconv()["decimal_point"]
            locale.setlocale(locale.LC_ALL, loc)    # restore saved locale
            if decsep == ',' :
                self.__csvseparator = ';'
        return self.__csvseparator


    # Returns the data as a list and optionally the colunm names (header) as list
    def csvload( self, csvfile, returnheaderslist: bool = False ) :
        csvdata = []
        if not os.path.exists(csvfile) :
            raise Exception( 'File not found "' + csvfile + '"')
        csvfilehandler  = open(csvfile, 'r', encoding='UTF8', newline='')
        try :
            csvfilereader   = csv.reader( csvfilehandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            firstrow = True
            columns = None
            for csvrow in csvfilereader :
                if firstrow :
                    firstrow = False
                    columns = csvrow        
                else :
                    row = {}
                    colcount = len(columns)
                    colid    = 0
                    while (colid < colcount) :
                        xkey = columns[colid]
                        if colid < len(csvrow) :
                            xval = csvrow[colid]
                            if xval.isdecimal() :
                                xval = int(xval)
                            elif xval.isnumeric() :
                                xval = float(xval)
                            elif xval.lower() == 'true' :
                                xval = True
                            elif xval.lower() == 'false' :
                                xval = False
                            elif not xval :
                                xval = None
                        else :
                            xval = None
                        row[xkey] = xval
                        colid += 1
                    csvdata.append(row)
            # if csvheaderslist :
            #     csvheaderslist = columns
        finally :
            csvfilehandler.close()
        if returnheaderslist :
            return csvdata, columns
        else :
            return csvdata
    

    def csvsave( self, csvfile, data, csvheaderslist = None ) :
        if os.path.exists(csvfile) :
            os.remove(csvfile)
        if not data :
            return
        if (type(data) is list) and len(data) == 0 :
            return
        # Detect headers if not supplyed
        csvheaders = csvheaderslist
        if not csvheaders :
            row = data[0]
            if (type(row) is dict) :
                csvheaders = list(row.keys())
        # Go for it
        filehandler = open(csvfile, 'w', encoding='UTF8', newline='')
        try :
            filewriter = csv.writer(filehandler, delimiter = self.csvseparator, quotechar = '"', doublequote = True, skipinitialspace = True, lineterminator = '\r\n' )
            # If we do not have headers, just dump
            if not csvheaders :
                if (type(data) is list) :
                    for row in data :
                        filewriter.writerow(row)
            else :
                filewriter.writerow(csvheaders)
                for row in data :
                    xrow = []
                    for key in csvheaders :
                        xrow.append( row[key])
                    filewriter.writerow( xrow )
        finally :
            filehandler.close()    


    def loadconfig( self, defaults = None, defaultname = None ) :
        if defaultname :
            self.__config = config(defaults = defaults, defaultname = defaultname)
        else :
            self.__config = config(defaults = defaults)
        self.__config.putvalue( 'version', version['version'])
        self.__verbose = self.__config.value('verbose') or self.__config.hascommand('verbose')
        if self.__config.value('help') or self.__config.value('h') or self.__config.hascommand('help') or self.__config.hascommand('h') :
            self.printhelp()
            sys.exit(0)
        return self.__config


    @property
    def config(self) :
        if not self.__config :
            raise Exception( 'A config object has not been set' )
        return self.__config


    @property
    def conn(self) :
        if not self.__conn :
            raise Exception( 'A connection object has not been set' )
        return self.__conn
    

    @property 
    def caches(self) :
        if not self.__caches :
            raise Exception( 'A cache object has not been set' )
        return self.__caches
    

    @property
    def verbose(self) :
        return self.__verbose
  

    def cache(self, cachetype ) :
        if not self.__caches :
            raise Exception( 'A cache object has not been set' )
        return self.__caches.cache(cachetype)


    def cacheoneof(self, cachetypes: list ) :
        if not self.__caches :
            raise Exception( 'A cache object has not been set' )
        return self.__caches.cacheoneof(cachetypes)


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


    # Helper: set the higher status, statuses are integers
    def setstatus(self, currentstatus, newstatus ) :
        status = currentstatus
        if newstatus > currentstatus :
            status = newstatus
        return status


    # Override as needed
    def logspath(self) :
        logspath = self.__config.mainrootpath()
        if LOGS_FOLDER :
            logspath = logspath + os.sep + LOGS_FOLDER
        os.makedirs(logspath, exist_ok = True)
        return logspath


    # Override as needed
    def datapath(self) :
        datapath = self.__config.mainrootpath()
        if DATA_FOLDER :
            datapath = datapath + os.sep + DATA_FOLDER
        os.makedirs(datapath, exist_ok = True)
        return datapath


    # Override as needed
    def printhelp(self) :
        return None


    # Override this
    def execute(self) :
        return None
