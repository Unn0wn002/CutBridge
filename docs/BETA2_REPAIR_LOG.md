# v0.2.3-beta.2 Repair Log

Status: **WORK IN PROGRESS**  
Release status: **NOT RELEASE READY**

This log records the current repair findings without rewriting historical beta.1 evidence.

| Finding | Severity | Current state | Evidence / action |
|---|---|---|---|
| LINE could pass Validate but fail later when Freestyle Render Layers output was unavailable | MAJOR | REPAIRED IN BRANCH / CI REQUIRED | Added non-destructive Freestyle socket preflight, actionable EN/JA diagnostic, Build-side defense-in-depth retained, no-partial-package/state-preservation regression. |
| Shadow capability was checked only by View Layer attribute, allowing unsupported renderer state to reach Build | MAJOR | REPAIRED IN BRANCH / CI REQUIRED | Added Shadow Render Layers capability probe with restored View Layer flag; Cycles+Shadow now fails Validate; EEVEE is used for the Blender 5.2 four-pass proof. |
| Depth warning exposed implementation terminology before user consequence | MINOR | REPAIRED IN BRANCH / CI REQUIRED | Added user-facing Depth Format Warning explaining precision, OpenEXR recommendation, and that continuation is allowed. |
| Diagnostics did not consistently answer WHAT / WHY / CAN CONTINUE / FIX | MAJOR UX | REPAIRED IN BLENDER BRANCH / CI REQUIRED | Added structured EN/JA diagnostic presentation while retaining stable support codes/canonical technical text. AE diagnostic presentation still requires native-panel UX follow-up. |
| Important Blender controls lacked contextual help | MINOR UX | REPAIRED IN BRANCH / CI REQUIRED | Added per-control contextual `?` help for passes, format, preset, Version, camera metadata, output path, Validate, and Build. |
| Four-pass behavior was not explicitly proven | MAJOR VALIDATION | REPAIRED FOR BLENDER 5.2 AUTOMATED SCOPE / NATIVE RERUN REQUIRED | Added Beauty/Line/Shadow/Depth combination matrix, manifest/path/format assertions, and renderer-boundary tests. |
| Per-pass output formats requested but current schema is package-global | MAJOR DESIGN RISK if rushed | DEFERRED BY DESIGN | Preserved existing global-format contract; improved Depth guidance; opened a bounded backward-compatible follow-up issue instead of half-implementing schema/AE changes. |
| AE interaction is already dockable but flat and lacks contextual help/status hierarchy | MINOR/MAJOR UX pending target-user observation | OPEN | Existing `CutBridge.jsx` is a dockable `Panel`/palette architecture and does not mutate project state on open. UI hierarchy/contextual-help redesign remains unfinished and needs a safe source-edit path plus native AE rerun. |
| AE 2020–2023 support was requested for evaluation without real-host evidence | COMPATIBILITY GATE | UNVERIFIED | Explicit compatibility campaign keeps 2020–2023 UNVERIFIED; no support claim is allowed before real-host evidence. |
| Existing AE 2026 native evidence predates material beta.2 source changes | RELEASE-SAFETY GATE | LEGACY/BOUNDED ONLY | Existing evidence remains historical/legacy evidence; exact beta.2 candidate must be rerun and frozen separately. |
| S14 representative Japanese target-user validation | RELEASE BLOCKER | OPEN | Must be executed by real representative users after the affected beta.2 repairs are frozen. No simulated evidence is acceptable. |
| Release governance / authorization | RELEASE BLOCKER | OPEN | `release-authorization.json` remains unapproved; no release/tag/publication/main promotion is authorized by this repair work. |

## Files introduced/updated in this repair branch

Blender repair/UX:

- `apps/blender/cutbridge/line_preflight.py`
- `apps/blender/cutbridge/shadow_preflight.py`
- `apps/blender/cutbridge/diagnostics.py`
- `apps/blender/cutbridge/help_content.py`
- `apps/blender/cutbridge/help_ops.py`
- `apps/blender/cutbridge/operators.py`
- `apps/blender/cutbridge/ui.py`
- `apps/blender/cutbridge/localization.py`
- `apps/blender/cutbridge/__init__.py`

Regression coverage:

- `tests/test_line_preflight_52.py`
- `tests/test_four_pass_workflow_52.py`
- `tests/test_context_help.py`
- `tests/test_beta2_usability_docs.py`
- updated `tests/test_s8_blender_localization.py`

Documentation/evidence planning:

- `docs/COMPATIBILITY_CAMPAIGN_BETA2.md`
- `docs/FOUR_PASS_WORKFLOW_BETA2.md`
- `docs/QUICK_START_BETA2.md`
- `docs/QUICK_START_BETA2_JA.md`
- this repair log

## Candidate boundary

These are material source changes. They invalidate any attempt to present beta.1 as unchanged-source evidence for the repaired product. A future `v0.2.3-beta.2` may be prepared only after the repair scope is complete, exact-head CI is green, required artifacts are deterministically rebuilt and hashed, candidate docs/evidence templates are generated, and the exact frozen candidate is identified.

No GitHub Release is authorized by this log.