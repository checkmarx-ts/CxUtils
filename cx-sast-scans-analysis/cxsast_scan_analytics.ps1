$VERSION = '1.1'
$server = ""
$cxUsername = ""
$cxPassword = ""
$serverRestEndpoint = ""
$tableFile = ".\summary.txt"
$dataFile = ".\data.csv"

$mark0 = Get-Date
$excel = $null
$workbook = $null
$global:chartCount = 1
$global:pivotOffset = 1
$global:chartOffset = 0
$global:cornerCell = "A1"

$obfuscate = $false
$useExcel = $false

$startDate = Get-Date

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function showForm(){
    $form = New-Object System.Windows.Forms.Form
    $form.ShowIcon = $false
    $form.Text = 'CxSAST Scans Analysis ' + $VERSION
    $form.Size = New-Object System.Drawing.Size(490,270)
    $form.StartPosition = 'CenterScreen'

    $OKButton = New-Object System.Windows.Forms.Button
    $OKButton.Location = New-Object System.Drawing.Point(150,185)
    $OKButton.Size = New-Object System.Drawing.Size(75,23)
    $OKButton.Text = 'RUN'
    $OKButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
    $form.AcceptButton = $OKButton
    $form.Controls.Add($OKButton)

    $CancelButton = New-Object System.Windows.Forms.Button
    $CancelButton.Location = New-Object System.Drawing.Point(235,185)
    $CancelButton.Size = New-Object System.Drawing.Size(75,23)
    $CancelButton.Text = 'CANCEL'
    $CancelButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    $form.CancelButton = $CancelButton
    $form.Controls.Add($CancelButton)

    $label = New-Object System.Windows.Forms.Label
    $label.Location = New-Object System.Drawing.Point(20,20)
    $label.Size = New-Object System.Drawing.Size(130,20)
    $label.Text = 'CxSAST Host:'
    $form.Controls.Add($label)

    $cxServer = New-Object System.Windows.Forms.TextBox
    $cxServer.Location = New-Object System.Drawing.Point(150,20)
    $cxServer.Size = New-Object System.Drawing.Size(250,20)
    $form.Controls.Add($cxServer)

    $label = New-Object System.Windows.Forms.Label
    $label.Location = New-Object System.Drawing.Point(20,45)
    $label.Size = New-Object System.Drawing.Size(130,20)
    $label.Text = 'CxSAST Username:'
    $form.Controls.Add($label)

    $cxUser = New-Object System.Windows.Forms.TextBox
    $cxUser.Location = New-Object System.Drawing.Point(150,45)
    $cxUser.Size = New-Object System.Drawing.Size(150,20)
    $form.Controls.Add($cxUser)

    $label = New-Object System.Windows.Forms.Label
    $label.Location = New-Object System.Drawing.Point(20,70)
    $label.Size = New-Object System.Drawing.Size(130,20)
    $label.Text = 'CxSAST Password:'
    $form.Controls.Add($label)

    $cxPass = New-Object Windows.Forms.MaskedTextBox
    $cxPass.PasswordChar = '*'
    $cxPass.Location = New-Object System.Drawing.Point(150,70)
    $cxPass.Size = New-Object System.Drawing.Size(150,20)
    $form.Controls.Add($cxPass)

    $label = New-Object System.Windows.Forms.Label
    $label.Location = New-Object System.Drawing.Point(20,95)
    $label.Size = New-Object System.Drawing.Size(130,20)
    $label.Text = 'Report Type'
    $form.Controls.Add($label)

    $rptPanel = New-Object System.Windows.Forms.Panel
    $rptPanel.Location = '150,95'
    $rptPanel.size = '220,20'

    $xlsButton = New-Object System.Windows.Forms.RadioButton
    $xlsButton.Location = '1,1'
    $xlsButton.size = '70,20'
    $xlsButton.Checked = $true 
    $xlsButton.Text = "Excel"
    $rptPanel.Controls.Add($xlsButton)
 
    $csvButton = New-Object System.Windows.Forms.RadioButton
    $csvButton.Location = '70,1'
    $csvButton.size = '150,20'
    $csvButton.Checked = $false
    $csvButton.Text = "Text Summary + CSV"
    $rptPanel.Controls.Add($csvButton)

    $form.Controls.Add($rptPanel)

    $label = New-Object System.Windows.Forms.Label
    $label.Location = New-Object System.Drawing.Point(20,120)
    $label.Size = New-Object System.Drawing.Size(130,20)
    $label.Text = 'Time Frame'
    $form.Controls.Add($label)

    $allTimeButton = New-Object System.Windows.Forms.RadioButton
    $allTimeButton.Location = '150,120'
    $allTimeButton.size = '70,20'
    $allTimeButton.Checked = $false 
    $allTimeButton.Text = "All Time"
    $form.Controls.Add($allTimeButton)
 
    $sixMoButton = New-Object System.Windows.Forms.RadioButton
    $sixMoButton.Location = '220,120'
    $sixMoButton.size = '100,20'
    $sixMoButton.Checked = $false
    $sixMoButton.Text = "Last 6 months"
    $form.Controls.Add($sixMoButton)

    $threeMoButton = New-Object System.Windows.Forms.RadioButton
    $threeMoButton.Location = '320,120'
    $threeMoButton.size = '150,20'
    $threeMoButton.Checked = $true
    $threeMoButton.Text = "Last 3 months"
    $form.Controls.Add($threeMoButton)


    $privateCBX = New-Object System.Windows.Forms.CheckBox
    $privateCBX.Location = '150,145'
    $privateCBX.size = '350,20'
    $privateCBX.Checked = $false
    $privateCBX.Text = "Remove any identifying information (e.g., project name)"
    $form.Controls.Add($privateCBX)

    $cxServer.Text = $server
    $cxUser.Text = $cxUsername
    $cxPass.Text = $cxPassword

    $tooltip1 = New-Object System.Windows.Forms.ToolTip
    $tooltip1.SetToolTip($csvButton, "Only available option when running this utility from a machine without MS Excel installed.")

    try{
        #will fail if Excel not installed on the system running this script
        $excel = New-Object -ComObject excel.application -ErrorAction Stop
        $workbook = $excel.Workbooks.Add()
        Add-Type -AssemblyName Microsoft.Office.Interop.Excel
        $xlChart=[Microsoft.Office.Interop.Excel.XLChartType]
        } 
    catch {
        $xlsButton.Enabled = $false
        $xlsButton.Checked = $false
        $csvButton.Checked = $true
    }

    $form.Topmost = $true
    $result = $form.ShowDialog()

    if ($result -eq [System.Windows.Forms.DialogResult]::OK)
    {
        $server = $cxServer.Text
        $serverRestEndpoint = $server + "/CxRestAPI/"
        $cxUsername = $cxUser.Text
        $cxPassword = $cxPass.Text
        $obfuscate = $privateCBX.Checked

        if($allTimeButton.Checked -eq $true){
            $startDate = (Get-Date).AddYears(-1000)
        }
        elseif ($threeMoButton.Checked -eq $true){
            $startDate = (Get-Date).AddMonths(-3)
        }
        else {
            $startDate = (Get-Date).AddMonths(-6)
        }

        If($csvButton.Checked -eq $true){
            $useExcel = $false
        }
        Else{
            $useExcel = $true
        }

        generatedReports
    }

}

