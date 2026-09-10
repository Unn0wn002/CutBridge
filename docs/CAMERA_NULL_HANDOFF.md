# S10 — Camera / Null Handoff Investigation

Status: **investigation in progress; no production camera/null importer is enabled.**

S10 exists to establish the Blender → After Effects spatial contract from reproducible evidence before CutBridge changes its production manifest or creates managed AE cameras/nulls.

## Current boundary

The production runtime remains unchanged by the S10 research harness:

- `cutbridge.json` still carries only the legacy active-camera name string;
- After Effects does not create a CutBridge-managed camera or null from that string;
- Studio Presets remain data-only and unrelated to this investigation;
- no S5/S6/S7 ownership, revision, rollback, or QC rule is relaxed;
- no release authorization, tag, GitHub Release, or `main` change is part of S10.

This is intentional. A plausible transform is not sufficient evidence for a cross-DCC handoff contract.

## Source conventions being reconciled

### Blender

Blender uses a Cartesian world coordinate system with **Z as the up axis**. X is left/right and Y is front/back. Camera navigation is expressed in the camera's local axes; the S10 synthetic fixture verifies the actual evaluated camera basis directly through Blender 5.2 rather than relying only on prose documentation.

Relevant Blender references:

- Blender 5.2 LTS Manual — Transform Orientation: https://docs.blender.org/manual/en/5.2/editors/3dview/controls/orientation.html
- Blender 5.2 LTS Manual — Cameras / Camera View: https://docs.blender.org/manual/en/5.2/render/cameras.html
- Blender Python API — camera/object matrix and projection APIs: https://docs.blender.org/api/current/

### After Effects

After Effects composition space uses an upper-left X/Y origin: X increases left→right, Y increases top→bottom, and Z depth increases near→far. Current AE scripting exposes the primitives needed for an eventual adapter:

- `LayerCollection.addCamera(name, centerPoint)`;
- `LayerCollection.addNull([duration])`;
- 3D Position / Orientation / X Rotation / Y Rotation / Z Rotation;
- Camera Point of Interest and Camera Options > Zoom.

Relevant Adobe references:

- Adobe Help — Use 3D layers in After Effects: https://helpx.adobe.com/after-effects/desktop/work-with-layers/3d-layers/3d-layers.html
- Adobe Help — Composition space and layer space: https://helpx.adobe.com/after-effects/desktop/work-with-layers/select-and-arrange-layers/selecting-arranging-layers.html
- After Effects Scripting Guide — LayerCollection: https://ae-scripting.docsforadobe.dev/layer/layercollection/
- After Effects Scripting Guide — CameraLayer: https://ae-scripting.docsforadobe.dev/layer/cameralayer/

## Candidate basis — not yet production-authorized

The current research candidate maps a Blender world vector `(X, Y, Z)` to AE as:

```text
AE X =  Blender X
AE Y = -Blender Z
AE Z =  Blender Y
```

or matrix form:

```text
[ 1  0  0 ]
[ 0  0 -1 ]
[ 0  1  0 ]
```

The matrix is orthonormal and has determinant `+1`, so this candidate is a proper right-handed basis rotation rather than a reflection.

Why this candidate is reasonable:

- Blender X right maps to AE X right;
- Blender Z up maps to AE negative Y, which is screen-up in AE;
- Blender Y front/back maps to AE Z depth.

This reasoning is **not** enough to ship it. Native AE projection must match Blender's projection for the fixed fixture in issue #47.

## Translation and spatial scale

For the research fixture only, Blender positions are mapped with a uniform scale `S` and composition-center offset:

```text
AE position = [compWidth/2 + S*X,
               compHeight/2 - S*Z,
               S*Y]
```

The fixture uses `S = 100` AE pixels per Blender unit. This value is chosen only to make probe geometry numerically readable. It is **not a proposed hard-coded studio/runtime scale**.

Perspective geometry is invariant to one uniform world scale when camera and objects are scaled together. A production design still needs an explicit scale policy before camera/null export is enabled.

## Camera optics candidate

The first fixture deliberately limits scope to one perspective camera with horizontal sensor fit:

