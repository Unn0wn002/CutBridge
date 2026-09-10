# CutBridge v0.2.3 — Test Plan

This plan describes the **S1–S9 integrated development baseline with S10 research in progress**. Automated tests are regression evidence; native GUI/end-to-end claims require real-host evidence.

The authoritative CI gate remains two jobs:

- `static-validation`;
- `blender-52-rna-runtime` using official `bpy==5.2.1`.

The Blender suite currently emits `Scene.use_nodes` deprecation warnings expected to matter for Blender 6.0; see [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).

## 1. Core automated gates

### Static / release / AE contract

CI must cover:

- canonical product-version synchronization;
- JSON schema/example validation;
- deterministic release packaging and SHA-256 checks;
- release authorization fail-closed behavior;
- AE manifest, path, sequence, pass, package-identity, ownership, revision, QC+, and localization contracts;
- Studio Preset schema/example/loader/security contracts;
- S10 pure spatial/FOV/timing research math;
- S10 native AE probe safety/tolerance contract and JavaScript syntax;
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
- S10 isolated synthetic camera/source projection probe;
- the complete pytest suite.

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
| B23 | S10 isolated front-camera fixture | Probe creates no user-scene dependency and removes every allocated probe data-block |
| B24 | S10 axis points through Blender `world_to_camera_view()` | Candidate AE projection agrees within **0.00005 px** source-side numeric precision |
| B25 | S10 50 mm / 36 mm perspective fixture | Blender horizontal FOV and derived AE Zoom remain dimensionally consistent; finite RNA quantization is recorded separately |

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

S10 adds **no production AE camera/null behavior yet**. Native S10 measurements are performed only by the research probe described in section 8.

## 4. S6 revision-manager gate

Required regression coverage includes producer-style V001/V002/V003 identity, strict revision parsing, tuple drift/collision safety, pass-set compatibility, live ownership revalidation, staged import, native source replacement, rollback, provenance, package-root ambiguity blocking, and Build/QC/reload consistency.

Real native AE validation for S6 is recorded in issue #19. Green host-shaped tests are not a substitute for that evidence.

## 5. S7 QC+ gate

QC+ must remain deterministic and diagnostic-only. Coverage verifies stable `CBQ-*` identifiers, PASS/WARNING/ERROR severity, remediation, sequence/comp/ownership/revision diagnostics, and no adoption/import/deletion/retagging/source replacement/automatic repair.

S7 real Adobe After Effects validation found and repaired native ExtendScript/revision-state defects before integration.

## 6. S8 localization / UX gate

S8 native validation established Japanese-first/default UI, deterministic English fallback, stable machine identifiers, non-mutating locale changes, and practical narrow-panel behavior. Final repaired gates passed in Blender 5.2.1 LTS and Adobe After Effects 2026 v26.3.0 Build 87.

## 7. S9 Studio Preset gate

S9 coverage establishes:

- built-in default equals published example and schema;
- strict schema/unknown-field/loader validation;
- UTF-8 JSON only and 64 KiB cap;
- source path never enters manifest provenance;
- unsafe/overlapping paths and unsafe templates rejected;
- only allowed passes/formats/version bounds accepted;
- Manual identity remains unchanged;
- one custom-preset snapshot is authoritative for one Build Package transaction;
- AE stays a resolved-manifest consumer.

S9 exact candidate/PR/post-merge CI is recorded in issue #44 and `COMPLETION_STATUS.md`.

## 8. S10 Camera / Null research gate

### 8.1 Research-only boundary

Until the native evidence is complete:

- production `cutbridge.json` continues to expose only the legacy camera-name string;
- `CutBridge.jsx` does not create a managed 3D camera/null from S10 data;
- no production manifest schema is changed for camera/null transforms;
- no S5/S6/S7 ownership/revision/QC behavior is weakened;
- no release authorization or `main` change is part of S10.

### 8.2 Candidate coordinate basis

Research candidate only:

```text
Blender (X, Y, Z) → AE (X, -Z, Y)
```

The basis matrix must remain orthonormal with determinant `+1` and axis tests must prove:

- Blender +X → AE +X;
- Blender +Y → AE +Z;
- Blender +Z → AE -Y.

