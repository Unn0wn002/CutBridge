# CutBridge v0.2.3 — Test Plan

This plan describes the **S1–S9 + S10A–S10B development baseline**. Automated tests are regression evidence; native GUI/end-to-end claims require real-host evidence.

The authoritative CI gate remains two jobs:

- `static-validation`;
- `blender-52-rna-runtime` using official `bpy==5.2.1`.

The Blender suite currently emits `Scene.use_nodes` deprecation warnings expected to matter for Blender 6.0; see [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).

## 1. Core automated gates

### Static / release / AE contract

CI must run the maintained pytest and Node suites covering:

- canonical product-version synchronization;
- JSON schema/example validation;
- deterministic release packaging and SHA-256 checks;
- release authorization fail-closed behavior;
- AE manifest, path, sequence, pass, package-identity, ownership, revision, QC+, and localization contracts;
- Studio Preset schema/example/loader/security contracts;
- S10A camera/null coordinate, timing, FOV/Zoom, and fail-closed primitives;
- S10B optional `handoff_3d` schema/backward compatibility;
- proof that the existing AE manifest validator accepts but does not consume the optional S10B block;
- JS/ExtendScript syntax for all shipped AE runtime files;
- Japanese/English localization fallback and stable machine identifiers.

Any missing mandatory dependency must fail the gate rather than silently skipping coverage.

### Blender 5.2.1 runtime

Authoritative CI installs official `bpy==5.2.1` and verifies:

- register → unregister → register → unregister lifecycle;
- scene metadata and validation behavior;
- render mapping and rollback;
- package generation/integrity;
- producer/consumer filename and manifest contracts;
- Japanese/UTF-8 handling;
- S8 Blender localization behavior;
- S9 Studio Preset integration;
- S10B evaluated-world camera and marked-Empty sampling;
- animated/parented Empty world-space baking;
- frame restoration and fail-closed S10 transform/camera cases;
- full package generation with a schema-valid optional `handoff_3d` block.

## 2. Blender behavioral matrix

| ID | Scenario | Expected |
|---|---|---|
| B01 | Required metadata missing | Actionable validation error; package creation blocked |
| B02 | No active camera | Validation error |
| B03 | Valid non-negative frame range | Manifest frame count/FPS agree with scene |
| B04 | Negative export range | Rejected with rebase-to-frame-0 guidance |
| B05 | Japanese metadata/path content | UTF-8 manifest/package handling remains correct |
| B06 | BEAUTY / selected pass combinations | Folder tree and manifest match selected passes |
| B07 | Unsupported renderer/pass source | Fail explicitly; do not fabricate output |
| B08 | Existing unrelated compositor nodes | Preserved |
| B09 | Replacement mapping fails | Pending changes roll back; prior valid mapping preserved |
| B10 | Same-version package already has render/user payload | Build blocked; payload preserved |
| B11 | Empty same-version CutBridge scaffold | Supported safe refresh only |
| B12 | V001/V002/V003 package workflow | Versions coexist deterministically |
| B13 | Extension enable/disable/re-enable | No stale RNA registration error |
| B14 | Partial registration failure then retry | Transactional cleanup permits retry |
| B15 | JA → EN locale switch | Only locale/UI state changes; workflow data unchanged |
| B16 | Narrow ~245 px N-panel | Core JA/EN labels/values/actions materially readable |
| B17 | Validate Cut / Build Package in JA and EN | Same safety decision; localized user-facing text |
| B18 | Existing scene with no S9-specific values | Defaults to Manual mode; legacy package identity remains unchanged |
| B19 | Default Studio Preset | Resolves built-in data-only preset without external file access |
| B20 | Valid Custom JSON preset | Resolved naming/folders/passes/format/version/AE comp are deterministic |
| B21 | Invalid Custom JSON preset | Stable `PRESET_*` error; Build Package blocked before unsafe output |
| B22 | Custom preset file changes during Build Package | One validated in-memory snapshot remains authoritative for the whole build |
| B23 | S10B 3D handoff disabled | No `handoff_3d` payload; historical package/manifest behavior preserved |
| B24 | Supported active perspective camera | Evaluated world-space samples use S10A axis/timing contract |
| B25 | Explicitly marked animated Empty | Only the marked Empty is serialized; per-frame evaluated position is baked |
| B26 | Parented/constraint-influenced marked Empty | Evaluated world-space result is baked; hierarchy is not serialized/recreated |
| B27 | Camera shift / non-square pixel / unsupported camera type | Stable fail-closed `HANDOFF_*` diagnostic; package build blocked |
| B28 | Marked non-Empty / zero-scale / shear / reflection | Stable fail-closed diagnostic; no approximate handoff is emitted |
| B29 | Sampling changes current frame | Original Blender frame/subframe restored after success or failure |
| B30 | Valid S10B Build Package | Full manifest validates under Draft 2020-12 and contains bounded optional handoff data |
| B31 | Excessive marked Empties / frames / total samples | Safety limit error; no unbounded manifest generation |

