@echo off
rem Second offline Sandbox run (scratch script, copied into the evidence folder).
rem Isolates the new "revision rule is newer-only" group: the earlier selectLatest assertion (test line 71)
rem also catches the <= to < mutant, so it is removed in sandbox-local copies only.
set OUT=C:\out
set PATH=C:\node;%PATH%
set DROP=powershell -NoProfile -Command "$p='tests\ae_s6_revision_checks.cjs'; $t=[IO.File]::ReadAllText($p); $old='    assert.equal(R.selectLatest(m(2), [m(1), m(2)]), null);'; if (-not $t.Contains($old)) { 'LINE 71 NOT FOUND'; exit 3 }; [IO.File]::WriteAllText($p, $t.Replace($old + [char]10, '')); 'line 71 assertion removed'"
echo started %DATE% %TIME% > %OUT%\sandbox-run2.txt
ping -n 1 -w 1000 github.com >> %OUT%\sandbox-run2.txt 2>&1 && echo NETWORK REACHABLE >> %OUT%\sandbox-run2.txt || echo network unreachable as configured >> %OUT%\sandbox-run2.txt
echo === control: line 71 removed, rule unchanged >> %OUT%\sandbox-run2.txt
robocopy C:\snap C:\ctl /E /NFL /NDL /NJH /NJS > nul
cd /d C:\ctl
%DROP% >> %OUT%\sandbox-run2.txt 2>&1
node tests\ae_s6_revision_checks.cjs > %OUT%\control2.txt 2>&1
echo control exit %ERRORLEVEL% >> %OUT%\sandbox-run2.txt
echo === mutant: line 71 removed, rule weakened from ^<= to ^< >> %OUT%\sandbox-run2.txt
robocopy C:\snap C:\mut2 /E /NFL /NDL /NJH /NJS > nul
cd /d C:\mut2
%DROP% >> %OUT%\sandbox-run2.txt 2>&1
powershell -NoProfile -Command "$p='apps\after-effects\revision_manager.js'; $t=[IO.File]::ReadAllText($p); $old='if (candidate.version <= current.version)'; if (-not $t.Contains($old)) { 'MUTATION TARGET NOT FOUND'; exit 3 }; [IO.File]::WriteAllText($p, $t.Replace($old, 'if (candidate.version < current.version)')); 'mutation applied'" >> %OUT%\sandbox-run2.txt 2>&1
node tests\ae_s6_revision_checks.cjs > %OUT%\mutant2.txt 2>&1
echo mutant exit %ERRORLEVEL% >> %OUT%\sandbox-run2.txt
echo finished %DATE% %TIME% >> %OUT%\sandbox-run2.txt
echo DONE > %OUT%\DONE2.txt
