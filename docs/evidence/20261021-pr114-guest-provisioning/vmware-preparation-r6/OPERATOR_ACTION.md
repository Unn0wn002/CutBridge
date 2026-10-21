# VMware route preparation — official installer boundary

**Verdict: INSUFFICIENT EVIDENCE.** The owner authorized preparing a separate VMware Workstation Pro route, then explicitly chose **“I prefer not to create an account.”** Registration was left untouched. No VMware installer has been downloaded, selected, executed or installed.

## Smallest remaining operator action

Provide the **local path to an already obtained official VMware Workstation Pro Windows x64 installer**, if one is available. The agent must verify its actual version, vendor signature and SHA-256 before execution and stop at installation consent, a required host reboot or security change. An official 26H1 release is documented, but no exact installer filename/build is invented or selected here.

The currently attempted official download route is unavailable without an account, which the owner declined. No further account-creation or repeated sign-in request is made. No purchase, unofficial mirror, guessed CDN URL, credential extraction or protected-download bypass is proposed.

## Exact completed preparation

- **Microsoft Edge** was used, selected browser ID `4`. [Broadcom's official download guide](https://knowledge.broadcom.com/external/article/368667/download-and-license-free-vmware-desktop.html) linked to the Workstation Pro free-download listing, which redirected to **Broadcom Inc. Customer sign-in**, `https://access.broadcom.com/default/ui/v1/signin/`. No username/password was entered or submitted.
- After the owner reported no account, the official portal's **Register** link opened `https://profile.broadcom.com/web/registration`. Its Email Address/CAPTCHA form was observed empty. No CAPTCHA, verification, password, personal-information form or terms acceptance was completed. The owner then declined account creation. Raw blank sign-in/registration screenshots are retained locally with hashes in `vmware-download-preflight.json`.
- A bounded official public-package-catalog check was also completed: `winget show --id VMware.WorkstationPro --exact --source winget --disable-interactivity` returned exit 1 / no package; `winget search VMware --source winget --disable-interactivity` returned exit 0 and no Workstation package. A matching GitHub manifest path returned 404. These observations do not prove that every possible official distribution route is absent. No installer or source agreement was accepted through these commands.
- Host inventory: Windows 11 Pro `10.0.26300`, AMD Ryzen 7 8700F (8 cores / 16 logical processors), NVIDIA GeForce RTX 5060 Ti. Exact Workstation-build/host compatibility remains unestablished.
- VMware's public product page advertises DirectX 11 / OpenGL 4.3 guest graphics. This supports considering a graphics preflight; it does not prove actual Blender/AE startup on this PC. The official [26H1 announcement](https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26h1/) was readable; its release-notes link returned HTTP 403 to the web reader. No protected document or download was bypassed.
- **Windows media is verified:** `C:\Users\unn0w\Downloads\Windows11_Client_x64_en-us_26300_9457.iso`, **9,047,330,816 bytes**, SHA-256 **`bd4307df32bc8af33b39ccecb1174aeb345386630f89a2b86c7a4e36b55ea650`**, matching Microsoft's generated English x64 checksum retained in `quick-create-r4/installation-media-required.json`. This was a data-only hash check; no mount or installation occurred. It does not bind the existing guest's installed OS.
- No new hypervisor, VM conversion, new guest, shared-folder/credential mapping, passthrough script, DLL copy, security/licensing change or host reboot was performed.

## Existing guest and release scope preserved

Preserve **AI Native Test** and its applications. Its Microsoft Hyper-V Video/OpenGL blocker and incomplete AE inspection remain as recorded in `guest-inspection-r5`. The AE **Continue with known issues** warning was left open at the owner's request. The native GPU/passthrough limitation was not worked around. The historical host Adobe DLL **HashMismatch** retains unknown cause and was neither copied nor repaired.

Frozen runtime: **`5aa2da24fc8be41626ee84178c7fdce05d02eebc`**. Pre-checkpoint documentation head: `36c15890ce613c46203f30e842dae31f33914427`; push/PR CI succeeded. AE ZIP remains `5363795c66b1fbb664444fd5346ca9532d99822ce2cf3315193d4abec1789b9c`; Blender ZIP remains `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe`. Exact native packet: `C:\Temp\CutBridge-native-qualification-20261021\operator-handoff`.

Implementation, packages, #113/#112 ancestry, completed automation/download inspection and AI administrative review are unchanged. No additional product-test rerun was justified. Actual guest setup observations are not native candidate passes or qualified-build screenshots.

Official installer retrieval/signature inspection, permitted installation, exact app/OS provenance, graphics-capable blank startup, offline/credential/read-only/writable-output boundaries, watchdog and no-candidate probe all precede candidate execution. All still-open native acceptance cases remain **NOT_EXECUTED**. No candidate was mapped or executed by the agent. Root release authorization remains false; no protected promotion/tag/publication/distribution occurred. Immutable held v0.2.4 and production v0.2.3 are untouched.
