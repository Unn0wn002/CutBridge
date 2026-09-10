# CutBridge v0.2.3 — Test Plan

This plan describes the **S1–S13 unreleased development baseline**. Automated tests are regression evidence; native GUI/end-to-end claims require real-host evidence.

The authoritative CI gate remains two jobs:

- `static-validation`;
- `blender-52-rna-runtime` using official `bpy==5.2.1`.

Latest integrated `develop` after S13F is:

`0a86d9a0605e1dd9714ef35a547693de76f714f4`

Latest post-merge evidence on that SHA:

- static suite: **132 passed + 2 subtests**;
- Blender/runtime suite: **245 passed + 2 subtests**;
- Blender 5.2.1 RNA lifecycle: PASS;
- deterministic release simulation/checksum verification: PASS;
- S13 native-host-shaped revision regression: PASS.

The Blender suite still emits `Scene.use_nodes` deprecation warnings relevant to Blender 6.0. Pinned Actions also emit Node-runtime deprecation warnings; see `TECHNICAL_DEBT.md`.

## 1. Core automated gates

### Static / release / AE contract

CI must cover:

- canonical product-version synchronization;
- JSON schema/example validation;
- deterministic release packaging and SHA-256 checks;
- release authorization fail-closed behavior;
- AE manifest/path/sequence/pass/package identity/ownership/revision/QC+/localization contracts;
- Studio Preset schema/loader/security contracts;
- S10A camera/null coordinate, timing, FOV/Zoom, and fail-closed primitives;
- S10B optional `handoff_3d` schema/backward compatibility;
- S10C Camera/3D Null validation, ownership, collision, and reconstruction regressions;
- S13 3D revision native-host-shaped regression;
- status/release-readiness documentation guards;
- JS/ExtendScript syntax for shipped AE runtime files;
- Japanese/English localization fallback and stable machine identifiers.

Missing mandatory dependencies must fail rather than silently skip coverage.

### Blender 5.2.1 runtime

Authoritative CI installs official `bpy==5.2.1` and verifies:

- register → unregister → register → unregister lifecycle;
- scene metadata and validation behavior;
- render mapping and rollback;
- package generation/integrity;
- filename/manifest contracts;
- Japanese/UTF-8 handling;
- localization behavior;
- Studio Preset integration;
- evaluated-world Camera/marked-Empty sampling;
- animated/parented Empty world-space baking;
- frame restoration and fail-closed handoff cases;
- full package generation with schema-valid optional `handoff_3d`.

## 2. Blender behavioral matrix

| ID | Scenario | Expected |
|---|---|---|
| B01 | Required metadata missing | Actionable validation error; Build blocked |
| B02 | No active Camera | Validation error |
| B03 | Valid non-negative frame range | Manifest frame count/FPS agree with scene |
| B04 | Negative export range | Rejected with rebase guidance |
| B05 | Japanese metadata/path | UTF-8 handling remains correct |
| B06 | BEAUTY / selected pass combinations | Folder tree and manifest match selection |
| B07 | Unsupported renderer/pass source | Fail explicitly |
| B08 | Existing unrelated compositor nodes | Preserved |
| B09 | Mapping failure | Pending changes roll back |
| B10 | Same-version package with payload | Build blocked; payload preserved |
| B11 | Empty same-version CutBridge scaffold | Safe refresh only |
| B12 | V001/V002/V003 package workflow | Versions coexist deterministically |
| B13 | Extension enable/disable/re-enable | No stale RNA registration error |
| B14 | Partial registration failure then retry | Transactional cleanup permits retry |
| B15 | JA → EN locale switch | UI state only; workflow data unchanged |
| B16 | Narrow N-panel | Core JA/EN labels/actions remain usable |
| B17 | Validate / Build in JA and EN | Same safety decision; localized text |
| B18 | Existing pre-S9 scene | Defaults to Manual; identity unchanged |
| B19 | Default Studio Preset | Built-in declarative preset resolves |
| B20 | Valid Custom JSON | Deterministic resolved behavior |
| B21 | Invalid Custom JSON | Stable `PRESET_*` failure; Build blocked |
| B22 | Preset file changes mid-Build | One validated snapshot remains authoritative |
| B23 | 3D handoff disabled | No `handoff_3d`; historical behavior preserved |
| B24 | Supported perspective Camera | Evaluated-world samples follow S10 contract |
| B25 | Marked animated Empty | Only marked Empty serialized |
| B26 | Parented/constrained marked Empty | World result baked; hierarchy not recreated |
| B27 | Shift/non-square/unsupported Camera | Fail closed |
| B28 | Invalid marked object/transform | Fail closed; no approximation |
| B29 | Sampling changes scene frame | Original frame/subframe restored |
| B30 | Valid handoff Build | Full schema-valid bounded manifest |
| B31 | Excessive frame/object/sample counts | Safety limit error |

