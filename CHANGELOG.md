# Changelog

All notable CutBridge changes are tracked here.

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
