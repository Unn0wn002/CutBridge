# CutBridge MVP v0.1

> Historical v0.1 guide. Use the [current README](../README.md), [development/test instructions](CONTRIBUTING.md), and [release checklist](RELEASE_CHECKLIST.md) for current versions and verification status. Render mapping and complete AE handoff remain unverified.

CutBridge is a student-project prototype for a **Blender → After Effects anime cut handoff**. The MVP implements the core idea from the project requirements: deterministic cut metadata, package folders, a human-readable JSON manifest, AE auto-comp, image sequence import, and basic QC.

## What works in v0.1

### Blender add-on
- Project / Episode / Scene / Cut / Take / Version metadata.
- Reads Blender FPS, resolution, frame range, and active camera.
- Selects BEAUTY / LINE / SHADOW / DEPTH package passes.
- Validates missing identifiers, camera, FPS, frame range, resolution, pass selection, output path.
- Creates deterministic folders.
- Writes UTF-8 `cutbridge.json`.

### After Effects script / ScriptUI panel
- Loads `cutbridge.json`.
- Creates AE folders: `01_COMP`, `02_RENDER`, `03_PRECOMP`, `04_OUTPUT`.
- Imports image sequences defined in the manifest.
- Conforms footage to manifest FPS.
- Creates a comp at manifest resolution/FPS/duration.
- Orders layers using `ae.layer_order`.
- Basic QC for manifest/frame count/resolution/pass folders/sources/comp FPS/duration.

## Current scope boundaries

Not implemented yet: live link, timesheet integration, native AE effect, render farm, toon shader, camera/null transfer, robust non-destructive revision update, studio preset editor, frame-by-frame missing-frame scan, automated render-pass configuration in Blender.

---

# 1. Install the Blender side

For source/development testing, package the contents of `apps/blender/cutbridge/` as the installable extension ZIP, or use the automated GitHub release workflow once a release tag is published.

1. Open Blender 4.2 LTS or later.
2. `Edit > Preferences > Add-ons` / `Extensions` depending on Blender version.
3. Choose **Install from Disk**.
4. Select the CutBridge Blender ZIP.
5. Enable **CutBridge**.
6. Open a 3D View and press `N`.
7. Select the **CutBridge** tab.

## Test Blender package creation

1. Save the `.blend` file.
2. Assign an active scene camera.
3. Set FPS, resolution, and frame range.
4. Fill Project/Episode/Scene/Cut/Take/Version.
5. Choose output directory.
6. Click **Validate Cut**.
7. Click **Build Package**.

Expected output:

```text
PROJECT_EP01_SC010_C012_T01_V001/
├── cutbridge.json
├── camera/
├── preview/
└── render/
    ├── beauty/
    ├── line/
    └── shadow/
```

The add-on does **not render** the passes yet. It creates the deterministic handoff contract and destination folders. Render output automation is the next Blender milestone.

---

# 2. Test the After Effects side

The repository intentionally does not include binary client/render assets. For AE testing, first create a CutBridge package in Blender, then place test image sequences into the generated pass folders using the filenames defined by `cutbridge.json`.

Example:

```text
render/beauty/C012_BEAUTY_0001.png
render/beauty/C012_BEAUTY_0002.png
...
render/line/C012_LINE_0001.png
...
```

Then:

1. Open After Effects.
2. `File > Scripts > Run Script File...`
3. Choose `apps/after-effects/CutBridge.jsx`.
4. Click **Import Package**.
5. Choose the generated `cutbridge.json`.
6. Click **Build Comp**.
7. Click **Run QC**.

The resulting composition should use the manifest resolution, FPS, frame duration, imported passes, and layer ordering.

### Dockable panel

Copy `CutBridge.jsx` into the After Effects `Scripts/ScriptUI Panels` folder and restart After Effects. Then open it from the `Window` menu.

Adobe's exact scripts folder location varies by OS/version, so for the first test use **Run Script File**.

---

# 3. Recommended next development order

1. **v0.2 Blender Render Mapping** — map package passes to View Layers/AOVs and set output paths automatically.
2. **v0.3 Revision Update** — load V002/V003 and replace only managed footage, preserving manual AE layers/effects.
3. **v0.4 QC+** — exact missing-frame scanner, filename/version checks, actionable fixes.
4. **v0.5 Studio Presets** — JSON naming/pass/layer/blend-mode rules.
5. **v0.6 Japanese UI** — full JA strings and Japanese quick-start.
6. **v0.7 Camera/Null Handoff** — adapter/exporter for camera and tracked empties.
7. **v0.8 Client Validation Build** — telemetry-free task timing sheet + acceptance checklist.

## Product rule

Do not hard-code one studio's naming convention until client interviews validate it. The architecture should remain preset-driven.
