param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$sast_url,
    [Parameter(Mandatory = $true)]
    [String]$username,
    [Parameter(Mandatory = $true)]
    [String]$password,
    [Parameter(Mandatory = $true)]
    [String]$csv_path,
    [Switch]$dbg
)

. "support/debug.ps1"

setupDebug($dbg.IsPresent)

#check to csv path
#validate csv values
#login to checkmarx
#update all result states

# Validate the CSV file exists
if (!(Test-Path -Path $csv_path -PathType Leaf)) {
    Throw "A file was not found at ${csv_path}."
}

Write-Output "Csv file was found"

# Validate the CSV File first and exit with any error. 
$validationLine = 0
Import-Csv $csv_path | ForEach-Object {
    $validationLine++

    if ($null -eq $_.project_name) {
        Throw "Error processing $_ - a project_name field does not exist on line ${validationLine}."
    }
    if ($null -eq $_.scanID) {
        Throw "Error processing $_ - a scanID field does not exist on line ${validationLine}."
    }
    if ($null -eq $_.resultId) {
        Throw "Error processing $_ - a resultID field does not exist on line ${validationLine}."
    }
    if ($null -eq $_.SimilarityId) {
        Throw "Error processing $_ - a SimilarityId field does not exist on line ${validationLine}."
    }
    if ($null -eq $_.current_state_id) {
        Throw "Error processing $_ - a current_state_id field does not exist on line ${validationLine}."
    }
    if ($null -eq $_.previous_state_id) {
        Throw "Error processing $_ - a previous_state_id field does not exist on line ${validationLine}."
    }
}

Write-Output "CSV file was validated. Ready to start the update for $validationLine records"

#get token to start updating records
$session = &"support/rest/sast/login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent
$updatecomment = "Reverting result state to previous state"

$timer = $(Get-Date)

Import-Csv $csv_path | ForEach-Object {
    &"support/rest/sast/patchResult.ps1" $session $_.scanID $_.resultID $_.previous_state_id $updatecomment
    
    $output = [String]::Format("Result state of scan: {0} resultID: {1} has been updated to {2}", $_.scanID, $_.resultID, $_.previous_result_state)
    Write-Output $output
}

Write-Output "All records have been successfully updated"