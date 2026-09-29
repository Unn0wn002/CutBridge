# Contributing

Start each focused `feature/*` or `fix/*` branch from current `develop`. Open a PR into `develop`; merge only after every CI job passes on the reviewed revision. Promote a tested release candidate separately to `main`.

## Complete automated validation

Prepare Python 3.13, Node.js 22, `pytest`, `jsonschema`, and the official Blender 5.2.1 wheel before candidate execution. Dependency preparation must be separate from candidate execution; do not enable network access to install dependencies while running candidate-controlled commands. Run these checks from the repository root inside the approved isolated environment. Candidate inputs remain read-only and all generated files go under `verification-output/`.

### Bash

```bash
OUT="$PWD/verification-output"
mkdir -p "$OUT/pycache" "$OUT/tmp"
export PYTHONPYCACHEPREFIX="$OUT/pycache"
export TEMP="$OUT/tmp" TMP="$OUT/tmp" TMPDIR="$OUT/tmp"

python -m compileall -q apps tools tests
python -m pytest -q -p no:cacheprovider
python tests/test_blender_runtime_52.py

for file in CutBridge.jsx revision_manager.js qc_plus.js localization.js; do
  cp "apps/after-effects/$file" "$TMPDIR/$file"
  node --check "$TMPDIR/$file"
done

VERSION="$(python -c "import tomllib; print(tomllib.load(open('apps/blender/cutbridge/blender_manifest.toml','rb'))['version'], end='')")"
DIST="$OUT/dist-ci"
python tools/build_release.py --tag "v${VERSION}" --output "$DIST"
test -f "$DIST/CutBridge-Blender-v${VERSION}.zip"
test -f "$DIST/CutBridge-AfterEffects-v${VERSION}.zip"
test -f "$DIST/SHA256SUMS.txt"
test -f "$DIST/release-metadata.json"
(cd "$DIST" && tr -d '\r' < SHA256SUMS.txt | sha256sum --check)
python - "$DIST/CutBridge-AfterEffects-v${VERSION}.zip" "$VERSION" <<'PY'
import sys, zipfile
with zipfile.ZipFile(sys.argv[1]) as archive:
    names = set(archive.namelist())
    required = {'CutBridge.jsx', 'revision_manager.js', 'qc_plus.js', 'localization.js', 'INSTALL.md', 'LICENSE'}
    assert required <= names, f'missing AE package files: {sorted(required - names)}'
    install = archive.read('INSTALL.md').decode('utf-8')
    assert 'development build' not in install.lower()
    assert 'unpublished' not in install.lower()
    assert 'RELEASE_TAG' not in install
    assert f'/blob/v{sys.argv[2]}/docs/RELEASE_READINESS.md' in install
PY
```

### PowerShell

```powershell
$out = Join-Path (Get-Location).Path 'verification-output'
$null = New-Item -ItemType Directory -Force "$out\pycache", "$out\tmp"
$env:PYTHONPYCACHEPREFIX = "$out\pycache"
$env:TEMP = "$out\tmp"; $env:TMP = $env:TEMP; $env:TMPDIR = $env:TEMP

python -m compileall -q apps tools tests
if ($LASTEXITCODE -ne 0) { throw 'Python compilation failed' }
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { throw 'Pytest failed' }
python tests/test_blender_runtime_52.py
if ($LASTEXITCODE -ne 0) { throw 'Blender RNA runtime checks failed' }

foreach ($file in @('CutBridge.jsx', 'revision_manager.js', 'qc_plus.js', 'localization.js')) {
    $jsCheck = Join-Path $env:TEMP $file
    Copy-Item (Join-Path 'apps/after-effects' $file) $jsCheck
    node --check $jsCheck
    if ($LASTEXITCODE -ne 0) { throw "After Effects syntax check failed: $file" }
}

$version = python -c "import tomllib; print(tomllib.load(open('apps/blender/cutbridge/blender_manifest.toml','rb'))['version'], end='')"
if ($LASTEXITCODE -ne 0) { throw 'Version lookup failed' }
$dist = Join-Path $out 'dist-ci'
if (Test-Path $dist) { throw "Use a fresh output directory: $dist" }
python tools/build_release.py --tag "v$version" --output $dist
if ($LASTEXITCODE -ne 0) { throw 'Release packaging simulation failed' }
foreach ($name in @("CutBridge-Blender-v$version.zip", "CutBridge-AfterEffects-v$version.zip", 'SHA256SUMS.txt', 'release-metadata.json')) {
    if (-not (Test-Path (Join-Path $dist $name))) { throw "Missing release artifact: $name" }
}
foreach ($line in Get-Content (Join-Path $dist 'SHA256SUMS.txt')) {
    if ($line -notmatch '^([a-f0-9]{64})  (.+)$') { throw "Invalid checksum line: $line" }
    $actual = (Get-FileHash (Join-Path $dist $Matches[2]) -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $Matches[1]) { throw "Checksum mismatch: $($Matches[2])" }
}
$aeZip = Join-Path $dist "CutBridge-AfterEffects-v$version.zip"
@'
import sys, zipfile
with zipfile.ZipFile(sys.argv[1]) as archive:
    names = set(archive.namelist())
    required = {'CutBridge.jsx', 'revision_manager.js', 'qc_plus.js', 'localization.js', 'INSTALL.md', 'LICENSE'}
    assert required <= names, f'missing AE package files: {sorted(required - names)}'
    install = archive.read('INSTALL.md').decode('utf-8')
    assert 'development build' not in install.lower()
    assert 'unpublished' not in install.lower()
    assert 'RELEASE_TAG' not in install
    assert f'/blob/v{sys.argv[2]}/docs/RELEASE_READINESS.md' in install
'@ | python - $aeZip $version
if ($LASTEXITCODE -ne 0) { throw 'After Effects archive inspection failed' }
```

The package check resolves the product version from `apps/blender/cutbridge/blender_manifest.toml`. Node checks JavaScript syntax only; it does not exercise AE APIs or prove ExtendScript runtime compatibility. Keep focused regression suites required by changed files and canonical CI in the verification run. The standalone Blender RNA script is required because pytest imports it but does not execute its lifecycle cycles.

For machines without Blender, Python 3.11+ can run static and release tests with `pytest` and `jsonschema`. This is partial evidence only; it does not replace the required Blender runtime check. A missing dependency is BLOCKED, not a pass or a reason to skip authoritative checks.

## Release output and source safety

Use a fresh output directory for each package build. The builder refuses unrelated files, directories, symlink artifacts, and source overlap. Fixed ZIP timestamps and permissions make identical source bytes reproducible with the same Python/zlib toolchain; do not assume compressed bytes match across different toolchain versions.

Keep versions, tests, and docs synchronized. Never commit generated ZIPs, local cut packages, client assets, credentials, or footage. Retain branch history according to [BRANCHING.md](BRANCHING.md).
