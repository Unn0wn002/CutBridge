# v0.2.5 candidate efa64cd: isolated rebuild and native re-verification - 2026-10-30 (WIB)

PRs #116 and #118 changed packaged text (Blender help, diagnostic, property description, handoff validation, AE `INSTALL.md`), so the earlier candidate ZIPs (`3a53f7af...`, `ae9bfb9c...`) no longer describe the branch. This folder rebuilds the candidate from `fix/v025-release-preparation` at `efa64cd0aaa489495430090cdd8fe68648a28e5d` and repeats the key checks on the new bytes. Bounded academic evidence; not a release approval. Run by Claude at the owner's request.

## Candidate

| Artifact | SHA-256 |
| --- | --- |
| `CutBridge-Blender-v0.2.5.zip` | `abf5882d56856d4662e95b2ac1335fb0dc6e818f5f7113235dce0529385b2207` |
| `CutBridge-AfterEffects-v0.2.5.zip` | `ecfb26ce8e5ad50638e17b35104efc2210d222b4ac8f10fccf0fba2748c17d8f` |

Built with Python 3.13.17 / zlib 1.3.1 inside the Sandbox below (`sandbox/release-metadata.json`, `sandbox/SHA256SUMS.txt`). The four AE runtime scripts are byte-identical to the previous candidate; the AE ZIP differs only in `INSTALL.md`.

## 1. Isolated build and verification (`sandbox/`): PASS

- **Isolation:** Windows Sandbox, `sandbox/qa-efa64cd.wsb`, with networking, vGPU, clipboard, audio, video and printer disabled. Mapped read-only:
  - a `git -c core.autocrlf=false archive` snapshot of `efa64cd` (513 files, no `.git`);
  - Python 3.13, the 2026-10-29 dependency folder (pytest, jsonschema, bpy 5.2.1);
  - Node and the VC++ runtime DLLs;
  - the run script.

  Only `out` was writable, and no credentials were mapped. The run log shows `github.com` unresolvable. Started with `wsb start` and run with `wsb exec` as SYSTEM inside the disposable VM.
- **Build:** `tools/build_release.py --tag v0.2.5` ran twice. The file names and all four outputs are byte-identical between the two runs.
- **Package identity:** `tools/verify_package.py --source-dir <snapshot>` reports `ok: true`. Both ZIPs are content-identical to the snapshot rebuild, with no missing, extra, changed, duplicate or unsafe entries (`sandbox/verify-package.json`).
- **Repository checks:**
  - `compileall`: exit 0.
  - `pytest -q -p no:cacheprovider`: **325 passed, 2 subtests passed**.
  - `tests/test_blender_runtime_52.py`: bpy 5.2.1 RNA registration PASS.
- **Integrity:** the snapshot SHA-256 manifest is identical before and after, both inside the Sandbox and on the host (`sandbox/manifest-*`).

## 2. Native re-run on the owner's host (`native/`): PASS

Blender 5.2.2 LTS and After Effects 26.5x89. These runs are **not isolated**: native-host evidence on the owner's machine, as in `../native-install-qa-20261028/` and `../native-retest-p5-n4-n5-n6-20261030/`. They used a fresh work folder, a fresh empty Blender profile, and a freshly started AE with no leftover CutBridge globals (`native/harness-log.json`). The procedure and scripts are those of `../native-retest-p5-n4-n5-n6-20261030/`, unchanged, plus one new Blender script.

- **Install:** `extension install-file` of the new Blender ZIP. All 21 installed files match it (`native/qa_blender_log_v00*.txt`).
- **Export:** V001, V002 and V003 were built and rendered. Their manifests are byte-identical to the earlier retest's (`native/inputs-SHA256.txt`); the changed files affect wording and validation, not this scene's output.

| ID | Result | Evidence |
| --- | --- | --- |
| P5 | **PASS**: one managed `Camera` and one 3D `QA_NULL`, tagged. The Null projection matches Blender within 0.000013 px after Build and after the V003 revision | `comparison.json`, `ae_projection-*.json`, `blender_projection_v001.json` |
| N4 | **PASS**: `LINE: optional pass skipped`; QC+ WARNING only | `harness-log.json` |
| N5 | **PASS**: V001 to V003 applied after confirmation. V003 to V002 and V003 to V003 rejected with `Candidate must be a newer revision.`, with project state unchanged (`state-09` = `state-11` = `state-12`) | `harness-log.json`, `comparison.json` |
| N6 | **PASS**: an untagged same-name `QA_NULL` and an untagged same-name `Camera` were each refused, with project state unchanged | `comparison.json` |

### New in this candidate: orientation fails closed (PR #118)

`native/qa_orientation_fail_closed.py` ran four fresh factory scenes with 3D handoff on, using the installed add-on (`native/orientation_results.json`):

| Case | Validate | Build | Package folders created |
| --- | --- | --- | --- |
| Level camera + marked Empty (control) | WARNING only | FINISHED | 1 |
| Camera rolled 10 degrees | `HANDOFF_CAMERA_ROLL_UNSUPPORTED` | refused | 0 |
| Marked Empty rotated 15 degrees | `HANDOFF_NULL_ROTATION_UNSUPPORTED` | refused | 0 |
| Empty level at frame 1, rotated on later keys | WARNING only | refused ("rotated at frame 2") | 0 |

## Limits

- One scenario on one machine (480x270, 3 frames, one camera, one Null). Projection parity compares geometric projections, not rendered pixels.
- Native panel actions were pressed by the harness with dialogs auto-answered; not a person clicking. The Blender "Install from Disk" dialog was not repeated for the new ZIP (`../native-p1-gui-install-20261030/` used the previous ZIP).
- Not repeated on these bytes:
  - full AE quit/relaunch (P3);
  - N1–N3;
  - P6 (dockable install);
  - S14B (NOT_EXECUTED).
- Branch commits after `efa64cd` that add this folder and update the records change docs only, not packaged files.
- Several `sandbox/*.txt` step logs are UTF-16 because Windows PowerShell 5 `Tee-Object` wrote them; `run.log` has the same content in UTF-8. All files here are stored byte-exact (`-text`).
- Renders, `.blend` files, ZIPs and the snapshot are not committed. The scratch folders were deleted after this folder was written.