function getDurationFromMark($mark){
    $now = Get-Date
    return New-TimeSpan -Start $mark -End $now
}

function getOAuth2Token(){
    $body = @{
        username = $cxUsername
        password = $cxPassword
        grant_type = "password"
        scope = "sast_rest_api"
        client_id = "resource_owner_client"
        client_secret = "014DF517-39D1-4453-B7B3-9930C563627C"
    }
    
    try {
        $response = Invoke-RestMethod -uri "${serverRestEndpoint}auth/identity/connect/token" -method post -body $body -contenttype 'application/x-www-form-urlencoded'
        return $response.token_type + " " + $response.access_token
    } catch {
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        throw "Could not authenticate"
    }
}

function getAllScans(){
    $headers = @{
        Authorization = $token
    }
    try {
        $response = Invoke-RestMethod -uri "${serverRestEndpoint}sast/scans" -method get -headers $headers -contenttype 'application/json;v=1.0'
        return $response
    } catch {
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        throw "Cannot get scans"
    }
}

function getScanResultStatistics($scanID){
    $headers = @{
        Authorization = $token
    }
    try {
        $response = Invoke-RestMethod -uri "${serverRestEndpoint}sast/scans/$scanID/resultsStatistics" -method get -headers $headers -contenttype 'application/json;v=1.0'
        return $response
    } catch {
        return $null
    }
}

