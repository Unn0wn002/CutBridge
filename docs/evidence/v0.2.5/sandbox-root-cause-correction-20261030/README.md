# Correction: Windows Sandbox crash root cause - 2026-10-30 (WIB)

Corrects one statement in `../sandbox-verification-20261029/README.md`, which is left unedited. The verdict there (`PASS` for `a1113a7`) is unaffected.

## What the earlier README says

> Earlier the same day the Sandbox itself failed with 0x80370106 (guest bugcheck 0x3B after a virtual PCI protocol mismatch); the owner reset the Windows Sandbox feature and it now boots.

This implies the feature reset fixed the crash.

## What later evidence shows

- The likely cause is **GPU sharing (vGPU)**, not something the feature reset repaired. The virtual PCI mismatch in that bugcheck matches the virtual GPU device.
- Every config that booted on 2026-10-29 had `<vGPU>Disable</vGPU>`, including the CutBridge run 5 config (`sandbox-config-run5.wsb`, recorded in the earlier README as "vGPU disabled").
- The first AE Glyph kit config on 2026-10-29 had vGPU at the default (enabled) and crashed again with **0x80370106** after the feature reset. Setting `<vGPU>Disable</vGPU>` in that config let it boot and stay up (VM present 18 of 18 checks over 90 s), and it was used for the 2026-10-30 AE Glyph panel run.
- Morning configs that spelled the element `VGpu` likely had it ignored, which would explain why the crash appeared before the reset.

## Effect on the verification

None. Run 5 ran with vGPU disabled and inside the stated isolation boundary; the results, manifests and package checks stand as recorded. Only the explanation of why the Sandbox started booting changes.

## For future runs on this host

Keep `<vGPU>Disable</vGPU>` in every `.wsb` config. Whether the feature reset was needed at all is unknown; it was not undone to test.
