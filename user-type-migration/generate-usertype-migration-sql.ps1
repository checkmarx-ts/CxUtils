
param (
    [Parameter(Mandatory = $True, ParameterSetName = "Flags")] [String] $MappingFile
  )
  
  Write-Output @"
  /*
    This is a T-SQL script to migrate users from one type to another intended for use with Checkmarx CxSAST 8.9 HF7. 
    This block takes care of the CxDB database.
  */
  USE [CxDB]
  GO
  BEGIN TRANSACTION;
  BEGIN TRY  
  "@
  
  Import-Csv -Path $MappingFile | ForEach-Object {
  
  $cxdb_users_usertype_updates = @"
      update CxDB.dbo.Users set [UserName] = '$($_.after_username)'  where [UserName] = '$($_.before_username)'
      update CxDB.dbo.UserType set [UserName] = '$($_.after_username)', [Type] = $($_.after_usertype) where [UserName] = '$($_.before_username)'
  
  "@
  
  
  $cxdb_username_ref_updates = @"
      update CxDB.dbo.ProjectOpenSourceSettings set [Username] = '$($_.after_username)' where [Username] = '$($_.before_username)'
      update CxDB.dbo.Query set [CurrentUserName] = '$($_.after_username)' where [CurrentUserName] = '$($_.before_username)'
      update CxDB.dbo.Auxiliary_Query set [CurrentUserName] = '$($_.after_username)' where [CurrentUserName] = '$($_.before_username)'
      update CxDB.dbo.ScanActions set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.FailedScans set [Initiator] = '$($_.after_username)' where [Initiator] = '$($_.before_username)'
      update CxDB.dbo.QueryTemp set [CurrentUserName] = '$($_.after_username)' where [CurrentUserName] = '$($_.before_username)'
      update CxDB.dbo.QueryVersion_bck set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.QueryVersion set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.Tasks_Legacy set [OpenedBy] = '$($_.after_username)' where [OpenedBy] = '$($_.before_username)'
      update CxDB.dbo.DataRetentionRequests set [InitiatorName] = '$($_.after_username)' where [InitiatorName] = '$($_.before_username)'
      update CxDB.dbo.Projects set [OpenedBy] = '$($_.after_username)' where [OpenedBy] = '$($_.before_username)'
      update CxDB.dbo.Origins set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.ScanRiskLevel set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.Config.CxProgramLanguages set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.Config.CxFileExtensionOwner set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.PivotLayouts set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.ConfigutaionsGroups set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.FailedScans set [Owner] = '$($_.after_username)' where [Owner] = '$($_.before_username)'
      update CxDB.dbo.TaskScans set [Owner] = '$($_.after_username)' where [Owner] = '$($_.before_username)'
      update CxDB.dbo.Presets set [Owner] = '$($_.after_username)' where [Owner] = '$($_.before_username)'
      update CxDB.dbo.ScansReports set [OwningUser] = '$($_.after_username)' where [OwningUser] = '$($_.before_username)'
      update CxDB.dbo.ScanRequests set [UserName] = '$($_.after_username)' where [UserName] = '$($_.before_username)'
      update CxDB.dbo.ScanRequests set [Owner] = '$($_.after_username)' where [Owner] = '$($_.before_username)'
      update CxDB.dbo.ResultsLabelsHistory set [CreatedBy] = '$($_.after_username)' where [CreatedBy] = '$($_.before_username)'
      update CxDB.dbo.CanceledScans set [Owner] = '$($_.after_username)' where [Owner] = '$($_.before_username)'
      update CxDB.dbo.PendingUsers set [UserName] = '$($_.after_username)' where [UserName] = '$($_.before_username)'
      update CxDB.dbo.Configurations set [Owner] = '$($_.after_username)' where [Owner] = '$($_.before_username)'
      update CxDB.dbo.PostScanActions set [Owner] = '$($_.after_username)' where [Owner] = '$($_.before_username)'
      update CxDB.dbo.Projects set [Owner] = '$($_.after_username)' where [Owner] = '$($_.before_username)'
      update CxDB.dbo.Tasks_Legacy set [Owner] = '$($_.after_username)' where [Owner] = '$($_.before_username)'
      update CxDB.dbo.ResultsLabels set [UpdatingUser] = '$($_.after_username)' where [UpdatingUser] = '$($_.before_username)'
      update CxDB.dbo.TaskScans set [InitiatorName] = '$($_.after_username)' where [InitiatorName] = '$($_.before_username)'
      update CxDB.dbo.LoggedinUser set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.QueryVersion_bck set [CurrentUserName] = '$($_.after_username)' where [CurrentUserName] = '$($_.before_username)'
      update CxDB.dbo.QueryTemp set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.Presets set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.Projects set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.Query set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.Auxiliary_Query set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.QueryVersion set [CurrentUserName] = '$($_.after_username)' where [CurrentUserName] = '$($_.before_username)'
      update CxDB.dbo.ResultState set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
      update CxDB.dbo.Configurations set [Name] = '$($_.after_username)' where [Name] = '$($_.before_username)'
  
  
      -- result labels special cases
  
     update CxDB.dbo.ResultsLabelsHistory set [Data] = '$($_.before_fname) $($_.before_lname)   ($($_.after_username))' where [Data] = '$($_.before_fname) $($_.before_lname)   ($($_.before_username))'
     update CxDB.dbo.ResultsLabelsHistory  set [Data] = 'Assigned to $($_.before_fname) $($_.before_lname)   ($($_.after_username))' where [Data] = 'Assigned to $($_.before_fname) $($_.before_lname)   ($($_.before_username))'
     
     update CxDB.dbo.ResultsLabels set [StringData] = '$($_.before_fname) $($_.before_lname)   ($($_.after_username))'  where [StringData]  = '$($_.before_fname) $($_.before_lname)   ($($_.before_username))'  and labeltype = 4;
     update CxDB.dbo.ResultsLabels set [StringData] = 'Assigned to $($_.before_fname) $($_.before_lname)   ($($_.after_username))'  where [StringData]  =  'Assigned to $($_.before_fname) $($_.before_lname)   ($($_.before_username))'  and labeltype = 1;
  
  "@
  
  Write-Output @"
      /* $($_.before_username) with usertype $($_.before_usertype) migrating to $($_.after_username) with usertype $($_.after_usertype) */
      -- Update user type
      $cxdb_users_usertype_updates
  
      -- Update references
      $cxdb_username_ref_updates
  
  
  "@
  
  }
  
  Write-Output @"
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
  
  "@
  
  
  Write-Output @"
  
  /*
  
  
  
  */
  
  "@
  
  
  
  
  
  
  Write-Output @"
  /*
    This is a T-SQL script to migrate users from one type to another intended for use with Checkmarx CxSAST 8.9 HF7. 
    This block takes care of the CxARM database.
  */
  USE [CxARM]
  GO
  BEGIN TRANSACTION;
  BEGIN TRY  
  "@
  
  Import-Csv -Path $MappingFile | ForEach-Object {
  
  Write-Output @"
      /* $($_.before_username) with usertype $($_.before_usertype) migrating to $($_.after_username) with usertype $($_.after_usertype) */
      update [CxARM].[dbo].[Users] set [UserName] = '$($_.after_username)' where [UserName] = '$($_.before_username)'
  
  "@
  }
  
  Write-Output @"
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
  
  "@