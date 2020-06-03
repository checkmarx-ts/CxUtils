
import sys;
import traceback;

sStatsId      = "CxRestAPIStatistics1.py";
sStatsVers    = "(v1.0502)";
sStatsDisp    = sStatsId+" "+sStatsVers+":"

bStatsVerbose = True;

# -------------------------------------------------------------------
#
# The following section contains the fields that may be customized
# to support the collection of 'statistics' for Cx Rest API's:
#
#   1) The # of Rest API call(s) that have been made.
#
# -------------------------------------------------------------------

# 'statistics' collector(s):

cRestAPICallsMade = 0;

def main():

    try:

        if bStatsVerbose == True:

            print("%s Stats VERBOSE flag is [%s]..." % (sStatsDisp, bStatsVerbose));
            print("");
            print("%s Stats 'cRestAPICallsMade' is [%s]..." % (sStatsDisp, cRestAPICallsMade));
            print("");

    except Exception as inst:

        print("%s 'main()' - exception occured..." % (sStatsDisp));
        print(type(inst));
        print(inst);

        excType, excValue, excTraceback = sys.exc_info();
        asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback);

        print("- - - ");
        print('\n'.join(asTracebackLines));
        print("- - - ");

        return False;

    return True;

if __name__ == '__main__':

    bCmdExecOk = main();

    if bCmdExecOk == False:

        print("%s Exiting with a Return Code of (31)..." % (sStatsDisp));

        sys.exit(31);

    print("%s Exiting with a Return Code of (0)..." % (sStatsDisp));

    sys.exit(0);

