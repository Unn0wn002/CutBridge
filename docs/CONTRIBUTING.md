# Contributing

Start each focused `feature/*` or `fix/*` branch from current `develop`. Open a PR into `develop`; merge only after every CI job passes on the reviewed revision. Promote a tested release candidate separately to `main`.

## Complete automated validation

Use Python 3.13 for the official Blender 5.2.1 wheel:

```bash
python -m pip install pytest jsonschema bpy==5.2.1
python -m compileall -q apps tools tests
python -m pytest -q
python tests/test_blender_runtime_52.py
TMPDIR="${TMPDIR:-/tmp}"
cp apps/after-effects/CutBridge.jsx "$TMPDIR/CutBridge.js"
node --check "$TMPDIR/CutBridge.js"
VERSION="$(python - <<'PY'
import tomllib
import sys
with open('apps/blender/cutbridge/blender_manifest.toml', 'rb') as fh:
    sys.stdout.write(tomllib.load(fh)['version'])
PY
)"
python tools/build_release.py --tag "v${VERSION}" --output dist-ci
test -f "dist-ci/CutBridge-Blender-v${VERSION}.zip"
test -f "dist-ci/CutBridge-AfterEffects-v${VERSION}.zip"
test -f dist-ci/SHA256SUMS.txt
test -f dist-ci/release-metadata.json
(cd dist-ci && tr -d '\r' < SHA256SUMS.txt | sha256sum --check)
```

PowerShell equivalent for the complete validation (Python 3.13, Node.js, and an empty `dist-ci` directory):

```powershell
$out = Join-Path (Get-Location).Path 'verification-output'
New-Item -ItemType Directory -Force "$out\pycache", "$out\tmp" | Out-Null
$env:PYTHONPYCACHEPREFIX = "$out\pycache"
$env:TEMP = "$out\tmp"; $env:TMP = $env:TEMP; $env:TMPDIR = $env:TEMP
python -m pip install pytest jsonschema bpy==5.2.1
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
python -m compileall -q apps tools tests
if ($LASTEXITCODE -ne 0) { throw 'Python compilation failed' }
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { throw 'Pytest failed' }
python tests/test_blender_runtime_52.py
if ($LASTEXITCODE -ne 0) { throw 'Blender RNA runtime checks failed' }
$jsCheck = Join-Path $env:TEMP 'CutBridge.js'
Copy-Item apps/after-effects/CutBridge.jsx $jsCheck
node --check $jsCheck
if ($LASTEXITCODE -ne 0) { throw 'After Effects JavaScript syntax check failed' }
$version = python -c "import tomllib; print(tomllib.load(open('apps/blender/cutbridge/blender_manifest.toml','rb'))['version'], end='')"
if ($LASTEXITCODE -ne 0) { throw 'Version lookup failed' }
$dist = 'dist-ci'
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
```

The packaging simulation reads the Blender manifest version, as CI does, so the tag and artifact checks stay aligned with the current source version. Its checksum check accepts CRLF line endings from Windows Python while still validating the artifact bytes. Use a fresh `dist-ci` output directory for each run.

The standalone RNA script must run separately: pytest imports it but does not execute its two lifecycle cycles. CI runs both the full pytest suite and this script. Node validates JavaScript syntax only; it does not exercise AE APIs or prove ExtendScript runtime compatibility.

For machines without Blender, Python 3.11+ can run the static and release tests with `pytest` and `jsonschema`. The release safety tests can also run without third-party packages:

```bash
python -m unittest discover -s tests -p test_release_hygiene.py -v
```

A missing dependency is BLOCKED, not a pass or a reason to skip authoritative tests. Use GitHub Actions evidence when local runtime installation is unavailable.

## Release output and source safety

Use an empty output directory, or one containing only the four artifacts of the same version. The builder refuses unrelated files, directories, symlink artifacts, and source overlap. Use a new directory for a different version. Fixed ZIP timestamps and permissions make identical source bytes reproducible with the same Python/zlib toolchain; do not assume compressed bytes match across different toolchain versions.

Keep versions, tests and docs synchronized. Never commit generated ZIPs, local cut packages, client assets, credentials, or footage. Retain branch history according to [BRANCHING.md](BRANCHING.md).

