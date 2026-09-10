# Changelog

All notable CutBridge changes are tracked here.

## [0.2.3] - Unreleased

### S11 — QA / Docs / Release Engineering

#### Added / changed
- Reconciled English and Japanese Quick Starts through the S10C camera/3D Null workflow and current release boundary.
- Reconciled `apps/after-effects/INSTALL.md` through S10C native reconstruction while preserving the four-runtime-file installation contract.
- Reconciled `docs/HANDOFF_3D.md` from obsolete producer-only language to the bounded S10B producer + S10C After Effects consumer workflow.
- Expanded `docs/COMPATIBILITY.md` to distinguish **bounded native evidence** from blanket host certification.
- Added canonical `docs/RELEASE_READINESS.md` separating automated QA, already-recorded native evidence, S12 release-target end-to-end validation, Japanese target-user evidence, repository governance, candidate freeze, deliberate `develop`→`main` promotion, exact authorization, publication, downloaded-asset verification, and production update/distribution verification.
- Added `tests/test_s11_docs.py` to prevent user/release docs from silently regressing to pre-S10C claims.
- Reconciled README, completion status, roadmap, and test plan so S12 is the next bounded product phase after S11 integration.

#### QA / release-engineering findings
- Existing deterministic release builder and release workflow were audited and retained: no reproducible release-runtime defect justified redesign.
- Existing release-hygiene, authorization, packaging simulation, AE regression, and Blender 5.2.1 runtime gates remain authoritative.
- Intermediate S11 CI `34449966185` passed static validation and Blender RNA registration but failed one newly added documentation regression because the assertion depended on one exact phrase; the runtime suite otherwise reported 235 PASS / 1 new-doc-test FAIL / 62 warnings / 2 subtests PASS.
- The assertion was repaired to verify the semantic managed-perspective-camera and managed-3D-Null claims separately without weakening the gate.
- Corrected head `818d9b8275319194c8c42329b8a139b35239e1aa`, CI `34450066759`: both authoritative jobs PASS.
- State-document reconciliation after that green run creates a later final S11 candidate SHA that must receive its own full CI before PR/merge.

#### Safety / release status
- S11 changes documentation, QA coverage, compatibility claims, and release-readiness organization; it does not authorize publication.
- `main` remains untouched by intended S11 work.
- `release-authorization.json` remains fail-closed.
- No release tags or GitHub Releases are created by S11.
- Issue #18 remains the independent repository-governance blocker.
- v0.2.3 remains **NOT RELEASE READY** until S12 release-target end-to-end evidence, applicable target-user evidence, repository governance, deliberate promotion, exact authorization, publication verification, and production distribution verification are complete.

### S10C — Native After Effects camera / 3D Null reconstruction

#### Added
- Native After Effects consumption of the optional S10B `handoff_3d` contract.
- Managed AE camera creation/update with baked position, point-of-interest, and Zoom keyframes.
- Managed AE 3D Null creation/update for explicitly serialized Blender Empties.
- Strict `handoff_3d` validation in `CutBridge.jsx` for schema/version, coordinate-space declaration, sampling contract, camera data, null data, finite values, and supported source types.
- Managed camera/null ownership lifecycle with fail-closed collision handling and rollback protection.
- Deterministic camera → 3D Null → footage layer ordering.
- Programmatic manifest/build/QC hooks used by the S10C native validation harness.
- `tests/ae_s10c_reconstruction_checks.cjs` and CI integration through the `Run S10C reconstruction checks` step.

#### Native validation
- Exact candidate: `3108058f03d11ccba62fb1771079e1b7fd15aa0c`.
- Candidate push CI `34439794396`: PASS.
- PR #54 event CI `34439880617`: PASS.
- Merged to `develop` as `493625ac5e83a0fcec8a858346ec96e0b4b0f2de`.
- Post-merge `develop` CI `34439972955`: PASS.
- Real host: Adobe After Effects 2026 Build 87 (`26.3x87`) on Windows 11 using Blender 5.2.1 LTS-produced handoff data.
- Maximum measured native 2D projection error: `0.00018066 px` against a `<= 0.05 px` gate.
- QC+ diagnostics: 10/10 PASS, zero errors/warnings.
- Idempotent rebuild: zero duplicate managed layers.
- Unmanaged camera/null name collisions: rejected fail-closed without adopting or damaging artist layers.
- Native project persistence verified.

