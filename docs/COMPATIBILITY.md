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

S4 automated coverage validates the manifest/schema contract, frame semantics, required/optional passes, exact sequence coverage, path containment, Unicode filename handling in contract/host mocks, legacy data-only JSON parsing, and AE product-version synchronization. These tests run through Node and mocked host adapters; they do **not** certify native After Effects APIs, ScriptUI behavior, filesystem semantics, sequence interpretation, or composition behavior on a supported desktop installation.

Real AE GUI import/comp/QC and Blender→AE end-to-end execution remain manual validation gates until actual evidence is recorded.
