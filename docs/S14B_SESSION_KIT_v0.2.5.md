# S14B session kit for the v0.2.5 candidate

Status: **Preparation only. S14B remains `NOT_EXECUTED`.** This kit records no participant result and grants no release, usability or compatibility claim.

The authoritative protocol is [S14_JP_USER_VALIDATION.md](S14_JP_USER_VALIDATION.md) (protocol version 1). This kit only binds that protocol to the current v0.2.5 candidate and gives the moderator a ready order of work. Where this kit and the protocol disagree, the protocol wins.

Files:

- this page: moderator runbook (English);
- [S14B_PARTICIPANT_GUIDE_JA.md](S14B_PARTICIPANT_GUIDE_JA.md): what the participant reads (Japanese);
- [S14B_SESSION_RECORD_v0.2.5.md](S14B_SESSION_RECORD_v0.2.5.md): one record sheet per participant (Japanese/English).

## 1. What one session can and cannot establish

- One participant moves the campaign to `IN_PROGRESS` at most. It can never produce S14B `PASS`.
- `PASS` needs at least **3 distinct representative participants** who all ran JP01–JP11 on the **same candidate SHA**, with no open BLOCKER or MAJOR finding (protocol section 9). The validator enforces the count and the SHA match.
- A friend or colleague who does not do animation, 3D, compositing or motion-graphics work is not a representative participant (protocol section 2). Do not record such a session as S14 evidence; it can still be a useful dry run, recorded as such outside the campaign.
- A finding that needs a product change produces a new candidate. Affected tasks then rerun on that candidate (protocol section 10), and every native row bound to the current bytes must be judged again.

## 2. Candidate binding

| Item | Value |
| --- | --- |
| Source SHA (campaign `candidate.source_sha` and every `participants[].candidate_sha`) | `efa64cd0aaa489495430090cdd8fe68648a28e5d` |
| Blender artifact | `CutBridge-Blender-v0.2.5.zip`, SHA-256 `abf5882d56856d4662e95b2ac1335fb0dc6e818f5f7113235dce0529385b2207` |
| After Effects artifact | `CutBridge-AfterEffects-v0.2.5.zip`, SHA-256 `ecfb26ce8e5ad50638e17b35104efc2210d222b4ac8f10fccf0fba2748c17d8f` |
| Build evidence | `docs/evidence/v0.2.5/candidate-efa64cd-20261030/` |
| Product version in the campaign record | `0.2.5` |
| Protocol version | 1 |

Later `develop` commits up to `3e90b30` change only files under `docs/` and the root `.gitattributes`; the isolated CI build of `3e90b30` produced the same two ZIP hashes. If a participant is given ZIPs with any other hash, the session is not bound to this candidate. Stop and record it as `BLOCKED`.

Before handing the ZIPs over, check both hashes on the participant's machine:

```powershell
Get-FileHash -Algorithm SHA256 CutBridge-Blender-v0.2.5.zip, CutBridge-AfterEffects-v0.2.5.zip, S14B-FX01-20261030.zip
```

## 3. Prerequisites (all must be true before the session starts)

1. **Participant** fits the protocol section 2 profile; record only an experience band and a role category.
2. **Consent** for any screen recording, screenshot or quote is obtained and stored **outside the repository**, together with anything that identifies the participant.
3. **Hosts**: Blender 4.2 or newer (5.2.x LTS is the automated target) and After Effects 2024–2026 with a working licence on the participant's machine. Record the exact builds and the OS. Results do not extend to other versions.
4. **Clean state**: CutBridge is not already enabled in Blender, and no CutBridge files exist in the After Effects `Scripts/ScriptUI Panels` folder. Record how this was confirmed.
5. **Fixture** S14B-FX01 (section 4) is on the participant's machine and its archive SHA-256 matches.
6. **Disposable folders**: an empty output folder for packages and a disposable folder for the After Effects project. Never point CutBridge at production data.
7. **Campaign record**: copy `tools/s14/evidence-template.json` to a new dated evidence folder (for example `docs/evidence/v0.2.5/s14b-<YYYYMMDD>/s14-evidence.json`). Do not edit the committed template. In the copy set `candidate.product_version` to `0.2.5` and fill the candidate block from section 2.

## 4. Fixture requirements

Use fixture **S14B-FX01** for every participant in the campaign: `S14B-FX01-20261030.zip`, SHA-256 `7e5d5dc90b55c091f6edfb3038339eaff9c69bf991c17877d4f998f333477c7d`, provenance `synthetic-original`. How it was built and dry-run against the candidate: `docs/evidence/v0.2.5/s14b-fixture-20261030/README.md`. The archive is kept outside the repository; check its hash before each session.

