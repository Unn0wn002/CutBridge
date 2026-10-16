# CutBridge Compatibility Policy

## Blender

- **Minimum runtime:** Blender `4.2.0`.
- **LTS-first targets:** Blender `4.2 LTS`, `4.5 LTS`, and `5.2 LTS`.
- Blender versions newer than the minimum but outside the current LTS target matrix are not blocked by the manifest; CutBridge labels them **Compatible baseline / unverified** until tested.
- Versions below `4.2.0` are unsupported and should not receive compatible update entries.

`blender_manifest.toml` intentionally defines a minimum version without a maximum version. If a future Blender release introduces a breaking incompatibility, a release may add `blender_version_max` or the distribution index may gate compatible versions.

### Blender 5.2 note

CutBridge 0.2.0 exposed a registration defect in Blender 5.2: the update preference used `StringProperty(subtype="URL")`, but Blender's supported string subtypes are `FILE_PATH`, `DIR_PATH`, `FILE_NAME`, `BYTE_STRING`, `PASSWORD`, and `NONE`. CutBridge 0.2.1 removed the invalid subtype and added transactional registration cleanup so a failed enable does not leave stale classes registered.

CutBridge 0.2.3 is covered by automated RNA lifecycle, render-mapping, package-generation, package-safety, Studio Preset, camera-handoff, and producer/consumer contract tests using the official `bpy 5.2.1` runtime.

These headless checks establish specific API/contract behavior but do not by themselves certify Blender GUI installation, every renderer configuration, operating-system filesystem behavior, or the complete Blender → After Effects workflow.

### Blender native evidence already recorded

The S8 native Blender gate passed on Blender 5.2.1 LTS for the tested Japanese/English N-panel, narrow-panel layout, Validate Cut, and Build Package workflow.

Current bounded native Blender evidence is **5.2.2**, build `d13f752e3b9c`, for the exact/equivalent package recorded at tested code SHA `5293cd46a819debfe8ecf41f740c4e94806dd89c`. The scripted GUI-event-loop V001–V003/36-output, preservation, negative/rollback and fresh-process reopen scope passed with actual exits 0; visual installation/panel/manual-update checks remain excluded. See [current preparation](RELEASE_PREPARATION_v0.2.5.md) for SHA-256 and equivalence boundaries. This is separate from the official `bpy 5.2.1` automated runtime.

S10B evaluated-world camera/Empty producer behavior is covered authoritatively by the official Blender 5.2.1 automated runtime/package suite. The broader release-target end-to-end campaign remains a separate release gate.

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
- **Native evidence for bounded scope** — real-host evidence exists for a specific named version/OS/workflow, but not for every feature or target combination.
- **Unsupported** — below the minimum version or explicitly excluded by release metadata.

Do not label a Blender/OS or After Effects/OS combination as broadly *certified* until the required real installation, package/render, cross-host, persistence, and release-target evidence has been recorded for the exact claim being made.

## After Effects

The current ExtendScript/ScriptUI implementation targets After Effects **2024–2026**. This remains a project target range rather than a blanket certification claim.

Automated coverage includes:

