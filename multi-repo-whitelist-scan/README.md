# multi-repo-whitelist-scan

This script is not supported by Checkmarx and edge cases are not tested.

The file bashCxCLI example uses the Checkmarx CLI to run a SAST scan on a folder that combines multiple repositiories of a whitelist of specific file extensions.
This should be used as an example only and the repositories, & user specific values need to be replaced.

Additional CxCLI commands can be found
https://checkmarx.atlassian.net/wiki/spaces/KC/pages/44335590/CxSAST+CLI+Plugin

#multirepoCxCLI.sh usage
Complete the following as shown in bashCxCLIexample.txt
* Install wget & unzip
```
git clone https://github.com/scxbush/multi-repo-whitelist-scan.git
cd multi-repo-whitelist-scan
```
* Download CxCLI & unzip
```
wget -O ./cli.zip https://download.checkmarx.com/8.9.0/Plugins/CxConsolePlugin-8.90.2.zip && unzip ./cli.zip && rm cli.zip
```
* Generate the CxCLI token replacing <> with your values
```
sh ./CxConsolePlugin-8.90.2/runCxConsole.sh GenerateToken -v -CxUser <yourusername> -CxPassword <yourpassword> -CxServer https://<yourcxserver>
```
* Add the following environment variables replacing <> with your values
  * CXSERVER=https://<mycheckmarxserver.net>
  * CXTOKEN=<5ee933c250fca59650db60a65a3b08b4>
  * PROJECT=<CxServer\\SP\\Company\\Users\\microservices-demo>
    * must escape \s in linux for fully qualified project name
* Edit the giturls.txt urls with your git repo urls
```
sh multirepoCxCLI.sh
```


