# Four-Pass Workflow — v0.2.3-beta.2 Repair Evidence

Status: **automated Blender 5.2.1 evidence; native GUI rerun still required**

CutBridge exposes four production pass selections:

- Beauty
- Line
- Shadow
- Depth

The four selections are not renderer-agnostic. `Validate Cut` must verify that the active Blender renderer/View Layer can expose every selected Render Layers output before `Build Package` is allowed to proceed.

## Blender 5.2 renderer boundary

Blender 5.2 documents the standalone **Shadow** render pass under **EEVEE**. Cycles exposes different light-pass options and Shadow Catcher rather than the same standalone `Shadow` Render Layers output expected by the current CutBridge pass contract.

Therefore the current CutBridge contract is:

- **EEVEE:** Beauty + Line + Shadow + Depth can be selected together when Freestyle is enabled and exposed **As Render Pass** for Line.
- **Cycles:** selecting CutBridge `Shadow` is invalid for the current contract. `Validate Cut` must report `SHADOW_OUTPUT_UNAVAILABLE` before Build; the user must switch to a renderer/View Layer that exposes Shadow or disable Shadow.
- **Line:** requires Blender Freestyle plus the active View Layer's Freestyle **As Render Pass** output. `Validate Cut` reports `LINE_OUTPUT_UNAVAILABLE` when this cannot be generated.
- **Depth:** is supported by the current renderer mapping where the View Layer exposes Z/Depth. OpenEXR is recommended when accurate camera-distance data matters; non-OpenEXR remains a warning rather than a blocker.

## Automated Blender 5.2.1 matrix

The authoritative `bpy==5.2.1` lane exercises:

| Pass selection | Renderer | Format | Expected result |
|---|---|---|---|
| Beauty | EEVEE | PNG | Build succeeds |
| Beauty + Line | EEVEE | PNG | Build succeeds when Freestyle/As Render Pass is available |
| Beauty + Shadow | EEVEE | PNG | Build succeeds |
| Depth | EEVEE | PNG | Build succeeds with `DEPTH_FORMAT_LOSSY` warning |
| Depth | EEVEE | OpenEXR | Build succeeds without the lossy-depth warning |
| Beauty + Line + Shadow | EEVEE | PNG | Build succeeds |
| Beauty + Line + Shadow + Depth | EEVEE | OpenEXR | Build succeeds |
| Beauty + Shadow | Cycles | PNG | Validate ERROR before Build; no package created |

For successful combinations, the regression asserts:

- no silent pass omission;
- deterministic pass order in the manifest;
- unique package-relative render paths;
- correct sequence extension for the package format;
- one managed File Output node per enabled pass;
- matching File Output format;
- package directories exist for every declared pass.

For unsupported Cycles + Shadow, the regression asserts:

- `Validate Cut` returns an actionable ERROR before Build;
- the temporary capability probe restores the artist View Layer pass flag;
- no temporary probe node group survives;
- Build remains blocked;
- no partial package is created.

## Format limitation in v0.2.3

The current manifest/preset contract has one package-level sequence format. The selected Sequence Format therefore applies to **all enabled passes**. Mixed per-pass formats are intentionally **not** half-implemented in this repair branch. The follow-up design is tracked separately so historical manifests and presets are not silently reinterpreted.

## Evidence boundary

This document does **not** upgrade Blender 4.2 or 4.5 to tested status and does not replace native GUI evidence. The exact frozen beta.2 artifact must still be exercised in the intended Blender host(s) and through Blender → package → After Effects before a broader compatibility claim is made.