# CutBridge 3D Handoff — S10B Producer + S10C After Effects Reconstruction

Status: **bounded cross-host workflow validated for the documented S10C subset**

CutBridge can optionally add a versioned `handoff_3d` block to `cutbridge.json`. S10B produces evaluated Blender world-space camera/Empty samples; S10C consumes the supported subset in After Effects to create or update CutBridge-managed camera and 3D Null layers.

This is deliberately **not** general Blender ↔ After Effects scene synchronization.

## Compatibility rule

Historical CutBridge package behavior remains the default:

- `handoff_3d_enabled = false` by default;
- manifests without `handoff_3d` remain valid;
- normal render-pass / package / revision / QC / Studio Preset contracts remain unchanged;
- enabling 3D handoff is explicit and independent from Studio Presets.

The producer is still not exposed as a normal N-panel control. Until product UX explicitly promotes it, enable it only for the bounded workflow described here.

## Blender engineering opt-in

From Blender Python:

```python
bpy.context.scene.cutbridge.handoff_3d_enabled = True
bpy.context.scene.cutbridge.handoff_3d_pixels_per_blender_unit = 100.0
```

Mark only explicit Blender Empties for export:

```python
empty["cutbridge_handoff_3d"] = True
```

A marked object that is not an `EMPTY` fails validation rather than being silently ignored.

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

Camera samples additionally contain mapped forward/up direction, evaluated horizontal FOV, and derived AE Zoom. Blender Euler channels are not serialized.

## Coordinate and timing contract

The S10A axis mapping remains authoritative:

```text
Blender (x, y, z) -> AE-oriented (x, -z, y)
```

Position origin is the AE composition center.

Timing is:

```text
AE_time_seconds = (frame - frame_start) / fps
```

The first exported Blender frame therefore maps to AE time `0.0`.

## Evaluated-world baking

For each exported frame CutBridge:

1. sets Blender to the exact integer frame;
2. obtains the evaluated dependency graph;
3. reads the evaluated world matrix for the active camera and each marked Empty;
4. maps position and basis using the S10A contract;
5. records one baked sample;
6. restores the user's original frame/subframe on success or failure.

Parenting, constraints, and drivers may influence the evaluated world result, but their hierarchy is not recreated in AE. S10 uses baked world-space handoff instead.

## Producer fail-closed boundaries

Blender rejects unsupported or unsafe producer cases, including:

- non-perspective cameras;
- non-square pixels;
- non-zero camera sensor shift;
- zero-scale transforms;
- shear;
- reflected/negative-handed transforms;
- more than 64 marked Empties;
- more than 10,000 baked frames;
- more than 100,000 total camera/null samples;
- CutBridge handoff markers on non-Empty objects.

These are CutBridge contract boundaries, not limitations of Blender or After Effects themselves.

## After Effects reconstruction boundary

S10C validates the `handoff_3d` contract before project mutation. For the supported subset it can create/update:

- one CutBridge-managed perspective camera;
- CutBridge-managed 3D Null layers for serialized Blender Empties;
- baked position/orientation/projection timing from the manifest.

Ownership remains identity-based rather than name-only. Repeated Build is idempotent, and same-name unmanaged artist camera/null collisions fail closed instead of being adopted or overwritten.

S10C does not add geometry, lights, bones, arbitrary hierarchy recreation, or general scene synchronization.

## Native S10C evidence

Native validation was executed in **Adobe After Effects 2026 Build 87 (`26.3x87`) on Windows 11** with Blender 5.2.1 LTS-produced handoff data.

Recorded results:

- camera + 3D Null reconstruction: PASS;
- deterministic managed layer ordering: PASS;
- maximum measured 2D projection error: **`0.00018066 px`**;
- acceptance gate: **`<= 0.05 px`**;
- QC+: **10/10 PASS**;
- repeated Build: **0 duplicate managed layers**;
- unmanaged camera/null collision rejection: PASS;
- project persistence: PASS.

This evidence validates the tested S10C subset in the named host. It does not certify every After Effects version, operating system, Blender renderer, or arbitrary camera setup.

## Release boundary

S10C validation does not authorize publication. v0.2.3 remains unreleased; release governance issue #18 remains open; `release-authorization.json` must remain fail-closed until a deliberate release-candidate process reaches the authorization stage.

See also:

- [CAMERA_NULL_HANDOFF_CONTRACT.md](CAMERA_NULL_HANDOFF_CONTRACT.md)
- [TEST_PLAN.md](TEST_PLAN.md)
- [COMPATIBILITY.md](COMPATIBILITY.md)
- [RELEASE_READINESS.md](RELEASE_READINESS.md)
