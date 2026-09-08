# CutBridge Compatibility Policy

## Blender

- **Minimum runtime:** Blender `4.2.0`.
- **LTS-first targets:** Blender `4.2 LTS`, `4.5 LTS`, and `5.2 LTS`.
- Blender versions newer than the minimum but outside the current LTS target matrix are not blocked by the manifest; CutBridge labels them **Compatible baseline / unverified** until tested.
- Versions below `4.2.0` are unsupported and should not receive compatible update entries.

`blender_manifest.toml` intentionally defines a minimum version without a maximum version. If a future Blender release introduces a breaking incompatibility, a release may add `blender_version_max` or the distribution index may gate compatible versions.

### Blender 5.2 note

CutBridge 0.2.0 exposed a registration defect in Blender 5.2: the update preference used `StringProperty(subtype="URL")`, but Blender's supported string subtypes are `FILE_PATH`, `DIR_PATH`, `FILE_NAME`, `BYTE_STRING`, `PASSWORD`, and `NONE`. CutBridge 0.2.1 removes the invalid subtype and adds transactional registration cleanup so a failed enable does not leave stale classes registered.

CutBridge 0.2.3 is covered by automated RNA lifecycle, render-mapping, package-generation, package-safety, and producer/consumer contract tests using the official `bpy 5.2.1` runtime. These headless checks establish specific API/contract behavior but do not by themselves certify Blender GUI installation, every renderer configuration, operating-system filesystem behavior, or the Blender→After Effects handoff.

## Platform identifiers

CutBridge uses Blender extension-repository style platform identifiers:

- `windows-x64`
- `windows-arm64`
- `macos-x64`
- `macos-arm64`
- `linux-x64`

The runtime diagnostic reports the detected platform. Update entries may restrict releases to a platform list.

## Certification terminology

CutBridge distinguishes between:

- **Target LTS** — a release series intentionally included in the test plan.
- **Compatible baseline / unverified** — meets the declared minimum but has not been validated in the current test matrix.
- **Unsupported** — below the minimum version or explicitly excluded by release metadata.

Do not label a Blender/OS combination as *certified* until the required real install, package-build/render workflow, and Blender→After Effects handoff evidence has been recorded for the release claim being made.

## After Effects

The current ExtendScript/ScriptUI implementation targets After Effects 2024–2026. This is a project target, not a certification claim.

Automated coverage currently includes:

- **S4 contract coverage:** manifest/schema validation, frame semantics, required/optional passes, exact sequence coverage, path containment, Unicode filename handling in contract/host mocks, legacy data-only JSON parsing, and AE product-version synchronization.
- **S5 reliability coverage:** deterministic managed comp/footage/layer ownership, repeated build and script-reload behavior, collision/drift rejection, cache rediscovery, managed-source/FPS validation, QC failure reporting, optional-pass behavior, and rollback of newly created managed objects.
- **S6 revision coverage:** compatibility classification, opaque revision tickets, live ownership revalidation, stage-all/validate-all replacement import, native-adapter `AVLayer.replaceSource(..., false)` usage, source-swap rollback, V001→V002→V003 host-shaped lifecycle checks, historical-footage provenance, package-root note preservation, Build/QC after revision and reload, fail-closed handling of missing/duplicate deterministic package structure, and #26 coverage proving pass-set additions/removals—including optional-pass removal—are rejected before confirmation or mutation while required/optional status changes on retained passes use the warning/confirmation path.

These tests run through Node, Python, contract helpers, and host-shaped/mocked adapters. They establish regression behavior and guard the intended native adapter code paths, but they do **not** certify a real After Effects desktop host, ScriptUI behavior, Undo semantics, save/reopen persistence, filesystem/sequence interpretation on a specific OS, or preservation of real artist properties in a supported AE installation.

### Native After Effects validation required before stable claims

Before a stable/release-ready compatibility claim for After Effects, record real desktop evidence for the intended AE version/OS combination, including:

1. load/import a real CutBridge package;
2. Build Comp and Run QC;
3. perform V001→V002→V003 source-only revision updates using the shipped `CutBridge.jsx` + `revision_manager.js` pair;
4. verify effects, masks, transforms, parenting, timing, layer order, artist-added layers, and unrelated project objects are preserved;
5. save, close, reopen, reload CutBridge, and repeat Build/QC;
6. verify a retained-pass required/optional status change follows the warning/confirmation path, and verify pass-set addition/removal plus geometry/timing drift block before mutation;
7. verify missing/duplicate managed package structure fails closed without project mutation; and
8. complete a real Blender → package → After Effects end-to-end smoke test.

Until that evidence exists, After Effects 2024–2026 remains a **target range / unverified desktop-host matrix**, not a certified compatibility claim.
