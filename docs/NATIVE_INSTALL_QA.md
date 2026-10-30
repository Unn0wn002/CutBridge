# CutBridge native install and restart checklist

Status: **Procedure, with recorded runs on 2026-10-28** (`docs/evidence/v0.2.5/native-install-qa-20261028/README.md`), **2026-10-29** (P6) **and 2026-10-30** (P5, N4, N5, N6: `docs/evidence/v0.2.5/native-rows-p5-n4-n5-n6-20261030/README.md`). Rows not listed as recorded stay `NOT_RUN`. This page grants no release, install or compatibility approval. Existing evidence is scoped in [RELEASE_READINESS.md](RELEASE_READINESS.md) and the `docs/evidence/v0.2.5/` records; its After Effects reopen checks are **same-process** reopens, not a full quit and relaunch.

## 0. Identify the candidate before installing anything

1. Record the full source commit: `git rev-parse HEAD`.
2. Build from a clean line-ending-neutral snapshot, not from a CRLF Windows checkout:

   ```text
   git -c core.autocrlf=false archive --format=tar -o source.tar HEAD
   ```

   Extract it to an empty folder and run `python tools/build_release.py --tag <tag> --output <empty folder>` from there.
3. Prove package-to-source identity. This compares every ZIP entry's uncompressed bytes with the same commit and ignores zlib differences:

   ```text
   python tools/verify_package.py --tag <tag> --source-commit <full sha> --blender-zip <file> --ae-zip <file> --output verify-report.json
   ```

   Pass means content identity only. Whole-ZIP SHA-256 values match across machines only when the same zlib built them; this host family may use zlib-ng, so a different hash with `content_identical: true` is expected. Record both ZIP SHA-256 values and the report.
