# Laptop direct-host checkpoint — 22 October 2026

**Verdict: INSUFFICIENT EVIDENCE. Release: HOLD.** Blank vendor applications initialize with graphics on this laptop. Candidate execution remains **NOT_EXECUTED** because the documented non-VM security boundary is not established. No CutBridge defect was observed.

The owner now requires directly installed Blender/After Effects and explicitly excludes further Hyper-V, VMware or Windows Sandbox creation, launch and troubleshooting. This supersedes the previous VM provisioning action. Before that instruction, read-only Hyper-V inventory returned permission denied and the owner reported no guest. No VM was created or launched in this laptop session.

## Repository and frozen identity

The supplied workspace was empty, with no checkout or existing local work. Cloned the existing `fix/free-release-20261021` branch without resetting or rebasing. Live PR #114 was open/draft at `fc3e1281d9bed1db5bbb6c963794ee4316a9fe16`, targeting develop `8cc5a4fe19e97c2f83105b888f96ccf1b423e8fd`; main was `a393e409d19445c4090460b7e7b4716779161fa4`. Apps, tools, tests, packages, workflows, GPL and release authorization match frozen tested source **`5aa2da24fc8be41626ee84178c7fdce05d02eebc`**. This checkpoint changes documentation/evidence only. Completed automated and historical native evidence retain their original identities and limitations.

## Actual blank application observations

Host: `AYAKUMI_NOZOMI_`, ASUS TUF Gaming F15 FX506HEB, Windows 11 Pro `10.0.26300` x64, 34,103,693,312 bytes RAM.

| Application | Actual startup and graphics observation | Process result |
| --- | --- | --- |
| Blender 5.2.3 LTS, build `e13b728c6880` | `blender.exe --factory-startup --disable-autoexec --debug-gpu`; fresh separate config/scripts/extensions/data/temp folders. Completed default Quick Setup, observed factory Cube/Camera/Light viewport. Vendor Help > Save System Info reports NVIDIA GeForce RTX 3050 Ti Laptop GPU, NVIDIA Corporation, `4.6.0 NVIDIA 617.42`, backend OPENGL. | PID 5608; 10:27:00.582–10:29:05.216 UTC; normal Ctrl+Q, exit 0. |
| After Effects 26.5.0 Build 89 | `AfterFX.exe -m`, no `-r`, existing owner profile. Observed empty Untitled Project workspace; Help > About confirms actual build. System Compatibility Report: **No conflicts to report**. Project Settings shows **Mercury GPU Acceleration (CUDA)**; inspected and cancelled without changing it. | PID 4176; 10:27:43.592–10:30:21.954 UTC; normal Ctrl+Q, exit 0. |

Each launching host process retained a 60-minute `WaitForExit` deadline with termination limited to its own native PID. Neither watchdog fired. Actual process records are adjacent JSON files. No artist project was opened or saved. Blender's first-run preferences were written to the temporary profile. AE used its existing profile, whose normal startup/cache/preference writes were not confined or inventoried as candidate outputs.

These observations establish bounded blank startup and reported graphics configuration. They do not establish GPU rendering correctness, a CutBridge native pass, or compatibility with the previously recorded Blender 5.2.2 build. Blender debug output includes shader/buffer performance warnings; the raw log is retained locally, not suppressed or treated as a product defect. No no-candidate harness probe or candidate harness was run in the owner context.

Full installed application-tree inventories cover **6,524 Blender files** and **9,852 AE files**, with identical before/after path, byte size, attributes and SHA-256 records. [Inventory receipts](vendor-inventories.json) bind the external catalogs. Shared OS/Adobe dependencies and the existing owner profile are not fully inventoried; this is not full environment acceptance. [Five actual screenshot hashes](screenshots.json) bind local vendor-only screenshots; these are not qualified CutBridge screenshots. Original screenshots, complete system report, logs and vendor catalogs remain outside Git at `C:\Temp\CutBridge-laptop-qualification-20261022`.

Blender.exe and AfterFX.exe signatures are Valid. **AfterFXLib.dll 26.5.0.89 reports HashMismatch**, SHA-256 `39cd58ef58211b00720ee27cfcd243332fb6d289d37582c8fc2ba1679255b87d`, exactly matching the separately recorded desktop DLL hash. Cause remains **UNKNOWN**. Successful blank startup does not resolve provenance. No DLL replacement, installation repair, security/licensing change or host reboot was performed. See [the actual signature records](environment.json).

