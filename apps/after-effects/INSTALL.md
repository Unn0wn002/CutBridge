# CutBridge for After Effects — Installation

CutBridge After Effects packages use **four adjacent runtime files**:

- `CutBridge.jsx` — panel, package import, Build, QC, revision adapter, localization binding, and S10C managed camera/3D Null reconstruction.
- `revision_manager.js` — S6 non-destructive revision-manager core.
- `qc_plus.js` — S7 deterministic QC+ diagnostic engine.
- `localization.js` — S8 Japanese-first / English-fallback localization engine.

**Keep these files together.** All four files should remain adjacent for normal use. `revision_manager.js` and `qc_plus.js` are safety-critical runtime sidecars. `localization.js` is UX-only: if it cannot be loaded, the panel must fall back deterministically to English without weakening Build/QC/Revision validation.

## Install and open the dockable panel (recommended)

1. Verify the ZIP's SHA-256 against both `SHA256SUMS.txt` and `release-metadata.json`, then extract it to a fresh directory.
2. Copy **all four** runtime files from that same package into your installed After Effects version's `Scripts/ScriptUI Panels` directory. On Windows the usual location is `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\Scripts\ScriptUI Panels`; use the corresponding folder for your version. On macOS use the installed application's `Scripts/ScriptUI Panels` folder. Installation may require normal administrator access.
3. Restart After Effects and open **Window > CutBridge** (some hosts display the `.jsx` suffix).
4. Drag the CutBridge tab into your workspace to dock it. Resize it as needed; use Japanese or English from the language selector. Save your workspace using AE's normal workspace controls if desired.
5. Load `cutbridge.json`, Build, then run QC+. Routine Build/QC results appear in the selectable, scrollable **Results** field. Review warnings and `CBQ-*` codes there. Revision confirmations and blocking operation errors still use dialogs.

Do not mix sidecars from different packages. Missing safety sidecars must not silently downgrade validation. Host compatibility and native acceptance remain limited to the exact evidence in the tagged readiness record.

## Optional floating fallback

Keep the same four files together in an extracted directory. Choose **File > Scripts > Run Script File...**, then select `CutBridge.jsx`. This opens a resizable floating palette. It does not install the panel into the Window menu. Avoid opening multiple CutBridge instances for the same project.

## Remove or update

Close CutBridge and After Effects. Remove only `CutBridge.jsx`, `revision_manager.js`, `qc_plus.js`, and `localization.js` from the folder where you installed them, then restart AE. For an update, replace all four together with the verified new package while AE is closed. Never remove artist projects, source packages, renders, or unrelated scripts. Existing AE project content remains in the saved project. For floating use, remove only the extracted CutBridge runtime copy when no longer needed.

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
- Camera Position, Point of Interest derived from `forward`, and Zoom at sample times;
- Null Position and supplied Scale at sample times.

Camera `up`/basis and Null basis data are serialized but are not applied to AE Orientation or rotation channels. Camera roll and Empty rotation are not reconstructed. QC+ checks manifest/sequence/comp/managed render state and obsolete managed tags; it does not check expected Camera/Null completeness, channel values/keyframes, or projection parity. Inspect the supported channels separately rather than treating a clean QC report as 3D transform acceptance.

CutBridge validates the handoff contract before project mutation. Ownership is identity-based, not visible-name-only. Repeated Build must be idempotent. A same-name unmanaged artist camera/null must cause fail-closed collision handling instead of adoption or overwrite.

S10C does **not** provide geometry transfer, light transfer, bones, arbitrary Blender hierarchy recreation, or general scene synchronization.

See `../../docs/HANDOFF_3D.md` in the source tree corresponding to the package tag. Source-tree `../../docs/` paths below are reference locations; those files are not included in the AE ZIP. The release-readiness link at the end of this guide is pinned to that tag during packaging.

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

These historical measurements cover the recorded fixture in the named real host. The projection measurement is separate from QC+ and does not establish camera-roll or Empty-rotation support. This evidence does **not** certify every After Effects 2024–2026 version, OS, camera configuration, production workflow, or later candidate package.

## Validation boundary

Automated Node/host-shaped tests protect contract and adapter behavior but are not native After Effects certification. Real-host evidence must remain scoped to the exact host/workflow that was actually exercised.

The remaining broader release-target Blender → package → AE campaign belongs to S12 and release readiness, not to this installation guide.

## Evidence and release-status boundary

The native evidence above is bounded to the named hosts and workflows. It does not establish blanket compatibility, representative-user usability, or broad production readiness.

This installation guide intentionally does not encode whether a particular tag is current, authorized, or published. For the exact identity and publication state of a release, use the release's adjacent `release-metadata.json` and `SHA256SUMS.txt` assets together with the corresponding [GitHub Release page](https://github.com/Unn0wn002/CutBridge/releases). The [release-readiness record](https://github.com/Unn0wn002/CutBridge/blob/develop/docs/RELEASE_READINESS.md) documents current validation scope; packaged copies pin this link to their source tag.

See:

- `../../docs/QUICK_START.md`
- `../../docs/QUICK_START_JA.md`
- `../../docs/HANDOFF_3D.md`
- `../../docs/COMPATIBILITY.md`
- [Release readiness](https://github.com/Unn0wn002/CutBridge/blob/develop/docs/RELEASE_READINESS.md)
- `../../docs/TEST_PLAN.md`
- `../../docs/COMPLETION_STATUS.md`
- `../../docs/ROADMAP.md`
