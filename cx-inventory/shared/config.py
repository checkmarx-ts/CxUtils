""" 
========================================================================

CLASS FOR HANDLING CONFIG FILES AND STRUCTURES

ORDERED CALL:
1. A yaml file  (.yaml or .yml) 
2. A json file  (.json)
3. Environment variables
4. Application arguments

DEFAULT CONFIG FILE WILL BE SEARCHED IN THE APPLICATION MAIN FOLDER:
1. config.yaml
2. config.yml
3. config.json

joao.costa@checkmarx.com
PS-EMEA
10-11-2022

========================================================================
"""


import __main__
import errno
import os
import pathlib
import sys
import json
import yaml


# Default prefix from environment variables in configuration
ENVVARS_PREFIX  = 'CXTOOL_'


class config(object) :

    # Constructor
    # - fileorpath: config file or the config location
    #   defaults to application mainmodule()\config.yaml/yml/json/ini
    # - defaults: a dictionary containing the default variable names and values
    #   if not present, fileorpath with be used to load whatever is available
    # - checkenvvars: will load configurations from environment variables
    #   if fileorpath is not defined, requires "defaults" to check environment variable names
    #   evironment variable names are uppercase and splitted by underscore ("_")
    # - envvarsprefix: environment variables are expected to be prefixed 
    #   such as CXTOOL_, representing a CXSAST_VARIABLE_NAME 
    # - autoclean: if set, parameters without a value will be removed
    #   if set, command like params will not work
    #   CXTOOL_ prefix is used by default


    def __init__(self, fileorpath = None, defaults = None, checkenvvars = True, envvarsprefix = None, autoclean = False, defaultname = 'config' ) :
        self.__content      = defaults
        self.__commands     = []
        self.__flat         = None
        self.__filename     = None
        self.__checkenv     = checkenvvars
        self.__autoclean    = autoclean
        if envvarsprefix :
            self.__envprefix    = envvarsprefix
        else :
            self.__envprefix    = ENVVARS_PREFIX
        if fileorpath :
            path = os.path.abspath(os.path.dirname(fileorpath))
            if (path != fileorpath) :
                self.__filename = fileorpath
        else :
            # Do we have a --config-file command line argument ?
            configfile = self.__command_arg('config-file' )
            if configfile :
                path = configfile
                if (not path) or (not os.path.exists(path)) :
                    raise FileNotFoundError( errno.ENOENT, 'Configuration file or path was not found', path)
                if os.path.isfile(path) :
                    self.__filename = path    
            else :
                # File name or path not set - resolve main application location
                path = self.mainrootpath()

        # Search for config.yaml, config.yml, config.json
        if (not self.__filename) and (path) :
            if os.path.exists(path + os.sep + defaultname + '.yaml') :
                self.__filename = path + os.sep + defaultname + '.yaml'
            elif os.path.exists(path + os.sep + defaultname + '.yml') :
                self.__filename = path + os.sep + defaultname + '.yml'
            elif os.path.exists(path + os.sep + defaultname + '.json') :
                self.__filename = path + os.sep + defaultname + '.json'

        # Check if configuration file exists    
        if self.__filename and not os.path.exists(self.__filename) :
            self.__filename = None
            raise FileNotFoundError( errno.ENOENT, 'Configuration file was not found', self.__filename)

        # Check if configuration file is the right type
        if self.__filename :
            extension = pathlib.Path(self.__filename).suffix.lower()
            if not extension in ['.yaml', '.yml', '.json'] :
                raise OSError( errno.ENOTTY, 'Unsupported configuration file type', self.__filename)
            
        # Load configurations
        self.__config_load()



    # Load config
    def __config_load(self) :
        # Load from configuartions file, if present
        self.__loadfromfile()
        # Load/override from environment variables, if present
        if self.__checkenv :
            self.__loadfromenvvars()
        # Load/override from application arguments, if matching
        self.__loadfromarguments()
        # Clean and adjust
        self.__content = self.__clean_values(self.__content)
        self.__flat    = self.__config_flat()



    # Add configuration (keyname.keyname.keyname = value)
    def __config_put( self, key, value = None, separator = '.' ) :
        if not key :
            return
        keys = key.lower().lstrip('-').split(separator)
        if len(keys) == 0 :
            return
        data = {}
        for xkey in keys[::-1]:
        # for xkey in keys :
            if not data :
                data[xkey] = value
            else:
                tmp = {}
                tmp[xkey] = data.copy()
                data = dict(tmp)
        self.__content = self.__mergedictionaries(self.__content, data)



    # Get configuration (keyname.keyname.keyname)
    def __config_get( self, key ) :
        if not key :
            return None
        if key in self.__flat :
            return self.__flat[key]



    # Checks if a key exists (keyname.keyname.keyname)
    def __config_keyexists(self, key) :
        if not key :
            return False
        return key in self.__flat



    # Get configuration and flat dictionary
    def __config_flat( self ) :
        data = {}
        def __getkeyvalue( elems, prefix ) :
            for xkey in elems.keys() :
                xvalue = elems[xkey]
                if (type(xvalue) is dict) :
                    xvalue = __getkeyvalue( xvalue, '.'.join([prefix, xkey]) if prefix else xkey)    
                else :
                    data[ '.'.join([prefix, xkey]) if prefix else xkey ] = xvalue
        if self.__content :
            __getkeyvalue( self.__content, None )
        return data



    # Get specific command line argument
    def __command_arg(self, argname) :
        if not argname :
            return None
        lastkey = ''
        args = sys.argv[1:]
        for arg in args :
            # Process keys
            if arg.startswith('-') or arg.startswith('--') :
                eq = arg.find('=')
                if eq > 2 :
                    nkey = arg[0:eq].strip().lower()
                    nval = arg[eq+1:].strip()
                else :
                    nkey = arg.strip().lower()
                    nval = None
                # Remove initial "-" or "--"
                lastkey = nkey.lstrip('-')
                if lastkey.lower() == argname.lower() :
                    return nval
            else :
                if lastkey.lower() == argname.lower() :
                    return arg
        return None



    # Get password from keyring
    def __keyring_password(self, key, section, username) :
        import keyring
        if sys.platform.startswith('win32'):
            from keyring.backends import Windows
            keyring.set_keyring(Windows.WinVaultKeyring())
        try :
            xpassw = keyring.get_password(section, username)
        except :
            xpassw = None
            pass
        if xpassw :
            self.__config_put( key, xpassw )
            self.__content = self.__clean_values(self.__content)
            self.__flat    = self.__config_flat()
            return True
        else :
            return False



    # Ensure yes/no maps to true/false and str with arrays are mapped to arrays
    def __clean_values(self, data) :
        clean = {}
        if data == None :
            return clean
        for k, v in data.items():
            if isinstance(v, dict):
                nested = self.__clean_values(v)
                if len(nested.keys()) > 0:
                    clean[k] = nested
            elif v is not None:
                if (type(v) is str) :
                    if v.strip().startswith('[') and v.strip().endswith(']') :
                        clean[k] = eval(v)
                    elif v.lower() in ['yes', 'true' ] :
                        clean[k] = True
                    elif v.lower() in ['no', 'false' ] :
                        clean[k] = False
                    else :
                        clean[k] = v
                else :
                    clean[k] = v
            else :
                if not self.__autoclean :
                    clean[k] = None    
        return clean



    def __mergedictionaries(self, dict1, dict2) :
        if dict1 == None or dict1 == {} :
            return dict2
        elif dict2 == None or dict2 == {} :
            return dict1
        else :
            z = {}
            overlapping_keys = dict1.keys() & dict2.keys()
            for key in dict1.keys() :
                if key in overlapping_keys :
                    if (type(dict1[key]) is dict) and (type(dict2[key]) is dict) :
                        z[key] = self.__mergedictionaries(dict1[key], dict2[key])
                    elif (type(dict1[key]) is list) and (type(dict2[key]) is list) :
                        z[key] = dict1[key] + [value for value in dict2[key] if value not in dict1[key]]
                    else:
                        z[key] = dict2[key]
                else :
                    z[key] = dict1[key]
            for key in dict2.keys() - overlapping_keys :
                z[key] = dict2[key]
            return z



    def __loadfromfile(self) :
        # Load according to extension
        if self.__filename :
            extension = pathlib.Path(self.__filename).suffix.lower()
            data = None
            if extension in ['.yaml', '.yml'] :
                f = open(self.__filename, 'r')
                data = yaml.load(f, Loader=yaml.FullLoader)
                f.close()
            elif extension == '.json' :
                f = open(self.__filename, 'r')
                data = json.load(fp = f)
                f.close()
            # ini not supported (at leat yet)
            # elif extension == '.ini' :
            # Merge data
            self.__content = self.__mergedictionaries(self.__content, data)



    def __loadfromenvvars(self) :
        # Get existing flat keys from matching
        # done = []
        flatvars = self.__config_flat()
        for key in flatvars.keys() :
            xval = None
            xkey = key
            if self.__envprefix :
                xkey = self.__envprefix + key
            # Search as is
            if not xval :
                xval = os.getenv(xkey)
            # Search upper case
            if not xval :
                ukey = xkey.upper()
                xval = os.getenv(ukey)
            # Search linux compatible format (transform '.' and '-' into '_')
            if not xval :
                xkey = xkey.replace('.', '_').replace('-', '_')
                xval = os.getenv(xkey)
            # Search linux compatible format uppercase
            if not xval :
                xkey = xkey.upper()
                xval = os.getenv(xkey)
            # Have we found it ?
            if xval :
                self.__config_put( key.lower(), xval )
                # done.append(xkey)



    def __loadfromarguments(self) :
        args = sys.argv[1:]
        lastkey = ''
        for arg in args :
            # Process keys
            if arg.startswith('-') or arg.startswith('--') :
                eq = arg.find('=')
                if eq > 2 :
                    nkey = arg[0:eq].strip().lower()
                    nval = arg[eq+1:].strip()
                else :
                    nkey = arg.strip().lower()
                    if (nkey == '--help') or (nkey == '-h') :
                        nkey = 'help'
                        nval = True
                    elif (nkey == '--verbose') or (nkey == '-v') :
                        nkey = 'verbose'
                        nval = True
                    elif (nkey == '--debug') :
                        nkey = 'debug'
                        nval = True
                    else :
                        nval = None
                # Remove initial "-" or "--"
                if nkey :
                    lastkey = nkey.lstrip('-')
                    self.__config_put( lastkey, nval )
                    if nval :
                        lastkey = ''
                else :
                    lastkey = ''
            else :
                if lastkey :
                    self.__config_put( lastkey.lower(), arg )
                else :
                    self.__commands.append( arg.lower() )
                    # self.__config_put( arg.lower(), None )
                lastkey = ''



    # Returns the configuration dictionary
    # In the format [key][key][key] = value
    @property
    def values(self) :
        return self.__content



    # Returns the configuration list
    # In the format  {key.key.key: value} 
    @property
    def flat(self) :
        return self.__flat



    # Returns the value from a specific key
    def value( self, key, default = None ) :
        xvalue = self.__config_get( key )
        if xvalue == None :
            xvalue = default
        return xvalue


    # Checks if specific key exists even if null
    def haskey( self, key ) :
        return self.__config_keyexists( key )



    # Checks ow many commands were entered in command line
    def commandcount(self) :
        return len(self.__commands)



    # Checks if specific key exists and is null
    def hascommand( self, command ) :
        xcommand = command.lower()
        return (xcommand in self.__commands) or (self.__config_keyexists(xcommand) and not self.value(xcommand, None))



    # Assigns a value to config key
    # Optionally loads it from an environment variable
    # Returns the value assigned
    def putvalue( self, key, value = None, envvariablename = None ) :
        if not key :
            return None
        xvalue = value
        if envvariablename :
            evalue = os.getenv(envvariablename)
            if evalue :
                xvalue = evalue
        self.__config_put( key, xvalue )
        self.__content = self.__clean_values(self.__content)
        self.__flat    = self.__config_flat()
        return self.__config_get( key )



    # Load a user password from keyring and assigns it to config key
    # Returns True if the password is successfuly loaded
    def putkeyringpassword( self, key, section, username ) : 
        return self.__keyring_password(key, section, username)



    # Get main module name
    @classmethod
    def mainmodulename(self) :
        xname = ''
        xfile = os.path.basename(__main__.__file__)
        if xfile :
            xname = os.path.splitext(xfile)[0]
        return xname
    

    # Get application running path, for scripts or compiled exe
    @classmethod
    def mainrootpath(self) :
        # Is it a frozen exe
        if getattr(sys, 'frozen', False) :
            # base_path = os.path.dirname(sys.executable)
            base_path = sys.executable
        else :
            # Get the path from __main__
            base_path = __main__.__file__
            if not base_path :
                base_path = __file__            
        return os.path.abspath(os.path.dirname(base_path))



# Add this library sub-folders to search path
if not getattr(sys, 'frozen', False) :
    current_path = os.path.abspath(os.path.dirname(__file__))
    # Get sub-folders from current
    def __fast_scandir(dirname):
        subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
        for dirname in list(subfolders):
            subfolders.extend(__fast_scandir(dirname))
        return subfolders
    sub_dirs = __fast_scandir(current_path)
    # Add all to libs path
    sys.path.insert(1, current_path)
    for sdir in sub_dirs :
        sys.path.insert(1, sdir)
