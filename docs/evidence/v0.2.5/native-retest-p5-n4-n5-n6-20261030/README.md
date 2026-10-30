# Native retest of rows P5, N4, N5, N6 - 2026-10-30 (WIB)

Evidence class: **NATIVE** (Blender 5.2.2 LTS and After Effects 26.5x89 on the owner's Windows 11 host) plus one **offline Windows Sandbox** run for the Node check. Procedure: `docs/NATIVE_INSTALL_QA.md` section 6. Bounded academic evidence; not a release approval. Run by Claude at the owner's request to retest these rows cleanly and close the gaps left by the first run the same day (`../native-rows-p5-n4-n5-n6-20261030/`, not edited).

## What this retest adds over the first run

| Gap in the first run | Covered here |
| --- | --- |
| Four harness-defect runs before the usable one | One single pass, no retries; the harness clears leftover CutBridge globals first and logs that none were present |
| Camera did not move; P5 checked key values only | Camera moves and turns, the Empty moves on x and y; Blender's and After Effects' projections of the Empty are compared per frame |
| N6 tested only a same-name Null | Same-name Null and same-name Camera |
| N5 tested only the skip case | Skip (V001 to V003), older (V003 to V002) and same (V003 to V003) |
| Newer-only test not run outside CI, not mutation-tested | Run in an offline Windows Sandbox, with a mutant that weakens the rule |

## Candidate and clean start

- ZIPs from `_sandbox_qa_20261029\zips\`, unchanged since 2026-10-29 verification (`inputs-SHA256.txt`): Blender `3a53f7af...a48aa48`, After Effects `ae9bfb9c...f70366`. The four AE runtime files have the same hashes as in the first run.
- The first run's scratch folder was deleted before starting. A new scratch folder and a new empty Blender profile were created; CutBridge was installed with `extension install-file` (`blender-install.txt`), and all 21 installed files match the ZIP (`qa_blender_log_v00*.txt`).
- After Effects had no running process; it was started fresh, ran the harness once, and was quit with `quit_ae.jsx`. Nothing was saved (`app.newProject()`, closed with `DO_NOT_SAVE_CHANGES`).

## How each host was driven

- Blender headless, `--factory-startup`, `qa_retest_export.py`: one disposable cut, preset `qa_preset_optional_line.json` (BEAUTY required, LINE optional), 3D handoff at 100 px per Blender unit, Cycles 1 sample with Freestyle as render pass. V001, V002 and V003 were built and rendered. Blender's own projection of the Empty (`world_to_camera_view`) is in `blender_projection_v00*.json`.
- Before After Effects, the three V001 LINE frames were moved out of the package (`removed-line-SHA256.txt`).
- After Effects: `QA_retest_harness.jsx` (sent with `AfterFX.exe -r`) evaluates the unmodified `CutBridge.jsx` and presses the real panel buttons (`1. パッケージ読み込み`, `2. コンポ作成`, `3. QC実行`, `4. 差し替え`) with `notify("onClick")`. The harness answered the dialogs: `File.openDialog` returned the queued manifest, `confirm` returned true, `alert` text was recorded (`harness-log.json`). This is not a person clicking. The panel ran in Japanese; errors include the `[EN]` line.
- Projection in After Effects: a temporary text layer with the expression `L.toComp(L.anchorPoint)` on `QA_NULL`, read at frames 0-2 and removed (`ae_projection-*.json`).
- `compare_states.py` compares the read-only state dumps (`state-*.json`) and projections; its output is `comparison.json`.

## Results

| ID | Case | Expected (matrix) | Result | Evidence |
| --- | --- | --- | --- | --- |
| P5 | Optional camera/Null handoff | Managed camera/Null reconstructed | **PASS** | Build created one `Camera` and one 3D `QA_NULL`, tagged `CUTBRIDGE|1|camera|...V001|Camera` / `CUTBRIDGE|1|null|...V001|QA_NULL`. Camera Position and Point of Interest are keyed per frame (the camera moves and turns), Zoom 666.67. Projection of `QA_NULL` matches Blender within 0.000013 px at all three frames, both after Build and after the V003 revision (limit 0.5 px). After the revision both layers were retagged to V003 with the same keys. |
| N4 | Optional pass removed | Warning only, no error | **PASS** | Build: `警告: LINE: optional pass skipped — missing frame(s): 1, 2, 3`. QC+: `WARNING — 1 warning(s)` (`CBQ-SEQ-OPTIONAL-FRAMES-MISSING`), no error. |
| N5 | Skipped revision applies; same or older is rejected | As in the matrix since `d626b44` | **PASS** | V001 to V003: confirmed and `V003へ差し替えました`. V003 to V002 and V003 to V003: `差し替えを実行できません: - Candidate must be a newer revision.`, with project state identical to the state after V003 (`state-09` = `state-11` = `state-12`). |
| N6 | Same-name unmanaged camera/Null | Fail closed, no adoption | **PASS** | Untagged `QA_NULL`: Build refused with `ambiguous managed null ownership ... will not adopt it or add a duplicate`, state unchanged (`state-04` = `state-05`). Untagged camera `Camera`: Build refused with `ambiguous managed camera ownership ...`, state unchanged (`state-06` = `state-07`). |

After removing the artist null and camera, the project matches the post-Build state except for the artist null's solid (`Null 2`) left in the Solids folder (`state-02` vs `state-08`).

## Newer-only Node check in an offline Sandbox (`sandbox-mutation/`)

- Windows Sandbox, `mutation.wsb`: networking disabled (the run log shows `github.com` unresolvable), vGPU disabled, no clipboard. Mapped read-only: a `git archive` snapshot of `3c3b26b` without `.git`, `node.exe` v24.22.1 and the run scripts. Only `out` was writable. No credentials were mapped. The snapshot's 463-file SHA-256 manifest is identical before and after both runs.
- Run 1: unmodified snapshot, `tests/ae_s6_revision_checks.cjs` PASS (31 groups). Mutant (`<=` weakened to `<` in `revision_manager.js`, in a Sandbox-local copy) FAIL, exit 1. The mutant was first caught by an older assertion (test line 71, `selectLatest`), so run 1 shows the rule is guarded but not that the new check catches it.
- Run 2: in Sandbox-local copies with that older assertion removed. Control (rule unchanged) PASS. Mutant FAIL, at the first assertion of the new group "revision rule is newer-only". So the new check catches the mutant by itself.
- The first Sandbox start in this session failed because the config spelled `VGpu` instead of `vGPU` (the cause recorded in `../sandbox-root-cause-correction-20261030/`). It was corrected before either run; no test ran in the failed start.

## Limits

- One scenario on one machine: 480x270, 3 frames, one camera, one Null. Projection parity compares geometric projections from Blender and After Effects. Rendered pixels were not measured.
- The camera layer reports `threeD=false` in the dumps. That is After Effects' value for camera layers, not a defect.
- The matrix rows in `docs/NATIVE_INSTALL_QA.md` are updated separately to reference this folder.
- The Blender GUI install dialog (P1 GUI) and S14B remain NOT_RUN / NOT_EXECUTED.
- Renders, `.blend` files, ZIPs, the AE runtime copies and the Sandbox snapshot are not committed. The scratch folders were deleted after this folder was written.
