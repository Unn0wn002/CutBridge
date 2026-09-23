# CutBridge for After Effects — Installation

CutBridge v0.2.4 development packages use **four adjacent runtime files**:

- `CutBridge.jsx` — panel, package import, Build, QC, revision adapter, localization binding, and S10C managed camera/3D Null reconstruction.
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
6. If the package contains a valid S10C `handoff_3d` block, confirm the CutBridge-managed camera/3D Null subset is reconstructed without adopting unmanaged same-name artist layers.

`Run Script File...` is the least ambiguous first test because Adobe script-install paths vary by After Effects version and operating system.

## Dockable panel

1. Copy all four files into the installed After Effects version's `Scripts/ScriptUI Panels` directory.
2. Restart After Effects.
3. Open **Window > CutBridge**.

Do not separate the runtime sidecars from the JSX panel file.

## Japanese / English UX

Japanese is the first-class/default display language and English is the deterministic fallback/support language.

Locale switching may change user-facing labels, prompts, status text, QC explanation, and revision guidance. It must not change:

- `CBQ-*` diagnostic identifiers;
- manifest fields or package names;
- `handoff_3d` values;
- CutBridge managed tags/ownership identity;
- Build, QC, revision, or S10C reconstruction safety decisions;
- unrelated AE project objects.

Japanese diagnostic text may retain canonical English technical detail for support/debug compatibility.

## Missing `localization.js` fallback

If only `localization.js` is missing/invalid:

- the effective UI must fall back to English;
- the visible language selector must also show English;
- persisted Japanese preference data must not be destructively rewritten merely because fallback is active;
- fallback must create/delete/move/re-tag no project objects;
- Build/QC/Revision/S10C safety must remain fail-closed.

Do not treat missing `revision_manager.js` or `qc_plus.js` as equivalent to missing localization. Those files participate in product safety behavior and their absence must not silently downgrade the workflow.

## S10C 3D handoff boundary

When `cutbridge.json` contains a valid optional `handoff_3d` block, S10C can reconstruct the supported subset as:

- one CutBridge-managed perspective camera;
- CutBridge-managed 3D Null layers for serialized Blender Empties;
- baked position/orientation/projection timing from the producer contract.

CutBridge validates the handoff contract before project mutation. Ownership is identity-based, not visible-name-only. Repeated Build must be idempotent. A same-name unmanaged artist camera/null must cause fail-closed collision handling instead of adoption or overwrite.

S10C does **not** provide geometry transfer, light transfer, bones, arbitrary Blender hierarchy recreation, or general scene synchronization.

See `../../docs/HANDOFF_3D.md`.

## Native validation status

### S7 / S8

S7 native validation passed in real Adobe After Effects and found/repaired native ExtendScript/revision-state defects before integration.

S8 targeted native retest passed on exact candidate `f477b745cc600b85708b63d059d6c4eaed9f0249` in **After Effects 2026 (26.3 Build 87)**, including Japanese locale persistence and deterministic English fallback when only `localization.js` was missing.

### S10C

S10C native reconstruction/parity validation passed in **Adobe After Effects 2026 Build 87 (`26.3x87`) on Windows 11** using Blender 5.2.1 LTS-produced handoff data.

Recorded S10C evidence:

- managed camera + 3D Null reconstruction: PASS;
- maximum measured 2D projection error: `0.00018066 px`;
- acceptance threshold: `<= 0.05 px`;
- QC+: 10/10 PASS;
- idempotent repeated Build: 0 duplicate managed layers;
- unmanaged camera/null name collisions: fail-closed PASS;
- project persistence: PASS.

This validates the bounded S10C scope in the named real host. It does **not** certify every After Effects 2024–2026 version, OS, camera configuration, or production workflow.

## Validation boundary

Automated Node/host-shaped tests protect contract and adapter behavior but are not native After Effects certification. Real-host evidence must remain scoped to the exact host/workflow that was actually exercised.

The remaining broader release-target Blender → package → AE campaign belongs to S12 and release readiness, not to this installation guide.

## Release boundary

The native evidence above does **not** authorize publication of v0.2.4. Stable v0.2.3 remains published and immutable; v0.2.4 development starts with fail-closed release authorization and requires its own exact-candidate validation before any future release.

See:

- `../../docs/QUICK_START.md`
- `../../docs/QUICK_START_JA.md`
- `../../docs/HANDOFF_3D.md`
- `../../docs/COMPATIBILITY.md`
- `../../docs/RELEASE_READINESS.md`
- `../../docs/TEST_PLAN.md`
- `../../docs/COMPLETION_STATUS.md`
- `../../docs/ROADMAP.md`