function buildScansDataTable($scans){
    $data = @()

    foreach($scan in $scans) {
        #check if scan date is valid and should be included in the report
        try { $include = (Get-Date $scan.dateAndTime.startedOn) -gt $startDate} catch { }
        if($include -eq $true){
            #get result counts for the scan
            $resultStatistics = getScanResultStatistics $scan.id
            $totalResults = $resultStatistics.highSeverity + $resultStatistics.mediumSeverity + $resultStatistics.lowSeverity + $resultStatistics.infoSeverity;

            Switch ($totalResults){
                {$_ -lt 500} {$resultsBucket = "< 500 results"}
                {$_ -ge 500 -and $_ -le 1000} {$resultsBucket = "500 - 1,000 results"}
                {$_ -ge 1001 -and $_ -le 10000} {$resultsBucket = "1000 - 10,000 results"}
                {$_ -ge 10001 -and $_ -le 100000} {$resultsBucket = "10,000 - 100,000 results"}
                {$_ -gt 100001} {$resultsBucket = "Fast (> 100,000 results)"}
            }

            

            #calculate the duration of the scan
            try {
                $scanDuration = New-TimeSpan -Start $scan.dateAndTime.engineStartedOn -End $scan.dateAndTime.engineFinishedOn
                $scanDurationInMinutes = $scanDuration.Minutes
                $scanDurationInHours = $scanDuration.Minutes / 60
                }
            catch { $scanDuration = 0 }

            #calculate the queue duration of the scan
            try {
                $queueDuration = New-TimeSpan -Start $scan.dateAndTime.startedOn -End $scan.dateAndTime.engineStartedOn
                }
            catch { $queueDuration = $null }

            #bucket by LOC
            Switch ($scan.scanState.linesofCode){
                {$_ -ge 1 -and $_ -le 1000} {$LOCrange = "1 - 1,000"}
                {$_ -ge 1001 -and $_ -le 10000} {$LOCrange = "1,001 - 10,000"}
                {$_ -ge 10001 -and $_ -le 100000} {$LOCrange = "10,001 - 100,000"}
                {$_ -ge 100001 -and $_ -le 250000} {$LOCrange = "100,001 - 250,000"}
                {$_ -ge 250001 -and $_ -le 500000} {$LOCrange = "250,001 - 500,000"}
                {$_ -ge 500001 -and $_ -le 1000000} {$LOCrange = "500,001 - 1,000,000"}
                {$_ -ge 1000001 -and $_ -le 2000000} {$LOCrange = "1,000,001 - 2,000,000"}
                {$_ -ge 2000001 -and $_ -le 3000000} {$LOCrange = "2,000,001 - 3,000,000"}
                {$_ -ge 3000001} {$LOCrange = "3,000,001+"}
            }

            #date data
            try { $dayOfTheWeek = (Get-Date $scan.dateAndTime.startedOn).DayOfWeek;} catch {$dayOfTheWeek = $null}
            try { $shortDate = (Get-Date $scan.dateAndTime.startedOn).ToShortDateString()} catch {$shortDate = $null}

            #scan time
            Switch ($scanDurationInMinutes){
                {$_ -ge 1 -and $_ -le 5} {$span = "1 - 5m"}
                {$_ -ge 6 -and $_ -le 10} {$span = "5m - 10m"}
                {$_ -ge 11 -and $_ -le 30} {$span = "10m - 30m"}
                {$_ -ge 30 -and $_ -le 60} {$span = "30m - 60m"}
                {$_ -ge 61 -and $_ -le 180} {$span = "1h - 3h"}
                {$_ -ge 181 -and $_ -le 600} {$span = "3h - 10h"}
                {$_ -ge 601 -and $_ -le 1440} {$span = "10h - 24h"}
                {$_ -ge 1441} {$span = "24h+"}
            }

            #scan speed
            try {
                $LOCperHour = $scan.scanState.linesofCode / $scanDurationInHours;
            }
            catch { $LOCperHour = $null}

            Switch ($LOCperHour){
                {$_ -lt 100000} {$speed = "Slow (< 100,000 LOC/hr)"}
                {$_ -ge 100000 -and $_ -le 500000} {$speed = "Normal"}
                {$_ -gt 500001} {$speed = "Fast (> 500,000 LOC/hr)"}
            }

            #populate the data table
            $data += [pscustomobject]@{
                #Primary Project/Scan Metrics
                projectName = If($obfuscate -eq $true) { "[ID=" + $scan.project.id + "]" } Else { $scan.project.name }; 
                scanId = $scan.id; 
                origin = If ($null -eq $scan.origin) { "Unknown" } Else { $scan.origin } 
                scanStatus = $scan.status.name;
                fullOrIncremental = If ($scan.isIncremental -eq "True") {"Incremental"} Else {"Full"};
                publicOrPrivate = If ($scan.isPublic -eq "True") {"Public"} Else {"Private"};

                #Date/Time Metrics
                startedOn = $scan.dateAndTime.startedOn;
                startedOnShortDate = $shortDate;
                startedOnDay = $dayOfTheWeek;
                finishedOn = $scan.dateAndTime.finishedOn;
                engineStartedOn = $scan.dateAndTime.engineStartedOn;
                engineFinishedOn = $scan.dateAndTime.engineFinishedOn;
                scanDuration = $scanDuration;
                queueDuration = $queueDuration;
                scanDurationInHours = $scanDurationInHours;
                durationRange = $span;

                #LOC/ File Metrics
                fileCount = $scan.scanState.filesCount;
                LOC = $scan.scanState.linesofCode;
                LOCrange = $LOCrange;
                failedLOC = $scan.scanState.failedLinesOfCode;
                LOCpHr = $LOCperHour;
                scanSpeed = $speed;
                
                #Results Metrics
                total = $totalResults;
                high = $resultStatistics.highSeverity;
                medium = $resultStatistics.mediumSeverity;
                low = $resultStatistics.lowSeverity;
                info = $resultStatistics.infoSeverity;
                resultCountRange = $resultsBucket;

                #Secondary Project/Scan Metrics
                projectId = $scan.project.id; 
                sourceID = $scan.scanState.sourceID;
                scanType = $scan.scanType.value;
                cxVersion = If($null -eq $scan.scanState.cxVersion) { "Unknown" } Else { $scan.scanState.cxVersion };
                initiatorName = $scan.initiatorName;
                teamID = $scan.owningTeamId;

                #Engine Metrics
                engineID = $scan.engineServer.id;
                engineName = If($obfuscate -eq $true) { $scan.engineServer.id; } Else { If ($null -eq $scan.engineServer.name) { "Unknown" } Else { $scan.engineServer.name } };

                #Language Metrics
                languages = $scan.scanState.languageStateCollection.languageName -join ","
                Unknown = If ($scan.scanState.languageStateCollection.languageName -contains "Unknown") { 1 } Else { 0 };
                CSharp = If ($scan.scanState.languageStateCollection.languageName -contains "CSharp") { 1 } Else { 0 };
                Java = If ($scan.scanState.languageStateCollection.languageName -contains "Java") { 1 } Else { 0 };
                CPP = If ($scan.scanState.languageStateCollection.languageName -contains "CPP") { 1 } Else { 0 };
                JavaScript = If ($scan.scanState.languageStateCollection.languageName -contains "JavaScript") { 1 } Else { 0 };
                Apex = If ($scan.scanState.languageStateCollection.languageName -contains "Apex") { 1 } Else { 0 };
                VbNet = If ($scan.scanState.languageStateCollection.languageName -contains "VbNet") { 1 } Else { 0 };
                VbScript = If ($scan.scanState.languageStateCollection.languageName -contains "VbScript") { 1 } Else { 0 };
                ASP = If ($scan.scanState.languageStateCollection.languageName -contains "ASP") { 1 } Else { 0 };
                VB6 = If ($scan.scanState.languageStateCollection.languageName -contains "VB6") { 1 } Else { 0 };
                PHP = If ($scan.scanState.languageStateCollection.languageName -contains "PHP") { 1 } Else { 0 };
                Ruby = If ($scan.scanState.languageStateCollection.languageName -contains "Ruby") { 1 } Else { 0 };
                Perl = If ($scan.scanState.languageStateCollection.languageName -contains "Perl") { 1 } Else { 0 };
                Objc = If ($scan.scanState.languageStateCollection.languageName -contains "Objc") { 1 } Else { 0 };
                PLSQL = If ($scan.scanState.languageStateCollection.languageName -contains "PLSQL") { 1 } Else { 0 };
                Python = If ($scan.scanState.languageStateCollection.languageName -contains "Python") { 1 } Else { 0 };
                Groovy = If ($scan.scanState.languageStateCollection.languageName -contains "Groovy") { 1 } Else { 0 };
                Scala = If ($scan.scanState.languageStateCollection.languageName -contains "Scala") { 1 } Else { 0 };
                Go = If ($scan.scanState.languageStateCollection.languageName -contains "Go") { 1 } Else { 0 };
                Typescript = If ($scan.scanState.languageStateCollection.languageName -contains "Typescript") { 1 } Else { 0 };
                Kotlin = If ($scan.scanState.languageStateCollection.languageName -contains "Kotlin") { 1 } Else { 0 };
                Common = If ($scan.scanState.languageStateCollection.languageName -contains "Common") { 1 } Else { 0 }

                #Long field at the end
                path = If($obfuscate -eq $true) { "Redacted" } Else { $scan.scanState.path };
                comment = If($obfuscate -eq $true) { "Redacted" } Else { $scan.comment };
                }
        }
    }

    return $data
}

