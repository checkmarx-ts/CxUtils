# user-type-migration

Checkmarx CxSAST supports application users (internal username and passwords), Active Directory, LDAP, and SAML user types. A user's type defines how the user will authenticate to their CxSAST account. Once a user has been added it's type cannot be changed through the application UI. However, it is possible to migrate user types on the backend in the database. This page explains how to do this.

Consult with Checkmarx Professional Services on user migration assitance before using this process. Do not use this process unless directed or referred to it by Checkmarx. This tool is highly dependent on the database schema version and may need to be modified for your Checkmarx system. 

This process works for CxSAST v8.9 HF7. It will likely work or be able to work with some modification for other version of 8.9. 

You should become familiar with this process and its limitations before you begin.

# How to migrate users from one type to another (e.g. LDAP to SAML).

At a high level you will need to: 

1. Prepare your authentication providers
1. Map your users to their new type and create a CSV mapping file.
1. Generate the SQL migration script
1. Execute the SQL in a maintenance window

The most difficult part of this is mapping your users. Follow the detailed steps outlined below to begin.

## Prepare your authentication providers

Configure your target authentication providers ahead of time whether you are migrating to SAML, LDAP, or Active Directory. 

* [SAML](https://checkmarx.atlassian.net/wiki/spaces/KC/pages/1243415011/SAML+Integration)
* [LDAP](https://checkmarx.atlassian.net/wiki/spaces/KC/pages/126917112/LDAP+Management)

## Map your users to their new type and create a CSV mapping file

Use this SQL query to extract your current users and map them to their future state. Delete any rows for users who you do not want to change. Use SQL Server Management Studio to run this and save the results for analysis in Excel.
```sql
select  u.username as 'before_username', 
ut.Type as 'before_usertype', 
u.FirstName as 'before_fname', 
u.LastName as 'before_lname', 
'?' as 'after_username', 
'?' as 'after_usertype', 
u.id, u.Email, u.upn, u.LastLoginDate
from cxdb.dbo.users u inner join cxdb.dbo.UserType ut on u.id = ut.UserId
where u.is_deprecated = 0;
```

Load the results into Excel and review it to create a CSV file with this sample structure.
```
before_username, before_usertype, before_fname, before_lname, after_username, after_usertype

# (Example) LDAP to SAML
"corp2\jdoe", "5", "John", "Doe", "SAML\jdoe@checkmarx.com", "6" 

# (Example) SAML to LDAP
"SAML\jdoe@checkmarx.com", "6" , "Jane", "Doe", "corp2\jdoe", "5"
```

Note: This example is annotated with `#` indicating a comment line. Your CSV file should not actually have comments.

The CSV fields are defined as:

Field | Description
--------|------------
before_username | The username as it currently is in the database. Obtain this from the SQL query and do not change it.
before_usertype | The user type ID as it currently is in the database. Obtain this from the SQL query and do not change it.
before_fname | The user first name as it currently is in the database. Obtain this from the SQL query and do not change it.
before_lname | The user last name as it currently is in the database. Obtain this from the SQL query and do not change it.
after_username | The new user name that you want the user to have. Chose this value based on the target user type (guidance below).
after_usertype | The new user type id that you want the user to have. Chose this value based on the target user type (guidance below).

### Specifying after_username and after_usertype values
The `after_username` field needs to be specially formatted when migrating users to SAML, LDAP, and Active Directory. `after_usertype` must be set to an ID corresonding to the type of user.

#### SAML
 SAML usernames take the form of `SAML\$username` where `$username` is the subject identifier (`NameID`) sent to Checkmarx by your Identity Provider. This is usually, but not always, the user's email address. For example: `SAML\jdoe@checkmarx.com`. If you are not sure what your SAML `$username` will be then create a test SAML user and look at what your Identity Provider uses or ask your SAML team.

 Note: Usernames begin with the literal string `SAML` - this is not a place holder value.

The `after_usertype` value for SAML is `6`.

#### LDAP
LDAP usernames take the form of `$corp\$username` where `$corp` is the name of the configured LDAP server within Checkmarx and `$username` is the configured `User Name Attribute` for the LDAP server connection within Checkmarx (sometimes `sAMAccountName`). For example: `checkmarx\jdoe`.

The `after_usertype` value for LDAP is `5`.

#### Active Directory
Active Directory usernames take the form of `$corp\$username` where `$corp` is the short name of the domain and `$username` is the user's domain name. For example: `checkmarx\jdoe`.

The `after_usertype` value for Active Directory is `1`.

## Generate the SQL migration script
Use the `generate-usertype-migration-sql.ps1` to generate the SQL statements needed to migrate your users based on the CSV mapping you have created.

Run this command passing your CSV file as input and saving the output to a file.

```.\generate-usertype-migration-sql.ps1 -MappingFile .\user-map.csv.txt | Out-File -Append user-migration.sql```

Review the generated SQL. Notice it has two transactions - one for CxDB and one for CxARM. The CxARM transaction is only applicable if you have the CxSAST M&O Feature installed. 

Here is an **example** output:

```sql
/*
  This is a T-SQL script to migrate users from one type to another intended for use with Checkmarx CxSAST 8.9 HF7. 
  This block takes care of the CxDB database.
*/
USE [CxDB]
GO
BEGIN TRANSACTION;
BEGIN TRY  
    /* corp2\nsekots with usertype 5 migrating to SAML\nebsekots@checkmarx.com with usertype 6 */
    -- Update user type
        update CxDB.dbo.Users set [UserName] = 'SAML\nebsekots@checkmarx.com'  where [UserName] = 'corp2\nsekots'
    update CxDB.dbo.UserType set [UserName] = 'SAML\nebsekots@checkmarx.com', [Type] = 6 where [UserName] = 'corp2\nsekots'


    -- Update references
        update CxDB.dbo.ProjectOpenSourceSettings set [Username] = 'SAML\nebsekots@checkmarx.com' where [Username] = 'corp2\nsekots'
    update CxDB.dbo.Query set [CurrentUserName] = 'SAML\nebsekots@checkmarx.com' where [CurrentUserName] = 'corp2\nsekots'
    update CxDB.dbo.Auxiliary_Query set [CurrentUserName] = 'SAML\nebsekots@checkmarx.com' where [CurrentUserName] = 'corp2\nsekots'
    update CxDB.dbo.ScanActions set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.FailedScans set [Initiator] = 'SAML\nebsekots@checkmarx.com' where [Initiator] = 'corp2\nsekots'
    update CxDB.dbo.QueryTemp set [CurrentUserName] = 'SAML\nebsekots@checkmarx.com' where [CurrentUserName] = 'corp2\nsekots'
    update CxDB.dbo.QueryVersion_bck set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.QueryVersion set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.Tasks_Legacy set [OpenedBy] = 'SAML\nebsekots@checkmarx.com' where [OpenedBy] = 'corp2\nsekots'
    update CxDB.dbo.DataRetentionRequests set [InitiatorName] = 'SAML\nebsekots@checkmarx.com' where [InitiatorName] = 'corp2\nsekots'
    update CxDB.dbo.Projects set [OpenedBy] = 'SAML\nebsekots@checkmarx.com' where [OpenedBy] = 'corp2\nsekots'
    update CxDB.dbo.Origins set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.ScanRiskLevel set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.Config.CxProgramLanguages set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.Config.CxFileExtensionOwner set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.PivotLayouts set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.ConfigutaionsGroups set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.FailedScans set [Owner] = 'SAML\nebsekots@checkmarx.com' where [Owner] = 'corp2\nsekots'
    update CxDB.dbo.TaskScans set [Owner] = 'SAML\nebsekots@checkmarx.com' where [Owner] = 'corp2\nsekots'
    update CxDB.dbo.Presets set [Owner] = 'SAML\nebsekots@checkmarx.com' where [Owner] = 'corp2\nsekots'
    update CxDB.dbo.ScansReports set [OwningUser] = 'SAML\nebsekots@checkmarx.com' where [OwningUser] = 'corp2\nsekots'
    update CxDB.dbo.ScanRequests set [UserName] = 'SAML\nebsekots@checkmarx.com' where [UserName] = 'corp2\nsekots'
    update CxDB.dbo.ScanRequests set [Owner] = 'SAML\nebsekots@checkmarx.com' where [Owner] = 'corp2\nsekots'
    update CxDB.dbo.ResultsLabelsHistory set [CreatedBy] = 'SAML\nebsekots@checkmarx.com' where [CreatedBy] = 'corp2\nsekots'
    update CxDB.dbo.CanceledScans set [Owner] = 'SAML\nebsekots@checkmarx.com' where [Owner] = 'corp2\nsekots'
    update CxDB.dbo.PendingUsers set [UserName] = 'SAML\nebsekots@checkmarx.com' where [UserName] = 'corp2\nsekots'
    update CxDB.dbo.Configurations set [Owner] = 'SAML\nebsekots@checkmarx.com' where [Owner] = 'corp2\nsekots'
    update CxDB.dbo.PostScanActions set [Owner] = 'SAML\nebsekots@checkmarx.com' where [Owner] = 'corp2\nsekots'
    update CxDB.dbo.Projects set [Owner] = 'SAML\nebsekots@checkmarx.com' where [Owner] = 'corp2\nsekots'
    update CxDB.dbo.Tasks_Legacy set [Owner] = 'SAML\nebsekots@checkmarx.com' where [Owner] = 'corp2\nsekots'
    update CxDB.dbo.ResultsLabels set [UpdatingUser] = 'SAML\nebsekots@checkmarx.com' where [UpdatingUser] = 'corp2\nsekots'
    update CxDB.dbo.TaskScans set [InitiatorName] = 'SAML\nebsekots@checkmarx.com' where [InitiatorName] = 'corp2\nsekots'
    update CxDB.dbo.LoggedinUser set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.QueryVersion_bck set [CurrentUserName] = 'SAML\nebsekots@checkmarx.com' where [CurrentUserName] = 'corp2\nsekots'
    update CxDB.dbo.QueryTemp set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.Presets set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.Projects set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.Query set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.Auxiliary_Query set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.QueryVersion set [CurrentUserName] = 'SAML\nebsekots@checkmarx.com' where [CurrentUserName] = 'corp2\nsekots'
    update CxDB.dbo.ResultState set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'
    update CxDB.dbo.Configurations set [Name] = 'SAML\nebsekots@checkmarx.com' where [Name] = 'corp2\nsekots'


    -- result labels special cases

   update CxDB.dbo.ResultsLabelsHistory set [Data] = 'Neb Sekots   (SAML\nebsekots@checkmarx.com)' where [Data] = 'Neb Sekots   (corp2\nsekots)'
   update CxDB.dbo.ResultsLabelsHistory  set [Data] = 'Assigned to Neb Sekots   (SAML\nebsekots@checkmarx.com)' where [Data] = 'Assigned to Neb Sekots   (corp2\nsekots)'
   
   update CxDB.dbo.ResultsLabels set [StringData] = 'Neb Sekots   (SAML\nebsekots@checkmarx.com)'  where [StringData]  = 'Neb Sekots   (corp2\nsekots)'  and labeltype = 4;
   update CxDB.dbo.ResultsLabels set [StringData] = 'Assigned to Neb Sekots   (SAML\nebsekots@checkmarx.com)'  where [StringData]  =  'Assigned to Neb Sekots   (corp2\nsekots)'  and labeltype = 1;



END TRY
BEGIN CATCH  
	print 'an error has occured'
    SELECT   
        ERROR_NUMBER() AS ErrorNumber  
        ,ERROR_SEVERITY() AS ErrorSeverity  
        ,ERROR_STATE() AS ErrorState  
        ,ERROR_PROCEDURE() AS ErrorProcedure  
        ,ERROR_LINE() AS ErrorLine  
        ,ERROR_MESSAGE() AS ErrorMessage;  
  
    IF @@TRANCOUNT > 0  
	BEGIN
		print concat('transaction count: ', @@TRANCOUNT)
	    print 'Rolling back'
        ROLLBACK TRANSACTION;  
	END
END CATCH;

print concat('transaction count: ', @@TRANCOUNT)  

IF @@TRANCOUNT > 0 
BEGIN  
  print 'Committing'
  COMMIT TRANSACTION;
END


/*



*/

/*
  This is a T-SQL script to migrate users from one type to another intended for use with Checkmarx CxSAST 8.9 HF7. 
  This block takes care of the CxARM database.
*/
USE [CxARM]
GO
BEGIN TRANSACTION;
BEGIN TRY  
    /* corp2\nsekots with usertype 5 migrating to SAML\nebsekots@checkmarx.com with usertype 6 */
    update [CxARM].[dbo].[Users] set [UserName] = 'SAML\nebsekots@checkmarx.com' where [UserName] = 'corp2\nsekots'

END TRY
BEGIN CATCH  
	print 'an error has occured'
    SELECT   
        ERROR_NUMBER() AS ErrorNumber  
        ,ERROR_SEVERITY() AS ErrorSeverity  
        ,ERROR_STATE() AS ErrorState  
        ,ERROR_PROCEDURE() AS ErrorProcedure  
        ,ERROR_LINE() AS ErrorLine  
        ,ERROR_MESSAGE() AS ErrorMessage;  
  
    IF @@TRANCOUNT > 0  
	BEGIN
		print concat('transaction count: ', @@TRANCOUNT)
	    print 'Rolling back'
        ROLLBACK TRANSACTION;  
	END
END CATCH;

print concat('transaction count: ', @@TRANCOUNT)  

IF @@TRANCOUNT > 0 
BEGIN  
  print 'Committing'
  COMMIT TRANSACTION;
END
```

## Execute the SQL in a maintenance window

At this point you have mapped your users in the CSV file and have a SQL migration script ready to run. The actual migration should run during a maintenance window when no one is using Checkmarx. You should also have a database backup and be ready to smoke test the migration. You may need to have some additional personnel available to help smoke test and troubleshoot. Make sure to create a database back up that you can rollback to in case anything goes wrong.

Prior to the maintenance window make sure you have configured any new authentication mechanisms you will be using.

Perform these steps within a maintenance window:
1. Shutdown the Checkmarx services
1. Take all Checkmarx databases offline (CxDB, CxARM, CxActivity)
1. Back up all Checkmarx databases (CxDB, CxARM, CxActivity)
1. Run the SQL migration script
1. Start the Checkmarx services
1. Smoke test the application, ensuring you can log in as the migrated users

If anything goes wrong, restore the database backups 

# Limitations

* Externalized team and role assignment is not supported in this process. If you need these features you should first migrate your users and then begin using whatever features of the users' new authentication type you require. 

* This approach works with CxSAST 8.9 HF7. 



