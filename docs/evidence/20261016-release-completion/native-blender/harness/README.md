# Prepared native Blender campaign input

Prepared without executing candidate code. Run only after the trusted launcher verifies the retained Windows Sandbox isolation policy and runtime boundary. This input is not native-result evidence until it runs.

Required read-only input mappings and runtime:

- `C:\Review\candidate.json` containing the exact 40-character `sha` (or `candidate_sha`).
- The exact built Blender ZIP, selected with `CUTBRIDGE_BLENDER_ZIP`; default `C:\Inputs\CutBridge-Blender-v0.2.5.zip`.
- This directory mapped read-only at the launcher's chosen path; invoke its `native_blender.py` with `C:\Blender\blender.exe --python-exit-code 1 --python <readonly-script-path>`.
- Blender's official extension manager must first create repo ID `cutbridge_candidate`, install this exact ZIP and enable `bl_ext.cutbridge_candidate.cutbridge` using the same isolated config/data/extensions directories as the GUI launch. The script compares installed file bytes to every ZIP entry. Preserve CLI install/enable logs; the script does not certify install dialogs.
- Use a fresh isolated profile with the normal default Camera/Cube scene. Do not add `--background`. Do not discard saved extension preferences with `--factory-startup` after installation.
- Set `PYTHONPYCACHEPREFIX`, `TEMP`, `TMP`, `TMPDIR`, `BLENDER_USER_CONFIG`, `BLENDER_USER_DATAFILES` and `BLENDER_USER_EXTENSIONS` under `C:\Evidence\verification-output`; the harness records/checks these paths. No owner home, credentials, sockets or network may be exposed.

Writable results: `C:\Evidence\verification-output\native-blender`. Packages are `packages\Native025_EP01_SC010_C001_T01_V001` through V003. Synthetic `.blend` fixtures and their SHA-256s, fixture contract, native evaluated-versus-manifest Camera/Empty comparisons, all package inventories/hashes, artist state and rollback before/after state are retained there.

The GUI timer starts the campaign after two seconds. It uses native operators/APIs to render 36 mixed PNG/OpenEXR pass outputs over V001–V003, verifies exact expected names/header bytes/nonzero files, checks value-level handoff data, preservation, overwrite/contract mismatch and injected missing-LINE rollback, saves and opens the final fixture within the same process. It then requests normal Blender quit after two seconds. The launcher must observe actual process exit, retain exit code/stdout/stderr, compare input manifests and verify output containment.

`native-blender.json` is authoritative only for the executed scripted scope. Assertions record actual failures. Missing prerequisites or unexpected harness/host exceptions report INSUFFICIENT EVIDENCE pending classification. GUI visual inspection, install-dialog/button-click inspection, fresh-process reopen, AE, live update behavior and S14B remain explicitly NOT_EXECUTED. No overall release PASS follows from this report alone.

For fresh-process persistence, the launcher can start a separate GUI process with the retained `fixtures\reopen-V003.blend` and an independently retained reopen harness; this script does not claim that check.
