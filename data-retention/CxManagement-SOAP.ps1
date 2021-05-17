<#
.SYNOPSIS
Controls (Starts & Stops) data retention.

.DESCRIPTION
Given the URL of a specific checkmarx web interface, starts a data retention by deleting either all scans within a specified date range or all but the last X scans for each project.
This command can also be used for stopping a currently running data retention process.

.PARAMETER serviceUrl
The URL of a Checkmarx web service.

.PARAMETER username
The Checkmarx user name of a user with permissions to run a data retention process (Server Administrator)

.PARAMETER pass
The password of the specified Checkmarx user

.PARAMETER StopRetention
Enable this switch to stop the Data Retention process.

.PARAMETER StartRetention
Enable this switch to start the Data Retention proccess.

.PARAMETER ByNumOfScans
A switch defining that all of the scans in the system, except for the most recent X scans in each project, will be deleted. The number of recent scans to be kept (X) is specified by the numOfScansToKeep parameter.

.PARAMETER numOfScansToKeep
When the ByNumOfScans switch is enables, defines how many recent scans are kept in each project when data retention is carried out.

.PARAMETER ByDateRange
A switch that defines that all of the scans within a specified date range will be deleted.

.PARAMETER startDate
An optional inclusive lower limit of the date range of scans to delete. Only considers dates, ignores hours.

.PARAMETER endDate
A mandatory inclusive upper limit of the date range of scans to delete. Only considers dates, ignores hours.

.PARAMETER ByRollingDate
A switch that defines that all of the scans within a specified number of days form the current date will be deleted.

.PARAMETER rollingDate
A mandatory integer that is used to define the end date of the data retention by subtracting it from the current date.

.PARAMETER retentionDurationLimit
An optional parameter that allows to limit the duration of the data retention process. Specified only in round hours (integers), and applies to all scans performed after this parameter was set. 
The duration limit does not override the data retention schedule. Scans are deleted in bulks of X (configured in the database with a default value of 3), and the data retention process stops only upon the completion of the last bulk that started before the duration limit has been reached. For example: if the duration limit was set to 4 hours, and the last bulk started 3:50 hours after this parameter was set, the retention process will stop only when this bulk completes, even if the completion takes place well past 4:00 hours.


.EXAMPLE
Delete all but the last 5 scans of each project.
CxManagement.ps1 -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByNumOfScans -numOfScansToKeep 5

.EXAMPLE
Delete all but the last 5 scans of each project, limit the duration of the data retention process to 2 hours.
CxManagement.ps1 -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByNumOfScans -numOfScansToKeep 5 -retentionDurationLimit 2

.EXAMPLE
Delete all of the scans performed before October 10 2015.
CxManagement.ps1 -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByDateRange -endDate "2015-10-10"

.EXAMPLE
Delete all of the scans between October 5 and October 10 2015.
CxManagement.ps1 -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByDateRange -startDate "2015-10-05" -endDate "2015-10-10"

.EXAMPLE
Delete all of the scans between october 5 and October 10 2015, and limit the duration of the data retention process to 2 hours.
CxManagement.ps1 -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByDateRange -startDate "2015-10-05" -endDate "2015-10-10" -retentionDurationLimit 2

.EXAMPLE
Delete all of the scans that have occurred 180 days after the current date.
CxManagement.ps1 -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByRollingDate -rollingDate 180

.EXAMPLE
Stops the data retention process.
CxManagement.ps1 -StopRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd"

.NOTES
- It is only possible to define either StartRetention -OR- StopRetention.
- It is only possible to define one type of retention at a time.
- The duration limit is not an immediate limit, scans are deleted in bulks of X (configured in the database with a default value of 3) and the data retention will only stop at the end of a bulk.
#>
[CmdletBinding()]
Param(
                
                [Parameter(Mandatory = $True, ParameterSetName = "stop")]
                [switch]
                $StopRetention,
                
                [Parameter(Mandatory = $True, ParameterSetName = "DatesRange")]
                [Parameter(Mandatory = $True, ParameterSetName = "RollingDate")]
                [Parameter(Mandatory = $True, ParameterSetName = "NumOfScans")]
                [switch]
                $StartRetention,
                
                [Parameter(Mandatory = $True)]
                [String]
                $serviceUrl,
                
                [Parameter(Mandatory = $True)]
                [String]
                $username,
                
                [Parameter(Mandatory = $True)]
                [String]
                $pass,
                
                [Parameter(Mandatory = $True, ParameterSetName = "NumOfScans")]
                [switch]
                $ByNumOfScans,
                
                [Parameter(Mandatory = $True, ParameterSetName = "NumOfScans")]
                [Int]
                $numOfScansToKeep,
                
                [Parameter(Mandatory = $True, ParameterSetName = "DatesRange")]
                [switch]
                $ByDateRange,
                
                [Parameter(Mandatory = $False, ParameterSetName = "DatesRange")]
                [Datetime]
                $startDate,
                
                [Parameter(Mandatory = $True, ParameterSetName = "DatesRange")]
                [Datetime]
                $endDate,

                [Parameter(Mandatory = $True, ParameterSetName = "RollingDate")]
                [switch]
                $ByRollingDate,

                [Parameter(Mandatory = $True, ParameterSetName = "RollingDate")]
                [int]
                $rollingDateRange,
                
                [Parameter(Mandatory = $False, ParameterSetName = "DatesRange")]
                [Parameter(Mandatory = $False, ParameterSetName = "NumOfScans")]
                [int]
                $retentionDurationLimit
)

