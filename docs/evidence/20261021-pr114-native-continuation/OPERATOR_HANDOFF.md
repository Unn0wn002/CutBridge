# PR #114 native qualification handoff

Verdict: **INSUFFICIENT EVIDENCE — environment unavailable; no observed CutBridge defect.**
Prepared 21 October 2026. No current-candidate native checks or qualified screenshots were executed.

## One operator action

Provide an initialized disposable Windows VM with **Adobe After Effects 26.5.0 Build 89 normally installed/provisioned through Adobe Creative Cloud**, plus normally provisioned Blender 5.2.2. Leave it available for qualification. Provision dependencies/licensing separately before candidate execution; do not expose owner credential stores, HOME, browser profiles or unrelated projects. A different host build needs explicitly recorded compatibility scope.

The current host file `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFXLib.dll` (26.5.0.89) reports Authenticode **HashMismatch**, SHA-256 `39cd58ef58211b00720ee27cfcd243332fb6d289d37582c8fc2ba1679255b87d`. Its cause is unknown. A successful launch does not establish provenance. Do not copy this DLL into the guest or replace DLLs individually. Adobe Creative Cloud is installed at `C:\Program Files\Adobe\Adobe Creative Cloud\ACC\Creative Cloud.exe`. No application repair, security or licensing change was performed.

WindowsSandbox.exe is available, but no suitable provisioned guest was established. Hyper-V inventory returned permission denied (inventory unknown). The working 19 October Font Preflight sandbox is no longer present. The closed startup investigation was not restarted. This action is environment provision, not a request for a human reviewer.

## Exact package identity

Runtime/source: `5aa2da24fc8be41626ee84178c7fdce05d02eebc`.
Pre-continuation review head: `ac71996ebcc8a522e05cc1e511457ac1e116efa3`.
Version: **0.2.5 candidate — unpublished**.

| File in artifacts/ | SHA-256 |
| --- | --- |
| CutBridge-AfterEffects-v0.2.5.zip | `5363795c66b1fbb664444fd5346ca9532d99822ce2cf3315193d4abec1789b9c` |
| CutBridge-Blender-v0.2.5.zip | `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe` |

These exact bytes are already on this PC. Read-only Actions transport run 39581132797 retrieved them from artifact 12334183017 / original run 39575739610; the outer hash was recomputed on the transfer runner. Eleven transmitted files, both ZIP checksums and bootstrap checksum were verified on the PC. All four AE runtime files plus GPL match raw Git source. The original outer ZIP is not present on the PC.

The separately retained user-reported ChatGPT inspection covers all 48 evidence checksums, repeat assets, before/after inventories and ZIP integrity. It is download verification, not native execution or human review. Its missing original JSON was not reconstructed or relabeled; this packet has a fresh PC receipt instead.

## Already staged

The 53 copied harness/fixture files are byte-identical to the retained historical packet. Existing harnesses and the source-replacement supplement are reused without changes. Current runtime, package and installation receipts explicitly replace the old 639 identities; old historical receipts remain preserved.

Map only these inputs read-only after environment acceptance:

| This directory | Guest path |
| --- | --- |
| native-ae-input | C:\NativeAEInput |
| native-blender-visual-input | C:\NativeBlenderInput |
| real-blender-input | C:\Packages |
| ae-runtime | C:\AERuntime |
| review | C:\Review |
| artifacts | C:\Artifacts |

Use a fresh `C:\Evidence\verification-output` as the writable output/temp/profile/cache area. Inputs must stay read-only; network must be denied during candidate execution. Native application cache/preference writes need an explicitly bounded guest location. Record actual adapter, mount/ACL and credential boundaries, full vendor inventories, process IDs/exits, before/after input inventories and a host-side 60-minute watchdog. The supplied environment-acceptance.json remains NOT_ACCEPTED.

First prove blank vendor startup and the existing no-candidate probe with **no candidate mapped**. Review host provenance and effective isolation before candidate load. A process existing or launcher exit is insufficient. Keep all preparation/licensing and required prompts separate from candidate execution.

## Native work dependent on that environment

Use `docs/NATIVE_VALIDATION_HANDOFF.md` in PR #114 for the existing commands and evidence assertions. Run existing `run_all.jsx`, then `source_replacement_rollback.jsx`, then `fresh_reopen.jsx` sequentially in actual distinct/exited AE processes as documented. Retain real V001–V003 state, all negative/rollback reports and saved-project hashes.

Complete actual Blender ZIP installation, EN/JA normal/narrow/help and button behavior; AE installation of the **four adjacent runtime files into Scripts/ScriptUI Panels**, restart, **Window > CutBridge**, dock/resize/reopen, EN/JA fit, selectable Results, Build/QC/repeat Build, V001→V002→V003 confirmations, artist-state preservation, negative cases, moved-folder rejection, prepared source-replacement rollback, save/close/fresh-process reopen. Capture actual package screenshots. Floating mode is optional fallback. Check Updates offline fail-closed behavior; do not invent positive online-update evidence.

Current native status for every open case: **NOT_EXECUTED**. Reuse earlier Blender evidence only for its exact unchanged-ZIP scripted scope. Source-replacement supplement remains PREPARED_NOT_EXECUTED. Unsupported camera roll/Empty rotation/general sync and unvalidated host compatibility remain excluded. S14B/representative-user research is deferred and is not a release prerequisite.

## Release disposition

Administrative AI review is authorized and recorded; no human approval is claimed. Required native gates remain open, root release authorization false. No protected promotion, tag, publication or distribution was performed. v0.2.4 stays immutable/held; production stays v0.2.3. After native qualification, use the existing protected develop/main promotion, exact tag authorization, publication, downloaded-release verification and distribution process. Feature development ends at qualified publication; critical defects only afterward.

