# Native P1 GUI install - 2026-10-30 (WIB)

Evidence class: **NATIVE** (Blender 5.2.2 LTS on the owner's Windows 11 host). Procedure: `docs/NATIVE_INSTALL_QA.md` section 1. Bounded academic evidence; not a release approval. This covers the part of row P1 that the 2026-10-28 run left open: the **Install from Disk** dialog (that run installed through the command line).

## Candidate

- `CutBridge-Blender-v0.2.5.zip`, SHA-256 `3a53f7af...a48aa48` (`inputs-SHA256.txt`), the same bytes verified on 2026-10-29 (`../sandbox-verification-20261029/`).

## How it ran

1. Claude created an empty profile folder (0 files) and started Blender 5.2.2 with `BLENDER_USER_RESOURCES` pointing at it, so the owner's normal Blender profile was not used.
2. Claude could not drive the window: computer-use screenshots of this Blender window came back as a flat grey frame, so no clicks were attempted. One extra Blender process that the automation tool started by itself (owner's default profile) was closed within seconds, before any action ran in it.
3. **The owner performed the install by hand** in the isolated Blender: Edit > Preferences > Get Extensions > Install from Disk..., selected the ZIP, installed, then pressed N in the 3D viewport and confirmed the **CutBridge** tab. The owner reported "Done" with no problems noted. Claude did not observe the screen during these steps.
4. Claude closed Blender normally (it saved the preferences on quit, `blender-gui-session-log.txt`) and ran `qa_gui_install_check.py` headless with the same profile and **without** `--factory-startup`, so the saved preferences decide what is enabled.

## Result

| ID | Case | Expected | Result |
| --- | --- | --- | --- |
| P1 (GUI) | Install from Disk with the verified Blender ZIP | Enables, panel visible | **PASS** |

From `qa_gui_install_check.txt`:

- All 22 ZIP entries are installed with identical SHA-256. No extra files apart from `__pycache__` (`installed-files-SHA256.txt`).
- `bl_ext.user_default.cutbridge` is enabled in the saved preferences, `addon_utils.check` reports loaded, and `scene.cutbridge` is registered.
- One `VIEW_3D` panel in the `CutBridge` sidebar category (`CutBridge`). This agrees with the owner's report that the N-panel tab appeared.

## Limits

- The visible result (dialog text, N-panel tab) rests on the owner's report. No screenshot was captured.
- One host, one Blender build. No other versions or operating systems.
- On quit, Blender also wrote its standard session-recovery file to `%TEMP%\quit.blend` (an empty scene), replacing whatever recovery file was there before.
- The isolated profile folder was deleted after this folder was written.
