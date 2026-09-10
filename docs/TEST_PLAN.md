# CutBridge v0.2.3 — Test Plan

This plan describes the **S1–S11 unreleased development baseline**. Automated tests are regression evidence; native GUI/end-to-end claims require real-host evidence.

The authoritative CI gate remains two jobs:

- `static-validation`;
- `blender-52-rna-runtime` using official `bpy==5.2.1`.

The Blender suite still emits `Scene.use_nodes` deprecation warnings expected to matter for Blender 6.0. Pinned GitHub Actions revisions that target deprecated Node 20 runtimes are also tracked as technical debt; see [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).

## 1. Core automated gates

### Static / release / AE contract

CI must run maintained pytest and Node suites covering:

- canonical product-version synchronization;
- JSON schema/example validation;
- deterministic release packaging and SHA-256 checks;
- release authorization fail-closed behavior;
- AE manifest, path, sequence, pass, package-identity, ownership, revision, QC+, localization, and S10C reconstruction contracts;
- Studio Preset schema/example/loader/security contracts;
- S10A camera/null coordinate, timing, FOV/Zoom, and fail-closed primitives;
- S10B optional `handoff_3d` schema/backward compatibility;
- S10C managed camera/3D Null validation, ownership, collision, and projection-parity regressions;
- S11 documentation/release-readiness guards;
- JS/ExtendScript syntax for shipped AE runtime files;
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
- full package generation with schema-valid optional `handoff_3d`;
- all static documentation/readiness regressions that are part of the complete pytest suite.

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
| B18 | Existing scene with no S9-specific values | Defaults to Manual; historical package identity unchanged |
| B19 | Default Studio Preset | Resolves built-in data-only preset |
| B20 | Valid Custom JSON preset | Resolved naming/folders/passes/format/version/AE comp deterministic |
| B21 | Invalid Custom JSON preset | Stable `PRESET_*` error; Build blocked |
| B22 | Custom preset file changes during Build | One validated in-memory snapshot remains authoritative |
| B23 | S10 3D handoff disabled | No `handoff_3d`; historical behavior preserved |
| B24 | Supported active perspective camera | Evaluated world samples use S10A axis/timing contract |
| B25 | Explicitly marked animated Empty | Only marked Empty serialized; per-frame evaluated position baked |
| B26 | Parented/constraint-influenced marked Empty | Evaluated world result baked; hierarchy not recreated |
| B27 | Shift/non-square/unsupported camera type | Fail-closed `HANDOFF_*`; package blocked |
| B28 | Marked non-Empty / zero-scale / shear / reflection | Fail closed; no approximate handoff |
| B29 | Sampling changes frame | Original frame/subframe restored on success/failure |
| B30 | Valid handoff Build Package | Full manifest schema-valid with bounded optional handoff data |
| B31 | Excessive Empty/frame/sample counts | Safety limit error; no unbounded manifest |

## 3. After Effects contract / Build matrix

| ID | Scenario | Expected |
|---|---|---|
| A01 | Valid `cutbridge.json` | Package identity/FPS/frame information loads |
| A02 | Unsupported schema/version | Reject before project mutation |
| A03 | Unsafe absolute/traversal/escaped path | Reject before footage import |
| A04 | Required sequence missing frame | Build/import blocked |
| A05 | Optional sequence unavailable | Warning/skip within policy |
| A06 | Extra or mis-padded matching file | Diagnosed; not treated as expected frame |
| A07 | Valid Japanese package/sequence path | Resolves without encoding failure |
| A08 | Existing artist same-name/source object | Not automatically adopted |
| A09 | Duplicate/moved/ambiguous managed object | Fail closed before unsafe mutation |
| A10 | Late Build failure | Newly created managed state rolls back |
| A11 | Script/project reload | Managed state rediscovered without duplication |
| A12 | Required managed layer deleted/de-tagged | QC ownership/source error; never clean PASS |
| A13 | Valid absent optional layer | Warning-only when otherwise unambiguous |
| A14 | Optional `studio_preset` provenance | Compatible; no new AE trust boundary |
| A15 | Preset-managed order/comp in manifest | AE consumes manifest; never opens preset JSON |
| A16 | Valid optional `handoff_3d` | Manifest validation accepts supported schema |
| A17 | Valid S10C handoff | Managed perspective camera + 3D Null subset reconstructed |
| A18 | Repeated S10C Build | Existing verified managed camera/null reused; no duplicates |
| A19 | Same-name unmanaged camera/null | Fail closed; artist object preserved |
| A20 | Unsupported/malformed `handoff_3d` | Reject before unsafe reconstruction |

## 4. S6 revision-manager gate

Regression coverage includes producer-style V001/V002/V003 identity, revision parsing, duplicate-candidate rejection, package/tuple drift, required/optional pass-set policy, live ownership/source/container/FPS revalidation, staged import, native `AVLayer.replaceSource(..., false)`, rollback, provenance, package-root ambiguity blocking, and Build/QC/reload consistency.

Native S6 evidence is recorded separately; host-shaped tests are not a substitute.

## 5. S7 QC+ gate

QC+ must remain deterministic and diagnostic-only. Coverage verifies stable `CBQ-*`, severity, remediation, sequence/comp/ownership/revision checks, stale/foreign/ambiguous state, and absence of automatic adoption/import/deletion/retag/source replacement/repair.

