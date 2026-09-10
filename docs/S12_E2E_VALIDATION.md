# CutBridge S12 — Release-Target End-to-End Validation

Status: **NATIVE CAMPAIGN NOT YET EXECUTED**

S12 validates the real desktop workflow:

`Blender artifact → real Blender GUI → CutBridge package + real sequences → exact After Effects runtime → Build / QC / Revision / save-reopen → recorded evidence`

This document is an execution runbook. Passing CI, unit tests, host-shaped tests, or `tools/s12/validate_evidence.py` does **not** establish native S12 PASS.

## 1. Verdict states

The S12 evidence record uses exactly one overall state:

- `NOT_EXECUTED` — no native campaign has started;
- `IN_PROGRESS` — at least one required native gate has been attempted but the campaign is incomplete;
- `PASS` — every required native gate passed and all required host/artifact/fixture/evidence fields are populated;
- `FAIL_REPAIR_REQUIRED` — one or more real-host gates failed and the finding requires investigation/repair.

Do not translate an incomplete or blocked campaign into PASS.

## 2. Candidate identity rule

Before native testing, freeze the exact `develop` SHA and build artifacts from that exact source state.

Record:

- exact `develop` SHA;
- Blender ZIP filename + SHA-256;
- After Effects ZIP filename + SHA-256;
- Blender version + OS;
- After Effects version + OS;
- fixture identifier/provenance + SHA-256.

If source changes after artifacts are built, the previous artifact evidence does not validate the changed candidate. Rebuild artifacts and repeat the affected release-target gates.

S12 preparation began from S11-integrated `develop`:

`6a0180e6141e0eac09c80b4767825978b115d07e`

That SHA is a preparation baseline, not automatically the eventual release candidate.

## 3. Evidence record setup

Copy the fail-closed template before testing.

PowerShell:

```powershell
Copy-Item tools\s12\evidence-template.json .\s12-evidence.json
python tools\s12\validate_evidence.py .\s12-evidence.json
```

Initial expected result:

```text
S12 evidence VALID: state=NOT_EXECUTED
Native S12 PASS has not been established by this record.
```

Do not start by copying a fake PASS example. No committed fake-PASS record should be used as native evidence.

## 4. SHA-256 recording

### Windows PowerShell

```powershell
Get-FileHash -Algorithm SHA256 .\CutBridge-Blender-*.zip
Get-FileHash -Algorithm SHA256 .\CutBridge-AfterEffects-*.zip
Get-FileHash -Algorithm SHA256 .\fixture.blend
```

### Python fallback

```python
from hashlib import sha256
from pathlib import Path

path = Path("file-to-hash")
h = sha256()
with path.open("rb") as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b""):
        h.update(chunk)
print(h.hexdigest())
```

Record lowercase 64-character SHA-256 values in the evidence JSON.

## 5. Fixture provenance

Use only:

- `synthetic-original` — created specifically for CutBridge validation; or
- `user-owned-original` — an original asset the tester owns and is authorized to use.

Do not use third-party studio production files, leaked assets, or copyrighted fixtures whose redistribution/evidence use is not authorized.

Recommended synthetic fixture ID:

`cutbridge-s12-synthetic-v1`

The fixture should be simple enough to diagnose but rich enough to exercise the release claim:

- one supported perspective camera;
- several render-visible geometric objects;
- stable lighting/materials sufficient to produce visible sequences;
- one or more explicitly marked Blender Empties for S10 handoff;
- at least one animated object/camera component appropriate to the claimed workflow;
- deterministic frame range and FPS;
- Japanese/Unicode metadata or path segment for the path gate;
- no dependency on external paid assets or missing add-ons.

## 6. Revision campaign design

Use three compatible package versions.

### V001 — baseline

- baseline cut metadata;
- fixed resolution/FPS/frame range;
- fixed required pass set;
- initial render content;
- optional S10 camera/Empty handoff enabled if this feature is in the release claim.

### V002 — compatible content revision

Change content that should remain compatible with S6 revision semantics, for example:

- animation/object appearance/rendered content;
- camera motion within the supported contract;
- Empty motion within the supported handoff contract.

Keep compatibility-critical geometry of the package contract unchanged:

- same resolution;
- same FPS;
- same frame-range geometry;
- same required/optional pass set;
- compatible managed identity.

### V003 — second compatible revision

Make another content-only compatible change. V003 proves that revision safety is not a single-update special case.

If the intended change is intentionally incompatible, test it separately as a fail-closed negative case; do not use it as the required V001→V002→V003 success chain.

