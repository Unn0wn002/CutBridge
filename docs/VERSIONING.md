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
5. Packaged artifact names.

CI checks the source-version pair, and `tools/build_release.py` rejects a release tag that does not match the extension manifest.

## Channels

- **stable** — intended for production-oriented testing/releases.
- **beta** — pre-release features requiring broader validation.
- **development** — experimental builds for the project team.

A selected update channel may see lower-risk channels as well: Beta can receive Stable, and Development can receive Stable/Beta/Development. Stable never selects Beta or Development releases.