## 3. After Effects Build / contract matrix

| ID | Scenario | Expected |
|---|---|---|
| A01 | Valid `cutbridge.json` | Package identity/FPS/frame data loads |
| A02 | Unsupported schema/version | Reject before mutation |
| A03 | Unsafe path | Reject before footage import |
| A04 | Required sequence missing frame | Build/import blocked |
| A05 | Optional sequence missing | Warning/skip within policy |
| A06 | Extra/mis-padded file | Diagnosed; not accepted as expected frame |
| A07 | Valid Japanese path | Resolves correctly |
| A08 | Artist same-name/source object | Not automatically adopted |
| A09 | Ambiguous managed object | Fail closed |
| A10 | Late Build failure | Newly created state rolls back |
| A11 | Script/project reload | Managed state rediscovered without duplication |
| A12 | Required managed layer missing/de-tagged | QC error |
| A13 | Valid absent optional layer | Warning-only when unambiguous |
| A14 | Optional Studio Preset provenance | Manifest-compatible; no new trust boundary |
| A15 | Preset-managed order/comp | AE consumes manifest only |
| A16 | Valid optional `handoff_3d` | Supported schema accepted |
| A17 | Valid S10C handoff | Managed Camera + 3D Nulls reconstructed |
| A18 | Repeated Build | Verified managed 3D layers reused |
| A19 | Unmanaged Camera/Null name collision | Fail closed; artist object preserved |
| A20 | Malformed/unsupported `handoff_3d` | Reject before unsafe reconstruction |

## 4. S6 revision-manager regression gate

Coverage must retain V001/V002/V003 identity, duplicate-candidate rejection, package/tuple drift detection, required/optional pass policy, live ownership/source/container/FPS revalidation, staging, source replacement, rollback, provenance, package-root ambiguity blocking, and Build/QC/reload consistency.

## 5. S7 QC+ gate

QC+ remains deterministic and diagnostic-only. Tests verify stable `CBQ-*`, severity, remediation, sequence/comp/ownership/revision checks, stale/foreign/ambiguous state, and absence of automatic repair/adoption.

## 6. S8 localization / UX gate

Automated and native evidence establishes Japanese-first display, deterministic English fallback, locale-independent machine identifiers/safety decisions, narrow-panel readability, and no project mutation from localization fallback.

## 7. S9 Studio Preset gate

Coverage retains strict schema/version/field/path/template/pass/format behavior, size/encoding limits, Manual backward compatibility, one-build snapshot consistency, no preset-source-path disclosure, and AE manifest-only consumption.

## 8. S10A/B/C handoff gates

S10A coverage retains:

- `(x,y,z) -> (x,-z,y)` axis mapping;
- composition-center origin;
- explicit scale;
- `(frame-frame_start)/fps` time mapping;
- FOV→Zoom math;
- fail-closed perspective/square-pixel/zero-shift boundary.

S10B coverage retains:

- backward-compatible optional schema;
- `EMPTY`-only Null sources;
- bounded samples;
- evaluated world-space sampling;
- deterministic marked-Empty selection;
- frame restoration;
- unsupported-case rejection.

