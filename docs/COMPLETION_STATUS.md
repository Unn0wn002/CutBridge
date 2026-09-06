# CutBridge Completion Status

- **Current Session:** S4 — AE Contract Hardening; PR #12 repair prepared for authoritative CI and independent review.
- **Completed Sessions:** S1 — Baseline & Repository Integrity; S2 — Blender Render Mapping; S3 — Blender Production Hardening.
- **Open PR:** [#12](https://github.com/Unn0wn002/CutBridge/pull/12), `fix/session-4-ae-contract-hardening` → `develop`.
- **Live baseline inspected:** `main` = `e282ef99b3fa5772b3d6d1dbbcbfa4957816b78c`; `develop` = `a7c63683b3734ac24e51f8db5b3b7aaad2db6d39`. Neither integration branch is changed by this repair.
- **Automated Gate Status:** Prior PR head `657e4825c9eee4cb7f307bf47d1b5d5a6eb31c5d` FAIL in both jobs of run 34042183334 (cross-realm pass-array regression). Repair-local Node contract/host-adapter groups, release hygiene, Python compilation and Node syntax checks PASS. Full pytest and official bpy 5.2.1 are BLOCKED locally by unavailable dependencies; current-head GitHub CI must supply authoritative results. See PR #12 for the final run linked to the repair SHA.
- **Independent Review:** Required on the complete current PR diff before integration. The prior top-level review findings are addressed by the repair; no approval is implied.
- **Manual Required:** Blender GUI, AE GUI import/comp/QC, Blender→AE end-to-end, native Japanese users and production/client validation: MANUAL NOT EXECUTED in this repair session.
- **Known Blockers:** S4 completion/integration awaits current-head CI and independent review. No stable release exists. Negative export frames are explicitly unsupported until signed sequence ordering can be verified in AE.
- **Next Session:** S5 — AE Import/Comp Reliability, only after S4 review, merge to `develop`, and authoritative post-merge CI PASS. Do not begin S5 in this repair session.

## S4 repair scope

- ES3-compatible cross-realm array validation; finite integer frame endpoints/counts; strict numeric FPS/resolution/pixel-aspect validation; schema/version and pass-field diagnostics.
- Consistent non-negative export ranges in Blender validation/direct manifest production, JSON Schema, AE validation/filename formatting/coverage. Frame 0 and positive ranges remain supported.
- Package-relative paths reject absolute paths, traversal, URI escapes, empty/dot segments and Windows-normalization hazards. Safe backslash separators normalize to `/`; Japanese/Unicode names remain valid. Host adapter rejects folder/file aliases and checks path containment. Sequence patterns must be safe basenames with exactly one `####` token.
- Exact missing-frame coverage, unexpected matching filename warnings, required-pass blocking and optional-pass skips. Node host mocks verify adapter behavior but cannot certify AE APIs or filesystem behavior on supported desktop OSes.
- Legacy JSON parsing accepts data without `eval` execution. AE product version has one constant checked centrally against the canonical Blender version by the release builder; UI text reads that constant.
- Node is explicitly installed in CI/release jobs; missing Node fails the contract gate.

## Negative-frame decision

Blender's `BLI_path_frame` uses integer precision (`%.*d`), so `####` formats frame -1 as `-0001`, not the prior AE helper's `00-1`. Official bpy CI exercises `scene.render.frame_path(frame=-1)` to verify this actual formatter. This does not establish native AE signed-sequence chronological ordering, especially across zero. S4 therefore uses the explicitly allowed rejection policy: rebase the cut and preroll to frame 0 or later before export. It does not silently clamp, renumber, or modify animation. The schema remains version 1; its frame endpoints now have `minimum: 0` to describe the supported export contract.

S4 is not marked complete or merged by this document. Preserve this PR for any remaining same-session repair.
