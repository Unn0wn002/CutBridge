# CutBridge for After Effects — Installation

CutBridge S7 development packages use **three adjacent script files**:

- `CutBridge.jsx` — panel, package import, Build Comp, QC, and the native After Effects revision adapter.
- `revision_manager.js` — non-destructive revision-manager core loaded by `CutBridge.jsx`.
- `qc_plus.js` — S7 deterministic QC+ diagnostic engine. The current S7 branch packages and tests this sidecar while native panel wiring is completed in the same S7 workstream.

Keep these files together. Copying or shipping only `CutBridge.jsx` leaves revision support unavailable and produces an incomplete S7 package.

## First development test

1. Keep `CutBridge.jsx`, `revision_manager.js`, and `qc_plus.js` in the same directory.
2. In After Effects, choose **File > Scripts > Run Script File...**.
3. Select `CutBridge.jsx`.
4. Import a CutBridge package, build the comp, and run QC.

`Run Script File...` is the least ambiguous first test because Adobe script-install paths vary by After Effects version and operating system.

## Dockable panel

For a dockable ScriptUI panel:

1. Copy **all three** files into the After Effects `Scripts/ScriptUI Panels` directory for the installed version.
2. Restart After Effects.
3. Open **Window > CutBridge**.

Do not separate the sidecars from the JSX panel file.

## Validation boundary

S6 native revision validation already covered V001 → V002 → V003, artist-property preservation, save/reopen behavior, Build Comp, and QC on the validated S6 candidate.

S7 QC+ automated tests verify diagnostic severity, stable codes, deterministic ordering, remediation requirements, non-mutating behavior, packaging, and compatibility with the complete existing regression suite. Native S7 panel behavior must not be claimed until the QC+ engine is wired into `CutBridge.jsx` and, if that host behavior materially changes, separately executed in real After Effects.

Automated Node/host-shaped tests are regression evidence; they are **not native After Effects certification**. See `../../docs/QUICK_START.md`, `../../docs/TEST_PLAN.md`, `../../docs/S6_REVISION_CONTRACT.md`, and `../../docs/S7_QC_PLUS_CONTRACT.md` for the validation boundaries.