$serviceUrl = $serviceUrl.TrimStart().TrimEnd()
if (-Not $serviceUrl.EndsWith('/'))
{
    $serviceUrl = $serviceUrl + '/'
}

$resolverUrlExtention = 'Cxwebinterface/CxWSResolver.asmx?wsdl'
$resolverUrl = $serviceUrl + $resolverUrlExtention
$resolver = New-WebServiceProxy -Uri $resolverUrl -UseDefaultCredential

if (!$resolver)
{
    "Could not resolve service URL."
    "Service might be down or a wrong URL was supplied."
    Exit
}


$webServiceAddressObject = $resolver.GetWebServiceUrl('SDK' ,1)



$proxy = New-WebServiceProxy -Uri $webServiceAddressObject.ServiceURL -UseDefaultCredential
if (!$proxy)
{
    "Could not find Checkmarx SDK service URL"
    Exit
}

$namespace = $proxy.GetType().Namespace

$credentialsType = ($namespace + '.Credentials')
$credentials = New-Object ($credentialsType)
$credentials.User = $username
$credentials.Pass = $pass

$loginResponse = $proxy.Login($credentials, 1033)
If(-Not $loginResponse.IsSuccesfull)
{
                "An Error occurred while logging in:"
                $loginResponse.ErrorMessage
}
Else
{
                $sessionId = $loginResponse.SessionId
                $retentionConfigurationType = ($namespace + '.CxDataRetentionConfiguration')
                $retentionConfiguration = New-Object ($retentionConfigurationType)
                
                If ($StartRetention.IsPresent)
                {
                
                    If($ByNumOfScans.IsPresent)
                    {
                                    $retentionConfiguration.DataRetentionType = "NumOfScansToPreserve"
                                    $retentionConfiguration.NumOfScansToPreserve = $numOfScansToKeep
                    }
                    Else
                    {
                        If($ByDateRange.IsPresent -OR $ByRollingDate.IsPresent)
                        { 
                                        $retentionConfiguration.DataRetentionType = "DatesRange"

                                        If($rollingDateRange)
                                        {
                                                        $startDate = Get-Date "2010-01-02"
                                                        $endDate = (Get-Date).AddDays(-$rollingDateRange)
                                                        
                                        }
                                        Else{
                                        
                                                        If(!($startDate.IsPresent)){
                                                                       
                                                                        $startDate = Get-Date "2010-01-01"
                                                        }
                                                       
                                                        $startDate = ($startDate).AddDays(1)
                                                        $endDate = ($endDate).AddDays(1)
                                        }                                               
                                        $retentionConfiguration.StartDate = $startDate.ticks
                                        $retentionConfiguration.EndDate = $endDate.ticks
                        }
                    }
                    If($retentionDurationLimit)
                    {
                                    $retentionConfiguration.DurationLimitInHours = $retentionDurationLimit
                    }
                    
                    
                    $retentionResponse = $proxy.ExecuteDataRetention($sessionId, $retentionConfiguration)
                    If($retentionResponse.IsSuccesfull)
                    {
                                    "Data retention ran successfully"
                    }
                    else
                    {
                                    "An error occurred while trying to start data retention:"
                                    $retentionResponse.ErrorMessage
                    }
                }
                else 
                {
                    $retentionResponse = $proxy.StopDataRetention($sessionId)
                    
                    If($retentionResponse.IsSuccesfull)
                    {
                                    "Data retention stopped"
                    }
                    else
                    {
                                    "An error occurred while trying to stop data retention:"
                                    $retentionResponse.ErrorMessage
                    }
                }
                   
                
                
                $loginResponse = $proxy.Logout($sessionId)
}