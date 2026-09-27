# CutBridge agent instructions

## Project identity

- Project: CutBridge
- Canonical repository: https://github.com/Unn0wn002/CutBridge
- Host applications: Blender and Adobe After Effects
- Technology: Blender Python (`bpy`) and After Effects ExtendScript/JavaScript
- Supported hosts: Blender 4.2.0 minimum; current LTS targets 4.2, 4.5, and 5.2, with Blender 5.2.1 the authoritative automated runtime. After Effects 2024–2026 is the target range; native evidence is scoped to the exact versions and scenarios recorded in `docs/COMPATIBILITY.md` and `docs/RELEASE_READINESS.md`.
- Source: `apps/blender/cutbridge/`, `apps/after-effects/`, `packages/`

## Branch and safety rules

- Read `docs/BRANCHING.md` before branching. Start focused work from the fetched `develop` tip; PRs target `develop`. Promotion to `main` is a separate release action.
- Treat `main`, `develop`, release tags, published releases, production distribution, and `release-authorization.json` as protected. Never modify protected release state, weaken a release gate, merge, or publish without the owner's explicit authorization.
- Use authenticated GitHub CLI operations for repository, issue, pull-request, and Actions inspection. Never expose or copy tokens or other credentials; keep any authorized development changes on an isolated branch.
- Preserve unrelated changes. Never reset, clean, or overwrite work you did not create.
- Do not commit generated ZIPs, local packages, client assets, credentials, or footage.

## Development and test contract

Use the existing commands in `docs/CONTRIBUTING.md`; do not create parallel scripts:

- Setup: `python -m pip install pytest jsonschema bpy==5.2.1` (Python 3.13 for the official Blender wheel).
- Static syntax check: `python -m compileall -q apps tools tests`.
- Unit, integration, and regression suite: `python -m pytest -q`.
- Blender host-runtime entry point: `python tests/test_blender_runtime_52.py`; run the complete pytest suite as well.
- Build/package validation: use the version-resolved packaging simulation in `docs/CONTRIBUTING.md` and `.github/workflows/ci.yml`; it invokes `tools/build_release.py` with a fresh output directory. This creates local verification artifacts only.
- Release verification: follow `docs/RELEASE_CHECKLIST.md` and `docs/RELEASE_READINESS.md`, including exact-candidate CI and required native-host evidence. There is no separate `verify-release` script; do not add a duplicate gate.

CI and local host evidence are distinct. `.github/workflows/ci.yml` runs `static-validation` and `blender-52-rna-runtime`; CI does not prove Blender GUI behavior or After Effects runtime behavior. Use the applicable real-host steps in `docs/RELEASE_CHECKLIST.md` when those gates are in scope. Prefer API/CLI checks over GUI automation.

Every reproducible fixed defect should receive a regression test when practical. Never claim success without recorded test evidence. A missing dependency or unavailable host is BLOCKED, not a pass.

There is no separate `test-regression` command; regression coverage is part of the complete pytest suite and is named in the applicable `tests/test_*.py` tests.

## Developer and verifier handoff

- Keep Developer and experiment work in separate worktrees branched from the fetched `origin/develop` tip; for example, `git worktree add -b feature/<slug> ../CutBridge-<slug> origin/develop` (use `fix/<slug>` for bug repairs). Do not let agents edit the same worktree concurrently. Verifier receives the immutable snapshot below, never Developer's live worktree.
- Developer works on an isolated `feature/*` or `fix/*` branch from the fetched `develop` tip and reports the candidate branch, exact commit SHA (or `UNCOMMITTED SNAPSHOT`), working-tree state, changed paths, commands, and outputs.
- Do not give Verifier Developer's live mutable checkout. Main creates a fresh verification snapshot from the exact candidate in a separate temporary directory. Exclude `.git`, credentials, unrelated user files, and caches unless a test requires them. Include the candidate diff against its recorded base as review input.
- Before Verifier runs, record `manifest-before.sha256` for every project input outside the designated writable `verification-output/` directory. Keep that directory out of both manifests. Do not broadly ignore cache names or other paths elsewhere in the snapshot.
- Redirect generated files into `verification-output/` before running checks. Set the Python bytecode cache and temporary-file paths as follows:

  ```powershell
  $out = Join-Path (Get-Location).Path 'verification-output'
  New-Item -ItemType Directory -Force "$out\pycache", "$out\tmp" | Out-Null
  $env:PYTHONPYCACHEPREFIX = "$out\pycache"
  $env:TEMP = "$out\tmp"; $env:TMP = $env:TEMP; $env:TMPDIR = $env:TEMP
  ```

  ```bash
  OUT="$PWD/verification-output"
  mkdir -p "$OUT/pycache" "$OUT/tmp"
  export PYTHONPYCACHEPREFIX="$OUT/pycache"
  export TMPDIR="$OUT/tmp" TMP="$OUT/tmp" TEMP="$OUT/tmp"
  ```

- Run pytest with its cache provider disabled, for example `python -m pytest -q -p no:cacheprovider`. For package checks, use the version-resolved command in `docs/CONTRIBUTING.md` and direct its output to `verification-output/` (for example, `--output verification-output/dist-ci`). Put reports and other test artifacts there too. Deliberately redirected bytecode, temporary files, reports, and build outputs inside that directory are permitted and excluded from the source/test manifest; cache or other generated files outside it are not.
- Verifier reads and tests the snapshot without editing source, tests, or project instructions. Any source/test input change or generated file outside `verification-output/` makes the run `INVALID`.
- Verifier independently inspects the supplied candidate diff, runs the relevant project checks, inspects outputs, and checks release safeguards. Do not accept Developer's claim as verification.
- After Verifier completes, regenerate the source/test manifest. Any difference outside `verification-output/` makes the verification `INVALID`; create a fresh snapshot before any rerun.
- Verifier returns exactly one verdict: `PASS`, `FAIL`, `INVALID`, `INSUFFICIENT EVIDENCE`, or `WORKSPACE_NOT_ACCESSIBLE`. `FAIL` means a genuine test or behavior failure and records the test, expected and actual result, reproduction evidence, and relevant logs. `INVALID` means integrity assumptions were violated, such as a changed source/test input, a manifest mismatch outside approved output, or mutation of protected snapshot inputs. An `INVALID` run is neither PASS nor FAIL, must not be reused, and requires a fresh snapshot before rerun. `PASS` records candidate SHA/snapshot ID, tests and results, and a matching source/test integrity comparison.
- If verification finds a defect, send its exact evidence to Developer for repair, then create a new snapshot and repeat independent verification. Never reuse a verifier snapshot after it has been modified.
- This snapshot-and-manifest procedure detects unexpected source changes but is not an OS-level read-only sandbox; do not claim hard filesystem enforcement.
- The Computer Operator is used only when a required GUI action cannot be verified through an API, CLI, logs, or observable project state. Never invent host results or screenshots.

This bootstrap adds instructions only. It does not authorize product changes, branch promotion, merge, release, or publication.
