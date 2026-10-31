# S14B reviewer record sheet (v0.2.5, asynchronous) / レビュー記録シート

Blank form for the **owner**, filled after a participant's material comes back. Copy it **for each participant** into the campaign's dated evidence folder (for example `docs/evidence/v0.2.5/s14b-<YYYYMMDD>/JP-U01-review.md`) and fill in the copy. Never fill in this file itself. Rules: [S14B_SESSION_KIT_v0.2.5.md](S14B_SESSION_KIT_v0.2.5.md) and [S14_JP_USER_VALIDATION.md](S14_JP_USER_VALIDATION.md), section 13.

Participants fill in their own sheet ([S14B_PARTICIPANT_RECORD_JA.md](S14B_PARTICIPANT_RECORD_JA.md)); that original stays outside the repository. This sheet is what goes into the evidence folder.

Do not write names, email addresses, employers, studio names or account IDs anywhere in this sheet. / 氏名・メール・所属・アカウント ID は記入しないこと。

## Session

| Field | Value |
| --- | --- |
| Participant ID / 参加者 ID | `JP-U__` |
| Representative per protocol section 2 / 代表性 | yes / no (if no, this is not S14 evidence) |
| Experience band / 経験 | beginner-production / intermediate-production / advanced-production |
| Role category / 職種カテゴリ | |
| Date returned / 返送日 | |
| Consent covers / 同意範囲 | screen and voice / screen only / no recording; quotes yes/no; screenshots yes/no (consent reply stored outside the repository) |
| Recording received / 録画 | yes (screen and voice / screen only) / no — **no recording means this run is supplementary feedback, not campaign evidence** |
| Blender build and OS (from participant sheet) | |
| After Effects build and OS (from participant sheet) | |
| Blender ZIP hash (participant's check) | `abf5882d…` matches: yes / no |
| AE ZIP hash (participant's check) | `ecfb26ce…` matches: yes / no |
| Data archive | `S14B-FX02-data-20261031.zip` |
| Candidate source SHA | `efa64cd0aaa489495430090cdd8fe68648a28e5d` |
| Fallback V001 used / fallback 使用 | yes (from which task) / no |
| Any message sent during the session / 実施中の連絡 | none / exact text, recorded as intervention |

If either ZIP hash does not match, the session is `BLOCKED` and not bound to this candidate.

## Tasks

Outcome is `PASS`, `FAIL`, `BLOCKED` or `NOT_RUN`. Observed behaviour comes **only from the recording**; what the participant wrote or said is a statement. A task done with the fallback V001, or after any message from you, is not unassisted. Evidence is a recording timestamp, screenshot name or record-sheet section, always together with this sheet's file name (it stays after recordings are deleted).

- Paraphrase statements. Quote record-sheet text word for word only if the participant consented to quotes; never quote the voice track word for word.
- A task reported as done but not visible in the recording is `NOT_RUN`, with "done per record sheet, not in recording" as the statement.

Repeat this block for JP01–JP11:

### JP__ — 

| Field | Record |
| --- | --- |
| Observed behaviour (from recording, with timestamps) / 観察 | |
| Participant statement (record sheet, voice) / 発言・記述 | |
| Intervention (fallback used, or message sent) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

Task-specific checks:

- **JP02:** materially wrong safety interpretation?
- **JP03:** all brief values set, no validation bypass?
- **JP04:** did the Japanese `CAMERA_MISSING` message lead to the right fix (assign `CAM_MAIN`)?
- **JP05:** package version understood; would they overwrite the same version?
- **JP06 / JP09:** own package or fallback, and from which task?
- **JP07:** artist work added (layer, effect, mask, opacity, parenting)?
- **JP08:** clean result understood; for `JP08_qc_check`, the Build warning and the QC+ WARNING `CBQ-SEQ-OPTIONAL-FRAMES-MISSING` interpreted correctly; did they assume QC+ repairs the project?
- **JP09 / JP10:** confirmation message understood; resulting versions; artist state intact after V003?
- **JP11:** full quit and reopen; version and QC+ result after reopen; duplicate managed state?

### JP12 — Optional Camera/3D Null handoff

`NOT_APPLICABLE` for v0.2.5: 3D handoff is enabled only from Blender Python, not from a normal N-panel control (`docs/HANDOFF_3D.md`). In the JSON: `observed_behavior: "Not run: 3D handoff is outside the normal UI in v0.2.5"`, `evidence: ["docs/HANDOFF_3D.md", "S14B_SESSION_KIT_v0.2.5.md section 6"]`.

## Findings

One row per finding. Severity per protocol section 7; do not downgrade to keep a PASS.

| ID | Tasks | Severity (BLOCKER / MAJOR / MINOR / NOTE) | Description | Evidence | Status (OPEN / RESOLVED) |
| --- | --- | --- | --- | --- | --- |
| F-01 | | | | | OPEN |

## Closing answers / 最後の質問

Summarise the participant's written answers. Quote them word for word only if they consented to quotes.

1. Most confusing label or term:
2. Moment of doubt about correctness:
3. Missing or in the way for production use:
4. Other:

## Reviewer notes

Breaks or crashes visible in the recording, gaps in the recording, and anything else that could affect the result.
