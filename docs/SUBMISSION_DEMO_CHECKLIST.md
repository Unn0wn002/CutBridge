# CutBridge submission and demo checklist

## Active bounded free release — 21 October 2026

Target: **Sunday, 25 October 2026 (Asia/Jakarta)**, confirmed by the owner. This supersedes the earlier 22 October working target. Scope is frozen; feature development stops at a qualified published release, with critical defects only afterward. See [the bounded release policy](FREE_RELEASE_2026-10-25.md).

The current branch `fix/free-release-20261021` retains all PR #113 commits and adds the dockable-first installation/compact ScriptUI/in-panel Build-QC patch. Earlier AE runtime/package hashes and frozen-runtime statements below describe historical candidates; they do not qualify this changed AE runtime. Historical 396-test/18-suite and Blender evidence remain bound to their exact recorded inputs.

The owner authorizes a separately documented AI code/evidence review instead of owner-controlled administrative human review for this release. This does not waive native acceptance or enforced GitHub approvals. S14B remains NOT_EXECUTED; unsupported channels and broad compatibility/commercial claims remain excluded.

Current native verdict: **INSUFFICIENT EVIDENCE**. Blank owner-session AE/Blender workspaces initialize, but the 19 October provisioned Sandbox is no longer present and the installed AE core DLL still reports HashMismatch. No current candidate code has been loaded into the owner session. The required isolated native campaign and qualified-build screenshots remain unexecuted. Release authorization remains false; v0.2.4 is immutable/held, production remains v0.2.3.

## Historical records (retain original identities and decisions)


Closeout, 17 October: frozen `639374c` completed **396 tests + 2 subtests**, RNA, 18 Node suites, syntax and repeated packaging; its unchanged [final receipt](evidence/20261017-validation-closeout/BASELINE_639374c_VERIFICATION.json) is authoritative. Runtime/package bytes remain frozen. The timeboxed follow-up did not establish an approved initializing native environment. Use [the operator handoff](NATIVE_VALIDATION_HANDOFF.md), [review packet](INDEPENDENT_RELEASE_REVIEW_PACKET.md) and unfilled [scope form](validation/scope-acceptance.json). Native execution, independent release approval and demonstrated-scope acceptance remain incomplete. Dated a447/5293 evidence below retains its own counts.

Working target: **22 October 2026**. The official submission deadline and evaluator-specific delivery requirements remain **unconfirmed**. This checklist prepares a reviewable v0.2.5 packet and demonstration using the existing [release checklist](RELEASE_CHECKLIST.md), [verification commands](CONTRIBUTING.md) and [S12 host procedure](S12_E2E_VALIDATION.md); it adds no parallel test command or publication path.

Current assessment, 16 October 2026: **INSUFFICIENT EVIDENCE**. Exact code `a44792099b3b5f5b7a2f69a41061268fe59586b3` passed independently trusted Linux verification (**395 tests + 2 subtests**, no skips) and ordinary CI. The equivalent-ZIP native Blender 5.2.2 scripted V001–V003/render/preservation/rollback/fresh-process-reopen scope passed. Current native AE and Blender visual checks are **BLOCKED** by host initialization before candidate execution. Manual-update checks, scope acceptance and independent release review remain open; see [current preparation](RELEASE_PREPARATION_v0.2.5.md) for hashes and exclusions. The local packet is ready for review at `dist/release-candidate-20261016/`; acceptance is incomplete. Historical `fef1023`/`049c095` isolation provenance remains incomplete. S14B is NOT_EXECUTED.

## Readiness decisions

| Decision | Evidence required | Current boundary |
| --- | --- | --- |
| Submission packet | Exact candidate and trusted verifier identities; required automated/native evidence for demonstrated scope; reproducible ZIPs/checksums/metadata; installation instructions; limitations and demo | Local review packet assembled with current trusted Linux and scoped Blender evidence; AE/visual/manual/scope acceptance and independent release review remain incomplete. Deadline/delivery rules remain unconfirmed. Candidate files remain unpublished. |
| Public release | All applicable release gates, independent review, protected promotion, explicit owner authorization for exact current-main/tag/channel/prerelease, guarded publication and independently verified downloads | Not authorized. `release-authorization.json` stays false. |
| Production distribution | Approved published artifacts, independent download verification, official Blender index generation and deployed install/update/no-downgrade checks | Held on v0.2.3. Published v0.2.4 remains immutable and is not mirrored because of Issue #99. |

Submission preparation does not authorize an external submission, protected merge, authorization change, tag, publication or distribution. No representative Japanese-user validation or broad production-usability claim is made.

## Freeze and retain the packet

