# CutBridge S14 — Japanese Target-User Validation Protocol

Status: **PROTOCOL PREPARATION / NO TARGET-USER PASS CLAIM YET**

Tracking issue: #71.

This protocol defines the bounded Japanese target-user validation required before CutBridge makes broad production-usability claims for v0.2.3. It is intentionally separate from S12/S13 native-host engineering evidence.

A green CI run, Japanese-localized UI, native AE validation, or completion of this document does **not** count as target-user validation.

## 1. Starting baseline

Protocol preparation starts from post-S13 closeout `develop`:

`e50eff3ce92b61781cd10949b5fa1ff195ffb8e3`

The SHA-bound S13F native/runtime baseline remains:

`0a86d9a0605e1dd9714ef35a547693de76f714f4`

Final native-tested S13F source:

`9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95`

v0.2.3 remains unreleased. `release-authorization.json` must remain `approved: false` throughout S14 preparation and user testing.

## 2. Target participant profile

S14 targets Japanese-speaking users who are reasonably representative of the intended CutBridge audience:

- animation, 3D, compositing, motion-graphics, or adjacent content-production work;
- practical Blender and/or After Effects familiarity appropriate to the tasks assigned;
- able to read the Japanese product UI naturally enough to judge terminology and instructions.

Do not present friends or unrelated testers as representative production users merely to fill a participant count. Record experience bands rather than unnecessary personal details.

Suggested non-identifying experience bands:

- `beginner-production`: some real project exposure but limited pipeline experience;
- `intermediate-production`: regularly completes Blender/AE production tasks;
- `advanced-production`: experienced pipeline/power user or technical artist/editor.

S14 PASS requires evidence from at least **3 distinct representative participants**. This is an internal minimum evidence threshold, not a claim of statistical representativeness. Broader claims may require more evidence.

## 3. Privacy and evidence rules

Use pseudonymous participant IDs such as `JP-U01`. Do not store names, emails, employer/studio names, account identifiers, private project names, or unrelated personal information in the product repository.

Use only synthetic-original or authorized user-owned test assets. Do not use leaked or unauthorized studio files.

If screenshots, screen recordings, or direct quotes are retained, obtain appropriate participant consent and store sensitive/raw material outside the product repository unless explicit repository storage is appropriate and authorized.

The repository evidence record should contain only the minimum evidence references required to audit the result.

## 4. Frozen candidate rule

Every S14 execution record must identify:

- exact CutBridge source SHA;
- Blender artifact filename + SHA-256;
- After Effects artifact filename + SHA-256;
- Blender version + OS;
- After Effects version + OS;
- fixture ID/provenance + SHA-256;
- protocol version.

If product source changes materially after a participant run, determine which tasks are affected. Do not silently transfer evidence to the changed candidate. Rerun affected tasks or explicitly mark the older evidence as superseded.

Documentation-only changes may be judged separately when they do not alter the tested user workflow, but the decision must be recorded rather than assumed.

## 5. Moderation rules

The moderator may explain the test setup and task goal but should not coach the user through the product unless the task specifically tests assisted recovery.

For every task distinguish:

- **Observed behavior** — what the participant actually did;
- **Participant statement** — what the participant said or reported;
- **Moderator intervention** — any help given;
- **Outcome** — PASS / FAIL / BLOCKED;
- **Evidence reference** — note, screenshot, timestamp, or other retained artifact.

Do not convert moderator assistance into an unassisted PASS.

## 6. Task matrix

### JP01 — Install and open Blender integration

Goal: install/enable the candidate and locate the CutBridge panel.

PASS when the participant can enable CutBridge and reach the panel without unsafe workaround or moderator step-by-step coaching.

Observe installation terminology, first-run understanding, panel discoverability, and any version/permission confusion.

### JP02 — Understand Japanese-first core UI

Goal: identify the purpose of Project/Episode/Scene/Cut/Take/Version fields, Validate Cut, Build Package, Studio Preset mode, and the main safety/status messages.

PASS when the participant can correctly explain or use the core controls without materially incorrect safety interpretation.

Terminology confusion should be recorded even if the participant eventually succeeds.

### JP03 — Configure a representative cut

Goal: set metadata, active camera, FPS, resolution, frame range, output location, and an assigned preset mode.

PASS when configuration matches the supplied task brief and does not require bypassing validation.

### JP04 — Recover from an intentional validation error

Goal: present one controlled, non-destructive setup error such as missing active camera or required metadata.

PASS when the participant can interpret the Japanese validation message, identify the corrective action, repair the setup, and rerun validation successfully.

A message that technically reports an error but leads users toward the wrong action is a material finding.

### JP05 — Build deterministic package safely

Goal: Build Package after validation and inspect the resulting package identity/structure.

PASS when the correct package is created and the participant understands the version/package identity well enough not to overwrite protected same-version payload.

### JP06 — Transfer/open package in After Effects

Goal: locate the correct `cutbridge.json`, open the AE integration, and load the package.

PASS when the participant reaches a validated loaded-package state without selecting an unsafe/incorrect package path.

