# CxSOAP API Examples
Checkmarx SOAP API Examples (8.X versions)

Examples:

- Powershell (Powershell/README.md):

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

- Postman Collection (Postman/README.md):

    - Login
    - Get All Teams
    - Get All Users
    - Get User By ID
    - Delete User By ID
    - Add New User - Server Manager
    - Add New User - SP Manager
    - Add New User - SP Manager - 2 Different SPs
    - Add New User - Company Manager
    - Add New User - Company Manager - 2 Different Companies
    - Add New User - Scanner
    - Add New User - Scanner - 2 Different Teams
    - Add New User - Scanner Delete
    - Add New User - Scanner Delete - 2 Different Teams
    - Add New User - Scanner NE
    - Add New User - Scanner NE - 2 Different Teams
    - Add New User - Scanner NE Delete
    - Add New User - Scanner NE Delete - 2 Different Teams
    - Add New User - Reviewer
    - Add New User - Reviewer - 2 Different Teams
    - Add New User - Reviewer Severity
    - Add New User - Reviewer Severity - 2 Different Teams
    - Update User

In order to build these scripts I had some help from the following endpoints available in 8.X Checkmarx Manager (replace "localhost" with your FQDN):

- Portal (MAIN):	http://localhost/CxWebInterface/Portal/CxWebService.asmx
- SDK:	http://localhost/CxWebInterface/SDK/CxSDKWebService.asmx
- Audit:	http://localhost/CxWebInterface/Audit/CxAuditWebService.asmx
- CLI V1:	http://localhost/CxWebInterface/CLI/CxCLIWebServiceV1.asmx
- CLI V0:	http://localhost/CxWebInterface/CLI/CxCLIWebService.asmx
- IntelliJ:	http://localhost/CxWebInterface/IntelliJ/CxIntelliJWebService.asmx
- Eclipse:	http://localhost/CxWebInterface/Eclipse/CxEclipseWebService.asmx
- Jenkins:	http://localhost/CxWebInterface/Jenkins/CxJenkinsWebService.asmx
- Priority:	http://localhost/CxWebInterface/Priority/CxPriorityService.asmx
- Sonar:	http://localhost/CxWebInterface/Sonar/CxSonarWebService.asmx
- VS:	http://localhost/CxWebInterface/VS/CxVSWebService.asmx

<strong>Note</strong>: Don't forget to have a look over the WSDL to see what is the expected format and structure. If you wanna convert automatically all of the SOAP calls to Postman format, please have a look over my other project called "wsdl2postman": https://github.com/miguelfreitas93/wsdl2postman

# Related projects & Credit
Samples taken from @miguelfreitas93 below
- https://github.com/miguelfreitas93/CxSOAP-API-Examples


# License

MIT License

Copyright (c) 2020 Miguel Freitas
