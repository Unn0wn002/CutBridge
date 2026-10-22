# Desktop fixture transfer for laptop qualification — 22 October 2026

**Verdict: INSUFFICIENT EVIDENCE. Native status: NOT_EXECUTED. Release: HOLD.**

The desktop fetched and fast-forwarded the existing PR branch to laptop commit `f7acc7f8e0e67a5d5379527c35c84f2072a7f28f`. Its 13 committed evidence checksums verify; push CI 39764355950 and PR CI 39764360727 succeeded. This is review of retained laptop evidence, not a repeat of laptop host execution.

The laptop's blank Blender 5.2.3 / e13b728c6880 and AE 26.5.0 Build 89 startup/exit-0 observations retain their documented scope. Non-VM credential/filesystem/network/input/write confinement is not proven. AE core DLL HashMismatch remains unresolved, cause UNKNOWN; successful startup does not resolve provenance. No VM investigation, security/licensing change, host repair, reboot, candidate script, product test or native campaign was performed here.

## Completed independent fixture preparation

All **39** files named by the laptop's [missing-fixtures catalog](../20261022-pr114-laptop-direct/missing-fixtures.json) exist in the retained desktop packet, with exact expected size and SHA-256: three V001–V003 manifests and 36 PNG/EXR renders, **9,235,554 bytes**. No file was regenerated or modified.

These files complete the 53 retained harness/fixture inputs when combined with the 14 already recovered. They do not supply the 10 historical root/review metadata entries or establish a current laptop environment receipt.

The new data-only ZIP contains those exact relative paths plus `transfer-manifest.json`: **40 entries**, **1,241,110 bytes**. Each of the 39 compressed fixture members was read back and its decompressed SHA-256 verified against the laptop catalog. All 39 original source hashes were checked again after packaging and still match. This is archive/data verification, not native acceptance.

- Desktop ZIP: `C:\Temp\CutBridge-laptop-fixture-transfer-20261022\CutBridge-PR114-retained-fixtures.zip`
- SHA-256: **`d355a28913c12e7f65f9a8ddd126b62e1381c7ebdf92b36a2ef208ffb37f94b4`**
- Adjacent `SHA256SUMS.txt` and `transfer-manifest.json` are retained locally.
- [The transfer receipt](transfer-receipt.json) records scope and bindings. ZIP and render bytes stay outside Git.
- Delivery to the laptop and laptop-side verification are **NOT_OBSERVED**. No connected upload capability or laptop file access is established in this desktop session; no alternate account, public release asset or credential extraction was used.

## Exact next operator action

Copy the single ZIP above to the laptop using your normal permitted file-transfer method, for example to `C:\Temp\CutBridge-laptop-qualification-20261022\CutBridge-PR114-retained-fixtures.zip`. Keep the original ZIP on the desktop.

Then give Codex on the laptop this instruction:

> Fetch current PR #114, preserve local work, and read docs/evidence/20261022-pr114-desktop-fixture-transfer/README.md. Verify the copied ZIP's exact SHA-256 above. Inspect its members as data, reject absolute/traversing/link paths, and stage into a fresh directory. Cross-check all 39 fixture hashes/sizes against the immutable f7acc7f missing-fixtures catalog before adding them to operator-handoff/real-blender-input. Preserve the existing 24 recovered entries; stop on conflicting bytes rather than overwrite. Reconcile the resulting packet against its retained catalog: 24 recovered entries plus these 39 fixtures gives 63/73 exact historical entries. The 10 root/review metadata entries are not in this ZIP and must be accounted for separately; create honest current laptop receipts instead of relabeling desktop environment metadata. Record transport and the actual laptop receipt without fabricating delivery, signatures, isolation or native execution. Continue only the already authorized direct-host work within the documented boundaries; no Hyper-V, VMware or Sandbox investigation.

Fixture delivery does not establish the execution boundary or clear AE provenance. Do not load CutBridge until both are accepted. A new non-VM restricted execution arrangement or normal vendor provisioning must be concrete and reviewable before requesting protected owner steps; it must not be assumed safe merely because a second account exists.

Frozen runtime: **`5aa2da24fc8be41626ee84178c7fdce05d02eebc`**.
AE ZIP: `5363795c66b1fbb664444fd5346ca9532d99822ce2cf3315193d4abec1789b9c`.
Blender ZIP: `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe`.

All implementation/packages, #113/#112 ancestry, completed automated checks, AI administrative review and historical unsuccessful observations remain preserved. No new qualified release or download exists. v0.2.4 remains immutable/held; production remains v0.2.3.

