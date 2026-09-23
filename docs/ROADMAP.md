# CutBridge Roadmap

Status reconciled through the v0.2.4 release-authorization gate. Stable v0.2.3 publication and production D1 distribution are complete; v0.2.4 has been promoted to protected `main` and its exact stable/non-prerelease tuple is authorized on the release branch, but no v0.2.4 tag, GitHub Release, or production distribution entry exists yet. Session numbers describe bounded product work and do not guarantee public release numbers.

## Completed foundation — S1–S9

### S1 — Baseline and release packaging
Completed.

Deterministic Blender + After Effects packaging, version consistency/checksums, GPL inclusion, output safety, and baseline release hygiene.

### S2 — Blender Render Mapping
Completed.

BEAUTY / LINE / SHADOW / DEPTH mapping, renderer/View Layer validation, deterministic output paths, and transactional artist-node preservation.

### S3 — Blender Production Hardening
Completed.

Package-target safety, same-version payload protection, V001/V002/V003 coexistence, package integrity, and Japanese/UTF-8 filesystem handling.

### S4 — AE Handoff Contract Hardening
Completed.

Schema/version gates, non-negative frame contract, safe package-relative paths, required/optional pass semantics, exact sequence coverage, safe legacy JSON parsing, and product-version enforcement.

### S5 — AE Import & Composition Reliability
Completed.

Deterministic managed ownership, repeated-build/reload safety, collision/ambiguity blocking, rollback, package-structure validation, and stricter QC ownership behavior.

### S6 — Non-Destructive Revision Manager
Completed and native-host validated.

Compatible revisions replace only verified managed sources, preserve unrelated artist work, retain historical provenance, and fail closed on incompatible/ambiguous state.

### S7 — QC+
Completed and native-host validated.

Deterministic `CBQ-*` diagnostics with severity/remediation, sequence/comp/ownership/revision checks, and diagnostic-only behavior.

### S8 — Japanese-First UX
Completed and native-host validated.

Japanese-first UI with deterministic English fallback in Blender and After Effects while stable machine identifiers and safety decisions remain locale-independent.

### S8.5 — Repository State Reconciliation
Completed.

Documentation/status maintenance after S8; no runtime or release authorization change.

### S9 — Studio Presets
Completed.

Safe declarative Manual / CutBridge Default / Custom JSON modes with deterministic package/folder/pass/version/comp conventions and no executable preset trust boundary in AE.

## S10 — Camera / Null handoff

### S10A — Contract investigation
**Completed and integrated.**

Established the bounded Blender ↔ After Effects coordinate/timing/camera/null contract, including `(x, y, z) -> (x, -z, y)`, composition-center positions, explicit spatial scale, frame-time mapping, FOV/Zoom primitives, and evaluated-world orientation strategy.

### S10B — Optional 3D handoff producer
**Completed and integrated.**

Added the optional/versioned `handoff_3d` producer, evaluated-world active camera and explicitly marked Empty baking, bounded sample counts, frame restoration, and fail-closed unsupported camera/transform behavior.

### S10C — Native After Effects reconstruction / parity
**Completed / integrated / native-host validated.**

Delivered managed AE Camera/3D Null reconstruction with idempotent rebuild and ownership/collision safety.

Native AE 2026 Build 87 / Windows 11 evidence includes:

- maximum projection error `0.00018066 px` against `<= 0.05 px`;
- QC+ 10/10 PASS;
- repeated Build with zero duplicate managed Camera/Null layers;
- unmanaged collision rejection;
- save/reopen persistence.

## S11 — QA / Docs / Release Engineering

**Completed and integrated.**

Delivered EN/JA onboarding, AE installation guidance, bounded compatibility claims, release-readiness architecture, release simulation/authorization regression coverage, and technical-debt tracking.

## S12 — Release-Target End-to-End Validation

**PASS / closed after S13F repair chain.**

The initial real-host campaign correctly exposed defects and remained `FAIL_REPAIR_REQUIRED` until repairs were verified. The campaign was reconciled to PASS only after the repaired native path completed the required V001→V002→V003 behavior and repository integration gates.

See `S12_E2E_VALIDATION.md` and `S12_S13_EVIDENCE_SUMMARY.md`.

## S13 — Real-Host Revision Repair

**PASS / integrated / native-host validated.**

The S13 sequence repaired actual findings from S12 instead of inventing speculative feature work:

- Camera/Null version-scoped ownership/data migration;
- native Camera Point-of-Interest access failure;
- missing canonical-CI execution of the host-shaped regression;
- native failure from repeated key removal/per-key writes.

