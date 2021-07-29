# Custom Engine Configurations

A database update is required to create custom engine configurations or to modify existing engine configurations in CxSAST.  The `AddCustomEngineConfig` stored procedure when added to `CxDB` will create and/or update any named engine configuration.


**CAUTION**: Engine configuration changes should be done with the guidance of Checkmarx.  Some of the configuration options can impact the accuracy and performance of scans if not configured correctly.

After creating or updating an engine configuration, restart all SAST services and IIS.


# Examples


## CxQL Debug and Bad Files to Scan Logs

This updates a configuration to add a list of files the scan considered as bad (e.g. not parsed properly) as well as show any debug output embedded in CxQL queries.

```
EXEC AddCustomEngineConfig '<your configuration name>', 'PRINT_DEBUG', 'true'
EXEC AddCustomEngineConfig '<your configuration name>', 'PRINT_BAD_FILES', 'true'

```

## Enable Improved Flow Algoritm in v9.3+

The Lazy Flow algorithm improves scan performance.  It is not turned on by default in v9.3, and may be off on systems that upgraded to v9.4.  A custom engine configuration can be created that allows evaluation of the algorithm on per-project basis by modifying the engine configuration


```
EXEC AddCustomEngineConfig 'Improved Flow', 'USE_LAZY_FLOW', 'true'
```


