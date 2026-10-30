# S14B session record sheet (v0.2.5) / セッション記録シート

Blank form. Copy it **for each participant** into the campaign's dated evidence folder (for example `docs/evidence/v0.2.5/s14b-<YYYYMMDD>/JP-U01-record.md`) and fill in the copy. Never fill in this file itself. Rules: [S14B_SESSION_KIT_v0.2.5.md](S14B_SESSION_KIT_v0.2.5.md) and [S14_JP_USER_VALIDATION.md](S14_JP_USER_VALIDATION.md).

Do not write names, email addresses, employers, studio names or account IDs anywhere in this sheet. / 氏名・メール・所属・アカウント ID は記入しないこと。

## Session

| Field | Value |
| --- | --- |
| Participant ID / 参加者 ID | `JP-U__` |
| Representative per protocol section 2 / 代表性 | yes / no (if no, this is not S14 evidence) |
| Experience band / 経験 | beginner-production / intermediate-production / advanced-production |
| Role category / 職種カテゴリ | |
| Date / 日付 | |
| Moderator / モデレーター | (role only) |
| Consent covers / 同意範囲 | recording / screenshots / quotes / none (stored outside the repository) |
| Blender build and OS | |
| After Effects build and OS | |
| Blender ZIP SHA-256 checked on this machine | `abf5882d…` matches: yes / no |
| AE ZIP SHA-256 checked on this machine | `ecfb26ce…` matches: yes / no |
| Clean state confirmed (how) | |
| Fixture ID and SHA-256 | |
| Candidate source SHA | `efa64cd0aaa489495430090cdd8fe68648a28e5d` |

If either ZIP hash does not match, stop here and record the session as `BLOCKED`.

## Tasks

Outcome is `PASS`, `FAIL` or `BLOCKED` (`NOT_RUN` if skipped). A task with any moderator intervention is not unassisted. Evidence is a timestamp, screenshot name or note ID.

### JP01 — Install and open Blender integration

| Field | Record |
| --- | --- |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP02 — Understand Japanese-first core UI

Check: metadata fields, Validate Cut, Build Package, Studio Preset mode, safety/status messages. Note any materially wrong safety interpretation.

| Field | Record |
| --- | --- |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP03 — Configure a representative cut

Check against the task brief: metadata, active camera, FPS, resolution, frame range, output location, preset. No validation bypass.

| Field | Record |
| --- | --- |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP04 — Recover from an intentional validation error

Setup done by moderator: active camera cleared (`CAMERA_MISSING`). Record whether the Japanese message led to the right fix.

| Field | Record |
| --- | --- |
| Setup confirmed / 準備確認 | yes / no |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP05 — Build deterministic package safely

Ask after the build: which version is this package, and what happens if you build the same version again?

| Field | Record |
| --- | --- |
| Package folder and version | |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP06 — Transfer/open package in After Effects

| Field | Record |
| --- | --- |
| Install route (Run Script File / ScriptUI Panels) | |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP07 — Build managed AE state

| Field | Record |
| --- | --- |
| Artist state added (layer, effect, mask, opacity, parenting) | |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP08 — Interpret QC+

Clean run first. Then the moderator's warning setup (optional-pass frame moved), and optionally the error setup (comp frame rate changed). Restore both before JP09.

| Field | Record |
| --- | --- |
| Clean result understood | yes / no |
| Warning setup and result | |
| Error setup and result (optional) | |
| Assumed QC+ repairs the project? | yes / no |
| Restored before JP09 | yes / no |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP09 — Apply V001 to V002 compatible revision

| Field | Record |
| --- | --- |
| Confirmation message understood | yes / no |
| Resulting version | |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP10 — Continue V002 to V003 and inspect preservation

| Field | Record |
| --- | --- |
| Resulting version | |
| Artist state intact (effect, mask, opacity, manual layer, parenting) | |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP11 — Save, close, reopen, reload

| Field | Record |
| --- | --- |
| No `AfterFX` process after quit | yes / no |
| Duplicate managed state after reopen | yes / no |
| Observed behaviour / 観察 | |
| Participant statement / 発言 | |
| Moderator intervention (exact words) / 介入 | none |
| Outcome / 結果 | |
| Unassisted / 介入なし | yes / no |
| Evidence / 証跡 | |
| Terminology confusion / 用語の混乱 | |

### JP12 — Optional Camera/3D Null handoff

`NOT_APPLICABLE` for v0.2.5: 3D handoff is enabled only from Blender Python, not from a normal N-panel control (`docs/HANDOFF_3D.md`).

## Findings

One row per finding. Severity per protocol section 7; do not downgrade to keep a PASS.

| ID | Tasks | Severity (BLOCKER / MAJOR / MINOR / NOTE) | Description | Evidence | Status (OPEN / RESOLVED) |
| --- | --- | --- | --- | --- | --- |
| F-01 | | | | | OPEN |

## Closing questions / 最後の質問

1. 一番わかりにくかった表示や用語 / Most confusing label or term:
2. 不安になった場面 / Moment of doubt about correctness:
3. 制作で使う上で足りない・邪魔なもの / Missing or in the way for production use:
4. その他 / Other:

## Moderator notes

Breaks, interruptions, environment problems, and anything that could affect the result.
