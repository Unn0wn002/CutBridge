# CutBridge

**CutBridge is a Blender → After Effects production handoff tool for animation cuts.**

It standardizes cut metadata, render-pass packaging, versioning, `cutbridge.json` handoff, After Effects project setup, QC, controlled revision handling, Japanese-first workflow UX, Studio Presets, and an optional bounded Camera/3D Null handoff.

CutBridge is designed for Japanese animation and content-production workflows, with a Japanese-first UI and deterministic English fallback. This is an implementation/design statement rather than a representative-user usability claim: S14B target-user validation remains NOT_EXECUTED. CutBridge is **not** a renderer, toon shader, animation generator, general scene exporter, or asset manager. Its job is to make the Blender → compositing handoff more repeatable, inspectable, and safer.

**v0.2.5 — unreleased development baseline.** GitHub Release v0.2.4 is published and immutable. Production distribution intentionally remains on v0.2.3 because the immutable v0.2.4 After Effects ZIP contains stale pre-publication `INSTALL.md` wording tracked in Issue #99. The source fix is included in v0.2.5 development; no v0.2.5 release is authorized or published.

## What CutBridge does

Typical workflow:

```text
Blender cut
  ↓
Cut metadata + Studio Preset
  ↓
Validate Cut
  ↓
Build Package
  ↓
Render sequences
  ↓
cutbridge.json + render payload
  ↓
After Effects Import / Build
  ↓
QC+
  ↓
Compatible V001 → V002 → V003 revisions
```

CutBridge currently provides:

- Project / Episode / Scene / Cut / Take / Version metadata;
- FPS, resolution, frame range, and active-camera capture;
- deterministic package and manifest generation;
- BEAUTY / LINE / SHADOW / DEPTH render-output mapping;
- same-version overwrite protection;
- versioned package coexistence such as V001 / V002 / V003;
- Japanese-first / English-fallback UI;
- Manual, CutBridge Default, and Custom JSON Studio Presets;
- After Effects package import and managed project construction;
- deterministic QC+ diagnostics with stable `CBQ-*` identifiers;
- non-destructive compatible revision handling;
- optional bounded Blender Camera / Empty → AE Camera / 3D Null handoff.

## Current development status

Engineering/native-host validation is complete through **S13**. **S14A**, the Japanese target-user validation protocol and fail-closed evidence tooling, is integrated. The v0.2.3 release-facing Japanese claim scope was deliberately narrowed instead of claiming S14B completion. **S14B remains NOT_EXECUTED** and is reserved for a future release or claim that needs representative Japanese target-user usability evidence.

GitHub Release v0.2.4 was published from protected `main` at `a393e409d19445c4090460b7e7b4716779161fa4`; tag `v0.2.4` points to that exact commit. Its published assets were independently verified. The separate production distribution intentionally remains on verified v0.2.3 while Issue #99 is carried forward through the v0.2.5 patch line:

- release index: `https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json`;
- Blender repository: `https://unn0wn002.github.io/cutbridge-distribution/blender/index.json`;
- distribution commit: `635c1384af2649d4ce49705cce41f98826a861cc`.

The v0.2.5 development baseline reconciles the published v0.2.4 `main` history with the Issue #99 source fix from protected `develop`. Product identity is bumped to 0.2.5 and `release-authorization.json` is restored to fail-closed. The manual update checker continues to use the verified production notification index; automatic startup update scheduling remains disabled after Issue #82.

The exact S13F native-tested source was:

```text
9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95
```

That native-tested repair was integrated through the S13F merge chain before the later documentation/S14A closeout work. S13 real-host validation includes Adobe After Effects 2026 `26.3x87` / Build 87 on Windows 11 for the repaired V001 → V002 → V003 workflow. The tested path covered Camera Position / Point of Interest / Zoom updates, Null Position / Scale updates, QC+, artist-state preservation, zero duplicate managed Camera/Null layers, and save/close/reopen persistence.

The bounded S10C Camera/Null reconstruction test measured a maximum 2D projection error of **0.00018066 px** against a **0.05 px** acceptance gate.

Native-host evidence is intentionally scoped to the exact tested hosts and scenarios. It is not blanket certification for every Blender, After Effects, OS, camera configuration, or production pipeline.

---

# How to Use CutBridge

This is the shortest end-to-end path. For detailed validation rules and edge cases, use [`docs/QUICK_START.md`](docs/QUICK_START.md). A Japanese guide is available at [`docs/QUICK_START_JA.md`](docs/QUICK_START_JA.md).

## 1. Install CutBridge in Blender

For development testing, use a verified CutBridge Blender ZIP built from the exact candidate you intend to test.

