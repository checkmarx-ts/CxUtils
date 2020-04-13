# CxSeverityOverride

A tool that helps in changing the severity of the queries.

## Description

This tool performs the following operations.
1) Change the severity of a query(or queries).
2) Add the queries to any number of presests.
3) Change the Type of query group (Cx/Corp/Project/Team)


## Getting Started

### Dependencies

  * Windows 10 or Server 2016
  * Python 3.8 or later
  * Python Library - pyodbc (installed through pip)
  * ODBC Data Source Administrator (Windows)

### Installation

* Downloading the solution
* Required Configuration -
	1. Install python.
	2. Install 'pyodbc' using PIP, eg: 'pip install pyodbc'.
	3. Create an ODBC database connection for Cx SQL Server instance:
		a. Open 'ODBC Data Sources' from Start Menu. Depening on the type of installed python, select 32 0r 64 bit.
		b. Under the 'System DSN', click 'Add' and select 'SQL Server' from the list of drivers.
		c. Enter the name of the data source as 'checkmarx'.
		d. The server address for a local SQL Server database would be: '.\SQLEXPRESS'
		e. Set default database to CxDB.
		f. You use integrated authentication or SQL authentication, depending on your database setup.

  * Refer to Repository Wiki for full/advanced details

### Execution

* Steps to execute
	* To export the available queries from CxDB, run this command : py export_query_info
	* This will generate two csv files.
	1. presest.csv - This includes all the available presets along with their preset ids. This file is only used for reference to preset ids.
	2. query.csv - This includes all the details required to update the severity,package type or preset of the queries.
			


## Additional Documentation

	Severity values :
	0 - Informational
	1 - Low
	2 - Medium
	3 - High
	
	| PackageType | PackageTypeName |
	|-------------|-----------------|
	|	0 |	Cx	|
	|	1 |	Corp|
	|	2 |	Project	|
	|	3 |	Team|
	
	
Refer to the project [Wiki](insert-wiki-url) for additional information


## Version History



## Contributing

We appreciate feedback and contribution to this repo! Before you get started, please see the following:

- [Checkmarx general contribution guidelines](https://github.com/checkmarx-ts/open-source-template/blob/master/GENERAL-CONTRIBUTING.md)
- [Checkmarx code of conduct guidelines](https://github.com/checkmarx-ts/open-source-template/blob/master/CODE-OF-CONDUCT.md)

## Support + Feedback

Include information on how to get support. Consider adding:

- Use [Issues](https://github.com/checkmarx-ts/open-source-template/issues) for code-level support


## License

Project Lisense can be found [here](LICENSE)