## 3. After Effects contract / Build matrix

| ID | Scenario | Expected |
|---|---|---|
| A01 | Valid `cutbridge.json` | Package identity/FPS/frame information loads |
| A02 | Unsupported schema/version | Reject before project mutation |
| A03 | Unsafe absolute/traversal/escaped path | Reject before footage import |
| A04 | Required sequence missing frame | Build/import blocked with diagnostic |
| A05 | Optional sequence unavailable | Warning/skip within policy |
| A06 | Extra or mis-padded matching file | Diagnosed; never treated as the expected frame |
| A07 | Valid Japanese package/sequence path | Resolves without encoding failure |
| A08 | Existing artist same-name/source object | Not automatically adopted |
| A09 | Duplicate/moved/ambiguous managed object | Fail closed before unsafe mutation |
| A10 | Late Build failure | Newly created managed state rolls back; artist work preserved |
| A11 | Script/project reload | Verified managed state is rediscovered without duplication |
| A12 | Required managed layer deleted/de-tagged | QC reports ownership/source error; never clean PASS |
| A13 | Optional managed layer absent with valid optional source | Warning-only when otherwise unambiguous |
| A14 | S9 manifest includes optional `studio_preset` provenance | Existing AE behavior remains compatible; metadata does not create a new trust boundary |
| A15 | Preset-managed pass order/comp name resolved in manifest | AE consumes manifest contract; it never opens Studio Preset JSON |
| A16 | Manifest includes valid optional `handoff_3d` | Current S10B AE validator/build path remains compatible and does not create camera/null layers |

S10B deliberately has **no A17 native camera/null reconstruction claim**. That behavior belongs to S10C and must be added only with real-host evidence.

## 4. S6 revision-manager gate

Required regression coverage includes:

- producer-style V001/V002/V003 identity;
- strict revision token parsing and duplicate candidate rejection;
- package/tuple drift and delimiter-collision safety;
- required/optional pass-set compatibility policy;
- live ownership/source/container/FPS revalidation;
- staged import before source replacement;
- native-adapter use of `AVLayer.replaceSource(..., false)` rather than direct source assignment;
- validation/import/swap/commit failure rollback;
- historical-footage provenance;
- package-root/folder ambiguity blocking;
- Build/QC/reload consistency after successful revision.

Real native AE validation for S6 is recorded in issue #19. Green host-shaped tests are not a substitute for that evidence.

## 5. S7 QC+ gate

QC+ must remain deterministic and diagnostic-only.

Automated coverage must verify:

- stable `CBQ-*` identifiers;
- PASS / WARNING / ERROR severity;
- remediation text for every warning/error;
- required/optional sequence diagnostics;
- unexpected matching files;
- resolution, pixel aspect, FPS, and duration drift;
- managed footage/layer ownership state;
- stale/foreign/ambiguous managed tags;
- revision compatibility diagnostics;
- no adoption/import/deletion/retagging/source replacement/automatic repair from QC.

S7 real Adobe After Effects validation found and repaired native ExtendScript/revision-state defects before integration. Treat that evidence as the native gate, not the Node harness alone.

## 6. S8 localization / UX gate

### Blender

Automated and native validation established:

- Japanese first-class/default UI;
- deterministic English switch/fallback;
- no slash-combined pseudo-localization for primary controls;
- stable machine identifiers and canonical support detail;
- locale changes do not alter unrelated scene/package state;
- practical narrow-panel readability.

Final repaired S8 Blender native test passed on candidate `f477b745...` in Blender 5.2.1 LTS at approximately 245 px N-panel width.

### After Effects

Automated and native validation established:

- Japanese first-class/default UI;
- explicit English selection and persistence;
- `CBQ-*` codes and safety decisions remain locale-independent;
- missing/invalid `localization.js` yields deterministic English fallback;
- visible selector reflects the effective fallback locale;
- fallback/localization changes cause zero unintended project mutation;
- Build/QC/Revision remain fail-closed under fallback.

Final repaired S8 AE native test passed on candidate `f477b745...` in Adobe After Effects 2026 v26.3.0 Build 87.

## 7. S9 Studio Preset gate

### Schema and loader

The S9 regression suite establishes:

- built-in default exactly matches the published safe example;
- published example validates under Draft 2020-12;
- root/schema/schema-version/required-field validation;
- unknown fields rejected;
- UTF-8 JSON only;
- custom file size capped at 64 KiB;
- preset source path never appears in normalized manifest provenance.

### Naming and path safety

Required rejection coverage includes:

- absolute paths and `..` traversal;
- backslash/non-normalized role paths;
- overlapping/nested render/preview/camera trees;
- path separators/control characters in naming templates;
- unsupported/introspection placeholders;
- template format conversions/specifiers;
- sequence template missing `{pass}` or literal `####`.

