# S14B session kit for the v0.2.5 candidate (asynchronous)

Status: **Preparation only. S14B remains `NOT_EXECUTED`.** This kit records no participant result and grants no release, usability or compatibility claim.

The authoritative protocol is [S14_JP_USER_VALIDATION.md](S14_JP_USER_VALIDATION.md) (protocol version 1). Sessions run **asynchronously** under its section 13: no meeting, call or live observation. This kit binds the protocol to the current v0.2.5 candidate and gives the owner a ready order of work. Where this kit and the protocol disagree, the protocol wins.

Files:

| File | For | Language |
| --- | --- | --- |
| this page | the owner (runbook) | English |
| [S14B_CONSENT_FORM_JA.md](S14B_CONSENT_FORM_JA.md) | participant, before anything is sent | Japanese |
| [S14B_PARTICIPANT_GUIDE_JA.md](S14B_PARTICIPANT_GUIDE_JA.md) | participant, in the bundle | Japanese |
| [S14B_PARTICIPANT_RECORD_JA.md](S14B_PARTICIPANT_RECORD_JA.md) | participant fills it in and sends it back | Japanese |
| [S14B_SESSION_RECORD_v0.2.5.md](S14B_SESSION_RECORD_v0.2.5.md) | the owner, when reviewing what came back | Japanese/English |
| [S14B_CONSENT_FORM_EN.md](S14B_CONSENT_FORM_EN.md), [S14B_PARTICIPANT_GUIDE_EN.md](S14B_PARTICIPANT_GUIDE_EN.md), [S14B_PARTICIPANT_RECORD_EN.md](S14B_PARTICIPANT_RECORD_EN.md) | English practice and feedback testers only; never S14B evidence | English |

## 1. What one session can and cannot establish

- One participant moves the campaign to `IN_PROGRESS` at most. It can never produce S14B `PASS`.
- `PASS` needs at least **3 distinct representative participants** who all ran JP01–JP11 on the **same candidate SHA**, with no open BLOCKER or MAJOR finding (protocol section 9). The validator enforces the count and the SHA match.
- **Only participants who send a screen recording count.** Without one there is no observed behaviour (protocol section 13); the run is kept as supplementary feedback outside the campaign record.
- A friend or colleague who does not do animation, 3D, compositing or motion-graphics work is not a representative participant (protocol section 2). Their session can be a useful dry run, recorded as such outside the campaign.
- English-form testers are practice and feedback only. Keep their material outside the S14B evidence folder and use `EN-P01`-style IDs.
- A finding that needs a product change produces a new candidate. Affected tasks then rerun on that candidate (protocol section 10), and every native row bound to the current bytes must be judged again.

## 2. Candidate binding

| Item | Value |
| --- | --- |
| Source SHA (campaign `candidate.source_sha` and every `participants[].candidate_sha`) | `efa64cd0aaa489495430090cdd8fe68648a28e5d` |
| Blender artifact | `CutBridge-Blender-v0.2.5.zip`, SHA-256 `abf5882d56856d4662e95b2ac1335fb0dc6e818f5f7113235dce0529385b2207` |
| After Effects artifact | `CutBridge-AfterEffects-v0.2.5.zip`, SHA-256 `ecfb26ce8e5ad50638e17b35104efc2210d222b4ac8f10fccf0fba2748c17d8f` |
| Build evidence | `docs/evidence/v0.2.5/candidate-efa64cd-20261030/` |
| Product version in the campaign record | `0.2.5` |
| Protocol version | 1, with the section 13 asynchronous rule |

Later `develop` commits up to `3e90b30` change only files under `docs/` and the root `.gitattributes`; the isolated CI build of `3e90b30` produced the same two ZIP hashes. The participant checks both hashes on their own machine (guide step 0) and writes the result on their record sheet. A mismatch means the session is not bound to this candidate: it is `BLOCKED`.

## 3. The bundle (fixture S14B-FX02)

Send each participant the data archive plus three documents, so nothing else has to be sent during the session:

- **data archive** `S14B-FX02-data-20261031.zip`, SHA-256 `f79b4770a057258c472ff302b48fe7dd565a7c3b232cdf6463c948bae94284a2`: the two candidate ZIPs and the test material. It is the same for every participant and both languages, and it is what the campaign record's fixture block names.
- **documents**, with the placeholders filled in: the participant guide, the participant record sheet and (for reference) the consent form, in the participant's language. They are kept out of the data archive so that filling in your contact details does not change its hash.

How the archive was built and dry-run against the candidate: `docs/evidence/v0.2.5/s14b-fixture-fx02-20261031/README.md`. It is kept outside the repository (renders and `.blend` files are not committed).

