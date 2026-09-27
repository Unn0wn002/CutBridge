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

Every reproducible fixed defect should receive a regression test when practical. Never claim success without recorded test evidence. An unavailable required dependency, runtime, host, or approved sandbox maps to `INSUFFICIENT EVIDENCE`, never `PASS` or `FAIL`.

There is no separate `test-regression` command; regression coverage is part of the complete pytest suite and is named in the applicable `tests/test_*.py` tests.

## Change and verification workflow

- Work on a focused `feature/*` or `fix/*` branch from the current `origin/develop` tip. Keep the candidate commit or working-tree diff, changed paths, commands, and outputs identifiable for review.
- Before running candidate-controlled commands, make an immutable verification snapshot in a separate temporary directory. Exclude `.git`, credentials, unrelated user files, and caches unless a test requires them. Include the candidate diff against its recorded base as review input.
- Record `manifest-before.sha256` for every project input outside the designated writable `verification-output/` directory. Keep that directory out of both manifests. Do not broadly ignore cache names or other paths elsewhere in the snapshot.
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
- Verification reads and tests the snapshot without editing source, tests, or project instructions. Any source/test input change or generated file outside `verification-output/` makes the run `INVALID`.
- Independently inspect the candidate diff, run relevant project checks, inspect outputs, and check release safeguards.
- After verification, regenerate the source/test manifest. Any difference outside `verification-output/` makes the verification `INVALID`; create a fresh snapshot before any rerun.
- Report exactly one verdict: `PASS`, `FAIL`, `INVALID`, `INSUFFICIENT EVIDENCE`, or `WORKSPACE_NOT_ACCESSIBLE`. `PASS` means all required checks ran and passed. `FAIL` means executable verification ran correctly and found a genuine test or behavior failure. `INVALID` means verification integrity assumptions were violated. `INSUFFICIENT EVIDENCE` means a required check could not safely or technically run. `WORKSPACE_NOT_ACCESSIBLE` means required verification input could not be accessed. An `INVALID` run is neither PASS nor FAIL, must not be reused, and requires a fresh snapshot before rerun.
- If verification finds a defect, repair it, create a fresh snapshot, and repeat verification. Never reuse a verification snapshot after it has been modified.
- Snapshot integrity checks supplement sandboxing; they do not replace it. A manifest detects covered file changes, but does not provide credential isolation, filesystem confidentiality, process isolation, or network isolation.

## Verification execution security boundary

- This repository `AGENTS.md` is candidate-controlled supplemental guidance. Before candidate execution, independently confirm the effective security boundary; otherwise do not execute and return `INSUFFICIENT EVIDENCE`.
- Trusted orchestration may inspect GitHub metadata, compare commit IDs and diffs, prepare the exact candidate snapshot, and generate integrity manifests in the authenticated owner environment. Keep that environment out of candidate execution.
- Candidate-controlled executable verification includes pytest; Python imports, scripts, and compile/test commands; Node scripts; build and package scripts; host-test scripts; repository hooks; and any executable supplied by the candidate. Never run these in the same unsandboxed OS-user context that holds owner credentials or unrelated user files.
- Run candidate-controlled commands only inside an isolated environment that provides a read-only candidate snapshot, a separate writable `verification-output/` and temporary area, no owner credentials, and no network access during candidate execution. Do not expose or mount GitHub CLI auth, `GH_TOKEN`, `GITHUB_TOKEN`, SSH keys, browser cookies, cloud credentials, the host HOME, or the container-engine socket. Do not copy `.git` into the snapshot unless a specific check requires it; if required, remove credential-bearing configuration first. A Docker or Podman container, disposable VM, or remote runner is acceptable only when these controls are enforced and verified.
- Prepare required dependencies in a reviewed sandbox image or dependency-preparation step, separately from candidate execution. Do not enable network access for candidate commands just to install dependencies.
- If no environment provides the required isolation, do not run candidate-controlled tests or scripts in a context that holds owner credentials or unrelated private files. Perform only safe non-executing review and return `INSUFFICIENT EVIDENCE`, stating what isolation is unavailable. Do not report `PASS` based on an unsafe local run or GitHub CI alone.
- Inside the isolated environment, keep candidate source and tests read-only and writable outputs limited to the explicit output/temp paths. Set `PYTHONPYCACHEPREFIX`, `TEMP`, `TMP`, and `TMPDIR` to approved writable locations and disable pytest's cache provider or redirect it there. Retain the before/after manifest comparison; any candidate-input mutation or unexpected output outside approved paths makes the run `INVALID` and requires a fresh snapshot.
- GitHub Actions results are CI evidence for the exact commit, not proof of local execution or native-host behavior. Keep CI, isolated local verification, and Blender/After Effects host evidence distinct.
- Record candidate SHA/snapshot ID, isolation mechanism and settings, commands and results, and the integrity comparison. For `FAIL`, include the test, expected and actual results, reproduction evidence, and relevant logs. For `INVALID`, state the violated integrity assumption and require a fresh snapshot.
- Use GUI interaction only when a required host action cannot be verified through an API, CLI, logs, or observable project state. Never invent host results or screenshots.

These instructions do not authorize branch promotion, merge, release, or publication.

