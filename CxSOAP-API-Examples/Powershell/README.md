# CxSOAP API Examples - Powershell

This folder contains the following Checkmarx SOAP API examples:

    - Add Comment to Results
    - Add New Application User Company Manager to Multiple Companies
    - Add New Application User Company Manager to Company
    - Add New Application User Reviewer with Severity Permissions to Team
    - Add New Application User Reviewer to Multiple Teams
    - Add New Application User Reviewer to Team
    - Add New Application User Scanner with Delete and Not Exploitable Permissions to Team
    - Add New Application User Scanner with Delete Permissions to Team
    - Add New Application User Scanner with Not Exploitable Permissions to Team
    - Add New Application User Scanner to Multiple Teams
    - Add New Application User Scanner to Team
    - Add New Application User Server Manager to Team
    - Add New Application User SP Manager to Multiple SPs
    - Add New Application User SP Manager to SP
    - Add Team to User
    - Change Assignee of Results
    - Change Severity of Results
    - Change State of Results
    - Create Empty Preset
    - Create Empty Preset Parameterized
    - Delete Preset
    - Delete Preset Parameterized
    - Delete User
    - Duplicate Preset
    - Duplicate Preset Parameterized
    - Get All Teams
    - Get All Users
    - Get Branch Projects
    - Get Customized Queries
    - Get Last Scan Results
    - Get List of Inactive Users
    - Get Presets
    - Get User
    - Login
    - Rename Preset
    - Rename Preset Parameterized

# Security

In order to not have hardcoded passwords in these scripts, "CredentialManager" module is being used for that purpose. This module retrieves Username and Password from Credential Manager in Windows. To use this module, it is required to install it beforehand, running the following command:

```ps1
Install-Module -Name "CredentialManager"
```

This package might require some permissions that need to be accepted during installation. 

Please find here, how to add credentials to Credentials Manager Vault: https://www.howtogeek.com/106906/how-to-add-credentials-to-the-windows-credential-manager-vault/

# Why Powershell ?

Usually for automation scripts regarding Checkmarx, Powershell is the selected language because of the machine's restrictions hosting Checkmarx, such as:

- No internet connectivity - so Node JS or Python <strong>CANNOT</strong> be installed there
- Cannot install anything on servers due to Company's policy - usually companies have a policy that any 3rd party software cannot be installed on their machines
- Powershell is the easiest scripting language available for doing automation.


# License

MIT License

Copyright (c) 2020 Miguel Freitas