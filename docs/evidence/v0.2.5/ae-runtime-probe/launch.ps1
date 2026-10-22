$ErrorActionPreference = 'Stop'
try {
    if ($env:GH_TOKEN -or $env:GITHUB_TOKEN -or (Test-Path 'C:\Users\unn0w')) { throw 'Owner environment exposed' }
    $cbWritable = $false
    try { [IO.File]::WriteAllText('C:\Inputs\unexpected-write.txt','probe'); $cbWritable = $true } catch {}
    if ($cbWritable) { throw 'Input mapping writable' }
    $cbTcp = [Net.Sockets.TcpClient]::new()
    try { $null = $cbTcp.ConnectAsync('1.1.1.1',443).Wait(1500); if ($cbTcp.Connected) { throw 'Network accessible' } }
    catch { if ($cbTcp.Connected) { throw } } finally { $cbTcp.Dispose() }
    $env:TEMP = 'C:\Evidence\tmp'; $env:TMP = $env:TEMP
    New-Item -ItemType Directory -Force $env:TEMP | Out-Null
    $env:PATH = 'C:\Inputs\runtime;' + $env:PATH
    $cbInfo = [Diagnostics.ProcessStartInfo]::new('C:\AfterEffects\AfterFX.com','-m -r C:\Inputs\probe.jsx')
    $cbInfo.UseShellExecute = $false; $cbInfo.CreateNoWindow = $true
    $cbInfo.RedirectStandardOutput = $true; $cbInfo.RedirectStandardError = $true
    $cbProcess = [Diagnostics.Process]::new(); $cbProcess.StartInfo = $cbInfo
    $null = $cbProcess.Start()
    $cbStdout = $cbProcess.StandardOutput.ReadToEndAsync(); $cbStderr = $cbProcess.StandardError.ReadToEndAsync()
    $cbExited = $cbProcess.WaitForExit(90000)
    if ($cbExited) { $cbStdout.Result | Set-Content 'C:\Evidence\stdout.log'; $cbStderr.Result | Set-Content 'C:\Evidence\stderr.log' }
    @{dependency_method='read-only Microsoft signed runtime DLLs';normal_exit=$cbExited;exit_code=$(if($cbExited){$cbProcess.ExitCode}else{$null});script_executed=(Test-Path 'C:\Evidence\ae-host.txt');timestamp_utc=[DateTime]::UtcNow.ToString('o');scope='AE availability only; no candidate runtime';license_files='NOT MAPPED';network='DISABLED';owner_environment='NOT EXPOSED'} | ConvertTo-Json | Set-Content 'C:\Evidence\probe.json'
    Get-WinEvent -FilterHashtable @{LogName='Application';StartTime=(Get-Date).AddMinutes(-5)} -ErrorAction SilentlyContinue | Select-Object Id,ProviderName,Message | ConvertTo-Json | Set-Content 'C:\Evidence\application-events.json'
} catch { @{error=$_.Exception.Message;verdict='INSUFFICIENT EVIDENCE'} | ConvertTo-Json | Set-Content 'C:\Evidence\error.json' }
finally { shutdown.exe /s /t 0 }
