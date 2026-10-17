$ErrorActionPreference='Stop'
$cbOut='C:\Evidence\verification-output'
$cbStart=[DateTime]::UtcNow
$cbResults=@()
$cbExpired=$false
function Save-ControlRecord { $script:cbResults|ConvertTo-Json -Depth 8|Set-Content -Encoding UTF8 "$cbOut\process-controls.json" }
function Invoke-Control([string]$name,[string]$exe,[string]$arguments,[int]$seconds,[bool]$visual=$false) {
    $cbAt=[DateTime]::UtcNow.ToString('o')
    $cbParams=@{FilePath=$exe;PassThru=$true;RedirectStandardOutput="$cbOut\$name-stdout.log";RedirectStandardError="$cbOut\$name-stderr.log";WorkingDirectory=(Split-Path -Parent $exe)}
    if($arguments){$cbParams.ArgumentList=$arguments}
    if($visual){$cbParams.WindowStyle='Normal'}else{$cbParams.WindowStyle='Hidden'}
    $cbProcess=Start-Process @cbParams
    $null=$cbProcess.Handle
    $cbRecord=@{name=$name;exe=$exe;arguments=$arguments;pid=$cbProcess.Id;started_utc=$cbAt;visual=$visual;candidate_code='NOT_MAPPED / NOT_EXECUTED';state='STARTED'}
    $script:cbResults+=$cbRecord; Save-ControlRecord
    $cbDeadline=[DateTime]::UtcNow.AddSeconds($seconds)
    do {
        $cbProcess.Refresh()
        $cbRecord.exited=$cbProcess.HasExited
        if($cbProcess.HasExited){$cbRecord.exit_code=$cbProcess.ExitCode;$cbRecord.state='EXITED';break}
        $cbRecord.window_title=$cbProcess.MainWindowTitle
        $cbRecord.state='RUNNING_REQUIRES_INDEPENDENT_VISUAL_OBSERVATION'
        Save-ControlRecord
        Start-Sleep -Seconds 2
    } while([DateTime]::UtcNow-lt$cbDeadline)
    $cbRecord.finished_utc=[DateTime]::UtcNow.ToString('o');Save-ControlRecord
    if(-not$cbProcess.HasExited){$script:cbExpired=$true;throw "Control $name remains running; no next host will launch and no normal exit is inferred"}
    return $cbProcess.ExitCode
}
try {
    $null=New-Item -ItemType Directory -Force "$cbOut\tmp","$cbOut\pycache","$cbOut\config","$cbOut\data","$cbOut\extensions"
    $env:TEMP="$cbOut\tmp";$env:TMP=$env:TEMP;$env:TMPDIR=$env:TEMP;$env:PYTHONPYCACHEPREFIX="$cbOut\pycache"
    $env:BLENDER_USER_CONFIG="$cbOut\config";$env:BLENDER_USER_DATAFILES="$cbOut\data";$env:BLENDER_USER_EXTENSIONS="$cbOut\extensions"
    $env:PATH='C:\Runtime;'+$env:PATH
    $cbAdapters=@(Get-NetAdapter -IncludeHidden -ErrorAction SilentlyContinue|Select-Object Name,Status,InterfaceDescription)
    $cbCreds=@(Get-ChildItem Env:|Where-Object Name -match 'TOKEN|SECRET|PASSWORD|CREDENTIAL|SSH_AUTH|AWS_|AZURE_|GOOGLE_|GITHUB_|GH_'|ForEach-Object Name)
    $cbRO=@{}
    foreach($cbPath in @('C:\Orchestration','C:\Runtime','C:\ControlBinary','C:\Blender','C:\AfterEffects')) {
        $cbWritable=$false;try{[IO.File]::WriteAllText("$cbPath\unexpected-write.txt",'probe');$cbWritable=$true}catch{}
        $cbRO[$cbPath]=(-not$cbWritable)
    }
    $cbNoCandidate=(-not(Test-Path C:\Candidate))-and(-not(Test-Path C:\AERuntime))-and(-not(Test-Path C:\Packages))-and(-not(Test-Path C:\Artifacts))
    $cbIsolation=@{started_utc=$cbStart.ToString('o');os=[Environment]::OSVersion.VersionString;identity=[Security.Principal.WindowsIdentity]::GetCurrent().Name;adapters=$cbAdapters;credential_environment_names=$cbCreds;owner_home_visible=(Test-Path C:\Users\unn0w);read_only_probes=$cbRO;candidate_paths_absent=$cbNoCandidate;TEMP=$env:TEMP;TMP=$env:TMP;TMPDIR=$env:TMPDIR;PYTHONPYCACHEPREFIX=$env:PYTHONPYCACHEPREFIX;vGPU='Enable per retained policy';policy_changes='NONE';execution_policy_override='NONE'}
    $cbIsolation|ConvertTo-Json -Depth 7|Set-Content -Encoding UTF8 "$cbOut\isolation.json"
    Get-ExecutionPolicy -List|ConvertTo-Json|Set-Content -Encoding UTF8 "$cbOut\execution-policies.json"
    if((Test-Path C:\Users\unn0w)-or$cbCreds.Count-or@($cbAdapters|Where-Object Status -eq 'Up').Count-or@($cbRO.Values|Where-Object {-not$_}).Count-or-not$cbNoCandidate){throw 'Independent isolation preflight failed'}
    $cbLocal=Invoke-Control 'os-native-where' 'C:\Windows\System32\where.exe' '/?' 20
    $cbMapped=Invoke-Control 'mapped-signed-where' 'C:\ControlBinary\where.exe' '/?' 20
    $cbBlender=Invoke-Control 'blender-vendor-version' 'C:\Blender\blender.exe' '--version' 30
    if($cbBlender-eq0){$null=Invoke-Control 'blender-blank-gui' 'C:\Blender\blender.exe' '--factory-startup --disable-autoexec' 150 $true}
    else{@{status='NOT_EXECUTED';reason='Vendor --version control did not initialize; no redundant GUI retry';precheck_exit=$cbBlender}|ConvertTo-Json|Set-Content -Encoding UTF8 "$cbOut\blender-visual-gate.json"}
    $null=Invoke-Control 'ae-blank-gui' 'C:\AfterEffects\AfterFX.exe' '-m' 180 $true
    @{verdict='INSUFFICIENT EVIDENCE';reason='Control run only. Visual/API availability requires actual independent observations; candidate not mapped.';candidate_execution='NOT_EXECUTED';candidate_scope='NONE';normal_exit_only_from_process_records=$true}|ConvertTo-Json|Set-Content -Encoding UTF8 "$cbOut\assessment.json"
}catch{
    $_|Out-String|Set-Content -Encoding UTF8 "$cbOut\orchestration-error.txt"
    @{verdict='INSUFFICIENT EVIDENCE';reason='See exact control/launcher logs; no inferred product failure or root cause';candidate_execution='NOT_EXECUTED';timeout=$cbExpired}|ConvertTo-Json|Set-Content -Encoding UTF8 "$cbOut\assessment.json"
}finally{
    foreach($cbLog in @('Application','Microsoft-Windows-CodeIntegrity/Operational','Microsoft-Windows-AppLocker/EXE and DLL')){
        $cbName=$cbLog.Replace('/','-').Replace(' ','_')
        try{Get-WinEvent -FilterHashtable @{LogName=$cbLog;StartTime=$cbStart.AddSeconds(-10)} -ErrorAction Stop|ForEach-Object{@{time_utc=$_.TimeCreated.ToUniversalTime().ToString('o');id=$_.Id;provider=$_.ProviderName;process_id=$_.ProcessId;message=$_.Message;xml=$_.ToXml()}}|ConvertTo-Json -Depth 7|Set-Content -Encoding UTF8 "$cbOut\events-$cbName.json"}catch{$_|Out-String|Set-Content -Encoding UTF8 "$cbOut\events-$cbName-unavailable.txt"}
    }
    [DateTime]::UtcNow.ToString('o')|Set-Content -Encoding UTF8 "$cbOut\completed-utc.txt"
    shutdown.exe /s /t 0
}
