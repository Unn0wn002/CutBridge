# CutBridge for After Effects — Installation

CutBridge S6 uses **two adjacent script files**:

- `CutBridge.jsx` — panel, package import, Build Comp, QC, and the native After Effects revision adapter.
- `revision_manager.js` — non-destructive revision-manager core loaded by `CutBridge.jsx`.

Keep these files together. Copying or shipping only `CutBridge.jsx` leaves the S6 revision workflow unavailable.

## First development test

1. Keep `CutBridge.jsx` and `revision_manager.js` in the same directory.
2. In After Effects, choose **File > Scripts > Run Script File...**.
3. Select `CutBridge.jsx`.
4. Import a CutBridge package, build the comp, and run QC.

`Run Script File...` is the least ambiguous first test because Adobe script-install paths vary by After Effects version and operating system.

## Dockable panel

For a dockable ScriptUI panel:

1. Copy **both** `CutBridge.jsx` and `revision_manager.js` into the After Effects `Scripts/ScriptUI Panels` directory for the installed version.
2. Restart After Effects.
3. Open **Window > CutBridge**.

Do not separate the sidecar from the JSX panel file.

## S6 revision validation

A real desktop validation must exercise at least V001 → V002 → V003 and verify effects, masks, transforms, parenting, timing, artist-added layers, save/reopen behavior, Build Comp, and QC after revision/reload.

Automated Node/host-shaped tests are regression evidence; they are not native After Effects certification. See `../../docs/QUICK_START.md`, `../../docs/TEST_PLAN.md`, and `../../docs/S6_REVISION_CONTRACT.md` for the full validation boundary.
