if(@(Get-NetAdapter | Where-Object Status -eq 'Up').Count){throw 'Network enabled'}
Start-Process -FilePath 'C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe' -ArgumentList '-r','C:\CutBridgeFault\capture.jsx' -WindowStyle Hidden
