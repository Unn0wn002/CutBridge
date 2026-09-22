# CutBridge Update Architecture

CutBridge separates **source-repository hosting** from **plugin distribution**. Repository visibility does not make the GitHub source repository the client update server.

## Development source

- Source repository: `Unn0wn002/CutBridge` (currently public and protected by branch/tag rulesets).
- `main`: protected promotion/release-candidate branch; promotion does not itself authorize publication.
- `develop`: protected active integration branch.
- `feature/*`: isolated work.

## Release pipeline

1. A tested release candidate is merged/promoted to `main`.
2. The manifest version and `version.py` must match the After Effects `PRODUCT_VERSION`.
3. Keep `release-authorization.json` unapproved until the exact `main` candidate has satisfied the applicable independent-review, real-app/manual, and CI gates.
4. Commit an explicit authorization for one exact tag/channel/prerelease combination; that authorization change must itself be validated.
5. A supported tag on the **current `main` HEAD** triggers `.github/workflows/release.yml`:
   - stable: `vX.Y.Z`
   - beta validation: `vX.Y.Z-rc.N` or `vX.Y.Z-beta.N`
   - development validation: `vX.Y.Z-dev.N`
6. The workflow fails before packaging if the tagged SHA is not current `main`, authorization is absent/unapproved, or tag/channel/prerelease metadata disagree.
7. CI runs the complete test suite, Blender RNA lifecycle validation, and After Effects JSX syntax checks.
8. `tools/build_release.py` creates:
   - `CutBridge-Blender-<tag>.zip`
   - `CutBridge-AfterEffects-<tag>.zip`
   - `SHA256SUMS.txt`
   - `release-metadata.json`
9. GitHub Release stores the validation/release artifacts for the development team. RC/beta/development tags are marked GitHub prereleases; the unsuffixed stable tag is not.
10. Download the published assets and independently re-verify contents/checksums before any distribution claim.
11. Production distribution mirrors approved stable artifacts and update metadata to the separately hosted `Unn0wn002/cutbridge-distribution` endpoint.

The release builder validates the numeric product version against `blender_manifest.toml`, `version.py`, and After Effects. Publication authorization is a separate gate and must never be inferred merely from matching versions or green CI.

## Release authorization is fail-closed

Root `release-authorization.json` defaults to an unapproved state. The release workflow requires all of the following:

- tagged SHA equals current `origin/main` HEAD;
- `approved` is exactly `true`;
- authorization `tag` equals the triggering tag;
- authorization `channel` equals the tag-derived channel;
- authorization `prerelease` equals the tag-derived prerelease status.

This prevents a stale feature/develop commit—or an old but correctly versioned `main`—from being published merely because somebody creates a matching tag. The authorization file is a technical lock, not a substitute for review/manual release evidence.

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

A production index should be hosted on a static HTTPS endpoint separate from the source repository and its development/release-control surface. A single host may contain both:

- Blender's generated extension repository `index.json` and release ZIP files.
- CutBridge's small release-notification index.

Production D1 is deployed and verified at:

- CutBridge notification index: `https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json`;
- Blender repository index: `https://unn0wn002.github.io/cutbridge-distribution/blender/index.json`.

The released v0.2.3 client keeps its compiled update URL blank. The v0.2.4 source baseline points its **manual** notification checker to the verified production index. The endpoint is not stored as a user-editable Blender RNA string and contains no credentials.

Automatic startup update scheduling remains disabled following Issue #82. Wiring the manual endpoint does not restore `bpy.app.timer` registration or background checks.

RC/beta/development GitHub Releases remain **manual validation artifacts** unless a matching entry is deliberately published to the production distribution. Do not represent GitHub prerelease publication alone as a functioning beta update channel inside Blender.

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

**Do not use source-repository visibility as an update-distribution mechanism.** Distribution artifacts and update metadata must be published through the separately verified distribution path.
