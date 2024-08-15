"""
========================================================================

CXQL PRESETS FROM SAST
 
antonio.silva@checkmarx.com
PS-EMEA
31-08-2023
 
Makes uses of specific collections from engine pack versions:
- 9.3.0     in sastdefaultpresets930.py
- 9.4.0     in sastdefaultpresets940.py
- 9.4.5     in sastdefaultpresets945.py
- 9.5.0     in sastdefaultpresets950.py
- 9.5.3     in sastdefaultpresets953.py
- 9.5.4     in sastdefaultpresets954.py
- 9.5.5     in sastdefaultpresets930.py
The collections were retieved from fresh installed/upgraded SAST version

========================================================================
"""

# Default presets configurations, out-of-the box
# Depending on version

def sastdefaultpresets( sastversion: None ) :
    # from SAST 9.5.5
    if not sastversion or sastversion['enginePack'].startswith('9.5.5') :
        from sastdefaultpresets955 import default_presets_955
        return default_presets_955
    # from SAST 9.5.4
    elif sastversion['enginePack'].startswith('9.5.4') :
        from sastdefaultpresets954 import default_presets_954
        return default_presets_954
    # from SAST 9.5.3
    elif sastversion['enginePack'].startswith('9.5.3') :
        from sastdefaultpresets953 import default_presets_953
        return default_presets_953
    # from SAST 9.5.0
    elif sastversion['version'].startswith('9.5.0') :
        from sastdefaultpresets950 import default_presets_950
        return default_presets_950
    # from SAST 9.4.5
    elif sastversion['enginePack'].startswith('9.4.5') :
        from sastdefaultpresets945 import default_presets_945
        return default_presets_945
    # from SAST 9.4.0
    elif sastversion['version'].startswith('9.4.0') :
        from sastdefaultpresets940 import default_presets_940
        return default_presets_940
    # from SAST 9.3.0
    elif sastversion['version'].startswith('9.3.0') :
        from sastdefaultpresets930 import default_presets_930
        return default_presets_930
    # anything else, use the lastest
    else :
        from sastdefaultpresets955 import default_presets_955
        return default_presets_955
         
    
