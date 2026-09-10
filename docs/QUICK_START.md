# CutBridge Quick Start

This guide describes the **v0.2.3 unreleased development workflow through S10C**.

CutBridge connects one Blender animation cut to After Effects through deterministic render-output mapping, a versioned package, `cutbridge.json`, managed AE project state, QC+, compatible source-only revision updates, Japanese-first UX, data-only Studio Presets, and the bounded optional 3D camera/Null handoff validated in S10C.

Intended flow:

`Blender metadata + optional Studio Preset + optional 3D handoff → Validate Cut → deterministic render mapping/package → render sequences → AE Import/Build → managed camera/Null reconstruction when handoff_3d is present → QC+ → compatible revision update`

Japanese guide: [QUICK_START_JA.md](QUICK_START_JA.md).

Studio Preset authoring reference: [STUDIO_PRESETS.md](STUDIO_PRESETS.md).

3D handoff reference: [HANDOFF_3D.md](HANDOFF_3D.md).

## Development status

S1–S8 established the deterministic handoff, ownership/revision/QC contracts, and Japanese-first UI. S9 added validated declarative Studio Presets. S10A defined the camera/Null coordinate, timing, and projection contract; S10B added the optional evaluated-world Blender producer; S10C added bounded managed After Effects camera/3D Null reconstruction and passed native AE projection-parity validation.

This is development evidence, not stable-release authorization. There is no release tag or GitHub Release, and `release-authorization.json` remains fail-closed. See [RELEASE_READINESS.md](RELEASE_READINESS.md).

## 1. Install the Blender extension

For development testing, install a verified CutBridge Blender ZIP built from the exact source candidate you intend to test.

1. Open a supported Blender version. Minimum declared runtime is 4.2.0; current authoritative automated runtime testing includes Blender 5.2.1 LTS.
2. Open Preferences and use the appropriate **Install from Disk** / extension installation action.
3. Select the CutBridge Blender ZIP and enable it.
4. In a 3D View, open the `N` sidebar and select **CutBridge**.
5. Japanese is the first-class/default UI language; use the language control to switch to English when needed.

Meeting the minimum Blender version alone is not a certification claim. See [COMPATIBILITY.md](COMPATIBILITY.md).

## 2. Prepare the Blender cut

Before validation:

1. Save the `.blend` file.
2. Set an active scene camera.
3. Set FPS and resolution.
4. Set the export frame range.
5. Enter Project / Episode / Scene / Cut / Take / Version metadata.
6. Select the package output directory.
7. Choose a **Studio Preset Mode**.

### Studio Preset modes

**Manual** is the backward-compatible default. It keeps the pre-S9 pass toggles and Sequence Format controls directly editable and preserves the canonical package identity such as:

`PROJECT_EP01_SC010_C012_T01_V001`

**CutBridge Default** uses the built-in declarative preset and reproduces the default CutBridge conventions through the S9 preset pipeline.

**Custom JSON** loads one validated UTF-8 Studio Preset file. Choose the JSON file in the N-panel, then run Validate Cut before Build Package.

A Studio Preset can control:

- package naming template;
- render / preview / camera folder roles;
- logical pass order and required/optional flags;
- sequence filename template;
- PNG / OpenEXR / TIFF output format;
- version-token prefix and padding;
- After Effects comp naming.

Studio Presets are data only. After Effects does not load the preset file; Blender resolves it into `cutbridge.json`.

See [STUDIO_PRESETS.md](STUDIO_PRESETS.md) for the schema, allowed placeholders, validation rules, and safe example.

### Frame-range rule

CutBridge supports export ranges beginning at frame `0` or later. Negative/preroll export ranges are rejected at Blender/schema/AE boundaries. CutBridge does not silently renumber animation; rebase the export range before package creation.

## 3. Optional 3D camera / Empty handoff

The S10 3D handoff is **optional and disabled by default**. It is still an engineering opt-in rather than a normal N-panel workflow.

To enable producer data from Blender Python:

