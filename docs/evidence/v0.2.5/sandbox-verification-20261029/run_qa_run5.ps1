# Runs inside Windows Sandbox. Snapshot, deps, python are mapped READ-ONLY; only C:\qa\out is writable.
$ErrorActionPreference = 'Continue'
$b = 'C:\Users\WDAGUtilityAccount\Desktop\qa'
$snap = "$b\snapshot"; $out = "$b\out"
New-Item -ItemType Directory -Force "$out\pycache","$out\tmp","$out\work" | Out-Null
$env:PYTHONPYCACHEPREFIX = "$out\pycache"
# run 4: temp area on the Sandbox's own disposable disk (mapped folders may not support symlinks); still outside the read-only snapshot
New-Item -ItemType Directory -Force C:\vtmp | Out-Null
$env:TEMP = "C:\vtmp"; $env:TMP = $env:TEMP; $env:TMPDIR = $env:TEMP
$env:PYTHONPATH = "$b\deps"; $env:PYTHONDONTWRITEBYTECODE = ''
$py = "$b\py\python.exe"
# run 3: Node (mapped read-only) for the AE-side .cjs checks the tests invoke
$env:PATH = "$b\node;$env:PATH"
$log = "$out\run.log"
function Log($m){ $m | Tee-Object -FilePath $log -Append }
Log "start $(Get-Date -Format o)"
Log "network test (expect failure):"; try { Log ((Invoke-WebRequest https://github.com -UseBasicParsing -TimeoutSec 8).StatusCode) } catch { Log "no network: $($_.Exception.Message)" }
Log "python: $(& $py -I -c 'import sys,zlib;print(sys.version.split()[0], zlib.ZLIB_RUNTIME_VERSION)')"
Log "whoami: $(whoami)"
Log "node: $(& node --version 2>&1)"
Log "temp: $env:TEMP  symlink privilege: $((whoami /priv | Select-String SeCreateSymbolicLink) -replace '\s+',' ')"
# run 2 (2026-10-29): a clean Sandbox lacks the Microsoft Visual C++ runtime that bpy needs. Copy the host's
# runtime DLLs (mapped read-only) into this disposable Sandbox's System32 before any test. Host is unaffected.
Log "vcrt copy: $((Get-ChildItem "$b\vcrt" -Filter *.dll | ForEach-Object { Copy-Item $_.FullName "$env:WINDIR\System32\" -Force -ErrorAction Continue; $_.Name }) -join ',')"
function Manifest($path){ Get-ChildItem $path -Recurse -File -Force | Sort-Object FullName | ForEach-Object { '{0}  {1}' -f (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower(), $_.FullName.Substring($path.Length) } }
Manifest $snap | Set-Content "$out\manifest-before-in-sandbox.txt"
Set-Location $snap
$steps = @(
 @{n='compileall'; a=@('-m','compileall','-q','apps','tools','tests')},
 @{n='pytest';     a=@('-m','pytest','-q','-p','no:cacheprovider')},
 @{n='blender-runtime-52'; a=@('tests/test_blender_runtime_52.py')},
 @{n='verify-package-zips'; a=@('tools/verify_package.py','--tag','v0.2.5','--source-dir',$snap,'--blender-zip',"$b\zips\CutBridge-Blender-v0.2.5.zip",'--ae-zip',"$b\zips\CutBridge-AfterEffects-v0.2.5.zip",'--output',"$out\verify-package.json")},
 @{n='verify-package-tests'; a=@('-m','pytest','-q','-p','no:cacheprovider','tests/test_verify_package.py')}
)
foreach($s in $steps){ Log "=== $($s.n) ==="; & $py @($s.a) *>&1 | Tee-Object -FilePath "$out\$($s.n).txt" | Select-Object -Last 40 | ForEach-Object { Log $_ }; Log "exit=$LASTEXITCODE" }
Set-Location $b
Manifest $snap | Set-Content "$out\manifest-after-in-sandbox.txt"
$same = (Get-FileHash "$out\manifest-before-in-sandbox.txt").Hash -eq (Get-FileHash "$out\manifest-after-in-sandbox.txt").Hash
Log "snapshot manifest identical before/after: $same"
Log "done $(Get-Date -Format o)"
'DONE' | Set-Content "$out\DONE.flag"




