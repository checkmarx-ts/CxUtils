
""" 
========================================================================

SIMILARITY ID CALCULATOR FOR CXONE

antonio.silva@checkmarx.com
PS-EMEA
24-08-2023

========================================================================
"""

import os
import numpy
import warnings
from enum import Enum



MAX_LINE_LENGTH     = 160

class SimilarityVersion(Enum) :
    Regular         = 0
    TrimLeading     = 1
    RemoveAll       = 2



class cxsimilarityid(object) :

    def __init__(self):
        self.__file1        = None
        self.__file2        = None
        self.__line1        = 0
        self.__column1      = 0
        self.__methodline1  = 0
        self.__source1      = None
        self.__source2      = None
        self.__line2        = 0
        self.__column2      = 0
        self.__methodline2  = 0
        self.__queryid      = 0
        self.__simIdVersion = SimilarityVersion.Regular
        # Overflow runtime warnings will appear for int32 bits calculation. we do not want it.
        warnings.filterwarnings( 'ignore', message = 'overflow encountered in scalar multiply' )



    @property
    def __issamenode( self ) :
        return ( self.__file1 == self.__file2 and self.__line1 == self.__line2 and self.__column1 == self.__column2 and self.__methodline1 == self.__methodline2 )


    def __GetPreviousSemicolon( self, line: str, column: int) :
        if (column <= 0) :
            return 0
        i = column
        while (i >= 0) :
            if (line[i:i+1] == ';' or line[i:i+1] == '\n' or line[i:i+1] == '\r') :
                return i
            i -= 1
        return i + 1
    

    def __GetNextSemicolon( self, line: str, column: int ) :
        if (column < 0) :
            return 0
        i = column
        while (i < len(line) ) :
            if (line[i:i+1] == ';' or line[i:i+1] == '\n' or line[i:i+1] == '\r') :
                return i
            i += 1
        return i - 1

    
    def __adjustColumn(self, column: int, prevSemiLocation: int, line: str) :
        if column >= prevSemiLocation :
            column -= prevSemiLocation
        return column


    def __ExtractLine( self, source: str, lineNumber: int, column: int ) :
        curLine = ''
        line = lineNumber - 1
        # line = lineNumber - 1
        if line >= len(source) :
            return curLine, column
        
        curLine = source[line]
        if curLine.endswith('\n') :
            curLine = curLine[:-1]

        if ( len(curLine) > MAX_LINE_LENGTH ) :
            if (column >= len(curLine)) :
                curLine = curLine[0:MAX_LINE_LENGTH]
            else :
                prevSemi = self.__GetPreviousSemicolon(curLine, column)
                nextSemi = self.__GetNextSemicolon(curLine, column)
                column = self.__adjustColumn(column, prevSemi, line)
                curLine = curLine[ prevSemi: nextSemi]
                # curLine = curLine[ prevSemi: prevSemi + (nextSemi - prevSemi) ]

        return curLine, column



    def __ExtractMethodLine( self, source: str, lineNumber: int ) :
        curLine = ''
        if (lineNumber <= 0) :
            lineNumber = 0
        line = lineNumber - 1
        if line >= len(source) :
            return curLine            
        curLine = source[line]
        if curLine.endswith('\n') :
            curLine = curLine[:-1]
        pos = 0
        found = False
        while pos < len(curLine) and not found :
            if str.isdigit( curLine[pos:pos+1]) :
                curLine = curLine[0:pos]
                found = True
            pos += 1
        if self.__simIdVersion == SimilarityVersion.TrimLeading :
            curLine = curLine.lstrip()
        return curLine
    

    def __CountDelimiter( self, line: str, column: int, delimiter: str ) :
        numberOfDelimiterAppearences = 0
        firstNonSpaceAppearance = False
        i = 0
        while i < column and i < len(line) :
            if (self.__simIdVersion == SimilarityVersion.TrimLeading) :
                if (line[i:i+1] != ' ' and line[i:i+1] != '\t') :
                    firstNonSpaceAppearance = True
                if (line[i:i+1] == delimiter and firstNonSpaceAppearance) :
                    numberOfDelimiterAppearences += 1
            else :
                if (line[i:i+1] == delimiter) :
                    numberOfDelimiterAppearences += 1
            i += 1
        return numberOfDelimiterAppearences
    

    def __stripLine( self, line: str, column: int ) :
        stripped = ''
        if(line == '') :
            return ''
        counter = 0
        i = 0
        while i < column :            
            if (line[i:i+1] == ' ' or line[i:i+1] == '\t') :
                counter += 1
            i += 1
        stripped = line.replace(' ', '')
        column -= counter
        return stripped, column


    def __calculateForNode( self, source: str, absoluteFileName: str, line: int, column: int, methodLine: int ) :

        fullLine, column            = self.__ExtractLine(source, line, column)        
        finalLine                   = ''
        finalMethodLine             = ''
        columnAsString              = str(column)
        methodContentNonStripped    = self.__ExtractMethodLine(source, methodLine)           
        fileName                    = os.path.basename(absoluteFileName).lower()
        appearanceOfComma           = 0
        appearanceOfSpace           = str( self.__CountDelimiter(fullLine, column, ' ') ) + ','

        if self.__simIdVersion == SimilarityVersion.TrimLeading :
            finalLine = fullLine.lstrip()
            finalMethodLine = methodContentNonStripped
            appearanceOfComma = self.__CountDelimiter(fullLine, column, ',')
            columnAsString = ''
        elif self.__simIdVersion == SimilarityVersion.RemoveAll :
            dummyColumn = 0
            strippedColumn = column
            strippedLine, strippedColumn = self.__stripLine(fullLine, strippedColumn)
            finalLine = strippedLine
            finalMethodLine, dummyColumn = self.__stripLine(methodContentNonStripped, dummyColumn)
            appearanceOfSpace = ''
            appearanceOfComma = self.__CountDelimiter(strippedLine, strippedColumn, ',')
            columnAsString = str(strippedColumn)
        else :
            appearanceOfComma = self.__CountDelimiter(fullLine, column, ',')
            finalLine = fullLine
            finalMethodLine = methodContentNonStripped
            columnAsString = ''

        return fileName + finalLine + finalMethodLine + ',' + appearanceOfSpace + str(appearanceOfComma) + columnAsString
    

    def __GetSimilarityHashCode(self, simIdcode: str) :
        # This must be a 32 bit integer, so we use numpy
        hashCode: numpy.int32 = 0
        i = 0
        while i < len(simIdcode) :
            v = ord( simIdcode[i:i+1] )
            hashCode = numpy.int32( hashCode) * 31 + v
            # hashCode = numpy.int32( numpy.int32( numpy.int32(hashCode) * 31 ) + v )
            i += 1
        return hashCode


    def __ComputeSimilarityId( self ) :
        node1 = self.__calculateForNode( self.__source1, self.__file1, self.__line1, self.__column1, self.__methodline1 )
        if self.__issamenode :
            node2 = node1
        else :
            node2 = self.__calculateForNode( self.__source2, self.__file2, self.__line2, self.__column2, self.__methodline2 )
        simcodestr = node1 + node2 + str(self.__queryid)
        simcode = self.__GetSimilarityHashCode(simcodestr)
        return simcode


    def __ReadSourceFiles( self, absoluteFileName1: str, absoluteFileName2: str, Encoding: str = 'UTF8' ) :
        
        # Read source file
        if (absoluteFileName1) and os.path.exists(absoluteFileName1) :
            if absoluteFileName1 != self.__file1 :
                self.__file1 = absoluteFileName1
                with open( absoluteFileName1, mode = 'r', encoding = Encoding ) as handle :
                    self.__source1 = handle.readlines()
        else :
            self.__file1 = None
            self.__source1 = None

        # Read sink file
        if (absoluteFileName2) and os.path.exists(absoluteFileName2) :
            if absoluteFileName2 != self.__file2 :
                self.__file2 = absoluteFileName2
                if absoluteFileName1 == absoluteFileName2 :
                    self.__source2 = self.__source1
                else :
                    with open( absoluteFileName2, mode = 'r', encoding = Encoding ) as handle :
                        self.__source2 = handle.readlines()
        else :
            self.__file2 = None
            self.__source2 = None


    # def GetSimilarity( self, absoluteFileName1: str, shortName1: str, line1: int, column1: int, methodLine1: int,
    #                 absoluteFileName2: str, shortName2: str, line2: int, column2: int, methodLine2: int,
    #                 queryId: int, Encoding: str = 'UTF8'  ) :
    # FROM ORIGINAL C# CODE THE PARAMETERS "shortName2" & "shortName2" ARE NOT USED ANYWHERE. REMOVED HERE
    def GetSimilarity( self, absoluteFileName1: str, line1: int, column1: int, methodLine1: int,
                    absoluteFileName2: str, line2: int, column2: int, methodLine2: int,
                    queryId: int, Encoding: str = 'UTF8', Version: SimilarityVersion = SimilarityVersion.Regular  ) :
        if not Encoding :
            Encoding = 'UTF8'

        self.__line1 = line1
        self.__column1 = column1
        self.__methodline1 = methodLine1
        self.__line2 = line2
        self.__column2 = column2
        self.__methodline2 = methodLine2
        self.__queryid = queryId

        self.__ReadSourceFiles(absoluteFileName1, absoluteFileName2, Encoding )
        self.__simIdVersion = Version
        retVal = self.__ComputeSimilarityId()
        return retVal

