# Release Checklist

Before tagging a CutBridge release:

- [ ] Static tests pass.
- [ ] Blender extension manifest version matches the release version.
- [ ] CutBridge manifest schema remains backward-compatible or schema version is intentionally bumped.
- [ ] Blender package builds successfully.
- [ ] After Effects JSX syntax check passes.
- [ ] Changelog is updated.
- [ ] Supported Blender/After Effects versions are documented.
- [ ] Manual Blender → package → After Effects smoke test passes.
- [ ] No private client assets, credentials, or production data are included.
- [ ] Release ZIP checksums are generated.
