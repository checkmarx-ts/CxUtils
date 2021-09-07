param( 
    [Parameter(Mandatory = $true)]
    [string]$cmd
    ) 

# Set the location of where results would normally be stored.  This removes
# the ability for a path injection when configuring the post scan action.    
$attachLoc = "C:\Program Files\Checkmarx\Checkmarx Jobs Manager\Results"

# Configure the parameters below to customize the email delivery options.
$SMTPServer = "<smtp server address goes here>"
$SMTPServerPort =  587
$SMTPUser = "<username for the smtp server goes here>"
$SMTPPassword = "<login password goes here>"
$EmailFrom = "<from address goes here>"
$Subject = "Checkmarx Scan Report"
$Body = "Compose body here"




Write-Host "cmd = $cmd`n"
Write-Host "attachLoc = $attachLoc`n"

Add-Type -AssemblyName System.Web

$cmdDecoded = [System.Web.HttpUtility]::UrlDecode($cmd)

# First char in the command is the quote separating the fields.
$quote_char = $cmdDecoded[0]

function Get-ArrayOfArgs() {
    param (
        [string]$csv
    )
    $retArray = @()

    $index = $csv.IndexOf($quote_char)
    while ($index -ne -1) {
        $nextIndex = $csv.IndexOf($quote_char, $index + 1)

        $extracted = $csv.Substring($index + 1, ($nextIndex - $index) - 1 )
      
        $retArray += $extracted

        $index = $csv.IndexOf($quote_char, $nextIndex + 1)
    }

    return $retArray
}

function Get-SanitizedAttachmentPath()
{
    param (
        [string]$path
    )

    $fname = [System.IO.Path]::GetFileName($path)

    Write-Host $fname
    while($true)
    {
        $pos = $fname.IndexOf("..")

        if ($pos -ne -1) {
          Write-Host "Found '..' at: $pos`n"
          $fname = $fname.Remove($pos, 2)
          Write-Host "New name: $fname`n"
        }
        else {
            Write-Host "Done removing relative path components`n"
            break
        }
    }

    return [System.IO.Path]::Combine($attachLoc, $fname)
}

$array = Get-ArrayOfArgs $cmdDecoded
$unsanitizedAttachPath = $array[1].Trim(' ')
$recipients = $array[0].Split(',')

[securestring]$s_password = ConvertTo-SecureString -String $SMTPPassword -AsPlainText -Force
[pscredential]$smtpCred = New-Object System.Management.Automation.PSCredential($SMTPUser, $s_password)

$attachPath = Get-SanitizedAttachmentPath @([Management.Automation.WildcardPattern]::Escape($unsanitizedAttachPath))
Write-Host "Orig: $unsanitizedAttachPath New: $attachPath`n"
Write-Host "Recipients: $recipients"

Send-MailMessage -Attachments "$attachPath" -Body $Body -From $EmailFrom -Credential $smtpCred -Port $SMTPServerPort -SmtpServer $SMTPServer -Subject $Subject -To $recipients -UseSsl
