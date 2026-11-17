# Runs inside Windows Sandbox (offline). Snapshot, deps, python, node, vcrt and this script are mapped READ-ONLY;
# only ...\qa\out is writable. Builds the v0.2.5 candidate ZIPs from the efa64cd snapshot twice, verifies them
# against the snapshot, then runs the repository's own checks. Adapted from the 2026-10-29 run5 kit.
$ErrorActionPreference = 'Continue'
$b = 'C:\Users\WDAGUtilityAccount\Desktop\qa'
$snap = "$b\snapshot"; $out = "$b\out"
New-Item -ItemType Directory -Force "$out\pycache" | Out-Null
$env:PYTHONPYCACHEPREFIX = "$out\pycache"
New-Item -ItemType Directory -Force C:\vtmp | Out-Null
$env:TEMP = "C:\vtmp"; $env:TMP = $env:TEMP; $env:TMPDIR = $env:TEMP
$env:PYTHONPATH = "$b\deps"
$py = "$b\py\python.exe"
$env:PATH = "$b\node;$env:PATH"
$log = "$out\run.log"
function Log($m){ $m | Tee-Object -FilePath $log -Append }
Log "start $(Get-Date -Format o)"
Log "network test (expect failure):"; try { Log ((Invoke-WebRequest https://github.com -UseBasicParsing -TimeoutSec 8).StatusCode) } catch { Log "no network: $($_.Exception.Message)" }
Log "python: $(& $py -I -c 'import sys,zlib;print(sys.version.split()[0], zlib.ZLIB_RUNTIME_VERSION)')"
Log "whoami: $(whoami)"
Log "node: $(& node --version 2>&1)"
Log "vcrt copy: $((Get-ChildItem "$b\vcrt" -Filter *.dll | ForEach-Object { Copy-Item $_.FullName "$env:WINDIR\System32\" -Force -ErrorAction Continue; $_.Name }) -join ',')"
function Manifest($path){ Get-ChildItem $path -Recurse -File -Force | Sort-Object FullName | ForEach-Object { '{0}  {1}' -f (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower(), $_.FullName.Substring($path.Length) } }
Manifest $snap | Set-Content "$out\manifest-before-in-sandbox.txt"
Set-Location $snap
$steps = @(
 @{n='build-dist';        a=@('tools/build_release.py','--tag','v0.2.5','--output',"$out\dist")},
 @{n='build-dist-repeat'; a=@('tools/build_release.py','--tag','v0.2.5','--output',"$out\dist-repeat")},
 @{n='verify-package-zips'; a=@('tools/verify_package.py','--tag','v0.2.5','--source-dir',$snap,'--blender-zip',"$out\dist\CutBridge-Blender-v0.2.5.zip",'--ae-zip',"$out\dist\CutBridge-AfterEffects-v0.2.5.zip",'--output',"$out\verify-package.json")},
 @{n='compileall'; a=@('-m','compileall','-q','apps','tools','tests')},
 @{n='pytest';     a=@('-m','pytest','-q','-p','no:cacheprovider')},
 @{n='blender-runtime-52'; a=@('tests/test_blender_runtime_52.py')}
)
foreach($s in $steps){ Log "=== $($s.n) ==="; & $py @($s.a) *>&1 | Tee-Object -FilePath "$out\$($s.n).txt" | Select-Object -Last 30 | ForEach-Object { Log $_ }; Log "exit=$LASTEXITCODE" }
Log "=== repeat-build comparison ==="
$a = Get-ChildItem "$out\dist" -File | Sort-Object Name; $r = Get-ChildItem "$out\dist-repeat" -File | Sort-Object Name
Log "names identical: $((($a.Name) -join ',') -eq (($r.Name) -join ','))"
foreach($f in $a){ $other = Join-Path "$out\dist-repeat" $f.Name; Log ("{0} {1} repeat-identical={2}" -f (Get-FileHash $f.FullName).Hash.ToLower(), $f.Name, ((Test-Path $other) -and ((Get-FileHash $f.FullName).Hash -eq (Get-FileHash $other).Hash))) }
Set-Location $b
Manifest $snap | Set-Content "$out\manifest-after-in-sandbox.txt"
$same = (Get-FileHash "$out\manifest-before-in-sandbox.txt").Hash -eq (Get-FileHash "$out\manifest-after-in-sandbox.txt").Hash
Log "snapshot manifest identical before/after: $same"
Log "done $(Get-Date -Format o)"
'DONE' | Set-Content "$out\DONE.flag"
