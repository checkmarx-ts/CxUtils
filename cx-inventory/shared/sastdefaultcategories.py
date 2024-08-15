"""
========================================================================

CXQL QUERIES CATEGORIES FROM SAST
 
antonio.silva@checkmarx.com
PS-EMEA
31-08-2023
 
Makes uses of specific collections from engine pack versions:
- 9.3.0     in sastdefaultcategories930.py
- 9.4.0     in sastdefaultcategories940.py
- 9.4.5     in sastdefaultcategories945.py
- 9.5.0     in sastdefaultcategories950.py
- 9.5.3     in sastdefaultcategories953.py
- 9.5.4     in sastdefaultcategories954.py
- 9.5.5     in sastdefaultcategories930.py
The collections were retieved from fresh installed/upgraded SAST version

========================================================================
"""

# Default query categories, out-of-the box
# Depending on version

def sastdefaultcategories( sastversion: None ) :
    # from SAST 9.5.5
    if not sastversion or sastversion['enginePack'].startswith('9.5.5') :
        from sastdefaultcategories955 import default_categories_955
        return default_categories_955
    # from SAST 9.5.4
    elif sastversion['enginePack'].startswith('9.5.4') :
        from sastdefaultcategories954 import default_categories_954
        return default_categories_954
    # from SAST 9.5.3
    elif sastversion['enginePack'].startswith('9.5.3') :
        from sastdefaultcategories953 import default_categories_953
        return default_categories_953
    # from SAST 9.5.0
    elif sastversion['version'].startswith('9.5.0') :
        from sastdefaultcategories950 import default_categories_950
        return default_categories_950
    # from SAST 9.4.5
    elif sastversion['enginePack'].startswith('9.4.5') :
        from sastdefaultcategories945 import default_categories_945
        return default_categories_945
    # from SAST 9.4.0
    elif sastversion['version'].startswith('9.4.0') :
        from sastdefaultcategories940 import default_categories_940
        return default_categories_940
    # from SAST 9.3.0
    elif sastversion['version'].startswith('9.3.0') :
        from sastdefaultcategories930 import default_categories_930
        return default_categories_930
    # anything else, use the lastest
    else :
        from sastdefaultcategories955 import default_categories_955
        return default_categories_955
         
    
