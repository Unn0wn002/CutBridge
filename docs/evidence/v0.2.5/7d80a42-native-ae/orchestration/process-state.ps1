Get-Process AfterFX -ErrorAction SilentlyContinue | Select-Object Id,Responding,MainWindowTitle,CPU | ConvertTo-Json | Set-Content 'C:\CutBridgeEvidence\r2\ae-process-state.json'
