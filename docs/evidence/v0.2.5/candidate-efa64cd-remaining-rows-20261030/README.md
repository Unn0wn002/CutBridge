# Remaining native rows on the efa64cd candidate bytes - 2026-10-30 (WIB)

Companion to `../candidate-efa64cd-20261030/`, which re-ran P5, N4, N5 and N6 on the rebuilt candidate. This folder covers the remaining recorded rows on the **same bytes**: P1 (GUI dialog), P2, P3, P4, N1, N2, N3, and P6. Bounded academic evidence; not a release approval. Run by Claude at the owner's request. The P1 GUI clicks were made by the owner.

| Artifact | SHA-256 |
| --- | --- |
| `CutBridge-Blender-v0.2.5.zip` | `abf5882d56856d4662e95b2ac1335fb0dc6e818f5f7113235dce0529385b2207` |
| `CutBridge-AfterEffects-v0.2.5.zip` | `ecfb26ce8e5ad50638e17b35104efc2210d222b4ac8f10fccf0fba2748c17d8f` |

## Rebuild (`sandbox-rebuild/`)

The ZIPs used here were rebuilt from `fix/v025-release-preparation` at `a48646d857fbe4f40b894ff4d0be8cd1d82328fe` (`tip.txt`).

- **Docs-only since efa64cd:** `git diff --name-only efa64cd..a48646d` lists 54 paths, all under `docs/` or `.gitattributes` (`diff-efa64cd-to-a48646d.txt`).
- **Build environment:** an offline Windows Sandbox with vGPU and networking disabled (`qa-build.wsb`), using Python 3.13.17 / zlib 1.3.1. The input was a read-only snapshot made with `git -c core.autocrlf=false archive` of that commit (`snapshot-command.txt`, 563-file `snapshot-manifest.sha256`).
- **Hash agreement:** both hashes equal the efa64cd Sandbox build (`../candidate-efa64cd-20261030/sandbox/SHA256SUMS.txt`) and the release metadata of four CI isolated runs for `392fff8` and `a48646d` (`ci-isolated-build-hashes.txt`, with run links).
- **Package identity:** `verify_package.py` reports `ok: true` (`verify-package.json`). It was given the snapshot folder, so its `source_commit` field is null; the commit is bound by `snapshot-command.txt`.

This step only built and verified; the full test suite ran in the companion folder.

## Native rows (`native/`, `p1-gui/`)

Blender 5.2.2 LTS and After Effects 26.5x89 on the owner's Windows 11 host. These runs are **not isolated**. Blender used a fresh empty profile. After Effects started with no leftover CutBridge globals in every phase (`harness-log-A.json`, `-B.json`, `-C.json`). The panel buttons were pressed by `QA_rows_harness_A.jsx`, `_B.jsx` and `_C.jsx` with dialogs auto-answered; this was not a person clicking. Each phase ran once, with no retries. Phase C was added after a self-review found that P4 had not been exercised by phases A and B.

Packages: V001, V002 and V003 were exported with `qa_retest_export.py`. Its install check compares every ZIP entry except `LICENSE` (21 of the 22 entries) with the installed files; all 21 match (`qa_blender_log_v00*.txt`). The P1 check below compares all 22. The negative packages come from `make_negative_packages.py` (`negative-packages.txt`):
- N1: V001 with `fps` removed.
- N2: V002 with `fps` set to 30.
- N3: V002 with required `C014_BEAUTY_0002.png` deleted.

Each sits in its own parent folder, so package folder names stay valid.

"State A = state B" below means the two dumps are equal after removing their `label` field (`compare_rows.py`, `compare_p4.py`; outputs in `comparison-*.json` and `compare-*-output.txt`). Quoted alert texts omit the `CutBridge エラー` header and the `[EN] Error:` prefix; the full texts are in the harness logs.

