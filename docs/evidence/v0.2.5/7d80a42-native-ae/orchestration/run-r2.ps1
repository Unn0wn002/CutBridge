$ErrorActionPreference='Stop'
$cbOut='C:\CutBridgeEvidence\r2'
$env:TEMP="$cbOut\tmp"; $env:TMP=$env:TEMP; $env:TMPDIR=$env:TEMP
if(Get-Process AfterFX -ErrorAction SilentlyContinue){throw 'AE process must be closed for controlled TEMP inheritance'}
if(@(Get-NetAdapter | Where-Object Status -eq 'Up').Count){throw 'Network must remain disabled'}
$cbWritable=$false;try{[IO.File]::WriteAllText('C:\CutBridgeInputsR2\write-boundary-probe.txt','probe');$cbWritable=$true}catch{}
if($cbWritable -or !(Test-Path 'C:\CutBridgeInputsR2\stage1.jsx')){throw 'Snapshot boundary invalid'}
@{temp=$env:TEMP;input_writable=$cbWritable;network_adapters_up=0;owner_home_visible=(Test-Path 'C:\Users\unn0w');credential_environment_present=[bool]($env:GH_TOKEN -or $env:GITHUB_TOKEN -or $env:AWS_SECRET_ACCESS_KEY)} | ConvertTo-Json | Set-Content "$cbOut\boundary.json"
$cbProc=Start-Process -FilePath 'C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe' -ArgumentList '-r','C:\CutBridgeInputsR2\stage1.jsx' -WindowStyle Hidden -PassThru
@{pid=$cbProc.Id;started=(Get-Date).ToUniversalTime().ToString('o');arguments='-r C:\CutBridgeInputsR2\stage1.jsx'} | ConvertTo-Json | Set-Content "$cbOut\process-start.json"