4. Never install a ZIP whose verifier result is not `ok: true`, and never reuse a published v0.2.4 AE ZIP (known stale `INSTALL.md`, Issue #99).

## 1. Clean Blender install from ZIP (supported host, Blender 4.2+; 5.2.x LTS is the automated target)

1. Use a clean Blender user profile or confirm CutBridge is not enabled; record which.
2. Preferences, extension **Install from Disk**, select `CutBridge-Blender-<tag>.zip`, enable it.
3. Record: Blender version/build, install result text, N-panel **CutBridge** visible, no console errors.

## 2. Export a package ([QUICK_START.md](QUICK_START.md) sections 2, 4, 6, 7)

Use a disposable `.blend` and an empty output folder. Do not point CutBridge at production data.

1. Prepare the cut: save, active camera, FPS, resolution, range starting at frame 0 or later, metadata, preset.
2. Run **Validate Cut**, then **Build Package** for V001. Render the selected sequences.
3. Record the package folder name, `cutbridge.json` hash, frame range, FPS and the rendered file count per pass.

## 3. After Effects install and import (use the AE ZIP from step 0)

1. Extract all four runtime files together (`CutBridge.jsx`, `revision_manager.js`, `qc_plus.js`, `localization.js`). Either **File > Scripts > Run Script File...** or copy them to `Scripts/ScriptUI Panels` and open **Window > CutBridge** after a restart.
2. Import the package, **Build**, run **QC+**. Record comp name, range, FPS, linked media paths and QC result.
3. Add a visible artist edit that CutBridge does not own (an unrelated layer, a marker, and a note).
4. Save the project to a disposable location.

## 4. Full quit and relaunch (the step existing evidence does not cover)

1. Quit After Effects completely from its menu. Confirm no `AfterFX` process remains:

   ```text
   Get-Process AfterFX -ErrorAction SilentlyContinue
   ```

   An empty result is required. A hung process is a `BLOCKED` note, not a pass.
2. Relaunch After Effects, reopen the saved project, reopen the CutBridge panel.
3. Verify and record each: comp frame range and FPS, footage still linked (no missing media), CutBridge-managed layers intact, the artist edits from step 3.3 unchanged.

## 5. Revisions V002 and V003 (after a relaunch)

Build V002 from a package whose content changed, then V003. Confirm V001/V002/V003 identities, artist-state preservation, and that nothing outside CutBridge ownership was altered.

## 6. Native acceptance matrix

| ID | Case | Expected | Status |
| --- | --- | --- | --- |
| P1 | Clean install from verified Blender ZIP | Enables, panel visible | PASS 2026-10-28 (CLI install, isolated profile; GUI dialog not exercised) |
| P2 | Export V001, import and Build in AE | Range, FPS, media match manifest | PASS 2026-10-28 |
| P3 | Full AE quit, relaunch, reopen | Range, linking, artist state preserved | PASS 2026-10-28 |
| P4 | V002 then V003 revisions | Correct revision tags, artist state kept | PASS 2026-10-28 |
| P5 | Optional camera/Null (only if handoff enabled) | Managed camera/Null reconstructed | PASS 2026-10-30 (one camera, one 3D Null; keys and ownership tags checked, camera projection parity not measured) |
| N1 | Bad or missing `cutbridge.json` field | Import rejected before any project change | PASS 2026-10-28 (missing `fps`) |
| N2 | FPS or range mismatch vs manifest | Rejected or flagged, no silent change | PASS 2026-10-28 (FPS, via revision swap; range not tested) |
| N3 | Missing or changed required pass | Rejected, nothing created | PASS 2026-10-28 (missing frame, rejected at apply with rollback; missing pass not tested) |
| N4 | Optional pass removed | Warning only, no error | PASS 2026-10-30 (LINE frames removed before import) |
| N5 | Skipped revision (V001 to V003, V002 never applied) | Applied after confirmation: the rule is "Candidate must be a newer revision" (`revision_manager.js`), matching README "newer package"; same or older revisions are rejected | PASS 2026-10-30 against this corrected expectation. Until 2026-10-30 this row expected "Rejected"; the run applied V001 to V003 and the original expectation was corrected, not the code (see the correction note below). Rejection of a same or older revision was not run natively; it is covered by the Node check "revision rule is newer-only" in `tests/ae_s6_revision_checks.cjs` |
| N6 | Same-name unmanaged camera/Null | Fail closed, no adoption | PASS 2026-10-30 (Null only; same-name unmanaged camera not run) |
| P6 | Dockable `ScriptUI Panels` install (Window menu, dock, relaunch) | Appears, docks, layout survives AE restart | PASS 2026-10-29 (see `docs/evidence/v0.2.5/dockable-install-qa-20261029/`; docked by hand; panel functions not exercised) |

N5 correction (2026-10-30): the original "Rejected" expectation required sequential revisions, which no user-facing document or code path specifies; the product contract is newer-only. Changing the code instead would have altered the verified v0.2.5 candidate. If sequential revisions are wanted, that is a product change needing its own test and native run.

Automated Node and pytest coverage for several rows exists but does not substitute for these native results. After a run, copy the recorded values into a dated evidence folder; do not edit existing evidence.

## 7. Limits

- Tested hosts only: record the exact Blender and After Effects builds. Do not extend a pass to other versions, operating systems or workflows.
- No representative Japanese-user validation (S14B stays `NOT_EXECUTED`). Do not distribute font files with a demo.
- This checklist does not authorize tagging, publishing or updating the distribution repository.

## 8. Five to ten minute demo script

1. (1 min) State the candidate: tag, source commit, verifier `ok: true`, ZIP hashes.
2. (1 min) Show Blender N-panel **CutBridge**, run **Validate Cut** on the prepared disposable cut.
3. (1 min) **Build Package** V001 and show the package folder and `cutbridge.json`.
4. (2 min) In After Effects import, **Build**, run **QC+**; point out range, FPS and linked media.
5. (1 min) Add an artist layer, save, quit After Effects fully, show no `AfterFX` process, relaunch and reopen.
6. (2 min) Show the artist layer and managed layers intact, then V002 revision and one negative case (changed pass rejected).
7. (1 min) Close with the unmet gates: native rows not run here, S14B, release authorization.
