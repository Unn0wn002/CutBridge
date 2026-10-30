# Native AE evidence at 049c095

Overall release-readiness verdict: **INSUFFICIENT EVIDENCE**. The executed scope below passed; this is not a complete S12 sign-off or authorization to publish.

Candidate: `049c095258f9fc2dd89cbf8f1d7b2b3114d80296`. Windows Sandbox with user-installed After Effects **26.5x89**, network disabled, immutable read-only source/package/fixture shares, no owner home or credentials, explicit writable verification-output/TEMP. Existing synthetic test checkpoints and rendered Blender 5.2.2 packages were reused as identified inputs. Sandbox installations were preserved.

Latest ZIP SHA-256: AE `ae9bfb9c2aa36c6764b324ac74ef85cc5022071b04bb7b7695e64a3651f70366`; Blender `3a53f7af8420909e5ed300440df115dffef2ba1dd196688c7c99789a8a48aa48` (unchanged). All four AE runtime files were extracted together from the exact downloaded CI ZIP. They remain unmodified.

Executed native checks:

- Clean V001 Build, QC, repeat Build with stable item/layer counts, and project save passed.
- Actual panel V001 → V002 → V003 revisions passed; each QC reported zero errors. All four sources point to the selected package revision. Camera and marked Null samples match the Blender manifest.
- Layer IDs/order, opacity keys/expression, effect/mask counts, enabled/shy flags, parenting and the unmanaged artist layer remain unchanged in the inspected snapshots. This does not certify exhaustive effect/mask values, artist transforms/timing, unrelated project objects or studio root notes.
- Same-process save, project close/reopen, panel reload, repeat Build and QC passed with unchanged layer snapshots. Normal AE process exit and a full fresh-process persistence campaign remain unverified.
- After that reload, actual panel V003 → V004 changes DEPTH from required to optional, presents the explicit warning, completes successfully and passes QC. The cached manager remains present from earlier panel/project sessions.
- Removing the complete optional DEPTH layer while retaining its managed footage now produces exactly one `CBQ-LAYER-OPTIONAL-MISSING` warning and zero errors. Native `isValid()` independently reports the removed handle invalid. Both exact-source and exact-ZIP reproductions passed.
- A fresh fixture with the optional DEPTH sequence absent builds only the three required passes; QC reports one optional-sequence warning and zero errors. Its corrected reporting harness passed.

The original optional-source reporting harness tried to serialize the native Build result (including its comp) and hit a stack overrun after observing correct Build/QC behavior. Its empty report is excluded; the screenshot and harness are retained as **INVALID** reporting evidence. A fresh harness serializing only scalar Build results reran successfully. A separate AE internal-context warning during scripted synthetic text creation is preserved in `host-context-warning.png`; do not treat that fixture as representative artist validation. Native alert Japanese glyphs retain the recorded Sandbox font limitation.

Historical defects remain recorded: [7d80a42](../7d80a42-native-ae/README.md) exposes stale manager state and removed-footage comparisons; [89b1dab](../89b1dab-native-ae/README.md) verifies the first repair and exposes optional deleted-layer QC. The current runtime fixes both, with regression coverage. Earlier FPS/pass-set rejection checks remain SHA-bound to 89b1dab; missing/de-tagged required-layer and folder checks remain bound to 7d80a42 and should be repeated for final release sign-off.

All **18 AE Node suites** passed separately in the offline Sandbox. Source/test/harness manifests before/after match; existing original package and revision-case manifests also match. Exact candidate [CI push](https://github.com/Unn0wn002/CutBridge/actions/runs/37180451191), [CI PR](https://github.com/Unn0wn002/CutBridge/actions/runs/37180453602), [isolated push](https://github.com/Unn0wn002/CutBridge/actions/runs/37180451235), and [isolated PR](https://github.com/Unn0wn002/CutBridge/actions/runs/37180453630) passed. Full automated suite: **313 tests + 2 subtests**, Blender RNA 5.2.1, syntax, identical repeated packaging, unchanged source manifests, and offline distribution-preview/update/downgrade checks.

Remaining gates include complete installation/native negative/preservation coverage, independent review, representative Japanese artist validation, protected promotion/authorization/publication, published-download verification and deployed distribution checks. Production remains v0.2.3; v0.2.4 is held; startup checking stays disabled. No ZIPs, AE projects or rendered sequences are committed here.
