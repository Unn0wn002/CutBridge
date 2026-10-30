# S14B fixture S14B-FX01 (2026-10-30)

**Fixture preparation and a scripted dry run only. No participant took part; S14B remains `NOT_EXECUTED`.** The dry run checks that the fixture works with the candidate. It is not usability evidence and is not a native acceptance row.

## Fixture identity

| Item | Value |
| --- | --- |
| Fixture ID | `S14B-FX01` |
| Provenance | `synthetic-original`: primitives, materials and animation made by `scripts/make_start_blend.py`; no third-party assets |
| Archive | `S14B-FX01-20261030.zip`, SHA-256 `7e5d5dc90b55c091f6edfb3038339eaff9c69bf991c17877d4f998f333477c7d` (`fixture-archive.sha256`) |
| Contents | 84 files, listed with SHA-256 in `fixture-MANIFEST.sha256` (the copy inside the archive is `MANIFEST.sha256`) |
| Stored | Outside the repository, on the owner's machine (`C:\Users\unn0w\Downloads\02_Projects\_s14b_fixture_20261030\fixture\`). Renders and `.blend` files are not committed (`AGENTS.md`). |

Archive layout:

- `participant/`: `S14B_FX01_start.blend`, `studio_preset_s14b_fx01.json`, `task_brief_JA.md`, and a copy of `docs/S14B_PARTICIPANT_GUIDE_JA.md`. The preset and brief are byte-identical to `participant/` in this folder.
- `moderator/revisions/`: V002 and V003 packages for JP09 and JP10.
- `moderator/reference/`: a V001 package built with the brief's values. Fallback only; handing it over is a moderator intervention.
- `moderator/sources/`: the `.blend` each package was built from. These contain absolute paths of the build machine.

The start scene deliberately does **not** match the brief (30 fps, 1920x1080, frames 1–250), so JP03 needs real configuration. Brief values: `S14B` / `EP01` / `SC001` / `C001` / `T01`, 24 fps, 960x540, frames 1–12, camera `CAM_MAIN`, custom preset `s14b-fx01` (BEAUTY required, LINE optional). V002 changes the body colour; V003 also moves the box.

## Candidate

The ZIPs were taken from the isolated CI run for `develop` `3e90b30` (`candidate-zips-source.txt`). Their hashes equal the recorded candidate (`candidate-zips.sha256`): Blender `abf5882d…`, AE `ecfb26ce…`.

## How it was built (owner host, Blender 5.2.2 LTS, not isolated)

1. Empty profile via `BLENDER_USER_RESOURCES` (`build/profile-before.txt`). Candidate installed with `extension install-file` (`build/install.txt`).
2. `scripts/make_start_blend.py` made the start scene without CutBridge loaded (`build/start-log.txt`).
3. `scripts/build_revision_package.py` ran once per version from the start scene. It checks that the 21 installed files (every ZIP entry except `LICENSE`) match the ZIP, applies the brief's values, runs Validate Cut, Build Package and a full render (`build/build_log_v00{1,2,3}.txt`, manifests `build/manifest-V00{1,2,3}.json`). All 75 package files still match the hashes in the build logs after the dry runs, which used copies.

Two earlier build attempts were discarded and are not in the fixture. In both, the LINE pass rendered blank: the empty factory scene's Freestyle line set had no line style. The script now assigns one, and the character no longer floats above the floor. The LINE frames in the fixture were checked by eye.

## Dry run (After Effects 26.5x89, owner host, not isolated)

The unmodified `CutBridge.jsx` from the AE ZIP was evaluated beside the harness. Its runtime file hashes are in `ae-dryrun/harness-SHA256.txt` and equal the candidate's. Buttons were pressed with `notify("onClick")`, and dialogs were answered by the harness. This was not a person. It worked on copies of the packages.

| Check | Result | Record |
| --- | --- | --- |
| V001 load, Build, QC+ | `C001_COMP` 960x540 @ 24 fps; QC+ PASS | `ae-dryrun/dryrun-log.json` |
| JP08 warning setup: one optional LINE frame renamed | QC+ `WARNING — 1 warning(s)`, `CBQ-SEQ-OPTIONAL-FRAMES-MISSING`, missing frame 6; PASS again after restore | `dryrun-log.json` steps 05–08 |
| Run A: artist solid (mask, Gaussian Blur, 50% opacity, parented to an artist null) and a comp marker; V002 then V003 | Both revisions applied after confirmation; artist state and marker unchanged; managed sources V002 then V003; QC+ PASS after each | `dryrun-state-*.json` |
| Run B: blur, mask and 40% opacity on the managed BEAUTY layer; managed LINE parented to an artist null; V002 then V003 | Both applied; all of it kept; QC+ PASS after each | `dryrun-log-B.json`, `dryrun-B-state-*.json` |
| JP04 setup in Blender (camera cleared on the configured V001 scene, UI language JA) | Validate Cut error `CAMERA_MISSING`: `アクティブカメラが設定されていません。`, fix `Scene Propertiesでアクティブカメラを設定してください。`; passes again with the camera restored | `build/jp04-check.txt` |

Notes:

- Run B started in the same After Effects process as run A, so the CutBridge globals were present and were cleared first (`dryrun-log-B.json`, first entry).
- The JP04 check ran on a scene whose V001 package already existed, so it also reported `PACKAGE_STATE_MISMATCH`. In a session JP04 comes before JP05, so that second error is not expected there.
- Launching After Effects with `-r` while it was not running started no process, twice (`ae-dryrun/launch.txt`). After Effects was then started normally and the scripts were sent to it. It was quit afterwards, leaving 0 `AfterFX` processes.
- Observation for the session, not a finding: the QC+ headline is bilingual for PASS (`合格 / PASS`) but English only for WARNING (`WARNING — 1 warning(s)`). The detail lines are bilingual. Watch whether participants notice this in JP08.

## Limits

- Scripted dry run on one host. It says nothing about how a person will understand the UI, which is what S14B measures.
- The participant will render V001 on their own machine. Render time was not measured (12 frames, BEAUTY and LINE, Cycles CPU at 16 samples, 960x540).
- Nothing was tagged, released or published.