| Path in the archive | Used in |
| --- | --- |
| `CutBridge-Blender-v0.2.5.zip`, `CutBridge-AfterEffects-v0.2.5.zip` | step 0 (hash check), JP01, JP06 |
| `S14B_FX01_start.blend`, `studio_preset_s14b_fx01.json`, `task_brief_JA.md` | JP03–JP05 and JP07 (the start scene's settings deliberately differ from the brief; English testers use the brief in their guide) |
| `S14B_FX01_JP04.blend` | JP04: brief values applied, active camera cleared; Validate Cut reports only `CAMERA_MISSING`. Must stay next to the preset file. |
| `JP08_qc_check/` | JP08: a V001 package with one optional LINE frame missing; Build warns and QC+ reports one WARNING (`CBQ-SEQ-OPTIONAL-FRAMES-MISSING`) |
| `revisions/` | JP09 (V002) and JP10 (V003) |
| `fallback/` | a V001 package built with the brief's values, for when the participant's own V001 cannot be used; using it counts as an intervention |

The revisions apply only to a V001 built with exactly the brief's values. A participant V001 with a different identity, FPS, range, resolution or preset is rejected at JP09; the guide tells the participant to note it and continue with the fallback V001.

## 4. Before sending a bundle

1. **Participant** fits the protocol section 2 profile; record only an experience band and a role category.
2. **Consent** is received in writing (the consent form's section 7 answers), before the bundle is sent. Store the reply outside the repository, together with anything that identifies the participant. Note whether they chose screen-and-voice, screen-only or no recording.
3. **Return folder:** create one private Google Drive folder per participant (named by their ID, e.g. `JP-U01`), shared with edit access **only** with that participant's email, and send its link with the bundle. Never share one folder between participants. Delete the folders on the consent form's dates. Participants without a Google account email a link to their own cloud storage instead. Contact for questions: nyxelharuka@gmail.com. Deletion dates are fixed in the consent form: contact details, sign-up answers and consent replies by 2027-01-10; record sheets, recordings and screenshots by 2027-03-31.
4. **Hosts** reported on the sign-up form: Blender 4.2 or newer and After Effects 2024–2026 with a working licence. Results do not extend to other versions.
5. **Campaign record**: copy `tools/s14/evidence-template.json` to a new dated evidence folder (for example `docs/evidence/v0.2.5/s14b-<YYYYMMDD>/s14-evidence.json`). Do not edit the committed template. In the copy set `candidate.product_version` to `0.2.5`, fill the candidate block from section 2 and the fixture block from section 3 (`S14B-FX02`, `synthetic-original`, the data archive hash).

## 5. Rules for the session (short form of protocol sections 5 and 13)

- Questions come by email. Answer questions about receiving the files or the hash check freely; they are not interventions. Answer questions about installing or using CutBridge only when the participant is stuck, as briefly as possible; keep the exact text and record it as an intervention on the reviewer sheet for the task it helped.
- Any extra file or instruction after the bundle is an intervention. So is the participant using `fallback/`.
- Results that rest only on the record sheet are participant statements, not observations.
- Statements are paraphrased in the evidence. Quote record-sheet text word for word only if the participant consented to quotes (consent item 4); never quote the voice track word for word.

## 6. Reviewing what comes back

1. Check the participant's record sheet: hash results, hosts, recording choice.
2. If there is a recording, watch it and fill one copy of [S14B_SESSION_RECORD_v0.2.5.md](S14B_SESSION_RECORD_v0.2.5.md) per participant in the dated evidence folder: observed behaviour from the recording, with timestamps; participant statements from the sheet and the voice track; interventions; outcome per task (`PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`); findings with protocol severities.
3. JP12 is `NOT_APPLICABLE` for v0.2.5: 3D handoff is enabled only from Blender Python (`docs/HANDOFF_3D.md`), not from a normal N-panel control.
4. A task the participant reports as done but that is not visible in the recording is `NOT_RUN`, noted "done per record sheet, not in recording".
5. Without a recording, do not enter the participant in `participants[]`. File their sheet as supplementary feedback; enter any findings in `findings[]` with the sheet as evidence.
6. A hash mismatch is not entered in the campaign record. Resend a verified bundle and treat the rerun as a new session.
7. Keep recordings, screenshots, record sheet originals and consent replies outside the repository. Delete them on the date promised in the consent form, which must fall after the campaign is closed. The filled reviewer sheet in the evidence folder is the retained record; cite it in every evidence reference.

## 7. After review

1. Copy the reviewer sheet's results into the campaign JSON: one `participants[]` entry with `participant_id` (`JP-U01`, `JP-U02`, …), `representative: true`, `experience_band`, `role_category`, `executed: true`, `candidate_sha`, `blender_host` and `after_effects_host` (`{version, os}` from the record sheet), and all twelve tasks; plus one `findings[]` entry per finding.
   - Each task is `{id, status, observed_behavior, participant_statement, moderator_intervention, unassisted, evidence: [...]}`. Write the section 13 intervention (fallback use, any message sent) under the key `moderator_intervention`: that is the key the validator checks against `unassisted`.
   - JP12: `status: "NOT_APPLICABLE"`, `observed_behavior: "Not run: 3D handoff is outside the normal UI in v0.2.5"`, `evidence: ["docs/HANDOFF_3D.md", "S14B_SESSION_KIT_v0.2.5.md section 6"]`. The validator requires both fields for any status other than `NOT_RUN`.
   - The campaign-level `candidate.blender_host` and `candidate.after_effects_host` required for PASS: record "per participant, see participants[]" in the version field and list the hosts in the README.
2. Set `overall_state` to `IN_PROGRESS`, or `FAIL_REPAIR_REQUIRED` if any task failed or was blocked, or an open BLOCKER or MAJOR finding exists.
3. Run the validator in the offline Windows Sandbox, not in the owner's credentialed context (`AGENTS.md`):

   ```text
   python tools/s14/validate_evidence.py docs/evidence/v0.2.5/s14b-<YYYYMMDD>/s14-evidence.json
   ```

   Keep its output in the evidence folder.
4. Write a short README in the same folder: candidate binding, asynchronous execution, hosts, what ran, what did not, and the limits. Put the asynchronous execution note in `summary.limitations` as well.
5. Do not edit `docs/S14_JP_USER_VALIDATION.md`, release readiness pages or `release-authorization.json` to claim progress. Change the S14B status there only in a separate reviewed change once the campaign state actually changes.

## 8. Limits

- This kit is not evidence. No participant has run it.
- Asynchronous sessions see less than a moderated one: without voice, the reasons behind a participant's actions rest on what they wrote.
- S14 `PASS`, if it is ever reached, covers only the recorded task scope and hosts. It does not authorize release, tagging or publication (protocol section 12).
