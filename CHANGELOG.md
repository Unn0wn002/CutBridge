# Changelog

All notable CutBridge changes are tracked here.

## [0.2.3] - Unreleased

### S8 — Japanese-first UX

#### Added
- First-class Japanese and deterministic English localization architecture in Blender and After Effects.
- Blender JA/EN language control and localized panel sections, actions, validation/build reports, environment/update UX, and production terminology.
- After Effects `localization.js` sidecar with locale-aware panel/actions/status/QC/revision guidance while preserving stable `CBQ-*` identifiers and canonical technical detail.
- S8 regression coverage for missing translation keys, invalid locale, locale persistence, safe fallback, non-mutation, and narrow-safe Blender panel layout.
- Deterministic After Effects packaging of four adjacent runtime files: `CutBridge.jsx`, `revision_manager.js`, `qc_plus.js`, and `localization.js`.

#### Fixed
- Blender S8 native testing found material clipping at approximately 245 px N-panel width; core fields/actions/pass controls were re-laid out for practical narrow-panel readability.
- AE S8 native testing found persisted Japanese + missing `localization.js` could render English fallback while the visible selector still said Japanese; fallback is now explicitly English-only and the selector synchronizes to the effective locale.

#### Validation
- Repaired candidate: `f477b745cc600b85708b63d059d6c4eaed9f0249`.
- Blender 5.2.1 LTS native retest: PASS at approximately 245 px width; JA/EN readability, localized validation, Validate Cut, and Build Package passed.
- Adobe After Effects 2026 v26.3.0 Build 87 native retest: PASS; persisted JA + missing localization sidecar yielded coherent English fallback with English selector and zero project mutation, and restoring the sidecar returned the UI to Japanese.
- Merged to `develop` as `368b977582feadc26543825b4d31ffd5f6266a4f`.
- Post-merge CI `34380737455`: PASS — static 88 + 2 subtests; full Blender/runtime 179 + 2 subtests; release simulation/checksums and S5/S6/S7/S8 regressions passed.

### S7 — QC+

#### Added
- Deterministic `CBQ-*` PASS / WARNING / ERROR QC+ diagnostic engine.
- Safe remediation text for warning/error findings.
- Sequence, comp, managed footage/layer, host ownership, and revision-aware diagnostics.
- Native binding from `CutBridge.jsx` through `qc_plus.js`.
- QC remains diagnostic-only with no automatic adoption, import, deletion, relocation, retagging, source replacement, or repair.

#### Fixed
- Native AE validation found an ExtendScript compatibility defect caused by an unquoted reserved `package` object key in `qc_plus.js`; repaired and regression-covered.
- Native AE validation found incorrect revision compatibility state from a nested ternary in `revision_manager.js`; replaced with explicit fail-closed branching and regression coverage.

#### Validation
- Repaired candidate: `b17b9d3cd5b67d7bfd3741a58df403d5946e2327`.
- Real After Effects QC+/revision campaign: PASS after repair.
- Merged to `develop` as `ef88d68f0178ed33ed4ba096416fcfe595c1eb6d`.

### S6 — Non-destructive revision manager

#### Added
- Revision-manager sidecar and native AE adapter.
- Newer-package discovery, compatibility planning, explicit confirmation, staged replacement import, source-only managed layer replacement, rollback, package/tag migration, and historical-footage provenance.
- Deterministic V001→V002→V003 host-shaped lifecycle coverage.
- Exact package-root/folder ownership resolution shared by Build, Revision, and QC.

#### Fixed / hardened
- Revision blocks incompatible geometry, pass-set additions/removals, stale/foreign ownership, ambiguous package structure, and invalid managed-layer state before mutation.
- Native source replacement uses `AVLayer.replaceSource(newSource, false)` and verifies live source state.
- Rollback/cleanup paths cover allocation-then-throw, mutate-then-throw, silent swap failure, restore failure, cleanup failure, and commit failure.
- QC requires valid current managed-layer ownership/source for complete required passes.
- Optional pass removal is fail-closed before mutation to prevent stale-layer lifecycle inconsistency.
- Release publication fails closed unless an exact current-main tag/channel/prerelease tuple is explicitly authorized.

