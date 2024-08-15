"""
========================================================================

CXQL QUERIES CATERGORIES FROM SAST V 9.4.5
 
antonio.silva@checkmarx.com
PS-EMEA
31-08-2023
 
The collections were retieved from fresh installed/upgraded SAST version

========================================================================
"""

# Default query categories, out-of-the box
# From SAST 9.4.5

default_categories_945 = [
  {
    "Id": 1,
    "CategoryName": "Must audit",
    "CategoryType": {
      "Id": 1,
      "Name": "Custom",
      "Order": 30
    }
  },
  {
    "Id": 2,
    "CategoryName": "Check",
    "CategoryType": {
      "Id": 1,
      "Name": "Custom",
      "Order": 30
    }
  },
  {
    "Id": 3,
    "CategoryName": "Optional",
    "CategoryType": {
      "Id": 1,
      "Name": "Custom",
      "Order": 30
    }
  },
  {
    "Id": 4,
    "CategoryName": "PCI DSS (3.2.1) - 6.5.1 - Injection flaws - particularly SQL injection",
    "CategoryType": {
      "Id": 2,
      "Name": "PCI DSS v3.2.1",
      "Order": 20
    }
  },
  {
    "Id": 5,
    "CategoryName": "PCI DSS (3.2.1) - 6.5.2 - Buffer overflows",
    "CategoryType": {
      "Id": 2,
      "Name": "PCI DSS v3.2.1",
      "Order": 20
    }
  },
  {
    "Id": 6,
    "CategoryName": "PCI DSS (3.2.1) - 6.5.3 - Insecure cryptographic storage",
    "CategoryType": {
      "Id": 2,
      "Name": "PCI DSS v3.2.1",
      "Order": 20
    }
  },
  {
    "Id": 7,
    "CategoryName": "PCI DSS (3.2.1) - 6.5.4 - Insecure communications",
    "CategoryType": {
      "Id": 2,
      "Name": "PCI DSS v3.2.1",
      "Order": 20
    }
  },
  {
    "Id": 8,
    "CategoryName": "PCI DSS (3.2.1) - 6.5.5 - Improper error handling",
    "CategoryType": {
      "Id": 2,
      "Name": "PCI DSS v3.2.1",
      "Order": 20
    }
  },
  {
    "Id": 9,
    "CategoryName": "PCI DSS (3.2.1) - 6.5.7 - Cross-site scripting (XSS)",
    "CategoryType": {
      "Id": 2,
      "Name": "PCI DSS v3.2.1",
      "Order": 20
    }
  },
  {
    "Id": 10,
    "CategoryName": "PCI DSS (3.2.1) - 6.5.8 - Improper access control",
    "CategoryType": {
      "Id": 2,
      "Name": "PCI DSS v3.2.1",
      "Order": 20
    }
  },
  {
    "Id": 11,
    "CategoryName": "PCI DSS (3.2.1) - 6.5.9 - Cross-site request forgery",
    "CategoryType": {
      "Id": 2,
      "Name": "PCI DSS v3.2.1",
      "Order": 20
    }
  },
  {
    "Id": 12,
    "CategoryName": "PCI DSS (3.2.1) - 6.5.10 - Broken authentication and session management",
    "CategoryType": {
      "Id": 2,
      "Name": "PCI DSS v3.2.1",
      "Order": 20
    }
  },
  {
    "Id": 13,
    "CategoryName": "A1-Injection",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 14,
    "CategoryName": "A2-Broken Authentication and Session Management",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 15,
    "CategoryName": "A3-Cross-Site Scripting (XSS)",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 16,
    "CategoryName": "A4-Insecure Direct Object References",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 17,
    "CategoryName": "A5-Security Misconfiguration",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 18,
    "CategoryName": "A6-Sensitive Data Exposure",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 19,
    "CategoryName": "A7-Missing Function Level Access Control",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 20,
    "CategoryName": "A8-Cross-Site Request Forgery (CSRF)",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 21,
    "CategoryName": "A9-Using Components with Known Vulnerabilities",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 22,
    "CategoryName": "A10-Unvalidated Redirects and Forwards",
    "CategoryType": {
      "Id": 3,
      "Name": "OWASP Top 10 2013",
      "Order": 10
    }
  },
  {
    "Id": 23,
    "CategoryName": "Access Control",
    "CategoryType": {
      "Id": 4,
      "Name": "FISMA 2014",
      "Order": 22
    }
  },
  {
    "Id": 24,
    "CategoryName": "Audit And Accountability",
    "CategoryType": {
      "Id": 4,
      "Name": "FISMA 2014",
      "Order": 22
    }
  },
  {
    "Id": 25,
    "CategoryName": "Configuration Management",
    "CategoryType": {
      "Id": 4,
      "Name": "FISMA 2014",
      "Order": 22
    }
  },
  {
    "Id": 26,
    "CategoryName": "Identification And Authentication",
    "CategoryType": {
      "Id": 4,
      "Name": "FISMA 2014",
      "Order": 22
    }
  },
  {
    "Id": 27,
    "CategoryName": "Media Protection",
    "CategoryType": {
      "Id": 4,
      "Name": "FISMA 2014",
      "Order": 22
    }
  },
  {
    "Id": 28,
    "CategoryName": "System And Communications Protection",
    "CategoryType": {
      "Id": 4,
      "Name": "FISMA 2014",
      "Order": 22
    }
  },
  {
    "Id": 29,
    "CategoryName": "System And Information Integrity",
    "CategoryType": {
      "Id": 4,
      "Name": "FISMA 2014",
      "Order": 22
    }
  },
  {
    "Id": 30,
    "CategoryName": "AC-12 Session Termination (P2)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 31,
    "CategoryName": "AC-3 Access Enforcement (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 32,
    "CategoryName": "AC-4 Information Flow Enforcement (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 33,
    "CategoryName": "AC-6 Least Privilege (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 34,
    "CategoryName": "AU-9 Protection of Audit Information (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 35,
    "CategoryName": "CM-6 Configuration Settings (P2)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 36,
    "CategoryName": "IA-5 Authenticator Management (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 37,
    "CategoryName": "IA-6 Authenticator Feedback (P2)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 38,
    "CategoryName": "IA-8 Identification and Authentication (Non-Organizational Users) (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 39,
    "CategoryName": "SC-12 Cryptographic Key Establishment and Management (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 40,
    "CategoryName": "SC-13 Cryptographic Protection (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 41,
    "CategoryName": "SC-17 Public Key Infrastructure Certificates (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 42,
    "CategoryName": "SC-18 Mobile Code (P2)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 43,
    "CategoryName": "SC-23 Session Authenticity (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 44,
    "CategoryName": "SC-28 Protection of Information at Rest (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 45,
    "CategoryName": "SC-4 Information in Shared Resources (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 46,
    "CategoryName": "SC-5 Denial of Service Protection (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 47,
    "CategoryName": "SC-8 Transmission Confidentiality and Integrity (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 48,
    "CategoryName": "SI-10 Information Input Validation (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 49,
    "CategoryName": "SI-11 Error Handling (P2)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 50,
    "CategoryName": "SI-15 Information Output Filtering (P0)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 51,
    "CategoryName": "SI-16 Memory Protection (P1)",
    "CategoryType": {
      "Id": 5,
      "Name": "NIST SP 800-53",
      "Order": 23
    }
  },
  {
    "Id": 52,
    "CategoryName": "A1-Injection",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 53,
    "CategoryName": "A2-Broken Authentication",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 54,
    "CategoryName": "A3-Sensitive Data Exposure",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 55,
    "CategoryName": "A4-XML External Entities (XXE)",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 56,
    "CategoryName": "A5-Broken Access Control",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 57,
    "CategoryName": "A6-Security Misconfiguration",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 58,
    "CategoryName": "A7-Cross-Site Scripting (XSS)",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 59,
    "CategoryName": "A8-Insecure Deserialization",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 60,
    "CategoryName": "A9-Using Components with Known Vulnerabilities",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 61,
    "CategoryName": "A10-Insufficient Logging & Monitoring",
    "CategoryType": {
      "Id": 6,
      "Name": "OWASP Top 10 2017",
      "Order": 5
    }
  },
  {
    "Id": 62,
    "CategoryName": "M1-Improper Platform Usage",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 63,
    "CategoryName": "M2-Insecure Data Storage",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 64,
    "CategoryName": "M3-Insecure Communication",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 65,
    "CategoryName": "M4-Insecure Authentication",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 66,
    "CategoryName": "M5-Insufficient Cryptography",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 67,
    "CategoryName": "M6-Insecure Authorization",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 68,
    "CategoryName": "M7-Client Code Quality",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 69,
    "CategoryName": "M8-Code Tampering",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 70,
    "CategoryName": "M9-Reverse Engineering",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 71,
    "CategoryName": "M10-Extraneous Functionality",
    "CategoryType": {
      "Id": 7,
      "Name": "OWASP Mobile Top 10 2016",
      "Order": 24
    }
  },
  {
    "Id": 371,
    "CategoryName": "APSC-DV-000640 - CAT II The application must provide audit record generation capability for the renewal of session IDs.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 372,
    "CategoryName": "APSC-DV-000650 - CAT II The application must not write sensitive data into the application logs.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 373,
    "CategoryName": "APSC-DV-000660 - CAT II The application must provide audit record generation capability for session timeouts.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 374,
    "CategoryName": "APSC-DV-000670 - CAT II The application must record a time stamp indicating when the event occurred.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 375,
    "CategoryName": "APSC-DV-000680 - CAT II The application must provide audit record generation capability for HTTP headers including User-Agent, Referer, GET, and POST.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 376,
    "CategoryName": "APSC-DV-000690 - CAT II The application must provide audit record generation capability for connecting system IP addresses.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 377,
    "CategoryName": "APSC-DV-000700 - CAT II The application must record the username or user ID of the user associated with the event.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 378,
    "CategoryName": "APSC-DV-000710 - CAT II The application must generate audit records when successful/unsuccessful attempts to grant privileges occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 379,
    "CategoryName": "APSC-DV-000720 - CAT II The application must generate audit records when successful/unsuccessful attempts to access security objects occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 380,
    "CategoryName": "APSC-DV-000730 - CAT II The application must generate audit records when successful/unsuccessful attempts to access security levels occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 381,
    "CategoryName": "APSC-DV-000740 - CAT II The application must generate audit records when successful/unsuccessful attempts to access categories of information (e.g., classification levels) occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 382,
    "CategoryName": "APSC-DV-000750 - CAT II The application must generate audit records when successful/unsuccessful attempts to modify privileges occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 383,
    "CategoryName": "APSC-DV-000760 - CAT II The application must generate audit records when successful/unsuccessful attempts to modify security objects occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 384,
    "CategoryName": "APSC-DV-000770 - CAT II The application must generate audit records when successful/unsuccessful attempts to modify security levels occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 385,
    "CategoryName": "APSC-DV-000780 - CAT II The application must generate audit records when successful/unsuccessful attempts to modify categories of information (e.g., classification levels) occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 386,
    "CategoryName": "APSC-DV-000790 - CAT II The application must generate audit records when successful/unsuccessful attempts to delete privileges occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 387,
    "CategoryName": "APSC-DV-000800 - CAT II The application must generate audit records when successful/unsuccessful attempts to delete security levels occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 388,
    "CategoryName": "APSC-DV-000810 - CAT II The application must generate audit records when successful/unsuccessful attempts to delete application database security objects occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 389,
    "CategoryName": "APSC-DV-000820 - CAT II The application must generate audit records when successful/unsuccessful attempts to delete categories of information (e.g., classification levels) occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 390,
    "CategoryName": "APSC-DV-000830 - CAT II The application must generate audit records when successful/unsuccessful logon attempts occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 391,
    "CategoryName": "APSC-DV-000840 - CAT II The application must generate audit records for privileged activities or other system-level access.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 392,
    "CategoryName": "APSC-DV-000850 - CAT II The application must generate audit records showing starting and ending time for user access to the system.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 393,
    "CategoryName": "APSC-DV-000860 - CAT II The application must generate audit records when successful/unsuccessful accesses to objects occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 394,
    "CategoryName": "APSC-DV-000870 - CAT II The application must generate audit records for all direct access to the information system.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 395,
    "CategoryName": "APSC-DV-000880 - CAT II The application must generate audit records for all account creations, modifications, disabling, and termination events.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 396,
    "CategoryName": "APSC-DV-000910 - CAT II The application must initiate session auditing upon startup.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 397,
    "CategoryName": "APSC-DV-000940 - CAT II The application must log application shutdown events.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 398,
    "CategoryName": "APSC-DV-000950 - CAT II The application must log destination IP addresses.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 399,
    "CategoryName": "APSC-DV-000960 - CAT II The application must log user actions involving access to data.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 400,
    "CategoryName": "APSC-DV-000970 - CAT II The application must log user actions involving changes to data.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 401,
    "CategoryName": "APSC-DV-000980 - CAT II The application must produce audit records containing information to establish when (date and time) the events occurred.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 402,
    "CategoryName": "APSC-DV-000990 - CAT II The application must produce audit records containing enough information to establish which component, feature or function of the application triggered the audit event.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 403,
    "CategoryName": "APSC-DV-001000 - CAT II When using centralized logging; the application must include a unique identifier in order to distinguish itself from other application logs.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 404,
    "CategoryName": "APSC-DV-001010 - CAT II The application must produce audit records that contain information to establish the outcome of the events.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 405,
    "CategoryName": "APSC-DV-001020 - CAT II The application must generate audit records containing information that establishes the identity of any individual or process associated with the event.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 406,
    "CategoryName": "APSC-DV-001030 - CAT II The application must generate audit records containing the full-text recording of privileged commands or the individual identities of group account users.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 407,
    "CategoryName": "APSC-DV-001040 - CAT II The application must implement transaction recovery logs when transaction based.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 408,
    "CategoryName": "APSC-DV-001050 - CAT II The application must provide centralized management and configuration of the content to be captured in audit records generated by all application components.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 409,
    "CategoryName": "APSC-DV-001070 - CAT II The application must off-load audit records onto a different system or media than the system being audited.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 410,
    "CategoryName": "APSC-DV-001080 - CAT II The application must be configured to write application logs to a centralized log repository.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 411,
    "CategoryName": "APSC-DV-001090 - CAT II The application must provide an immediate warning to the SA and ISSO (at a minimum) when allocated audit record storage volume reaches 75% of repository maximum audit record storage capacity.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 412,
    "CategoryName": "APSC-DV-001100 - CAT II Applications categorized as having a moderate or high impact must provide an immediate real-time alert to the SA and ISSO (at a minimum) for all audit failure events.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 413,
    "CategoryName": "APSC-DV-001110 - CAT II The application must alert the ISSO and SA (at a minimum) in the event of an audit processing failure.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 414,
    "CategoryName": "APSC-DV-001120 - CAT II The application must shut down by default upon audit failure (unless availability is an overriding concern).",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 415,
    "CategoryName": "APSC-DV-001130 - CAT II The application must provide the capability to centrally review and analyze audit records from multiple components within the system.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 416,
    "CategoryName": "APSC-DV-001140 - CAT II The application must provide the capability to filter audit records for events of interest based upon organization-defined criteria.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 417,
    "CategoryName": "APSC-DV-001150 - CAT II The application must provide an audit reduction capability that supports on-demand reporting requirements.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 418,
    "CategoryName": "APSC-DV-001160 - CAT II The application must provide an audit reduction capability that supports on-demand audit review and analysis.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 419,
    "CategoryName": "APSC-DV-001170 - CAT II The application must provide an audit reduction capability that supports after-the-fact investigations of security incidents.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 420,
    "CategoryName": "APSC-DV-001180 - CAT II The application must provide a report generation capability that supports on-demand audit review and analysis.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 421,
    "CategoryName": "APSC-DV-001190 - CAT II The application must provide a report generation capability that supports on-demand reporting requirements.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 422,
    "CategoryName": "APSC-DV-001200 - CAT II The application must provide a report generation capability that supports after-the-fact investigations of security incidents.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 423,
    "CategoryName": "APSC-DV-001210 - CAT II The application must provide an audit reduction capability that does not alter original content or time ordering of audit records.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 424,
    "CategoryName": "APSC-DV-001220 - CAT II The application must provide a report generation capability that does not alter original content or time ordering of audit records.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 425,
    "CategoryName": "APSC-DV-001250 - CAT II The applications must use internal system clocks to generate time stamps for audit records.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 426,
    "CategoryName": "APSC-DV-001260 - CAT II The application must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT).",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 427,
    "CategoryName": "APSC-DV-001270 - CAT II The application must record time stamps for audit records that meet a granularity of one second for a minimum degree of precision.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 428,
    "CategoryName": "APSC-DV-001280 - CAT II The application must protect audit information from any type of unauthorized read access.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 429,
    "CategoryName": "APSC-DV-001290 - CAT II The application must protect audit information from unauthorized modification.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 430,
    "CategoryName": "APSC-DV-001300 - CAT II The application must protect audit information from unauthorized deletion.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 431,
    "CategoryName": "APSC-DV-001310 - CAT II The application must protect audit tools from unauthorized access.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 432,
    "CategoryName": "APSC-DV-001320 - CAT II The application must protect audit tools from unauthorized modification.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 433,
    "CategoryName": "APSC-DV-001330 - CAT II The application must protect audit tools from unauthorized deletion.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 434,
    "CategoryName": "APSC-DV-001340 - CAT II The application must back up audit records at least every seven days onto a different system or system component than the system or component being audited.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 435,
    "CategoryName": "APSC-DV-001570 - CAT II The application must electronically verify Personal Identity Verification (PIV) credentials.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 436,
    "CategoryName": "APSC-DV-001350 - CAT II The application must use cryptographic mechanisms to protect the integrity of audit information.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 437,
    "CategoryName": "APSC-DV-001360 - CAT II Application audit tools must be cryptographically hashed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 438,
    "CategoryName": "APSC-DV-001370 - CAT II The integrity of the audit tools must be validated by checking the files for changes in the cryptographic hash value.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 439,
    "CategoryName": "APSC-DV-001390 - CAT II The application must prohibit user installation of software without explicit privileged status.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 440,
    "CategoryName": "APSC-DV-001410 - CAT II The application must enforce access restrictions associated with changes to application configuration.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 441,
    "CategoryName": "APSC-DV-001420 - CAT II The application must audit who makes configuration changes to the application.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 442,
    "CategoryName": "APSC-DV-001430 - CAT II The application must have the capability to prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the orga",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 443,
    "CategoryName": "APSC-DV-001440 - CAT II The applications must limit privileges to change the software resident within software libraries.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 444,
    "CategoryName": "APSC-DV-001460 - CAT II An application vulnerability assessment must be conducted.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 445,
    "CategoryName": "APSC-DV-001480 - CAT II The application must prevent program execution in accordance with organization-defined policies regarding software program usage and restrictions, and/or rules authorizing the terms and conditions of software program usage.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 446,
    "CategoryName": "APSC-DV-001490 - CAT II The application must employ a deny-all, permit-by-exception (whitelist) policy to allow the execution of authorized software programs.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 447,
    "CategoryName": "APSC-DV-001500 - CAT II The application must be configured to disable non-essential capabilities.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 448,
    "CategoryName": "APSC-DV-001510 - CAT II The application must be configured to use only functions, ports, and protocols permitted to it in the PPSM CAL.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 449,
    "CategoryName": "APSC-DV-001520 - CAT II The application must require users to reauthenticate when organization-defined circumstances or situations require reauthentication.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 450,
    "CategoryName": "APSC-DV-001530 - CAT II The application must require devices to reauthenticate when organization-defined circumstances or situations requiring reauthentication.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 451,
    "CategoryName": "APSC-DV-001540 - CAT I The application must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users).",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 452,
    "CategoryName": "APSC-DV-001550 - CAT II The application must use multifactor (Alt. Token) authentication for network access to privileged accounts.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 453,
    "CategoryName": "APSC-DV-001560 - CAT II The application must accept Personal Identity Verification (PIV) credentials.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 454,
    "CategoryName": "APSC-DV-001580 - CAT II The application must use multifactor (e.g., CAC, Alt. Token) authentication for network access to non-privileged accounts.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 455,
    "CategoryName": "APSC-DV-001590 - CAT II The application must use multifactor (Alt. Token) authentication for local access to privileged accounts.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 456,
    "CategoryName": "APSC-DV-001600 - CAT II The application must use multifactor (e.g., CAC, Alt. Token) authentication for local access to non-privileged accounts.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 457,
    "CategoryName": "APSC-DV-001610 - CAT II The application must ensure users are authenticated with an individual authenticator prior to using a group authenticator.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 458,
    "CategoryName": "APSC-DV-001620 - CAT II The application must implement replay-resistant authentication mechanisms for network access to privileged accounts.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 459,
    "CategoryName": "APSC-DV-001630 - CAT II The application must implement replay-resistant authentication mechanisms for network access to non-privileged accounts.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 460,
    "CategoryName": "APSC-DV-001640 - CAT II The application must utilize mutual authentication when endpoint device non-repudiation protections are required by DoD policy or by the data owner.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 461,
    "CategoryName": "APSC-DV-001650 - CAT II The application must authenticate all network connected endpoint devices before establishing any connection.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 462,
    "CategoryName": "APSC-DV-001660 - CAT II Service-Oriented Applications handling non-releasable data must authenticate endpoint devices via mutual SSL/TLS.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 463,
    "CategoryName": "APSC-DV-001670 - CAT II The application must disable device identifiers after 35 days of inactivity unless a cryptographic certificate is used for authentication.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 464,
    "CategoryName": "APSC-DV-001680 - CAT I The application must enforce a minimum 15-character password length.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 465,
    "CategoryName": "APSC-DV-001690 - CAT II The application must enforce password complexity by requiring that at least one upper-case character be used.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 466,
    "CategoryName": "APSC-DV-001700 - CAT II The application must enforce password complexity by requiring that at least one lower-case character be used.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 467,
    "CategoryName": "APSC-DV-001710 - CAT II The application must enforce password complexity by requiring that at least one numeric character be used.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 468,
    "CategoryName": "APSC-DV-001720 - CAT II The application must enforce password complexity by requiring that at least one special character be used.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 469,
    "CategoryName": "APSC-DV-001730 - CAT II The application must require the change of at least 8 of the total number of characters when passwords are changed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 470,
    "CategoryName": "APSC-DV-001740 - CAT I The application must only store cryptographic representations of passwords.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 471,
    "CategoryName": "APSC-DV-001850 - CAT I The application must not display passwords/PINs as clear text.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 472,
    "CategoryName": "APSC-DV-001750 - CAT I The application must transmit only cryptographically-protected passwords.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 473,
    "CategoryName": "APSC-DV-001760 - CAT II The application must enforce 24 hours/1 day as the minimum password lifetime.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 474,
    "CategoryName": "APSC-DV-001770 - CAT II The application must enforce a 60-day maximum password lifetime restriction.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 475,
    "CategoryName": "APSC-DV-001780 - CAT II The application must prohibit password reuse for a minimum of five generations.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 476,
    "CategoryName": "APSC-DV-001790 - CAT II The application must allow the use of a temporary password for system logons with an immediate change to a permanent password.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 477,
    "CategoryName": "APSC-DV-001795 - CAT II The application password must not be changeable by users other than the administrator or the user with which the password is associated.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 478,
    "CategoryName": "APSC-DV-001800 - CAT II The application must terminate existing user sessions upon account deletion.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 479,
    "CategoryName": "APSC-DV-001820 - CAT I The application, when using PKI-based authentication, must enforce authorized access to the corresponding private key.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 480,
    "CategoryName": "APSC-DV-001830 - CAT II The application must map the authenticated identity to the individual user or group account for PKI-based authentication.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 481,
    "CategoryName": "APSC-DV-001870 - CAT II The application must uniquely identify and authenticate non-organizational users (or processes acting on behalf of non-organizational users).",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 482,
    "CategoryName": "APSC-DV-001810 - CAT I The application, when utilizing PKI-based authentication, must validate certificates by constructing a certification path (which includes status information) to an accepted trust anchor.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 483,
    "CategoryName": "APSC-DV-001840 - CAT II The application, for PKI-based authentication, must implement a local cache of revocation data to support path discovery and validation in case of the inability to access revocation information via the network.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 484,
    "CategoryName": "APSC-DV-001860 - CAT II The application must use mechanisms meeting the requirements of applicable federal laws, Executive Orders, directives, policies, regulations, standards, and guidance for authentication to a cryptographic module.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 485,
    "CategoryName": "APSC-DV-001880 - CAT II The application must accept Personal Identity Verification (PIV) credentials from other federal agencies.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 486,
    "CategoryName": "APSC-DV-001890 - CAT II The application must electronically verify Personal Identity Verification (PIV) credentials from other federal agencies.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 487,
    "CategoryName": "APSC-DV-002050 - CAT II Applications making SAML assertions must use FIPS-approved random numbers in the generation of SessionIndex in the SAML element AuthnStatement.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 488,
    "CategoryName": "APSC-DV-001900 - CAT II The application must accept FICAM-approved third-party credentials.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 489,
    "CategoryName": "APSC-DV-001910 - CAT II The application must conform to FICAM-issued profiles.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 490,
    "CategoryName": "APSC-DV-001930 - CAT II Applications used for non-local maintenance sessions must audit non-local maintenance and diagnostic sessions for organization-defined auditable events.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 491,
    "CategoryName": "APSC-DV-000310 - CAT III The application must have a process, feature or function that prevents removal or disabling of emergency accounts. ",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 492,
    "CategoryName": "APSC-DV-001940 - CAT II Applications used for non-local maintenance sessions must implement cryptographic mechanisms to protect the integrity of non-local maintenance and diagnostic communications.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 493,
    "CategoryName": "APSC-DV-001950 - CAT II Applications used for non-local maintenance sessions must implement cryptographic mechanisms to protect the confidentiality of non-local maintenance and diagnostic communications.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 494,
    "CategoryName": "APSC-DV-001960 - CAT II Applications used for non-local maintenance sessions must verify remote disconnection at the termination of non-local maintenance and diagnostic sessions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 495,
    "CategoryName": "APSC-DV-001970 - CAT II The application must employ strong authenticators in the establishment of non-local maintenance and diagnostic sessions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 496,
    "CategoryName": "APSC-DV-001980 - CAT II The application must terminate all sessions and network connections when non-local maintenance is completed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 497,
    "CategoryName": "APSC-DV-001995 - CAT II The application must not be vulnerable to race conditions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 498,
    "CategoryName": "APSC-DV-002000 - CAT II The application must terminate all network connections associated with a communications session at the end of the session.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 499,
    "CategoryName": "APSC-DV-002010 - CAT II The application must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 500,
    "CategoryName": "APSC-DV-002020 - CAT II The application must utilize FIPS-validated cryptographic modules when signing application components.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 501,
    "CategoryName": "APSC-DV-002030 - CAT II The application must utilize FIPS-validated cryptographic modules when generating cryptographic hashes.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 502,
    "CategoryName": "APSC-DV-002040 - CAT II The application must utilize FIPS-validated cryptographic modules when protecting unclassified information that requires cryptographic protection.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 503,
    "CategoryName": "APSC-DV-002150 - CAT II The application user interface must be either physically or logically separated from data storage and management interfaces.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 504,
    "CategoryName": "APSC-DV-002210 - CAT II The application must set the HTTPOnly flag on session cookies.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 505,
    "CategoryName": "APSC-DV-002220 - CAT II The application must set the secure flag on session cookies.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 506,
    "CategoryName": "APSC-DV-002230 - CAT I The application must not expose session IDs.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 507,
    "CategoryName": "APSC-DV-002240 - CAT I The application must destroy the session ID value and/or cookie on logoff or browser close.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 508,
    "CategoryName": "APSC-DV-002250 - CAT II Applications must use system-generated session identifiers that protect against session fixation.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 509,
    "CategoryName": "APSC-DV-002260 - CAT II Applications must validate session identifiers.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 510,
    "CategoryName": "APSC-DV-002270 - CAT II Applications must not use URL embedded session IDs.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 511,
    "CategoryName": "APSC-DV-002280 - CAT II The application must not re-use or recycle session IDs.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 512,
    "CategoryName": "APSC-DV-002290 - CAT II The application must use the Federal Information Processing Standard (FIPS) 140-2-validated cryptographic modules and random number generator if the application implements encryption, key exchange, digital signature, and hash functionality.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 513,
    "CategoryName": "APSC-DV-002300 - CAT II The application must only allow the use of DoD-approved certificate authorities for verification of the establishment of protected sessions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 514,
    "CategoryName": "APSC-DV-002310 - CAT I The application must fail to a secure state if system initialization fails, shutdown fails, or aborts fail.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 515,
    "CategoryName": "APSC-DV-002320 - CAT II In the event of a system failure, applications must preserve any information necessary to determine cause of failure and any information necessary to return to operations with least disruption to mission processes.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 516,
    "CategoryName": "APSC-DV-002330 - CAT II The application must protect the confidentiality and integrity of stored information when required by DoD policy or the information owner.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 517,
    "CategoryName": "APSC-DV-002340 - CAT II The application must implement approved cryptographic mechanisms to prevent unauthorized modification of organization-defined information at rest on organization-defined information system components.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 518,
    "CategoryName": "APSC-DV-002350 - CAT II The application must use appropriate cryptography in order to protect stored DoD information when required by the information owner or DoD policy.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 519,
    "CategoryName": "APSC-DV-002360 - CAT II The application must isolate security functions from non-security functions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 520,
    "CategoryName": "APSC-DV-002370 - CAT II The application must maintain a separate execution domain for each executing process.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 521,
    "CategoryName": "APSC-DV-002380 - CAT II Applications must prevent unauthorized and unintended information transfer via shared system resources.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 522,
    "CategoryName": "APSC-DV-002390 - CAT II XML-based applications must mitigate DoS attacks by using XML filters, parser options, or gateways.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 523,
    "CategoryName": "APSC-DV-002400 - CAT II The application must restrict the ability to launch Denial of Service (DoS) attacks against itself or other information systems.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 524,
    "CategoryName": "APSC-DV-002410 - CAT II The web service design must include redundancy mechanisms when used with high-availability systems.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 525,
    "CategoryName": "APSC-DV-002420 - CAT II An XML firewall function must be deployed to protect web services when exposed to untrusted networks.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 526,
    "CategoryName": "APSC-DV-002610 - CAT II The application must remove organization-defined software components after updated versions have been installed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 527,
    "CategoryName": "APSC-DV-002440 - CAT I The application must protect the confidentiality and integrity of transmitted information.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 528,
    "CategoryName": "APSC-DV-002450 - CAT II The application must implement cryptographic mechanisms to prevent unauthorized disclosure of information and/or detect changes to information during transmission unless otherwise protected by alternative physical safeguards, such as, at a minimum, a Prot",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 529,
    "CategoryName": "APSC-DV-002460 - CAT II The application must maintain the confidentiality and integrity of information during preparation for transmission.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 530,
    "CategoryName": "APSC-DV-002470 - CAT II The application must maintain the confidentiality and integrity of information during reception.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 531,
    "CategoryName": "APSC-DV-002480 - CAT II The application must not disclose unnecessary information to users.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 532,
    "CategoryName": "APSC-DV-002485 - CAT I The application must not store sensitive information in hidden fields.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 533,
    "CategoryName": "APSC-DV-002490 - CAT I The application must protect from Cross-Site Scripting (XSS) vulnerabilities.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 534,
    "CategoryName": "APSC-DV-002500 - CAT II The application must protect from Cross-Site Request Forgery (CSRF) vulnerabilities.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 535,
    "CategoryName": "APSC-DV-002510 - CAT I The application must protect from command injection.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 536,
    "CategoryName": "APSC-DV-002520 - CAT II The application must protect from canonical representation vulnerabilities.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 537,
    "CategoryName": "APSC-DV-002530 - CAT II The application must validate all input.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 538,
    "CategoryName": "APSC-DV-002540 - CAT I The application must not be vulnerable to SQL Injection.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 539,
    "CategoryName": "APSC-DV-002550 - CAT I The application must not be vulnerable to XML-oriented attacks.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 540,
    "CategoryName": "APSC-DV-002560 - CAT I The application must not be subject to input handling vulnerabilities.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 541,
    "CategoryName": "APSC-DV-002570 - CAT II The application must generate error messages that provide information necessary for corrective actions without revealing information that could be exploited by adversaries.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 542,
    "CategoryName": "APSC-DV-002580 - CAT II The application must reveal error messages only to the ISSO, ISSM, or SA.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 543,
    "CategoryName": "APSC-DV-002590 - CAT I The application must not be vulnerable to overflow attacks.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 544,
    "CategoryName": "APSC-DV-002630 - CAT II Security-relevant software updates and patches must be kept up to date.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 545,
    "CategoryName": "APSC-DV-002760 - CAT II The application performing organization-defined security functions must verify correct operation of security functions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 546,
    "CategoryName": "APSC-DV-002900 - CAT II The ISSO must ensure application audit trails are retained for at least 1 year for applications without SAMI data, and 5 years for applications including SAMI data.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 547,
    "CategoryName": "APSC-DV-002770 - CAT II The application must perform verification of the correct operation of security functions: upon system startup and/or restart; upon command by a user with privileged access; and/or every 30 days.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 548,
    "CategoryName": "APSC-DV-002780 - CAT III The application must notify the ISSO and ISSM of failed security verification tests.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 549,
    "CategoryName": "APSC-DV-002870 - CAT II Unsigned Category 1A mobile code must not be used in the application in accordance with DoD policy.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 550,
    "CategoryName": "APSC-DV-002880 - CAT II The ISSO must ensure an account management process is implemented, verifying only authorized users can gain access to the application, and individual accounts designated as inactive, suspended, or terminated are promptly removed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 551,
    "CategoryName": "APSC-DV-002890 - CAT I Application web servers must be on a separate network segment from the application and database servers if it is a tiered application operating in the DoD DMZ.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 552,
    "CategoryName": "APSC-DV-002910 - CAT II The ISSO must review audit trails periodically based on system documentation recommendations or immediately upon system security events.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 553,
    "CategoryName": "APSC-DV-002920 - CAT II The ISSO must report all suspected violations of IA policies in accordance with DoD information system IA procedures.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 554,
    "CategoryName": "APSC-DV-002930 - CAT II The ISSO must ensure active vulnerability testing is performed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 555,
    "CategoryName": "APSC-DV-002980 - CAT II New IP addresses, data services, and associated ports used by the application must be submitted to the appropriate approving authority for the organization, which in turn will be submitted through the DoD Ports, Protocols, and Services Management (DoD PPS",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 556,
    "CategoryName": "APSC-DV-002950 - CAT II Execution flow diagrams and design documents must be created to show how deadlock and recursion issues in web services are being mitigated.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 557,
    "CategoryName": "APSC-DV-002960 - CAT II The designer must ensure the application does not store configuration and control files in the same directory as user data.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 558,
    "CategoryName": "APSC-DV-002970 - CAT II The ISSO must ensure if a DoD STIG or NSA guide is not available, a third-party product will be configured by following available guidance.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 559,
    "CategoryName": "APSC-DV-002990 - CAT II The application must be registered with the DoD Ports and Protocols Database.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 560,
    "CategoryName": "APSC-DV-002990 - CAT II The application must be registered with the DoD Ports and Protocols Database.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 561,
    "CategoryName": "APSC-DV-002995 - CAT II The Configuration Management (CM) repository must be properly patched and STIG compliant.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 562,
    "CategoryName": "APSC-DV-003000 - CAT II Access privileges to the Configuration Management (CM) repository must be reviewed every three months.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 563,
    "CategoryName": "APSC-DV-003010 - CAT II A Software Configuration Management (SCM) plan describing the configuration control and change management process of application objects developed by the organization and the roles and responsibilities of the organization must be created and maintained.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 564,
    "CategoryName": "APSC-DV-003020 - CAT II A Configuration Control Board (CCB) that meets at least every release cycle, for managing the Configuration Management (CM) process must be established.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 565,
    "CategoryName": "APSC-DV-003030 - CAT II The application services and interfaces must be compatible with and ready for IPv6 networks.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 566,
    "CategoryName": "APSC-DV-003040 - CAT II The application must not be hosted on a general purpose machine if the application is designated as critical or high availability by the ISSO.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 567,
    "CategoryName": "APSC-DV-003050 - CAT II A disaster recovery/continuity plan must exist in accordance with DoD policy based on the applications availability requirements.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 568,
    "CategoryName": "APSC-DV-003060 - CAT II Recovery procedures and technical system features must exist so recovery is performed in a secure and verifiable manner. The ISSO will document circumstances inhibiting a trusted recovery.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 569,
    "CategoryName": "APSC-DV-003070 - CAT II Data backup must be performed at required intervals in accordance with DoD policy.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 570,
    "CategoryName": "APSC-DV-003080 - CAT II Back-up copies of the application software or source code must be stored in a fire-rated container or stored separately (offsite).",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 571,
    "CategoryName": "APSC-DV-003090 - CAT II Procedures must be in place to assure the appropriate physical and technical protection of the backup and restoration of the application.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 572,
    "CategoryName": "APSC-DV-003100 - CAT II The application must use encryption to implement key exchange and authenticate endpoints prior to establishing a communication channel for key exchange.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 573,
    "CategoryName": "APSC-DV-003110 - CAT I The application must not contain embedded authentication data.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 574,
    "CategoryName": "APSC-DV-003120 - CAT I The application must have the capability to mark sensitive/classified output when required.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 575,
    "CategoryName": "APSC-DV-003130 - CAT III Prior to each release of the application, updates to system, or applying patches; tests plans and procedures must be created and executed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 576,
    "CategoryName": "APSC-DV-003150 - CAT II At least one tester must be designated to test for security flaws in addition to functional testing.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 577,
    "CategoryName": "APSC-DV-003140 - CAT II Application files must be cryptographically hashed prior to deploying to DoD operational networks.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 578,
    "CategoryName": "APSC-DV-003160 - CAT III Test procedures must be created and at least annually executed to ensure system initialization, shutdown, and aborts are configured to verify the system remains in a secure state.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 579,
    "CategoryName": "APSC-DV-003170 - CAT II An application code review must be performed on the application.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 580,
    "CategoryName": "APSC-DV-003180 - CAT III Code coverage statistics must be maintained for each release of the application.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 581,
    "CategoryName": "APSC-DV-003190 - CAT II Flaws found during a code review must be tracked in a defect tracking system.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 582,
    "CategoryName": "APSC-DV-003200 - CAT II The changes to the application must be assessed for IA and accreditation impact prior to implementation.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 583,
    "CategoryName": "APSC-DV-003210 - CAT II Security flaws must be fixed or addressed in the project plan.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 584,
    "CategoryName": "APSC-DV-003215 - CAT III The application development team must follow a set of coding standards.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 585,
    "CategoryName": "APSC-DV-003220 - CAT III The designer must create and update the Design Document for each release of the application.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 586,
    "CategoryName": "APSC-DV-003230 - CAT II Threat models must be documented and reviewed for each application release and updated as required by design and functionality changes or when new threats are discovered.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 587,
    "CategoryName": "APSC-DV-003235 - CAT II The application must not be subject to error handling vulnerabilities.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 588,
    "CategoryName": "APSC-DV-003250 - CAT I The application must be decommissioned when maintenance or support is no longer available.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 589,
    "CategoryName": "APSC-DV-003236 - CAT II The application development team must provide an application incident response plan.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 590,
    "CategoryName": "APSC-DV-003240 - CAT I All products must be supported by the vendor or the development team.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 591,
    "CategoryName": "APSC-DV-003260 - CAT III Procedures must be in place to notify users when an application is decommissioned.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 592,
    "CategoryName": "APSC-DV-003270 - CAT II Unnecessary built-in application accounts must be disabled.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 593,
    "CategoryName": "APSC-DV-003280 - CAT I Default passwords must be changed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 594,
    "CategoryName": "APSC-DV-003330 - CAT II The system must alert an administrator when low resource conditions are encountered.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 595,
    "CategoryName": "APSC-DV-003285 - CAT II An Application Configuration Guide must be created and included with the application.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 596,
    "CategoryName": "APSC-DV-003290 - CAT II If the application contains classified data, a Security Classification Guide must exist containing data elements and their classification.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 597,
    "CategoryName": "APSC-DV-003300 - CAT II The designer must ensure uncategorized or emerging mobile code is not used in applications.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 598,
    "CategoryName": "APSC-DV-003310 - CAT II Production database exports must have database administration credentials and sensitive data removed before releasing the export.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 599,
    "CategoryName": "APSC-DV-003320 - CAT II Protections against DoS attacks must be implemented.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 600,
    "CategoryName": "APSC-DV-003340 - CAT III At least one application administrator must be registered to receive update notifications, or security alerts, when automated alerts are available.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 601,
    "CategoryName": "APSC-DV-003360 - CAT III The application must generate audit records when concurrent logons from different workstations occur.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 602,
    "CategoryName": "APSC-DV-003345 - CAT III The application must provide notifications or alerts when product update and security related patches are available.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 603,
    "CategoryName": "APSC-DV-003350 - CAT II Connections between the DoD enclave and the Internet or other public or commercial wide area networks must require a DMZ.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 604,
    "CategoryName": "APSC-DV-003400 - CAT II The Program Manager must verify all levels of program management, designers, developers, and testers receive annual security training pertaining to their job function.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 605,
    "CategoryName": "APSC-DV-000010 - CAT II The application must provide a capability to limit the number of logon sessions per user.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 606,
    "CategoryName": "APSC-DV-000060 - CAT II The application must clear temporary storage and cookies when the session is terminated.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 607,
    "CategoryName": "APSC-DV-000070 - CAT II The application must automatically terminate the non-privileged user session and log off non-privileged users after a 15 minute idle time period has elapsed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 608,
    "CategoryName": "APSC-DV-000080 - CAT II The application must automatically terminate the admin user session and log off admin users after a 10 minute idle time period is exceeded.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 609,
    "CategoryName": "APSC-DV-000090 - CAT II Applications requiring user access authentication must provide a logoff capability for user initiated communication session.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 610,
    "CategoryName": "APSC-DV-000100 - CAT III The application must display an explicit logoff message to users indicating the reliable termination of authenticated communications sessions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 611,
    "CategoryName": "APSC-DV-000110 - CAT II The application must associate organization-defined types of security attributes having organization-defined security attribute values with information in storage.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 612,
    "CategoryName": "APSC-DV-000120 - CAT II The application must associate organization-defined types of security attributes having organization-defined security attribute values with information in process.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 613,
    "CategoryName": "APSC-DV-000130 - CAT II The application must associate organization-defined types of security attributes having organization-defined security attribute values with information in transmission.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 614,
    "CategoryName": "APSC-DV-000160 - CAT II The application must implement DoD-approved encryption to protect the confidentiality of remote access sessions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 615,
    "CategoryName": "APSC-DV-000170 - CAT II The application must implement cryptographic mechanisms to protect the integrity of remote access sessions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 616,
    "CategoryName": "APSC-DV-000190 - CAT I Messages protected with WS_Security must use time stamps with creation and expiration times.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 617,
    "CategoryName": "APSC-DV-000180 - CAT II Applications with SOAP messages requiring integrity must include the following message elements:-Message ID-Service Request-Timestamp-SAML Assertion (optionally included in messages) and all elements of the message must be digitally signed.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 618,
    "CategoryName": "APSC-DV-000200 - CAT I Validity periods must be verified on all application messages using WS-Security or SAML assertions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 619,
    "CategoryName": "APSC-DV-000210 - CAT II The application must ensure each unique asserting party provides unique assertion ID references for each SAML assertion.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 620,
    "CategoryName": "APSC-DV-000220 - CAT II The application must ensure encrypted assertions, or equivalent confidentiality protections are used when assertion data is passed through an intermediary, and confidentiality of the assertion data is required when passing through the intermediary.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 621,
    "CategoryName": "APSC-DV-000230 - CAT I The application must use the NotOnOrAfter condition when using the SubjectConfirmation element in a SAML assertion.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 622,
    "CategoryName": "APSC-DV-000240 - CAT I The application must use both the NotBefore and NotOnOrAfter elements or OneTimeUse element when using the Conditions element in a SAML assertion.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 623,
    "CategoryName": "APSC-DV-000250 - CAT II The application must ensure if a OneTimeUse element is used in an assertion, there is only one of the same used in the Conditions element portion of an assertion.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 624,
    "CategoryName": "APSC-DV-000260 - CAT II The application must ensure messages are encrypted when the SessionIndex is tied to privacy data.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 625,
    "CategoryName": "APSC-DV-000290 - CAT II Shared/group account credentials must be terminated when members leave the group.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 626,
    "CategoryName": "APSC-DV-000280 - CAT II The application must provide automated mechanisms for supporting account management functions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 627,
    "CategoryName": "APSC-DV-000300 - CAT II The application must automatically remove or disable temporary user accounts 72 hours after account creation.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 628,
    "CategoryName": "APSC-DV-000320 - CAT III The application must automatically disable accounts after a 35 day period of account inactivity.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 629,
    "CategoryName": "APSC-DV-000330 - CAT II Unnecessary application accounts must be disabled, or deleted.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 630,
    "CategoryName": "APSC-DV-000420 - CAT II The application must automatically audit account enabling actions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 631,
    "CategoryName": "APSC-DV-000340 - CAT II The application must automatically audit account creation.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 632,
    "CategoryName": "APSC-DV-000350 - CAT II The application must automatically audit account modification.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 633,
    "CategoryName": "APSC-DV-000360 - CAT II The application must automatically audit account disabling actions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 634,
    "CategoryName": "APSC-DV-000370 - CAT II The application must automatically audit account removal actions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 635,
    "CategoryName": "APSC-DV-000380 - CAT III The application must notify System Administrators and Information System Security Officers when accounts are created.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 636,
    "CategoryName": "APSC-DV-000390 - CAT III The application must notify System Administrators and Information System Security Officers when accounts are modified.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 637,
    "CategoryName": "APSC-DV-000400 - CAT III The application must notify System Administrators and Information System Security Officers of account disabling actions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 638,
    "CategoryName": "APSC-DV-000410 - CAT III The application must notify System Administrators and Information System Security Officers of account removal actions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 639,
    "CategoryName": "APSC-DV-000430 - CAT III The application must notify System Administrators and Information System Security Officers of account enabling actions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 640,
    "CategoryName": "APSC-DV-000440 - CAT II Application data protection requirements must be identified and documented.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 641,
    "CategoryName": "APSC-DV-000520 - CAT II The application must audit the execution of privileged functions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 642,
    "CategoryName": "APSC-DV-000450 - CAT II The application must utilize organization-defined data mining detection techniques for organization-defined data storage objects to adequately detect data mining attempts.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 643,
    "CategoryName": "APSC-DV-000460 - CAT I The application must enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 644,
    "CategoryName": "APSC-DV-000470 - CAT II The application must enforce organization-defined discretionary access control policies over defined subjects and objects.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 645,
    "CategoryName": "APSC-DV-000480 - CAT II The application must enforce approved authorizations for controlling the flow of information within the system based on organization-defined information flow control policies.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 646,
    "CategoryName": "APSC-DV-000490 - CAT II The application must enforce approved authorizations for controlling the flow of information between interconnected systems based on organization-defined information flow control policies.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 647,
    "CategoryName": "APSC-DV-000500 - CAT II The application must prevent non-privileged users from executing privileged functions to include disabling, circumventing, or altering implemented security safeguards/countermeasures.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 648,
    "CategoryName": "APSC-DV-000510 - CAT I The application must execute without excessive account permissions.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 649,
    "CategoryName": "APSC-DV-000530 - CAT I The application must enforce the limit of three consecutive invalid logon attempts by a user during a 15 minute time period.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 650,
    "CategoryName": "APSC-DV-000560 - CAT III The application must retain the Standard Mandatory DoD Notice and Consent Banner on the screen until users acknowledge the usage conditions and take explicit actions to log on for further access.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 651,
    "CategoryName": "APSC-DV-000540 - CAT II The application administrator must follow an approved process to unlock locked user accounts.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 652,
    "CategoryName": "APSC-DV-000550 - CAT III The application must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the application.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 653,
    "CategoryName": "APSC-DV-000570 - CAT III The publicly accessible application must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the application.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 654,
    "CategoryName": "APSC-DV-000580 - CAT III The application must display the time and date of the users last successful logon.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 655,
    "CategoryName": "APSC-DV-000630 - CAT II The application must provide audit record generation capability for the destruction of session IDs.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 656,
    "CategoryName": "APSC-DV-000590 - CAT II The application must protect against an individual (or process acting on behalf of an individual) falsely denying having performed organization-defined actions to be covered by non-repudiation.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 657,
    "CategoryName": "APSC-DV-000600 - CAT II For applications providing audit record aggregation, the application must compile audit records from organization-defined information system components into a system-wide audit trail that is time-correlated with an organization-defined level of tolerance ",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 658,
    "CategoryName": "APSC-DV-000610 - CAT II The application must provide the capability for organization-identified individuals or roles to change the auditing to be performed on all application components, based on all selectable event criteria within organization-defined time thresholds.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 659,
    "CategoryName": "APSC-DV-000620 - CAT II The application must provide audit record generation capability for the creation of session IDs.",
    "CategoryType": {
      "Id": 8,
      "Name": "ASD STIG 4.10",
      "Order": 40
    }
  },
  {
    "Id": 660,
    "CategoryName": "API1-Broken Object Level Authorization",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 661,
    "CategoryName": "API2-Broken Authentication",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 662,
    "CategoryName": "API3-Excessive Data Exposure",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 663,
    "CategoryName": "API4-Lack of Resources and Rate Limiting",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 664,
    "CategoryName": "API5-Broken Function Level Authorization",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 665,
    "CategoryName": "API6-Mass Assignment",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 666,
    "CategoryName": "API7-Security Misconfiguration",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 667,
    "CategoryName": "API8-Injection",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 668,
    "CategoryName": "API9-Improper Assets Management",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 669,
    "CategoryName": "API10-Insufficient Logging and Monitoring",
    "CategoryType": {
      "Id": 9,
      "Name": "OWASP Top 10 API",
      "Order": 41
    }
  },
  {
    "Id": 670,
    "CategoryName": "A1-Injection",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 671,
    "CategoryName": "A2-Cross-Site Scripting (XSS)",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 672,
    "CategoryName": "A3-Broken Authentication and Session Management",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 673,
    "CategoryName": "A4-Insecure Direct Object References",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 674,
    "CategoryName": "A5-Cross-Site Request Forgery (CSRF)",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 675,
    "CategoryName": "A6-Security Misconfiguration",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 676,
    "CategoryName": "A7-Insecure Cryptographic Storage",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 677,
    "CategoryName": "A8-Failure to Restrict URL Access",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 678,
    "CategoryName": "A9-Insufficient Transport Layer Protection",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 679,
    "CategoryName": "A10-Unvalidated Redirects and Forwards",
    "CategoryType": {
      "Id": 10,
      "Name": "OWASP Top 10 2010",
      "Order": 42
    }
  },
  {
    "Id": 680,
    "CategoryName": "CWE top 25",
    "CategoryType": {
      "Id": 11,
      "Name": "CWE top 25",
      "Order": 44
    }
  },
  {
    "Id": 681,
    "CategoryName": "MOIS(KISA) API misuse",
    "CategoryType": {
      "Id": 12,
      "Name": "MOIS(KISA) Secure Coding 2021",
      "Order": 43
    }
  },
  {
    "Id": 682,
    "CategoryName": "MOIS(KISA) Code error",
    "CategoryType": {
      "Id": 12,
      "Name": "MOIS(KISA) Secure Coding 2021",
      "Order": 43
    }
  },
  {
    "Id": 683,
    "CategoryName": "MOIS(KISA) Encapsulation",
    "CategoryType": {
      "Id": 12,
      "Name": "MOIS(KISA) Secure Coding 2021",
      "Order": 43
    }
  },
  {
    "Id": 684,
    "CategoryName": "MOIS(KISA) Error processing",
    "CategoryType": {
      "Id": 12,
      "Name": "MOIS(KISA) Secure Coding 2021",
      "Order": 43
    }
  },
  {
    "Id": 685,
    "CategoryName": "MOIS(KISA) Security Functions",
    "CategoryType": {
      "Id": 12,
      "Name": "MOIS(KISA) Secure Coding 2021",
      "Order": 43
    }
  },
  {
    "Id": 686,
    "CategoryName": "MOIS(KISA) Time and status",
    "CategoryType": {
      "Id": 12,
      "Name": "MOIS(KISA) Secure Coding 2021",
      "Order": 43
    }
  },
  {
    "Id": 687,
    "CategoryName": "MOIS(KISA) Verification and representation of input data",
    "CategoryType": {
      "Id": 12,
      "Name": "MOIS(KISA) Secure Coding 2021",
      "Order": 43
    }
  },
  {
    "Id": 688,
    "CategoryName": "V01 Architecture, Design and Threat Modeling",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 689,
    "CategoryName": "V02 Authentication",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 690,
    "CategoryName": "V03 Session Management",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 691,
    "CategoryName": "V04 Access Control",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 692,
    "CategoryName": "V05 Validation, Sanitization and Encoding",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 693,
    "CategoryName": "V06 Stored Cryptography",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 694,
    "CategoryName": "V07 Error Handling and Logging",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 695,
    "CategoryName": "V08 Data Protection",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 696,
    "CategoryName": "V09 Communication",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 697,
    "CategoryName": "V10 Malicious Code",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 698,
    "CategoryName": "V11 Business Logic",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 699,
    "CategoryName": "V12 Files and Resources",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 700,
    "CategoryName": "V13 API and Web Service",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 701,
    "CategoryName": "V14 Configuration",
    "CategoryType": {
      "Id": 13,
      "Name": "OWASP ASVS",
      "Order": 45
    }
  },
  {
    "Id": 702,
    "CategoryName": "A1-Broken Access Control",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 703,
    "CategoryName": "A2-Cryptographic Failures",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 704,
    "CategoryName": "A3-Injection",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 705,
    "CategoryName": "A4-Insecure Design",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 706,
    "CategoryName": "A5-Security Misconfiguration",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 707,
    "CategoryName": "A6-Vulnerable and Outdated Components",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 708,
    "CategoryName": "A7-Identification and Authentication Failures",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 709,
    "CategoryName": "A8-Software and Data Integrity Failures",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 710,
    "CategoryName": "A9-Security Logging and Monitoring Failures",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 711,
    "CategoryName": "A10-Server-Side Request Forgery",
    "CategoryType": {
      "Id": 14,
      "Name": "OWASP Top 10 2021",
      "Order": 5
    }
  },
  {
    "Id": 712,
    "CategoryName": "SANS top 25",
    "CategoryType": {
      "Id": 15,
      "Name": "SANS top 25",
      "Order": 43
    }
  }
]