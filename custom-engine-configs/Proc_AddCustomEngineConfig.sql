CREATE OR ALTER PROCEDURE AddCustomEngineConfig
@CONFIG_NAME NVARCHAR(50),
@CONFIG_KEY  NVARCHAR(256),
@CONFIG_VALUE NVARCHAR(256)
AS
BEGIN

	DECLARE @Cfgid numeric(18,0);

	if EXISTS (SELECT Id FROM CxDB.Config.CxEngineConfiguration WHERE [Name] = @CONFIG_NAME)
	BEGIN
	  SELECT @CfgId = Id FROM CxDB.Config.CxEngineConfiguration WHERE [Name] = @CONFIG_NAME
	END
	ELSE
	BEGIN
		INSERT INTO CxDB.Config.CxEngineConfiguration (Name) VALUES (@CONFIG_NAME)
		SET @CfgId = @@IDENTITY
	END


	DECLARE @CfgValueid numeric(18,0);
	SELECT @CfgValueid = Id FROM [CxDB].[Config].[CxEngineConfigurationKeysMeta]
	WHERE KeyName = @CONFIG_KEY

	IF EXISTS (SELECT * FROM [CxDB].[Config].[CxEngineConfigurationValues] 
	WHERE ConfigurationId=@CfgId AND ConfigurationKeyId=@CfgValueid)
	BEGIN
		UPDATE [CxDB].[Config].[CxEngineConfigurationValues] SET [Value]=@CONFIG_VALUE
		WHERE ConfigurationId=@CfgId AND ConfigurationKeyId=@CfgValueid

	END
	ELSE
	BEGIN
		INSERT INTO [CxDB].[Config].[CxEngineConfigurationValues] (ConfigurationId,ConfigurationKeyId, Value)
		VALUES (@CfgId,@CfgValueid,@CONFIG_VALUE);
	END


END
