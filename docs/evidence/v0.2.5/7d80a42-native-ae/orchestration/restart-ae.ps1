$ErrorActionPreference='Stop'
if(Get-Process AfterFX -ErrorAction SilentlyContinue){throw 'AE process must be closed'}
if(@(Get-NetAdapter | Where-Object Status -eq 'Up').Count){throw 'Network enabled'}
$env:TEMP='C:\CutBridgeEvidence\r2\tmp';$env:TMP=$env:TEMP;$env:TMPDIR=$env:TEMP
$cbP=Start-Process -FilePath 'C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe' -WindowStyle Hidden -PassThru
@{pid=$cbP.Id;started=(Get-Date).ToUniversalTime().ToString('o');temp=$env:TEMP} | ConvertTo-Json | Set-Content 'C:\CutBridgeEvidence\r2\process-restart.json'