function getPivotCount($data, $tableTitle, $tableField, $onlyFinished, $writeToSummaryTxtFile){
    if($onlyFinished -eq $true){
        $total = ($data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} | Measure-Object).Count
        $table = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} |
            Select-Object $tableField | 
            Group-Object -Property $tableField -NoElement |
            Sort-Object count -Descending | 
            Select-Object  @{L = $tableTitle; E = {$_.Name} },
                    @{L = 'Count' ; E = {$_.count} },
                    @{L = 'Percent' ; E = {“{0:p2}” -f ($_.count / $total)}} 
    
        if($writeToSummaryTxtFile -eq $true) {
            $table | Format-Table | Out-File $tableFile -Append
        }         
    }
    else {
        $total = $data.Count
        $table = $data | Select-Object $tableField | 
                Group-Object -Property $tableField -NoElement |
                Sort-Object count -Descending | 
                Select-Object  @{L = $tableTitle; E = {$_.Name} },
                        @{L = 'Count' ; E = {$_.count} },
                        @{L = 'Percent' ; E = {“{0:p2}” -f ($_.count / $total)}} 
        
        if($writeToSummaryTxtFile -eq $true) {
            $table | Format-Table | Out-File $tableFile -Append
        }  

    }
    return $table
}

function getSummary($data, $writeToSummaryTxtFile){
    $table = @()

    $highMetrics = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} | Measure-Object -Property high -Maximum -Sum -Average -Minimum
    $mediumMetrics = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} | Measure-Object -Property medium -Maximum -Sum -Average -Minimum
    $lowMetrics = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} | Measure-Object -Property low -Maximum -Sum -Average -Minimum
    $infoMetrics = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} | Measure-Object -Property info -Maximum -Sum -Average -Minimum
    $totalResults = $highMetrics.Sum + $mediumMetrics.Sum + $lowMetrics.Sum + $infoMetrics.Sum
    $totalScans = ($data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} | Measure-Object).Count

    $speedMetricsInc = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished" -and $_.fullOrIncremental -eq "Incremental"} | Measure-Object -Property LOCpHr -Maximum -Sum -Average -Minimum
    $speedMetricsFull = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished" -and $_.fullOrIncremental -eq "Full"} | Measure-Object -Property LOCpHr -Maximum -Sum -Average -Minimum

    $scansByDay = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} |
            Select-Object startedOnShortDate | 
            Group-Object -Property startedOnShortDate -NoElement | Measure-Object -Property Count -Maximum -Minimum -Average

    $fileCountMetrics = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished" -and $_.fullOrIncremental -eq "Full"} | Measure-Object -Property fileCount -Maximum -Sum -Average -Minimum

    $table += [pscustomobject]@{Metric = "All Scans"; Minimum = "N/A"; Maximum = "N/A"; Average = "N/A"; Total = $data.Count; Percent = (1).ToString("P") }
    $table += [pscustomobject]@{Metric = "All Results"; Minimum = "N/A"; Maximum = "N/A"; Average = [Math]::Round($totalResults / $totalScans); Total = $totalResults; Percent = (1).ToString("P") }
    $table += [pscustomobject]@{Metric = "High Results"; Minimum = $highMetrics.Minimum; Maximum = $highMetrics.Maximum; Average = [Math]::Round($highMetrics.Average); Total = $highMetrics.Sum; Percent = ($highMetrics.Sum / $totalResults).toString("P") }
    $table += [pscustomobject]@{Metric = "Medium Results"; Minimum = $mediumMetrics.Minimum; Maximum = $mediumMetrics.Maximum; Average = [Math]::Round($mediumMetrics.Average); Total = $mediumMetrics.Sum; Percent = ($mediumMetrics.Sum / $totalResults).toString("P") }
    $table += [pscustomobject]@{Metric = "Low Results"; Minimum = $lowMetrics.Minimum; Maximum = $lowMetrics.Maximum; Average = [Math]::Round($lowMetrics.Average); Total = $lowMetrics.Sum; Percent = ($lowMetrics.Sum / $totalResults).toString("P") }
    $table += [pscustomobject]@{Metric = "Info Results"; Minimum = $infoMetrics.Minimum; Maximum = $infoMetrics.Maximum; Average = [Math]::Round($infoMetrics.Average); Total = $infoMetrics.Sum; Percent = ($infoMetrics.Sum / $totalResults).toString("P") }
    $table += [pscustomobject]@{Metric = "Scan Speed Inc (LOC/hr)"; Minimum = [Math]::Round($speedMetricsInc.Minimum); Maximum = [Math]::Round($speedMetricsInc.Maximum); Average = [Math]::Round($speedMetricsInc.Average); Total = "N/A"; Percent = "N/A" }
    $table += [pscustomobject]@{Metric = "Scan Speed Full (LOC/hr)"; Minimum = [Math]::Round($speedMetricsFull.Minimum); Maximum = [Math]::Round($speedMetricsFull.Maximum); Average = [Math]::Round($speedMetricsFull.Average); Total = "N/A"; Percent = "N/A" }
    $table += [pscustomobject]@{Metric = "Scans per Day"; Minimum = $scansByDay.Minimum; Maximum = $scansByDay.Maximum; Average = [Math]::Round($scansByDay.Average); Total = "N/A"; Percent = "N/A" }
    $table += [pscustomobject]@{Metric = "File(s) per Scan"; Minimum = $fileCountMetrics.Minimum; Maximum = $fileCountMetrics.Maximum; Average = [Math]::Round($fileCountMetrics.Average); Total = "N/A"; Percent = "N/A" }

    if($writeToSummaryTxtFile -eq $true) {
        $table | Format-Table | Out-File $tableFile -Append
    }
    return $table
}

