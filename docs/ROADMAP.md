# CutBridge Roadmap

Status reconciled through **S11 — QA / Docs / Release Engineering**. Version labels 0.2.0–0.2.3 remain unreleased development history; session numbers describe bounded product work and do not guarantee public release numbers.

## Completed foundation — S1–S9

### S1 — Baseline and release packaging
Completed.

Deterministic Blender + After Effects packaging, version consistency/checksums, GPL inclusion, release-output safety, and baseline documentation.

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
Completed and integrated.

Compatible revisions replace only verified managed sources, preserve unrelated artist work, migrate current managed metadata, retain historical-footage provenance, and fail closed on incompatible/ambiguous state.

### S7 — QC+
Completed and integrated.

Deterministic `CBQ-*` diagnostics with severity/remediation, sequence/comp/ownership/revision checks, and diagnostic-only behavior.

### S8 — Japanese-First UX
Completed and integrated.

Japanese-first UI with deterministic English fallback in Blender and After Effects while stable machine identifiers and safety decisions remain locale-independent. Native S8 validation passed in Blender 5.2.1 LTS and After Effects 2026 Build 87 before integration.

### S8.5 — Repository State Reconciliation
Completed and integrated.

Repository documentation/status was reconciled after S8; Japanese onboarding and technical-debt tracking were added; runtime and release authorization remained untouched.

### S9 — Studio Presets
Completed and integrated.

Delivered safe declarative Manual / CutBridge Default / Custom JSON modes, deterministic package/sequence/folder/pass/version/comp conventions, strict validation, one-build snapshot consistency, Japanese/English UI, and no executable preset trust boundary in AE.

Reference: [STUDIO_PRESETS.md](STUDIO_PRESETS.md).

## S10 — Camera / Null handoff

### S10A — Contract investigation
**Completed and integrated.**

Established the bounded Blender ↔ After Effects coordinate/timing/camera/null contract, including the axis map `(x, y, z) -> (x, -z, y)`, composition-center positions, explicit spatial scale, frame-time mapping, FOV/Zoom primitives, and evaluated-world orientation strategy rather than direct Euler copying.

Reference: [CAMERA_NULL_HANDOFF_CONTRACT.md](CAMERA_NULL_HANDOFF_CONTRACT.md).

### S10B — Optional 3D handoff producer
**Completed and integrated.**

Added the optional/versioned `handoff_3d` producer, evaluated-world active camera and explicitly marked Empty baking, bounded sample counts, frame restoration, and fail-closed unsupported camera/transform behavior. Historical manifests remain valid and the feature remains default-off.

Key evidence:

- candidate `2a222520da9dde7128dc1b9ddc1ed29b1e7a23b2`;
- candidate CI `34429145031`: PASS;
- PR #51 CI `34429245773`: PASS;
- merge `444a786e6f7a64143e50f933fa35ca84ea36138e`;
- post-merge CI `34429324559`: PASS.

### S10C — Native After Effects reconstruction / parity
**Completed and integrated; native-host validated.**

Delivered managed AE camera/3D Null reconstruction from the S10B handoff contract, idempotent rebuild, ownership/collision safety, and bounded real-host parity evidence.

Native evidence in Adobe After Effects 2026 Build 87 on Windows 11:

- maximum projection error: `0.00018066 px`;
- gate: `<= 0.05 px`;
- QC+: 10/10 PASS;
- repeated Build: 0 duplicate managed camera/null layers;
- unmanaged collisions: fail-closed PASS;
- project persistence: PASS.

Final S10C repository reconciliation on `develop`: `e63dcb7a97831fee43c94a3f351a2a196eaf981c` with post-reconciliation CI `34440714199` PASS.

Reference: [HANDOFF_3D.md](HANDOFF_3D.md).

## S11 — QA / Docs / Release Engineering

**Implementation complete on the S11 integration candidate; integration gate in progress.**

Delivered:

- English Quick Start reconciled through S10C;
- Japanese Quick Start reconciled through S10C with the same safety semantics;
- After Effects installation guide reconciled through S10C;
- `HANDOFF_3D.md` updated from producer-only language to the validated S10B producer + S10C consumer boundary;
- compatibility policy now distinguishes bounded native evidence from blanket certification;
- canonical [RELEASE_READINESS.md](RELEASE_READINESS.md) added;
- release readiness explicitly separates automated QA, native evidence, S12 end-to-end work, Japanese target-user evidence, repository governance, deliberate promotion, exact authorization, publication, published-asset verification, and production update/distribution verification;
- S11 documentation/readiness regression tests added;
- existing release builder/workflow retained because audit found no reproducible release-runtime defect.

Candidate validation:

- intermediate CI `34449966185`: static PASS, Blender job failed only because a new S11 documentation assertion depended on one exact phrase; runtime/RNA tests themselves passed and pytest reported 235 PASS / 1 new-doc-test failure;
- assertion repaired semantically without weakening the gate;
- corrected head `818d9b8275319194c8c42329b8a139b35239e1aa`;
- corrected CI `34450066759`: PASS for both authoritative jobs.

S11 changes publication readiness from scattered documentation to an explicit fail-closed checklist. It does **not** make v0.2.3 release-ready.

## S12 — End-to-End Validation Harness — NEXT

Build and execute an evidence-grade Blender → package → After Effects release-target campaign using exact candidate artifacts.

Required focus:

- install exact candidate Blender artifact in the release-target GUI host;
- build a representative cut/package and real render sequences;
- load exact candidate AE runtime files;
- Build + QC the real package;
- exercise V001→V002→V003 compatible revisions;
- verify artist-state preservation where claimed;
- save, close, reopen, reload, and re-check;
- exercise the S10C camera/Null path from release-candidate artifacts;
- record exact hosts, fixtures, checksums, screenshots/logs, and outcomes;
- never infer GUI success from headless tests.

## S13 — Manual-Finding Repair

Run only when actual S12/real-host testing produces a reproducible defect. Do not invent defects merely to continue a session.

## S14 — Japanese Target-User Validation Preparation

Prepare Japanese-oriented task scripts, timing/error/rework metrics, feedback templates, and acceptance criteria. Do not fabricate participants, measurements, or usability claims.

## Release-governance track — independent blocker

Issue #18 remains open independently of feature development.

Before any RC/stable publication:

- protect `main` and `develop` through repository-level governance;
- restrict `v*` tag mutation to the intended release path or equivalent;
- protect against publication from historical workflow commits;
- complete release-target validation;
- freeze an exact candidate;
- deliberately reconcile/promote the materially diverged `develop` candidate to `main` rather than blind-merging;
- explicitly authorize the exact current-main/tag/channel/prerelease tuple;
- publish only through the authorized release workflow;
- independently verify downloaded release artifact checksums/contents;
- validate the production update endpoint/index;
- satisfy target-user evidence appropriate to the release claim.

The canonical gate is [RELEASE_READINESS.md](RELEASE_READINESS.md).

## Technical-debt track

See [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).

Current priorities include Blender 6.0 migration away from deprecated `Scene.use_nodes`, refreshing pinned GitHub Actions revisions that still target deprecated Node 20 runtimes, deliberate `main`/`develop` promotion reconciliation, and recorded Japanese target-user evidence.

## Stable-release goal

A production-oriented Japanese-first Blender → After Effects handoff tool with deterministic packaging, revision-safe source updates, actionable QC, safe Studio Presets, a validated bounded camera/null handoff, documented compatibility, controlled distribution/update architecture, green automated gates, and recorded real-host/target-user validation appropriate to the release claim.