### 8.3 Pure math / timing gate

Automated tests must verify:

- finite vector/point conversion;
- composition-center translation;
- horizontal FOV from lens/sensor width;
- AE Zoom equation;
- depth-aware projection for the synthetic centered camera;
- frame-to-time mapping `(frame - frameStart) / fps`, including frame 0 and fractional FPS;
- invalid dimensions/FPS/FOV/scale fail closed.

### 8.4 Blender source-side probe

The exact first fixture is:

- 1920×1080 square-pixel composition/render;
- perspective camera at `(0,-10,0)`;
- exact evaluated basis: local +X→world +X, local +Y→world +Z, local -Z→world +Y;
- 50 mm lens;
- 36 mm horizontal sensor width;
- five world points: origin, +X, +Y, +Z, mixed +XYZ;
- research spatial scale 100 px/Blender-unit.

The probe must use Blender's own `world_to_camera_view()` and remove its synthetic scene/camera data in `finally`.

Blender 5.2 source-side projection comparison is bounded at **≤ 0.00005 px**. This tolerance is intentionally separate from and 1000× tighter than the native AE threshold. It accommodates measured finite-precision projection/RNA behavior; it is not permission to adjust the coordinate mapping to fit a test.

### 8.5 Native After Effects gate — issue #47

Run `tools/research/s10_ae_probe.jsx` in the real AE validation host.

The probe must:

- require an existing project and explicit user confirmation;
- create one uniquely named disposable comp;
- create only probe camera/null layers in that comp;
- set the candidate camera Position / Point of Interest / Zoom;
- evaluate fixture null projection through native `toComp()`;
- compare all five points against expected coordinates;
- require **maximum error ≤ 0.05 px**;
- remove the disposable comp on success and failure;
- force FAIL if cleanup fails;
- write JSON only after explicit Save dialog;
- record AE version/build and OS.

Do not widen the 0.05 px threshold merely to obtain PASS. If the candidate fails, revise the model from the measurements and rerun.

### 8.6 S10 runtime decision gate

A green research harness alone does not authorize production camera/null creation.

Before runtime implementation, also investigate:

- arbitrary camera orientation and a stable rotation representation;
- Empty/camera parenting chains;
- constraint/evaluated-transform policy;
- perspective sensor-fit variants;
- production spatial-scale policy;
- managed AE camera/null ownership, reload, collision, rollback, revision, and QC behavior.

S10 may conclude as **investigation PASS / runtime deferred** if this evidence is not sufficient for a safe minimal production subset.

Reference: [CAMERA_NULL_HANDOFF.md](CAMERA_NULL_HANDOFF.md).

## 9. Release-simulation gate

Every relevant branch/PR should simulate packaging using the canonical product version and verify expected Blender/AE ZIPs, `SHA256SUMS.txt`, release metadata, archive/license contents, deterministic checksums, version/channel consistency, and separation between build success and release authorization.

A successful simulation does **not** authorize publication.

## 10. Manual / real-host release gates still required

Before a stable release claim, execute and record appropriate real application/end-to-end checks: supported Blender GUI use, real render sequences, Blender→package→AE handoff, Build/QC/revision/save-reopen, filesystem/OS behavior, Studio Preset usability where claimed, release-asset verification, production update-index verification, and Japanese target-user validation.

Already-passed S6/S7/S8 native gates should not be relabeled as unexecuted, but they do not automatically certify every release-target host/OS/workflow combination.

## 11. Repository/session merge gate

For an S10 **research-harness integration increment**:

- branch from exact green post-S9 `develop` baseline;
- production runtime/manifest behavior remains unchanged;
- `main` untouched;
- `release-authorization.json` unchanged and unapproved;
- issues #46 and #47 remain open while native S10 evidence is pending;
- exact candidate static validation passes;
- deterministic release simulation passes;
- S6/S7/S8/S9 regressions remain green;
- S10 pure math/probe contract tests pass;
- full Blender 5.2.1 suite including source projection probe passes;
- PR targets `develop`;
- PR-event CI passes on the exact head;
- post-merge `develop` CI passes.

Merging a research harness does **not** mark S10 complete. S11 is not eligible to start until S10 reaches an explicit evidence-backed completion decision.