1. Open a supported Blender version.
2. Open **Preferences** and use the appropriate **Install from Disk** / extension installation action.
3. Select the CutBridge Blender ZIP and enable it.
4. Open a **3D View**.
5. Press `N` to open the sidebar.
6. Select the **CutBridge** tab.

Minimum declared Blender runtime: **4.2.0**.

Current LTS-first targets include Blender **4.2 LTS**, **4.5 LTS**, and **5.2 LTS**. Blender **5.2.1** is the current authoritative automated runtime target.

## 2. Prepare the Blender cut

Before building a package:

1. Save the `.blend` file.
2. Assign an active scene camera.
3. Set FPS and resolution.
4. Set the export frame range.
5. Enter Project / Episode / Scene / Cut / Take / Version metadata.
6. Select the package output directory.
7. Choose a **Studio Preset Mode**.

### Studio Preset modes

**Manual** keeps pass and sequence-format controls directly editable.

**CutBridge Default** uses the built-in CutBridge conventions.

**Custom JSON** loads a validated data-only Studio Preset. CutBridge validates the preset before package creation; presets cannot execute arbitrary Blender operations.

See [`docs/STUDIO_PRESETS.md`](docs/STUDIO_PRESETS.md).

## 3. Run Validate Cut

Click **Validate Cut** before building the package.

Validation covers the handoff contract, including:

- identifiers and metadata;
- active camera;
- FPS and resolution;
- frame range;
- selected/resolved render passes;
- Studio Preset validity;
- output target;
- renderer / View Layer capability;
- package-target safety;
- optional 3D handoff validity when enabled.

If CutBridge reports an **ERROR**, fix the problem before continuing. Review warnings rather than ignoring them.

## 4. Build the package

After validation passes, click **Build Package**.

A normal Manual/default package resembles:

```text
PROJECT_EP01_SC010_C012_T01_V001/
├── cutbridge.json
├── camera/
├── preview/
└── render/
    ├── beauty/
    ├── line/
    ├── shadow/
    └── depth/
```

The exact package structure depends on the resolved Studio Preset and enabled passes.

`cutbridge.json` is the handoff contract consumed by the After Effects side.

### Version safety

Do not overwrite an existing same-version package that already contains render/user payload. Create the next version instead:

```text
V001 → V002 → V003
```

CutBridge intentionally fails closed around unsafe same-version replacement.

## 5. Render the required sequences

Render using the CutBridge-configured outputs.

Before moving to After Effects, confirm required pass folders contain the expected frame range. Optional passes may be absent only when permitted by the manifest contract.

## 6. Install CutBridge in After Effects

The current development runtime uses four adjacent files:

```text
CutBridge.jsx
revision_manager.js
qc_plus.js
localization.js
```

**Keep all four files together.**

For a first test:

1. Open After Effects.
2. Choose **File → Scripts → Run Script File...**.
3. Select `CutBridge.jsx`.
4. Confirm the CutBridge panel opens.
5. Use the Japanese / English selector as needed.

For a dockable panel, place all four files in the installed After Effects version's `Scripts/ScriptUI Panels` directory, restart After Effects, then open **Window → CutBridge**.

See [`apps/after-effects/INSTALL.md`](apps/after-effects/INSTALL.md).

## 7. Load `cutbridge.json` and Build

In the CutBridge panel:

1. Select the package's `cutbridge.json`.
2. Review the package identity.
3. Confirm FPS, frame count, and validation state.
4. Run **Build**.

CutBridge creates/reuses only verified CutBridge-managed project objects. It does not automatically adopt unrelated artist objects merely because they have similar names.

If a valid optional `handoff_3d` block exists, CutBridge can reconstruct the supported managed Camera and 3D Null subset.

## 8. Run QC+

After Build, run **QC**.

QC+ reports deterministic PASS / WARNING / ERROR diagnostics using stable `CBQ-*` identifiers. Typical checks include:

- package and manifest state;
- required/optional sequence availability;
- comp resolution, pixel aspect, FPS, and duration;
- managed footage/layer ownership;
- source consistency;
- Camera/Null state where applicable;
- revision compatibility boundaries.

QC is **diagnostic-only**. It does not silently repair ownership, replace sources, or mutate unrelated artist content.

## 9. Apply a compatible revision

When Blender produces a newer package such as V002:

1. Keep the current AE project intact.
2. Select the newer CutBridge package through the revision workflow.
3. Review compatibility diagnostics.
4. Confirm compatible warning-class changes when prompted.
5. Apply the revision.
6. Run Build/QC again.

CutBridge updates only verified managed state inside its revision boundary. Incompatible geometry/pass-set/ownership/package-structure changes fail before unsafe source replacement.

The tested S13 path includes chained:

