# CutBridge Completion Status

## Current state

- **Completed product sessions:** S1–S9 plus S10A–S10C.
- **Completed maintenance session:** S8.5 — repository/documentation state reconciliation.
- **Release branch baseline:** `main` remains the conservative unreleased/release-locked branch and is not changed by S10.
- **Active integration branch:** `feature/session-10c-camera-null-reconstruction` targeted for `develop`.
- **Product version:** `0.2.3` unreleased.
- **Release authorization:** fail-closed; `release-authorization.json` remains `approved: false`.
- **Git tags / GitHub Releases:** none.
- **Next engineering session:** S11 — QA / Docs / Release Engineering.

S10C completion does not authorize an RC or stable release. Release governance issue #18 remains independently blocking publication.

## Integrated sessions

### S1 — Baseline / release packaging
PASS / integrated.

Repository baseline, GPL license inclusion, deterministic packaging, checksum verification, release-output safety, and documentation/release hygiene foundation.

### S2 — Blender render mapping
PASS / integrated.

Transactional BEAUTY / LINE / SHADOW / DEPTH mapping, deterministic output paths, renderer/View Layer capability checks, and artist-node preservation.

### S3 — Blender production hardening
PASS / integrated.

Same-version payload overwrite protection, package integrity, V001/V002/V003 coexistence, Japanese/UTF-8 filesystem handling, and actionable Blender validation.

### S4 — After Effects handoff contract hardening
PASS / integrated.

Schema/version gates, strict frame semantics, safe package paths, required/optional pass rules, exact sequence coverage, legacy JSON data parsing, and AE/version consistency checks.

### S5 — AE import / composition reliability
PASS / integrated.

Deterministic managed ownership, repeated-build/reload safety, collision handling, rollback, package-structure checks, and stricter QC ownership validation.

### S6 — Non-destructive revision manager
PASS / integrated.

- Candidate: `f996d64182c292c32361b9af145d85d0128f63dc`.
- Merge commit: `5d309f51d75b357974d17c94090792d27dea6163`.
- Native AE gate #19: PASS / closed.
- Solo-maintainer adversarial gate #20: PASS / closed.
- Post-merge CI `34260351796`: PASS.

Compatible revision updates use verified managed-source replacement, rollback, package/tag migration, and historical-footage provenance while preserving unrelated artist work.

### S7 — QC+
PASS / integrated.

- Candidate: `b17b9d3cd5b67d7bfd3741a58df403d5946e2327`.
- Merge commit: `ef88d68f0178ed33ed4ba096416fcfe595c1eb6d`.
- PR #35: merged.
- Native AE validation: PASS after repairing real ExtendScript and revision-state defects.

QC+ provides deterministic `CBQ-*` PASS / WARNING / ERROR diagnostics, actionable remediation, sequence/comp/ownership/revision checks, and remains diagnostic-only/non-mutating.

### S8 — Japanese-first UX
PASS / integrated.

- Repaired candidate: `f477b745cc600b85708b63d059d6c4eaed9f0249`.
- Merge commit: `368b977582feadc26543825b4d31ffd5f6266a4f`.
- PR #40: merged.
- AE native gate #38: PASS / closed.
- Blender native gate #41: PASS / closed.
- Post-merge CI `34380737455`: PASS.

S8 established Japanese-first / English-fallback UI while preserving locale-independent manifest values, ownership tags, diagnostic codes, and safety decisions.

### S8.5 — Repository state reconciliation
PASS / integrated.

Documentation/status maintenance only. S8.5 reconciled README/status/roadmap/Quick Start/Test Plan/changelog/AE install state, added Japanese onboarding and technical-debt tracking, and preserved release authorization as fail-closed.

### S9 — Studio Presets
PASS / integrated.

S9 adds a bounded, versioned, declarative Studio Preset contract without adding executable configuration or a second preset trust boundary in After Effects.

Implemented behavior:

- [x] three Blender modes: Manual, CutBridge Default, Custom JSON;
- [x] Manual remains default and preserves the pre-S9 package identity/pass/format controls;
- [x] strict `cutbridge-studio-preset` schema version 1;
- [x] safe built-in default and published example JSON;
- [x] custom preset files limited to 64 KiB, UTF-8 JSON only;
- [x] unknown fields, unsupported schema versions, invalid placeholders, duplicate passes, unsafe paths, and unsupported formats fail closed;
- [x] render / preview / camera role folders must be relative, disjoint, and non-overlapping;
- [x] configurable package naming, sequence naming, folder roles, pass order, required/optional flags, PNG/OpenEXR/TIFF format, version token, and AE comp naming;
- [x] custom preset is frozen to one validated in-memory snapshot for the full Build Package transaction;
- [x] Blender records normalized `studio_preset` provenance in `cutbridge.json` without storing the source preset path;
- [x] old manifests remain valid because Studio Preset metadata is optional in the manifest schema;
- [x] AE continues to consume resolved manifest fields and never opens the Studio Preset JSON;
- [x] Japanese/English UI and stable `PRESET_*` validation codes;
- [x] existing canonical `safe_token`, `version_token`, and `package_name` producer primitives remain unchanged for Blender↔AE identity compatibility;
- [x] regression coverage includes valid/default/manual/custom, malicious/invalid input, overlapping folders, bounded loader behavior, one-build snapshot consistency, and no preset-path disclosure.

Reference: [STUDIO_PRESETS.md](STUDIO_PRESETS.md).

### S10A — Camera / Null Handoff Contract Investigation
PASS / integrated.

S10A established the coordinate/timing/camera/null contract before any cross-host 3D reconstruction was allowed to ship.

Integration evidence:

- base: `19d09722678b4e6389d2b3f852a8c4c3a5dbf52f`;
- candidate: `8a87044f8b7c830f342a1cd26568f6a3e05cf503`;
- candidate push CI `34427616559`: PASS;
- PR #49 event CI `34427691064`: PASS;
- merge: `7b506d357faea08ea936daa90ccd0c94ea565f21`;
- post-merge `develop` CI `34427809612`: PASS.

Established contract:

- Blender → AE-oriented axis map: `(x, y, z) -> (x, -z, y)`;
- Blender world origin maps to AE composition center for positions;
- spatial scale is explicit, never inferred heuristically;
- frame-time mapping is `(frame - frame_start) / fps`;
- direct Blender Euler → AE Euler conversion is not approved;
- evaluated world-space baking is the first safe transform strategy;
- the initial camera subset is perspective, square-pixel, zero sensor shift only;
- arbitrary parent/constraint/driver reconstruction is deferred.

Reference: [CAMERA_NULL_HANDOFF_CONTRACT.md](CAMERA_NULL_HANDOFF_CONTRACT.md).

### S10B — Optional 3D handoff data model + Blender evaluated-world producer
PASS / integrated.

S10B adds the producer-side data model while deliberately keeping AE reconstruction disabled.

Integration evidence:

- base: `7b506d357faea08ea936daa90ccd0c94ea565f21`;
- candidate: `2a222520da9dde7128dc1b9ddc1ed29b1e7a23b2`;
- candidate push CI `34429145031`: PASS;
- PR #51 event CI `34429245773`: PASS;
- merge: `444a786e6f7a64143e50f933fa35ca84ea36138e`;
- post-merge `develop` CI `34429324559`: PASS.

Implemented behavior:

- [x] optional/versioned `handoff_3d` manifest block using schema `cutbridge-handoff-3d` version 1;
- [x] feature default OFF so historical package behavior remains unchanged;
- [x] old manifests without `handoff_3d` remain schema-valid;
- [x] active supported perspective camera sampled in evaluated Blender world space per exported frame;
- [x] only explicitly marked Blender Empties are serialized;
- [x] parent/constraint/driver effects may influence evaluated world state, but hierarchy is not recreated in AE;
- [x] samples contain position, normalized basis, scale, source frame, and AE composition time;
- [x] camera samples additionally contain forward/up direction, horizontal FOV, and derived AE Zoom;
- [x] Blender frame/subframe is restored after sampling, including failure paths;
- [x] camera shift, non-square pixels, non-perspective cameras, zero-scale, shear, reflections, invalid markers, and excessive sample counts fail closed;
- [x] current AE validator accepts/ignores the optional block; it does not create camera/null layers;
- [x] Draft 2020-12 schema tests and Blender 5.2.1 evaluated-world/package integration tests are part of CI.

Reference: [HANDOFF_3D.md](HANDOFF_3D.md).

### S10C — Native After Effects camera/null reconstruction and parity validation
PASS / native-host validated.

- Consumes the optional `handoff_3d` contract deterministically.
- Constructs managed AE camera (`S10C_Camera`) and 3D Null layers (`ORIGIN`, `X_PLUS`, `Y_PLUS`, `Z_PLUS`, `XYZ_PLUS`) with baked per-frame position and zoom keyframes.
- Validated in Adobe After Effects 2026 Build 87 (`26.3x87`) on Windows 64-bit with 0 unhandled errors.
- Native projection parity measured against ground truth fixtures: maximum error across all fixtures is **0.00018 px**, well inside the 0.05 px tolerance gate.
- QC+ diagnostic engine passed (10/10 checks PASS, 0 errors).
- Idempotent rebuild verified (0 duplicate camera or null layers created on repeated build).
- Collision safety gate verified (unmanaged camera and null collisions rejected with fail-closed ambiguous ownership errors).
- Native project file saved and verified (`s10c_reconstruction_validated.aep`, 147,993 bytes).

Reference: [HANDOFF_3D.md](HANDOFF_3D.md), [CAMERA_NULL_HANDOFF_CONTRACT.md](CAMERA_NULL_HANDOFF_CONTRACT.md).

## Release boundary

Release governance issue #18 remains **OPEN** and independent of product-session completion.

Current safeguards:

- tag publication workflow fails closed unless the tag targets current `main` and exact release authorization is explicitly approved;
- release-sensitive actions are pinned;
- packaging/checksum validation is deterministic;
- `release-authorization.json` is unapproved by default.

Still required before any RC/stable publication:

- actual repository-level protection for `main` and `develop`;
- controlled `v*` tag creation/update/deletion policy or equivalent;
- repository-level protection against historical-workflow publication;
- explicit auditable authorization for the exact current-main/tag/channel/prerelease tuple;
- deliberate promotion of a fully validated candidate to `main`;
- real authorized tag-triggered publication and downloaded-asset checksum/content verification;
- production update-endpoint/index verification;
- remaining release/end-to-end and target-user validation appropriate to the release claim.

Green CI alone is never release authorization.

## Known technical debt

See [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).

Priority items remain:

1. Blender 6.0 migration away from deprecated `Scene.use_nodes` behavior.
2. Refresh pinned GitHub Actions revisions that still target deprecated Node 20 runtimes.
3. Reconcile `main`/`develop` deliberately before a release candidate; do not treat the diverged histories as a trivial promotion merge.
4. Record Japanese target-user evidence before making production usability claims.

## Next engineering session

**S11 — QA / Docs / Release Engineering**

Reconcile final CI/test matrix, update end-to-end documentation across Blender and After Effects, verify release packaging, and prepare release readiness under governance issue #18.
