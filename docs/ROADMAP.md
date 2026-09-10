# CutBridge Roadmap

Status reconciled through **S10B — Optional 3D handoff data model + Blender evaluated-world producer**. Version labels 0.2.0–0.2.3 remain unreleased development history; session numbers describe bounded product work and do not guarantee public release numbers.

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

Goal achieved: make CutBridge adaptable to different animation/content-production teams without hard-coding a studio workflow or introducing executable configuration.

Delivered:

- versioned `cutbridge-studio-preset` JSON schema;
- data-only Manual / CutBridge Default / Custom JSON modes;
- Manual as backward-compatible default;
- safe built-in default preset and published example;
- strict unknown-field/schema/path/template/pass/format/version validation;
- bounded 64 KiB UTF-8 custom preset loader;
- disjoint render / preview / camera folder roles;
- configurable deterministic package and sequence naming;
- configurable pass order and required/optional policy;
- PNG / OpenEXR / TIFF selection;
- configurable version display token;
- configurable After Effects comp name and layer order through the normalized manifest;
- one validated custom-preset snapshot per Build Package transaction;
- optional `studio_preset` manifest provenance without recording the source file path;
- AE remains a manifest consumer and does not parse preset JSON;
- Japanese/English UI and stable `PRESET_*` diagnostics;
- regressions for manual compatibility, valid/custom/default presets, malicious input, unsafe/overlapping folders, loader bounds, and snapshot consistency.

Safety boundaries preserved:

- no arbitrary code or expression execution;
- no environment-variable or command expansion;
- no hidden network action;
- no automatic ownership adoption;
- no confidential real-studio preset bundled;
- S5/S6/S7 ownership/revision/QC behavior remains authoritative;
- canonical Blender↔AE package-identity primitives remain unchanged;
- `main` and release authorization are not modified by S9.

Reference: [STUDIO_PRESETS.md](STUDIO_PRESETS.md).

## S10 — Camera / Null handoff

### S10A — Contract investigation
**Completed and integrated.**

Established the bounded Blender ↔ After Effects coordinate/timing/camera/null contract before adding producer or consumer behavior.

Delivered:

- explicit Blender → AE-oriented axis map `(x, y, z) -> (x, -z, y)`;
- composition-center origin convention for mapped positions;
- explicit product-defined spatial scale;
- frame-to-AE-time formula `(frame - frame_start) / fps`;
- camera FOV/Zoom conversion primitives;
- evaluated world-space/basis strategy instead of direct Euler conversion;
- fail-closed camera MVP restrictions;
- documentation and mathematical regression fixtures.

S10A deliberately added no AE camera/null creation and no `handoff_3d` manifest field.

Reference: [CAMERA_NULL_HANDOFF_CONTRACT.md](CAMERA_NULL_HANDOFF_CONTRACT.md).

### S10B — Optional 3D handoff producer
**Completed and integrated.**

Added the producer-side data model without widening the current AE trust/mutation boundary.

Delivered:

- optional `cutbridge-handoff-3d` version 1 block in `cutbridge.json`;
- feature default OFF for historical compatibility;
- evaluated active perspective-camera sampling per exported frame;
- explicit marked-Empty selection only;
- baked position/basis/scale/time samples;
- camera forward/up/FOV/derived AE Zoom samples;
- frame/subframe restoration after sampling;
- strict sample-count bounds;
- fail-closed rejection of unsupported camera projection, sensor shift, non-square pixels, zero scale, shear, reflections, and invalid markers;
- existing AE importer compatibility: optional block tolerated but not consumed;
- Draft 2020-12 schema and official Blender 5.2.1 runtime/package tests.

Integration evidence:

- candidate `2a222520da9dde7128dc1b9ddc1ed29b1e7a23b2`;
- candidate CI `34429145031`: PASS;
- PR #51 CI `34429245773`: PASS;
- merge `444a786e6f7a64143e50f933fa35ca84ea36138e`;
- post-merge CI `34429324559`: PASS.

Reference: [HANDOFF_3D.md](HANDOFF_3D.md).

### S10C — Native After Effects reconstruction / parity
**PASS / native-host validated.**

Consumed the optional `handoff_3d` block in `CutBridge.jsx` and validated reconstruction in real Adobe After Effects 2026 Build 87:

- managed AE camera creation and update with baked position, point-of-interest, and zoom keyframes;
- managed AE 3D Null creation and update for serialized Empties (`ORIGIN`, `X_PLUS`, `Y_PLUS`, `Z_PLUS`, `XYZ_PLUS`);
- deterministic keyframe timing ($t = (\text{frame} - \text{start}) / \text{fps}$);
- orientation and projection verified with native `toComp()` evaluation: max error across all 5 spatial fixtures is **0.00018 px** (tolerance $\le 0.05\text{ px}$);
- idempotent rebuild verified (0 duplicate layers);
- fail-closed collision safety gate verified (unmanaged camera or null collisions rejected);
- project saved and reopened cleanly in real AE host (`s10c_reconstruction_validated.aep`).

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

See [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).

Current priorities include Blender 6.0 migration away from deprecated `Scene.use_nodes` behavior, refreshing pinned GitHub Actions revisions that still target deprecated Node 20 runtimes, deliberate `main`/`develop` promotion reconciliation, and recorded Japanese target-user evidence.

## Stable-release goal

A production-oriented Japanese-first Blender → After Effects handoff tool with deterministic packaging, revision-safe source updates, actionable QC, safe Studio Presets, a validated bounded camera/null handoff, documented compatibility, controlled distribution/update architecture, green automated gates, and recorded real-host/target-user validation appropriate to the release claim.
