# Versioning

CutBridge uses semantic versioning during development.

- PATCH (`0.2.0` → `0.2.1`): compatible fixes or narrowly scoped additions.
- MINOR (`0.2.x` → `0.3.0`): new backward-compatible capabilities.
- MAJOR (`0.x` → `1.0.0` and later): production contract or compatibility changes that require deliberate migration.

## Release invariants

For every release, the following values must agree:

1. `apps/blender/cutbridge/blender_manifest.toml` → `version`.
2. `apps/blender/cutbridge/version.py` → `__version__` / `VERSION`.
3. Git tag → `vMAJOR.MINOR.PATCH`.
4. Changelog release heading.
5. Packaged artifact names and `release-metadata.json`.
6. Generated `cutbridge.json` → `cutbridge_version` and `bl_info["version"]`.
7. README current development version.
8. `CutBridge.jsx` → single `PRODUCT_VERSION` constant, also used by its UI.

CI checks version synchronization. `tools/build_release.py` rejects a tag that does not match the extension manifest or either canonical version constant, and rejects a missing, duplicate or mismatched AE `PRODUCT_VERSION` before writing artifacts. Update that one AE constant with the canonical Blender version; never hard-code a second version in AE UI text.

Version 0.2.3 remains unreleased. Session 1 changes packaging, tests and repository documentation without changing the Blender/AE runtime or handoff schema; it does not mint a new plugin version. Historical test versions are deliberate update-selection fixtures. `release-index.example.json` uses placeholder URLs/checksums and is not a published release.

Three schema versions are independent: Blender extension metadata uses `1.0.0`; CutBridge handoff JSON currently emits integer `1`; the update index/release metadata also uses integer `1`. These are not product versions. The shared schema permits integer versions above 1 for future producers; AE explicitly accepts only handoff version 1. S4 narrows supported export frame endpoints to non-negative integers in the schema and both producer/consumer boundaries. This rejects previously inconsistent negative-frame packages; it does not renumber animation.

## Channels

- **stable** — intended for production-oriented testing/releases.
- **beta** — pre-release features requiring broader validation.
- **development** — experimental builds for the project team.

A selected update channel may see lower-risk channels as well: Beta can receive Stable, and Development can receive Stable/Beta/Development. Stable never selects Beta or Development releases.
