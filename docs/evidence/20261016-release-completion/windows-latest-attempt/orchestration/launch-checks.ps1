$ErrorActionPreference = 'Stop'
$cbOut = 'C:\Evidence\verification-output'
$cbChecks = @()
try {
    $null = New-Item -ItemType Directory -Force "$cbOut\tmp", "$cbOut\pycache", "$cbOut\config", "$cbOut\data", "$cbOut\extensions"
    $null=New-Item -ItemType Directory -Force C:\LocalVerification\verification-output\tmp; $env:TEMP = "C:\LocalVerification\verification-output\tmp"; $env:TMP = $env:TEMP; $env:TMPDIR = $env:TEMP
    $env:PYTHONPYCACHEPREFIX = "$cbOut\pycache"
    $env:PYTHONPATH = 'C:\Deps'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
    $env:BLENDER_USER_CONFIG = "$cbOut\config"
    $env:BLENDER_USER_DATAFILES = "$cbOut\data"
    $env:BLENDER_USER_EXTENSIONS = "$cbOut\extensions"
    $env:PATH = 'C:\Runtime;C:\Node;C:\Python;' + $env:PATH
    Set-Location C:\Orchestration
    $cbAdapters = @(Get-NetAdapter -IncludeHidden -ErrorAction SilentlyContinue | Select-Object Name,Status,InterfaceDescription)
    $cbWritable = $false
    try { [IO.File]::WriteAllText('C:\Candidate\unexpected-write.txt','probe'); $cbWritable = $true } catch {}
    $cbCredentialNames = @(Get-ChildItem Env: | Where-Object Name -match '^(GH_TOKEN|GITHUB_TOKEN|SSH_AUTH_SOCK|ACTIONS_RUNTIME_TOKEN|AWS_.*|AZURE_.*)$' | ForEach-Object Name)
    @{timestamp_utc=[DateTime]::UtcNow.ToString('o');os=[Environment]::OSVersion.VersionString;identity=[Security.Principal.WindowsIdentity]::GetCurrent().Name;adapters=$cbAdapters;source_writable=$cbWritable;owner_home_visible=(Test-Path C:\Users\unn0w);credential_environment_names=$cbCredentialNames;source_git_visible=(Test-Path C:\Candidate\.git);TMPDIR=$env:TMPDIR;PYTHONPYCACHEPREFIX=$env:PYTHONPYCACHEPREFIX} | ConvertTo-Json -Depth 6 | Set-Content "$cbOut\isolation.json"
    if ($cbWritable -or (Test-Path C:\Users\unn0w) -or $cbCredentialNames.Count -or @($cbAdapters | Where-Object Status -eq 'Up').Count) { throw 'Isolation preflight failed' }
    $cbPreflight = Start-Process C:\Python\python.exe -ArgumentList '-c "import sys,pytest,jsonschema,bpy; print(sys.version); print(bpy.app.version_string); assert bpy.app.version == (5,2,1)"' -WindowStyle Hidden -PassThru -Wait -RedirectStandardOutput "$cbOut\dependency-preflight.log" -RedirectStandardError "$cbOut\dependency-preflight-stderr.log"
    if ($cbPreflight.ExitCode -ne 0) { throw "Required Python/Blender dependency preflight failed: $($cbPreflight.ExitCode)" }
    & C:\Node\node.exe --version
    if ($LASTEXITCODE -ne 0) { throw 'Node dependency preflight failed' }
    function Invoke-CBCheck([string]$name,[string]$exe,[string[]]$arguments) {
        "CHECK $name" | Tee-Object -FilePath "$cbOut\checks.log" -Append
        & $exe @arguments 2>&1 | Tee-Object -FilePath "$cbOut\checks.log" -Append
        $cbCode = $LASTEXITCODE
        $script:cbChecks += @{name=$name;exit_code=$cbCode}
        $script:cbChecks | ConvertTo-Json -Depth 5 | Set-Content "$cbOut\check-results.json"
    }
    Set-Location C:\Candidate
    Invoke-CBCheck 'compileall' 'C:\Python\python.exe' @('-m','compileall','-q','apps','tools','tests')
    Invoke-CBCheck 'pytest-full' 'C:\Python\python.exe' @('-m','pytest','-q','-p','no:cacheprovider',"--junitxml=$cbOut\pytest.xml")
    Invoke-CBCheck 'blender-rna-5.2.1' 'C:\Python\python.exe' @('tests/test_blender_runtime_52.py')
    foreach ($cbFile in @('CutBridge.jsx','revision_manager.js','qc_plus.js','localization.js')) {
        $cbName = if ($cbFile -eq 'CutBridge.jsx') { 'CutBridge.js' } else { $cbFile }
        Copy-Item -LiteralPath "apps/after-effects/$cbFile" -Destination "$cbOut\tmp\$cbName"
        Invoke-CBCheck "syntax-$cbFile" 'C:\Node\node.exe' @('--check',"$cbOut\tmp\$cbName")
    }
    foreach ($cbTest in Get-ChildItem tests -Filter 'ae*.cjs' | Sort-Object Name) {
        Invoke-CBCheck $cbTest.Name 'C:\Node\node.exe' @($cbTest.FullName)
    }
    $cbVersion = & C:\Python\python.exe C:\Orchestration\version_lookup.py
    if ($LASTEXITCODE -ne 0) { throw 'Version resolution failed' }
    Invoke-CBCheck 'package-first' 'C:\Python\python.exe' @('tools/build_release.py','--tag',"v$cbVersion",'--output',"$cbOut\dist-ci")
    Invoke-CBCheck 'package-repeat' 'C:\Python\python.exe' @('tools/build_release.py','--tag',"v$cbVersion",'--output',"$cbOut\dist-repeat")
    Invoke-CBCheck 'artifact-inspection' 'C:\Python\python.exe' @('C:\Orchestration\inspect_packages.py',$cbOut,$cbVersion)
    Invoke-CBCheck 'distribution-preview' 'C:\Python\python.exe' @('C:\Orchestration\distribution_preview.py')
    if (@($cbChecks | Where-Object exit_code -ne 0).Count) { 'FAIL' | Set-Content "$cbOut\verdict.txt" } else { 'PASS' | Set-Content "$cbOut\verdict.txt" }
} catch {
    $_ | Out-String | Set-Content "$cbOut\infrastructure-error.txt"
    'INSUFFICIENT EVIDENCE' | Set-Content "$cbOut\verdict.txt"
} finally {
    [DateTime]::UtcNow.ToString('o') | Set-Content "$cbOut\completed-utc.txt"
    shutdown.exe /s /t 0
}
