
# Post Scan Email with Distribution List

This script can be used as a post-scan action that allows the email distribution list to be defined as part of the post-scan action configuration.  The email distribution list is defined as part of the "arguments" configuration in the post-scan action details.

## Quick Start

1. Copy `email.bat` and `email.ps1` to the `Executables` folder located in your CxSAST installation folder.
2. Modify the variables in `email.bat` and `email.ps1` as appropriate for your system.
3. Configure a post-scan action to call `email.bat`.
4. As arguments to the post-scan action use something similar to:

```
'person1@gmail.com,person2@checkmarx.com',';[PDF_output];'
```

Substitute your comma-separated list of emails as appropriate.  

Use this exact format for the arguments or things won't work very well.  

If you need to use non-ASCII characters in the email addresses (e.g. `+` or multi-byte chars), you will need to use URL encoded characters as documented below.  This single-quote delimited format should work for most implementations without needing to use URL encoded characters.


## URL Encoded Character Support

There are cases where an email address may have non-ASCII characters.  A good example would be `person+abc@gmail.com` where the `+` extension can be used to track the originator of the email.  Some addressee names may also have non-ASCII characters.

In this case, you can URL Encode some of the characters so that the script will handle them properly.  Example:

`%22person1%2Babc@gmail.com,person2@checkmarx.com%22,%22;[PDF_output];%22`

This would translate to the script interpreting this as:
`"person1+abc@gmail.com,person2@checkmarx.com","(PDF path)"`

**Note:** The `;`,`[`, and `]` characters should not be URL encoded.


## Report Attachments

Any supported report type (PDF, XML, CSV) can be sent as an attachment.  Use the appropriate argument variable. (e.g. `[PDF_output]` attaches a PDF, etc.)


## Troubleshooting


### Output Logging

You can temporarily append `>> %cx_install_path%\Executables\email.log 2>&1` to the line in `email.bat` where PowerShell is invoked.  This will send the output to a file named `email.log` found in the `Executables` folder.

If there are multiple project using this script in their post-scan actions, the log file will be mangled if mulitple post-scan actions are executed concurrently.  It is suggested the logging only be used with a post-scan action assigned to one project.

### Email Issues

To verify your email configuration is correct, you can invoke `Send-MailMessage` directly in PowerShell on the CxSAST manager to ensure that your system can appropriately communicate with your mail server.  Often the following issues can make sending email from the CxSAST server difficult:

* Wrong SMTP port selected for using `STARTTLS` email transmission.
* SMTP ports access is blocked for the manager server by subnet firewalls, proxy servers, etc.
* SMTP server credentials are wrong. (e.g. the username for some services may differ from the email address for the account)
* SMTP servers don't allow relaying messages for the account. (e.g. Gmail requires you enable [Less Secure Apps](https://support.google.com/accounts/answer/6010255?hl=en) to allow relaying of messages via SMTP)
* SMTP servers don't allow the authenticated account and the `From` email address to differ.

