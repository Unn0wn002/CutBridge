# Final QA review (non-executing) - 2026-10-29

Reviewer: Claude (Sonnet 5.5), independent read-only review for the Prompt 04 stage. Date: 2026-10-29 (WIB).
Scope: PR #115 (`work/cutbridge-install-qa-20261028`) and the evidence it carries. This is **not** a release approval, push, merge or tag.

## Verdict

- AGENTS.md verification verdict: **`INSUFFICIENT EVIDENCE`**. Reason: no environment satisfying the AGENTS.md "Verification execution security boundary" was available/approved, so no candidate-controlled command (pytest, Python scripts, build, Node) was executed by this review. No Docker or Podman is installed. Windows Sandbox (`WindowsSandbox.exe`) is present but was not set up or started (needs a dependency-preparation step and the owner's go-ahead).
- Demo recommendation: **`READY_FOR_ACADEMIC_DEMO`, bounded** to the recorded scenario (P1-P4, N1-N3). Everything else is `BLOCKED_ON_NATIVE_TEST` (P5, N4, N5, N6, GUI install dialog, dockable ScriptUI install).

## Identity

| Item | Value |
| --- | --- |
| Reviewed HEAD | `c1336696a19f87d54ab8e2000e94556bad69c145` (clean tree, equals `origin/work/cutbridge-install-qa-20261028`) |
| PR base / product candidate | `35fb9b9aede318624eea80d46b1dea3462ec4747` (PR #112 head). PR #115 adds only docs, evidence, `tools/verify_package.py`, `tests/test_verify_package.py` (11 files, +759 lines). No product source changed. |
| Diff hash (`git diff base...HEAD \| sha256sum`) | `22c28b2baf4ea8321cba98c2f1ef78fc06c2f5faeaf8bab1551765dee4dd9890` |
| Tag `v0.2.5` | Not present locally or on the remote at review time (earlier handoff said local). |
| PR #115 CI | `static-validation`, `blender-52-rna-runtime`, `isolated-candidate` all pass on `c133669`; merge state CLEAN. CI is not host evidence. |

## What I did check (VERIFIED_THIS_SESSION)

1. Git state, PR #115 checks/base/draft state, PR list (via `git`/`gh`, read-only).
2. Re-hashed the recorded evidence files; they match the values cited in the native README: `ae-state-before-quit.json` = `69cbc996...da71cf`; `manifest-V001/V002/V003` = `843db106...a9a277`, `c667ca30...094595bac`, `0ea0a0c9...b033f3e4`. This proves the files are unaltered, not that the runs were correct.
3. Read `tools/verify_package.py` in full. Findings: compares entry names, order and uncompressed SHA-256; rejects absolute/`..`/drive-colon names, duplicates and wrong filenames; the snapshot comes from `git archive` with autocrlf off; exit code follows `ok`. Limits: it executes `tools/build_release.py` from the snapshot (so it is itself candidate-controlled and must run inside the isolation boundary for a qualifying verdict); it checks only the supplied ZIPs' names for safety, not the rebuilt ones; it proves package-to-source identity only.
4. Compared documentation claims with proofs: matrix rows P1-P4/N1-N3 PASS, P5/N4/N5/N6 NOT_RUN agree with the native README. The partial scopes (N2 FPS only, N3 missing frame only, P1 CLI path only) are stated in the matrix. No overclaim found.

## Acceptance matrix (CutBridge package/native matrix)

| ID | Result | Evidence class | Code path / proof |
| --- | --- | --- | --- |
| Package identity | `ok: true` recorded for both ZIPs | HISTORICAL_RECORDED (2026-10-28, Python 3.13 / zlib 1.3.1) | `tools/verify_package.py`; ZIP SHA-256 `3a53f7af...a48aa48` (Blender), `ae9bfb9c...f70366` (AE) match CI record; not re-run |
| Verifier unit tests | 6 tests recorded passing | HISTORICAL_RECORDED, outside the AGENTS.md boundary | `tests/test_verify_package.py`; not re-run |
| P1 install (CLI, isolated profile) | PASS | HISTORICAL_RECORDED, native | `blender-run-v003.log`; GUI dialog NOT_RUN |
| P2 export, AE import/Build, QC+ 10/10 | PASS | HISTORICAL_RECORDED, native | native README, manifests |
| P3 AE quit/relaunch, byte-identical state | PASS | HISTORICAL_RECORDED, native | `ae-state-before-quit.json` (hash re-verified) |
| P4 V002/V003 swaps keep artist state | PASS | HISTORICAL_RECORDED, native | native README |
| P5 camera/Null handoff | NOT_RUN | - | handoff disabled |
| N1 missing `fps` rejected | PASS | HISTORICAL_RECORDED, native | native README |
| N2 FPS change refused | PASS (FPS only; range untested) | HISTORICAL_RECORDED, native | |
| N3 missing frame rejected with rollback | PASS (frame only; missing pass untested) | HISTORICAL_RECORDED, native | |
| N4 optional pass removed | NOT_RUN | - | |
| N5 skipped revision | NOT_RUN (an unintended same-version attempt was refused) | - | |
| N6 unmanaged same-name camera/Null | NOT_RUN | - | |

## Error paths, honesty, data safety (static review)

- Verifier writes only to a `tempfile` directory and the optional `--output` path; never installs or modifies the source tree.
- Failure modes: a corrupt ZIP raises `ValueError`; a missing ZIP raises an OS error; both end non-zero, never a false `ok`.
- Native runs used a disposable AE project and an isolated Blender profile; the saved project file was reported unchanged. Not independently re-observed.
- Known cosmetic issue (recorded, not fixed): the panel header keeps the previous package name after a successful swap. Missing-frame candidates are caught at apply time (with rollback), not at assessment.

## Open issues found by this review

1. **Isolation gap:** every local test/build run so far (including the 2026-10-28 session) was outside the AGENTS.md boundary. A qualifying verdict needs a sandboxed, no-network, read-only-snapshot run with before/after manifests.
2. **Undocumented sibling PRs:** #113 (`fix/current-release-completion-20261016`, 390 files) and #114 (`fix/free-release-20261021`, 498 files) are open drafts on the same merge-base `35fb9b9`. They add a candidate-verification toolchain (`tools/candidate_verification.py`, `tools/candidate_checks.sh`), validation JSON and native test scripts. PR #115 neither contains nor depends on them. PR #114 makes the dockable ScriptUI the primary install, so the dockable-install row may need re-scoping against it. Not reviewed in depth.
3. **Branching rule:** `AGENTS.md` says PRs target `develop`; #115 is stacked on #112. Base decision (task C) is still open.
4. **Evidence is one scenario on one machine** (single BEAUTY pass, 480x270, 3 frames). No Japanese-user validation (S14B `NOT_EXECUTED`).
5. **Toolchain caveat:** hashes match CI only with Python 3.13 (zlib 1.3.1); other toolchains differ in ZIP bytes and are checked by content identity only.

## Short demonstration script (bounded, ~10 min)

State up front: "one scenario, one machine, Blender 5.2.2 + After Effects 26.5x89, not a release."
1. Show `tools/verify_package.py` output (`ok: true`) and the two ZIP hashes versus the CI record.
2. Blender (isolated profile): install the ZIP, export V001 (3 frames).
3. After Effects: import the package, Build, show the managed `BEAUTY` layer and QC+ 10/10.
4. Make an artist-only change (the extra `Null 1` layer), swap to V002, then V003; show the layer survives.
5. Show one negative: load the manifest without `fps` and show the rejection message.
6. Close with the limits: P5/N4/N5/N6 not run, no sandboxed verification, no release.
Use a pre-recorded fallback (the evidence folder) if After Effects misbehaves; do not claim live results you did not see.

## Reproduce / next verification

1. Prepare Python 3.13 + `pytest jsonschema bpy==5.2.1` in a reviewed image/folder separately from execution.
2. Take a `git archive` snapshot of the candidate; record `manifest-before.sha256`.
3. Run inside a disposable VM (for example Windows Sandbox with networking disabled and a read-only mapped snapshot), with `PYTHONPYCACHEPREFIX`, `TEMP`, `TMP`, `TMPDIR` set to `verification-output/`: `python -m compileall -q apps tools tests`, `python -m pytest -q -p no:cacheprovider`, `python tests/test_blender_runtime_52.py`, `python tools/verify_package.py ...`.
4. Regenerate the manifest; any difference outside `verification-output/` makes the run `INVALID`.
Expected: `test_artifact_symlink_cannot_overwrite_another_file` fails with WinError 1314 on unprivileged Windows (machine limit).

## Remaining unknowns

Sandboxed pass/fail of the full suite; P5/N4/N5/N6; Blender GUI install; dockable ScriptUI install; interaction with PRs #113/#114; PR #115 final base; S14B.

## Addendum: sandbox attempt - BLOCKED (2026-10-29, WIB)

A Windows Sandbox run was prepared (read-only snapshot of `c133669`, copied deps, network disabled, only `out\` writable; kit at `_sandbox_qa_20261029\`, not committed). Four launches failed before the script started: two before a host reboot and two after, one of them a bare default sandbox with no mapped folders. Error: `The virtual machine or container exited unexpectedly (0x80370106)`. `out\` stayed empty, so **no candidate code was executed** and no test result exists. The failure is in the host virtualization platform, not the kit. Fixing it needs administrator action (for example checking Virtual Machine Platform / Windows Sandbox / Hyper-V features and conflicting virtualization software), which I did not attempt. Verdict unchanged: `INSUFFICIENT EVIDENCE`; sandboxed verification is `BLOCKED`.