- `participant/`: the start `.blend` (its settings deliberately differ from the brief), the custom preset (`BEAUTY` required, `LINE` optional) and the Japanese task brief `task_brief_JA.md`. The brief gives values only, no UI steps, and asks for the JP07 artist work (a layer, an effect, a mask, an opacity change, a parenting link).
- `moderator/revisions/`: the V002 and V003 packages. Hand over V002 at JP09 and V003 at JP10, not earlier.
- `moderator/reference/`: a V001 package built with the brief's values, for when the participant's own V001 cannot be used. Handing it over is a moderator intervention.

The revisions apply only to a V001 built with exactly the brief's values. A participant V001 with a different identity, FPS, range, resolution or preset is rejected at JP09; record what happened, then decide whether to continue with the reference V001.

Record the fixture ID, provenance and archive SHA-256 in the campaign record.

## 5. Controlled scenarios the moderator sets up

These are protocol-required and must be set up **without the participant watching how**:

- **JP04, validation error**: before the task, clear the active scene camera (Scene Properties, Camera field empty). The expected Japanese message is `アクティブカメラが設定されていません。` with the remediation `Scene Propertiesでアクティブカメラを設定してください。` (`CAMERA_MISSING`). Record whether the message leads the participant to the right fix.
- **JP08, QC+ warning**: after a clean QC+ run, rename or move one frame inside the **optional** pass folder (`CBQ-SEQ-OPTIONAL-FRAMES-MISSING`, severity WARNING).
- **JP08, QC+ error** (if time allows): change the managed comp's frame rate in Composition Settings (`CBQ-COMP-DRIFT-…`, severity ERROR).
- Restore both JP08 changes before JP09, and record that you did. QC+ does not repair anything; a participant who expects it to is a finding.

## 6. Session order and timing

Plan 90–120 minutes. Breaks are allowed; record where they happened.

1. (5 min) Read the participant guide's opening section together. Confirm consent. Start recording only if consent covers it.
2. (5 min) Hash check of both ZIPs (section 2).
3. JP01–JP05 in Blender, JP06–JP11 in After Effects, in protocol order.
4. JP12 is recorded as `NOT_APPLICABLE` for v0.2.5: 3D handoff is still enabled only from Blender Python (`docs/HANDOFF_3D.md`), not from a normal N-panel control, so it is outside the normal user-facing workflow (protocol section 6, JP12).
5. (10 min) Closing questions from the record sheet. Stop recording.

## 7. Moderation rules (short form of protocol section 5)

- Explain the goal of each task; do not explain the UI.
- If the participant is stuck, wait. If you must help, say as little as possible and write down exactly what you said. A task with help cannot be recorded as unassisted PASS.
- For every task record separately: observed behaviour, what the participant said, your intervention, outcome (`PASS` / `FAIL` / `BLOCKED`), evidence reference (timestamp, screenshot name or note ID).
- Record terminology confusion even when the task succeeds.
- Assign each finding one severity (BLOCKER / MAJOR / MINOR / NOTE). Do not downgrade a finding to keep a PASS.

## 8. After the session

1. Copy the record sheet's results into the campaign JSON: one `participants[]` entry with `participant_id` (`JP-U01`, `JP-U02`, …), `representative: true`, `experience_band`, `role_category`, `executed: true`, `candidate_sha`, and all twelve tasks; plus one `findings[]` entry per finding.
2. Set `overall_state` to `IN_PROGRESS`, or `FAIL_REPAIR_REQUIRED` if any task failed or was blocked, or an open BLOCKER or MAJOR finding exists.
3. Run the validator in the offline Windows Sandbox, not in the owner's credentialed context (`AGENTS.md`):

   ```text
   python tools/s14/validate_evidence.py docs/evidence/v0.2.5/s14b-<YYYYMMDD>/s14-evidence.json
   ```

   Keep its output in the evidence folder.
4. Write a short README in the same folder: candidate binding, hosts, what ran, what did not, and the limits. Store recordings, consent and anything identifying outside the repository.
5. Do not edit `docs/S14_JP_USER_VALIDATION.md`, release readiness pages or `release-authorization.json` to claim progress. Change the S14B status there only in a separate reviewed change once the campaign state actually changes.

## 9. Limits

- This kit is not evidence. No participant has run it.
- S14 `PASS`, if it is ever reached, covers only the recorded task scope and hosts. It does not authorize release, tagging or publication (protocol section 12).
