# CutBridge v0.2.3 — Test Plan

Run the complete automated commands in [CONTRIBUTING.md](CONTRIBUTING.md). Release safety coverage also checks repeatability, license inclusion, output preservation, artifact symlinks and mismatched version constants.

## Blender tests

| ID | Test | Expected |
|---|---|---|
| B01 | Empty Cut ID | Validation error |
| B02 | No active camera | Validation error |
| B03 | Frame 1–12, 24 fps | Manifest count = 12, fps = 24 |
| B04 | Japanese metadata e.g. `テスト作品` | UTF-8 JSON is created correctly |
| B05 | BEAUTY+LINE only | Only two render pass folders + manifest entries |
| B06 | Build V001 then V002 | Two deterministic package folders |
| B07 | Register CutBridge 0.2.3 with official `bpy 5.2.1` | Extension registers without `StringProperty` or RNA registration errors |
| B08 | Disable and re-enable CutBridge in the same Blender session | No `already registered as a subclass` error |
| B09 | Simulate/encounter a failed registration, then retry enable | CutBridge cleans partial registrations and can retry without restarting Blender |
| B10 | Open Environment panel on Blender 5.2 | Reports CutBridge 0.2.3, Blender 5.2.x, platform, Python, and Target LTS status |
| B11 | Build a package with CutBridge 0.2.3 | Generated manifest version matches the canonical extension version |
| B12 | Missing camera, Cut ID, output, passes, or valid frame range | Validation reports the corresponding error and blocks package generation |
| B13 | BEAUTY; BEAUTY+LINE; all four passes | Folder tree and manifest entries match the selected passes exactly |
| B14 | Build a release artifact | Root manifest/modules, synchronized metadata, and recomputed SHA-256 values pass |

Automated Blender checks run headlessly. Blender GUI installation/panel behavior and
After Effects GUI behavior remain manual test areas.

## After Effects tests

| ID | Test | Expected |
|---|---|---|
| A01 | Load a valid CutBridge manifest | Status shows package / FPS / frame count |
| A02 | Build comp from prepared image sequences | Resolution, FPS, and duration match manifest |
| A03 | Layer order | Layers follow `ae.layer_order` in manifest |
| A04 | Remove a required pass folder and run QC | QC reports pass folder/source missing |
| A05 | Change manifest FPS and build a new comp | Comp uses manifest FPS |
| A06 | Japanese path/package name | Manifest loads without encoding failure |

## Client task test

Measure:
1. Manual setup time for one cut in AE.
2. CutBridge setup time.
3. Number of handoff errors.
4. Whether the tester understood errors without developer intervention.
5. Which automation was useful vs. intrusive.