## 6. S8 localization / UX gate

Automated and native gates establish Japanese-first display, deterministic English fallback, locale-independent machine identifiers/safety decisions, narrow-panel readability, and zero unintended project mutation from localization fallback.

## 7. S9 Studio Preset gate

Coverage establishes strict schema/version/field/path/template/pass/format rules, 64 KiB UTF-8 custom-loader bound, safe published example, Manual backward compatibility, one-build custom-preset snapshot consistency, no preset-source-path disclosure, and AE manifest-only consumption.

## 8. S10A camera/null contract gate

Coverage establishes axis `(x,y,z)->(x,-z,y)`, handedness, composition-center mapping, explicit positive scale, frame→AE-time mapping, FOV→Zoom math, supported perspective/square-pixel/zero-shift boundaries, and stable failure codes. Direct Blender Euler→AE Euler mapping is not an approved contract.

## 9. S10B producer gate

Coverage establishes backward-compatible optional schema v1, strict fields, `EMPTY`-only null sources, bounded samples, default-off producer behavior, evaluated dependency-graph sampling, deterministic marked-Empty selection, world-space baking, frame restoration, unsupported-case rejection, and full Build Package integration.

## 10. S10C native reconstruction gate

S10C is not considered proven from Node tests alone. Recorded native evidence comes from **Adobe After Effects 2026 Build 87 (`26.3x87`) on Windows 11** using Blender 5.2.1 LTS-produced handoff data.

Recorded native results:

- managed camera + 3D Null reconstruction PASS;
- deterministic ordering PASS;
- maximum 2D projection error `0.00018066 px`;
- acceptance gate `<= 0.05 px`;
- QC+ 10/10 PASS;
- repeated Build 0 duplicate managed layers;
- unmanaged camera/null collisions rejected fail-closed;
- project persistence PASS.

This is bounded native evidence for the tested S10C scope, not blanket certification of the AE 2024–2026 target range.

## 11. S11 QA / Docs / Release Engineering gate

S11 is a documentation, QA, compatibility-claim, and release-readiness reconciliation session. It must not use documentation work as a reason to broaden release authorization or mutate `main`.

Required S11 assertions:

- EN Quick Start describes the workflow through S10C and points to S12 next;
- JA Quick Start describes the same contract/safety boundary;
- `HANDOFF_3D.md` no longer claims AE reconstruction is future work;
- AE `INSTALL.md` records S10C without blanket AE certification;
- `COMPATIBILITY.md` identifies the exact tested native AE host and distinguishes bounded evidence from broad certification;
- `RELEASE_READINESS.md` states `UNRELEASED / PUBLICATION BLOCKED`, #18 remains external, S12 is required, promotion is not a blind merge, and production update verification is separate from GitHub Release publication;
- existing release-hygiene and authorization tests remain green;
- current release builder/workflow is not redesigned without a reproducible defect.

S11 CI chronology:

- intermediate head `13899401e8afc857b6c1ec0527c142f778f56a8e`, run `34449966185`: static PASS; Blender RNA PASS; complete pytest 235 PASS / 1 FAIL / 62 warnings / 2 subtests PASS. Sole failure was a new phrase-specific S11 documentation assertion.
- corrected head `818d9b8275319194c8c42329b8a139b35239e1aa`, run `34450066759`: both authoritative jobs PASS after the assertion was changed to test the semantic managed-camera and managed-3D-Null requirements separately.

Any later S11 state-document change creates a new final candidate SHA and requires another complete candidate CI before PR/merge.

## 12. Release-simulation gate

Every relevant candidate/PR must simulate packaging and verify:

- Blender ZIP;
- After Effects ZIP;
- `SHA256SUMS.txt`;
- `release-metadata.json`;
- archive contents and license inclusion;
- deterministic checksums for identical inputs;
- version/tag/channel/prerelease consistency;
- release authorization remains separate from build success.

A successful simulation does **not** authorize publication.

## 13. Real-host release gates still required

Already-passed S6/S7/S8/S10C native gates should not be relabeled as unexecuted, but they do not certify every release-target host/OS/workflow combination.

S12 must execute the broader release-target Blender → package → AE campaign using exact candidate artifacts, including installation, representative real render sequences, Build/QC, V001→V002→V003 compatible revisions, save-close-reopen/reload, artist-state preservation where claimed, path/Unicode behavior appropriate to the target, and S10C handoff from candidate artifacts.

Published-asset checksum/content verification and production update-index verification can occur only after a real authorized publication and remain separate gates.

Japanese target-user evidence must be recorded before making corresponding production-usability claims.

The canonical checklist is [RELEASE_READINESS.md](RELEASE_READINESS.md).

## 14. Repository/session merge gate

For S11 and later bounded integration:

- branch from exact green `develop`;
- keep `main` untouched;
- keep `release-authorization.json` unapproved;
- keep #18 open;
- exact final candidate gets both authoritative CI jobs PASS;
- release simulation and historical regression suites remain green;
- PR targets `develop` with unchanged exact head;
- PR-event CI passes;
- merge uses exact validated head;
- post-merge `develop` CI passes;
- status/issues are reconciled to the exact final merge.

Only after these gates pass is S11 fully integrated and S12 eligible to begin.
