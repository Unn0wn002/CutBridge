# Quick Create gallery and Windows-media checkpoint — 21 October 2026

**Verdict: INSUFFICIENT EVIDENCE.** No guest, candidate execution, native pass or qualified CutBridge screenshot is claimed. Frozen runtime `5aa2da24fc8be41626ee84178c7fdce05d02eebc` and both verified release packages are unchanged. Pre-checkpoint documentation head is `8b09c434b3b5018f505275d741d204c56fdee80f`.

## Immediate operator action

In the already open **Create Virtual Machine** window, dismiss the floating menu and select **Windows 11 dev environment** on the left; leave **Create Virtual Machine** unclicked, then reply “done.” This is the current manual UI checkpoint. The image's actual details must be inspected before a guest creation/licensing decision.

The operator's prior actions are now observed: the consent window closed, and manually opening Quick Create produced `VMCreate.exe` window 723400. The gallery lists Windows 10 MSIX packaging, Ubuntu 18.04/20.04/22.04, Windows 11 dev environment and Local installation source. The current visible selection is Local installation source with creation disabled. A floating Hide menu/More actions/Send to Copilot/Copy/Search overlay obscures part of the dialog. One supported blank-area click and one Escape key action produced no visible change. No alternate input technology, privilege bypass or repeated standalone launch was used.

## Read-only official image inspection

Microsoft's default gallery redirected to:

`https://download.microsoft.com/download/5/f/5/5f5197e8-7a9a-49dd-bd81-5d4bfa27d6a9/en-us/GalleryHyperV.JSON`

The exact raw metadata SHA-256 is `372a93efc92e77d86c3f3cea1a2d59347ec67e388d879e8cbbce786d9422445a`. It is UTF-16 LE with BOM, retained in `official-gallery.raw`. An initial UTF-8 assumption was rejected by the JSON parser; a raw retrieval and BOM-aware reader then parsed it correctly. No executable data ran.

The Windows 11 entry is dated **25 July 2024**, advertises version **10.0.22621**, describes an evaluation copy with a predetermined expiry, and links `WinDev2407Eval.HyperV.zip`. Its description calls it “21H2,” which is retained as source wording, not adjudicated as the actual guest version. A read-only HEAD request returned HTTP 200 and 23,299,441,890 bytes. This establishes current URL availability only. It does **not** establish current evaluation validity, license acceptance, installed OS/build, normal boot or AE compatibility. No exact expiry is invented. The 23 GB image was not downloaded or used.

## Independent current Windows ISO preparation

Used the normal official [Microsoft Windows 11 download page](https://www.microsoft.com/en-us/software-download/windows11) in the already bound Chrome browser 3. Chose the x64 multi-edition ISO and English (United States). The page identified **Windows 11 2026 Update / 26H2** and generated:

- Label: Windows 11 Client — Build 26300.9457 English.
- Filename: `Windows11_Client_x64_en-us_26300_9457.iso`.
- Published English SHA-256: `bd4307df32bc8af33b39ccecb1174aeb345386630f89a2b86c7a4e36b55ea650`.
- Download host: `software.download.prss.microsoft.com`; generated link expiry `2026-10-22T11:20:38.17604Z`.

One normal download click produced **“This page has been blocked by Chrome” / ERR_BLOCKED_BY_CLIENT**. Its cause is unknown. No ISO was downloaded, mounted, installed or hash-verified. No installation assistant, media-creation executable, host upgrade or reboot was run. Browser protections/settings were not changed, and the blocked URL was not retried through another transport. The blocked tab is retained as a browser handoff. A usable permitted Windows installation source remains to be established if the gallery entry proves unsuitable.

Actual setup screenshots and records are retained under `C:\Temp\CutBridge-hyperv-quick-create-20261021-r2`; see `screenshot-receipts.json`. These are setup observations, not qualified-build screenshots. Raw unsuccessful decoding and earlier attempts remain separately preserved locally, without being relabeled as success.

## Preserved boundaries

The official signed Blender 5.2.2 and Creative Cloud installers remain staged at `C:\Temp\CutBridge-guest-setup-20261021-r1\installers`, unexecuted. The current host AE DLL was not copied or changed; its HashMismatch cause remains unknown. The failed Sandbox launch was not repeated.

Completed automated checks, exact package download verification and authorized AI administrative review are reused without expanding their scope. No implementation change, new product test, security/licensing setting change, Windows feature change or host restart occurred. All remaining native installation/Window-menu/dock/resize/EN-JA/results/Build-QC/revisions/preservation/negative/source-replacement-rollback/fresh-process-reopen cases remain NOT_EXECUTED.

No native guest boundary has been accepted. Keep candidate files unmapped during preparation; the existing offline/credential/read-only/writable-output rules must be established before candidate load. Release authorization remains false; no protected merge, tag, publication or distribution occurred. v0.2.4 remains immutable/held, production v0.2.3, and S14B remains deferred.