#### Validation
- Candidate: `f996d64182c292c32361b9af145d85d0128f63dc`.
- Native AE gate #19: PASS / closed.
- Solo-maintainer adversarial gate #20: PASS / closed.
- Merged to `develop` as `5d309f51d75b357974d17c94090792d27dea6163`.
- Post-merge CI `34260351796`: PASS.

### S5 — AE import / composition reliability

- Added deterministic managed-object tags and repeated-build/reload safety.
- Hardened managed comp/footage/layer ownership, stale cache recovery, collision blocking, package-root structure validation, rollback, and QC live-state behavior.
- Required managed layer deletion/de-tagging cannot produce a false clean QC PASS.
- Artist objects are preserved and never adopted merely because name/source resembles CutBridge state.

### S4 — AE handoff contract hardening

- Added schema/version gating, realm-safe array handling, strict finite integer/non-negative frame semantics, safe package-relative paths, required/optional pass rules, exact sequence coverage, data-only legacy JSON parsing, and canonical AE product-version checks.
- Negative export ranges are rejected consistently; CutBridge does not silently renumber animation.

### S3 — Blender production hardening

- Added same-version payload overwrite protection and safe empty-scaffold refresh behavior.
- Added package integrity checks, V001/V002/V003 coexistence, Japanese/UTF-8 metadata, filesystem-safe naming, and actionable validation.

### S2 — Blender render mapping

- Added transactional BEAUTY / LINE / SHADOW / DEPTH render mapping with deterministic package paths and renderer/View Layer capability checks.
- Artist compositor nodes are preserved; failed replacement mapping rolls back safely.

### S1 / release foundation

- Added GPL license text and license inclusion in release ZIPs.
- Added reproducible release packaging, source/output safety, checksum verification, release metadata, and baseline documentation.
- Generated `cutbridge.json` reads the canonical CutBridge version rather than a stale literal.

### Technical debt recorded after S8

- Current Blender 5.2.1 suite passes but emits 61 `Scene.use_nodes` deprecation warnings expected to matter for Blender 6.0.
- Some pinned GitHub Actions revisions still target deprecated Node 20 runtimes and are currently forced by GitHub onto Node 24. CI passes, but pins should be refreshed deliberately.

### Release status

- v0.2.3 remains unreleased.
- No release tag or GitHub Release exists.
- `release-authorization.json` remains unapproved by design.
- Repository-level release governance issue #18 remains a blocker independently of S1–S8 product integration.

## [0.2.2] - Unreleased

### Fixed
- Removed updater URL/status strings from AddonPreferences RNA after Blender 5.2 registration testing showed they were unsafe there.
- Moved update endpoint transport state out of persistent RNA preferences.

### Added
- Official `bpy==5.2.1` lifecycle CI on Python 3.13.

## [0.2.1] - Unreleased

### Fixed
- Blender 5.2 registration failure from unsupported `StringProperty(subtype="URL")`.
- Partial-registration rollback and stale-registration cleanup before retry.

### Changed
- Blender 5.2 LTS added to the compatibility target set.

## [0.2.0] - Unreleased

### Added
- Central version constants and compatibility policy.
- Environment diagnostics and update-channel preferences.
- Notification-only update discovery.
- Deterministic Blender + After Effects release builder, SHA-256 sums, metadata, and release-index schema.

### Safety
- Private source control remains separate from customer distribution/update hosting.
- CutBridge does not force-update active extension code.

## [0.1.0]

### Added
- Initial Blender metadata/validation/package MVP.
- UTF-8 `cutbridge.json` generation.
- Initial After Effects importer, comp setup, image-sequence import, and basic QC.
- Initial CI/release workflow foundation.
