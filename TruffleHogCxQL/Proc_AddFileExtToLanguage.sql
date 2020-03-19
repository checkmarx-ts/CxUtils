CREATE OR ALTER PROCEDURE AddFileExtToLanguage
@LANGUAGE NVARCHAR(50),
@EXTENSION  NVARCHAR(50),
@LANG_GROUP NVARCHAR(50)
AS
BEGIN
	DECLARE @PLG_ID BIGINT
	DECLARE @PLG_NAME NVARCHAR(50)
	DECLARE @PLG_OWNER BIGINT
	DECLARE @EXT_COUNT INT

    
SET @EXT_COUNT = (
    SELECT Count(*)
      FROM CxDB.Config.CxProgramLanguageGroups plg
      JOIN CxDB.Config.CxProgramLanguages pl on plg.ProgramLanguageId = pl.Id
      JOIN CxDB.Config.CxFileExtension fe on fe.ProgramLanguageGroupId = plg.Id
     WHERE pl.[Name] LIKE @LANGUAGE AND fe.Value LIKE '.'+@EXTENSION)
  
IF @EXT_COUNT = 0
BEGIN
    SET @PLG_OWNER = (SELECT ID FROM CxDB.Config.CxFileExtensionOwner WHERE Name ='Checkmarx')
     
	SELECT @PLG_ID = plg.Id, @PLG_NAME = pl.[Name]
          FROM CxDB.Config.CxProgramLanguageGroups plg
          JOIN CxDB.Config.CxProgramLanguages pl on plg.ProgramLanguageId = pl.Id
         WHERE plg.[Name] LIKE @LANG_GROUP
      
    INSERT INTO CxDB.Config.CxFileExtension (
        ProgramLanguageGroupId,
        FileExtensionOwnerId,
        Symbol,
        Value,
        [Enable])
    VALUES(
        @PLG_ID,
        @PLG_OWNER,
        UPPER(@PLG_NAME+ '_' + @EXTENSION),
        '.'+@EXTENSION,
        NULL)
END
END
