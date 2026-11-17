$ErrorActionPreference='Stop'
$cbOutput='C:\CutBridgeEvidence'
New-Item -ItemType Directory -Force "$cbOutput\tmp" | Out-Null
$env:TEMP="$cbOutput\tmp"; $env:TMP=$env:TEMP; $env:TMPDIR=$env:TEMP
$cbAdapters=@(Get-NetAdapter | Where-Object Status -eq 'Up'); $cbAdapters.Name | ConvertTo-Json | Set-Content "$cbOutput\network-before.json"
$cbAdapters | Disable-NetAdapter -Confirm:$false
$cbWritable=$false; try{[IO.File]::WriteAllText('C:\CutBridgeInputs\write-boundary-probe.txt','probe');$cbWritable=$true}catch{}
$cbClient=New-Object Net.Sockets.TcpClient
$cbConnected=$false;try{$cbTask=$cbClient.ConnectAsync('1.1.1.1',443);if($cbTask.Wait(2000)){$cbConnected=$cbClient.Connected}}catch{}finally{$cbClient.Dispose()}
$cbBoundary=@{owner_home_visible=(Test-Path 'C:\Users\unn0w');credential_environment_present=[bool]($env:GH_TOKEN -or $env:GITHUB_TOKEN -or $env:AWS_SECRET_ACCESS_KEY);input_writable=$cbWritable;network_connected=$cbConnected;active_adapters=@(Get-NetAdapter | Where-Object Status -eq 'Up' | Select-Object Name,Status);temp=$env:TEMP}
$cbBoundary | ConvertTo-Json -Depth 5 | Set-Content "$cbOutput\boundary.json"
if($cbBoundary.owner_home_visible -or $cbBoundary.credential_environment_present -or $cbWritable -or $cbConnected -or $cbBoundary.active_adapters.Count){throw 'Isolation boundary rejected'}
Start-Process -FilePath 'C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe' -ArgumentList '-r','C:\CutBridgeInputs\stage1.jsx' -WindowStyle Hidden
