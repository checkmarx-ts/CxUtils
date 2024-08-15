""" 
========================================================================

PROCESS IDS FROM FILE FILTERS

antonio.silva@checkmarx.com
PS-EMEA
24-08-2023

========================================================================
"""

import os
import string
from enum import Enum

class ValidFilter(Enum) :
    NumericIds          = 0
    NumericOdataIds     = 1
    StringIds           = 2
    StringNames         = 3
    NumericIdsOrNames   = 4

# All methods are class methods. An instance is not needed

class paramfilters(object) :

    # Processes a expression with external files option
    @classmethod
    def idsfromfilter( self, filter, validator: ValidFilter = None, filtername: str = None ) :
        xfilter = filter
        if filter and isinstance(filter, str) and filter.strip().startswith('@') :
            xfilename = filter[1::].strip()
            if xfilename :
                xfilter = paramfilters.idsfromfile( xfilename )
        if validator :
            paramfilters.validatefilter( xfilter, validator, filtername )
        return xfilter


    # Loads filter elements from an external file into a list
    @classmethod
    def idsfromfile( self, filename, validator: ValidFilter = None, filtername: str = None ) :
        if not os.path.exists(filename) :
            raise Exception( 'Params file not found "' + filename + '"')
        if not os.path.isfile(filename) :
            raise Exception( 'Params file is not a valid file "' + filename + '"')
        data = []        
        with open( filename, 'r' ) as pfile :
            lines = pfile.readlines()
        for line in lines :
            xline = line.replace('[', '')
            xline = xline.replace(']', '')
            xline = xline.replace(';', ',')
            for token in xline.split(',') :
                xval = token.strip()
                if xval :
                    if xval.isdigit():
                        data.append(int(xval))
                    else :
                        data.append(xval)
        data = list(set(data))
        if validator  :
            paramfilters.validatefilter( data, validator, filtername )
        if len(data) > 0 :
            return data
        else :
            return None


    # Checks if a filter expression is valid and throws an error if it is not
    @classmethod
    def validatefilter( self, xfilter, validator: ValidFilter = None, filtername: str = None ) :
        if not xfilter or not validator :
            return
        isvalid = True
        message = ''
        stringidsvalidchars = '-' + string.digits + string.ascii_letters
        # Special case:
        # - Goes to NumericIds or StringNames
        if validator == ValidFilter.NumericIdsOrNames :
            if isinstance(xfilter, list) :
                if len(xfilter) == 0 :
                    isvalid = False
                    message = 'filter list of ids is empty'
                else :
                    if isinstance(xfilter[0], int) or xfilter[0].strip().isdigit() :
                        validator = ValidFilter.NumericIds
                    else  :
                        validator = ValidFilter.StringNames
            else :
                if isinstance(xfilter, int) or xfilter.strip().isdigit() :
                    validator = ValidFilter.NumericIds
                else  :
                    validator = ValidFilter.StringNames
        # Numeric ids can be:
        # - a single number
        # - an array of numbers
        if validator == ValidFilter.NumericIds :
            if isinstance(xfilter, list) :
                if len(xfilter) == 0 :
                    isvalid = False
                    message = 'filter list of ids is empty'
                else :
                    textel = next( filter( lambda el: not isinstance(el,int), xfilter ), None )
                    if textel :
                        isvalid = False
                        message = 'filter list of ids must contain only numbers'
            elif isinstance(xfilter, str) :
                isvalid = xfilter.strip().isdigit()
                if not isvalid :
                    message = 'filter id is not a number'
            elif not isinstance(xfilter, int) :
                isvalid = False
                message = 'filter id is not a number'
        # Odata numeric ids can be:
        # - a single number
        # - an array of numbers
        # - greater than >number
        # - greater than or equal >=number
        # - smaller than <number
        # - smaller or equal <=number
        # - equals a number =number or ==number
        if validator == ValidFilter.NumericOdataIds :
            if isinstance(xfilter, list) :
                if len(xfilter) == 0 :
                    isvalid = False
                    message = 'filter list of ids is empty'
                else :
                    textel = next( filter( lambda el: not isinstance(el,int), xfilter ), None )
                    if textel :
                        isvalid = False
                        message = 'filter list of ids must contain only numbers'
            elif isinstance(xfilter, str) :
                temp = xfilter.strip()
                xval = ''
                if temp.startswith('>') or temp.startswith('<') or temp.startswith('=') :
                    xval = temp[1:].strip()
                elif temp.startswith('>=') or temp.startswith('<=') or temp.startswith('==') :
                    xval = temp[2:].strip()
                else :
                    xval = temp
                isvalid = xval.isdigit()
                if not isvalid :
                    message = 'filter id is not a number'
            elif not isinstance(xfilter, int) :
                isvalid = False
                message = 'filter id is not a number'
        # String ids can be:
        # - a single unspaced string (usually guid)
        # - an array of unspaced strings (usually guid)
        if validator == ValidFilter.StringIds :
            if isinstance(xfilter, list) :
                if len(xfilter) == 0 :
                    isvalid = False
                    message = 'filter list of ids is empty'
                else :
                    textel = next( filter( lambda el: not isinstance(el,str) or any(char not in stringidsvalidchars for char in el), xfilter ), None )
                    if textel :
                        isvalid = False
                        message = 'filter list of ids contains invalid values'
            if isinstance(xfilter, str) :
                isvalid = not any(char not in stringidsvalidchars for char in xfilter)
                if not isvalid :
                    message = 'filter id value is invalid'
            elif isinstance(xfilter, int) :
                isvalid = False
                message = 'filter cannot be a number'
        # String names can be anything:
        # - a single string
        # - an array of strings
        if validator == ValidFilter.StringNames :
            if isinstance(xfilter, list) :
                if len(xfilter) == 0 :
                    isvalid = False
                    message = 'filter list of values is empty'
            else :
                if str(xfilter).strip() == '' :
                    isvalid = False
                    message = 'filter value is empty'
        # Verify and throw error
        if not isvalid :
            if not message :
                message = 'invalid filter'
            if filtername :
                message = filtername + ': ' + message
            raise Exception(message)


    # Converts a filter into a list of values
    @classmethod
    def processfilter( self, xfilter, stripstrings: bool = False ) :
        pfilter = []
        if xfilter :
            if isinstance(xfilter, list):
                pfilter = xfilter
            elif isinstance(xfilter, str) :
                pfilter.append(xfilter)
            elif isinstance(xfilter, int) :
                pfilter.append(xfilter)
        if len(pfilter) > 0 :
            if stripstrings :
                for xvalue in pfilter :
                    if isinstance(xvalue, str) :                    
                        xvalue = xvalue.strip()
            return pfilter
        else :
            return None


    # Converts a filter into an ODATA filter if filter is not a list
    @classmethod
    def processodatafilter( self, xfilter, odatafield: str ) :
        pfilter = ''
        pfilterlist = False
        if not odatafield :
            odatafield = 'Id'       # Defaults to SAST projects Id field (should not be)
        if xfilter :
            if isinstance(xfilter, list):
                pfilterlist = True
            elif isinstance(xfilter, str) :
                xfilter = xfilter.strip()
                if xfilter.startswith('>') :
                    pfilter = '&$filter=' + odatafield + ' gt ' + xfilter[1:].strip()
                elif xfilter.startswith('>=') :
                    pfilter = '&$filter=' + odatafield + ' ge ' + xfilter[2:].strip()
                elif xfilter.startswith('<') :
                    pfilter = '&$filter=' + odatafield + ' lt ' + xfilter[1:].strip()
                elif xfilter.startswith('<=') :
                    pfilter = '&$filter=' + odatafield + ' le ' + xfilter[2:].strip()
                elif xfilter.startswith('=') :
                    pfilter = '&$filter=' + odatafield + ' eq ' + xfilter[1:].strip()
                elif xfilter.startswith('==') :
                    pfilter = '&$filter=' + odatafield + ' eq ' + xfilter[2:].strip()
                else :
                    pfilter = str('&$filter=' + odatafield + ' eq ') + xfilter
            elif isinstance(xfilter, int) :
                pfilter = str('&$filter=' + odatafield + ' eq ') + str(xfilter)
        return pfilter, pfilterlist
        

