# CutBridge Compatibility Policy

## Blender

- **Minimum runtime:** Blender `4.2.0`.
- **LTS-first targets:** Blender `4.2 LTS`, `4.5 LTS`, and `5.2 LTS`.
- Blender versions newer than the minimum but outside the current LTS target matrix are not blocked by the manifest; CutBridge labels them **Compatible baseline / unverified** until tested.
- Versions below `4.2.0` are unsupported and should not receive compatible update entries.

`blender_manifest.toml` intentionally defines a minimum version without a maximum version. If a future Blender release introduces a breaking incompatibility, a release may add `blender_version_max` or the distribution index may gate compatible versions.

### Blender 5.2 note

CutBridge 0.2.0 exposed a registration defect in Blender 5.2: the update preference used `StringProperty(subtype="URL")`, but Blender's supported string subtypes are `FILE_PATH`, `DIR_PATH`, `FILE_NAME`, `BYTE_STRING`, `PASSWORD`, and `NONE`. CutBridge 0.2.1 removes the invalid subtype and adds transactional registration cleanup so a failed enable does not leave stale classes registered.

Blender 5.2 LTS is therefore an explicit test target starting with CutBridge 0.2.1. It must still pass a real install/runtime and Blender→After Effects handoff test before being described as certified.

CutBridge 0.2.3 is covered by automated RNA lifecycle and package-generation
tests using the official `bpy 5.2.1` runtime. These headless checks do not replace
a Blender GUI install/panel test or an After Effects handoff test, so certification
still requires those manual results.

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

Do not label a Blender/OS combination as *certified* until an actual install, package-build, Blender runtime, and Blender→After Effects handoff test has been recorded.

## After Effects

The current ExtendScript MVP targets After Effects 2024–2026. This is a project target, not a certification claim. Version-specific runtime testing is tracked separately from the Blender extension compatibility policy.
