# CutBridge Technical Debt

This file records known engineering debt that does not currently invalidate the green S8-integrated product baseline but should be resolved deliberately before it becomes a release or compatibility risk.

## Priority A — Blender 6.0 compositor API migration

### Current evidence

The post-S8 Blender 5.2.1 runtime suite passes **179 tests + 2 subtests**, but currently emits **61 deprecation warnings** associated primarily with `Scene.use_nodes` usage in render-mapping state capture/rollback.

Blender reports that this behavior is expected to be removed in Blender 6.0.

### Risk

CutBridge currently supports and tests Blender 5.2.1 successfully, so this is not a present Blender 5.2.1 failure. However, leaving the deprecated API in the mapping/rollback path may cause Blender 6.x compatibility failure or force a rushed migration later.

### Required work

- [ ] Inspect the current Blender 6.x compositor API contract before editing.
- [ ] Replace deprecated `Scene.use_nodes` dependence with the supported equivalent while preserving transactional mapping semantics.
- [ ] Add regression coverage proving prior valid mapping and artist nodes survive failed replacement attempts.
- [ ] Run the existing Blender 5.2.1 suite to prevent backward-regression.
- [ ] Add authoritative Blender 6.x runtime coverage only after an explicit compatibility target decision.
- [ ] Do not claim Blender 6.x support merely because the warning is removed.

## Priority A — GitHub Actions Node runtime migration

### Current evidence

Current CI passes, but GitHub warns that pinned revisions of actions such as checkout/setup-node/setup-python target deprecated Node 20 action runtimes and are being forced to execute on Node 24.

### Risk

CutBridge intentionally pins release-sensitive actions for supply-chain/reproducibility safety. Relying indefinitely on GitHub's compatibility override weakens confidence that the pinned action/runtime combination will remain supported.

### Required work

- [ ] Identify current official action revisions that natively support the supported GitHub Actions runtime.
- [ ] Review upstream action release notes/security changes before changing pins.
- [ ] Update pins deliberately rather than switching to floating major tags.
- [ ] Verify `persist-credentials: false` and existing release-isolation assumptions remain intact.
- [ ] Run complete CI and release simulation after pin updates.
- [ ] Record exact new SHAs and validation evidence.

## Priority A — `main` / `develop` release-promotion reconciliation

### Current evidence

`main` is intentionally a conservative release-locked baseline while `develop` contains S1–S8. The branches are materially diverged rather than a simple linear promotion state.

### Risk

A naive merge/cherry-pick strategy immediately before release could accidentally omit safety changes, reintroduce stale files, or create a release candidate whose tree differs from the tested `develop` candidate.

### Required work before RC promotion

- [ ] Freeze the exact candidate SHA on `develop`.
- [ ] Compare `main...candidate` file-by-file and classify all `main`-only commits.
- [ ] Produce an explicit promotion plan that preserves release locks and the tested product tree.
- [ ] Verify the promoted `main` tree matches the intended candidate plus only documented release-governance differences.
- [ ] Require green authoritative CI on the exact promoted `main` SHA.
- [ ] Keep release authorization unapproved until all release gates are deliberately satisfied.

## Priority B — Release governance / repository controls

Tracked primarily in issue #18.

Workflow-local authorization is defense-in-depth but cannot replace repository-level control of branches, tags, and historical-workflow publication.

Required before RC/stable publication:

- branch protection/governance for `main` and `develop`;
- `v*` tag creation/update/deletion restriction or equivalent release-path control;
- protection against stale/historical commit workflow publication;
- explicit auditable authorization for exact main/tag/channel/prerelease;
- post-publication artifact checksum/content verification.

## Priority B — Japanese target-user evidence

S8 native UI validation passed, but UI correctness is not the same as representative target-user usability/productivity evidence.

Before claims about Japanese workflow productivity or ease of use:

- [ ] recruit appropriate representative testers through a legitimate process;
- [ ] run the S14 task protocol;
- [ ] record completion time, failure/rework points, terminology confusion, and qualitative feedback;
- [ ] separate anecdotal feedback from measured results;
- [ ] do not fabricate participant data or performance claims.

## Priority C — Documentation drift prevention

S8.5 exists because several repository documents continued to describe S6/S7 as incomplete after S8 was already merged.

Recommended prevention:

- [ ] treat `docs/COMPLETION_STATUS.md` as the canonical session-state page;
- [ ] require session integration PRs to update README, roadmap, completion status, changelog, and relevant Quick Start/Test Plan entries in the same candidate or an immediately bounded reconciliation PR;
- [ ] keep exact native evidence in issues/PRs and summarize it in docs rather than duplicating every transient candidate state;
- [ ] add a simple static documentation-state regression later if it can be made reliable without hard-coding brittle commit counts.

## Non-debt / intentional boundaries

The following are deliberate design boundaries, not defects:

- negative/preroll export ranges are rejected rather than silently renumbered;
- QC is diagnostic-only and does not automatically repair ownership;
- revision updates are source-oriented and fail closed on incompatible geometry/pass-set/package structure;
- private source control is separate from customer update distribution;
- release authorization defaults to false;
- Japanese is the primary UI language while English remains a deterministic fallback/support language.
