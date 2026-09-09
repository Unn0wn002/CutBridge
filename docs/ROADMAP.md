# CutBridge Roadmap

Status reconciled through the completed S8.5 documentation-maintenance session. Version labels 0.2.0–0.2.3 remain unreleased development history; session numbers describe bounded product work and do not guarantee public release numbers.

## Completed foundation — S1–S8

### S1 — Baseline and release packaging
Completed.

- deterministic Blender + After Effects packaging;
- version consistency and checksums;
- GPL license inclusion;
- release-output safety and baseline documentation.

### S2 — Blender Render Mapping
Completed.

- BEAUTY / LINE / SHADOW / DEPTH logical pass mapping;
- renderer/View Layer capability validation;
- deterministic output paths;
- transactional replacement with unrelated artist nodes preserved.

### S3 — Blender Production Hardening
Completed.

- package-target safety;
- same-version payload overwrite prevention;
- V001/V002/V003 coexistence;
- package integrity and Japanese/UTF-8 filesystem handling.

### S4 — AE Handoff Contract Hardening
Completed.

- schema/version gates;
- finite integer/non-negative frame contract;
- safe package-relative paths;
- required/optional pass semantics;
- exact sequence coverage;
- data-only legacy JSON parsing;
- canonical product-version enforcement.

### S5 — AE Import & Composition Reliability
Completed.

- deterministic managed ownership;
- repeated-build/reload safety;
- collision/ambiguity blocking;
- rollback and managed-package structure validation;
- stricter QC ownership behavior.

### S6 — Non-Destructive Revision Manager
Completed and integrated.

- merge: `5d309f51d75b357974d17c94090792d27dea6163`;
- native AE gate #19 PASS;
- solo-maintainer adversarial gate #20 PASS;
- post-merge CI PASS.

Compatible revisions replace only verified managed sources, preserve unrelated artist work, migrate current managed metadata, retain historical-footage provenance, and fail closed on incompatible/ambiguous state.

### S7 — QC+
Completed and integrated.

- repaired candidate: `b17b9d3cd5b67d7bfd3741a58df403d5946e2327`;
- merge: `ef88d68f0178ed33ed4ba096416fcfe595c1eb6d`;
- real AE validation found and repaired ExtendScript/revision-state defects before merge.

QC+ supplies deterministic `CBQ-*` diagnostics with severity, remediation, sequence/comp/ownership/revision checks, and no automatic mutation or repair.

### S8 — Japanese-First UX
Completed and integrated.

- repaired candidate: `f477b745cc600b85708b63d059d6c4eaed9f0249`;
- merge: `368b977582feadc26543825b4d31ffd5f6266a4f`;
- AE gate #38 PASS in After Effects 2026 v26.3.0 Build 87;
- Blender gate #41 PASS in Blender 5.2.1 LTS at approximately 245 px N-panel width;
- post-merge CI `34380737455` PASS.

S8 delivers Japanese-first UI with deterministic English fallback in Blender and After Effects while stable machine identifiers and safety decisions remain locale-independent.

## S8.5 — Repository State Reconciliation
Completed and integrated.

Scope completed:

- reconciled README/completion/roadmap/Quick Start/Test Plan/changelog/AE installation status after S8;
- added Japanese onboarding documentation;
- recorded technical debt and current release-governance blockers;
- kept `main`, runtime implementation, workflow behavior, and release authorization untouched;
- established S9 as the next engineering feature.

Evidence:

- PR #42 final head: `e61a1fc7c14e49c062c2d29b95e829636ef16bb7`;
- PR CI `34383043982`: PASS;
- merge: `00b6e8fd62826d9cecfda542f6cb85f7174a7dd2`;
- post-merge `develop` CI `34383182746`: PASS.

## S9 — Studio Presets
**Next engineering session.**

Goal: make CutBridge adaptable to different animation/content-production teams without hard-coding a studio workflow.

Candidate scope:

- external data-only preset format;
- naming conventions;
- deterministic folder structure;
- default pass sets and required/optional policy defaults;
- AE layer ordering;
- output formats;
- version-pattern/display conventions;
- built-in safe default preset;
- explicit preset validation and fallback behavior;
- migration/versioning policy for preset schema.

Safety boundaries:

- no arbitrary code execution from preset files;
- no hidden filesystem/network actions;
- no automatic ownership adoption;
- no confidential real-studio preset bundled without explicit permission;
- existing S5/S6/S7 fail-closed ownership/revision/QC behavior remains authoritative.

## S10 — Camera / Null Handoff Investigation

Research Blender ↔ AE coordinate systems, axes, units, camera/lens/FOV/sensor representation, parenting, empties/nulls, and frame timing. Ship only a minimal subset whose behavior can be established and tested reliably.

## S11 — QA / Docs / Release Engineering

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

See `TECHNICAL_DEBT.md`.

Current priorities include Blender 6.0 migration away from deprecated `Scene.use_nodes` behavior and updating pinned GitHub Actions revisions that still target deprecated Node 20 runtimes.

## Stable-release goal

A production-oriented Japanese-first Blender → After Effects handoff tool with deterministic packaging, revision-safe source updates, actionable QC, safe studio presets, documented compatibility, controlled distribution/update architecture, green automated gates, and recorded real-host/target-user validation appropriate to the release claim.