```python
bpy.context.scene.cutbridge.handoff_3d_enabled = True
bpy.context.scene.cutbridge.handoff_3d_pixels_per_blender_unit = 100.0
```

Mark only the Blender Empties that should become managed AE 3D Nulls:

```python
empty["cutbridge_handoff_3d"] = True
```

Supported producer subset:

- active perspective camera;
- square pixels;
- zero camera shift;
- explicitly marked Empties;
- baked evaluated-world samples.

Unsupported camera/transform cases fail closed. Parenting, constraints, and drivers may influence the evaluated Blender world transform, but CutBridge does not recreate the Blender hierarchy in AE.

See [HANDOFF_3D.md](HANDOFF_3D.md) before enabling this workflow.

## 4. Validate Cut

Run **Validate Cut**.

Validation covers identifiers, camera, FPS, resolution, frame range, Studio Preset validity, selected/resolved passes, output target, renderer/View Layer capability, package-target safety, and—when 3D handoff is enabled—the supported S10 producer contract.

- `ERROR` means stop and fix the problem.
- Warnings require review before proceeding.
- Stable machine-facing validation semantics do not change when switching JA/EN.
- Invalid custom preset or unsupported 3D handoff data fails closed before package creation.

Preset-specific stable codes include `PRESET_JSON_INVALID`, `PRESET_SCHEMA_INVALID`, `PRESET_SCHEMA_UNSUPPORTED`, `PRESET_FIELD_INVALID`, and `PRESET_PATH_UNSAFE`.

## 5. Render-output mapping

CutBridge configures deterministic compositor output mapping for the resolved logical passes.

Safety rules:

- CutBridge-owned compositor state uses the `CUTBRIDGE_` namespace.
- Unrelated artist nodes are preserved.
- Replacement mapping is transactional.
- Unsupported renderer/View Layer pass combinations fail with guidance instead of fabricating output.
- A failed replacement attempt must not destroy a prior valid CutBridge mapping.
- Custom preset data cannot add arbitrary Blender operations or executable expressions.

## 6. Build Package

After validation succeeds, run **Build Package**.

In Manual/default conventions a package looks like:

```text
PROJECT_EP01_SC010_C012_T01_V001/
├── cutbridge.json
├── camera/
├── preview/
└── render/
    ├── beauty/
    ├── line/
    ├── shadow/
    └── depth/
```

Only resolved passes are represented. The exact path, sequence filename, required/optional policy, comp name, and layer order are recorded in `cutbridge.json`.

When the 3D handoff opt-in is enabled and valid, the manifest additionally includes a versioned `handoff_3d` block with baked camera/Empty transform and projection samples.

For Custom JSON mode, Build Package freezes the already validated preset to one in-memory snapshot for the entire build. A mid-build edit to the source JSON cannot produce one naming/folder contract in Blender and a different contract in the generated manifest.

The manifest records only normalized preset provenance (`mode`, schema/version, preset `id`, and display `name`). It does not record the source preset file path.

### Same-version safety

CutBridge must not silently overwrite an existing same-version package that already contains render/user payload. Create a new version such as V002/V003, or deliberately manage the older package yourself. Empty CutBridge scaffolds may only be refreshed through the supported safe path.

## 7. Render the selected sequences

Render through the mapped CutBridge outputs.

Before opening the package in AE, verify that required pass folders contain the expected sequence range. Optional passes may be absent only according to the manifest contract.

## 8. Install CutBridge for After Effects

Current development packages use **four adjacent runtime files**:

- `CutBridge.jsx`
- `revision_manager.js`
- `qc_plus.js`
- `localization.js`

Keep them together.

First test:

1. In After Effects choose **File > Scripts > Run Script File...**.
2. Select `CutBridge.jsx`.
3. Confirm the panel opens and the JA/EN selector works.

For a dockable panel, place all four files in the appropriate `Scripts/ScriptUI Panels` directory and restart After Effects.

If `localization.js` is missing or invalid, CutBridge must fall back to coherent English UI without weakening Build/QC/Revision safety. The safety-critical revision and QC sidecars must remain available.

