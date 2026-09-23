# CutBridge Technical Debt

This file records known engineering/release debt that does not invalidate the current S1–S13 validated product baseline or the protected promotion to `main`, but should be resolved deliberately before it becomes a release or compatibility risk.

S12/S13 closeout reference points:

- PR #69 state-reconciliation merge: `fbfe83324808c9051e88e845d7ffe225bd56530f`;
- S13F runtime integration baseline: `0a86d9a0605e1dd9714ef35a547693de76f714f4`;
- stable v0.2.3: released and immutable at main/tag SHA `1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f`;
- stable v0.2.4: published and independently verified on GitHub at main/tag SHA `a393e409d19445c4090460b7e7b4716779161fa4`;
- active development: `0.2.5`; Issue #99 source remediation included; release authorization is `approved: false`;
- production distribution: intentionally remains on v0.2.3 until a corrected post-v0.2.4 release is published and verified;
- publication governance issue #18: CLOSED / COMPLETED; Issue #99 is the separate release-hygiene/distribution hold.

## Priority A — Blender 6.0 compositor API migration

### Current evidence

The latest exact-head Blender 5.2.1 runtime suite on the v0.2.4 integration baseline passes **307 tests + 2 subtests** and emits **72 deprecation warnings**. The principal known source remains `Scene.use_nodes` usage in render-mapping state capture/rollback.

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

## RESOLVED — `main` / `develop` release-promotion reconciliation

### Verified result

The promotion risk was resolved deliberately rather than by blind merge:

- exact protected `develop` promotion head: `501f9bd6b6c69cf8859f96f0fd6441afc48c0b50`;
- fresh pre-promotion PR CI `35511056270` attempt 2: PASS;
- PR #74 merged through protected `main`;
- promoted `main` merge commit: `049081f0fe3d3e74d77db807910c2e0fff56fe73`;
- post-promotion `main` CI `35513361337`: PASS;
- `main` is one merge commit ahead of `develop` with zero file differences;
- the hardened release workflow and fail-closed authorization controls are present on `main`;
- `release-authorization.json` remained unapproved throughout promotion.

This item is no longer release-promotion debt. Future changes should continue through protected `develop` and deliberate PR promotion to protected `main`.

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

Repository-level configuration is now present on the public repository:

- protected `main` via `Protect main`;
- protected `develop` via `Protect develop`;
- admin-controlled `v*.*.*` tag mutation via `Protect release tags`;
- independent no-bypass required check `release-tag-eligibility` via `Require release tag eligibility`;
- exact current-main/tag/channel/prerelease authorization remains fail-closed.

The v0.2.3 governance path is complete:

- unauthorized-current-main and stale/historical tag attempts were rejected;
- the explicitly authorized exact-current-main eligibility path passed;
- the v0.2.3 GitHub Release and downloaded artifacts were independently verified;
- production D1 is deployed separately at `Unn0wn002/cutbridge-distribution` commit `635c1384af2649d4ce49705cce41f98826a861cc`.

Issue #18 is closed as completed after the authorized v0.2.4 exact-current-main tag/publication path and independent asset verification passed. Issue #99 remains open because the immutable published v0.2.4 AE ZIP contains stale release-state wording; its source fix is carried by active v0.2.5 development. Subsequent releases must repeat exact-candidate authorization, protected tag creation, independent asset verification, and additive distribution publication.

## Priority B — Japanese target-user evidence

S8 native UI validation and later real-host engineering validation passed, but UI correctness is not the same as representative target-user usability/productivity evidence.

For v0.2.3, the release-facing Japanese claim was deliberately narrowed. S14A is complete and S14B remains NOT_EXECUTED; representative-user evidence is therefore deferred unless a future release intends broader usability/productivity claims.

Before any future broad claims about Japanese workflow productivity or ease of use:

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
- source-repository hosting is separate from customer update distribution; repository visibility does not turn GitHub source hosting into the production update endpoint;
- release authorization defaults to false;
- Japanese is the primary UI language while English remains a deterministic fallback/support language.
