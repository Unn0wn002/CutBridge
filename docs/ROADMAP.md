# Roadmap

Status reconciled on 2026-09-06. Versions 0.2.1–0.2.3 were used for registration and manifest/test fixes; render mapping was not delivered by those fixes. Future milestones below are plans, not completion claims.

## Implemented foundation — v0.2.0 through v0.2.3 (unreleased)
- Harden Blender Extension packaging and manifest metadata.
- Add central version constants.
- Add environment/version/platform diagnostics.
- Add LTS-first compatibility policy.
- Add Stable/Beta/Development update discovery.
- Add deterministic release builder, checksums, and release metadata.
- Keep private source control separate from distribution/update hosting.

## Next — Blender Render Mapping (version to be assigned)
- Map package passes to Blender render outputs / View Layers.
- Set deterministic output paths automatically.
- Validate pass/output configuration before render.

## Before Revision Manager — AE handoff contract hardening
S4 repair is in PR #12, pending authoritative CI and independent review. S5 is not started. GUI/user validation remains separate.
- Gate manifest schema versions explicitly.
- Respect optional passes.
- Check exact sequence frame coverage.
- Reconcile stale AE MVP labels.

## v0.3 — Revision Manager
- Detect newer cut revisions.
- Replace only CutBridge-managed footage in After Effects.
- Preserve manual effects, masks, adjustment layers, and compositor work.

## v0.4 — QC+
- Missing-frame scanner.
- FPS/duration/resolution mismatch diagnostics.
- Pass/version/naming validation.
- Actionable fixes.

## v0.5 — Studio Presets
- Preset-driven naming conventions.
- Pass mappings and AE layer rules.
- Avoid hard-coding one studio workflow.

## v0.6 — Japanese UX
- English/Japanese UI switching.
- Japanese quick-start documentation.
- Terminology validation with target users.

## v0.7 — Camera / Null Handoff
- Camera metadata/export adapter.
- Tracked empties/null transfer where technically appropriate.

## v0.8 — Client Validation Build
- Real workflow timing test.
- Acceptance checklist.
- Error/rework comparison against manual handoff.

## 1.0 goal
A production-oriented Blender → After Effects handoff tool with deterministic packaging, revision-safe updates, QC, studio presets, documented compatibility, and a controlled update channel.
