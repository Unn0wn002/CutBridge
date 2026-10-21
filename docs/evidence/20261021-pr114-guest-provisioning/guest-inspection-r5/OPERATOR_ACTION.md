# AI Native Test guest preflight — 21 October 2026

**Verdict: INSUFFICIENT EVIDENCE.** The VM exists and is running, but the graphics preflight blocks Blender. After Effects remains at its compatibility warning at the owner's request. These are vendor/environment observations before any CutBridge load, not a CutBridge defect or qualification pass.

## Completed inspection

- Hyper-V Manager visibly lists `AI Native Test` running with 32768 MB. The operator opened its console after the elevated Manager ignored one supported double-click. The console was accessible after the owner explicitly resumed computer interaction.
- Device Manager exposes **Microsoft Hyper-V Video** only under Display adapters. It reports working properly; Microsoft driver `10.0.26100.1150`, dated `6/21/2006`, displayed signer Microsoft Windows. This is a UI observation, not a full binary/signature inventory.
- The host is Windows 11 Pro `10.0.26300`, with NVIDIA GeForce RTX 5060 Ti driver `32.0.16.1742` plus the separately recorded virtual display adapters. Host GPU availability does not establish guest GPU availability.
- One agent Start-menu launch of **Blender 5.2** reproduced **Unsupported Graphics Card Configuration: OpenGL 4.3 or higher required**. Its exact build, factory-startup control, process ID and exit evidence were not established. No CutBridge file was loaded.
- The owner reports that guest Adobe was installed through official Creative Cloud. One agent launch of **Adobe After Effects 2026** presented Crash Repair Options referring to a previous crash. Its cause and previous session are unknown. Continue was selected within this same attempt, without resetting preferences or using Safe Mode.
- AE displayed an Untitled Project workspace behind a System Compatibility Report: **no suitable GPU; rendering will use software (CPU)**. The owner explicitly chose **Leave the warning open**. **Continue with known issues remains unclicked.** Exact AE build, full provenance, blank-startup acceptance, normal process exit and no-candidate probe remain unverified.

[Microsoft's GPU troubleshooting guidance](https://learn.microsoft.com/en-us/troubleshoot/windows-server/virtualization/troubleshoot-hyper-v-gpu-assignment-partitioning-passthrough-issues) says DDA and GPU-P are not supported on client OSes such as Windows 11 Pro. No community GPU script, driver/DLL copy, unsupported passthrough, security change, host repair or host reboot was attempted. This does not assert that every possible virtualization product is unavailable.

## Current handoff

Preserve **AI Native Test**, its installed applications and the open AE warning. There is no further request to download Windows or repeat the old consent/gallery selections. Those records remain historical.

A separately approved graphics-capable isolated route is the next dependency for Blender GUI qualification. Installing another hypervisor falls outside the owner's route limited to existing approved facilities; no new hypervisor has been installed. Bounded uninstall-registry inventory did not list VMware or VirtualBox; that is not an exhaustive proof of absence. VMware Workstation's documented 3D/OpenGL route is an option for further approval and preflight, not a qualified replacement or a guarantee that AE will meet requirements. Do not delete or convert the existing guest as part of this record.

The [computer-use skill](C:/Users/unn0w/.codex/plugins/cache/openai-bundled/computer-use/26.1016.51333/skills/computer-use/SKILL.md) refers to [confirmation rules](C:/Users/unn0w/.codex/plugins/cache/openai-bundled/computer-use/26.1016.51333/docs/confirmations.md) covering “Accept third-party ‘are you sure?’ warnings.” Confirmation was requested for AE's compatibility warning; the owner declined acceptance. This preserves that exact stopping point without treating it as consent or a test failure.

## Evidence and release scope

Raw actual preflight screenshots are retained at `C:\Temp\CutBridge-hyperv-guest-inspection-20261021-r5`; their exact SHA-256 values and observed fields are in `guest-preflight.json`. They are **not qualified-build CutBridge screenshots**. Guest OS/media and vendor dependency trees have not been hash-bound. Credential isolation, effective network denial, read-only inputs, writable outputs and the host-side watchdog remain unaccepted. No candidate was mapped or executed by the agent. No PID/exit or harness JSON is invented.

Frozen runtime: `5aa2da24fc8be41626ee84178c7fdce05d02eebc`. Pre-checkpoint documentation head: `60692059ed9734e6931a8e56800284906abb3398`.
AE ZIP: `5363795c66b1fbb664444fd5346ca9532d99822ce2cf3315193d4abec1789b9c`.
Blender ZIP: `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe`.
The existing packet stays at `C:\Temp\CutBridge-native-qualification-20261021\operator-handoff`.

Implementation, prior automated verification, artifact inspection, AI administrative review and complete #113/#112 ancestry are retained. A data-only Git comparison confirms apps/tools/tests/workflows/packages/GPL/release authorization still match the frozen source. No product-test rerun was justified by this documentation-only preflight.

All required candidate installation, dock/layout, selectable results, Build/QC/repeat, V001–V003, preservation, negative/source-replacement rollback and fresh-process reopen cases remain NOT_EXECUTED. Previously valid Blender scripted evidence is reused only within its recorded unchanged-package scope. The historical host `AfterFXLib.dll` **HashMismatch** remains of unknown cause; it is neither attributed to this guest error nor resolved by visible AE startup.

Release remains on hold, root authorization false. No merge/tag/publication/distribution occurred. v0.2.4 assets stay immutable and held; production remains v0.2.3. AI review remains authorized; representative-user research stays deferred.
