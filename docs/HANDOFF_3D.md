# S10B — Producer-only 3D handoff data

Status: **experimental producer contract; no After Effects reconstruction yet**

S10B adds an optional `handoff_3d` block to `cutbridge.json`. The block is disabled by default and is intended for engineering validation before CutBridge creates AE cameras or nulls.

## Compatibility rule

Historical CutBridge behavior remains the default:

- `handoff_3d_enabled = false` by default;
- manifests without `handoff_3d` remain valid;
- the existing After Effects importer ignores the optional field;
- no existing pass/package/revision/QC/Studio Preset contract is changed.

## Engineering opt-in

Until native AE reconstruction is validated, S10B intentionally does not expose this feature as a normal N-panel workflow.

From Blender Python, enable producer data with:

```python
bpy.context.scene.cutbridge.handoff_3d_enabled = True
bpy.context.scene.cutbridge.handoff_3d_pixels_per_blender_unit = 100.0
```

Mark only explicit Blender Empties for export:

```python
empty["cutbridge_handoff_3d"] = True
```

Objects carrying that marker but not of type `EMPTY` fail validation rather than being silently ignored.

## Data model

The optional manifest member is versioned independently:

```json
{
  "handoff_3d": {
    "schema": "cutbridge-handoff-3d",
    "schema_version": 1,
    "space": {
      "coordinate_system": "after-effects-composition",
      "axis_map": "blender_xyz_to_ae_x_negz_y",
      "origin": "composition-center",
      "position_units": "pixels",
      "pixels_per_blender_unit": 100.0
    },
    "sampling": {
      "mode": "baked-per-frame",
      "frame_start": 1,
      "frame_end": 120,
      "frame_step": 1
    },
    "camera": {
      "name": "Camera",
      "type": "PERSP",
      "samples": []
    },
    "nulls": []
  }
}
```

Each transform sample contains:

- source Blender frame;
- AE composition time in seconds;
- AE-oriented position in pixels;
- normalized mapped local basis vectors `x`, `y`, `z`;
- evaluated world basis lengths as `scale`.

Camera samples additionally contain:

- mapped forward direction;
- mapped up direction;
- evaluated horizontal FOV in radians;
- derived AE Zoom in pixels.

No Blender Euler angles are serialized.

## Coordinate and timing contract

S10B uses the S10A mapping unchanged:

```text
Blender (x, y, z) -> AE-oriented (x, -z, y)
```

Blender world origin maps to the AE composition center for positions.

Timing is:

```text
AE_time_seconds = (frame - frame_start) / fps
```

The first exported frame is therefore AE time `0.0`.

## Evaluated-world baking

For every exported frame CutBridge:

1. sets Blender to that exact integer frame;
2. obtains the evaluated dependency graph;
3. reads the evaluated world matrix of the active camera and each marked Empty;
4. maps position and basis through the S10A axis contract;
5. records a baked sample;
6. restores the user's original Blender frame and subframe when sampling finishes or fails.

Parenting, constraints, and drivers may influence the evaluated world result, but their hierarchy is **not** recreated in AE. This is deliberate: the first safe handoff is baked world-space data.

## Fail-closed boundaries

S10B rejects cases that do not yet have a proven reconstruction contract:

- non-perspective cameras;
- non-square pixels;
- camera sensor shift;
- zero-scale transforms;
- shear in evaluated world transforms;
- reflected transforms with negative handedness;
- more than 64 marked Empties;
- more than 10,000 baked frames;
- more than 100,000 total camera/null samples;
- CutBridge handoff markers on non-Empty objects.

These limits are safety/contract boundaries, not claims about what Blender or After Effects can theoretically support.

## After Effects boundary

S10B **does not create, modify, or parent AE cameras/nulls**. The current AE importer continues to consume the existing manifest fields only.

A later S10C phase must validate real AE camera/null reconstruction using native host fixtures before this producer data becomes a user-facing cross-host workflow.

## Validation

S10B requires:

- Draft 2020-12 manifest-schema coverage for old manifests and the new optional block;
- proof that the existing AE validator accepts manifests containing `handoff_3d` without consuming it;
- Blender 5.2.1 runtime tests for evaluated camera/null sampling, animation, parenting/world baking, frame restoration, marker filtering, fail-closed transforms, and full Build Package integration.
