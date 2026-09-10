# CutBridge Completion Status

## Current state

- **Completed product sessions:** S1–S9.
- **Completed maintenance session:** S8.5 — repository/documentation state reconciliation.
- **Current engineering session:** S10 — Camera / Null Handoff Investigation.
- **Integrated `develop` baseline entering S10:** `19d09722678b4e6389d2b3f852a8c4c3a5dbf52f`; post-S9 CI `34424286137` PASS.
- **Release branch baseline:** `main` remains `cc6dc4dacce55b730b37eeb1d65afdf6ea98c50c` and is not changed by S10.
- **Product version:** `0.2.3` unreleased.
- **Release authorization:** fail-closed; `release-authorization.json` remains `approved: false`.
- **Git tags / GitHub Releases:** none.

S10 is currently a **research/validation session**, not a production camera/null feature. The shipped manifest/importer behavior remains unchanged until the cross-DCC spatial contract is supported by reproducible evidence.

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

### S7 — QC+
PASS / integrated.

- Candidate: `b17b9d3cd5b67d7bfd3741a58df403d5946e2327`.
- Merge commit: `ef88d68f0178ed33ed4ba096416fcfe595c1eb6d`.
- PR #35: merged.
- Native AE validation: PASS after repairing real ExtendScript/revision-state defects.

### S8 — Japanese-first UX
PASS / integrated.

- Repaired candidate: `f477b745cc600b85708b63d059d6c4eaed9f0249`.
- Merge commit: `368b977582feadc26543825b4d31ffd5f6266a4f`.
- PR #40: merged.
- AE native gate #38: PASS / closed.
- Blender native gate #41: PASS / closed.
- Post-merge CI `34380737455`: PASS.

### S8.5 — Repository state reconciliation
PASS / integrated.

Documentation/status maintenance only. S8.5 reconciled repository state, added Japanese onboarding and technical-debt tracking, and preserved release authorization as fail-closed.

### S9 — Studio Presets
PASS / integrated.

- Exact candidate: `ea305d19ab2ff0667a8fa9e94c1e1ebca5e51b22`.
- Candidate push CI `34424041843`: PASS.
- PR #45 event CI `34424216448`: PASS.
- Merge: `19d09722678b4e6389d2b3f852a8c4c3a5dbf52f`.
- Post-merge `develop` CI `34424286137`: PASS.
- Issue #44: PASS / closed.

S9 adds a bounded, versioned, declarative Studio Preset contract while preserving the legacy Manual identity contract and keeping After Effects as a resolved-manifest consumer rather than a preset-file trust boundary.

Reference: [STUDIO_PRESETS.md](STUDIO_PRESETS.md).

## S10 — Camera / Null Handoff Investigation

**IN PROGRESS — research harness only; production runtime unchanged.**

Tracking:

- issue #46 — S10 investigation;
- issue #47 — native After Effects spatial-probe gate;
- branch `feature/session-10-camera-null-handoff` from exact green S9 merge `19d0972...`.

Current research scope:

- [x] confirm production manifest currently contains only the legacy camera-name string and AE does not create a 3D camera/null from it;
- [x] document Blender and AE coordinate-space assumptions from current platform documentation;
- [x] establish research-only basis candidate Blender `(X,Y,Z)` → AE `(X,-Z,Y)`;
- [x] add pure spatial/FOV/frame-time math fixture and fail-closed tests;
- [x] add isolated Blender 5.2 projection probe using `world_to_camera_view()`;
- [x] add disposable native AE projection probe using `addCamera`, 3D nulls, and `toComp()`;
- [x] enforce explicit Save dialog and disposable-comp cleanup in the AE probe;
- [x] keep native AE projection acceptance at **≤ 0.05 px**;
- [x] quantify Blender source-side projection precision separately at **≤ 0.00005 px** after observing approximately `0.0000319 px` finite-precision error;
- [ ] obtain a fully green exact-head automated S10 research run after source-probe hardening;
- [ ] execute native AE issue #47 and record exact host/report evidence;
- [ ] investigate arbitrary camera orientation before any general camera rotation conversion;
- [ ] investigate Empty/camera parent chains before choosing sampled-world-transform versus reproduced-parent hierarchy behavior;
- [ ] define a production spatial-scale policy;
- [ ] decide whether S10 stops at validated research or ships a minimal runtime subset.

Important non-claims:

- the current `100 px / Blender unit` value is a synthetic fixture scale, not production policy;
- the candidate basis is not production-authorized until the native AE gate passes;
- orthographic/panoramic cameras, lens shift, DOF equivalence, arbitrary constraints, and general parenting are not certified;
- automated `bpy` evidence is not relabeled as Blender GUI/user validation;
- Node syntax checks are not relabeled as native After Effects validation.

Reference: [CAMERA_NULL_HANDOFF.md](CAMERA_NULL_HANDOFF.md).

## Release boundary

Release governance issue #18 remains **OPEN** and independent of product-session progress.

Current safeguards:

- tag publication workflow fails closed unless the tag targets current `main` and exact release authorization is explicitly approved;
- release-sensitive actions are pinned;
- packaging/checksum validation is deterministic;
- `release-authorization.json` is unapproved by default.

Still required before any RC/stable publication:

- repository-level protection for `main` and `develop`;
- controlled `v*` tag creation/update/deletion policy or equivalent;
- repository-level protection against historical-workflow publication;
- explicit auditable authorization for the exact current-main/tag/channel/prerelease tuple;
- deliberate promotion of a fully validated candidate to `main`;
- real authorized tag-triggered publication and downloaded-asset checksum/content verification;
- production update-endpoint/index verification;
- remaining release/end-to-end and target-user validation appropriate to the release claim.

Green CI or a successful S10 research probe is never release authorization.

## Known technical debt

See [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).

Priority items remain:

1. Blender 6.0 migration away from deprecated `Scene.use_nodes` behavior.
2. Refresh pinned GitHub Actions revisions that still target deprecated Node 20 runtimes.
3. Reconcile `main`/`develop` deliberately before a release candidate; do not treat the diverged histories as a trivial promotion merge.
4. Record Japanese target-user evidence before making production usability claims.

## Next decision

Complete the **S10 native AE spatial-probe gate (#47)** and use the measurements to decide whether the candidate coordinate/optics model is strong enough to expand toward arbitrary orientation/parenting or whether the runtime feature should remain deferred.
