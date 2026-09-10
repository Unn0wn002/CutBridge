# CutBridge Technical Debt

This file records known engineering/release debt that does not invalidate the current S1–S13 green `develop` baseline but should be resolved deliberately before it becomes a release or compatibility risk.

S12/S13 closeout reference points:

- PR #69 state-reconciliation merge: `fbfe83324808c9051e88e845d7ffe225bd56530f`;
- S13F runtime integration baseline: `0a86d9a0605e1dd9714ef35a547693de76f714f4`;
- product version: `0.2.3` unreleased;
- release authorization: `approved: false`;
- publication governance issue #18: OPEN.

## Priority A — Blender 6.0 compositor API migration

### Current evidence

The latest Blender 5.2.1 runtime suite passes **245 tests + 2 subtests** and currently emits **62 deprecation warnings**. The principal known source remains `Scene.use_nodes` usage in render-mapping state capture/rollback.

Blender reports that `Scene.use_nodes` is expected to be removed in Blender 6.0.

### Risk

CutBridge currently supports and tests Blender 5.2.1 successfully, so this is not a present Blender 5.2.1 failure. Leaving the deprecated API in the transactional mapping/rollback path may create a Blender 6.x compatibility failure or force a rushed migration later.

### Required work

- [ ] Inspect the actual Blender 6.x compositor API contract before editing.
- [ ] Replace deprecated `Scene.use_nodes` dependence with the supported equivalent while preserving transactional mapping semantics.
- [ ] Add regression coverage proving prior valid mapping and artist nodes survive failed replacement attempts.
- [ ] Run the existing Blender 5.2.1 suite to prevent backward regression.
- [ ] Add authoritative Blender 6.x runtime coverage only after an explicit compatibility-target decision.
- [ ] Do not claim Blender 6.x support merely because the warning disappears.

## Priority A — GitHub Actions runtime migration

### Current evidence

Current CI passes, but GitHub warns that pinned revisions of actions such as checkout/setup-node/setup-python target deprecated Node 20 action runtimes and are being forced to execute on Node 24.

### Risk

CutBridge intentionally pins release-sensitive actions for supply-chain/reproducibility safety. Relying indefinitely on GitHub's compatibility override weakens confidence that the pinned action/runtime combination will remain supported.

### Required work

- [ ] Identify current official action revisions that natively support the supported GitHub Actions runtime.
- [ ] Review upstream action release notes/security changes before changing pins.
- [ ] Update pins deliberately rather than switching to floating major tags.
- [ ] Verify `persist-credentials: false` and release-isolation assumptions remain intact.
- [ ] Run complete CI and release simulation after pin updates.
- [ ] Record exact new SHAs and validation evidence.

## Priority A — `main` / `develop` release-promotion reconciliation

### Current evidence

`main` is intentionally a conservative release-locked baseline while `develop` contains the completed S1–S13 product/validation work plus subsequent status reconciliation. The histories are materially diverged rather than a simple linear promotion state.

The `develop` release workflow is also newer and more strongly segmented than the older `main` workflow: validation, packaging, and publication are separated, authorization is revalidated, release-sensitive actions are pinned, and the downloaded bundle is rechecked before publication.

### Risk

A naive merge/cherry-pick strategy immediately before release could omit safety changes, restore the older release workflow, reintroduce stale files, or produce a `main` tree that differs materially from the validated `develop` candidate.

### Required work before RC promotion

- [ ] Freeze the exact release-candidate SHA on `develop` only after remaining prerequisite evidence is complete.
- [ ] Compare `main...candidate` file-by-file and classify every `main`-only change.
- [ ] Preserve required `main`-side release-lock intent deliberately.
- [ ] Preserve the hardened `develop` release workflow rather than reverting to the older `main` workflow.
- [ ] Produce an explicit promotion plan/tree whose contents are explainable.
- [ ] Verify the promoted `main` tree matches the intended candidate plus only documented release-governance differences.
- [ ] Require green authoritative CI on the exact promoted `main` SHA.
- [ ] Keep release authorization unapproved until all release gates are deliberately satisfied.

## Priority A — S12 structured evidence traceability

### Current evidence

S12 issue #58 was reconciled to PASS after the final S13F native repair. The exact native-tested source `9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95` was pushed, passed exact-head CI, passed PR #68 CI, was merged intact, and passed post-merge CI.

