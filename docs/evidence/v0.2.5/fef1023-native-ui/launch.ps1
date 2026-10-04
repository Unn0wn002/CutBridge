$ErrorActionPreference = 'Stop'
$cbOut = 'C:\Evidence\verification-output'
$null = New-Item -ItemType Directory -Force "$cbOut/tmp", "$cbOut/pycache", "$cbOut/config", "$cbOut/data", "$cbOut/extensions"
try {
    if ($env:GH_TOKEN -or $env:GITHUB_TOKEN -or (Test-Path 'C:\Users\unn0w')) { throw 'Owner environment exposed' }
    $cbWritable = $false
    try { [IO.File]::WriteAllText('C:\Inputs\unexpected-write.txt', 'probe'); $cbWritable = $true } catch {}
    if ($cbWritable) { throw 'Input mapping is writable' }
    $cbTcp = [Net.Sockets.TcpClient]::new()
    try { $null = $cbTcp.ConnectAsync('1.1.1.1',443).Wait(1500); if ($cbTcp.Connected) { throw 'Network is accessible' } }
    catch { if ($cbTcp.Connected) { throw } } finally { $cbTcp.Dispose() }
    $env:TEMP = "$cbOut/tmp"; $env:TMP = $env:TEMP
    $env:PYTHONPYCACHEPREFIX = "$cbOut/pycache"
    $env:PYTHONIOENCODING = 'utf-8'
    $env:BLENDER_USER_CONFIG = "$cbOut/config"
    $env:BLENDER_USER_DATAFILES = "$cbOut/data"
    $env:BLENDER_USER_EXTENSIONS = "$cbOut/extensions"
    $env:PATH = 'C:\Inputs\runtime;' + $env:PATH
    $cbPython = Start-Process 'C:\Blender\5.2\python\bin\python.exe' -ArgumentList '--version' -WindowStyle Hidden -PassThru -Wait -RedirectStandardOutput "$cbOut/python-version.log" -RedirectStandardError "$cbOut/python-version-stderr.log"
    @{python_exit_code=$cbPython.ExitCode} | ConvertTo-Json | Set-Content "$cbOut/python-probe.json"
    $cbRepo = Start-Process 'C:\Blender\blender.exe' -ArgumentList '--command extension repo-add cutbridge_candidate --name CutBridgeCandidate --directory C:\Evidence\verification-output\extensions\candidate' -WindowStyle Hidden -PassThru -Wait -RedirectStandardOutput "$cbOut/repo-add.log" -RedirectStandardError "$cbOut/repo-add-stderr.log"
    if ($cbRepo.ExitCode -ne 0) { throw 'Extension repo-add failed' }
    $cbInstall = Start-Process 'C:\Blender\blender.exe' -ArgumentList '--command extension install-file -r cutbridge_candidate --enable C:\Inputs\CutBridge-Blender-v0.2.5.zip' -WindowStyle Hidden -PassThru -Wait -RedirectStandardOutput "$cbOut/install-file.log" -RedirectStandardError "$cbOut/install-file-stderr.log"
    if ($cbInstall.ExitCode -ne 0) { throw 'Extension install-file failed' }
    if (-not (Test-Path "$cbOut/extensions/candidate/cutbridge/__init__.py")) {
        Get-WinEvent -FilterHashtable @{LogName='Application';StartTime=(Get-Date).AddMinutes(-5)} -ErrorAction SilentlyContinue | Select-Object Id,ProviderName,Message | ConvertTo-Json | Set-Content "$cbOut/application-events.json"
        throw 'Extension installation produced no installed source; host dependency probe retained'
    }
    $cbProcess = Start-Process 'C:\Blender\blender.exe' -ArgumentList '--python-exit-code 1 --python C:\Inputs\native_blender.py' -WindowStyle Hidden -PassThru -Wait -RedirectStandardOutput "$cbOut/blender-stdout.log" -RedirectStandardError "$cbOut/blender-stderr.log"
    @{exit_code=$cbProcess.ExitCode;timestamp_utc=[DateTime]::UtcNow.ToString('o');method='Blender normal process exit; no force termination'} | ConvertTo-Json | Set-Content "$cbOut/process.json"
} catch {
    @{error=$_.Exception.Message;candidate_result='INSUFFICIENT EVIDENCE'} | ConvertTo-Json | Set-Content "$cbOut/launcher-error.json"
} finally { shutdown.exe /s /t 0 }
