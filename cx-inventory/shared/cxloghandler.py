""" 
========================================================================

GENERAL GLOBAL CLASS FOR LOG HANDLING

joao.costa@checkmarx.com
PS-EMEA
01-11-2023

========================================================================
"""


import os
import traceback
import threading
from datetime import datetime
from config import config

DEFAULT_LOGS_PATH   = 'logs'

LEVEL_INFO          = 'INFO'
LEVEL_WARNING       = 'WARNING'
LEVEL_ERROR         = 'ERROR'
LEVEL_CRITICAL      = 'CRITICAL'
LEVEL_DEBUG         = 'DEBUG'


cx_global_debug_flag: bool = False


class cxverboseandloghandler(object) :

    def __init__(self) :
        self.__verbose: bool    = False
        self.__lastverbose: str = None
        self.__locker           = threading.RLock()
        self.__logfile          = None
        self.__logactive: bool  = False
        self.__logdebug: bool   = False


    def __del__(self) :
        self.shutdown()
        self.__locker = None


    def activate( self, verbose: bool = True, logging: bool = True, debug: bool = None ) :
        self.__locker.acquire()
        try :
            if verbose :
                self.__verbose = True    
            if logging :
                if self.__logactive :
                    self.__logdebug    = debug
                    return    
                logspath = config.mainrootpath() + os.sep + DEFAULT_LOGS_PATH
                os.makedirs(logspath, exist_ok = True)
                filename = logspath + os.sep + config.mainmodulename() + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.log'
                if not self.__logfile :
                    self.__logfile = open(filename, 'w', encoding='UTF8', newline='', buffering=1)
                self.__logdebug    = debug
                self.__logactive   = True
        finally :
            self.__locker.release()


    def shutdown(self, verbose: bool = True, logging: bool = True ):
        self.__locker.acquire()
        try :
            if verbose :
                self.__verbose = False    
            if logging :
                if self.__logfile :
                    self.__logactive = False
                    self.__logfile.close()
                    self.__logfile = None
                self.__logdebug    = None
                self.__logactive   = False
        finally :
            self.__locker.release()


    def verbose(self, message: str, newline: bool = True, appendline: bool = False, error: bool = False, exception = None, autolog: bool = True ) :
        # Print to screen ?
        self.__locker.acquire()
        try :
            if self.__verbose :
                if (error) :
                    if self.__lastverbose :
                        print( '' )
                    print( 'ERROR: ' + message )
                    self.__lastverbose = None
                elif (newline) :
                    if self.__lastverbose :
                        print( '' )
                    print( message, end = '\r' )
                    self.__lastverbose = message
                else :
                    spaces = ''
                    if appendline and self.__lastverbose:
                        message = self.__lastverbose + message
                    if (self.__lastverbose) and (len(message) < len(self.__lastverbose)) :
                        spaces = ' ' * (len(self.__lastverbose) - len(message))
                    print( message + spaces, end = '\r' )
                    self.__lastverbose = message
        finally :
            self.__locker.release()
        # Write to log
        if message.strip() != '' and autolog :
            if error or exception :
                self.logerror( message, exception )
            else :
                self.loginfo( message, exception )


    def __log( self, message: str, level: str = LEVEL_INFO, exception = None ) :
        self.__locker.acquire()
        try :        
            if not self.__logactive :
                return
            if level == LEVEL_DEBUG and ( self.__logdebug == False or (self.__logdebug == None and not cx_global_debug_flag) ) :
                return
            if message.strip() == '' :
                return
            if not self.__logfile :
                return
            if exception and level == LEVEL_INFO :
                level = LEVEL_ERROR
            if message.lstrip(' ').lstrip('-').lstrip(' ') == '' :
                xtext = message
            else :
                xtext = message.lstrip(' ').lstrip('-').lstrip(' ')
            slogtext = datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' - ' + level + ' - ' + xtext
            self.__logfile.write( slogtext + os.linesep )
            # Has an exception
            if exception :
                try :
                    error_info = traceback.extract_tb(exception.__traceback__, limit=None)
                    if error_info and len(error_info) > 0 :
                        # Write the line    
                        slogtext = datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' - EXCEPTION - '
                        sspaces = ' ' * len(slogtext)
                        self.__logfile.write( slogtext + 'Call stack for "' + str(exception) + '"' + os.linesep )
                        for error_stack in error_info[::-1] :
                            self.__logfile.write( sspaces + '> func: ' + error_stack.name + os.linesep )
                            self.__logfile.write( sspaces + '  line: ' + str(error_stack.lineno) + os.linesep )
                            self.__logfile.write( sspaces + '  code: ' + error_stack.line + os.linesep )
                            self.__logfile.write( sspaces + '  file: ' + error_stack.filename + os.linesep )
                except:
                    pass
        finally :
            self.__locker.release()


    def loginfo( self, message: str, exception = None ) :
        if self.__logactive :
            self.__log( message, LEVEL_INFO, exception )


    def logwarning( self, message: str, exception = None ) :
        if self.__logactive :
            self.__log( message, LEVEL_WARNING, exception )


    def logerror( self, message: str, exception = None ) :
        if self.__logactive :
            self.__log( message, LEVEL_ERROR, exception )


    def logfatal( self, message: str, exception = None ) :
        if self.__logactive :
            self.__log( message, LEVEL_CRITICAL, exception )


    def logcritical( self, message: str, exception = None ) :
        if self.__logactive :
            self.__log( message, LEVEL_CRITICAL, exception )


    def logdebug( self, message: str, exception = None ) :
        if self.__logactive and self.__logdebug:
            self.__log( message, LEVEL_DEBUG, exception )



# Expose global logger (cxlogger)
cxlogger: cxverboseandloghandler = cxverboseandloghandler()