#### Compatibility / safety
- S10C remains bounded to the existing `handoff_3d` camera/Empty contract; it is not general Blender ↔ AE scene synchronization.
- No geometry, lights, bones, arbitrary hierarchy recreation, or broad scene export is introduced.
- Artist-created camera/null objects are not adopted by visible name alone.
- `main`, release tags, GitHub Releases, and `release-authorization.json` are unchanged by S10C.
- Repository-level release governance issue #18 remains independently blocking publication.

### S10B — Optional evaluated-world 3D handoff producer

#### Added
- Optional, versioned `handoff_3d` manifest block using `cutbridge-handoff-3d` schema v1.
- Blender sampling for the active supported perspective camera and explicitly marked Empties.
- Per-frame evaluated-world position, normalized basis, scale, source-frame, and AE-time samples.
- Camera forward/up direction, horizontal FOV, and derived AE Zoom producer data.
- Explicit pixels-per-Blender-unit scale and strict bounds for frames, marked Empties, and total serialized samples.
- `docs/HANDOFF_3D.md`, Draft 2020-12 schema tests, and Blender 5.2.1 evaluated-world/package integration tests.

#### Compatibility / safety
- Historical manifests remain valid because `handoff_3d` is optional.
- Direct Blender Euler → AE Euler conversion remains prohibited by the S10A contract.
- Parent/constraint/driver effects may influence evaluated Blender world state, but hierarchy/rig logic is not recreated in AE.
- Non-perspective cameras, non-square pixels, sensor shift, zero-scale, shear, reflected transforms, non-Empty handoff markers, and excessive sample counts fail closed.
- Blender frame/subframe is restored after sampling, including failure paths.

#### Validation
- Exact candidate: `2a222520da9dde7128dc1b9ddc1ed29b1e7a23b2`.
- Candidate push CI `34429145031`: PASS.
- PR #51 event CI `34429245773`: PASS.
- Merged to `develop` as `444a786e6f7a64143e50f933fa35ca84ea36138e`.
- Post-merge CI `34429324559`: PASS.

### S10A — Camera / Null handoff contract investigation

#### Added
- Evidence-backed Blender ↔ After Effects coordinate/timing/camera/null contract.
- Pure producer-side axis, position, timing, FOV/Zoom, and fail-closed camera primitives in `camera_handoff.py`.
- Explicit axis map `(x, y, z) -> (x, -z, y)` and composition-center position origin.
- Explicit deterministic spatial scale rather than hidden scene-dependent inference.
- Frame-time mapping `(frame - frame_start) / fps`.
- `docs/CAMERA_NULL_HANDOFF_CONTRACT.md` with host facts, risks, deferred cases, and native-validation requirements.
- Mathematical regression fixtures for axis mapping, handedness, origin, timing, Zoom, and unsupported camera cases.

#### Compatibility / safety
- No direct Blender Euler → AE Euler mapping is approved.
- Evaluated world-space/basis data is the chosen implementation strategy.
- Initial camera contract is restricted to perspective cameras, square pixels, and zero sensor shift.
- Initial Empty/Null strategy is baked/unparented world-space reconstruction rather than Blender hierarchy replication.

#### Validation
- Exact candidate: `8a87044f8b7c830f342a1cd26568f6a3e05cf503`.
- Candidate push CI `34427616559`: PASS.
- PR #49 event CI `34427691064`: PASS.
- Merged to `develop` as `7b506d357faea08ea936daa90ccd0c94ea565f21`.
- Post-merge CI `34427809612`: PASS.

### S9 — Studio Presets

