# TruffleHog CxQL

A port of the original [TruffleHog](https://github.com/dxa4481/truffleHog) code that executes in Checkmarx SAST as a CxQL customization.

# Warning

The queries here will have a tendency to generate many false positives.  Before implementing this, consider weighing the value of spending time marking several false positives as "Non-Exploitable" against perhaps finding a few true positives that reveal publicly exposed secrets. Some secrets will be benign; others will have the potential for granting administrative access to your production system.

## How to Install

These queries are not specific to any language, therefore it can be used in scans
for multilple language types.  The downside is that you have to install it under 
queries **each** language for which it should be executed.  


1. In CxAudit, make a group under Corp where the query will live.
   This was tested in Java, but may apply to JavaScript and other languages.
   Example: Corp/{Company Name}

2. Under the created group, make a query with a name that corresponds to the name of 
   each .cxql file ncluded with this package.  Paste the contents of each file into
   the corresponding query you created. (e.g. Resolve_Code_And_Comment_Flows)

3. Set the properties on each query as follows:
   * Potential_Hardcoded_Passwords:
	  * Set severity to the level desired
	  * Choose categories as needed (likely fits in Sensitive Data Exposure categories)
	  * CWE ID 798
	  * Executable should be checked
   
   * TruffleHog_Regex_Matches:
	  * Set severity to the level desired
	  * Choose categories as needed (likely fits in Sensitive Data Exposure categories)
	  * CWE ID 798
	  * Executable should be checked

   * TruffleHog_HighEntropy_Strings:
	  * Set severity to the level desired
	  * Choose categories as needed (likely fits in Sensitive Data Exposure categories)
	  * CWE ID 798
	  * Executable should be checked
   
   * Resolve_Code_And_Comment_Flows:
     * Only uncheck the "Executable" checkbox.  All other properties are not applicable.

4. Save the queries and exit CxAudit. Adjust your presets to include your new TruffleHog
queries.

5. (Optional) Execute the SQL script in file "Proc_AddFileExtToLanguage.sql" in the CxDB. This
adds the required stored procedure to the SQL server for adding extensions of files
that are included in a scan.  If there are no additional file types needed for inclusion,
then this step is not necessary.

6. (Optional) Execute the following SQL commands to add supported extentions.  Modify as
needed to support extensions for your language of choice.

```
	exec AddFileExtToLanguage 'Java', 'properties', 'JAVA_XML_EXTENSIONS'
	exec AddFileExtToLanguage 'Java', 'yaml', 'JAVA_XML_EXTENSIONS'
	exec AddFileExtToLanguage 'Java', 'yml', 'JAVA_XML_EXTENSIONS'
	exec AddFileExtToLanguage 'Java', 'json', 'JAVA_XML_EXTENSIONS'
	
	exec AddFileExtToLanguage 'JavaScript', 'properties', 'JS_XML_EXTENSIONS'
	exec AddFileExtToLanguage 'JavaScript', 'yaml', 'JS_XML_EXTENSIONS'
	exec AddFileExtToLanguage 'JavaScript', 'yml', 'JS_XML_EXTENSIONS'

	exec AddFileExtToLanguage 'PHP', 'properties', 'PHP_COMMON_EXTENSIONS'
	exec AddFileExtToLanguage 'PHP', 'yaml', 'PHP_COMMON_EXTENSIONS'
	exec AddFileExtToLanguage 'PHP', 'yml', 'PHP_COMMON_EXTENSIONS'
	exec AddFileExtToLanguage 'PHP', 'json', 'PHP_COMMON_EXTENSIONS'
		
	exec AddFileExtToLanguage 'Ruby', 'yaml', 'RUBY_OTHERS_EXTENSIONS'
	exec AddFileExtToLanguage 'Ruby', 'yml', 'RUBY_OTHERS_EXTENSIONS'
	exec AddFileExtToLanguage 'Ruby', 'json', 'RUBY_OTHERS_EXTENSIONS'
		
	exec AddFileExtToLanguage 'Groovy', 'yaml', 'GROOVY_EXTENSIONS'
	exec AddFileExtToLanguage 'Groovy', 'yml', 'GROOVY_EXTENSIONS'
	exec AddFileExtToLanguage 'Groovy', 'json', 'GROOVY_EXTENSIONS'
	
	exec AddFileExtToLanguage 'Scala', 'yaml', 'SCALA_EXTENSIONS'
	exec AddFileExtToLanguage 'Scala', 'yml', 'SCALA_EXTENSIONS'
	exec AddFileExtToLanguage 'Scala', 'json', 'SCALA_EXTENSIONS'
	
	exec AddFileExtToLanguage 'Python', 'yaml', 'PYTHON_CORE_EXTENSIONS'
	exec AddFileExtToLanguage 'Python', 'yml', 'PYTHON_CORE_EXTENSIONS'
	exec AddFileExtToLanguage 'Python', 'json', 'PYTHON_CORE_EXTENSIONS'
```



   These commands will add ".properties", ".yml", ".yaml", and ".json" files to the scan so the
   queries can execute Regex searches on the contents.


7. Restart all IIS servers.

8. Adjust scanning presets on projects to include the new rules added in CxAudit.

9. Perform scans and inspect vulnerabilities reported with the new queries.



# General Comments

## Potential_Hardcoded_Passwords
Searching for password fields in files without a specification for the form of the
sensitive string will be prone to many false-positive and false-negatives.

The reason for false-positives is that there may be variables names matching
search names that aren't actually related to passwords or other sensitive data.

The reason for false-negatives is that it is possible to change config key values
or variable names to something that is not recognized as a potential element
that is exposing sensitive data.


## TruffleHog_Regex_Matches
The results from this query will likey be more accurate because it is searching
for concrete patterns that match sensitive data.  The only caveat to this is that
the Regex specifying the format needs to exist and be accurate.  

In at least two cases that are indicated in the list of TruffleHog queries incorporated
in the query, the TruffleHog Regexes were not formed to properly recognize general
matches.  The ability to recognize sensitive data is directly related to the ability
of the provided Regex to match the pattern of the sensitive data.

## TruffleHog_HighEntropy_Strings

### Things to know

* The TruffleHog project is moving away from using high entropy string detection in favor
of using regular expressions.  
* The high entropy detection method implemented in TruffleHog comes from a [blog post](http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html).
* There are some constants embedded in the TruffleHog code that are used as entropy thresholds.


### What does this mean?

While there is no denying that the TruffleHog implementation can detect some known secrets, it is hard to know which unknown secrets it can't detect.  False positives may not be as much of a concern until there are thousands to sift through.  It may be necessary to tune some of the different threshold parameters to dial down the amount false positives.  If you are implementing this CxQL query as part of your preset, you will have to perform any required tuning to make it work best for your scanned projects.

  
## Test Code
A directory of test code was provided to simulate the examples given for the CxQL
queries.  This can be opened with CxAudit to evaluate how the CxQL queries recognize
sensitive data.  The best test is known-vulnerable, real code to validate how the
sensitive data is reported as a result.
  

## False Negatives/Positives
A good way to see false negatives/positives is to run TruffleHog itself against the
CxPSPowerHacks repository to see what it detects:

```
docker run  dxa4481/trufflehog --entropy=True https://github.com/checkmarx-ts/CxPsPowerHacks.git
```

There are a few cases where the shorter passwords are not detected by the high-entropy sub-routines; this is a false
negative.  Running it with the `--regex` option can pick up some of the shorter passwords.

```
docker run  dxa4481/trufflehog --regex --entropy=True https://github.com/checkmarx-ts/CxPsPowerHacks.git
```

Running TruffleHog against your own branch, then running the TruffleHog CxQL queries during a scan should yield
similar results.


## Performance
The iterative nature of some of these queries may make them perform poorly.
