# CutBridge Update Architecture

CutBridge should separate **source control** from **plugin distribution**.

## Development

- Private source repository: this repository.
- `main`: stable/release-ready.
- `develop`: active integration.
- `feature/*`: feature development.

## Release pipeline

1. Merge a tested release candidate to `main`.
2. Tag the release, for example `v0.2.0`.
3. GitHub Actions packages the Blender extension and After Effects script.
4. The release workflow publishes versioned ZIP files and SHA-256 checksums.

## Blender updates

The long-term target is Blender's official Extension repository mechanism rather than a self-modifying Python downloader.

Recommended production behavior:

- Check for updates automatically.
- Notify the user when a compatible release exists.
- Let the user approve installation or stage the update for restart.
- Never force-update an active production environment.
- Gate releases by Blender compatibility.
- Preserve rollback capability.

## Privacy/distribution note

The source can remain private during development. A production auto-update channel may later require a separately hosted distribution endpoint or repository that Blender clients can access without GitHub developer credentials. Do not expose the private source repository merely to implement updates.