- [x] Record tested branch/code SHA `a44792099b3b5f5b7a2f69a41061268fe59586b3`, fetched base, true merge-base, changed paths and candidate diff; triage current versus superseded findings with code evidence. See [review triage](evidence/20261016-release-completion/REVIEW_TRIAGE.md), [retained inputs](evidence/20261016-release-completion/retained-inputs.json) and the [trusted verification record](evidence/20261016-release-completion/trusted-linux/passed-r2/verification.json). Independent release approval remains separate.
- [x] Review the verifier independently of candidate refs and retain bootstrap `8d1ecef5e2abb8c0b27f7951eb5a3eb75773afcc`, trust SHA `a6ee2445f81906c024fd5b9e1689faac017f198a`, image/toolchain, exact snapshot inventory/modes/bytes, manifests and enforced no-network/read-only/no-owner-credential output/temp settings in the [trusted Linux evidence](evidence/20261016-release-completion/trusted-linux/passed-r2/).
- [x] Run all required **automated** CONTRIBUTING commands and relevant regressions on the recorded tested code: **395 passed + 2 subtests**, no skips, `bpy 5.2.1`, 18 AE Node suites, syntax and package checks. Retain [commands/logs](evidence/20261016-release-completion/trusted-linux/passed-r2/checks.log), exact-head [ordinary CI](https://github.com/Unn0wn002/CutBridge/actions/runs/38909885640), source manifests and verdict. Native/manual acceptance is excluded from this completed row.
- [x] Build twice with `tools/build_release.py` inside isolation; compare complete inventories/bytes of both ZIPs, checksums and metadata. [Both Linux build inventories](evidence/20261016-release-completion/trusted-linux/passed-r2/repeated-package-inventory.json) match. Retain Linux exact assets as the primary packet. Windows/Linux ZIPs match; metadata/checksum CRLF/LF bytes differ with equivalent entries. Each toolchain's four-asset repeat is individually identical.
- [x] Record tested source/snapshot, artifact, fixture, rendered-package and native-harness hashes, host/build and observed process identities in [retained inputs](evidence/20261016-release-completion/retained-inputs.json), [native Blender evidence](evidence/20261016-release-completion/native-blender/) and [AE assessment](evidence/20261016-release-completion/native-ae/assessment.json). These identities do not claim that the blocked corrected AE harness executed.
- [x] Retain actual isolation policies/settings and before/after integrity records for executed scoped campaigns in [current evidence](evidence/20261016-release-completion/). The [trusted Linux settings](evidence/20261016-release-completion/trusted-linux/passed-r2/isolation-before.json) enforce the boundary and approved TEMP/TMP/TMPDIR/bytecode paths; current Windows/native policy records remain distinct from historical incomplete `fef1023`/`049c095` records.
- [x] Assemble the unpublished local review packet at `dist/release-candidate-20261016/` with both ZIPs, exact Linux `SHA256SUMS.txt`/`release-metadata.json`, `README.md`, `EVIDENCE_BINDING.json`, source/diff inputs and `DEMO_CHECKLIST.md`; retain logs before expiry. Hash both ZIPs independently and compare their values with the current preparation table and adjacent metadata/checksums. Generated packages, footage and native projects stay outside Git.
- [x] Frozen final engineering head `639374ce5f1b5f0d36847258d052c36ab21dd208` completed ordinary CI and independently trusted verification (**396 passed + 2 subtests**); the unchanged local `FINAL_HEAD_VERIFICATION.json` is also retained as [baseline evidence](evidence/20261017-validation-closeout/BASELINE_639374c_VERIFICATION.json). Later documentation-only closeout changes do not reassign counts or create native acceptance.
- [ ] Execute the corrected current AE installation/workflow/revision/preservation/negative/rollback/reopen scope in an approved host that initializes successfully.
- [ ] Complete applicable EN/JP/narrow panel/help and installation visual checks, real button/manual-update checks and explicit demonstrated-scope acceptance. The current visual attempt stopped before candidate execution.
- [ ] Obtain independent exact-candidate release review. Keep public-release promotion, authorization, publication and distribution on their separate authorized paths; S14B remains NOT_EXECUTED.

Historical evidence may only be reused for demonstrated equivalence: compare exact runtime-file/fixture/harness bytes, toolchain and host/build, describe excluded changes and limit the reused scope. A guide-only ZIP change still requires inspection of that exact packaged guide and current installation sign-off. Runtime changes invalidate any blanket claim that old native results accept the new candidate.

## Native execution sheet

Use synthetic/disposable copies. The table defines execution requirements; it does not mark every check complete. Record exact inputs/scope and evidence for each executed check, distinguishing the current scripted Blender results from pending visual/manual and AE work. Retain screenshots where they establish UI behavior and scalar/state logs for API-checkable outcomes. A checklist or prerecorded historical demo is not execution evidence.

| Check | Required observation |
| --- | --- |
| Blender installation and UI | Install the exact ZIP through the actual supported install path, enable it, inspect normal/narrow N-panel in Japanese and English, save/reopen preferences as applicable; no stale install is silently reused. |
| Blender package/render | Save a synthetic cut; Validate → Build → real Render Animation with normal panel active. Produce V001/V002/V003 and expected nonzero frame counts for the claimed pass/format combinations; all render paths stay within approved output. |
| Blender safety/rollback | Same-version payload overwrite refused; mismatch and unsupported pass/camera cases fail closed; injected mapping failure restores compositor/artist nodes and original frame/state. Include applicable 4.2/4.5 legacy-path checks without claiming full-host coverage from a focused probe. |
| AE installation | Verify exact-ZIP hashes and four adjacent runtime files; launch through Run Script File and, if claimed, dockable ScriptUI installation/restart. Confirm JP/EN UI; test localization-only fallback separately in a disposable runtime copy. Missing safety sidecars fail closed. |
| Cross-host baseline | Import the actual rendered Blender V001 package; Build/QC, expected sequence paths/FPS/frame range/comp dimensions, repeat Build with stable managed counts and no artist-object adoption. |
| Revision chain | Use actual V001 → V002 → V003 packages; observe source paths and current ownership after each revision, Build/QC and panel reload. Reuse the cached panel/manager across the chain to exercise live-state lookup. |
| Preservation | Compare before/after effects and mask values, transforms, parent IDs, in/out/start times, time stretch, layer order/IDs, expressions/keys, flags, artist layers, unrelated footage/comps/folders and studio/package-root notes. Managed Camera/Null channels are intentionally refreshed; preserve unrelated artist state. |
| Optional/pass policy | Required↔optional status change shows explicit warning/confirmation. Complete optional layer absent and optional sequence absent remain warning/skip only. Added pass, required removal and optional removal reject before import/source/tag mutation. |
| Negative ownership/contract | Missing and separately de-tagged required layer, missing/duplicate/moved deterministic folders, unmanaged same-name collision, invalid manifest/path, FPS/frame-range/pixel-aspect/resolution drift all fail closed without changing the original package/project. |
| Import/replace failure | Inject failure after import but before validation succeeds, and separately during source replacement. Captured imported IDs are removed even after native handles become invalid; previous sources, metadata/root notes and unrelated objects survive rollback. Record object inventories and reload/Build/QC recovery. |
| Camera/Null subset, if shown | Compare manifest samples with Camera Position/Point of Interest/Zoom and Null Position/Scale values/times, ownership and counts after Build/revisions. Check projection with an explicit fixture if projection is claimed. QC alone cannot validate these values, expected completeness or projection. Do not demonstrate camera roll or Empty rotation as supported. |
| Reopen and exit | Save revised project, close/reopen within process, reload panel, Build/QC and compare preserved state. Then close AE normally, record actual exit, relaunch a fresh process, reopen the saved project and repeat checks. Save/reopen Blender where in scope; record normal exit. |

## Demonstration sequence

1. Show the candidate SHA, host/builds, ZIP hashes and actual executed scope. State “working target 22 October; official deadline unconfirmed,” unpublished status and S14B NOT_EXECUTED.
2. Show Blender's metadata, preset/pass selection and Validate result. Build V001, render the short synthetic cut, inspect the manifest and complete pass sequences.
3. Launch AE from the exact package, load V001, Build, show managed comp/sequence setup, QC result and one artist-added layer/effect/root note used as preservation sentinels.
4. Apply V002 then V003. Show updated sources alongside unchanged artist sentinels and managed counts; run Build/QC after panel reload.
5. Show a supported required/optional status warning and an overwrite/incompatible-revision refusal in disposable copies. Show before/after state establishing no unintended mutation.
6. If 3D is included, state the implemented channel list and inspect those channels directly. Explain that Camera roll, Empty rotation, full-scene sync and 3D transform/projection QC are outside scope. Keep the normal 2D handoff as the primary path.
7. Save, quit normally, reopen in a fresh AE process, reload CutBridge and repeat Build/QC. End with the limitations, evidence verdict and remaining blockers rather than a broad production-readiness claim.

The spoken demonstration can use a short subset; the complete native execution sheet remains required for the corresponding release claims. Never fill missing native results or participant feedback with simulated outcomes.
