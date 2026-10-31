# S14B fixture S14B-FX02 (2026-10-31, asynchronous sessions)

**Fixture preparation and scripted dry runs only. No participant took part; S14B remains `NOT_EXECUTED`.** The dry runs check that the fixture works with the candidate. They are not usability evidence and not native acceptance rows.

S14B-FX02 repackages S14B-FX01 (`docs/evidence/v0.2.5/s14b-fixture-20261030/`) for asynchronous sessions under protocol section 13. Without a moderator, the JP04 and JP08 problem setups ship as prepared files, and the V002/V003 and fallback V001 packages ship with everything else. FX01's files are reused byte for byte, except the task brief.

## Fixture identity

| Item | Value |
| --- | --- |
| Fixture ID | `S14B-FX02` |
| Provenance | `synthetic-original` (FX01's scene, made by `docs/evidence/v0.2.5/s14b-fixture-20261030/scripts/make_start_blend.py`) |
| Archive | `S14B-FX02-data-20261031.zip`, SHA-256 `f79b4770a057258c472ff302b48fe7dd565a7c3b232cdf6463c948bae94284a2` (`fixture-archive.sha256`) |
| Contents | 105 files plus `MANIFEST.sha256`, listed with SHA-256 in `fixture-MANIFEST.sha256` |
| Stored | Outside the repository (`C:\Users\unn0w\Downloads\02_Projects\_s14b_fx02_20261031\fixture\`). Renders, `.blend` files and ZIPs are not committed (`AGENTS.md`). |

The archive holds data only. The participant guide, record sheet and consent form are sent alongside it with the owner's contact details filled in, so the archive hash does not change when those are filled.

| Path | Source | Used in |
| --- | --- | --- |
| `CutBridge-Blender-v0.2.5.zip`, `CutBridge-AfterEffects-v0.2.5.zip` | candidate ZIPs, `abf5882d…` / `ecfb26ce…` (FX01 `candidate-zips.sha256`) | step 0, JP01, JP06 |
| `S14B_FX01_start.blend`, `studio_preset_s14b_fx01.json` | FX01 `participant/`, unchanged | JP03–JP05 |
| `task_brief_JA.md` | `participant/task_brief_JA.md` here: FX01's brief with the output folder no longer "prepared by the moderator", and a note that the FX01 file names are expected | JP03–JP05, JP07 |
| `S14B_FX01_JP04.blend` | new, `scripts/make_jp04_blend.py` | JP04 |
| `JP08_qc_check/` | new: FX01's reference V001 with `render/line/C001_LINE_0006.png` removed (`build/jp08-make.txt`) | JP08 |
| `revisions/` | FX01 `moderator/revisions/`, unchanged | JP09, JP10 |
| `fallback/` | FX01 `moderator/reference/`, unchanged | only if the participant's own V001 cannot be used |

`build/packed-vs-tested.txt` confirms the packed JP04 file and JP08 package are the same bytes that were dry-run, and that `revisions/` and `fallback/` equal FX01's.

## JP04 file (Blender 5.2.2 LTS, owner host, not isolated)

The installed candidate in the empty FX01 profile still matched the ZIP: 21/21 files (`build/installed-vs-zip.txt`). `make_jp04_blend.py` opened FX01's start scene and applied the brief's values. It set the output folder and preset path relative to the `.blend` (`//`), set the UI language to JA, cleared the active camera and saved (`build/jp04-make-log.txt`).

`check_jp04_file.py` then opened a copy placed in a different folder next to the preset (`build/jp04-check.txt`):

- Validate Cut: **one error only**, `CAMERA_MISSING`, `アクティブカメラが設定されていません。`, fix `Scene Propertiesでアクティブカメラを設定してください。`
- After assigning `CAM_MAIN`: `検証に合格しました。`

The relative paths mean the file validates the same way wherever the participant extracts the archive, as long as it stays next to the preset file. It still contains the build machine's absolute save path in Blender's file header.

## JP08 package (After Effects 26.5x89, owner host, not isolated)

`scripts/FX02_jp08_dryrun.jsx` evaluated the unmodified `CutBridge.jsx` from the AE ZIP; its runtime file hashes equal the candidate's (`ae-dryrun/harness-SHA256.txt`). It ran in a new project, pressed the panel buttons with `notify("onClick")` and answered dialogs itself. This was not a person. Single pass (`ae-dryrun/jp08-dryrun-log.json`):

| Step | Result |
| --- | --- |
| Load and Build | `C001_COMP` 960x540 @ 24 fps, with the alert `警告: - LINE: optional pass skipped — missing frame(s): 6` |
| QC+ | `WARNING — 1 warning(s)`: `CBQ-SEQ-OPTIONAL-FRAMES-MISSING`, LINE, missing frame 6, with the bilingual remediation |

After Effects was started normally, the script sent with `-r`, and After Effects quit afterwards, leaving 0 `AfterFX` processes (`ae-dryrun/ae-launch.txt`).

Observations for the sessions, not findings: the Build alert's warning line (`optional pass skipped — missing frame(s)`) is English only, and so is the QC+ WARNING headline. The detail lines are bilingual.

## Not re-run

The V001 → V002 → V003 revision chain with artist work was dry-run on FX01's packages (`docs/evidence/v0.2.5/s14b-fixture-20261030/ae-dryrun/`). The same bytes are used here, so it was not repeated.

## Limits

- Scripted dry runs on one host. They say nothing about how a person will understand the UI, which is what S14B measures.
- Nothing was tagged, released or published.