#### Added
- Versioned, declarative `cutbridge-studio-preset` schema v1.
- Blender Studio Preset modes: Manual, CutBridge Default, and Custom JSON.
- Safe built-in default preset plus `docs/examples/studio-preset.default.json`.
- Strict preset validation for schema/version, known fields, naming templates, folder roles, pass definitions/order, sequence format, and version-token conventions.
- Bounded 64 KiB UTF-8-only custom JSON loader.
- Configurable package naming, render/preview/camera folder roles, pass order and required/optional policy, PNG/OpenEXR/TIFF sequence format, version-token prefix/padding, and After Effects comp naming.
- Optional normalized `studio_preset` provenance in `cutbridge.json` without storing the source preset path.
- Japanese/English Studio Preset UI text and stable `PRESET_*` diagnostic codes.
- Dedicated Studio Preset authoring/security documentation and English/Japanese Quick Start integration.

#### Compatibility / safety
- Manual remains the default and preserves historical package identity behavior.
- Canonical `safe_token`, `version_token`, and `package_name` producer primitives remain unchanged.
- Custom preset folders must be safe relative, disjoint role trees; absolute/traversal/overlapping paths fail closed.
- Presets cannot execute code or expressions, expand commands/environment variables, trigger network behavior, or adopt existing AE objects.
- After Effects does not parse Studio Preset JSON; it consumes resolved manifest values only.

### S8 — Japanese-first UX

#### Added
- First-class Japanese and deterministic English localization architecture in Blender and After Effects.
- Blender JA/EN language control and localized panel sections, actions, validation/build reports, environment/update UX, and production terminology.
- After Effects `localization.js` sidecar with locale-aware panel/actions/status/QC/revision guidance while preserving stable `CBQ-*` identifiers.
- S8 regression coverage for missing translation keys, invalid locale, locale persistence, safe fallback, non-mutation, and narrow-safe Blender panel layout.

#### Fixed
- Blender native testing found material clipping at approximately 245 px N-panel width; core fields/actions/pass controls were re-laid out.
- AE native testing found persisted Japanese + missing `localization.js` could render English fallback while the visible selector still said Japanese; fallback and selector synchronization were repaired.

#### Validation
- Repaired candidate: `f477b745cc600b85708b63d059d6c4eaed9f0249`.
- Blender 5.2.1 LTS native retest: PASS.
- Adobe After Effects 2026 Build 87 native retest: PASS.
- Merged to `develop` as `368b977582feadc26543825b4d31ffd5f6266a4f`.
- Post-merge CI `34380737455`: PASS.

### S7 — QC+

#### Added
- Deterministic `CBQ-*` PASS / WARNING / ERROR QC+ diagnostic engine.
- Safe remediation text for warning/error findings.
- Sequence, comp, managed footage/layer, host ownership, and revision-aware diagnostics.
- Native binding from `CutBridge.jsx` through `qc_plus.js`.

#### Fixed
- Repaired an ExtendScript compatibility defect caused by an unquoted reserved `package` object key in `qc_plus.js`.
- Repaired incorrect revision compatibility state from a nested ternary in `revision_manager.js`.

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

#### Safety / validation
- Revision blocks incompatible geometry, pass-set additions/removals, stale/foreign ownership, ambiguous package structure, and invalid managed-layer state before mutation.
- Native source replacement uses `AVLayer.replaceSource(newSource, false)` and verifies live source state.
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

### Technical debt

- Current Blender 5.2.1 suite passes but emits `Scene.use_nodes` deprecation warnings expected to matter for Blender 6.0.
- Some pinned GitHub Actions revisions still target deprecated Node 20 runtimes and are currently forced by GitHub onto Node 24; pins should be refreshed deliberately.
- `main` / `develop` promotion must be reconciled deliberately before an RC.
- S10C native reconstruction has passed its bounded AE parity gate, but broader release-target end-to-end host/OS coverage and Japanese target-user evidence remain separate requirements.

### Release status

- v0.2.3 remains unreleased / NOT RELEASE READY.
- No release tag or GitHub Release exists.
- `release-authorization.json` remains unapproved by design.
- Repository-level release governance issue #18 remains independently blocking publication.
- S12 release-target end-to-end validation is the next product gate after S11 integration.

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