### JP07 — Build managed AE state

Goal: execute Build and identify the resulting CutBridge-managed project/comp/layers.

PASS when Build completes for the valid fixture and the participant can distinguish managed output from unrelated artist objects at the level needed for normal operation.

### JP08 — Interpret QC+

Goal: run QC+ and interpret at least one clean result plus one controlled warning/error scenario supplied by the protocol fixture or moderator.

PASS when the participant correctly understands severity and the remediation direction without assuming QC automatically repairs the project.

### JP09 — Apply V001→V002 compatible revision

Goal: apply the provided compatible revision package while preserving supplied artist state.

PASS when the participant follows the intended revision flow, understands compatibility/confirmation messaging, completes the revision, and verifies the new managed source/version state.

### JP10 — Continue V002→V003 and inspect preservation

Goal: exercise chained revision behavior rather than a single update.

PASS when the participant completes V003 and can confirm the expected managed version while the supplied artist-owned effect/mask/opacity/manual-layer/parenting state remains intact for the fixture.

### JP11 — Save, close, reopen, reload

Goal: save the project, fully close AE, reopen, reload CutBridge, and return to a coherent QC/managed-state workflow.

PASS when the participant can re-establish the workflow without duplicate managed state or manual reconstruction.

### JP12 — Optional Camera/3D Null handoff

This task is required only if the intended v0.2.3 release-facing user workflow explicitly claims this feature as a normal user-facing capability.

Goal: use a prepared supported `handoff_3d` fixture and understand the bounded Camera/3D Null result.

PASS when the participant can identify the reconstructed managed Camera/Null context and does not infer unsupported geometry/light/bone/general-scene synchronization.

If the feature remains engineering opt-in rather than normal user-facing release scope, record JP12 as `NOT_APPLICABLE` with rationale rather than forcing it into the usability claim.

## 7. Finding severity

Every material finding must use one severity:

- **BLOCKER** — core claimed workflow cannot be completed safely, data/work is at credible risk, or the UI directs the user toward materially unsafe behavior;
- **MAJOR** — workflow can eventually complete but substantial confusion/rework or incorrect safety interpretation undermines the intended production claim;
- **MINOR** — localized wording/layout/friction issue without material workflow or safety risk;
- **NOTE** — preference or observation that does not justify a product change by itself.

Do not downgrade a finding merely to reach PASS.

## 8. S14 campaign verdicts

Allowed campaign states:

- `NOT_EXECUTED` — no real participant run has started;
- `IN_PROGRESS` — at least one real participant/task has been executed but the campaign is incomplete;
- `FAIL_REPAIR_REQUIRED` — one or more unresolved BLOCKER/MAJOR findings invalidate the intended usability claim or a required task fails materially;
- `PASS` — all acceptance conditions below are satisfied.

## 9. PASS acceptance conditions

S14 may be marked PASS only when all are true:

1. at least 3 distinct representative participants completed the required protocol on attributable candidate builds;
2. required tasks JP01–JP11 have PASS results for every participant, unless a documented protocol exception is explicitly justified before the run;
3. JP12 is either PASS for every applicable participant or explicitly `NOT_APPLICABLE` because the feature is outside the normal release-facing workflow claim;
4. no unresolved BLOCKER finding exists;
5. no unresolved MAJOR finding contradicts the intended Japanese production-usability claim;
6. material repairs were rerun on affected tasks using an attributable repaired candidate;
7. evidence references exist for every executed task and material finding;
8. the campaign summary separates observations from participant statements and moderator interventions;
9. no participant identities or measurements were fabricated;
10. the S14 evidence validator accepts the final structured record.

A PASS result means only that the documented S14 task scope passed under the recorded conditions. It is not a universal usability or compatibility certification.

## 10. Repair and rerun rules

When a BLOCKER or MAJOR finding produces a product change:

1. create a bounded issue/repair branch from the current validated baseline;
2. add regression coverage where technically applicable;
3. require candidate/PR/post-merge CI;
4. identify which S14 tasks the change invalidates;
5. rerun those tasks with the affected participant cohort or an explicitly justified equivalent cohort;
6. keep prior failed evidence rather than rewriting history.

MINOR changes may be batched if they do not alter safety behavior, but the final evidence record must still identify the tested candidate(s).

## 11. Evidence files

S14A provides:

- `tools/s14/evidence-template.json` — fail-closed starting structure;
- `tools/s14/validate_evidence.py` — structural/acceptance validator;
- `tests/test_s14_evidence.py` — validator regression coverage.

Copy the template for a real campaign. Do not edit the committed template into a fake PASS example.

## 12. Release boundary

S14 PASS still does not authorize publication.

Before RC/stable publication, CutBridge still requires:

- repository governance #18;
- deliberate `develop`→`main` promotion;
- authoritative CI on the exact promoted `main` tree;
- exact release authorization tuple;
- intended tag-triggered publication;
- independent downloaded-asset verification;
- production update/distribution verification.

Keep `main`, tags, GitHub Releases, and `release-authorization.json` untouched during S14 protocol preparation.