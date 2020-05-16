# CxSAST-Engine-Cleanup

This batch file is used to clean up scans & logs from CxSAST engine servers.
The script can be automated through windows task scheduler using the following instructions:

* Download and place this file on the desktop of the CxEngine you wish to clean up on a schedule
* Click on Start and under search, type in Task and click open Task Scheduler
* Select Create Basic Task from the Action pane on the right of the window
* Under Create Basic Task, type in "CxEngine-Cleanup" and click Next
* From the Trigger select "Weekly", click Next, select Saturday, and click Next
* Then click on Start a Program and click Next
* Now click on Browse and select Desktop then cxcleanup-engine.bat file
* Finally, click on Finish to create the Task

Now that we have created a Task, we have to make sure it runs with the highest privilege. Since we have UAC settings we have to make sure that when you run the file it should not fail if it does not bypass the UAC settings.

* Click on Task Scheduler Library and double click on "CxEngine-Cleanup"
* Click on Run with Highest privilege then click OK

You have successfully created a Scheduled Task to automate the CxSAST Engine Cleanup script.



