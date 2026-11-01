# UI readability: colour-coded status line — 2026-11-01

Owner request (course plugin set): make the plugins' UI easier to see. Branch `ui/readability-20261101` from `develop` 9c33c8f, commit 368a626: in the After Effects panel the status line (READY / WARNING / ERROR) is bold and coloured (green / amber / red). Display only; no change to load, build, QC or revision logic, and no change to the Blender add-on.

IMPORTANT: this changes `apps/after-effects/CutBridge.jsx`, so the candidate identity (abf5882d / ecfb26ce) would change if merged. Do not merge while S14B testers are using the current kit/candidate; re-build and re-verify the candidate after merging.

## Native observation (one machine, After Effects 2026)
Panel run from the branch worktree with File > Scripts > Run Script File (not installed; the installed copy in Program Files was not touched). No package loaded → 「Status: WARNING」 shown in bold amber. READY/ERROR colours not shown natively this run.

## Checks on the branch
pytest (CI AE/static set + test_ae_beta2_panel_ux): 151 passed, 1 failed — `test_artifact_symlink_cannot_overwrite_another_file` (WinError 1314, Windows symlink privilege; known machine limitation, not a code defect). Node AE checks: 18/18 pass.
