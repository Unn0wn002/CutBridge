# Changelog

All notable CutBridge changes are tracked here.

## [0.2.3] - Unreleased

### Fixed
- S5 ownership/cache repair resolves footage and layers from live project state on every reuse, rejects tag/container drift and ambiguous duplicate identities without reclaiming artist objects, and applies the same live footage checks in QC.
- S5 follow-up hardening resolves managed comps from live package-scoped ownership, rejects duplicate/moved comp tags before replacement, keeps QC live after script reload, excludes skipped optional layers from current-build ordering, and makes manifest membership safe for prototype-key names.
- S5 cache/QC hardening now treats a still-live cached object with combined tag/name/source/container drift as an ownership collision, rehydrates verified layer cache observations, and reports missing managed comps or required footage during project-state QC after reload.
- S5 AE build/import reliability now preflights required sequence coverage before project mutation, reuses only package-scoped CutBridge-managed comps/footage/layers, blocks same-name manual comp collisions, and refuses silent managed-comp metadata rewrites.
- S4 AE contract: realm-safe arrays, finite integer frame semantics, safe package-relative pass paths and basename patterns, Unicode filename decoding, and executable JSON rejection in legacy ExtendScript.
- Negative export ranges now fail consistently at Blender/schema/AE boundaries with a rebase instruction; zero-based export remains supported. Signed AE sequence ordering is not certified.
- AE-facing version text reads one centrally checked product-version constant; release builds reject divergence.
- S3 package rebuild safety blocks same-version overwrite when render/user payload already exists while allowing safe refresh of an empty CutBridge scaffold.
- S3 package-integrity checks fail incomplete package creation before reporting success.
- S2 render mapping is transactional: failed replacement attempts preserve the previous valid CutBridge mapping and restore render/View Layer settings.
- Release ZIP entries now use fixed timestamps and permissions, so identical sources built with the same Python/zlib toolchain produce identical checksums.
- Release output validation preserves unrelated files, rejects source-directory overlap and artifact symlinks, and checks both canonical version constants before writing.
- Generated `cutbridge.json` files now read `cutbridge_version` from the canonical Blender extension version instead of emitting the stale `0.1.0` literal.

### Added
- S5 deterministic managed-object tags and Node/pytest host-adapter regressions for repeated-build/reload idempotency, manual comp collision safety, comp metadata drift, layer order, and preflight no-mutation behavior.
- S2 Blender render-output mapping for logical BEAUTY / LINE / SHADOW / DEPTH passes using CutBridge-owned compositor nodes and deterministic package-relative output locations.
- S2 renderer/View Layer capability validation and Blender 5.2.1 regressions for mapping behavior without deleting unrelated artist nodes.
- S3 actionable Blender validation UI, V001/V002/V003 coexistence coverage, Japanese/UTF-8 and Windows-invalid-name hardening, lazy payload detection, and package preservation regressions.
- Node AE contract and mocked host-adapter regressions for required/optional passes, exact coverage, unexpected files, unsafe paths, aliases and legacy JSON parsing; official bpy producer-to-AE filename contract checks.
- Root GPL license text and license inclusion in both release ZIPs, matching the existing GPL-3.0-or-later declaration.
- Session 1 baseline/branch-history audit, release safety regression tests, and schema/example validation.
- Official `bpy 5.2.1` integration coverage for scene metadata, JSON Schema validation, render-pass layouts, V001/V002 coexistence, UTF-8 Japanese metadata, and validation failures.
- Release checks now recompute artifact SHA-256 values and verify every shipped Blender Python module plus archived version metadata.
- Release CI now installs the Blender 5.2.1 runtime dependencies and runs the full automated suite and RNA lifecycle test.

## [0.2.2] - Unreleased

### Fixed
- Removed updater URL/status strings from AddonPreferences RNA after the first Blender 5.2 registration fix proved insufficient.
- Moved the update endpoint to a distribution code constant and status to transient runtime state.

### Added
- Official `bpy==5.2.1` lifecycle CI on Python 3.13, checking two register/unregister cycles and stale RNA cleanup.

## [0.2.1] - Unreleased

### Fixed
- Blender 5.2 registration failure caused by the unsupported `StringProperty(subtype="URL")` declaration in CutBridge preferences.
- Partial enable failures now roll back already-registered CutBridge classes instead of leaving Blender in an `already registered as a subclass` state.
- Retrying enable after a failed/partial registration now cleans stale CutBridge RNA registrations first.

### Changed
- Blender 5.2 LTS is now an explicit CutBridge compatibility target pending real runtime validation.
- Static CI now checks Blender `StringProperty` subtypes and regression coverage for transactional registration.
- CutBridge version bumped to 0.2.1.

## [0.2.0] - Unreleased

### Added
- Central CutBridge version constants and Blender compatibility minimum.
- Blender environment diagnostics for version, Python, platform, compatibility status, and online-access state.
- LTS-first compatibility policy targeting Blender 4.2 LTS and 4.5 LTS.
- Stable, Beta, and Development update-channel preferences.
- User-triggered and optional startup update discovery.
- Release-index schema and compatibility selection logic.
- Network checks that respect `bpy.app.online_access`.
- Deterministic `tools/build_release.py` packaging for Blender and After Effects.
- SHA-256 checksums and release metadata generation.
- CI release-build simulation on every relevant branch/PR.
- Distribution/update architecture and rollback policy documentation.

### Changed
- Blender extension manifest version bumped to 0.2.0 and now declares Animation tag, network permission, and build exclusions.
- Release workflow now validates source before packaging and uses the deterministic release builder.
- CutBridge UI now displays environment/update status.

### Safety
- Update discovery is notification-only. CutBridge does not force-update or replace active extension code.
- Private source control remains separated from public/client distribution.

## [0.1.0]

### Added
- Initial Blender metadata/validation/package MVP.
- UTF-8 `cutbridge.json` generation.
- After Effects importer, auto-comp, image-sequence import, and basic QC.
- Initial CI and release workflow foundations.
