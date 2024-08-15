# Checkmarx Tooling Library

Common shared tools and classes for Checkmarx PS tools

### Notice

Tooling developed using Python. Please use Python3!

## Table of contents

- **config**: class for config files, environment variables, and arguments
- **version**: class containing product version information
- **cxoneapicaller**: low level class for CXONE REST api calls
- **cxonecache**: class specialized in caching preloaded CXONE objects
- **cxoneconn**: class for CXONE connections (REST & KEYCLOAK)
- **sastapicaller**: low level class for CXSAST REST api calls
- **sastauditcaller**: low level class for CXSAST AUDIT SOAP calls
- **sastsoapcaller**: low level class for CXSAST SOAP calls
- **sastcache**: class specialized in caching preloaded CXSAST objects
- **sastconn**: class for CxSAST connections (REST, AC, AUDIT & SOAP)
- **scaapicaller**: low level class for SCA REST api calls
- **scacache**: class specialized in caching preloaded SCA objects
- **scaconn**: class for SCA connections (REST & AC)
- **sastdefaultcategories**: structures with default query categories delivered out-of-the box from different versions
- **sastdefaultpresets**: structures with default presets and associated queries delivered out-of-the box from different versions


## Config usage

The **config** module is used to apply the runtime configurations, in the following sequence:

1. Read from configuration file (yaml or json). *Example (yaml)*: 
   ```
   project:
      name: project_name
      csv-semicolon-delimiter: yes
      verbose: yes
   sast:
      url: https://your.fqdn.com
      username: sast_username
      password: sast_password
      proxy_url: 
      proxy_username: 
      proxy_password: 
    ```
		
2. Override configurations from environment variables, with sections separated by underscore, hyphens also written as underscores, and prefixed by "CXTOOL_".
. *Examples*:
   ```
   CXTOOL_PROJECT_NAME=project_name
   CXTOOL_PROJECT_CSV_SEMICOLON_DELIMITER=yes
   CXTOOL_SAST_USERNAME=new_sast_username
   CXTOOL_SAST_PASSWORD=new_sast_password
   ```
		
3. Override configurations from command line, with sections separated by dots. *Examples*:
   ```
   --sast.username=new_sast_username --sast.password=new_sast_password
   ```
	
