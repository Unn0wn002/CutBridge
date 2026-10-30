$ErrorActionPreference = 'Continue'
$b = 'C:\Users\WDAGUtilityAccount\Desktop\qa'; $snap = "$b\snapshot"; $out = "$b\out"
New-Item -ItemType Directory -Force "$out\pycache" | Out-Null; $env:PYTHONPYCACHEPREFIX = "$out\pycache"
New-Item -ItemType Directory -Force C:\vtmp | Out-Null; $env:TEMP = "C:\vtmp"; $env:TMP = $env:TEMP; $env:TMPDIR = $env:TEMP
$py = "$b\py\python.exe"; $log = "$out\run.log"
function Log($m){ $m | Out-File -FilePath $log -Append -Encoding utf8 }
Log "start $(Get-Date -Format o)"
try { Log ((Invoke-WebRequest https://github.com -UseBasicParsing -TimeoutSec 8).StatusCode) } catch { Log "no network: $($_.Exception.Message)" }
Log "python: $(& $py -I -c 'import sys,zlib;print(sys.version.split()[0], zlib.ZLIB_RUNTIME_VERSION)')"
Set-Location $snap
Log "=== build ==="; & $py tools/build_release.py --tag v0.2.5 --output "$out\dist" *>&1 | Out-File "$out\build.txt" -Encoding utf8; Log "exit=$LASTEXITCODE"
Log "=== verify ==="; & $py tools/verify_package.py --tag v0.2.5 --source-dir $snap --blender-zip "$out\dist\CutBridge-Blender-v0.2.5.zip" --ae-zip "$out\dist\CutBridge-AfterEffects-v0.2.5.zip" --output "$out\verify-package.json" *>&1 | Out-File "$out\verify.txt" -Encoding utf8; Log "exit=$LASTEXITCODE"
Get-ChildItem "$out\dist" -File | ForEach-Object { Log ("{0}  {1}" -f (Get-FileHash $_.FullName).Hash.ToLower(), $_.Name) }
Log "done $(Get-Date -Format o)"; 'DONE' | Set-Content "$out\DONE.flag"
