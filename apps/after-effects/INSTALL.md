# CutBridge for After Effects — Installation

CutBridge S8 development packages use **four adjacent runtime files**:

- `CutBridge.jsx` — panel, package import, Build, QC, revision adapter, and locale-aware UI binding.
- `revision_manager.js` — S6 non-destructive revision-manager core.
- `qc_plus.js` — S7 deterministic QC+ diagnostic engine.
- `localization.js` — S8 Japanese-first / English-fallback localization engine.

**Keep these files together.** All four files should remain adjacent for normal development use. `revision_manager.js` and `qc_plus.js` are safety-critical runtime sidecars. `localization.js` is UX-only: if it cannot be loaded, the panel must fall back deterministically to English without weakening Build/QC/Revision validation.

## First development test

1. Keep `CutBridge.jsx`, `revision_manager.js`, `qc_plus.js`, and `localization.js` in the same directory.
2. In After Effects choose **File > Scripts > Run Script File...**.
3. Select `CutBridge.jsx`.
4. Confirm the panel opens in Japanese by default and can switch explicitly to English.
5. Load a representative CutBridge package, Build, run QC, and smoke-test compatible revision behavior.

`Run Script File...` is the least ambiguous first test because Adobe script-install paths vary by After Effects version and operating system.

## Dockable panel

1. Copy all four files into the installed After Effects version's `Scripts/ScriptUI Panels` directory.
2. Restart After Effects.
3. Open **Window > CutBridge**.

Do not separate the runtime sidecars from the JSX panel file.

## Japanese / English UX

S8 uses Japanese as the first-class/default display language and English as a deterministic fallback/support language.

Locale switching may change user-facing labels, prompts, status text, QC explanation, and revision guidance. It must not change:

- `CBQ-*` diagnostic identifiers;
- manifest fields or package names;
- CutBridge managed tags/ownership identity;
- Build, QC, or revision safety decisions;
- unrelated AE project objects.

Japanese diagnostic text may retain canonical English technical detail for support/debug compatibility.

## Missing `localization.js` fallback

If only `localization.js` is missing/invalid:

- the effective UI must fall back to English;
- the visible language selector must also show English;
- persisted Japanese preference data must not be destructively rewritten merely because fallback is active;
- fallback must create/delete/move/re-tag no project objects;
- Build/QC/Revision safety must remain fail-closed.

Do not treat missing `revision_manager.js` or `qc_plus.js` as equivalent to missing localization. Those files participate in product safety behavior and their absence must not silently downgrade the workflow.

## Native validation status

S7 native validation passed in real Adobe After Effects and found/repaired native ExtendScript/revision-state defects before integration.

S8 final targeted native retest passed on exact candidate `f477b745cc600b85708b63d059d6c4eaed9f0249` in **Adobe After Effects 2026 v26.3.0 Build 87**.

The repaired S8 test verified:

- product ZIP checksum matched the expected candidate artifact;
- Japanese locale persistence;
- missing-only-`localization.js` fallback rendered coherent English UI;
- the visible selector synchronized to English;
- project item count remained unchanged during fallback;
- restoring the exact sidecar returned the UI to Japanese;
- representative guards remained fail-closed.

S8 merged to `develop` as `368b977582feadc26543825b4d31ffd5f6266a4f`; post-merge CI `34380737455` passed.

## Release boundary

This native evidence establishes the tested S8 candidate behavior; it does **not** authorize publication of v0.2.3 or certify every OS/AE configuration.

There is currently no GitHub Release/tag. Release governance issue #18 and the broader release checklist remain required before RC/stable publication.

See:

- `../../docs/QUICK_START.md`
- `../../docs/QUICK_START_JA.md`
- `../../docs/TEST_PLAN.md`
- `../../docs/COMPLETION_STATUS.md`
- `../../docs/ROADMAP.md`