See [../apps/after-effects/INSTALL.md](../apps/after-effects/INSTALL.md).

## 9. Import the package and Build

In CutBridge for After Effects:

1. Select/load `cutbridge.json`.
2. Review package identity, FPS, frame count, and validation result.
3. Build the CutBridge-managed project structure/comp.
4. Required sequences must be complete before successful build.
5. Optional unavailable passes follow warning/skip policy.
6. If a valid `handoff_3d` block is present, CutBridge reconstructs the supported managed camera and 3D Null layers from the baked data.

CutBridge reuses only verified managed objects. Same-name or source-similar artist objects are not automatically adopted.

The S10C reconstruction path remains bounded: no geometry, lights, bones, arbitrary hierarchy recreation, or general scene synchronization.

Native AE 2026 Build 87 validation measured a maximum 2D projection error of `0.00018066 px` against a `0.05 px` acceptance gate for the tested fixture. That evidence is specific to the tested S10C scope; it is not broad host certification.

## 10. Run QC+

Run **QC** after Build and after relevant project changes.

QC+ reports deterministic records using stable `CBQ-*` identifiers with PASS / WARNING / ERROR severity and safe remediation text.

QC checks include, where inspectable:

- package/manifest state;
- required/optional sequence availability and unexpected matching files;
- comp resolution, pixel aspect, FPS, and duration;
- managed footage/layer ownership and sources;
- managed S10C camera/Null state where present;
- stale/foreign/ambiguous managed state;
- revision compatibility boundaries.

QC is diagnostic-only. It must not silently adopt, import, move, retag, replace sources, or auto-repair ownership state.

## 11. Update to a compatible revision

For a newer package such as V002/V003:

1. Keep the current managed project intact.
2. Select the newer CutBridge package through the revision workflow.
3. Review compatibility diagnostics.
4. Warning-class compatible changes require explicit confirmation.
5. Incompatible geometry/pass-set/ownership/package-structure changes fail before source replacement.
6. Compatible revision updates replace only verified CutBridge-managed sources and migrate current managed metadata inside the rollback boundary.
7. Historical managed footage retains prior-version provenance.
8. Run Build/QC again after a successful revision.

The revision workflow is deliberately source-oriented; it does not resize/re-time a comp to force compatibility. Custom display prefixes such as `R0012` do not replace the numeric manifest `version` used by revision compatibility.

## 12. Japanese / English behavior

Japanese is the intended first-class/default display language. English is a deterministic fallback and support language.

Locale switching must not alter:

- manifest values;
- package identity;
- Studio Preset resolution;
- 3D handoff data;
- managed ownership tags;
- stable `CBQ-*` or `PRESET_*` codes;
- Build/QC/Revision decisions;
- unrelated scene/project objects.

## 13. Development and release boundary

Do not publish or label v0.2.3 as stable merely because CI and product-session gates pass.

Before an RC/stable release, CutBridge still requires repository-level release governance in issue #18, a fully validated release candidate, deliberate promotion to `main`, exact release authorization, real tag-triggered publication, downloaded-asset checksum verification, production update-index verification, and remaining release/end-to-end/target-user validation appropriate to the claim.

Use [RELEASE_READINESS.md](RELEASE_READINESS.md) as the canonical release checklist.

## Next product phase

After S11 QA / Docs / Release Engineering, the next bounded phase is **S12 — End-to-End Blender → package → After Effects validation harness**.

See:

- [HANDOFF_3D.md](HANDOFF_3D.md)
- [STUDIO_PRESETS.md](STUDIO_PRESETS.md)
- [RELEASE_READINESS.md](RELEASE_READINESS.md)
- [COMPATIBILITY.md](COMPATIBILITY.md)
- [COMPLETION_STATUS.md](COMPLETION_STATUS.md)
- [ROADMAP.md](ROADMAP.md)
- [TEST_PLAN.md](TEST_PLAN.md)
- [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md)
- [../apps/after-effects/INSTALL.md](../apps/after-effects/INSTALL.md)