S10C native evidence remains bounded to Adobe After Effects 2026 Build 87 (`26.3x87`) on Windows 11 using Blender 5.2.1-produced handoff data. Recorded results include maximum projection error `0.00018066 px`, QC+ 10/10, zero duplicates on repeated Build, collision rejection, and persistence.

## 9. S12 release-target end-to-end gate

Status: **PASS after S13F repair chain**.

The initial native campaign produced real failures and remained fail-closed. S12 was reconciled to PASS only after the repaired path succeeded on exact native-tested commit:

`9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`

Required behavior that passed for the repaired tested scope:

- V001 Build/QC baseline;
- V001→V002 compatible revision;
- V002→V003 compatible revision;
- Camera Position/POI/Zoom refresh;
- Null Position/Scale refresh;
- version-scoped 3D ownership migration;
- QC clean;
- artist-state preservation;
- zero duplicate managed Camera/Null layers;
- save/close/reopen/reload persistence.

The current repository lacks a final committed structured `s12-evidence.json` PASS artifact. This is tracked as an evidence-traceability limitation; do not fabricate retroactive hashes/evidence paths. See `S12_S13_EVIDENCE_SUMMARY.md`.

## 10. S13 native revision-repair gate

S13 regression coverage must retain the actual repaired failure modes:

- stale version-scoped Camera/Null ownership/data;
- unsafe Camera Point-of-Interest access forms;
- mandatory canonical-CI execution of the host-shaped 3D revision test;
- rejection of sample-topology drift;
- rejection of destructive key removal/single-key mutation in the host-shaped regression;
- bulk animated-property writes through `setValuesAtTimes()` after key topology/time preflight;
- V001→V002→V003 ownership/data/QC consistency;
- zero duplicate managed Camera/Null layers.

Native-tested final source `9c99ae23...` passed the full repaired path before intact integration through PR #68.

## 11. Documentation / state regression gate

Status tests must validate **semantic live-state invariants**, not freeze a historical session as “next.”

Current required assertions include:

- README identifies latest integrated `develop` and S12/S13 completion;
- completion status identifies S1–S13 integrated/completed and S14 next;
- release readiness remains `UNRELEASED / PUBLICATION BLOCKED`;
- issue #18 remains an external governance blocker;
- release authorization remains false;
- S12 structured-evidence limitation is stated truthfully;
- deliberate promotion is not a blind `develop`→`main` merge;
- no documentation claims v0.2.3 is published or broadly certified.

## 12. Release-simulation gate

Every relevant candidate/PR must simulate packaging and verify:

- Blender ZIP;
- After Effects ZIP;
- `SHA256SUMS.txt`;
- `release-metadata.json`;
- archive contents and license inclusion;
- deterministic checksums for identical inputs;
- version/tag/channel/prerelease consistency;
- separation between build success and release authorization.

A successful simulation does **not** authorize publication.

## 13. S14 target-user validation gate

Before broad Japanese production-usability claims:

- define real user tasks and acceptance criteria;
- use actual target users when making corresponding usability claims;
- record task completion, friction, rework, terminology feedback, and material blockers;
- repair material findings and rerun affected tasks;
- never fabricate participants or measurements.

## 14. Repository / promotion gate

For bounded integration on `develop`:

- branch from exact green `develop`;
- keep `main` untouched unless executing a deliberate promotion session;
- keep `release-authorization.json` unapproved;
- keep #18 open until governance exists and is tested;
- require final candidate CI;
- require PR-event CI;
- merge exact validated head;
- require post-merge `develop` CI;
- reconcile status/issues after merge.

For release promotion:

- compare `main...candidate` file-by-file;
- preserve required main-side release-lock intent;
- preserve the hardened `develop` release workflow;
- produce an explicit promotion tree/commit;
- run authoritative CI on exact promoted `main`;
- keep release authorization false until every release prerequisite is complete.

The canonical publication checklist is `RELEASE_READINESS.md`.