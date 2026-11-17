# Native rows P5, N4, N5, N6 - 2026-10-30 (WIB)

Evidence class: **NATIVE** (Blender 5.2.2 LTS and After Effects 26.5x89 on the owner's Windows 11 host). Procedure: `docs/NATIVE_INSTALL_QA.md` section 6. Bounded academic evidence; not a release approval. Run by Claude while the owner was away; the owner asked for these rows to be run.

## Candidate

- ZIPs from `_sandbox_qa_20261029\zips\`, the same bytes verified on 2026-10-29 (`verify_package.py` `ok: true`, see `../sandbox-verification-20261029/`): Blender `3a53f7af...a48aa48`, After Effects `ae9bfb9c...f70366`. Product source equals PR #115 head `a1113a7` (= `35fb9b9`).
- Blender: `extension install-file` into an isolated `BLENDER_USER_RESOURCES` profile; all 21 installed files match the ZIP (`qa_blender_log_v00*.txt`).
- After Effects: the four runtime files extracted from the AE ZIP into a scratch folder and run from there (`inputs-SHA256.txt`); they also match the copies installed in `ScriptUI Panels`.

## How each host was driven

- Blender headless, `--factory-startup`, script `qa_native_rows_export.py`: one disposable cut, custom preset `qa_preset_optional_line.json` (BEAUTY required, LINE optional), 3D handoff enabled (perspective `Camera` plus one marked Empty `QA_NULL` moving x 0 to 1 over frames 1-3), 100 px per Blender unit, Cycles 1 sample with Freestyle as render pass. Built and rendered V001 and V003 of the same cut.
- Before After Effects: the three V001 LINE frames were moved out of the package (hashes in `inputs-SHA256.txt`), so LINE is declared optional but unavailable.
- After Effects: `QA_native_rows_harness.jsx` (sent with `AfterFX.exe -r` to a freshly started AE) evaluates the unmodified `CutBridge.jsx`, captures its palette and presses the real panel buttons (`1. パッケージ読み込み`, `2. コンポ作成`, `3. QC実行`, `4. 差し替え`) with `notify("onClick")`. Dialogs were answered by the harness: `File.openDialog` returned the queued manifest, `confirm` returned true, `alert` text was recorded (`harness-log.json`). This is not a person clicking; AGENTS.md prefers script/API checks over GUI automation. The panel ran in Japanese (the stored locale preference); error texts include the `[EN]` line.
- Read-only state dumps after each step: `state-*.json`.

## Results

| ID | Case | Expected (matrix) | Result | Evidence |
| --- | --- | --- | --- | --- |
| P5 | Optional camera/Null handoff | Managed camera/Null reconstructed | **PASS** | Build created `Camera` (camera layer) and `QA_NULL` (3D null) in `C014_COMP`, each tagged `CUTBRIDGE|1|camera|...` / `CUTBRIDGE|1|null|...`. Null position keys 240 / 290 / 340 px at frames 0-2, matching the Empty's 0 / 0.5 / 1 BU at 100 px/BU; camera keyed at a constant position (the camera did not move). After the V003 revision both kept their keys and were retagged to V003 (`state-02-after-build.json`, `state-07-after-revision.json`). |
| N4 | Optional pass removed | Warning only, no error | **PASS** | Build completed with `警告: LINE: optional pass skipped — missing frame(s): 1, 2, 3`; QC+ `WARNING — 1 warning(s)` (`CBQ-SEQ-OPTIONAL-FRAMES-MISSING`), all other checks PASS, no error. |
| N5 | Unexpected revision (skip V002 to V003) | Rejected | **FAIL against the matrix expectation** | `4. 差し替え` from V001 to V003 asked for confirmation and then reported `V003へ差し替えました` (applied). The code's rule is only "Candidate must be a newer revision" (`revision_manager.js`), so a skipped version is accepted by design. Either the matrix row or the code is wrong; that is an owner decision, not settled here. Post-revision QC+: WARNING only (`CBQ-FOOTAGE-OPTIONAL-MISSING` for LINE). |
| N6 | Same-name unmanaged camera/Null | Fail closed, no adoption | **PASS** | With an untagged artist null named `QA_NULL` added to `C014_COMP`, Build refused: `QA_NULL: ambiguous managed null ownership ... CutBridge will not adopt it or add a duplicate.` Project state before and after the refused Build is identical (`state-04-before-rebuild.json` vs `state-05-after-rebuild.json`, equal apart from the label field); the artist null stayed untagged and no second managed null appeared. |

Only the null half of N6 was exercised; a same-name unmanaged *camera* was not, although the camera path uses the same check (`findManagedCamera`).

## Earlier runs (`earlier-runs/`, kept, not used for the results)

1. `run1-harness-scope-artifact`: my wrapper made `CutBridge.jsx`'s top-level `var CutBridgeContract` local, so `revision_manager.js` fell back and the revision failed with "managed-state access is unavailable for 3D revision migration; rollback completed". Harness defect; fixed by re-exporting `CutBridgeContract` to `$.global` as a normal run has it.
2. `run2-stale-global-artifact`: same AE process; `CutBridge.jsx` reuses a global `CutBridgeRevisionManager` (line 1169) left by run 1, so the same error repeated. AE was quit and restarted before every later run.
3. `run3-dump-classification-bug` and `run4-dump-evalfile-bug`: same dialog results as the final run; my state dumps misclassified project items, so layer details were missing. Final run dumps inline in the harness.

P5, N4 and N6 dialog outcomes were the same in all four runs. N5 applied in runs 3, 4 and the final run once the harness defects were removed.

## Limits and notes

- One scenario on one machine: 480x270, 3 frames, one camera and one null; projection parity of the camera (FOV/orientation vs Blender render) was not measured, only reconstruction, ownership and key values.
- QC+ output does not list camera/null checks for this package; P5 rests on the state dumps.
- In the dumps the top-level item `kind` field is unreliable (an ExtendScript `instanceof` quirk inside that expression); use `typeName`. Layer data is unaffected.
- The harness added and then removed the artist null; its solid (`Null 2`) stays in the Solids folder, which is the only difference between `state-02` and `state-06`.
- Nothing was saved: every run used `app.newProject()` and closed with `DO_NOT_SAVE_CHANGES`. Renders, `.blend` files, ZIPs and the AE runtime copies are not committed.
- GUI install dialog (Blender "Install from Disk") and S14B remain NOT_RUN / NOT_EXECUTED. Matrix rows in `docs/NATIVE_INSTALL_QA.md` are not edited here.