## Independent package preparation completed here

Retrieved the original [artifact 12334183017](https://github.com/Unn0wn002/CutBridge/actions/runs/39575739610/artifacts/12334183017) through the authenticated GitHub connector and its returned download URL. The entire 12,366,041-byte outer ZIP is now on this laptop. Independently recomputed SHA-256: `04ef1fe67cd580200c4af6604c825680986745e4f56fc8184455166a566014cd`.

- Verified all **48** evidence-catalog checksums and the separate bootstrap checksum after guarded data extraction.
- Compared all four dist-ci/dist-repeat asset hashes; identical. Recorded before/after JSON inventories and checksum manifests are byte-identical. These are inspections of the retained run, not new product executions.
- AE ZIP: `5363795c66b1fbb664444fd5346ca9532d99822ce2cf3315193d4abec1789b9c`.
- Blender ZIP: `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe`.
- Extracted AE package as data; all four runtime files and GPL equal the raw frozen source. All six AE package files match the retained handoff catalog, including INSTALL.
- Recovered **14/53** retained harness/configuration files with exact catalog hashes. Recovered config applies only the previously documented installation-metadata-path amendment; resulting SHA-256 is exactly `c0026f4e41b45b56628e29ea08b428320eb716d24ed8685387e736e2bdfef59a`. The source-replacement supplement retains its reviewed hash and PREPARED_NOT_EXECUTED status.
- **39 fixture files remain unavailable here:** three V001–V003 manifests plus 36 rendered PNG/EXR files. The original artifact's raw source archive and current repository do not contain them. [Expected hashes](missing-fixtures.json) are preserved; no fixtures were regenerated. Data-only transfer of `real-blender-input` from the desktop's `C:\Temp\CutBridge-native-qualification-20261021\operator-handoff` is still required. Recheck all 39 hashes after transport.

The partial local packet is `C:\Temp\CutBridge-laptop-qualification-20261022\operator-handoff`: **24/73** historical handoff entries recovered exactly. It is explicitly incomplete, is not an immutable execution mount, and has no accepted environment/installation receipt. [Fresh laptop receipt](package-receipt.json) and [recovered input hashes](recovered-inputs.json) do not recreate or relabel the inaccessible original user verification JSON.

## Exact missing non-VM boundary and next action

The blank processes ran under the existing owner Windows account. No separate credential/filesystem confidentiality boundary or restricted candidate process token exists. Owner HOME and unrelated files remain accessible; redirecting Blender preferences does not remove those permissions. AE demonstrably uses the owner profile. Effective candidate network denial is unproven and was not configured; Wi-Fi and ZeroTier were Up. No immutable read-only execution inputs and enforced output/temp/profile/cache write confinement exist for a non-VM candidate run. Installed AE provenance also remains unresolved.

**Next prerequisite is a concrete, independently verified non-VM execution arrangement** that denies the candidate access to owner HOME/credentials/private files, denies candidate network access, enforces read-only exact inputs and bounded writable outputs/profiles/caches, and retains the existing host watchdog. A dedicated Windows test account with appropriately enforced filesystem and network controls is a possible preparation route, not an accepted boundary merely because the account exists. Protected account/consent/licensing steps belong to the owner. No security changes or credentials were copied to create such an arrangement here. Do not resume VM investigation. The current mismatched AE installation cannot be silently accepted as a clean vendor control; establish accepted vendor provenance separately without individual DLL substitution or weakening licensing/security.

Until those controls are actually established, do not load CutBridge, run its probes/imports/tests/builds, or install its add-on/panel in this owner account. Complete the missing fixture transfer as data-only preparation. After boundary/provenance acceptance, use the existing handoff/harnesses and exact packages for all outstanding installation, docking, EN/JA, Results, Build/QC/repeat, revisions, preservation, negative/moved-folder, rollback, fresh-reopen and screenshot gates. No new validation framework is introduced.

Root release authorization remains false. No promotion, tag, publication or distribution occurred. [PR #114](https://github.com/Unn0wn002/CutBridge/pull/114) stays draft; [v0.2.4](https://github.com/Unn0wn002/CutBridge/releases/tag/v0.2.4) remains immutable/held and production stays v0.2.3. There is no new release/download verification to link. Deadline remains Sunday, 25 October 2026, Asia/Jakarta. Existing authorization covers the protected release process once its applicable gates pass.