Allowed placeholders remain:

`{project}`, `{episode}`, `{scene}`, `{cut}`, `{take}`, `{version}`, `{pass}`.

### Manual compatibility / snapshot

The historical `safe_token`, `version_token`, and `package_name` primitives remain authoritative for Manual mode and Blender↔AE identity parity.

For Custom JSON mode, one normalized preset snapshot is authoritative for the complete Build Package transaction; later valid file edits apply only to later builds.

AE continues to consume resolved manifest data and never parses Studio Preset JSON.

## 8. S10A camera/null contract gate

S10A automated coverage establishes only deterministic host-independent primitives:

- axis mapping `(x, y, z) -> (x, -z, y)`;
- proper handedness/basis behavior;
- composition-center position mapping;
- explicit positive spatial scale;
- frame → AE-time mapping;
- FOV → AE Zoom math;
- perspective/square-pixel/zero-shift MVP constraints;
- stable failure codes for invalid values/camera cases.

S10A explicitly rejects direct Blender Euler → AE Euler mapping as a contract.

## 9. S10B producer gate

### Schema/backward compatibility

Required static coverage establishes:

- historical manifests without `handoff_3d` remain valid;
- `handoff_3d.schema == "cutbridge-handoff-3d"`;
- `handoff_3d.schema_version == 1`;
- unknown members inside the handoff block fail schema validation;
- null source type is `EMPTY` only;
- bounded camera/null sample arrays;
- existing AE validation accepts the optional block without consuming it.

### Blender evaluated-world sampling

Required official `bpy==5.2.1` coverage establishes:

- feature is disabled by default;
- active camera is sampled through the evaluated dependency graph;
- marked Empties are sorted/serialized deterministically;
- unmarked objects are omitted;
- animation is sampled per integer export frame;
- parent transforms influence baked world result without hierarchy recreation;
- position, normalized basis, scale, camera forward/up, FOV and Zoom are serialized;
- source frame and AE time agree with S10A timing;
- current frame/subframe is restored in a `finally` path;
- unsupported camera/transform/marker/sample-count cases fail closed;
- Build Package emits a full schema-valid manifest when handoff is enabled.

### S10B integration evidence

- base `7b506d357faea08ea936daa90ccd0c94ea565f21`;
- exact candidate `2a222520da9dde7128dc1b9ddc1ed29b1e7a23b2`;
- candidate push CI `34429145031`: PASS;
- PR #51 event CI `34429245773`: PASS;
- merge `444a786e6f7a64143e50f933fa35ca84ea36138e`;
- post-merge `develop` CI `34429324559`: PASS.

## 10. Release-simulation gate

Every relevant branch/PR should simulate packaging using the canonical product version and verify:

- expected Blender ZIP;
- expected After Effects ZIP;
- `SHA256SUMS.txt`;
- `release-metadata.json`;
- archive contents and license inclusion;
- deterministic checksums for identical sources/toolchain;
- version/tag/channel/prerelease consistency;
- release authorization remains separate from build success.

A successful simulation does **not** authorize publication.

## 11. Manual / real-host release gates still required

Before a stable release claim, execute and record the appropriate real application/end-to-end checks, including:

- installation and normal use in supported Blender GUI builds;
- real render sequence production for release-target renderer/View Layer configurations;
- Blender → package → After Effects handoff using release-candidate artifacts;
- representative Build/QC/revision/save-reopen workflow;
- real filesystem/path behavior for the supported OS matrix;
- Studio Preset UI/file-selection usability where that behavior is part of the release claim;
- S10C native AE camera/null reconstruction and projection/orientation/timing parity before 3D handoff is user-facing;
- published release-asset checksum/content verification;
- production update-index/update-discovery verification;
- Japanese target-user validation appropriate to the claim.

Already-passed S6/S7/S8 native gates should not be relabeled as unexecuted, but they also do not automatically certify every release-target host/OS/workflow combination.

S9 does not require a new native AE gate because AE receives no preset parser or preset UI. S10B likewise does not claim AE reconstruction; producer automation is not a substitute for the S10C native host gate.

## 12. Repository/session merge gate

For bounded feature integration such as S10B:

- branch from the exact green `develop` baseline;
- keep `main` untouched;
- keep `release-authorization.json` unchanged/unapproved;
- keep issue #18 open;
- static validation passes on the exact candidate;
- release simulation passes;
- historical S6/S7/S8 and identity/localization regressions remain green;
- full Blender 5.2.1 RNA/runtime suite passes;
- PR targets `develop` and the exact head is unchanged;
- independent PR-event CI passes;
- merge uses the exact validated candidate;
- post-merge `develop` CI passes on the exact merge commit;
- repository status documentation is reconciled before declaring the session fully closed.

Only after those gates pass is S10B considered fully integrated and S10C eligible to begin.
