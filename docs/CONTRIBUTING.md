# Contributing

Start each focused `feature/*` or `fix/*` branch from current `develop`. Open a PR into `develop`; merge only after every CI job passes on the reviewed revision. Promote a tested release candidate separately to `main`.

## Complete automated validation

Use Python 3.13 for the official Blender 5.2.1 wheel:

```bash
python -m pip install pytest jsonschema bpy==5.2.1
python -m compileall -q apps tools tests
python -m pytest -q
python tests/test_blender_runtime_52.py
cp apps/after-effects/CutBridge.jsx /tmp/CutBridge.js
node --check /tmp/CutBridge.js
python tools/build_release.py --tag v0.2.3 --output dist-ci
(cd dist-ci && sha256sum --check SHA256SUMS.txt)
```

The standalone RNA script must run separately: pytest imports it but does not execute its two lifecycle cycles. CI runs both the full pytest suite and this script. Node validates JavaScript syntax only; it does not exercise AE APIs or prove ExtendScript runtime compatibility.

For machines without Blender, Python 3.11+ can run the static and release tests with `pytest` and `jsonschema`. The release safety tests can also run without third-party packages:

```bash
python -m unittest discover -s tests -p test_release_hygiene.py -v
```

A missing dependency is BLOCKED, not a pass or a reason to skip authoritative tests. Use GitHub Actions evidence when local runtime installation is unavailable.

## Release output and source safety

Use an empty output directory, or one containing only the four artifacts of the same version. The builder refuses unrelated files, directories, symlink artifacts, and source overlap. Use a new directory for a different version. Fixed ZIP timestamps and permissions make identical source bytes reproducible with the same Python/zlib toolchain; do not assume compressed bytes match across different toolchain versions.

Keep versions, tests and docs synchronized. Never commit generated ZIPs, local cut packages, client assets, credentials, or footage. Retain branch history according to [BRANCHING.md](BRANCHING.md).