function getProjectSummary($data, $writeToSummaryTxtFile){
    $table = @()
    $projects = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} | Select-Object projectName | Sort-Object projectName -Unique

    foreach($project in $projects) {
        $subset = $data | Where-Object -FilterScript {$_.projectName -eq $project.projectName}
        $scanCount = $subset.scanID.Count
        $avgLOC = ($subset | Measure-Object -Property LOC -Average).Average
        $avgScanTimeInHrs = [Math]::Round((($subset | Measure-Object -Property scanDurationInHours -Average).Average),2)
        $avgResultCount = ($subset | Measure-Object -Property total -Average).Average
        
        $table += [pscustomobject]@{Project = $project.projectName; Scans = $scanCount; 'Avg Loc' = [Math]::Round($avgLOC); 'Avg Scan Time (Hrs)' = $avgScanTimeInHrs; 'Avg Results' = [Math]::Round($avgResultCount)}
    }

    if($writeToSummaryTxtFile -eq $true) {
        $table | Format-Table | Out-File $tableFile -Append
    }
    return $table
}

function getLanguageSummary($data, $writeToSummaryTxtFile){
    $languageList = "Unknown","CSharp","Java","CPP","JavaScript","Apex","VbNet","VbScript","ASP","VB6","PHP","Ruby","Perl","Objc","PLSQL","Python","Groovy","Scala","Go","Typescript","Kotlin","Common"
    $table = @()
    
    foreach($language in $languageList){
        $langCount = $data | Where-Object -FilterScript {$_.scanStatus -eq "Finished"} | Measure-Object -Property $language -Sum
        if($langCount.Sum -ne 0){
            $table += [pscustomobject]@{Language = $language; "Scans" = $langCount.Sum; "Percent" = ($langCount.Sum / $data.Count).ToString("P") }
        }
    }

    if($writeToSummaryTxtFile -eq $true) {
        $table | Sort-Object Scans -Descending | Format-Table | Out-File $tableFile -Append
    }

    return $table | Sort-Object Scans -Descending
}

