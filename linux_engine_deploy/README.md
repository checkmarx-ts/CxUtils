# linux_engine_deploy
linux engine deploy for 9.3 - AMAZON LINUX

install.sh installs docker from https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html you can skip that if docker is already installed.

## Steps
- Update CxEndpointIP to the IP of your CxManager (http not required, just the IP).
- Update NineThreeURL to the 9.3 installer (to unzip the engine).
- Update NineThreePassword to the password to unzip the installer.
- Update line 34 - 43 with server.env details specific from the readme packed with the linux engine via the 9.3 installer.

### From Readme
In order to retrieve its password, connect to CxSAST database, and execute the following SQL query:
```
  SELECT TOP (1000) [Id]
      ,[Key]
      ,[Value]
      ,[Description]
  FROM [CxDB].[dbo].[CxComponentConfiguration]
  where [Key] = 'MessageQueuePassword'
```

TODO
- Verify if it's possible 61616 port is inaccurate based on fresh installs.
- Add in error handling
- Check for docker
- Check if CxURL is responsive
- Add in engine registration and API calls 
- Add in kicking off a scan via API calls for smoke test to generate some results.
