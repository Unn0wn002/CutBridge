# CutBridge Quick Start

This guide describes the **v0.2.3 unreleased development workflow through S9**.

CutBridge connects one Blender animation cut to After Effects through deterministic render-output mapping, a versioned package, `cutbridge.json`, managed AE project state, QC+, compatible source-only revision updates, Japanese-first UX, and data-only Studio Presets.

Intended flow:

`Blender metadata + optional Studio Preset → Validate Cut → deterministic render mapping/package → render sequences → AE Import/Build → QC+ → compatible revision update`

Japanese guide: [QUICK_START_JA.md](QUICK_START_JA.md).

Studio Preset authoring reference: [STUDIO_PRESETS.md](STUDIO_PRESETS.md).

## Development status

S1–S8 established the deterministic handoff, ownership/revision/QC contracts, and Japanese-first UI. S9 adds a validated Studio Preset layer while preserving Manual mode and the existing Blender↔AE identity contract.

This is development evidence, not stable-release authorization. There is no release tag or GitHub Release, and `release-authorization.json` remains fail-closed.

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

**CutBridge Default** uses the built-in declarative preset. It intentionally reproduces the default CutBridge conventions through the S9 preset pipeline.

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

See [STUDIO_PRESETS.md](STUDIO_PRESETS.md) for the complete schema, allowed placeholders, validation rules, and safe example.

### Frame-range rule

CutBridge supports export ranges beginning at frame `0` or later. Negative/preroll export ranges are rejected at Blender/schema/AE boundaries. CutBridge does not silently renumber animation; rebase the export range before package creation.

## 3. Validate Cut

Run **Validate Cut**.

Validation covers identifiers, camera, FPS, resolution, frame range, Studio Preset validity, selected/resolved passes, output target, renderer/View Layer capability, and package-target safety.

- `ERROR` means stop and fix the problem.
- Warnings require review before proceeding.
- Stable machine-facing validation semantics do not change when switching JA/EN.
- Invalid custom preset data fails closed before package creation.

Preset-specific stable codes include `PRESET_JSON_INVALID`, `PRESET_SCHEMA_INVALID`, `PRESET_SCHEMA_UNSUPPORTED`, `PRESET_FIELD_INVALID`, and `PRESET_PATH_UNSAFE`.

## 4. Render-output mapping

CutBridge configures deterministic compositor output mapping for the resolved logical passes.

Safety rules:

- CutBridge-owned compositor state uses the `CUTBRIDGE_` namespace.
- Unrelated artist nodes are preserved.
- Replacement mapping is transactional.
- Unsupported renderer/View Layer pass combinations fail with guidance instead of fabricating output.
- A failed replacement attempt must not destroy a prior valid CutBridge mapping.
- Custom preset data cannot add arbitrary Blender operations or executable expressions.

## 5. Build Package

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

For Custom JSON mode, Build Package freezes the already validated preset to one in-memory snapshot for the entire build. A mid-build edit to the source JSON cannot produce one naming/folder contract in Blender and a different contract in the generated manifest.

The manifest records only normalized preset provenance (`mode`, schema/version, preset `id`, and display `name`). It does not record the source preset file path.

### Same-version safety

CutBridge must not silently overwrite an existing same-version package that already contains render/user payload. Create a new version such as V002/V003, or deliberately manage the older package yourself. Empty CutBridge scaffolds may only be refreshed through the supported safe path.

## 6. Render the selected sequences

Render through the mapped CutBridge outputs.

Before opening the package in AE, verify that required pass folders contain the expected sequence range. Optional passes may be absent only according to the manifest contract.

## 7. Install CutBridge for After Effects

S8+ development packages use **four adjacent runtime files**:

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

If `localization.js` is missing or invalid, S8 must fall back to coherent English UI without weakening Build/QC/Revision safety. The safety-critical revision and QC sidecars must remain available.

## 8. Import the package and Build

In CutBridge for After Effects:

1. Select/load `cutbridge.json`.
2. Review the package identity, FPS, frame count, and validation result.
3. Build the CutBridge-managed project structure/comp.
4. Required sequences must be complete before successful build.
5. Optional unavailable passes follow warning/skip policy.

CutBridge reuses only verified managed objects. Same-name or source-similar artist objects are not automatically adopted.

S9 does not create a second preset trust boundary in After Effects. AE consumes the already-resolved manifest fields and never parses the custom Studio Preset JSON.

## 9. Run QC+

Run **QC** after Build and after relevant project changes.

S7 QC+ reports deterministic records using stable `CBQ-*` identifiers with PASS / WARNING / ERROR severity and safe remediation text.

QC checks include, where inspectable:

- package/manifest state;
- required/optional sequence availability and unexpected matching files;
- comp resolution, pixel aspect, FPS, and duration;
- managed footage/layer ownership and sources;
- stale/foreign/ambiguous managed state;
- revision compatibility boundaries.

QC is diagnostic-only. It must not silently adopt, import, move, retag, replace sources, or auto-repair ownership state.

## 10. Update to a compatible revision

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

## 11. Japanese / English behavior

Japanese is the intended first-class/default display language. English is a deterministic fallback and support language.

Locale switching must not alter:

- manifest values;
- package identity;
- Studio Preset resolution;
- managed ownership tags;
- stable `CBQ-*` or `PRESET_*` codes;
- Build/QC/Revision decisions;
- unrelated scene/project objects.

## 12. Development and release boundary

Do not publish or label v0.2.3 as stable merely because CI and product-session gates pass.

Before an RC/stable release, CutBridge still requires the release-governance controls in issue #18, deliberate promotion to `main`, exact release authorization, real tag-triggered publication, downloaded-asset checksum verification, production update-index verification, and remaining release/end-to-end/target-user validation appropriate to the claim.

## Next product phase

After S9 Studio Presets is integrated, the next engineering phase is **S10 — Camera / Null Handoff Investigation**.

See:

- [STUDIO_PRESETS.md](STUDIO_PRESETS.md)
- [COMPLETION_STATUS.md](COMPLETION_STATUS.md)
- [ROADMAP.md](ROADMAP.md)
- [TEST_PLAN.md](TEST_PLAN.md)
- [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md)
- [../apps/after-effects/INSTALL.md](../apps/after-effects/INSTALL.md)