```text
V001 → V002 → V003
```

with artist-owned state preserved for the tested fixture.

## 10. Save, close, and reopen normally

Save the After Effects project normally. After reopening, reopen/reload CutBridge and run QC when you need to verify the managed workflow remains coherent.

The native S13 test covered save → close → reopen persistence for the tested AE 2026 workflow.

---

## Optional Camera / 3D Null handoff

The 3D handoff is deliberately bounded. It is **not** general Blender scene synchronization.

Current mapping:

```text
Blender (x, y, z) → AE-oriented (x, -z, y)
```

Timing:

```text
AE time = (frame - frame_start) / fps
```

Supported producer scope includes the active perspective camera and explicitly marked Blender Empties under the documented constraints.

CutBridge does **not** promise arbitrary geometry, lights, bones, rigs, hierarchy recreation, or full-scene synchronization.

See [`docs/HANDOFF_3D.md`](docs/HANDOFF_3D.md) and [`docs/CAMERA_NULL_HANDOFF_CONTRACT.md`](docs/CAMERA_NULL_HANDOFF_CONTRACT.md).

## Japanese / English behavior

Japanese is the intended first-class/default UI language. English is the deterministic fallback/support language.

Changing language must not alter package identity, manifest values, managed ownership, Studio Preset resolution, QC identifiers, revision decisions, or unrelated Blender/AE project state.

## Compatibility

### Blender

- Minimum declared runtime: **4.2.0**
- LTS-first targets: **4.2 LTS / 4.5 LTS / 5.2 LTS**
- Current authoritative automated runtime: **5.2.1**

### After Effects

Target range: **After Effects 2024–2026**.

Current real-host evidence includes **After Effects 2026 Build 87 (`26.3x87`) on Windows 11**. This does not imply every AE/OS combination has been natively certified.

See [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md).

## Release status

**v0.2.5 UNRELEASED / PUBLICATION NOT AUTHORIZED.** GitHub Release v0.2.4 remains published and immutable. Production distribution remains on v0.2.3 pending a corrected post-v0.2.4 release.

`release-authorization.json` remains deliberately fail-closed:

```json
{
  "approved": false,
  "tag": null,
  "channel": null,
  "prerelease": null
}
```

Before any v0.2.5 publication:

1. merge the reviewed baseline through protected `develop` only after authoritative CI;
2. complete applicable native validation for an exact future candidate;
3. explicitly authorize one exact current-main/tag/channel/prerelease tuple only at release time;
4. publish only through the guarded Release workflow;
5. independently verify published artifacts before adding a production distribution entry.

For v0.2.3, S14B is **not** listed as a prerequisite because the release-facing claim is explicitly narrowed. The release must not state or imply representative Japanese-user validation, customer validation, proven ease of use, broad Japanese production usability, or S14B PASS.

The source repository is now public and protected by active branch/tag rulesets. Repository visibility is not a substitute for release authorization, release-tag eligibility, artifact verification, or a production update/distribution channel.

## Development roadmap

```text
S1–S13  ✅ engineering/native validation completed for documented scope
S14A    ✅ Japanese target-user protocol + evidence tooling integrated
S14B    ⏸ NOT_EXECUTED; deferred for broader future usability claims
v0.2.3  ✅ production distribution remains deployed
v0.2.4  ✅ GitHub stable release published; production distribution held for Issue #99
v0.2.5  🛠 patch-development baseline; authorization false
```

S14 target-user evidence must come from real representative participants. CI, localization, owner testing, simulated participants, or AI-generated feedback do not count as real target-user validation. Accordingly, v0.2.3 makes no representative Japanese-user usability claim.

See [`docs/S14_JP_USER_VALIDATION.md`](docs/S14_JP_USER_VALIDATION.md).

## Documentation

- [English Quick Start](docs/QUICK_START.md)
- [日本語 Quick Start](docs/QUICK_START_JA.md)
- [After Effects Installation](apps/after-effects/INSTALL.md)
- [Studio Presets](docs/STUDIO_PRESETS.md)
- [3D Handoff](docs/HANDOFF_3D.md)
- [Compatibility](docs/COMPATIBILITY.md)
- [S14 Japanese Target-User Validation](docs/S14_JP_USER_VALIDATION.md)
- [Release Readiness](docs/RELEASE_READINESS.md)
- [Completion Status](docs/COMPLETION_STATUS.md)
- [S12/S13 Evidence Summary](docs/S12_S13_EVIDENCE_SUMMARY.md)
- [Technical Debt](docs/TECHNICAL_DEBT.md)

## License

CutBridge uses **GPL-3.0-or-later**. The full GPL v3 text is included in [`LICENSE`](LICENSE) and in release packaging.
