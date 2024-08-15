# Checkmarx Tooling Library

Application to inventory relevant contents from a Checkmarx product instance or tenant.

### Objective

Extract and identify all the relevant system and object contents from a Checkmarx product instance.
Identify potential issues, collisions, and blockers, that may require any type of correction, handling, or preparation.
Assist in a migration planning, specially from CXSAST to CXONE. 

## Coverage

The tool can extract data from SAST, from SCA, or from CXONE.

## Configuration

See config.yaml file for the CXSAST connectivity parameters.
Also invokable using command line arguments, such as the example below, which extracts the inventory from SAST:
- **cxinventory sast --inventory --verbose --sast.url https://sast.domain.net --sast.username user_name --sast.password  user_pass**
Simple help can be viewed using:
- **cxinventory --help**

### Filter options

Optionally, you can apply a filter to extract information from specific projects only, by using the option **--filter.projects**, either on the config.yaml or as command line argument.
The filter can be set as:
- A single project ID, like ***--filter.projects 1*** (SAST) or ***--filter.projects 5ba5b65-4171-4636-a076-74f2576c1eb3*** (SCA or CXONE)
- An array of project IDs, like ***--filter.projects [1,2,3]*** (SAST) or ***--filter.projects [95ba5b65-4171-4636-a076-74f2576c1eb3,1bb43b88-4a7b-4cba-b7b7-ae730678999a]*** (SCA or CXONE)
- A file containing a list of project IDs, like ***--filter.projects "@C:\data\filter.txt"***
- All projects below an ID, exclusive, like ***--filter.projects <2*** (SAST only)
- All projects above an ID, exclusive, like ***--filter.projects >2*** (SAST only)
- All projects below an ID, inclusive, like ***--filter.projects <=2*** (SAST only)
- All projects above an ID, inclusive, like ***--filter.projects >=2*** (SAST only)

## Output

CSV files are generated with the relevant content, with the names prefixed with the environment type, with the following detail:

SAST inventory related
- **sast_inventorysummary.csv**: SAST status summary per object type, to easy spot potential migration issues 
- **sast_inventory.csv**: SAST inventory of all the objects and each migration readiness status
- **sast_inventoryprojects.csv**: SAST existing projects with detailed information about configuration and readiness
- **sast_inventorypresets.csv**: SAST existing presets with detailed information about queries, customizations, and readiness
CXONE inventory related
- **cxone_inventorysummary.csv**: CXONE status summary per object type, to easy spot potential migration issues 
- **cxone_inventory.csv**: CXONE inventory of all the objects and each migration readiness status
- **cxone_inventoryprojects.csv**: CXONE existing projects with detailed information about configuration and readiness
- **cxone_inventorypresets.csv**: CXONE existing presets with detailed information about queries, customizations, and readiness
- **cxone_inventoryqueriesmapsast.csv**: CXONE query id mapping with the SAST ones
SCA inventory related
- **sca_inventorysummary.csv**: SCA status summary per object type, to easy spot potential migration issues 
- **sca_inventory.csv**: SCA inventory of all the objects and each migration readiness status
- **sca_inventoryprojects.csv**: SCA existing projects with detailed information about configuration and readiness

## Invocation commands, options, and arguments

All the below can be used from command line, in the config.yaml, and in environment variables prefixed with "*CXTOOL_*"

General commands, to indicate the target system type (SAST, CXONE, or SCA). Only one can be selected.

|Command|Description|
|---|---|
|sast|Command to use a CXSAST environment. This is the default and will be used if no command is selected.|
|cxone|Command to use a CXONE tenant.|
|sca|Command to use an SCA tenant.|

Execution options. Multiple can be selected.

|Argument|Description|
|---|---|
|--inventory|To extract a system inventory. This is the default and will be used in no extraction option is selected.|
|--triages-count|To extract the count of triaged results per project and per state.|
|--triages-all|To extract all the triaged results per project (heavy).|
|--custom-queries|To extract all the cunstom queries, from SAST only.|

Filtering options.  Multiple can be selected.

|Argument|Description|
|---|---|
|--filter.projects|To extract data from specific projects only.|

Optional arguments.

|Argument|Description|
|---|---|
|--help|To display and help screen.|
|--verbose|To outupt the execution progress in the screen.|

