# CutBridge v0.2.3 — Test Plan

This plan describes the **S1–S9 development baseline**. Automated tests are regression evidence; native GUI/end-to-end claims require real-host evidence.

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
- S9 Studio Preset integration through the complete pytest suite.

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
| A15 | Preset-managed pass order/comp name is already resolved in manifest | AE consumes manifest contract; it never opens Studio Preset JSON |

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

The S9 regression suite must establish:

- built-in default exactly matches the published safe example;
- published example validates under the Draft 2020-12 Studio Preset schema;
- root/schema/schema-version/required-field validation;
- unknown fields rejected;
- UTF-8 JSON only;
- custom file size capped at 64 KiB;
- preset source path never appears in normalized manifest provenance.

### Naming and path safety

Required rejection coverage:

- absolute paths;
- `..` parent traversal;
- backslash/non-normalized folder paths;
- overlapping/nested render/preview/camera folder trees;
- path separators or control characters in naming templates;
- unsupported placeholders such as object/introspection syntax;
- template format conversions/specifiers;
- sequence template missing `{pass}`;
- sequence template missing literal `####`.

Allowed placeholders are limited to:

`{project}`, `{episode}`, `{scene}`, `{cut}`, `{take}`, `{version}`, `{pass}`.

### Pass / output / version behavior

Required coverage:

- only BEAUTY / LINE / SHADOW / DEPTH;
- no duplicate pass definitions;
- explicit boolean `required` value;
- array order preserved into manifest pass order / `ae.layer_order`;
- only PNG / OPEN_EXR / TIFF;
- version prefix/padding bounded;
- numeric manifest `version` remains separate from display `version_label`.

### Manual compatibility

S9 must not rewrite the historical package identity contract.

The existing self-contained producer primitives remain authoritative:

- `safe_token`;
- `version_token` → `V###`;
- `package_name` → `{project}_{episode}_{scene}_{cut}_{take}_{version}`.

Existing AE parity tests must continue extracting/executing those functions independently and passing unchanged.

### Build snapshot consistency

For Custom JSON mode:

1. validate and normalize the selected file;
2. freeze the normalized data for one Build Package transaction;
3. use that same snapshot for package naming, compositor mapping, directory creation, and manifest generation;
4. clear the snapshot after the transaction;
5. later builds may load a newly edited valid preset.

Automated regression must edit the source JSON during an active snapshot and prove the current build still reads the original snapshot, while a later load reads the updated file.

### AE boundary

No S9 preset parser is added to After Effects.

Existing S4–S8 AE tests must stay green, proving that AE continues to consume resolved manifest data. Optional `studio_preset` provenance must not be required for old manifests.

## 8. Release-simulation gate

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

## 9. Manual / real-host release gates still required

Before a stable release claim, execute and record the appropriate real application/end-to-end checks, including:

- installation and normal use in supported Blender GUI builds;
- real render sequence production for release-target renderer/View Layer configurations;
- Blender → package → After Effects handoff using release-candidate artifacts;
- representative Build/QC/revision/save-reopen workflow;
- real filesystem/path behavior for the supported OS matrix;
- Studio Preset UI/file-selection usability where that behavior is part of the release claim;
- published release-asset checksum/content verification;
- production update-index/update-discovery verification;
- Japanese target-user validation appropriate to the claim.

Already-passed S6/S7/S8 native gates should not be relabeled as unexecuted, but they also do not automatically certify every release-target host/OS/workflow combination.

S9 does not require a new native After Effects gate because AE receives no new preset-file parser or preset UI. Do not fabricate native Blender GUI evidence merely from `bpy` automation.

## 10. Repository/session merge gate

For S9 integration:

- implementation and documentation are on a feature branch from the exact green `develop` baseline;
- `main` remains untouched;
- `release-authorization.json` remains unchanged and unapproved;
- issue #18 remains open;
- static validation passes on the exact candidate;
- release simulation passes;
- S6/S7/S8 regression suites and JS syntax pass;
- full Blender 5.2.1 RNA/runtime suite passes;
- PR targets `develop`;
- after merge, `develop` CI passes on the exact merge commit.

Only after those gates pass is S9 considered integrated and S10 eligible to begin.