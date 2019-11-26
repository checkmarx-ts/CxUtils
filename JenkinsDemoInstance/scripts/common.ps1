$dir = Split-Path $StorageLoc

if ("" -eq $dir -or $null -eq $dir)
{
    $StorageLoc = (Get-Location).Path + "\" + $StorageLoc
}


if (-Not (Test-Path $StorageLoc) )
{
    $null = New-Item $StorageLoc -ItemType Directory
}

docker pull $JenkinsImage