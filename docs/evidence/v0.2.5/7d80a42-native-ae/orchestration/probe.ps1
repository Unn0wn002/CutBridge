$ErrorActionPreference='Stop'
$cbOut='C:\CutBridgeEvidence'
$cbReport=@{username=$env:USERNAME;owner_home_visible=(Test-Path 'C:\Users\unn0w');credential_environment_present=[bool]($env:GH_TOKEN -or $env:GITHUB_TOKEN -or $env:AWS_SECRET_ACCESS_KEY);blender_installed=(Test-Path 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe');ae_installed=(Test-Path 'C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe');network_adapters=@(Get-NetAdapter | Select-Object Name,Status);host_shares=@(Get-CimInstance Win32_LogicalDisk | Select-Object DeviceID,DriveType,ProviderName)}
$cbReport | ConvertTo-Json -Depth 5 | Set-Content "$cbOut/environment.json"
