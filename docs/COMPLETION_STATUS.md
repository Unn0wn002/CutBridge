# CutBridge Completion Status

## Current state

- **Completed product sessions:** S1–S9.
- **Completed maintenance session:** S8.5 — repository/documentation state reconciliation.
- **Release branch baseline:** `main` remains the conservative unreleased/release-locked branch and is not changed by S9.
- **Product version:** `0.2.3` unreleased.
- **Release authorization:** fail-closed; `release-authorization.json` remains `approved: false`.
- **Git tags / GitHub Releases:** none.
- **Next engineering session:** S10 — Camera / Null Handoff Investigation.

S9 completion does not authorize an RC or stable release. Exact S9 candidate/CI/merge evidence is recorded in issue #44 and the GitHub Actions history.

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
- [x] regression coverage includes valid/default/manual/custom, malicious/invalid input, overlapping folders, bounded loader behavior, one-build snapshot consistency, and no preset-path disclosure;
- [x] existing S6/S7/S8 and Blender 5.2.1 suites remain part of the authoritative CI gate.

Documentation:

- [STUDIO_PRESETS.md](STUDIO_PRESETS.md)
- [QUICK_START.md](QUICK_START.md)
- [QUICK_START_JA.md](QUICK_START_JA.md)

### S9 validation boundary

Automated coverage establishes the data contract, Blender RNA/runtime compatibility, packaging/regression behavior, and existing AE contract preservation.

S9 does **not** claim a new native After Effects feature because AE does not load presets directly. It also does not fabricate a native Blender GUI usability result; broader real-user/target-user validation remains a later release-validation concern.

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

**S10 — Camera / Null Handoff Investigation**

Research Blender ↔ After Effects coordinate systems, axes, units, camera/lens/FOV/sensor representation, parenting, empties/nulls, and frame timing. Ship only behavior whose coordinate/timing contract can be established and tested reliably.