function ConvertTo-MultiArray {
 <#
 .Notes
 NAME: ConvertTo-MultiArray
 AUTHOR: Tome Tanasovski
 Website: https://powertoe.wordpress.com
 Twitter: http://twitter.com/toenuff
 Version: 1.0
 CREATED: 11/5/2010
 LASTEDIT:
 11/5/2010 1.0
 Initial Release
 11/5/2010 1.1
 Removed array parameter and passes a reference to the multi-dimensional array as output to the cmdlet
 11/5/2010 1.2
 Modified all rows to ensure they are entered as string values including $null values as a blank ("") string.

 .Synopsis
 Converts a collection of PowerShell objects into a multi-dimensional array

 .Description
 Converts a collection of PowerShell objects into a multi-dimensional array.  The first row of the array contains the property names.  Each additional row contains the values for each object.

 This cmdlet was created to act as an intermediary to importing PowerShell objects into a range of cells in Exchange.  By using a multi-dimensional array you can greatly speed up the process of adding data to Excel through the Excel COM objects.

 .Parameter InputObject
 Specifies the objects to export into the multi dimensional array.  Enter a variable that contains the objects or type a command or expression that gets the objects. You can also pipe objects to ConvertTo-MultiArray.

 .Inputs
 System.Management.Automation.PSObject
        You can pipe any .NET Framework object to ConvertTo-MultiArray

 .Outputs
 [ref]
        The cmdlet will return a reference to the multi-dimensional array.  To access the array itself you will need to use the Value property of the reference

 .Example
 $arrayref = get-process |Convertto-MultiArray

 .Example
 $dir = Get-ChildItem c:\
 $arrayref = Convertto-MultiArray -InputObject $dir

 .Example
 $range.value2 = (ConvertTo-MultiArray (get-process)).value

 .LINK
 https://powertoe.wordpress.com

#>
    param(
        [Parameter(Mandatory=$true, Position=1, ValueFromPipeline=$true)]
        [PSObject[]]$InputObject
    )
    BEGIN {
        $objects = @()
        [ref]$array = [ref]$null
    }
    Process {
        $objects += $InputObject
    }
    END {
        $properties = $objects[0].psobject.properties | ForEach-Object{$_.name}
        $array.Value = New-Object 'object[,]' ($objects.Count+1),$properties.count
        # i = row and j = column
        $j = 0
        $properties | ForEach-Object{
            $array.Value[0,$j] = $_.tostring()
            $j++
        }
        $i = 1
        $objects | ForEach-Object {
            $item = $_
            $j = 0
            $properties | ForEach-Object {
                if ($null -eq $item.($_)) {
                    $array.value[$i,$j] = ""
                }
                else {
                    $array.value[$i,$j] = $item.($_).tostring()
                }
                $j++
            }
            $i++
        }
        $array
    }
}

function writeDatatoExcelFromCell($data, $sheet, $startCol, $Row, $endCol){
    $sheet.Activate()
    $array = ($data | ConvertTo-MultiArray).Value
    
    $range = $sheet.Range("$startCol$Row","$endCol$($array.GetLength(0) + $Row - 1)")
    $range.Value2 = $array

    #Format Excel -- Add borders, color
    $endHeader = $endCol + $Row
    $headerRange = $sheet.Range($startCol + $Row, $endHeader)
    $headerRange.Font.Bold = $true
    $headerRange.Interior.ColorIndex = 35

    foreach($item in @(11,12,8,10,7,9)){
        $sheet.Range($startCol + $Row).CurrentRegion.Borders.Item($item).Weight = 1
        $sheet.Range($startCol + $Row).CurrentRegion.Borders.Item($item).LineStyle = 1
    }
}

function writeDatatoExcel($data, $sheet){
    $sheet.Activate()
    $array = ($data | ConvertTo-MultiArray).Value

    $starta = [int][char]'a' - 1
    if ($array.GetLength(1) -gt 26) {
        $col = [char]([int][math]::Floor($array.GetLength(1)/26) + $starta) + [char](($array.GetLength(1)%26) + $Starta)
    } else {
        $col = [char]($array.GetLength(1) + $starta)
    }
    
    $range = $sheet.Range("A$global:pivotOffset","$col$($array.GetLength(0) + $global:pivotOffset - 1)")
    $range.Value2 = $array

    #Format Excel -- Add borders, color
    $endHeader = $col + $global:pivotOffset
    $headerRange = $sheet.Range("A$global:pivotOffset", $endHeader)
    $headerRange.Font.Bold = $true
    $headerRange.Interior.ColorIndex = 35

    foreach($item in @(11,12,8,10,7,9)){
        $sheet.Range("A$global:pivotOffset").CurrentRegion.Borders.Item($item).Weight = 1
        $sheet.Range("A$global:pivotOffset").CurrentRegion.Borders.Item($item).LineStyle = 1
    }

    if($sheet.Name -ne "Raw Data") {
        $global:cornerCell = "A$global:pivotOffset"
        $global:pivotOffset = $sheet.UsedRange.rows.count + 2
    }
    else {
        $headerRange.AutoFilter() | Out-Null
    }
}
function writeChartDataExcel($x, $y, $width, $height, $title, $sheet, $chartType, $showLegend){
    $sheet.Activate()
    $dataForChart = $workbook.Worksheets.Item(2).Range($global:cornerCell).CurrentRegion
    
    #drop Percent column and header from data range for chart
    $dataForChart = $dataForChart.Offset(1,0).Resize($dataForChart.Rows.Count - 1, $dataForChart.Columns.Count - 1)
    
    $chart = $sheet.Shapes.AddChart().Chart
    $chart.HasTitle = $true
    $chart.ChartTitle.Text = $title
    $chart.SetSourceData($dataForChart)
    $chart.HasLegend = $showLegend
    $chart.ChartType = $chartType
    $sheet.shapes.item("Chart $chartCount").top = $y
    $sheet.shapes.item("Chart $chartCount").left = $x
    $sheet.shapes.item("Chart $chartCount").width = $width
    $sheet.shapes.item("Chart $chartCount").height = $height

    $global:chartCount++
    $global:chartOffset += $height + 10
}