| ID | Case | Result | Evidence |
| --- | --- | --- | --- |
| N1 | Manifest without `fps` | **PASS**: rejected on load with `Manifest contract rejected: - Manifest FPS must be a finite number greater than zero.`; the project, still empty, was unchanged (`state-00` = `state-01`) | `harness-log-A.json`, `comparison-rows.json` |
| N2 | Revision candidate at 30 fps vs 24 | **PASS**: refused with `FPSの変更には対応していません。 [EN] FPS changes are unsupported.`; project unchanged (`state-05` = `state-06`) | same |
| N3 | Revision candidate missing a required frame | **PASS**: reached the confirmation, then `Revision failed: ... BEAUTY: candidate pass does not contain the complete required frame sequence.; rollback completed.`; project unchanged (`state-05` = `state-07`) | same |
| P2 | Export V001, import, Build, QC+ | **PASS**: V001 exported in Blender (the 21 compared entries match the installed files); AE loaded it, built `C014_COMP` 480x270 @ 24 fps; QC+ PASS | `qa_blender_log_v001.txt`, `harness-log-A.json` |
| P3 | Full quit, relaunch, reopen | **PASS** (details below) | `p3-quit-relaunch.txt`, `state-08`, `state-09`, `state-12`, `comparison-rows.json` |
| P4 | V002 then V003 revisions with artist work present | **PASS**: phase C (`QA_rows_harness_C.jsx`, in a newly started AE with no AE process running beforehand; pid not captured, `p4-process.txt`) built V001, added the same artist null, note and marker, then applied V001→V002 and V002→V003 in order. Each revision asked for confirmation and reported success; QC+ PASS after each. Every managed layer was retagged to V002 and then V003; layer names and order, the artist null (note and position) and the marker were unchanged | `harness-log-C.json`, `state-22`, `state-23`, `state-25`, `comparison-p4.json` |
| P6 | Dockable `ScriptUI Panels` install | **Bound by bytes, not re-docked**: the four files in `...\Scripts\ScriptUI Panels` (last written 2026-10-29) have full SHA-256 values equal to the new AE ZIP's runtime files, so the 2026-10-29 docking result (`../dockable-install-qa-20261029/`) applies to these bytes | `p6-installed-vs-new-zip.txt` |
| P1 | Blender "Install from Disk" dialog | **PASS**, details below | `p1-gui/` |

**P3 details.** V001 was built with QC+ PASS. Then the harness added work CutBridge does not own: an untagged null `ARTIST_NOTE` with a layer comment, and an `artist marker` comp marker. After the project was saved (`qa_p3.aep`, SHA-256 `c97c2fc2...`), `app.quit()` left **0** `AfterFX` processes. A new process started (pid 38556; phase A's was 34464). Phase B reopened the project:
- The state dump equals the pre-quit dump. The label-free canonical hash is `d805843e...` for both (`compare-rows-output.txt`).
- No footage is missing, and comp size, FPS and duration are unchanged.
- The artist null, its note and the marker are intact, and the managed BEAUTY layer is still tagged.
- After the panel was reopened in the new process, loading V001 and running QC+ gave PASS and changed nothing (`state-09` = `state-12`).
- The project file was not changed by phase B (same SHA-256 afterwards, `p3-quit-relaunch.txt`).

**P1 GUI details.** Claude started Blender with `BLENDER_USER_RESOURCES` pointing at a newly created folder counted as empty, so the owner's normal profile was not used (`profile-before-launch.txt`, transcribed from the launching command's output). **The owner** ran Edit > Preferences > Get Extensions > Install from Disk with the ZIP above and confirmed the N-panel **CutBridge** tab. Claude did not observe the screen. Claude then closed Blender normally, which saved the preferences (`blender-gui-session-log.txt`), and ran `qa_gui_install_check.py` headless without `--factory-startup`:
- all 22 ZIP entries installed byte-identical, with no extra files;
- the extension enabled in the saved preferences and loaded;
- `scene.cutbridge` registered, with one VIEW_3D panel in the `CutBridge` category.

## Limits

- One scenario on one machine (480x270, 3 frames). P3 is a scripted save/quit/relaunch/reopen, not a person working in the project.
- P6 was not re-docked on these bytes; its claim rests on byte identity of the installed files.
- The P1 visible result rests on the owner's report; no screenshot was captured. On quit, Blender also rewrote its standard `%TEMP%\quit.blend` recovery file.
- S14B remains NOT_EXECUTED. No release, tag or authorization change.
- Renders, `.blend` files, the AE project, ZIPs and the snapshot are not committed. The scratch folders were deleted after this folder was written.
