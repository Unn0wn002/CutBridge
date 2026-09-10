# CutBridge

**CutBridge is a Blender-to-After Effects production pipeline tool for animation cuts.** It standardizes cut metadata, render-pass packaging, versioning, JSON handoff, compositing setup, QC, controlled revision handling, Japanese-first workflow UX, Studio Presets, and a bounded 3D handoff workflow so artists can move work from Blender into After Effects with less repetitive setup and fewer handoff errors.

The primary audience is Japanese animation and content-production artists and studios. English remains a deterministic supported fallback. CutBridge is not a renderer, toon shader, animation generator, general scene exporter, or asset manager; its role is the handoff layer between 3D cut production and compositing.

## Current development status

**v0.2.3 — unreleased development candidate**

Current integrated `develop` baseline after the S13F native repair:

`0a86d9a0605e1dd9714ef35a547693de76f714f4`

Product engineering and validation are complete through **S13**:

- S1–S9: baseline packaging, Blender render mapping, production hardening, AE import/revision/QC foundations, Japanese-first UX, and Studio Presets.
- S10A: Blender ↔ After Effects coordinate/timing/camera/Null contract.
- S10B: optional evaluated-world `handoff_3d` producer.
- S10C: managed AE Camera/3D Null reconstruction with native projection-parity validation.
- S11: QA, documentation, compatibility scoping, and release-readiness architecture.
- S12: release-target real-host Blender → package → After Effects campaign, reconciled to PASS after the S13 repair chain.
- S13: real-host Camera/Null revision defects repaired and native-validated through V001→V002→V003.

The exact S13F native-tested commit was:

`9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`

That exact commit passed Adobe After Effects 2026 `26.3x87` / Build 87 on Windows 11 for the repaired V001→V002→V003 path, including Camera Position/Point of Interest/Zoom refresh, Null Position/Scale refresh, QC+, artist-state preservation, zero duplicate managed Camera/Null layers, and save/close/reopen persistence. It was merged intact through PR #68 and post-merge CI passed on `develop` `0a86d9a...`.

## Current automated validation

The latest post-merge CI on `0a86d9a...` is green:

- `static-validation`: **132 passed + 2 subtests**;
- deterministic v0.2.3 release-package simulation and checksum verification: PASS;
- S6 revision regressions: PASS;
- S7 QC+ regressions: PASS;
- S8 localization regressions: PASS;
- S10C reconstruction: **8/8 groups PASS**;
- S13 3D revision native-host-shaped regression: PASS;
- ExtendScript syntax checks: PASS;
- Blender 5.2.1 RNA registration lifecycle: PASS;
- complete Blender/runtime pytest suite: **245 passed + 2 subtests**.

Automated host-shaped tests do not replace native-host evidence; the relevant real AE evidence is recorded in the S12/S13 issue history and summarized in `docs/S12_S13_EVIDENCE_SUMMARY.md`.

## Blender workflow

CutBridge currently provides:

- Project / Episode / Scene / Cut / Take / Version metadata;
- FPS, resolution, frame range, and active-camera capture;
- cut validation and deterministic package generation;
- transactional BEAUTY / LINE / SHADOW / DEPTH render-output mapping while preserving unrelated compositor nodes;
- same-version overwrite protection when render/user payload already exists;
- V001 / V002 / V003 package coexistence;
- UTF-8 `cutbridge.json` manifest generation;
- environment diagnostics and LTS-first compatibility status;
- Stable / Beta / Development update-channel preferences with notification-only update checks;
- Japanese-first / English-fallback UI;
- Studio Preset modes: Manual, CutBridge Default, and Custom JSON;
- strict data-only preset validation;
- optional evaluated-world camera/Empty sampling into `handoff_3d`.

## After Effects workflow

CutBridge currently provides:

- ExtendScript / ScriptUI package import;
- manifest schema/version/path validation;
- deterministic managed folders, comps, footage, and layer ownership;
- exact sequence-frame coverage validation;
- safe repeated Build/reload behavior and conservative collision handling;
- non-destructive revision workflow with rollback and historical-footage provenance;
- QC+ PASS / WARNING / ERROR diagnostics with stable `CBQ-*` identifiers;
- Japanese-first / English-fallback localization;
- managed Camera and 3D Null reconstruction from supported `handoff_3d` data;
- version-scoped Camera/Null revision migration using fail-closed topology checks and native-safe bulk keyframe updates.

## 3D handoff boundary

CutBridge intentionally supports a bounded 3D handoff rather than arbitrary Blender scene synchronization.

The current axis contract is:

```text
Blender (x, y, z) -> AE-oriented (x, -z, y)
```

Timing is baked using:

```text
AE time = (frame - frame_start) / fps
```

The S10C native validation measured a maximum 2D projection error of **0.00018066 px** against a **0.05 px** acceptance gate.

Unsupported camera projection, non-square pixels, sensor shift, invalid transforms/markers, unsupported topology changes, ambiguous ownership, or unsafe collisions fail closed rather than being silently approximated.

See `docs/CAMERA_NULL_HANDOFF_CONTRACT.md` and `docs/HANDOFF_3D.md`.

## Compatibility

Minimum declared Blender runtime is **4.2.0**. Current LTS-first targets are Blender **4.2 LTS**, **4.5 LTS**, and **5.2 LTS**. Blender 5.2.1 is the current authoritative automated runtime target.

After Effects **2024–2026** remains the target range, but native evidence is bounded to the hosts and scenarios actually tested. Current real-host evidence includes Adobe After Effects 2026 Build 87 (`26.3x87`) on Windows 11. This is not blanket certification for every AE/OS/workflow combination.

The Blender suite still reports `Scene.use_nodes` deprecation warnings relevant to Blender 6.0 migration. See `docs/TECHNICAL_DEBT.md`.

## Release status

**UNRELEASED / PUBLICATION BLOCKED.**

There are no GitHub Releases and `release-authorization.json` remains deliberately fail-closed:

```json
{
  "approved": false,
  "tag": null,
  "channel": null,
  "prerelease": null
}
```

Product/native validation progress does **not** authorize publication.

The remaining release blockers are primarily release engineering and governance:

1. repository-level branch/tag protection in issue #18;
2. reconciliation of the materially diverged `develop` and `main` histories through an explicit promotion candidate rather than a blind merge;
3. authoritative CI on the exact promoted `main` candidate;
4. Japanese target-user evidence appropriate to production-usability claims;
5. exact release authorization only after every prerequisite is complete;
6. published-asset checksum/content verification and production update/distribution verification.

Current GitHub plan/configuration does not provide the required private-repository ruleset controls. Do not make the source repository public merely to satisfy that gate; keep publication blocked until appropriate controls are available.

## Next product/release phase

The next bounded phase is **S14 — Japanese target-user validation and release-preparation evidence**.

Before feature expansion, keep the current S12/S13 native evidence stable, reconcile repository status documents, and prepare the deliberate `develop` → `main` promotion plan without changing release authorization.

## Key documentation

- English Quick Start: `docs/QUICK_START.md`
- 日本語 Quick Start: `docs/QUICK_START_JA.md`
- Studio Presets: `docs/STUDIO_PRESETS.md`
- 3D handoff: `docs/HANDOFF_3D.md`
- Release readiness: `docs/RELEASE_READINESS.md`
- Completion status: `docs/COMPLETION_STATUS.md`
- S12/S13 evidence summary: `docs/S12_S13_EVIDENCE_SUMMARY.md`
- Technical debt: `docs/TECHNICAL_DEBT.md`

## License

CutBridge uses **GPL-3.0-or-later**. The full GPL v3 text is included in `LICENSE` and in release packaging.