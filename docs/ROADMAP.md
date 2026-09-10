# CutBridge Roadmap

Status reconciled through **S13 — native AE revision repair**. Version `0.2.3` remains unreleased; session numbers describe bounded product work and do not guarantee public release numbers.

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

## S14 — Japanese Target-User Validation & Release Preparation — NEXT

S14 is now the next bounded phase.

Objectives:

- define Japanese target-user task scripts and acceptance criteria;
- validate terminology, onboarding, install, Blender validation/build, package transfer, AE Build/QC, revision handling, and error recovery with actual target users when making production-usability claims;
- record task completion, friction, rework, terminology feedback, and material blockers;
- repair material user-facing findings before release claims;
- preserve bounded compatibility language;
- do not fabricate participants, observations, timing, or measurements.

S14 should not broaden CutBridge into a renderer, shader system, asset manager, geometry exporter, or arbitrary scene synchronizer.

## Release-preparation track

Release engineering can proceed in parallel only where it does not weaken governance or disturb validated source behavior.

### A. Evidence reconciliation

- preserve the S12/S13 SHA-bound native record;
- recover the authentic structured S12 PASS evidence file if it exists externally;
- if it never existed, retain the evidence-traceability limitation instead of manufacturing historical data.

### B. Repository governance

Issue #18 remains an independent publication blocker.

Required before RC/stable publication:

- protect `main` and `develop`;
- require authoritative CI for protected promotion/integration;
- restrict `v*` release-tag mutation;
- protect against historical-workflow publication;
- record and test repository-admin controls.

Current private-repository plan/configuration does not expose the required ruleset capability. Do not make the repository public merely to satisfy the gate.

### C. Deliberate `develop` → `main` promotion

`main` and `develop` are materially diverged. Do not blind-merge.

Before promotion:

- compare `main...candidate` file-by-file;
- preserve required main-side release-lock intent;
- preserve the newer hardened release workflow on `develop`;
- produce an explicit promotion tree/commit;
- run authoritative CI on the exact promoted `main` candidate;
- keep release authorization false during promotion validation.

### D. Exact release authorization

Only after every prerequisite is complete, authorize one exact current-main/tag/channel/prerelease tuple. Authorization must not be reusable or broad.

### E. Publication and distribution verification

After an authorized publication:

- independently download and checksum release assets;
- verify package contents and release metadata;
- deploy/verify the production update/distribution endpoint separate from the private source repository;
- verify notification-only update behavior and rollback policy.

## Technical-debt track

Current priority debt:

1. Blender 6.0 migration away from deprecated `Scene.use_nodes`;
2. refresh pinned GitHub Actions revisions whose underlying action runtimes still emit Node 20 deprecation warnings;
3. prevent session-status tests from freezing historical state as current state;
4. reconcile branch history before release promotion;
5. maintain a durable native-evidence trail.

See `TECHNICAL_DEBT.md`.

## Stable-release goal

A production-oriented Japanese-first Blender → After Effects animation-cut handoff tool with deterministic packaging, revision-safe source updates, actionable QC, safe Studio Presets, validated bounded Camera/Null handoff, documented compatibility, controlled distribution/update architecture, green automated gates, and real-host/target-user evidence appropriate to the claims actually made.