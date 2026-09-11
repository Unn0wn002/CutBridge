# Versioning

CutBridge uses semantic versioning during development.

- PATCH (`0.2.0` → `0.2.1`): compatible fixes or narrowly scoped additions.
- MINOR (`0.2.x` → `0.3.0`): new backward-compatible capabilities.
- MAJOR (`0.x` → `1.0.0` and later): production contract or compatibility changes that require deliberate migration.

## Release invariants

For every release, the following values must agree:

1. `apps/blender/cutbridge/blender_manifest.toml` → product `version`.
2. `apps/blender/cutbridge/version.py` → `__version__` / `VERSION`.
3. Stable Git tag → `vMAJOR.MINOR.PATCH`, or validation prerelease tag → `vMAJOR.MINOR.PATCH-rc.N`, `-beta.N`, or `-dev.N`.
4. Changelog release heading.
5. Packaged artifact names and `release-metadata.json`.
6. Generated `cutbridge.json` → `cutbridge_version` and `bl_info["version"]`.
7. README current development version.
8. `CutBridge.jsx` → single `PRODUCT_VERSION` constant, also used by its UI.

The numeric product version in Blender/AE stays `MAJOR.MINOR.PATCH`. A prerelease tag adds distribution metadata without changing the source product version: for example, source `0.2.3` may produce validation artifact `0.2.3-rc.1`.

CI checks version synchronization. `tools/build_release.py` rejects a tag whose numeric product version does not match the extension manifest or either canonical version constant, and rejects a missing, duplicate or mismatched AE `PRODUCT_VERSION` before writing artifacts. Update that one AE constant with the canonical Blender version; never hard-code a second version in AE UI text.

## Publication authorization

A matching version is **not** sufficient authorization to publish.

The tag-triggered Release workflow must also pass `tools/validate_release_authorization.py`. Publication fails closed unless:

1. the tagged SHA is exactly the current `main` HEAD;
2. root `release-authorization.json` exists;
3. `approved` is exactly `true`;
4. the authorization `tag` exactly matches the triggering tag;
5. the authorization `channel` and `prerelease` values exactly match the tag semantics.

The repository keeps `release-authorization.json` unapproved by default. Changing it to an approved release is a deliberate release-candidate change that must itself pass the applicable review, real-app validation, and exact-head CI gates before tagging. Never use the authorization file to bypass those gates.

Supported tag/channel mapping:

- `vX.Y.Z` → `stable`, GitHub Release is not a prerelease.
- `vX.Y.Z-rc.N` → `beta`, GitHub Release is a prerelease.
- `vX.Y.Z-beta.N` → `beta`, GitHub Release is a prerelease.
- `vX.Y.Z-dev.N` → `development`, GitHub Release is a prerelease.

Other tag forms fail closed.

Version 0.2.3 remains unreleased. Historical test versions are deliberate update-selection fixtures. `release-index.example.json` uses placeholder URLs/checksums and is not a published release.

Three schema versions are independent: Blender extension metadata uses `1.0.0`; CutBridge handoff JSON currently emits integer `1`; the update index/release metadata also uses integer `1`. These are not product versions. The shared schema permits integer versions above 1 for future producers; AE explicitly accepts only handoff version 1. S4 narrows supported export frame endpoints to non-negative integers in the schema and both producer/consumer boundaries. This rejects previously inconsistent negative-frame packages; it does not renumber animation.

## Channels

- **stable** — intended for production-oriented testing/releases.
- **beta** — release candidates/pre-release features requiring broader validation.
- **development** — experimental builds for the project team.

A selected update channel may see lower-risk channels as well: Beta can receive Stable, and Development can receive Stable/Beta/Development. Stable never selects Beta or Development releases.

The production update endpoint is not deployed yet. Until it exists and its index-generation/publication process is verified, RC/beta/development GitHub Releases are validation artifacts to install/download deliberately; do not claim that the in-plugin updater distributes them.
