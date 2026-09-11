# S10A — Camera / Null Handoff Contract Investigation

Status: **investigation / contract only**

This document records the evidence-backed contract CutBridge will use before any Blender → After Effects camera/null importer behavior is allowed to ship.

## Decision summary

S10 must not translate Blender Euler values directly into After Effects Euler values. The two hosts expose different world/screen axis conventions and different parenting/orientation behaviors. CutBridge will instead:

1. evaluate Blender objects in **world space** at each exported frame;
2. map world-space positions and basis vectors through one explicit axis transform;
3. bake the result per frame for the first safe implementation;
4. keep Blender parenting/constraints/rig structure out of the first AE handoff;
5. store orientation as normalized basis/direction data rather than assuming an Euler order;
6. add camera/null data only as an **optional** future manifest extension so S1–S9 manifests stay valid;
7. require native Blender→AE projection validation before importer behavior is called complete.

## Authoritative host facts

### After Effects

Adobe documents composition space with:

- origin at the upper-left;
- +X left → right;
- +Y top → bottom;
- +Z near → far;
- 3D Position measured in composition space.

References:

- https://helpx.adobe.com/after-effects/desktop/work-with-layers/3d-layers/3d-layers.html
- https://helpx.adobe.com/after-effects/desktop/work-with-layers/select-and-arrange-layers/selecting-arranging-layers.html

Adobe scripting exposes `LayerCollection.addCamera(name, centerPoint)` and initializes the Point of Interest at `[x, y, 0]`. Camera properties include Position, Point of Interest, Orientation, X/Y/Z rotation and Zoom.

References:

- https://ae-scripting.docsforadobe.dev/layer/layercollection/
- https://ae-scripting.docsforadobe.dev/layer/cameralayer/

Adobe defines camera Zoom as the lens-to-image-plane distance in pixels and documents that Angle of View, Focal Length, Film Size and Zoom are coupled.

Reference:

- https://helpx.adobe.com/after-effects/desktop/work-with-layers/camera-layer/cameras-lights-points-interest.html

AE keyframe scripting uses seconds. `Property.setValueAtTime()` treats the beginning of the composition as time 0. Adobe expression time conversion similarly defines frame duration as seconds per frame.

References:

- https://ae-scripting.docsforadobe.dev/property/property/
- https://helpx.adobe.com/after-effects/desktop/work-with-expressions/expression-language-reference/expression-language-reference.html

Parenting changes child transform semantics to be relative to the parent. Adobe's scripting guide also notes that assigning `layer.parent` introduces compensating transform offsets to avoid a visible jump.

References:

- https://helpx.adobe.com/after-effects/desktop/work-with-layers/layer-properties/layer-properties.html
- https://ae-scripting.docsforadobe.dev/layer/layer/

Adobe's own Maya handoff guidance is conservative: targeted cameras use a locator/point-of-interest pattern, Maya locator nodes become AE nulls, and Adobe specifically warns against parenting locator nodes to each other for this interchange path.

Reference:

- https://helpx.adobe.com/after-effects/desktop/import-files/import-and-add-3d-models/preparing-importing-3d-image-files.html

### Blender 5.2

Blender uses a 3D world in which Z is the normal vertical/up axis. Camera sensor fit changes angular field of view based on output dimensions. Blender's documented camera projection helper `bpy_extras.object_utils.world_to_camera_view()` returns normalized camera-frame coordinates and already accounts for camera shift, lens angle, sensor size and perspective/orthographic projection.

References:

- https://docs.blender.org/manual/en/5.2/render/cameras.html
- https://docs.blender.org/api/5.2/bpy_extras.object_utils.html

Blender Empties are non-rendering coordinate handles and are therefore the closest native Blender concept to an AE control/null layer.

Reference:

- https://docs.blender.org/manual/en/5.2/modeling/empties.html

Blender parenting and camera rigs can alter evaluated world transforms independently of the camera object's local channels, so S10 must sample evaluated world state rather than assuming local transform channels describe the final result.

Reference:

- https://docs.blender.org/manual/en/latest/scene_layout/object/properties/relations.html

## CutBridge coordinate contract v1

For the first handoff contract, CutBridge defines the proper axis rotation:

```text
Blender world (x, y, z) -> AE-oriented vector (x, -z, y)
```

Therefore:

```text
Blender +X -> AE +X  (right)
Blender +Y -> AE +Z  (farther / into comp depth)
Blender +Z -> AE -Y  (up on screen)
```

This mapping is a proper rotation, not a reflection. The transformed basis remains right-handed.

### Position origin

Direction vectors use only the axis rotation.

World positions additionally map Blender origin to the AE composition center:

```text
AE.x = comp_width  / 2 + Blender.x * pixels_per_blender_unit
AE.y = comp_height / 2 - Blender.z * pixels_per_blender_unit
AE.z =                    Blender.y * pixels_per_blender_unit
```

`pixels_per_blender_unit` is **explicit CutBridge metadata**, not an inferred value. The investigation default is `100.0` px/BU. A future UI may make this configurable, but it must remain deterministic and serialized.

The absolute scale does not alter perspective projection when every camera/object distance is scaled uniformly; it primarily controls usable AE coordinate magnitudes.

