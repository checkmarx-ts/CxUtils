# CxSOAP API Examples - Postman

This collection contains the following Checkmarx SOAP API examples:

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

### Available Roles in 8.X Checkmarx Versions:

- Server Manager
- SP Manager
- Company Manager
- Scanner
- Scanner with Permissions to Delete Projects\Scans (Delete)
- Scanner with Permissions to Apply Not Exploitable State (NE)
- Scanner with Permissions to Apply Not Exploitable State and to Delete Projects\Scans (NE Delete)
- Reviewer
- Reviewer with Permissions to change Severity\Status

### Limitations

Regarding these roles, there are some limitations on 8.X versions, such as:

- User <strong>CANNOT</strong> have at same time:
    - Server Manager and SP Manager role
    - Server Manager and Company Manager role
    - Server Manager and any Scanner role
    - Server Manager and any Reviewer role
    - SP Manager and Company Manager role
    - SP Manager and any Scanner role
    - SP Manager and any Reviewer role
    - Company Manager and any Scanner role
    - Company Manager and any Reviewer role
    - Any Scanner and Any Reviewer role
- If user belong to 2 different Teams, we needs to have the <strong>same role in both</strong> and those teams should have the same permissions levels

<strong>NOTE:</strong> These limitations will be overcome in next version 9.0 with a new Access Control which implements a RBAC Authorization mechanism, so users won't be restricted in the roles and permissions they can tie to an user.

### Postman

In this folder you can find 2 artifacts:

- Postman Collection (Checkmarx APIs.postman_collection.json), to be imported in Postman Collections section
- Postman Enviroments (SOAP UI Examples.postman_environment.json), to be imported in Postman Enviroments section

Please find more info here: https://learning.postman.com/docs/postman/collection-runs/working-with-data-files/



# License

MIT License

Copyright (c) 2020 Miguel Freitas