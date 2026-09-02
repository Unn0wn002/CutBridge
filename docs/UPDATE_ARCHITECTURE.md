# CutBridge Update Architecture

CutBridge separates **private source control** from **plugin distribution**. The private GitHub repository is never treated as the client update server.

## Development source

- Private source repository: `Unn0wn002/CutBridge`.
- `main`: stable/release-ready source.
- `develop`: active integration.
- `feature/*`: isolated work.

## Release pipeline

1. A tested release candidate is merged to `main`.
2. The manifest version and `version.py` must match.
3. A semantic tag such as `v0.2.0` triggers `.github/workflows/release.yml`.
4. CI runs the complete static test suite and validates After Effects JSX syntax.
5. `tools/build_release.py` creates:
   - `CutBridge-Blender-vX.Y.Z.zip`
   - `CutBridge-AfterEffects-vX.Y.Z.zip`
   - `SHA256SUMS.txt`
   - `release-metadata.json`
6. GitHub Release stores the build artifacts for the development team.
7. Production distribution later mirrors approved artifacts to a separately hosted update endpoint.

The build script rejects a release tag when it does not exactly match `blender_manifest.toml`.

## Blender update model

The production target is Blender's official **Remote Extension Repository** mechanism. Blender remote repositories support listing and updating extensions and can check for repository updates at startup.

CutBridge also contains a lightweight **notification checker**. It reads a separate CutBridge release index and only answers:

- Is a newer release available?
- Is it compatible with this Blender version?
- Is it compatible with this platform?
- Is it visible on the selected Stable/Beta/Development channel?

The checker **never downloads, installs, replaces, or deletes active CutBridge code**.

### User-approved update flow

```text
Blender starts
    ↓
CutBridge diagnostics
    ↓
Optional release-index check
    ↓
Compatible update found?
    ├── No  → Up to date
    └── Yes → Show version + release page
                         ↓
                   User reviews update
                         ↓
              Blender/distribution workflow
                         ↓
                  User-approved install
```

## Update index

The client format is defined by:

- `packages/update/release-index.schema.json`
- `packages/update/release-index.example.json`

A production index should be hosted on a static HTTPS endpoint that does **not** expose the private source repository. A single host may contain both:

- Blender's generated extension repository `index.json` and release ZIP files.
- CutBridge's small release-notification index.

The in-plugin update URL remains blank in source until such an endpoint is deployed. Users/developers may configure a test endpoint in Blender Preferences.

## Blender online-access policy

CutBridge checks `bpy.app.online_access` before any HTTP request. If Blender online access is disabled, CutBridge reports that state and performs no remote request.

## Rollback policy

Rollback is a distribution concern, not an active-session self-modification feature.

- Keep previous stable release ZIPs available.
- Never delete the previous stable release when publishing a new one.
- Use compatibility metadata to prevent incompatible upgrades.
- Allow a production user to reinstall a known-good previous release.
- Never force an update during an active project.

## Privacy rule

**Do not make the private source repository public solely to implement updates.** Distribution artifacts and update metadata must be published separately.