function addPivotAndChart($data, $pivotSheet, $x, $y, $width, $height, $title, $chartSheet, $chartType, $showLegend, $field, $onlyFinished, $writeToSummaryTxtFile) {
    #Get Pivot table data
    $table = getPivotCount $data $title $field $onlyFinished $writeToSummaryTxtFile
    
    #Write table to Pivot Sheet
    $pivotSheet.Activate()
    $array = ($table | ConvertTo-MultiArray).Value

    $starta = [int][char]'a' - 1
    if ($array.GetLength(1) -gt 26) {
        $col = [char]([int][math]::Floor($array.GetLength(1)/26) + $starta) + [char](($array.GetLength(1)%26) + $Starta)
    } else {
        $col = [char]($array.GetLength(1) + $starta)
    }

    $range = $pivotSheet.Range("A$global:pivotOffset","$col$($array.GetLength(0) + $global:pivotOffset - 1)")
    $range.Value2 = $array

    #Format table
    $beginHeader = "A$global:pivotOffset"
    $endHeader = "$col$($global:pivotOffset)"
    $headerRange = $pivotSheet.Range($beginHeader, $endHeader)
    $headerRange.Font.Bold = $true
    $headerRange.Interior.ColorIndex = 35

    foreach($item in @(11,12,8,10,7,9)){
        $range.Borders.Item($item).Weight = 1
        $range.Borders.Item($item).LineStyle = 1
    }

    if($pivotSheet.Name -ne "Raw Data") {
        $global:cornerCell = "A$global:pivotOffset"
        $global:pivotOffset = $pivotSheet.UsedRange.rows.count + 2
    }

    #Add Chart
    $chartSheet.Activate()
    $dataForChart = $workbook.Worksheets.Item(2).Range($global:cornerCell).CurrentRegion
    
    #drop Percent column and header row from data range for chart
    $dataForChart = $dataForChart.Offset(1,0).Resize($dataForChart.Rows.Count - 1, $dataForChart.Columns.Count - 1)
    
    $chart = $chartSheet.Shapes.AddChart().Chart
    $chart.HasTitle = $true
    $chart.ChartTitle.Text = $title
    $chart.SetSourceData($dataForChart)
    #$chart.Axes(1,2)
    $chart.HasLegend = $showLegend
    $chart.ChartType = $chartType
    $chartSheet.shapes.item("Chart $chartCount").top = $y
    $chartSheet.shapes.item("Chart $chartCount").left = $x
    $chartSheet.shapes.item("Chart $chartCount").width = $width
    $chartSheet.shapes.item("Chart $chartCount").height = $height

    $global:chartCount++
    $global:chartOffset += $height + 10
}

function addTableWithoutPivot($chartSheet, $rawDataSheet, $title, $range, $chartType){
    $chartSheet.Activate()
    $dataForChart = $rawDataSheet.Range($range)
    $dataForChart.Interior.ColorIndex = 55

    $chart = $chartSheet.Shapes.AddChart().Chart
    $chart.HasTitle = $true
    $chart.ChartTitle.Text = $title
    $chart.SetSourceData($dataForChart)
    
    
    #$chart.HasLegend = $showLegend
    $chart.ChartType = $chartType
    #$chartSheet.shapes.item("Chart $chartCount").top = $y
    #$chartSheet.shapes.item("Chart $chartCount").left = $x
    #$chartSheet.shapes.item("Chart $chartCount").width = $width
    #$chartSheet.shapes.item("Chart $chartCount").height = $height

    $global:chartCount++
    $global:chartOffset += $height + 10

}