## Timing contract

For an exported Blender frame `f`:

```text
AE_time_seconds = (f - frame_start) / fps
```

The first exported frame therefore maps to AE `0.0` seconds.

This intentionally matches the existing CutBridge comp contract:

```text
comp_duration = frame_count / fps
```

The final exported sample lands at `(frame_count - 1) / fps`, leaving exactly one frame duration through the comp out point.

## Orientation contract

CutBridge will not serialize Blender Euler channels as the authoritative handoff representation.

For each sampled object/camera, the future producer should derive evaluated world-space basis vectors from the evaluated Blender world matrix and transform those vectors with the same axis map used above.

For a camera, the minimum orientation representation is:

- transformed world position;
- normalized transformed **forward** vector;
- normalized transformed **up** vector.

The AE importer may then reconstruct the host camera using a native-tested method. Possible mechanisms include Point of Interest plus roll, or explicit Orientation/rotation channels. That reconstruction is intentionally **not frozen in S10A** because native AE validation is still required.

This keeps the manifest independent of Blender Euler order, local parents and animation rigs.

## Camera projection MVP gate

The first implementation should fail closed unless all of these are true:

- Blender camera type is `PERSP`;
- composition pixel aspect is 1.0;
- Blender camera shift X/Y are zero;
- camera projection is centered;
- no orthographic, panorama or custom camera mode is requested.

Why the restrictions exist:

- Adobe's 3D interchange guidance explicitly calls out square-pixel compositions for the documented targeted-camera workflow.
- Blender sensor fit and camera shift affect projection.
- AE scripting exposes Zoom but does not provide a direct one-to-one Blender sensor-shift control.

For a centered square-pixel perspective camera, the investigation math is:

```text
AE_zoom_px = comp_width / (2 * tan(horizontal_fov / 2))
```

Before shipping, this must be checked against a native projection fixture. The preferred Blender-side oracle is `world_to_camera_view()` because it accounts for Blender's real projection rules rather than duplicating sensor-fit logic in CutBridge.

## Empty -> AE Null MVP

The first safe null handoff should:

- include only explicitly selected/marked Blender Empty objects;
- sample the evaluated **world** transform at every exported frame;
- create AE nulls as 3D layers;
- keep them unparented initially;
- apply baked world-space samples;
- preserve stable CutBridge ownership metadata separately from the artist's layer name.

Do **not** reproduce Blender parent chains in the first implementation. AE parenting changes child transforms into parent-relative values and scripting can insert compensating offsets. Baking world transforms avoids a large class of hierarchy mismatch bugs.

## Proposed future optional manifest block

This is a proposal, not yet part of `cutbridge-manifest.schema.json`:

```json
{
  "handoff_3d": {
    "schema_version": 1,
    "coordinate_map": "blender_xyz_to_ae_x_negz_y",
    "origin": "composition_center",
    "pixels_per_blender_unit": 100.0,
    "sampling": "baked_per_frame",
    "camera": {
      "name": "Camera",
      "projection": {
        "type": "perspective",
        "zoom_px": 1600.0
      },
      "samples": [
        {
          "frame": 1001,
          "position": [960.0, 540.0, -1200.0],
          "forward": [0.0, 0.0, 1.0],
          "up": [0.0, -1.0, 0.0]
        }
      ]
    },
    "nulls": [
      {
        "id": "empty:tracking_origin",
        "name": "tracking_origin",
        "samples": [
          {
            "frame": 1001,
            "position": [960.0, 540.0, 0.0]
          }
        ]
      }
    ]
  }
}
```

If implemented, the block must remain optional so historical S1–S9 manifests continue to validate and import unchanged.

## Native validation matrix required before importer shipment

At minimum:

1. Blender origin and +/- global axes.
2. Camera at origin looking along a known axis.
3. 90° yaw, pitch and roll fixtures.
4. Combined rotations that would expose Euler-order assumptions.
5. Animated camera translation + rotation.
6. Animated Empty translation.
7. Parented/constraint-driven camera sampled in evaluated world space.
8. Parented Empty sampled in evaluated world space.
9. 24 / 25 / 30 / 29.97-style frame-rate timing checks.
10. Projection overlay: known Blender world points must land on the same AE pixels.
11. Rebuild/revision behavior must not duplicate or adopt manual AE camera/null layers.
12. Japanese/English UI/error-path check once user-facing controls exist.

## Explicitly deferred / not safe to ship yet

- Blender Euler -> AE Euler direct conversion.
- Preserving arbitrary Blender parent hierarchies in AE.
- Constraint/driver recreation in AE.
- Bones/armatures.
- Mesh/geometry scene export.
- Orthographic cameras.
- Panoramic/custom cameras.
- Shifted sensors.
- Non-square-pixel camera parity.
- Depth of field parity.
- Focus/aperture/bokeh parity.
- Motion blur/shutter parity.
- Automatic object selection beyond an explicit Empty handoff set.

## Advancement rule

S10B implementation may begin only from primitives that are deterministic in automated tests. Camera reconstruction in AE remains blocked until a native host fixture proves pixel-position and orientation parity for the supported subset.
