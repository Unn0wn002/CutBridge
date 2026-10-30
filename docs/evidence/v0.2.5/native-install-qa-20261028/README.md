# Native install and restart QA - 2026-10-28

Evidence class: **NATIVE** (Blender 5.2.2 LTS and After Effects 26.5x89, both real hosts). Procedure: `docs/NATIVE_INSTALL_QA.md`. This is bounded academic evidence. It is **not** a release approval, and the overall release-readiness verdict stays `INSUFFICIENT EVIDENCE` (see `docs/RELEASE_PREPARATION_v0.2.5.md`).

## Candidate identity

- Source: PR #112 head `35fb9b9aede318624eea80d46b1dea3462ec4747` (product source unchanged since `049c095`). Tag used for the local build: `v0.2.5` (unpublished, local only).
- Built from an LF `git archive` snapshot with Python 3.13 (zlib 1.3.1), the same toolchain family as CI:

| Artifact | SHA-256 | Matches the CI record |
| --- | --- | --- |
| `CutBridge-Blender-v0.2.5.zip` | `3a53f7af8420909e5ed300440df115dffef2ba1dd196688c7c99789a8a48aa48` | yes |
| `CutBridge-AfterEffects-v0.2.5.zip` | `ae9bfb9c2aa36c6764b324ac74ef85cc5022071b04bb7b7695e64a3651f70366` | yes |

- `tools/verify_package.py --tag v0.2.5 --source-commit 35fb9b9...` reported `ok: true` for both ZIPs.

## Hosts and how each was driven

- Blender 5.2.2 LTS (build hash `d13f752e3b9c`, 2026-09-15). Run headless (`blender -b --factory-startup`) with `BLENDER_USER_RESOURCES` pointing at a scratch folder, so the user's own Blender profile was not touched. The Blender GUI "Install from Disk" dialog and the N-panel were **not** exercised.
- After Effects 26.5x89, build 89, en_US, Windows 11. Driven through its UI. The panel was opened with File > Scripts > Run Script File on `CutBridge.jsx` extracted from the verified AE ZIP; the dockable `ScriptUI Panels` install and its restart step were **not** exercised.
- Before this run the user repaired the AE installation (`jpeg_wrapper.dll` had been missing).

## Results

| ID | Case | Result | Evidence |
| --- | --- | --- | --- |
| P1 | Clean install of the verified Blender ZIP | PASS (CLI path) | `extension install-file` reported `Installed "cutbridge"`; all 21 installed files match the ZIP bytes; the extension enables and `scene.cutbridge` registers; see `blender-run-v003.log` |
| P2 | Export V001 and import/Build/QC in AE | PASS | Blender `validate` and `build_package` returned FINISHED, 3 frames rendered; AE loaded V001 (24 fps, 3 frames), built `C012_COMP` 480x270 with a managed `BEAUTY` layer, QC+ reported 10/10 PASS |
| P3 | Full AE quit, relaunch, reopen | PASS | `AfterFX` process absent after Exit, a new process started afterwards, project reopened with media rendering; the project state dump before the quit and after the relaunch is byte-identical (SHA-256 `69cbc996d963fc05acc1d9bc3bc50d0c707dd95dadc7d8b3ebc02c6f87da71cf`) |
| P4 | V002 then V003 revision swaps | PASS | each swap asked for confirmation and reported that managed layer properties and working layers were preserved; QC+ after V003: 10/10 PASS; the untagged artist `Null 1` layer survived, including after the relaunch |
| P5 | Optional camera/Null handoff | NOT_RUN | handoff was disabled in this run |
| N1 | Manifest without `fps` | PASS | rejected on load: "Manifest contract rejected: Manifest FPS must be a finite number greater than zero."; panel shows ERROR and no package |
| N2 | Revision candidate with a different FPS (30 vs 24) | PASS | refused before applying: "FPS changes are unsupported." |
| N3 | Revision candidate missing frame 2 | PASS, rejected at apply | the swap reached the confirmation prompt, then failed with "candidate pass does not contain the complete required frame sequence; rollback completed"; project state unchanged |
| N4 | Optional pass removed | NOT_RUN | |
| N5 | Skipped or non-newer revision | NOT_RUN as designed (an unintended same-version attempt was correctly refused with "Candidate must be a newer revision"; see below) | |
| N6 | Unmanaged same-name camera/Null | NOT_RUN | |

After N1, N2 and N3 a third project state dump is again byte-identical to the pre-quit state (same SHA-256), and the saved project file on disk was unchanged.

Frame content differed per revision (first-frame SHA-256 prefixes: V001 `C900824F99A0`, V002 `507C8B715FD7`, V003 `27F940E1CE38`). Manifest hashes: V001 `843db106...a9a277`, V002 `c667ca30...094595bac`, V003 `0ea0a0c9...b033f3e4`.

## Observations

- The revision button asks for the *current* package first when none is loaded in the panel session (for example after a relaunch). Answering that first dialog with the new package makes current and candidate equal, which is refused correctly as "must be a newer revision"; this happened once during testing and was a test-driving error, not a defect.
- The panel's header text kept showing the previous package name after a successful swap (cosmetic; the project folder and QC reflected the new version).
- The missing-frame candidate is caught at apply time with rollback, not at assessment time, so the user sees the confirmation prompt first.

## Limits

- One scenario on one machine: a single BEAUTY pass of a default scene, 480x270, 3 frames; no optional passes, no camera/Null handoff.
- Blender part: headless operators in the real host with an isolated profile, not the GUI.
- No claim about other hosts or builds, Japanese-user validation (S14B is still `NOT_EXECUTED`) or distribution. Nothing was published or tagged.
- The AGENTS.md isolated-snapshot verification protocol was not used for this run, so no `PASS` verdict is issued under it; the rows above are scenario results.

## Files in this folder

`ae-state-before-quit.json`, `blender-run-v003.log`, `manifest-V001.json`, `manifest-V002.json`, `manifest-V003.json`, and the two scratch scripts used (`qa_blender_export.py`, `QA_DumpState.jsx`). Rendered frames, ZIPs and the AE project are not committed.
