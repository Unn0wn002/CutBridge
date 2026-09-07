# CutBridge Completion Status

- **Current Session:** S5 — AE Import & Composition Reliability; bounded implementation on `feature/session-5-ae-import-reliability`.
- **Completed Sessions:** S1 — Baseline & Repository Integrity; S2 — Blender Render Mapping; S3 — Blender Production Hardening; S4 — AE Contract Hardening; S4.5 — Documentation Reconciliation.
- **Open Implementation PR:** [#14](https://github.com/Unn0wn002/CutBridge/pull/14), `feature/session-5-ae-import-reliability` → `develop`.
- **Live baseline inspected:** `main` = `e282ef99b3fa5772b3d6d1dbbcbfa4957816b78c`; `develop` = `aab6c9b8ce9236d07386b7bf6f0c95034587246c`.
- **Automated Gate Status:** S4.5 merged through PR #13 at `aab6c9b8ce9236d07386b7bf6f0c95034587246c`; post-merge `develop` CI run `34051334080` PASS. S5 has green executable regression evidence on its implementation commits; the exact final PR head must remain green before independent integration.
- **S5 Blocker / Review Status:** The stale-cache ownership bypass and the first five independent-review blockers were repaired on PR #14 through head `18b8f1105bd997c66783e5a305c716e97b224955`. A follow-up independent review found two additional blockers involving combined cache drift and missing managed-state QC. A second bounded repair is now prepared locally; S5 is **not complete** until it is pushed, passes exact-head CI, and receives fresh independent review.
- **Independent Review:** Session 2 review found merge blockers; see [docs/S5_INDEPENDENT_REVIEW.md](S5_INDEPENDENT_REVIEW.md). Green CI is not self-approval; the implementation worker must not merge its own PR.
- **Manual Required:** After Effects GUI import/comp/QC, Blender→AE end-to-end, native Japanese-user validation, and production/client validation remain `MANUAL NOT EXECUTED` unless separately recorded with real evidence.
- **Known Blockers:** No stable GitHub release exists. Negative export frames remain intentionally unsupported until signed sequence ordering can be verified safely in After Effects; users must rebase export/preroll to frame 0 or later.
- **S6 Status:** Has not started. This repair is bounded Session 1 of the completion prompt; it remains product session S5.
- **Next Session:** S6 — Non-Destructive Revision Manager, only after S5 is independently reviewed, merged to `develop`, and authoritative post-merge CI is green.

## Session 2 independent-review gate

The independent review passes were **not safe to merge**. The first pass reproduced four S5 ownership/QC defects: a moved managed comp can cause a replacement comp before failure, duplicate managed comp tags are silently accepted, comp metadata QC disappears after script reload, and skipped optional passes can still be included in managed-layer ordering without current verification. It also found a reserved-prototype-key false duplicate in manifest membership validation. A follow-up pass against head `18b8f1105bd997c66783e5a305c716e97b224955` found two further defects: combined tag/name/source/container drift could still create replacement footage/layers in the same session, and QC could pass after reload when managed comp or required footage was deleted. These findings are recorded in [docs/S5_INDEPENDENT_REVIEW.md](S5_INDEPENDENT_REVIEW.md). A second bounded repair is prepared locally; no merge or S6 work is authorized until exact-head CI and a fresh independent review pass.

## S5 implementation scope

- Required-pass sequence coverage is preflighted before CutBridge mutates the AE project, so known missing required frames do not leave partial managed folders/comps/imports.
- CutBridge-managed comps, footage items, and pass layers receive deterministic package-scoped ownership tags in item/layer comments.
- Repeated Build operations reuse only matching CutBridge-managed objects instead of duplicating footage, comps, or managed pass layers.
- Reloading the same manifest rediscovers tagged project objects, so idempotency does not depend only on in-memory panel state.
- Same-name non-CutBridge comps are not hijacked; CutBridge blocks with an actionable collision error rather than modifying manual work.
- Existing managed comp metadata is checked against manifest resolution, pixel aspect, FPS, and duration. Drift blocks silent destructive correction.
- Managed comps are resolved from all live project items before creation; moved, renamed, wrong-type, or duplicate tagged comps fail closed without replacement.
- After every successful pass loop, including partial-build retries, deterministic manifest ordering is restored within the managed layer subset. Only managed layers are moved to the beginning; artist layers are not selected for movement and retain their relative order. Absolute artist indices/interleaving are not promised.
- Layer ordering considers only passes verified in the current build; skipped optional passes are not reused or reordered.
- A cached footage/layer reference that remains live but loses all ownership evidence blocks replacement instead of allowing a same-session duplicate; validated live layer lookups rehydrate the cache for later same-session checks.
- QC reports missing managed comp and required managed footage when a package-owned project folder exists, while retaining package-only QC before any managed project state has been created.
- Duplicate pass names and invalid/duplicate `ae.layer_order` references are rejected at the contract boundary.
- S5 behavior is covered by Node host-adapter regressions wired into pytest/CI. These mocks do not certify native After Effects APIs or desktop filesystem behavior.

## Bounded Session 1 — ownership/cache repair

**Reproduced before editing:** Removing a managed footage comment after Build still reported `reused safely` in the same panel session; re-evaluating the script then rebuilding created a second footage item. Removing a managed layer comment similarly produced false same-session success and a second layer after reload.

**Root cause:** `state.imported[tag] || findTaggedProjectItem(...)` and the early `state.layers[tag]` return bypassed live tag/container checks. Type/path/FPS and layer-source checks alone did not establish managed ownership.

**Repair policy:**

- Caches are observations, never lookup authority. Each lookup discards its cache entry and scans live project items/layers, then records only validated reusable objects.
- Footage must prove its exact package/pass tag, live project membership, `FootageItem` type, expected render-folder membership, source path, and readable matching conform FPS.
- Layers must prove their exact package/pass tag, live membership in the expected comp, `AVLayer` type, `containingComp`, and a readable source equal to the validated managed footage.
- Matching tags outside the expected folder/comp and duplicate managed tags block reuse. Removing/changing a tag does not grant permission to recreate or reclaim the object.
- An unverified item using the expected source path or generated footage name, or a layer in the managed comp using the expected pass name/source, is an ambiguity that blocks Build. These signals establish a collision, **not** ownership. This also applies to intentionally duplicated artist items using those signals.
- Errors preserve artist objects and request deliberate recovery: restore original managed metadata only if intended, move/remove a conflicting layer, or preserve the original project and build in a clean project. CutBridge does not automatically re-tag, replace, or delete them.
- QC uses live footage discovery too, so invalidated caches cannot hide source/FPS/ownership errors after a failed retry or script reload.

**Limits:** If an artist removes *all* identifying signals (tag, generated name, source association and managed container), there is no reliable persistent evidence tying the object to CutBridge after reload. It is treated as unrelated work and is never adopted. S5 does not introduce a hidden ownership registry or certify real AE runtime behavior.

**Regression evidence:** The S5 Node host harness now has 41 groups. Added coverage includes live moved/duplicate managed comps, reload-safe QC metadata discovery, prototype-key pass names, optional-pass skip ordering, removed/changed/unreadable tags; moved footage/layers; wrong types/containers; repeated same-session failures; actual script re-evaluation against the same project; duplicate tags; valid persistent fallback after replacing a cached reference; combined multi-field cache drift; missing managed comp/required footage after reload; and preservation of actual mock artist footage/layers. Original source/FPS, rollback, coverage, and partial-retry ordering regressions remain required.

**Validation:** Local S5 Node regressions: `PASS` (41 groups), plus the partial-retry, managed-layer guard, and rollback fixture checks. Local complete pytest remains `BLOCKED` at collection because official `bpy==5.2.1` is unavailable in this Python 3.12 environment. This second repair is not yet pushed; it still requires exact-head authoritative CI and a fresh independent review before any merge.

## S4 contract retained

- ES3-compatible cross-realm array validation and strict schema/schema-version handling.
- Finite integer frame endpoints/counts with `count = end - start + 1` and consistent non-negative export policy across Blender, shared schema, AE validation, and tests.
- Package-relative path hardening against absolute paths, traversal, URI escapes, empty/dot segments, unsafe Windows-normalization cases, aliases, and host-path escape.
- Japanese/Unicode relative names remain supported where valid.
- Exact expected-frame coverage, unexpected/mis-padded sequence diagnostics, required-pass errors, and optional-pass warning/skip behavior.
- Legacy JSON parsing without `eval` execution.
- AE-facing product version checked against the canonical release version by the release builder.

## Session discipline

S5 is limited to AE import/composition reliability and idempotency. It does not implement S6 revision replacement/preservation semantics. Real After Effects GUI behavior remains a manual gate until actually executed. S6 starts only after the S5 PR is independently reviewed, merged, and verified on `develop`.
