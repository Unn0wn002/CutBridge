# PR #114 guest provisioning — 21 October 2026

**Verdict: INSUFFICIENT EVIDENCE.** Vendor environment provisioning stopped before a usable guest desktop. No CutBridge defect, candidate execution, native pass or qualified-package screenshot is claimed.

## Exact stopping point and one operator action

**In the open Hyper-V Manager window, select `AYAKUMI_NOZOMI` in the left pane and report the resulting VM list or access/error message.** No VM creation or alteration is requested at this checkpoint.

The management console currently has the root selected. The computer-use helper reports: “Accessibility is limited because the target window has higher Windows integrity than the Computer Use helper.” This is a Windows integrity boundary; no coordinate input or alternate automation was attempted against it. The actual screenshot is retained locally at `C:\Temp\CutBridge-guest-setup-20261021-r1\hyperv-manager.jpg`. Its observation does not establish the existence or absence of any usable VM.

The [computer-use skill](C:/Users/unn0w/.codex/plugins/cache/openai-bundled/computer-use/26.1016.51333/skills/computer-use/SKILL.md) delegates confirmation handling to [its rules](C:/Users/unn0w/.codex/plugins/cache/openai-bundled/computer-use/26.1016.51333/docs/confirmations.md), which require handoff for “Bypass Windows/browser/web safety barriers.” No elevation, group membership/access change, host repair, reboot, Windows-feature change or security/licensing adjustment was performed.

## Setup actually attempted

- Reviewed supported Microsoft [Sandbox CLI](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-cli) and [configuration](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file) interfaces. `wsb.exe` version **0.8.107.0** is available; its initial list was empty. Hyper-V services vmms/vmcompute/hns run and a hypervisor is present. Prior `Get-VM` permission denial remains an unknown inventory, not proof of absence.
- Created one fresh preparation policy, with 16 GiB RAM, default-enabled vGPU/networking for official installer preparation, disabled audio/video/printer/clipboard redirection, and only the new writable `C:\PreparationEvidence` mapping. No owner HOME, credentials, host Adobe tree, candidate, fixture or package was mapped.
- Issued exactly one `wsb start --config <retained XML> --raw`. It exited **-2143878906 / 0x80370106**: “The virtual machine or container exited unexpectedly.” No sandbox ID or usable guest desktop was returned; the subsequent list was empty. The agent did not close a provisioned guest and did not repeat the start.
- At **17:22:23 Asia/Jakarta**, Windows Error Reporting event 1001 recorded `ContainerCrashDump`, P1 `59`, P2 `3221225477`, for `C:\ProgramData\Microsoft\Windows\Containers\Dumps\06968013-d9e1-412c-b786-67bcd9cc12c4.dmp`. Compute/Worker/VMMS Admin event logs explicitly require elevated rights; access was not bypassed. Local raw observations remain outside Git. Crash cause is unknown; no relationship with the separate AE DLL finding is inferred.
- Opened the supported Microsoft management console; Hyper-V Manager displayed the local host node but was elevated above the helper. No UI input was sent to this console. Its host selection is the precise handoff above.

Host observation: **Windows 11 Pro, 26H2, build 26300.9711**, Sandbox package 0.8.107.0. Registry ProductName retains “Windows 10 Pro”; the OS caption and build are recorded separately without treating that legacy registry string as a second OS. This is a new explicitly authorized provisioning attempt, not a rerun of the exhausted host-application startup investigation.

## Independent preparation completed

Official installers are staged at `C:\Temp\CutBridge-guest-setup-20261021-r1\installers`; none was executed on the host or guest:

| Vendor file | Bytes | SHA-256 |
| --- | --- | --- |
| blender-5.2.2-windows-x64.msi | 364822528 | `8dac2751ebe8e3867327eec52f1ef9b344c0a27499bb6221a301b4b35f2828d1` |
| ACCCx6_11_0_478_6.zip | 325658691 | `171563e44a92343e3ea5a6dc54df99843e3f477e7df22b1e34c2356e75f4edb8` |

Blender MSI Authenticode is **Valid**, signer **Blender Foundation**. Source: [official Blender 5.2 release directory](https://download.blender.org/release/Blender5.2/). Adobe's Windows 64-bit link on its [official direct-download page](https://helpx.adobe.com/download-install/apps/download-install-apps/creative-cloud-apps/download-creative-cloud-desktop-app-using-direct-links.html) provided the Creative Cloud 6.11.0.478.6 archive. Its 223 members were path/duplicate checked and fully extracted into `installers\AdobeCreativeCloud`; per-file hashes are retained. `Set-up.exe` Authenticode is **Valid**, signer **Adobe Inc.**, SHA-256 `1647412d83e4062f6378405ea67f032871fa59a3c97ec33a4f7c3365e43417f0`. This is the Creative Cloud installer, not an already installed After Effects build or an authenticated license. No Adobe sign-in or consent prompt was reached.

The current host `AfterFXLib.dll` was neither copied nor altered. Its existing HashMismatch observation and unknown cause remain in the prior preflight.

## Preserved qualification and release scope

Pre-provisioning documentation head: `cb11e2120bc63275f63c5f4baf64d2591fb7f8e2`.
Frozen runtime: `5aa2da24fc8be41626ee84178c7fdce05d02eebc`.
Exact existing packet: `C:\Temp\CutBridge-native-qualification-20261021\operator-handoff`.

AE ZIP remains bound to `5363795c66b1fbb664444fd5346ca9532d99822ce2cf3315193d4abec1789b9c`; Blender ZIP remains bound to `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe`. No package/runtime/implementation changes or redundant product checks were made. Completed automation, download inspection and authorized AI administrative review retain their existing exact identities.

Application installation, accepted vendor provenance, offline/credential/read-only/writable-output boundaries, blank startup, no-candidate probe, native installation/dock/layout/results/Build/QC/V001–V003/preservation/negative/source-replacement-rollback/fresh-process-reopen and screenshots remain **NOT_EXECUTED** in this attempted environment. The previous exact-package Blender scripted scope stays reusable as recorded; it is not expanded by setup.

No accepted candidate boundary exists yet. Do not map CutBridge into a networked preparation guest. When a guest becomes available, retain it while qualification is pending and preserve evidence through the dedicated output route. Complete permitted provisioning/account work separately, then independently establish the existing isolation controls before any candidate load.

Release remains held with authorization false. No promotion, tag, publication or distribution occurred. v0.2.4 remains immutable/held, production v0.2.3. Scope, deadline (Sunday 25 October 2026, Asia/Jakarta), deferred S14B and critical-defects-only stopping policy are unchanged.

