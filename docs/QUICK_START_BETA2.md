# CutBridge v0.2.3-beta.2 Usability Quick Start

Status: **repair-candidate guidance; not a release claim**

This guide documents the usability contract being prepared for the next material-source candidate. It does not replace release governance, host compatibility evidence, or S14 Japanese target-user validation.

Japanese: [QUICK_START_BETA2_JA.md](QUICK_START_BETA2_JA.md)

## Core workflow

`Prepare cut → Validate Cut → fix ERRORs / review WARNINGs → Build Package → render sequences → Load Package in AE → Build → QC+ → new Version for revisions`

## Blender pass controls

### Beauty

The normal Combined/Image render and the main picture sequence. Enable it when After Effects needs the primary rendered image.

### Line

A Blender Freestyle line-art pass. Line requires:

1. Freestyle enabled for the scene/render setup;
2. Freestyle enabled for the active View Layer;
3. Freestyle **As Render Pass** enabled;
4. an actual `Freestyle` output on the active Render Layers node.

If any of those conditions is missing, **Validate Cut returns an ERROR before Build Package**. You cannot safely continue with Line enabled. Configure Freestyle correctly or disable Line.

### Shadow

A renderer-dependent standalone Shadow pass. In Blender 5.2, the current CutBridge Shadow contract is validated against EEVEE's Shadow Render Layers output. Cycles does not expose the same standalone Shadow output required by this contract.

If Shadow is selected but the active renderer/View Layer cannot expose the expected output, **Validate Cut returns an ERROR before Build Package**. Switch to a supported renderer/View Layer setup or disable Shadow.

### Depth

Camera-distance data used for depth-based compositing/effects.

- **OpenEXR:** recommended when accurate depth values matter.
- **PNG/TIFF:** CutBridge may continue, but validation shows a WARNING because precision can be reduced.

A Depth format warning is not an error.

## Four-pass workflow

The requested `Beauty + Line + Shadow + Depth` combination is supported by the current Blender 5.2.1 automated mapping evidence **with EEVEE**, provided Line/Freestyle requirements are satisfied.

The regression matrix also exercises Beauty only, Beauty+Line, Beauty+Shadow, Depth PNG, Depth OpenEXR, and Beauty+Line+Shadow.

See [FOUR_PASS_WORKFLOW_BETA2.md](FOUR_PASS_WORKFLOW_BETA2.md) for the exact automated evidence boundary.

## Sequence Format

The v0.2.3 manifest/preset architecture has one package-level Sequence Format. The selected format currently applies to **every enabled pass**.

Per-pass formats are not half-implemented in this candidate. A backward-compatible design is tracked separately because it affects presets, Blender compositor output, manifest semantics, package integrity, AE sequence import, and historical compatibility.

## Studio Preset

Studio Presets are declarative data profiles that can control naming, folders, pass selection, sequence format, version token, and AE comp naming.

- **Manual:** pass and Sequence Format controls are editable.
- **Preset-controlled modes:** managed values are read-only to preserve deterministic package identity.

Custom presets must validate before Build Package.

## Validate Cut vs Build Package

### Validate Cut

Validation answers four questions for important findings:

- **What happened?**
- **Why did it happen?**
- **Can I continue?**
- **How do I fix it?**

Severity contract:

- **INFO:** informational; no action necessarily required.
- **WARNING:** workflow may continue after the consequence is understood.
- **ERROR:** workflow cannot safely continue until repaired.

Stable technical codes remain visible for support/debugging but are not the first wording the user must interpret.

Validation is preflight only. It does not create the package.

### Build Package

Build configures CutBridge-managed compositor output mapping and creates the deterministic versioned package only after preflight passes.

Defense-in-depth remains in the Build path: if host state changes or validation is bypassed, direct Render Layers socket checks still fail closed before package directories are created.

Artist-owned compositor state must remain intact. CutBridge owns only its managed mapping namespace.

### After Build Package: render-ready state

Once the current package contains render/user payload, **Build Package remains protected and will not overwrite the same Version**. That protection is action-specific: it does not block Blender's Render Animation command.

If the existing `cutbridge.json` still matches the current cut/render contract, general Validation Status reports **Package Already Built — Ready to Render** (`PACKAGE_RENDER_READY`). Continue Render Animation and do not run Build Package again for that same Version.

If the package already contains payload but the current cut/render settings no longer match its manifest, validation reports `PACKAGE_STATE_MISMATCH`. Restore the original settings or increment Version before creating new output; do not mix changed settings into the existing revision.

## Version workflow

`Version` is the package revision number.

- first handoff: V001;
- next revision: V002;
- next revision: V003.

Do not overwrite an existing same-version package that contains render/user payload. Increase Version for a new revision so older packages can coexist. If the same Version is already built and still matches the current settings, continue rendering that package without rebuilding it.

## Package Output

The Package Output field selects the parent directory for versioned CutBridge packages.

A Blender `//` path is relative to the saved `.blend` file. Save the `.blend` before relying on a relative output path.

CutBridge checks the target before Build and fails closed on protected same-version data, unsafe targets, or collisions.

## Camera / 3D handoff

The active Blender scene camera is required metadata for the cut.

The existing producer-side Camera/3D sample-data path remains **experimental and intentionally non-release-facing** in the normal Blender panel until the exact candidate's native AE Camera/3D Null workflow is fully validated. Do not treat the hidden producer control as a general Blender↔AE scene-sync feature.

## After Effects panel

`CutBridge.jsx` already supports both:

- docked ScriptUI Panel usage when installed under `Scripts/ScriptUI Panels`;
- palette/undocked execution when run as a script.

Opening the panel does **not** build or modify CutBridge-managed project state. Explicit user action is required.

Current workflow actions:

- **Load Package:** choose/read `cutbridge.json` and update package status.
- **Build:** create/reuse only verified CutBridge-managed folders, footage, comp, and layers according to the manifest.
- **QC+:** inspect package/project state and report deterministic findings without silently repairing ownership.
- **Revision:** apply only compatible source-oriented revision updates to verified managed state.

CutBridge-managed objects are identified by CutBridge ownership metadata. Artist-owned objects must not be adopted merely because their names or sources look similar.

The AE panel's visual hierarchy/contextual-help redesign is still part of the beta.2 repair campaign and requires native-host rerun before a support claim.

## Compatibility boundary

Do not infer host support from this guide.

See [COMPATIBILITY_CAMPAIGN_BETA2.md](COMPATIBILITY_CAMPAIGN_BETA2.md) for the required Blender 4.2/4.5/5.2 and AE 2020–2026 campaign. Older AE versions remain unverified until real-host evidence exists.

## Release boundary

This repair work does not authorize v0.2.3 publication. The sequence remains:

`S14 PASS → governance resolved → exact RC freeze → exact RC CI → deliberate main promotion → promoted-main CI → exact authorization tuple → publication → independent artifact verification → distribution/update verification`

Until those gates are genuinely complete, CutBridge is **NOT RELEASE READY**.