The repository nevertheless does **not** contain a final committed structured `s12-evidence.json` PASS record. It contains the S12 template and fail-closed validator only.

### Risk

The issue/PR/native evidence is sufficient to establish the recorded project history, but the missing structured artifact weakens auditability and makes it harder to independently reconstruct the original complete S12 evidence bundle later.

### Required work

- [ ] Search legitimate project storage/attachments for the authentic original structured S12 evidence record.
- [ ] If found, preserve the exact original hashes/evidence references and validate it with `tools/s12/validate_evidence.py`.
- [ ] If no authentic structured record exists, retain the limitation explicitly instead of manufacturing one retroactively.
- [ ] For future release-target campaigns, store the structured record and referenced evidence together under a durable evidence policy.

See `S12_S13_EVIDENCE_SUMMARY.md`.

## Priority B — Release governance / repository controls

Tracked primarily in issue #18.

Workflow-local authorization is defense-in-depth but cannot replace repository-level control of branches, tags, and historical-workflow publication.

Current private-repository plan/configuration does not provide the required ruleset capability. Do **not** make the source repository public merely to satisfy the checklist.

Required before RC/stable publication:

- branch protection/governance for `main` and `develop`;
- `v*` tag creation/update/deletion restriction or equivalent release-path control;
- protection against stale/historical commit workflow publication;
- explicit auditable authorization for exact main/tag/channel/prerelease;
- post-publication artifact checksum/content verification.

## Priority B — Japanese target-user evidence

S8 native UI validation and later real-host engineering validation passed, but UI correctness is not the same as representative target-user usability/productivity evidence.

S14 is the next bounded product/release-readiness phase.

Before broad claims about Japanese workflow productivity or ease of use:

- [ ] define the exact target-user tasks and acceptance criteria;
- [ ] recruit appropriate representative testers through a legitimate process;
- [ ] run the S14 task protocol;
- [ ] record completion, failure/rework points, terminology confusion, and qualitative feedback;
- [ ] separate anecdotal feedback from measured results;
- [ ] repair material findings and rerun affected tasks where needed;
- [ ] do not fabricate participant data or performance claims.

## Priority C — Documentation/state drift prevention

### Current evidence

Several state-bearing documents remained stuck at S11/S12-preparation language after S12/S13 had already completed. `tests/test_s11_docs.py` also encoded some of the obsolete “S12 is next” state, which meant a regression test was preserving historical status rather than current semantic invariants.

PR #69 reconciled README, completion status, release readiness, roadmap, S12 record, test plan, and the documentation regression test. Post-merge `develop` CI `34507502143` passed on `fbfe83324808c9051e88e845d7ffe225bd56530f`.

### Required prevention

- [ ] Treat `docs/COMPLETION_STATUS.md` as the canonical session-state page.
- [ ] Require integration PRs to update README, roadmap, completion status, changelog, Quick Starts, and Test Plan when their current-state wording changes.
- [ ] Keep exact native evidence in issues/PRs plus a bounded evidence summary rather than duplicating every transient candidate state everywhere.
- [ ] Test semantic invariants such as “publication blocked” and “current phase” without hard-coding brittle historical counts where possible.
- [ ] Avoid calling a historical runtime integration SHA “latest develop” after documentation-only reconciliation advances the branch.

## Priority C — Repository hygiene

Many historical feature/fix/validation branches remain after their work was integrated. They are not a runtime defect, but they increase repository navigation noise and can obscure the small number of active branches.

### Required work

- [ ] Identify branches already fully merged or retained only for historical validation evidence.
- [ ] Preserve any branch required by a SHA-bound evidence record until the evidence is safely indexed by commit SHA/PR.
- [ ] Delete only branches that are no longer operationally or evidentially required.
- [ ] Keep `main`, `develop`, and active bounded work branches clearly distinguishable.

## Non-debt / intentional boundaries

The following remain deliberate design boundaries, not defects:

- negative/preroll export ranges are rejected rather than silently renumbered;
- QC is diagnostic-only and does not automatically repair ownership;
- revision updates are source-oriented and fail closed on incompatible geometry/pass-set/package structure;
- Camera/3D Null handoff is bounded and is not arbitrary scene synchronization;
- private source control is separate from customer update distribution;
- release authorization defaults to false;
- Japanese is the primary UI language while English remains a deterministic fallback/support language.