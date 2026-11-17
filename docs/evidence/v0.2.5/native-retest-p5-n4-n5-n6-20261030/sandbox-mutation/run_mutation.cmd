@echo off
rem Offline Windows Sandbox run (scratch script, copied into the evidence folder).
rem C:\snap = read-only snapshot of 3c3b26b, C:\node = read-only node.exe, C:\out = only writable mapped folder.
set OUT=C:\out
set PATH=C:\node;%PATH%
echo started %DATE% %TIME% > %OUT%\sandbox-run.txt
ping -n 1 -w 1000 github.com >> %OUT%\sandbox-run.txt 2>&1 && echo NETWORK REACHABLE >> %OUT%\sandbox-run.txt || echo network unreachable as configured >> %OUT%\sandbox-run.txt
node --version >> %OUT%\sandbox-run.txt
echo === unmodified snapshot (read-only) >> %OUT%\sandbox-run.txt
cd /d C:\snap
node tests\ae_s6_revision_checks.cjs > %OUT%\unmodified.txt 2>&1
echo unmodified exit %ERRORLEVEL% >> %OUT%\sandbox-run.txt
echo === mutant: newer-only rule weakened from ^<= to ^< >> %OUT%\sandbox-run.txt
robocopy C:\snap C:\mut /E /NFL /NDL /NJH /NJS > nul
powershell -NoProfile -Command "$p='C:\mut\apps\after-effects\revision_manager.js'; $t=[IO.File]::ReadAllText($p); $old='if (candidate.version <= current.version)'; if (-not $t.Contains($old)) { 'MUTATION TARGET NOT FOUND'; exit 3 }; [IO.File]::WriteAllText($p, $t.Replace($old, 'if (candidate.version < current.version)')); 'mutation applied'" >> %OUT%\sandbox-run.txt 2>&1
cd /d C:\mut
node tests\ae_s6_revision_checks.cjs > %OUT%\mutant.txt 2>&1
echo mutant exit %ERRORLEVEL% >> %OUT%\sandbox-run.txt
echo finished %DATE% %TIME% >> %OUT%\sandbox-run.txt
echo DONE > %OUT%\DONE.txt
