# Native validation operator handoff — PR #113

## Active bounded free release — 21 October 2026

Current runtime source: `5aa2da24fc8be41626ee84178c7fdce05d02eebc`; [generated evidence/packages](https://github.com/Unn0wn002/CutBridge/actions/runs/39575739610/artifacts/12334183017) contain `candidate-output/dist-ci/` with the four artifacts. The CI packaging log reports Blender ZIP `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe` and changed AE ZIP `5363795c66b1fbb664444fd5346ca9532d99822ce2cf3315193d4abec1789b9c`. Independently download and verify all manifests/inventories and exact runtime bytes before native staging. The old 639-bound operator bundle below is historical: reuse its existing harnesses/real rendered fixtures only after review, and replace its runtime/package/receipt bindings explicitly. Never run it unchanged and attribute its identity to this new AE package. Keep the source-replacement supplement's own hash and preparation identity separate. See [the AI review](AI_RELEASE_REVIEW_2026-10-21.md).

Target: **Sunday, 25 October 2026 (Asia/Jakarta)**, confirmed by the owner. This supersedes the earlier 22 October working target. Scope is frozen; feature development stops at a qualified published release, with critical defects only afterward. See [the bounded release policy](FREE_RELEASE_2026-10-25.md).

The current branch `fix/free-release-20261021` retains all PR #113 commits and adds the dockable-first installation/compact ScriptUI/in-panel Build-QC patch. Earlier AE runtime/package hashes and frozen-runtime statements below describe historical candidates; they do not qualify this changed AE runtime. Historical 396-test/18-suite and Blender evidence remain bound to their exact recorded inputs.

The owner authorizes a separately documented AI code/evidence review instead of owner-controlled administrative human review for this release. This does not waive native acceptance or enforced GitHub approvals. S14B remains NOT_EXECUTED; unsupported channels and broad compatibility/commercial claims remain excluded.

Current native verdict: **INSUFFICIENT EVIDENCE**. Blank owner-session AE/Blender workspaces initialize, but the 19 October provisioned Sandbox is no longer present and the installed AE core DLL still reports HashMismatch. No current candidate code has been loaded into the owner session. The required isolated native campaign and qualified-build screenshots remain unexecuted. Release authorization remains false; v0.2.4 is immutable/held, production remains v0.2.3.

## Historical records (retain original identities and decisions)


Prepared 17 October 2026. **INSUFFICIENT EVIDENCE / NOT_EXECUTED / ACCEPTANCE NOT_RECEIVED.** This is the single handoff for the remaining native work. It does not authorize a security change, protected merge, publication or distribution. S14B is NOT_EXECUTED. Working target: 22 October; official deadline unconfirmed.

## Frozen inputs and completed work

Engineering baseline: `639374ce5f1b5f0d36847258d052c36ab21dd208`, branch `fix/current-release-completion-20261016`. The 5a4f43b closeout changed documentation/evidence only; the subsequent source-replacement rollback preparation changes test inputs and this handoff, while packaged runtime stays frozen. Preserve the exact-baseline **396 tests + 2 subtests**, RNA, 18 AE Node suites, syntax and repeat-package PASS in `FINAL_HEAD_VERIFICATION.json`. Later preparation checks retain their own tested SHA. Existing native Blender 5.2.2 build `d13f752e3b9c` evidence covers only its recorded unchanged-ZIP scripted scope.

Packet: `C:\Users\unn0w\.codex\worktrees\5d5d\CutBridge\dist\release-candidate-20261016`. The data-staged `operator-handoff` subdirectory contains existing native harnesses, the real rendered Blender V001–V003 packages, exact extracted AE runtime, 639374c review metadata and unfilled acceptance forms. It contains no claimed execution or approval. The original harness config is retained; its derived installation-metadata path points at read-only review input. Review all derivative configuration and hashes before execution.

| Frozen artifact | SHA-256 |
| --- | --- |
| Blender ZIP | `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe` |
| AE ZIP | `427a36ba8638e88940b18f9daa34537c7e41ad939f3b81fddb50a3812d691268` |
| Linux release metadata | `a9e0d91202173cb9ad431a3f1b85ca0b8b8d4a416ad49a5e8e3c336e23a1722f` |
| Linux checksums | `d153d2ca56594f28ee4ed75d9b97859d4430a0950ad1385aaa6d32fedebbe4bb` |

These read-only owner/reviewer commands verify identity without executing candidate code:

```powershell
$packet = 'C:\Users\unn0w\.codex\worktrees\5d5d\CutBridge\dist\release-candidate-20261016'
Get-Content -LiteralPath "$packet\FINAL_HEAD_VERIFICATION.json"
Get-FileHash -Algorithm SHA256 -LiteralPath "$packet\CutBridge-Blender-v0.2.5.zip", "$packet\CutBridge-AfterEffects-v0.2.5.zip", "$packet\release-metadata.json", "$packet\SHA256SUMS.txt"
```

## Current blocker and diagnosis boundary

The diagnosis window began `2026-10-16T15:55:38Z`, with deadline `16:55:38Z`. It elapsed during an interrupted turn. On resumption at `2026-10-17T00:47:41Z`, no further startup attempt was launched. The pending control had produced no guest files; its desktop alone did not prove native availability. No claim is made that the VM stopped at the deadline. Its 7,511 input records were identical before/after.

Full AE preparation encountered an unreadable `AfterFXLib.dll.bak` path; a subsequent lookup did not find it. The active `AfterFXLib.dll` Authenticode check reported **HashMismatch**, while AfterFX.exe and Blender.exe signatures verified. AE was excluded from the fresh control. This does not establish the cause of prior `0xc0e90002`, the separate `rpds` Application Control block, or the absent control output. No installation, authorization or security policy was changed. See [the retained assessment](evidence/20261017-validation-closeout/assessment.json).

Do not repeat those identical failed attempts. The next operator must supply a materially different, independently approved environment with normally provisioned vendor installations and working orchestration. Do not repair the current installation, copy license stores, disable security controls, or override execution policy through this handoff.

## Environment acceptance before any candidate load

Use a disposable Windows VM/Sandbox with supported, normally installed and appropriately provisioned Blender/AE. Prefer the recorded Blender 5.2.2 and AE 26.5x89 for comparable scope; other builds require their own explicit scope. Dependencies and permitted host licensing/profile preparation occur separately from candidate execution. No owner HOME, browser, SSH/cloud/GitHub authentication or other owner credential store may be exposed.

An independent operator/reviewer must record and approve:

- Exact OS/host/build and hashes of the full executable/dependency/startup-script trees; readable inventories and appropriate vendor provenance/signature checks. Current mismatched or unreadable AE inputs cannot be silently accepted as clean controls.
- Effective network denial, actual adapters/interfaces, read-only input mounts/ACLs, and explicit writable `verification-output`/temporary/profile/cache locations. Native host preferences and caches must fit the approved boundary; environment variables alone are not proof that the host honors it.
- Normal, approved orchestration and script/file permissions. Do not add an execution-policy bypass or alter application security/privacy settings to make a report appear.
- A host-side 60-minute deadline/watchdog independent of guest logon. Stop on missing isolation proof, unreadable/mutated inputs, initialization failure or a required permission/credential prompt. Preserve incomplete results as INSUFFICIENT EVIDENCE.

First launch **blank vendor hosts with no CutBridge code, ZIPs or fixtures mapped**. Blender uses `--factory-startup --disable-autoexec`; AE omits `-r`. Observe actual native workspaces, close normally, and record actual process IDs/exits. Then use separate fresh outputs for a reviewed no-candidate API probe. Keep vendor bytes/settings identical except the probe argument; record fresh/warm profile differences. An OS helper running or a process existing is not native availability. Require the probe JSON, exact build, actual native process and normal-exit evidence. Do not infer mapped-path causation from local versus mapped controls whose binary bytes/builds differ.

The existing no-candidate AE probe is `native-ae-input/probe.jsx`. A reviewed invocation inside the approved isolated guest is:

```powershell
& 'C:\AfterEffects\AfterFX.exe' -m
# After independent blank-workspace observation and actual normal exit,
# use a fresh probe output/profile under the same approved controls:
& 'C:\AfterEffects\AfterFX.exe' -m -r 'C:\NativeAEInput\probe.jsx'
```

Expected probe result: `native-ae/availability.json` says AVAILABLE, reports the exact host/build and says candidate execution/native campaign NOT_EXECUTED. Availability is not a workflow PASS. Complete `environment-acceptance.json` only after real independent acceptance; its supplied status is NOT_RECEIVED.

## Exact input layout and commands after acceptance

Use a new empty output for every attempt. Retain the reviewed VM policy and host-side before/after path/type/mode/byte inventories. Do not relaunch old r6 policies or reuse old output directories: they bind older review metadata and contain unsuccessful attempts.

| Read-only staged input | Approved guest path |
| --- | --- |
| `operator-handoff/native-ae-input` | `C:\NativeAEInput` |
| `operator-handoff/native-blender-visual-input` | `C:\NativeBlenderInput` |
| `operator-handoff/review` | `C:\Review` |
| `operator-handoff/ae-runtime` | `C:\AERuntime` |
| `operator-handoff/real-blender-input` | `C:\Packages` |
| `operator-handoff/artifacts` | `C:\Artifacts` |
| Reviewed, normally installed vendor applications | `C:\AfterEffects` and `C:\Blender` aliases |
| Fresh designated output only | `C:\Evidence\verification-output` writable |

These paths are a required layout, not proof that a VM is approved. `review/candidate.json` binds 639374c; `review/installation.json` records actual extracted file hashes as **data staging**, not installation acceptance. Independently compare all runtime/fixture/harness bytes with the bundle inventory. Native AE's common harness reads the receipt but does not itself authenticate those bytes; the external inventory is the authority.

Set `TEMP`, `TMP`, `TMPDIR` and `PYTHONPYCACHEPREFIX` under approved output. Set Blender config/data/extensions paths there too. Use reviewed orchestration to retain actual process IDs/exits, stdout/stderr and report state. The following are the existing native application commands, executed **only inside that approved guest**, sequentially:

```powershell
& 'C:\AfterEffects\AfterFX.exe' -m -r 'C:\NativeAEInput\run_all.jsx'
# Require the previous actual AfterFX.exe exit and saved artist-V003.aep first.
& 'C:\AfterEffects\AfterFX.exe' -m -r 'C:\NativeAEInput\fresh_reopen.jsx'
```

Expected `native-ae` outputs: campaign/negative/rollback/reopen JSON, all-status.json, artist-V001.aep through artist-V003.aep, preservation-baseline.json, reopened-V003.aep and fresh-process-reopen.json. Require each phase PASS, distinct actual native PIDs, prior exit before fresh launch, both actual normal exits, unchanged inputs, and concrete state assertions. Existing launcher `verdict.txt` reflects run_all only and does **not** gate on successful fresh-process reopen; adjudicate the full evidence yourself. A `.com` launcher exit or Sandbox shutdown is not native normal-exit evidence.

## Required native cases and retained-harness limits

- Execute real V001–V003 Build/QC/repeat Build/revisions using the 36 real rendered Blender inputs. Compare source paths, persistent ownership IDs, counts, dimensions/FPS/frame range, and concrete artist/root-note state.
- Execute existing required deletion/de-tagging, renamed/duplicate folder, incompatible timing/pass-set, required/optional status, optional-layer and optional-sequence cases. Require blocked operations to preserve the before/after project inventory.
- Execute existing post-import failure: capture the actual allocated numeric ID, require its removal and native `isValid(handle) == false`, preserve prior sources/notes/artist state and verify recovery Build/QC. Exercise stale native footage/layer rediscovery separately.
- Add the **moved deterministic folder** manual case in a disposable V003 copy: move the managed comp folder outside its package root; Build/revision/QC must reject without recreating/adopting structure or mutating other objects. Retain original and actual parent/item IDs.
- The historical r5 harness alone does **not** inject native source-replacement failure. The [supplemental phase](../tests/native_ae/source_replacement_rollback.jsx) below extends its existing CB helpers. Its status is **PREPARED_NOT_EXECUTED**; mock preparation checks do not establish native behavior. Do not relabel the post-import case as this separate gate.
- Inspect supported Camera Position/POI/Zoom and Null Position/Scale against manifest values/times independently of QC. Camera roll, Empty rotation, general projection and expected 3D completeness are excluded. Preservation fixtures do not cover every possible artist property; explicitly name extra claims such as blending/mattes or temporal ease if tested.
- Save/reopen within process, reload panel/Build/QC, then exit normally and reopen in a distinct fresh process. Return saved-project hashes and actual source/state comparisons.

## Prepared source-replacement rollback supplement

Status: **PREPARED_NOT_EXECUTED**. Targeted inventory and independent read-only review found no existing reviewed supplement. This phase uses unchanged retained `common.jsx`, actual packaged revision UI/adapter/executor and the campaign's disposable `artist-V003.aep`; it creates only an output-side V004 fixture. It does not replace the native campaign or its independent environment acceptance.

Reviewed preparation SHA: `85b8eb06617c1f195385c1b96ce9452882b63b8e`; supplemental file SHA-256: `332dfcf34551caabd741e4cc6b31216d36a11899e7af1aae1ac30148ad97e54d`. [Trusted offline verification](https://github.com/Unn0wn002/CutBridge/actions/runs/39012397226) passed 396 tests + 2 subtests, RNA, 18 AE Node suites, syntax and complete repeated packaging, with unchanged manifests and frozen assets. [The preparation record](evidence/20261017-source-replacement-rollback/preparation.json) retains the exact snapshot/image/host/artifact identity and initial failed diagnostic attempt. This evidence validates preparation, not the native operation. The packet's `SOURCE_REPLACEMENT_ROLLBACK_PREPARATION.json` and `operator-handoff/review/source-replacement-rollback.json` supplement the original 639-bound candidate receipt without rewriting it.

Before guest execution, stage the exact reviewed `tests/native_ae/source_replacement_rollback.jsx` alongside `operator-handoff/native-ae-input/common.jsx` as `C:\NativeAEInput\source_replacement_rollback.jsx`. Bind its SHA-256 and preparation commit separately from the frozen runtime SHA in the external input inventory; keep the input read-only. The amended operator bundle includes this phase and its checksum. Require at least two active managed passes, a successful existing campaign and its saved V003 artist project. The existing approved environment requirements above apply unchanged. The closed startup investigation must not be retried as part of this preparation.

After `run_all.jsx` has completed and its actual native process has exited, invoke inside that approved isolated guest:

```powershell
& 'C:\AfterEffects\AfterFX.exe' -m -r 'C:\NativeAEInput\source_replacement_rollback.jsx'
# Retain the actual AfterFX.exe PID and normal exit, then run the existing
# fresh_reopen.jsx command separately. A launcher exit is insufficient.
```

Expected output under `C:\Evidence\verification-output\native-ae`:

- `source-replacement-rollback.json`: every recorded check passes; native host/build, original candidate metadata and scope remain bound to the input inventory.
- `source-replacement-rollback-evidence.json`: complete `before`, staged numeric IDs/paths, two swap records, `after_first_swap`, `after`, cleanup and `recovered`. The first real swap must change the source. The second calls the real adapter with null and must actually throw from native `replaceSource`; retain exception text/file/line, unchanged native method and live-input checks. A synthetic wrapper throw, no-op first swap or accepted null argument cannot establish this gate.
- All staged IDs must be absent, every captured removed handle must satisfy native `isValid(handle) === false`, and original source paths/IDs, manifests, ownership comments, folder names/parents, caches and the retained campaign's measured artist state must equal the baseline. The existing preservation scope excludes unmeasured artist properties and unsupported 3D channels.
- `instrumentation_restored: true` after `finally` restores the manager factory and each adapter wrapper. The phase reloads the actual installed panel/manifest, runs Build/QC, compares recovered state and saves `source-replacement-rollback-recovered.aep`. Return its external SHA-256 plus process/log/input-integrity evidence. Partial evidence is flushed before/after injection and on failure; missing native throw or recovery is not a successful case.

Preparation is exercised through the existing `tests/ae_s6_native_host_checks.cjs` suite and canonical CONTRIBUTING verification, with adversarial mocks for a non-throwing native method, failed/no-op first swap and retained replacement IDs. Those results prove preparation only. The remaining blocker is an independently approved, initializing native AE environment; no native execution, environment approval or demonstrated-scope acceptance is claimed.

## Installation, visible UI and manual update

Blender: install the exact ZIP through the real Preferences > Get Extensions > Install from Disk flow, enable it and record actual EN/JA normal/narrow panel/help and Validate/Build button observations. Official CLI installation alone does not prove those actions. The existing visual orchestration uses:

```powershell
& 'C:\Blender\blender.exe' --command extension validate 'C:\Artifacts\CutBridge-Blender-v0.2.5.zip'
& 'C:\Blender\blender.exe' --command extension repo-add cutbridge_candidate --name CutBridgeCandidate --directory 'C:\Evidence\verification-output\extensions\candidate'
& 'C:\Blender\blender.exe' --command extension install-file -r cutbridge_candidate --enable 'C:\Artifacts\CutBridge-Blender-v0.2.5.zip'
& 'C:\Blender\blender.exe' --python-exit-code 1 --python 'C:\NativeBlenderInput\visual_blender.py'
```

The visual harness reports `native-blender-visual/ready.json` and captures native screenshots. Its adjacent README specifies output-side phase.json commands: EN, JA, NARROW_API_EN/JA, HELP_CAMERA_EN/JA, CAPTURE and QUIT. Issue one phase at a time, wait for its matching sequence, inspect real pixels and measured width, then continue. Capture failure or an unselected tab is not visual PASS.

AE: keep the four runtime files adjacent. Observe File > Scripts > Run Script File and EN/JA. For dockable acceptance, prepare the exact four files in the actual guest application's Scripts/ScriptUI Panels directory through approved installation preparation, verify/freeze their bytes read-only before candidate execution, restart AE, and observe Window > CutBridge. The old read-only mapped application cannot be written to for that installation; it needs the approved disposable installation target. Run Script File/evalFile is not dockable-menu evidence.

Manual update: with candidate networking denied, exercise the real Check for Updates UI and record unavailable/fail-closed behavior plus unchanged disabled startup scheduling. Positive discovery/selection/install requires a separately identified approved offline fixture/interface; absent that, leave it NOT_EXECUTED. Do not enable networking, publish or deploy v0.2.5 merely to make the check pass. Live publication/distribution checks belong to their separately authorized gates.

## Evidence and acceptance to return

Return one fresh evidence directory with environment acceptance, actual VM/network/credential/mount controls, full input inventories before/after, exact SHA and all artifact/runtime/fixture/harness hashes, OS/host/build, native command lines/start-end/PIDs/exits, complete stdout/stderr/events, phase JSON and native object/state comparisons, observed screenshots with case-specific notes, saved-project hashes and any exclusions. Keep ZIPs/projects/renders outside Git. Include a SHA-256 catalog and preserve interrupted checkpoints/raw unsuccessful results.

Use exactly one overall verdict: PASS, FAIL, INVALID, INSUFFICIENT EVIDENCE or WORKSPACE_NOT_ACCESSIBLE. Missing initialization/isolation/report/host evidence is insufficient; changed input integrity is invalid; an actual candidate assertion failure needs a valid isolated reproduction. Return the unfilled [scope form](validation/scope-acceptance.json) only after actual execution/review and named owner acceptance. The [independent review packet](INDEPENDENT_RELEASE_REVIEW_PACKET.md) is prepared; review and demonstrated-scope acceptance are both NOT_RECEIVED. Neither form authorizes a release or waives an unexecuted gate.
