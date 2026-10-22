# Laptop fixture transfer receipt — 22 October 2026

**Verdict: INSUFFICIENT EVIDENCE. Transfer: VERIFIED_AND_STAGED_DATA_ONLY. Candidate execution: NOT_EXECUTED. Release: HOLD.**

Fetched live PR #114 and fast-forwarded from `f7acc7f8e0e67a5d5379527c35c84f2072a7f28f` to desktop transfer head `935ee764f7a93735f45502b996ce8a2948a4a4c1`. Preserved the owner's untracked extracted folder and ignored ZIP. Followed the [desktop transfer handoff](../20261022-pr114-desktop-fixture-transfer/README.md); no branch reset, rebase, unrelated-file overwrite, candidate execution or VM investigation occurred.

## Actual laptop verification and staging

- Located `CutBridge-PR114-retained-fixtures.zip` and the owner's extracted `CutBridge-PR114-retained-fixtures/` in `C:\Users\unn0w\Downloads\Management Project Testing\Cutbridge`.
- ZIP: **1,241,110 bytes**, SHA-256 **`d355a28913c12e7f65f9a8ddd126b62e1381c7ebdf92b36a2ef208ffb37f94b4`**. Rechecked after staging; unchanged.
- Pinned expected catalog: original f7acc7f [missing-fixtures.json](../20261022-pr114-laptop-direct/missing-fixtures.json), SHA-256 `98ffc2fd388ab1626785768ca88a4e49bef83bef51ac7a70254fea0b21e3ecf5`.
- Inspected all **40 ZIP members** before extraction: exactly the 39 expected fixture paths plus `transfer-manifest.json`. Rejected absolute/traversing/backslash/colon, duplicate, unexpected, directory, link and nonregular entries. Checked filesystem ancestors for reparse points. Extracted as data to a new unique external directory; its actual path is in [the laptop receipt](laptop-receipt.json).
- All **39/39 files**, **9,235,554 bytes** total, match expected size and SHA-256 in both fresh archive extraction and the owner's existing extraction. Both transfer manifests match desktop hash `d42c79b5740104f28975e5a81dd60b9d217a397396aeaee9f4b872adf6a98eb7`.
- Preflighted every destination before copying. Added **39 new files** to `C:\Temp\CutBridge-laptop-qualification-20261022\operator-handoff\real-blender-input`, using create-without-overwrite copies. **Zero conflicts, zero overwrites.** No file was regenerated.
- Rechecked all staged fixture sizes/hashes and all **24 existing packet files** after copying; original entries are unchanged. Rechecked both fixture sources; unchanged. Source ZIP and owner's extraction remain in place.

[Before inventory](packet-before.json), [after inventory](packet-after.json), and [per-file verification/actions](fixture-verification.json) retain actual laptop results. ZIPs, manifests/renders used as fixtures and package bytes remain outside Git; only documentary receipts/catalogs are committed.

The packet now contains **63/73 exact historical entries**, including **53/53 retained harness/fixture inputs**. The [10 missing historical root/review metadata entries](missing-historical-metadata.json) are explicitly accounted for. They include old environment/installation/candidate receipts and the old operator handoff. They were not copied from desktop metadata or fabricated. This new laptop receipt describes transport and staging only; it does not fill an environment-acceptance or installation-acceptance form. Existing old receipts and the original missing-fixtures catalog remain historical, unchanged records.

Two initial verifier invocation errors occurred before extraction or packet writes: JavaScript rejected an unescaped template delimiter, then PowerShell rejected an unsupported Split-Path parameter combination. Corrected the trusted data-only orchestration and completed verification; neither error executed candidate code or changed packet inputs. No failed candidate run or product test result is inferred.

## Remaining prerequisite and smallest next operator action

**Fixture transport is closed. Do not launch CutBridge.** Supply a concrete non-VM execution configuration for review/acceptance: execution identity with enforced denial of owner HOME/credentials/private files, effective outbound network denial, read-only exact inputs, confined writable output/temp/profile/cache paths, and the host-side watchdog. A second account or redirected profile alone does not establish those controls. The smallest next operator action is to provide that actual configuration and its control evidence for acceptance; protected consent/sign-in remains with the owner.

AE provenance remains separately unaccepted: the prior laptop `AfterFXLib.dll` HashMismatch is unresolved, cause unknown. No signature recheck, application launch, repair, security/licensing change or reboot was performed for this data transfer. Prior blank application startup/graphics/normal-exit observations retain their original scope. No further Hyper-V, VMware or Sandbox investigation is an action item.

Frozen tested runtime stays **`5aa2da24fc8be41626ee84178c7fdce05d02eebc`**, candidate version **0.2.5**. Exact AE/Blender packages and completed automated/AI-review evidence are preserved. Native CutBridge tests remain NOT_EXECUTED, root release authorization remains false, v0.2.4 remains immutable/held and production remains v0.2.3. No promotion, tag, publication or distribution occurred.