Final native-tested source:

`9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`

Integration:

- exact-head push CI `34503571091`: PASS;
- PR #68 CI `34503805612`: PASS;
- merge to `develop` `0a86d9a0605e1dd9714ef35a547693de76f714f4`;
- post-merge CI `34504009878`: PASS.

## S14 — Japanese Target-User Validation & Release Preparation

**S14A COMPLETE / S14B NOT_EXECUTED for v0.2.3.**

The S14 protocol and fail-closed evidence tooling are integrated. For v0.2.3, the release-facing Japanese claim was deliberately narrowed instead of fabricating or waiting on representative-user evidence.

Current boundary:

- Japanese-first UI and deterministic English fallback may be described as implemented behavior;
- engineering/native evidence may be described only for its recorded tested scope;
- no representative Japanese-user validation, customer validation, proven ease-of-use, broad Japanese production-usability, statistical usability, or S14B PASS claim may be made;
- S14B remains available for a future release or claim that needs broader representative target-user evidence.

S14 must not broaden CutBridge into a renderer, shader system, asset manager, geometry exporter, or arbitrary scene synchronizer.

## Release-preparation track

Release engineering can proceed in parallel only where it does not weaken governance or disturb validated source behavior.

### A. Evidence reconciliation

- preserve the S12/S13 SHA-bound native record;
- recover the authentic structured S12 PASS evidence file if it exists externally;
- if it never existed, retain the evidence-traceability limitation instead of manufacturing historical data.

### B. Repository governance

Issue #18 remains **OPEN** as the live governance/release evidence log. Its latest evidence records the v0.2.3 authorized path, publication, independent artifact verification, and production D1 deployment as complete.

Configured and verified:

- protected `main`;
- protected `develop`;
- authoritative CI required for protected promotion/integration;
- admin-controlled `v*.*.*` release-tag mutation;
- no-bypass `release-tag-eligibility` required check for matching tag creation;
- v0.2.3 authorization and publication completed on exact protected `main`;
- active v0.2.4 release authorization is fail-closed.

Future release work:

- repeat the exact-current-main authorization and eligibility path for each subsequent release;
- keep v0.2.4 publication blocked while authorization is false;
- preserve the existing protected-branch/tag controls and evidence trail.

### C. Historical v0.2.3 `develop` → `main` promotion

**COMPLETE / VERIFIED.**

- promotion head: `501f9bd6b6c69cf8859f96f0fd6441afc48c0b50`;
- fresh PR CI `35511056270` attempt 2: PASS;
- PR #74 merged through protected `main`;
- promoted `main`: `049081f0fe3d3e74d77db807910c2e0fff56fe73`;
- post-promotion CI `35513361337`: PASS;
- release authorization remained false;
- `main` and `develop` trees are identical; `main` is one merge commit ahead.

### D. Exact release authorization

**v0.2.3 COMPLETE / VERIFIED.** The exact `v0.2.3` / stable / non-prerelease tuple was authorized only for current `main`. Active v0.2.4 authorization is false. Future authorization must remain exact, non-reusable, and limited to a fully validated current-main candidate.

### E. Publication and distribution verification

**v0.2.3 COMPLETE / VERIFIED.** Publication, downloaded-asset checks, metadata verification, and the separate production D1 endpoint are complete at distribution commit `635c1384af2649d4ce49705cce41f98826a861cc`:

- notification index: `https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json`;
- Blender repository: `https://unn0wn002.github.io/cutbridge-distribution/blender/index.json`;
- stable v0.2.3 assets remain versioned and immutable.

Production endpoint deployment is no longer pending. Future distribution work concerns subsequent releases and distribution automation, including additive retention, index generation, and independently verified promotion of newly authorized artifacts.

## Technical-debt track

Current priority debt:

1. Blender 6.0 migration away from deprecated `Scene.use_nodes`;
2. refresh pinned GitHub Actions revisions whose underlying action runtimes still emit Node 20 deprecation warnings;
3. prevent session-status tests from freezing historical state as current state;
4. preserve exact-candidate release governance and verification for subsequent releases;
5. maintain a durable native-evidence trail.

See `TECHNICAL_DEBT.md`.

## Stable-release goal

A production-oriented Japanese-first Blender → After Effects animation-cut handoff tool with deterministic packaging, revision-safe source updates, actionable QC, safe Studio Presets, validated bounded Camera/Null handoff, documented compatibility, controlled distribution/update architecture, green automated gates, and real-host/target-user evidence appropriate to the claims actually made.
