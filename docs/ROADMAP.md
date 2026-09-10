# CutBridge Roadmap

Status reconciled through S9 Studio Presets with **S10 Camera / Null Handoff Investigation in progress**. Version labels 0.2.0–0.2.3 remain unreleased development history; session numbers describe bounded product work and do not guarantee public release numbers.

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

Japanese-first UI with deterministic English fallback in Blender and After Effects while stable machine identifiers and safety decisions remain locale-independent. Native S8 validation passed in Blender 5.2.1 LTS and After Effects 2026 v26.3.0 Build 87 before integration.

### S8.5 — Repository State Reconciliation
Completed and integrated.

Repository documentation/status was reconciled after S8; Japanese onboarding and technical-debt tracking were added; `main`, runtime behavior, and release authorization remained untouched.

### S9 — Studio Presets
Completed and integrated.

S9 provides a versioned data-only preset contract, Manual / CutBridge Default / Custom JSON modes, safe naming/folder/pass/output/version customization, one-build snapshot consistency, Japanese/English UI, and preserved Blender↔AE identity/ownership boundaries.

Evidence:

- candidate `ea305d19ab2ff0667a8fa9e94c1e1ebca5e51b22`;
- candidate CI `34424041843` PASS;
- PR #45 CI `34424216448` PASS;
- merge `19d09722678b4e6389d2b3f852a8c4c3a5dbf52f`;
- post-merge CI `34424286137` PASS.

Reference: [STUDIO_PRESETS.md](STUDIO_PRESETS.md).

## S10 — Camera / Null Handoff Investigation
**IN PROGRESS — investigation first; production runtime unchanged.**

Goal: establish Blender ↔ After Effects spatial, camera-optics, timing, and parenting behavior from reproducible evidence before adding any production camera/null importer.

Current research increment:

- pure research math for candidate basis Blender `(X,Y,Z)` → AE `(X,-Z,Y)`;
- deterministic 1920×1080 / 50 mm / 36 mm synthetic perspective fixture;
- Blender 5.2 source-side projection probe using `world_to_camera_view()`;
- disposable After Effects native projection probe using CameraLayer, 3D Nulls, and `toComp()`;
- source-side projection precision budget **≤ 0.00005 px**;
- native AE acceptance **≤ 0.05 px** without widening to mask a conversion defect;
- timing candidate `(frame - frameStart) / fps`;
- explicit documentation that `100 px / Blender unit` is fixture scale only, not production policy.

Pending gates:

1. freeze a green automated research-harness candidate;
2. run native AE gate #47 and record exact projection/cleanup evidence;
3. investigate arbitrary camera orientation;
4. investigate parented Empty/camera chains and constraints;
5. define explicit production scale policy;
6. decide whether S10 stops at validated research or safely ships a minimal runtime subset.

Acceptance principle: ship only behavior whose coordinate/timing contract is derived, represented explicitly, and tested reliably. If evidence is insufficient, **runtime deferred** is an acceptable S10 result.

Reference: [CAMERA_NULL_HANDOFF.md](CAMERA_NULL_HANDOFF.md).

## S11 — QA / Docs / Release Engineering

S11 starts only after S10 reaches an explicit completion decision.

- reconcile final CI/test matrix;
- update installation/usage/revision/QC/troubleshooting documentation;
- verify packaging and compatibility metadata;
- prepare controlled distribution/update infrastructure;
- address release-governance issue #18 before publication.

## S12 — End-to-End Validation Harness

Maintain legal/original/synthetic fixtures and an evidence-grade Blender → package → AE checklist, including V001→V002→V003 revision preservation and save/reopen behavior. Never infer GUI success from headless tests.

## S13 — Manual-Finding Repair

Run only when actual real-host/manual testing produces a reproducible defect. Do not invent defects merely to continue a session.

## S14 — Japanese Target-User Validation Preparation

Prepare Japanese-oriented task scripts, timing/error/rework metrics, feedback templates, and acceptance criteria. Do not fabricate participants, measurements, or usability claims.

## Release-governance track — independent blocker

Issue #18 remains open independently of feature development.

Before any RC/stable publication:

- protect `main` and `develop` through repository-level governance;
- restrict `v*` tag mutation to the intended release path or equivalent;
- protect against publication from historical workflow commits;
- explicitly authorize the exact current-main/tag/channel/prerelease tuple;
- deliberately promote a validated candidate to `main`;
- publish through the authorized tag workflow;
- download and independently verify release artifact checksums/contents;
- validate the production update endpoint/index;
- satisfy the remaining release/end-to-end and target-user gates.

## Technical-debt track

See [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).

Current priorities include Blender 6.0 migration away from deprecated `Scene.use_nodes` behavior, refreshing pinned GitHub Actions revisions that still target deprecated Node 20 runtimes, deliberate `main`/`develop` promotion reconciliation, and recorded Japanese target-user evidence.

## Stable-release goal

A production-oriented Japanese-first Blender → After Effects handoff tool with deterministic packaging, revision-safe source updates, actionable QC, safe Studio Presets, evidence-backed camera/null handoff behavior if S10 authorizes it, documented compatibility, controlled distribution/update architecture, green automated gates, and recorded real-host/target-user validation appropriate to the release claim.
