$ErrorActionPreference='Stop'
$cbOut='C:\Evidence\verification-output'
try {
    $null=New-Item -ItemType Directory -Force "$cbOut\tmp","$cbOut\pycache","$cbOut\native-ae"
    $env:TEMP="$cbOut\tmp";$env:TMP=$env:TEMP;$env:TMPDIR=$env:TEMP
    $env:PYTHONPYCACHEPREFIX="$cbOut\pycache"
    $env:PATH='C:\Runtime;'+$env:PATH
    $cbAdapters=@(Get-NetAdapter -IncludeHidden -ErrorAction SilentlyContinue|Select-Object Name,Status,InterfaceDescription)
    $cbCredentials=@(Get-ChildItem Env:|Where-Object Name -match '^(GH_TOKEN|GITHUB_TOKEN|SSH_AUTH_SOCK|ACTIONS_RUNTIME_TOKEN|AWS_.*|AZURE_.*)$'|ForEach-Object Name)
    $cbWritable=$false;try{[IO.File]::WriteAllText('C:\NativeAEInput\unexpected-write.txt','probe');$cbWritable=$true}catch{}
    @{adapters=$cbAdapters;owner_home_visible=(Test-Path C:\Users\unn0w);credential_environment_names=$cbCredentials;inputs_writable=$cbWritable;timestamp_utc=[DateTime]::UtcNow.ToString('o');TMPDIR=$env:TMPDIR;os=[Environment]::OSVersion.VersionString;vGPU='Enabled for native GUI; network disabled by retained policy'}|ConvertTo-Json -Depth 6|Set-Content "$cbOut\isolation.json"
    if($cbWritable -or(Test-Path C:\Users\unn0w)-or$cbCredentials.Count-or@($cbAdapters|Where-Object Status -eq 'Up').Count){throw 'Isolation preflight failed'}
    $cbProcess=Start-Process C:\AfterEffects\AfterFX.com -ArgumentList '-m -r C:\NativeAEInput\run_all.jsx' -WindowStyle Hidden -PassThru -RedirectStandardOutput "$cbOut\after-effects-stdout.log" -RedirectStandardError "$cbOut\after-effects-stderr.log"
    $null=$cbProcess.Handle
    $cbNative=$null
    $cbDeadline=[DateTime]::UtcNow.AddSeconds(600)
    $cbStatus=$null
    while([DateTime]::UtcNow-lt$cbDeadline){
        if(-not$cbNative){$cbNative=Get-Process AfterFX -ErrorAction SilentlyContinue|Select-Object -First 1;if($cbNative){$null=$cbNative.Handle;@{id=$cbNative.Id;started=$cbNative.StartTime.ToUniversalTime().ToString('o')}|ConvertTo-Json|Set-Content "$cbOut\native-process-start.json"}}
        if(Test-Path "$cbOut\native-ae\all-status.json"){try{$cbStatus=Get-Content -Raw -LiteralPath "$cbOut\native-ae\all-status.json"|ConvertFrom-Json;if($cbStatus.status-ne'IN_PROGRESS'){break}}catch{}}
        $cbProcess.Refresh();if($cbNative){$cbNative.Refresh();if($cbNative.HasExited){break}};Start-Sleep -Seconds 3
    }
    if($cbStatus-and$cbStatus.status-ne'IN_PROGRESS'){$cbExited=$cbProcess.WaitForExit(60000);$cbProcess.Refresh()}else{$cbExited=$cbProcess.HasExited}
    @{pid=$cbProcess.Id;script_result=$(if($cbStatus){$cbStatus.status}else{'NOT_EXECUTED'});launcher_exited=$cbExited;exit_code=$(if($cbExited){$cbProcess.ExitCode}else{$null});normal_ae_exit='Requires native process/quit record; .com launch exit alone is insufficient';timestamp_utc=[DateTime]::UtcNow.ToString('o');scope='Scripted native exact-package tests; no S14B or visual installer sign-off'}|ConvertTo-Json|Set-Content "$cbOut\process.json"
    Get-Process AfterFX -ErrorAction SilentlyContinue|Select-Object Id,StartTime,ProcessName|ConvertTo-Json|Set-Content "$cbOut\remaining-ae-processes.json"
    if($cbNative){$cbNativeExited=$cbNative.WaitForExit(60000);$cbNative.Refresh();@{pid=$cbNative.Id;exited=$cbNativeExited;exit_code=$(if($cbNativeExited){$cbNative.ExitCode}else{$null});method='Observed actual AfterFX.exe; no force termination'}|ConvertTo-Json|Set-Content "$cbOut\native-process-exit.json"}
    if($cbNativeExited-and$cbStatus-and(Test-Path "$cbOut\native-ae\artist-V003.aep")){
        if(Test-Path "$cbOut\native-ae\reopen.json"){Copy-Item -LiteralPath "$cbOut\native-ae\reopen.json" -Destination "$cbOut\native-ae\same-process-reopen.json"}
        $cbFresh=Start-Process C:\AfterEffects\AfterFX.com -ArgumentList '-m -r C:\NativeAEInput\fresh_reopen.jsx' -WindowStyle Hidden -PassThru -RedirectStandardOutput "$cbOut\fresh-stdout.log" -RedirectStandardError "$cbOut\fresh-stderr.log";$null=$cbFresh.Handle
        $cbFreshDeadline=[DateTime]::UtcNow.AddSeconds(300);$cbFreshNative=$null
        while([DateTime]::UtcNow-lt$cbFreshDeadline-and-not(Test-Path "$cbOut\native-ae\fresh-process-reopen.json")){if(-not$cbFreshNative){$cbFreshNative=Get-Process AfterFX -ErrorAction SilentlyContinue|Select-Object -First 1;if($cbFreshNative){$null=$cbFreshNative.Handle}};Start-Sleep -Seconds 3}
        if($cbFreshNative){$cbFreshExited=$cbFreshNative.WaitForExit(60000);$cbFreshNative.Refresh();@{pid=$cbFreshNative.Id;previous_pid=$cbNative.Id;distinct_process=($cbFreshNative.Id-ne$cbNative.Id);exited=$cbFreshExited;exit_code=$(if($cbFreshExited){$cbFreshNative.ExitCode}else{$null});method='Actual fresh AfterFX.exe; no force termination'}|ConvertTo-Json|Set-Content "$cbOut\fresh-native-process-exit.json"}
    }
    if(-not$cbStatus-or$cbStatus.status-eq'IN_PROGRESS'){'INSUFFICIENT EVIDENCE'|Set-Content "$cbOut\verdict.txt"}else{$cbStatus.status|Set-Content "$cbOut\verdict.txt"}
}catch{$_|Out-String|Set-Content "$cbOut\infrastructure-error.txt";'INSUFFICIENT EVIDENCE'|Set-Content "$cbOut\verdict.txt"}
finally{[DateTime]::UtcNow.ToString('o')|Set-Content "$cbOut\completed-utc.txt";shutdown.exe /s /t 0}
