# Roadmap

## v0.2 — Blender Render Mapping
- Map package passes to Blender render outputs / View Layers.
- Set deterministic output paths automatically.
- Harden Blender Extension packaging.
- Add environment/version diagnostics.

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