## 7. Blender native campaign

### B_INSTALL

1. Start from the exact candidate Blender ZIP.
2. Record its filename and SHA-256.
3. Install it through the actual Blender GUI release-target installation flow.
4. Record Blender full version/build and OS.
5. Confirm CutBridge enables cleanly and the N-panel is available.
6. Capture evidence.

### B_VALIDATE_MANUAL

1. Open/create the S12 fixture.
2. Set Project/Episode/Scene/Cut/Take/Version.
3. Set resolution, FPS, frame range, active camera, package output.
4. Use **Manual** Studio Preset mode.
5. Run **Validate Cut** in the release-claimed locale(s).
6. Confirm the decision and diagnostics are correct.
7. Capture evidence.

### B_STUDIO_PRESET

Exercise each Studio Preset mode actually included in the intended release claim.

At minimum, if CutBridge Default is claimed:

1. switch to **CutBridge Default**;
2. Validate Cut;
3. confirm resolved naming/folders/pass policy/format/comp naming;
4. return to the intended package mode for the main campaign or create a separate package fixture.

If Custom JSON is part of the claim, use a legal local test preset and record its hash. Do not silently treat untested modes as validated.

### B_HANDOFF_3D

If S10 handoff is part of the release claim:

1. enable `handoff_3d_enabled` explicitly;
2. record `pixels_per_blender_unit`;
3. mark only intended Empties with `cutbridge_handoff_3d = true`;
4. confirm the active camera satisfies perspective / square-pixel / zero-shift rules;
5. Validate Cut;
6. verify unsupported cases are not being approximated;
7. capture the produced `handoff_3d` manifest evidence.

If the release claim excludes the optional S10 path, update the release claim rather than falsely marking this required S12 gate PASS. The current S12 gate set assumes the feature is included.

### B_BUILD_V001

1. Build Package for V001.
2. Confirm expected package structure and `cutbridge.json`.
3. Confirm no unrelated files were modified.
4. Record package path and manifest evidence.

### B_RENDER_REAL

Render real sequences through Blender from the fixture.

This must be actual Blender render output, not placeholder files generated only to satisfy filename checks.

Confirm:

- required passes exist;
- expected frame range is complete;
- naming/padding matches manifest;
- optional pass behavior matches the selected contract;
- output is visually non-empty/meaningful enough for AE verification.

### B_BUILD_V002_V003

Repeat the package + real render process for compatible V002 and V003. Record the manifest/package evidence for all three versions.

## 8. After Effects native campaign

### AE_LOAD_RUNTIME

1. Record exact AE package/runtime ZIP filename + SHA-256.
2. Extract/use the four shipped runtime files:
   - `CutBridge.jsx`
   - `revision_manager.js`
   - `qc_plus.js`
   - `localization.js`
3. Record After Effects full version/build and OS.
4. Load the exact candidate runtime in the real desktop host.
5. Confirm the panel opens normally.

### AE_BUILD_V001

1. Load V001 `cutbridge.json`.
2. Build the package.
3. Confirm deterministic managed folder/comp/footage/layer state.
4. Confirm required sequences are present and interpreted correctly.
5. Confirm unrelated artist state is not adopted.
6. Capture evidence.

### AE_QC_V001

Run QC+ after V001 Build.

Record:

- PASS/WARNING/ERROR summary;
- any `CBQ-*` records;
- exact remediation text if warnings/errors exist;
- screenshots/logs.

A material QC ERROR blocks S12 PASS.

### AE_S10C_CAMERA_NULL

For packages containing valid `handoff_3d`:

1. confirm managed camera creation/reuse;
2. confirm expected managed 3D Nulls;
3. confirm no duplicate managed camera/null layers after repeated Build;
4. confirm same-name unmanaged artist objects are not adopted;
5. confirm projection/orientation behavior remains consistent with the S10C bounded contract;
6. record evidence.

S12 does not need to re-prove every S10C synthetic math case, but it must prove the released candidate artifacts actually carry the S10C workflow end to end.

## 9. Artist-state preservation fixture

Before V002 revision, deliberately add representative artist-authored AE state that CutBridge claims to preserve.

Recommended test objects:

- one artist-created unrelated layer;
- an effect on a managed footage layer where preservation is part of the revision claim;
- a mask where preservation is claimed;
- transform adjustments where preservation is claimed;
- parenting relationship where preservation is claimed;
- layer order adjustments where preservation is claimed.

Record a before-revision matrix of the exact properties being tested.