Connection parameters, to use the one associated to the system being used (SAST, CXONE, or SCA)

|Parameter|Description|
|---|---|
|--sast.url|SAST url (i.e.: https://portal.checkmarx.net).|
|--sast.username|SAST user name.|
|--sast.password|SAST password.|
|--sast.proxy_url|SAST outbound proxy url, if a proxy is used to connect.|
|--sast.proxy_username|SAST proxy user name, if the proxy requires authentication (basic only).|
|--sast.proxy_password|SAST proxy password, if the proxy requires authentication (basic only).|
|--cxone.url|CXONE portal url (i.e.: https://eu.ast.checkmarx.net).|
|--cxone.acl|CXONE access control url (i.e.: https://eu.iam.checkmarx.net).|
|--cxone.tenant|CXONE tenant name.|
|--cxone.apikey|CXONE api key.|
|--cxone.clientid|CXONE client id, defaults to "*ast-app*".|
|--cxone.granttype|CXONE grant type, defaults to "*refresh_token*"|
|--cxone.proxy_url|CXONE outbound proxy url, if a proxy is used to connect.|
|--cxone.proxy_username|CXONE proxy user name, if the proxy requires authentication (basic only).|
|--cxone.proxy_password|CXONE proxy password, if the proxy requires authentication (basic only).|
|--sca.url|SCA portal url (i.e.: https://api-sca.checkmarx.net).|
|--sca.acl|SCA access control url (i.e.: https://platform.checkmarx.net).|
|--sca.tenant|SCA tenant name.|
|--sca.username|SCA user name.|
|--sca.password|SCA password.|
|--sca.proxy_url|SCA outbound proxy url, if a proxy is used to connect.|
|--sca.proxy_username|SCA proxy user name, if the proxy requires authentication (basic only).|
|--sca.proxy_password|SCA proxy password, if the proxy requires authentication (basic only).|

## Examples (command line)

Extract from SAST:
- Inventory: **`cxinventory --verbose --sast.url https://portal.checmarx.net --sast.username username --sast.password password`**
- Inventory: **`cxinventory sast --verbose --sast.url https://portal.checmarx.net --sast.username username --sast.password password`**
- Custom queries: **`cxinventory --custom-queries --verbose --sast.url https://portal.checmarx.net --sast.username username --sast.password password`**
- Custom queries: **`cxinventory sast --custom-queries --verbose --sast.url https://portal.checmarx.net --sast.username username --sast.password password`**
- Inventory & triage counts: **`cxinventory --inventory --triages-count --verbose --sast.url https://portal.checmarx.net --sast.username username --sast.password password`**
- Inventory & triage counts: **`cxinventory sast --inventory --triages-count --verbose --sast.url https://portal.checmarx.net --sast.username username --sast.password password`**

Extract from CXONE:
- Inventory: **`cxinventory cxone --verbose --cxone.url https://eu.ast.checkmarx.net --cxone.acl https://eu.iam.checkmarx.net --cxone.tenant tenant_name --cxone.apikey eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia`**
- Triage counts: **`cxinventory cxone --triages-count --verbose --cxone.url https://eu.ast.checkmarx.net --cxone.acl https://eu.iam.checkmarx.net --cxone.tenant tenant_name --cxone.apikey eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia`**
- Inventory and triage counts: **`cxinventory cxone --inventory --triages-count --verbose --cxone.url https://eu.ast.checkmarx.net --cxone.acl https://eu.iam.checkmarx.net --cxone.tenant tenant_name --cxone.apikey eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia`**

Extract from SCA:
- Inventory: **`cxinventory sca --verbose --sca.url https://api-sca.checkmarx.net --sca.acl https://platform.checkmarx.net --sca.tenant tenant_name --sca.username username --sca.password password`**
- Triage counts: **`cxinventory sca --triages-count --verbose --sca.url https://api-sca.checkmarx.net --sca.acl https://platform.checkmarx.net --sca.tenant tenant_name --sca.username username --sca.password password`**
- Inventory and triage counts: **`cxinventory sca --triages --triages-count --verbose --sca.url https://api-sca.checkmarx.net --sca.acl https://platform.checkmarx.net --sca.tenant tenant_name --sca.username username --sca.password password`**