- render/comp: `1920 × 1080`, square pixels;
- Blender camera location: `(0, -10, 0)`;
- Blender camera Euler XYZ: `(90°, 0°, 0°)`;
- lens: `50 mm`;
- sensor width: `36 mm`;
- spatial scale: `100`.

For horizontal field of view:

```text
fovX = 2 * atan(sensorWidth / (2 * lens))
AE Zoom = compWidth / (2 * tan(fovX / 2))
```

For the fixture this yields:

```text
fovX ≈ 39.597752709°
AE Zoom = 2666.6666666667 px
```

The candidate AE camera is therefore:

```text
Position          [960, 540, -1000]
Point of Interest [960, 540,     0]
Zoom               2666.6666666667
```

This first gate does **not** authorize:

- orthographic or panoramic Blender cameras;
- vertical/auto sensor-fit edge cases;
- lens shift;
- depth of field equivalence;
- arbitrary camera Euler decomposition;
- camera constraints or unsupported parenting.

## Synthetic projection fixture

The research harness uses five Blender world points:

```text
ORIGIN   (0, 0, 0)
X_PLUS   (1, 0, 0)
Y_PLUS   (0, 1, 0)
Z_PLUS   (0, 0, 1)
XYZ_PLUS (1, 1, 1)
```

The Blender probe uses Blender's own `world_to_camera_view()` result as the source-side reference. The AE native probe maps the same fixture through the candidate basis, uses a real AE CameraLayer and 3D nulls, then evaluates `toComp()` to obtain native projected coordinates.

Native PASS requires maximum 2D projection error **≤ 0.05 px** for all five points. Do not widen the tolerance to hide a mapping error.

## Research files

- `tools/research/s10_spatial_math.py` — pure candidate basis/FOV/timing math and deterministic fixture.
- `tools/research/s10_blender_probe.py` — isolated Blender 5.2 projection probe; removes every allocated probe data-block.
- `tools/research/s10_ae_probe.jsx` — disposable native AE probe; removes its temporary comp and only saves JSON after an explicit Save dialog.
- `tests/test_s10_camera_null_research.py` — pure math/fail-closed regression tests.
- `tests/test_s10_blender_probe_52.py` — Blender-runtime source-projection parity tests.
- `tests/test_s10_ae_probe_contract.py` — research-probe safety/tolerance contract.

Native AE evidence is tracked in **issue #47**.

## Parenting decision

No parent hierarchy is exported in the first probe.

For the eventual product feature, CutBridge should prefer the smallest deterministic contract. The current preferred direction is **sampled/evaluated world transforms** rather than recreating arbitrary Blender parent/constraint graphs in AE. This reduces dependence on AE parenting compensation and avoids silently approximating Blender constraints.

That direction is not yet a shipped decision. S10 must explicitly test parented camera/Empty cases before production implementation.

## Timing candidate

The timing candidate uses the existing manifest FPS and non-negative frame contract:

```text
timeSeconds = (frame - frameStart) / fps
```

This preserves frame 0 and fractional frame-rate representations without silently retiming animation. Sampling precision and keyframe serialization remain future implementation decisions.

## What must happen before runtime implementation

1. Blender 5.2 probe CI must pass on the exact S10 candidate.
2. Native AE probe issue #47 must PASS with the exact JSON measurements and cleanup confirmed.
3. If the candidate basis fails, revise the mapping from evidence; do not weaken validation.
4. Expand fixtures for arbitrary camera orientation before writing general camera-rotation conversion.
5. Expand fixtures for parented Empty/camera chains before deciding bake-vs-parent behavior.
6. Define explicit production spatial-scale policy.
7. Only then add an optional versioned manifest block and managed AE camera/null creation with S5-style ownership and rollback.

## S10 completion rule

S10 may conclude in either of two safe ways:

- **investigation PASS, runtime deferred** — the evidence and limitations are documented, but production camera/null creation remains disabled; or
- **minimal runtime subset PASS** — only after every shipped conversion has automated parity evidence and the required native AE gate.

A guessed conversion is not an acceptable completion state.