Do not claim preservation for a property that is not in the product contract.

## 10. Revision V002 / V003

### AE_REVISION_V002

1. select V002 through the actual revision workflow;
2. review compatibility result;
3. confirm when required;
4. apply the revision;
5. verify managed source replacement is correct;
6. verify historical footage provenance;
7. verify the artist-state preservation matrix;
8. run QC+;
9. capture evidence.

### AE_REVISION_V003

Repeat the same process with V003. The second revision must preserve the expected state again; V003 is not merely a duplicate-name package.

Any reproducible destructive change is a real S12 finding. Record it and use `FAIL_REPAIR_REQUIRED`; do not weaken the expectation to force a pass.

## 11. Save / close / reopen / reload

### AE_SAVE_CLOSE_REOPEN

1. Save the `.aep`.
2. Close the project/application as appropriate.
3. Reopen the saved project in the real host.
4. Reload/reopen CutBridge.
5. Run the relevant Build/QC discovery path again.
6. Confirm managed identity is rediscovered without duplication or unsafe adoption.
7. Confirm artist-state preservation remains intact.
8. Capture evidence.

A save-only test is not equivalent to this gate.

## 12. Unicode / path gate

### PATH_UNICODE

Exercise a legal path/metadata case containing Japanese or other Unicode characters appropriate to the target OS, for example a parent folder or project metadata segment.

Verify the same candidate can:

- Build the Blender package;
- render sequences;
- read `cutbridge.json` in AE;
- import sequences;
- Build/QC/revise as applicable.

Do not use path characters illegal on the target OS.

## 13. Evidence archive

### EVIDENCE_ARCHIVE

Store evidence references in a durable, reviewable location. Each PASS/FAIL gate in the JSON must have at least one evidence reference.

Recommended evidence set:

```text
s12-evidence/
├── evidence.json
├── environment.txt
├── checksums.txt
├── fixture/
│   └── fixture-info.txt
├── blender/
│   ├── install.png
│   ├── validate.png
│   ├── build-v001.png
│   └── render-notes.txt
├── packages/
│   ├── v001-manifest.json
│   ├── v002-manifest.json
│   └── v003-manifest.json
└── after-effects/
    ├── build-v001.png
    ├── qc-v001.png
    ├── revision-v002.png
    ├── revision-v003.png
    ├── reopen.png
    └── preservation-notes.txt
```

Repository commits should contain only evidence that is appropriate to store in Git. Large binary `.blend`, rendered sequences, or `.aep` files do not need to be committed merely to satisfy the gate; record stable locations/checksums instead.

## 14. Updating the evidence JSON

After each gate:

1. set that gate to `PASS` or `FAIL` only after actual execution;
2. add one or more real evidence references;
3. update environment/artifact/fixture fields as they become known;
4. use `IN_PROGRESS` while the campaign is incomplete;
5. run:

```powershell
python tools\s12\validate_evidence.py .\s12-evidence.json
```

The validator checks structure/completeness. It cannot inspect the truthfulness of screenshots or substitute for reviewer judgment.

## 15. Failure handling

If a required native gate fails:

1. set the gate to `FAIL`;
2. set overall state to `FAIL_REPAIR_REQUIRED`;
3. record exact host, artifact SHA, fixture SHA, steps, expected result, actual result, screenshot/log/reference;
4. open or update a focused defect record;
5. repair only the reproduced defect;
6. add automated regression coverage where feasible;
7. rebuild exact candidate artifacts if code changed;
8. rerun the affected native gate and any dependent gates.

S13 exists for real findings. Do not invent S13 work when S12 has no reproducible defect.

## 16. PASS decision

S12 may be marked PASS only when:

- real Blender host executed;
- real After Effects host executed;
- exact candidate artifact hashes are recorded;
- fixture provenance/hash is recorded;
- all required gates are PASS;
- every gate contains evidence references;
- evidence JSON validates structurally;
- a human review confirms the referenced evidence is credible and matches the exact candidate.

The validator may print:

```text
Record is structurally eligible for S12 PASS; review referenced native evidence manually.
```

That message means the record is complete enough for review. It is not independent proof that the desktop-host actions occurred.

## 17. Release boundary

Even S12 PASS does not publish v0.2.3.

Issue #18 repository governance, target-user evidence appropriate to the release claim, exact candidate freeze, deliberate `develop`→`main` promotion, exact release authorization, authorized publication, downloaded-asset verification, and production update/distribution verification remain separate gates in [RELEASE_READINESS.md](RELEASE_READINESS.md).
