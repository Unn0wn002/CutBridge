$ErrorActionPreference='Stop'
$cbExe='C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe'
$cbInfo=(Get-Item -LiteralPath $cbExe).VersionInfo
$cbInfo | Select-Object ProductVersion,FileVersion | ConvertTo-Json | Set-Content 'C:\CutBridgeEvidence\ae-installed-version.json'
Start-Process -FilePath $cbExe -WindowStyle Hidden
