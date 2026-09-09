# CutBridge for After Effects — Installation

CutBridge S8 development packages use **four adjacent script files**:

- `CutBridge.jsx` — panel, package import, Build Comp, QC, revision adapter, and locale-aware UI binding.
- `revision_manager.js` — non-destructive revision-manager core loaded by `CutBridge.jsx`.
- `qc_plus.js` — S7 deterministic QC+ diagnostic engine.
- `localization.js` — S8 Japanese-first / English-fallback user-interface localization engine.

Keep these files together. `revision_manager.js` and `qc_plus.js` remain safety-critical runtime sidecars. `localization.js` is UX-only: the S8 panel must fall back deterministically to English if localization data cannot be loaded, without weakening Build/QC/Revision validation.

## First development test

1. Keep `CutBridge.jsx`, `revision_manager.js`, `qc_plus.js`, and `localization.js` in the same directory.
2. In After Effects, choose **File > Scripts > Run Script File...**.
3. Select `CutBridge.jsx`.
4. Confirm the panel opens in Japanese by default and can switch explicitly to English.
5. Import a CutBridge package, build the comp, run QC, and smoke-test revision behavior in both locales.

`Run Script File...` is the least ambiguous first test because Adobe script-install paths vary by After Effects version and operating system.

## Dockable panel

For a dockable ScriptUI panel:

1. Copy **all four** files into the After Effects `Scripts/ScriptUI Panels` directory for the installed version.
2. Restart After Effects.
3. Open **Window > CutBridge**.

Do not separate the runtime sidecars from the JSX panel file.

## Japanese / English UX

S8 uses Japanese as the first-class/default display language and English as a deterministic fallback. The locale switch changes user-facing panel labels, status text, prompts, and QC guidance only. It must not change:

- `CBQ-*` diagnostic identifiers;
- manifest fields or package names;
- CutBridge managed tags/ownership identity;
- Build, QC, or revision safety decisions.

Japanese diagnostic text may retain canonical English technical detail for support/debug compatibility.

## Validation boundary

S7 native validation passed in real Adobe After Effects 2026 (26.3 Build 87) on Windows 11, covering QC+, ownership failures, missing sidecar fail-closed behavior, revision compatibility/incompatibility guards, and artist-state preservation.

S8 automated tests verify the JA/EN localization contract, stable diagnostic identifiers, fallback behavior, packaging, and compatibility with the existing S5–S7 regression suite. Real S8 After Effects JA/EN panel behavior must still be validated separately on the exact frozen S8 candidate before S8 is merged.

Automated Node/host-shaped tests are regression evidence; they are **not native After Effects certification**. See `../../docs/QUICK_START.md`, `../../docs/TEST_PLAN.md`, `../../docs/S6_REVISION_CONTRACT.md`, and `../../docs/S7_QC_PLUS_CONTRACT.md` for the existing safety boundaries.