function generatedReports(){
    Clear-Host
    Remove-Item $tableFile -ErrorAction SilentlyContinue
    Remove-Item $dataFile -ErrorAction SilentlyContinue

    #get auth token
    Write-Host "Authenticating..."
    $mark = Get-Date
    $token = getOAuth2Token

    #get all scans
    Write-Host "Retrieving all scans..."
    $mark = Get-Date
    $scans = getAllScans

    #build raw data table with all scans data including result counts
    Write-Host "Retrieving all scan data..."
    $mark = Get-Date
    $data = buildScansDataTable $scans

    if($useExcel -eq $true){
        #Create worksheets in Excel workbook
        Write-Host "Building Excel report..."
        $rawDataSheet = $workbook.Worksheets.Item(1)
        $rawDataSheet.Name = "Raw Data"
        $pivotSheet = $workbook.Worksheets.Add()
        $pivotSheet.Name = "Tables"
        $pivotSheet.columns.item('A').NumberFormat = "@"
        $chartSheet = $workbook.Worksheets.Add()
        $chartSheet.Name = "Charts"

        #Build raw data worksheet
        writeDatatoExcel $data $rawDataSheet

        #Build all pivot tables and charts and add them to the workbook
        #addPivotAndChart($data, $pivotSheet, $x, $y, $width, $height, $title, $chartSheet, $chartType, $showLegend, $field, $onlyFinished, $writeToSummaryTxtFile)
        addPivotandChart $data $pivotSheet 0 $global:chartOffset 450 150 "Scan Status (All Scans)" $chartSheet $xlChart::xlBarClustered $false "scanStatus" $false $false
        addPivotandChart $data $pivotSheet 0 $global:chartOffset 450 150 "Scan Type (All Scans)" $chartSheet $xlChart::xlPie $true "fullOrIncremental" $false $false
        addPivotandChart $data $pivotSheet 0 $global:chartOffset 450 250 "CxSAST Version (All Scans)" $chartSheet $xlChart::xlBarStacked $false "cxVersion" $true $false
        $table = getLanguageSummary $data $false
        writeDatatoExcel $table $pivotSheet
        writeChartDataExcel 0 $global:chartOffset 450 600 "Scans by Language (Finished Scans)" $chartSheet $xlChart::xlBarStacked $false

        $global:chartOffset = 0

        addPivotandChart $data $pivotSheet 460 $global:chartOffset 450 250 "Scan Origin (All Scans)" $chartSheet $xlChart::xlBarStacked $false "origin" $false $false
        addPivotandChart $data $pivotSheet 460 $global:chartOffset 450 200 "LOC per Scan (All Scans)" $chartSheet $xlChart::xlBarStacked $false "LOCrange" $false $false
        addPivotandChart $data $pivotSheet 460 $global:chartOffset 450 200 "Results per Scan (Finished Scans)" $chartSheet $xlChart::xlBarStacked $false "resultCountRange" $true $false
        addPivotandChart $data $pivotSheet 460 $global:chartOffset 450 200 "Scans by Engine (Finished Scans)" $chartSheet $xlChart::xlBarStacked $false "engineName" $true $false

        $global:chartOffset = 0

        addPivotandChart $data $pivotSheet 920 $global:chartOffset 450 200 "Scan Speed (Finished Scans)" $chartSheet $xlChart::xlBarStacked $false "scanSpeed" $true $false
        addPivotandChart $data $pivotSheet 920 $global:chartOffset 450 200 "Scan Duration (Finished Scans)" $chartSheet $xlChart::xlBarStacked $false "durationRange" $true $false
        addPivotandChart $data $pivotSheet 920 $global:chartOffset 450 200 "Scans Submited by Day of the Week (Finished Scans)" $chartSheet $xlChart::xlBarStacked $false "startedOnDay" $true $false
        addPivotandChart $data $pivotSheet 920 $global:chartOffset 450 200 "Scans by Team (All Scans)" $chartSheet $xlChart::xlBarStacked $false "teamId" $false $false
    
        $table = getSummary $data $false
        writeDatatoExcelFromCell $table $pivotSheet "E" 1 "J"
        $table = getProjectSummary $data $false
        writeDatatoExcelFromCell $table $pivotSheet "E" 13 "I"

        #addTableWithoutPivot $chartSheet $rawDataSheet "Scanned LOC per Hour" "R1:R48,O1:O48" $xlChart::xlXYScatter

        #formatting excel
        $rawDataSheet.UsedRange.Columns.Autofit() | Out-Null
        $pivotSheet.UsedRange.Columns.Autofit() | Out-Null
    
        $excel.visible = $True
    }
    else {
        #export raw data table to CSV
        Write-Host "Exporting CSV File..."
        $data | Export-Csv -Path $dataFile
    
        #calculate specific metrics
        Write-Host "Exporting Summary File..."
        $table = getSummary $data $true
        $table = getPivotCount $data "SCAN STATUS" "scanStatus" $false $true
        $table = getPivotCount $data "SCAN TYPE" "fullOrIncremental" $false $true
        $table = getPivotCount $data "CX VERSION (FINISHED SCANS)" "cxVersion" $true $true
        $table = getPivotCount $data "SCAN ORIGIN (FINISHED SCANS)" "origin" $true $true
        $table = getPivotCount $data "LOC (FINISHED SCANS)" "LOCrange" $true $true
        $table = getPivotCount $data "RESULTS (FINISHED SCANS)" "resultCountRange" $true $true
        $table = getPivotCount $data "SCAN SPEED (FINISHED SCANS)" "scanSpeed" $true $true
        $table = getPivotCount $data "DURATION (FINISHED SCANS)" "durationRange" $true $true
        $table = getPivotCount $data "DAY OF WEEK" "startedOnDay" $true $true
        $table = getLanguageSummary $data $true
        $table = getPivotCount $data "ENGINE (FINISHED SCANS)" "engineName" $true $true
        $table = getPivotCount $data "SCANS BY TEAM" "teamID" $false $true
        $table = getProjectSummary $data $true

        Invoke-Item $tableFile
    }

    Write-Host "Export complete."
    Write-Host "Time to complete:  " -NoNewline
    getDurationFromMark $mark0 | Write-Host
}

showForm