- **S4 contract coverage:** manifest/schema validation, frame semantics, required/optional passes, exact sequence coverage, path containment, Unicode filename handling in contract/host mocks, legacy data-only JSON parsing, and AE product-version synchronization.
- **S5 reliability coverage:** deterministic managed comp/footage/layer ownership, repeated build and script-reload behavior, collision/drift rejection, cache rediscovery, managed-source/FPS validation, QC failure reporting, optional-pass behavior, and rollback of newly created managed objects.
- **S6 revision coverage:** compatibility classification, opaque revision tickets, live ownership revalidation, stage-all/validate-all replacement import, native-adapter `AVLayer.replaceSource(..., false)` usage, source-swap rollback, V001→V002→V003 host-shaped lifecycle checks, historical-footage provenance, package-root note preservation, Build/QC after revision and reload, fail-closed handling of missing/duplicate deterministic package structure, pass-set rejection semantics, and managed-layer QC verification.
- **S7 QC+ coverage:** deterministic `CBQ-*` diagnostics, native binding guards, sequence/comp/managed render ownership checks and warning/error remediation semantics. Revision compatibility is assessed by the revision workflow; a clean QC report does not certify 3D transforms.
- **S8 localization coverage:** Japanese-first / English-fallback behavior, invalid/missing localization handling, persistence semantics, and native UI binding guards.
- **S10C reconstruction coverage:** optional `handoff_3d` validation, managed camera/3D Null ownership, Camera Position/Point of Interest/Zoom and Null Position/Scale, repeated-build isolation, collision rejection, and fixture-scoped simulated projection parity. Camera roll and Empty rotation are not reconstructed. QC+ does not check expected Camera/Null completeness, channel values/keyframes or projection parity; see [the exact channel boundary](HANDOFF_3D.md#after-effects-reconstruction-boundary).

These automated tests establish regression behavior and guard intended native adapter paths. They do **not** by themselves certify a real After Effects desktop host, ScriptUI behavior, Undo semantics, save/reopen persistence, filesystem/sequence interpretation on a specific OS, or preservation of all artist-authored properties.

## Native After Effects evidence

The v0.2.5 Blender `fef1023` and AE `049c095` campaigns preserve useful host observations, but their retained records do not establish the required offline/mount/credential isolation configuration. Their release-gate verdict is **INSUFFICIENT EVIDENCE**; historical PASS observations must not be applied to the current candidate. See [release preparation](RELEASE_PREPARATION_v0.2.5.md). The current native AE campaign is **PENDING**; current exact-candidate AE installation, preservation, rollback and reopen acceptance is not claimed here.

### S6 / S7 / S8 evidence

Real After Effects campaigns have already been executed for bounded S6 revision, S7 QC+, and S8 localization/fallback scopes. Material native defects found during those campaigns were repaired before integration.

### S10C native reconstruction / projection parity

S10C was executed in **Adobe After Effects 2026 Build 87 (`26.3x87`) on Windows 11** using real `handoff_3d` data produced by Blender 5.2.1 LTS.

Recorded bounded results:

- managed camera reconstruction: PASS;
- managed 3D Null reconstruction: PASS;
- deterministic layer ordering: PASS;
- maximum measured 2D projection error: **`0.00018066 px`**;
- acceptance threshold: **`<= 0.05 px`**;
- QC+: **10/10 PASS**;
- repeated Build: **0 duplicate managed layers**;
- unmanaged camera/null collision rejection: PASS;
- project persistence: PASS.

Therefore **After Effects 2026 Build 87 on Windows 11 has real native evidence for the tested S10C reconstruction scope**. This must not be expanded into a claim that all After Effects 2026 behavior, every Windows configuration, or the entire AE 2024–2026 target range is certified.

## Real-host release gates still required

Before a stable/release-ready compatibility claim, record the remaining evidence appropriate to the release target, including:

1. installation and normal use in the exact release-target Blender GUI build(s);
2. real render-sequence production for the intended renderer/View Layer configurations;
3. Blender → package → After Effects handoff using the exact release-candidate artifacts;
4. representative Build/QC/revision/save-close-reopen workflow;
5. V001→V002→V003 source-only revision preservation using shipped runtime files;
6. preservation of effects, masks, transforms, parenting, timing, layer order, artist-added layers, and unrelated project objects where that preservation is part of the release claim;
7. supported filesystem/path behavior for the intended OS matrix;
8. Studio Preset UI/file-selection behavior where included in the release claim;
9. S10C camera/null reconstruction on release-candidate artifacts without reinterpreting the already-passed bounded native gate as a broader host certification;
10. downloaded published-asset checksum/content verification; and
11. production update-index/update-discovery verification.

The authoritative execution checklist is [RELEASE_READINESS.md](RELEASE_READINESS.md). The broader cross-host campaign belongs to S12.

## Current compatibility summary

- Blender 4.2 / 4.5 / 5.2 LTS: target matrix; automated authoritative runtime centers on 5.2.1. Bounded historical 5.2.1 and current scripted 5.2.2 native scopes are distinct; neither certifies the complete target matrix.
- After Effects 2024–2026: target range.
- After Effects 2026 Build 87 on Windows 11: bounded real native evidence exists for S6–S8 scopes and S10C reconstruction/parity.
- Stable broad compatibility certification: **not yet claimed**.

v0.2.4 is published on GitHub; production distribution remains on v0.2.3 while Issue #99 is open. Compatibility evidence does not authorize a future publication.
