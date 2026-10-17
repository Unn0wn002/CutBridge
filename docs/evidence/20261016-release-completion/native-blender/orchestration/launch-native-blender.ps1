$ErrorActionPreference='Stop'
$cbOut='C:\Evidence\verification-output'
$cbProcesses=@()
try {
    $null=New-Item -ItemType Directory -Force "$cbOut\tmp","$cbOut\pycache","$cbOut\config","$cbOut\data","$cbOut\extensions","$cbOut\native-blender\repository"
    $env:TEMP="$cbOut\tmp"; $env:TMP=$env:TEMP; $env:TMPDIR=$env:TEMP
    $env:PYTHONPYCACHEPREFIX="$cbOut\pycache"
    $env:PYTHONIOENCODING='utf-8'
    $env:BLENDER_USER_CONFIG="$cbOut\config"
    $env:BLENDER_USER_DATAFILES="$cbOut\data"
    $env:BLENDER_USER_EXTENSIONS="$cbOut\extensions"
    $env:CUTBRIDGE_BLENDER_ZIP='C:\Artifacts\CutBridge-Blender-v0.2.5.zip'
    $env:PATH='C:\Runtime;'+$env:PATH
    $cbAdapters=@(Get-NetAdapter -IncludeHidden -ErrorAction SilentlyContinue | Select-Object Name,Status,InterfaceDescription)
    $cbCredentials=@(Get-ChildItem Env: | Where-Object Name -match '^(GH_TOKEN|GITHUB_TOKEN|SSH_AUTH_SOCK|ACTIONS_RUNTIME_TOKEN|AWS_.*|AZURE_.*)$' | ForEach-Object Name)
    $cbWritable=$false
    try{[IO.File]::WriteAllText('C:\Artifacts\unexpected-write.txt','probe');$cbWritable=$true}catch{}
    @{adapters=$cbAdapters;owner_home_visible=(Test-Path C:\Users\unn0w);credential_environment_names=$cbCredentials;artifact_inputs_writable=$cbWritable;timestamp_utc=[DateTime]::UtcNow.ToString('o');TMPDIR=$env:TMPDIR;PYTHONPYCACHEPREFIX=$env:PYTHONPYCACHEPREFIX;os=[Environment]::OSVersion.VersionString;vGPU='Enabled for native GUI; networking disabled by retained configuration'} | ConvertTo-Json -Depth 6 | Set-Content "$cbOut\isolation.json"
    if($cbWritable -or (Test-Path C:\Users\unn0w) -or $cbCredentials.Count -or @($cbAdapters | Where-Object Status -eq 'Up').Count){throw 'Isolation preflight failed'}
    function Invoke-CBNative([string]$name,[string]$arguments,[int]$seconds=120){
        $cbStarted=[DateTime]::UtcNow.ToString('o')
        $cbProcess=Start-Process C:\Blender\blender.exe -ArgumentList $arguments -WindowStyle Hidden -PassThru -RedirectStandardOutput "$cbOut\$name-stdout.log" -RedirectStandardError "$cbOut\$name-stderr.log"
        $null=$cbProcess.Handle
        $cbExited=$cbProcess.WaitForExit($seconds*1000)
        $cbProcess.Refresh()
        $script:cbProcesses+=@{name=$name;pid=$cbProcess.Id;started_utc=$cbStarted;exited=$cbExited;exit_code=$(if($cbExited){$cbProcess.ExitCode}else{$null});finished_utc=[DateTime]::UtcNow.ToString('o');command_arguments=$arguments;method='Normal application process exit; no force termination'}
        $script:cbProcesses | ConvertTo-Json -Depth 6 | Set-Content "$cbOut\native-processes.json"
        if(-not $cbExited){throw "Native process unavailable/timed out: $name"}
        if($cbProcess.ExitCode -ne 0){throw "Native process nonzero exit: $name ($($cbProcess.ExitCode)); inspect logs before classifying candidate behavior"}
    }
    Invoke-CBNative 'official-package-validator' '--command extension validate C:\Artifacts\CutBridge-Blender-v0.2.5.zip'
    Copy-Item -LiteralPath $env:CUTBRIDGE_BLENDER_ZIP -Destination "$cbOut\native-blender\repository"
    Invoke-CBNative 'official-repository-generator' '--command extension server-generate --repo-dir C:\Evidence\verification-output\native-blender\repository'
    Invoke-CBNative 'extension-repo-add' '--command extension repo-add cutbridge_candidate --name CutBridgeCandidate --directory C:\Evidence\verification-output\extensions\candidate'
    Invoke-CBNative 'extension-install-enable' '--command extension install-file -r cutbridge_candidate --enable C:\Artifacts\CutBridge-Blender-v0.2.5.zip'
    if(-not(Test-Path "$cbOut\extensions\candidate\cutbridge\__init__.py")){throw 'Official extension installation produced no installed source'}
    Invoke-CBNative 'native-blender-campaign' '--python-exit-code 1 --python C:\NativeBlenderInput\native_blender.py' 600
    $cbReport=Get-Content -Raw -LiteralPath "$cbOut\native-blender\native-blender.json" | ConvertFrom-Json
    if($cbReport.overall_scope_result -ne 'PASS'){throw "Native Blender campaign incomplete: $($cbReport.overall_scope_result); inspect native report"}
    Get-FileHash -LiteralPath "$cbOut\native-blender\native-blender.json","$cbOut\native-blender\fixtures\reopen-V003.blend" -Algorithm SHA256 | Select-Object Path,Hash | ConvertTo-Json | Set-Content "$cbOut\before-fresh-process-inputs.json"
    Invoke-CBNative 'native-blender-fresh-reopen' '--python-exit-code 1 --python C:\NativeBlenderInput\reopen_blender.py' 180
    Get-FileHash -LiteralPath "$cbOut\native-blender\native-blender.json","$cbOut\native-blender\fixtures\reopen-V003.blend" -Algorithm SHA256 | Select-Object Path,Hash | ConvertTo-Json | Set-Content "$cbOut\after-fresh-process-inputs.json"
    $cbReopened=Get-Content -Raw -LiteralPath "$cbOut\native-blender\reopen-blender.json" | ConvertFrom-Json
    if($cbReopened.overall_scope_result -ne 'PASS'){throw 'Fresh process reopen did not pass; inspect report'}
    'PASS' | Set-Content "$cbOut\verdict.txt"
}catch{$_ | Out-String | Set-Content "$cbOut\infrastructure-or-harness-error.txt"; 'INSUFFICIENT EVIDENCE' | Set-Content "$cbOut\verdict.txt"}
finally{[DateTime]::UtcNow.ToString('o') | Set-Content "$cbOut\completed-utc.txt";shutdown.exe /s /t 0}
