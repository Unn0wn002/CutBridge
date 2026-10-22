# VMware guest graphics checkpoint — 22 October 2026

**Verdict: INSUFFICIENT EVIDENCE.** The owner installed Windows and Blender in **AI Native Test - VMware**. The agent observed the running desktop and existing Blender **OpenGL 4.3 or higher required** dialog. This is a blank application startup blocker, without CutBridge execution or an observed CutBridge defect. Exact guest Windows/Blender builds and display-driver version remain unverified.

## Smallest current operator action

Press Ctrl+Alt to release guest input and open VMware’s **VM** menu. If it offers **Install VMware Tools**, complete its normal guest installer and restart **only the guest**. If it offers **Reinstall VMware Tools**, leave that unclicked and report it so the installed display driver is inspected first. Leave the guest open afterward. No host reboot, host driver/security change, DLL replacement, or another virtualization facility is requested.

The agent’s supported coordinate, accessible-menu and keyboard inputs produced no visible menu. The owner reported completing the manual menu action, but the menu was not visible after returning to the console. No additional equivalent input loop or unsupported automation was attempted. [Broadcom’s official instructions](https://knowledge.broadcom.com/external/article/315363/install-vmware-tools-in-vmware-products.html) describe mounting Tools through the VM menu and installing from the guest CD-ROM.

## Observed evidence and its limits

The saved hardware had 16 GB RAM, four virtual cores, a 200 GB growing disk, TPM and Accelerate 3D checked. VMware then explicitly required a Tools update for 3D. The vendor vmware.log at startup 06:30:30 UTC records **3d enabled**, Tools legacy version **0** and **noTools / install possible**. Later Tools heartbeats exist; the startup record does not establish the current guest display driver. Neither a checked 3D option nor a heartbeat proves OpenGL 4.3 support.

[The checkpoint](graphics-checkpoint.json) identifies the actual error screenshot retained outside Git and its SHA256. No new Blender launch was triggered by the agent, no AE launch occurred in this guest, and no candidate package was loaded. The original r9 creation/encryption/hardware records remain historical and unchanged.

Frozen runtime `5aa2da24fc8be41626ee84178c7fdce05d02eebc`, AE ZIP `5363795c66b1fbb664444fd5346ca9532d99822ce2cf3315193d4abec1789b9c`, Blender ZIP `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe`. Completed checks/packages/review and #113/#112 ancestry are preserved. Documentation head `8c35974` passed push CI 39734402104 and PR CI 39734406023.

Vendor provenance/inventories, blank startup, no-candidate probe, effective offline/credential/read-only/output/temp/watchdog boundaries and all outstanding native acceptance remain required. Native cases remain NOT_EXECUTED; release remains held, v0.2.4 immutable and production v0.2.3. Historical host Adobe HashMismatch cause remains UNKNOWN; no Sandbox retry or host security/licensing change.
