# Roadmap

Status reconciled during S6 repair after S5 integration. Versions 0.2.1–0.2.3 remain unreleased development history; milestone labels below describe product sessions rather than guaranteed release numbers unless explicitly assigned.

## Implemented foundation — v0.2.0 through v0.2.3 (unreleased)
- Harden Blender Extension packaging and manifest metadata.
- Add central version constants and release-time version drift checks.
- Add environment/version/platform diagnostics.
- Add LTS-first compatibility policy.
- Add Stable/Beta/Development update discovery.
- Add deterministic release builder, ZIP validation, checksums, and release metadata.
- Keep private source control separate from distribution/update hosting.
- Add Blender 5.2.1 automated RNA lifecycle and package-generation coverage.

## Completed S2 — Blender Render Mapping
- Map logical BEAUTY / LINE / SHADOW / DEPTH package passes to supported Blender render/View Layer/compositor outputs.
- Configure deterministic output directories and sequence patterns.
- Preserve unrelated artist compositor nodes and commit CutBridge mapping transactionally.
- Validate renderer/View Layer capability before committing replacement mapping.

## Completed S3 — Blender Production Hardening
- Add actionable validation UI and package-target safety checks.
- Prevent silent same-version overwrite when render/user payload exists.
- Preserve V001 / V002 / V003 package coexistence.
- Harden package integrity, UTF-8/Japanese metadata, and filesystem-safe naming behavior.

## Completed S4 — AE Handoff Contract Hardening
- Gate manifest schema and schema version explicitly.
- Enforce finite integer frame semantics and a consistent non-negative export policy.
- Respect required versus optional passes.
- Check exact expected sequence frame coverage and diagnose extra/mis-padded matches.
- Harden package-relative path handling and reject unsafe aliases/escapes.
- Replace executable legacy JSON fallback with a data-only parser.
- Reconcile stale AE MVP/version labeling and enforce release-time AE version consistency.

Real AE GUI/end-to-end behavior remains a separate manual validation gate.

## Completed S5 — AE Import & Composition Reliability
- Harden malformed-package and manifest-loading behavior.
- Make composition/folder/layer creation deterministic and safe across repeated imports.
- Verify FPS, resolution, pixel aspect, duration, layer ordering, Japanese/Unicode/Windows paths, and actionable failures.
- Expand runtime-independent regression coverage without claiming native AE GUI execution.

## In progress S6 — Non-Destructive Revision Manager
- PR #15 is blocked pending native AE adapter/panel/persistent-state/release integration and independent review. The tested revision core alone does not complete S6.
- Detect newer compatible cut revisions.
- Replace only CutBridge-managed footage/sources where technically safe.
- Preserve manual effects, masks, transforms, parenting, timing, layers, and compositor work where possible.
- Surface compatibility warnings and require confirmation for risky changes.

## S7 — QC+
- PASS / WARNING / ERROR diagnostics for package, manifest, pass, sequence, version, and inspectable AE state.
- Missing/extra-frame, FPS/duration/resolution/pixel-aspect, naming, and revision compatibility checks.
- Actionable remediation text without dangerous automatic fixes.

## S8 — Japanese-First UX
- Maintainable English/Japanese user-facing string architecture.
- Japanese quick-start documentation and terminology pass.
- English fallback and explicit native-user validation boundary.

## S9 — Studio Presets
- External/configurable naming, folder, pass, layer-order, output-format, and version-pattern presets.
- Safe schema/defaults with no arbitrary code execution or confidential studio preset distribution.

## S10 — Camera / Null Handoff Investigation
- Research Blender/AE coordinate, axis, handedness, units, camera/lens/FOV/sensor, parenting, null/empty, and frame-timing constraints.
- Ship only a minimal reliable subset with tests; defer anything not technically established.

## S11 — QA / Docs / Release Engineering
- Reconcile full CI/test matrix, release packaging, compatibility, security, install/usage/revision/QC/troubleshooting documentation, and distribution metadata.
- Keep the private source repository separate from customer update delivery.

## S12 — End-to-End Validation Harness
- Maintain legal/original/synthetic fixtures.
- Provide a deterministic manual Blender 5.2.1 → After Effects checklist including V001→V002 revision preservation.
- Never infer GUI success from headless tests.

## S13 — Manual-Finding Repair
- Run only when real manual Blender/AE failure evidence exists.
- Do not invent defects to keep development moving.

## S14 — Target-User Validation Prep
- Prepare Japanese-oriented usability, timing, error, and rework validation protocol plus feedback templates.
- Do not fabricate participants or results.

## Stable-release goal
A production-oriented Blender → After Effects handoff tool with deterministic packaging, revision-safe updates, QC, studio presets, documented compatibility, controlled distribution/update architecture, green automated gates, and recorded real-app/manual validation appropriate to the release claim.
