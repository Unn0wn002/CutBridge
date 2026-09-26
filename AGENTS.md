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

- Developer implements on its isolated feature/fix/bootstrap branch and reports the exact commit SHA, changed paths, commands, and outputs.
- Verifier independently inspects that exact commit and its full diff, using a separate checkout/worktree. It runs the relevant tests itself, checks repository integrity and release safeguards, and reports evidence or BLOCKED. Never accept the Developer's claim as verification.
- Developer and Verifier must not edit the same worktree concurrently. For a local verifier worktree, from the repository root use `git worktree add --detach <sibling-verifier-path> <exact-commit-sha>`. Remove a worktree only after its work is finished and its changes are accounted for.
- If verification finds a defect, return the finding and evidence to Developer for repair; then verify the new exact commit independently.
- The Computer Operator is used only when a required GUI action cannot be verified through an API, CLI, logs, or observable project state. Never invent host results or screenshots.

This bootstrap adds instructions only. It does not authorize product changes, branch promotion, merge, release, or publication.
