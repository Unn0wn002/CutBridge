# CutBridge submission and demo checklist

Working target: **22 October 2026**. The official submission deadline and evaluator-specific delivery requirements remain **unconfirmed**. This checklist prepares a reviewable v0.2.5 packet and demonstration using the existing [release checklist](RELEASE_CHECKLIST.md), [verification commands](CONTRIBUTING.md) and [S12 host procedure](S12_E2E_VALIDATION.md); it adds no parallel test command or publication path.

Current assessment, 16 October 2026: **INSUFFICIENT EVIDENCE**. Exact code `5293cd46a819debfe8ecf41f740c4e94806dd89c` has isolated Windows automated and ordinary Linux CI evidence plus bounded native Blender 5.2.2 scripted V001–V003/render/preservation/rollback/fresh-process-reopen results. Current native AE is **PENDING**. Trusted Linux verifier execution/review, applicable visual/manual checks and scope acceptance remain open; see [current preparation](RELEASE_PREPARATION_v0.2.5.md) for counts, exact hashes and exclusions. Historical `fef1023`/`049c095` isolation provenance is still incomplete. S14B is NOT_EXECUTED.

## Readiness decisions

| Decision | Evidence required | Current boundary |
| --- | --- | --- |
| Submission packet | Exact candidate and trusted verifier identities; required automated/native evidence for demonstrated scope; reproducible ZIPs/checksums/metadata; installation instructions; limitations and demo | Current scoped automated/Blender results recorded; AE, trusted Linux verifier/review and applicable manual acceptance pending. Unconfirmed deadline/delivery rules remain explicit. Candidate files remain unpublished. |
| Public release | All applicable release gates, independent review, protected promotion, explicit owner authorization for exact current-main/tag/channel/prerelease, guarded publication and independently verified downloads | Not authorized. `release-authorization.json` stays false. |
| Production distribution | Approved published artifacts, independent download verification, official Blender index generation and deployed install/update/no-downgrade checks | Held on v0.2.3. Published v0.2.4 remains immutable and is not mirrored because of Issue #99. |

Submission preparation does not authorize an external submission, protected merge, authorization change, tag, publication or distribution. No representative Japanese-user validation or broad production-usability claim is made.

## Freeze and retain the packet

- [ ] Record branch, exact candidate SHA, fetched base SHA, true merge-base, changed paths and candidate diff; resolve each review against current code and mark superseded findings with code evidence.
- [ ] Independently review the verifier outside candidate-controlled refs. Retain its immutable SHA, dependency-image/toolchain identities, exact snapshot inventory/modes/bytes and source manifests. Confirm no owner credentials, no network, read-only inputs and explicit writable output/temp paths before executing candidate commands.
- [ ] Run every required command from CONTRIBUTING and relevant existing regressions. Retain command lines, exit codes, complete logs, CI run/head identity, before/after input manifests and a single verdict for each verification run. Missing hosts/dependencies/isolation are INSUFFICIENT EVIDENCE; input mutation is INVALID.
- [ ] Build twice through `tools/build_release.py` in fresh output directories inside isolation. Compare complete inventories and bytes for both ZIPs, `SHA256SUMS.txt` and `release-metadata.json`; retain all four files from each build outside Git. Independently recompute hashes and inspect archive paths, required runtime files, license, versions and the tag-pinned AE guide.
- [ ] Record snapshot ID/SHA and SHA-256 for both ZIPs, checksum file, metadata, test fixtures, Blender packages, native harnesses and retained evidence inputs. Record OS/build, Blender version/build hash, AE version/build, installation method and host binary identity. Do not infer Blender 5.2.1 native behavior from a 5.2.2 run.
- [ ] Retain the actual Sandbox/VM policy and runtime settings, disabled-network state, complete read-only mounts, writable paths and credential-isolation evidence. Set PYTHONPYCACHEPREFIX, TEMP, TMP and TMPDIR to approved output paths. Manifests supplement this boundary; they do not establish it.
- [ ] Include both ZIPs, checksums, metadata, source SHA/diff, installation directions, a verification summary with blockers, limitations and the demo sequence. Keep generated ZIPs, rendered footage, native projects and private assets out of Git. Preserve logs before Actions artifact expiry.

Historical evidence may only be reused for demonstrated equivalence: compare exact runtime-file/fixture/harness bytes, toolchain and host/build, describe excluded changes and limit the reused scope. A guide-only ZIP change still requires inspection of that exact packaged guide and current installation sign-off. Runtime changes invalidate any blanket claim that old native results accept the new candidate.

## Native execution sheet

Use synthetic/disposable copies. The table defines execution requirements; it does not mark every check complete. Record exact inputs/scope and evidence for each executed check, distinguishing the current scripted Blender results from pending visual/manual and AE work. Retain screenshots where they establish UI behavior and scalar/state logs for API-checkable outcomes. A checklist or prerecorded historical demo is not execution evidence.

| Check | Required observation |
| --- | --- |
| Blender installation and UI | Install the exact ZIP through the actual supported install path, enable it, inspect normal/narrow N-panel in Japanese and English, save/reopen preferences as applicable; no stale install is silently reused. |
| Blender package/render | Save a synthetic cut; Validate → Build → real Render Animation with normal panel active. Produce V001/V002/V003 and expected nonzero frame counts for the claimed pass/format combinations; all render paths stay within approved output. |
| Blender safety/rollback | Same-version payload overwrite refused; mismatch and unsupported pass/camera cases fail closed; injected mapping failure restores compositor/artist nodes and original frame/state. Include applicable 4.2/4.5 legacy-path checks without claiming full-host coverage from a focused probe. |
| AE installation | Verify exact-ZIP hashes and four adjacent runtime files; launch through Run Script File and, if claimed, dockable ScriptUI installation/restart. Confirm JP/EN UI; test localization-only fallback separately in a disposable runtime copy. Missing safety sidecars fail closed. |
| Cross-host baseline | Import the actual rendered Blender V001 package; Build/QC, expected sequence paths/FPS/frame range/comp dimensions, repeat Build with stable managed counts and no artist-object adoption. |
| Revision chain | Use actual V001 → V002 → V003 packages; observe source paths and current ownership after each revision, Build/QC and panel reload. Reuse the cached panel/manager across the chain to exercise live-state lookup. |
| Preservation | Compare before/after effects and mask values, transforms, parent IDs, in/out/start times, time stretch, layer order/IDs, expressions/keys, flags, artist layers, unrelated footage/comps/folders and studio/package-root notes. Managed Camera/Null channels are intentionally refreshed; preserve unrelated artist state. |
| Optional/pass policy | Required↔optional status change shows explicit warning/confirmation. Complete optional layer absent and optional sequence absent remain warning/skip only. Added pass, required removal and optional removal reject before import/source/tag mutation. |
| Negative ownership/contract | Missing and separately de-tagged required layer, missing/duplicate/moved deterministic folders, unmanaged same-name collision, invalid manifest/path, FPS/frame-range/pixel-aspect/resolution drift all fail closed without changing the original package/project. |
| Import/replace failure | Inject failure after import but before validation succeeds, and separately during source replacement. Captured imported IDs are removed even after native handles become invalid; previous sources, metadata/root notes and unrelated objects survive rollback. Record object inventories and reload/Build/QC recovery. |
| Camera/Null subset, if shown | Compare manifest samples with Camera Position/Point of Interest/Zoom and Null Position/Scale values/times, ownership and counts after Build/revisions. Check projection with an explicit fixture if projection is claimed. QC alone cannot validate these values, expected completeness or projection. Do not demonstrate camera roll or Empty rotation as supported. |
| Reopen and exit | Save revised project, close/reopen within process, reload panel, Build/QC and compare preserved state. Then close AE normally, record actual exit, relaunch a fresh process, reopen the saved project and repeat checks. Save/reopen Blender where in scope; record normal exit. |

## Demonstration sequence

1. Show the candidate SHA, host/builds, ZIP hashes and actual executed scope. State “working target 22 October; official deadline unconfirmed,” unpublished status and S14B NOT_EXECUTED.
2. Show Blender's metadata, preset/pass selection and Validate result. Build V001, render the short synthetic cut, inspect the manifest and complete pass sequences.
3. Launch AE from the exact package, load V001, Build, show managed comp/sequence setup, QC result and one artist-added layer/effect/root note used as preservation sentinels.
4. Apply V002 then V003. Show updated sources alongside unchanged artist sentinels and managed counts; run Build/QC after panel reload.
5. Show a supported required/optional status warning and an overwrite/incompatible-revision refusal in disposable copies. Show before/after state establishing no unintended mutation.
6. If 3D is included, state the implemented channel list and inspect those channels directly. Explain that Camera roll, Empty rotation, full-scene sync and 3D transform/projection QC are outside scope. Keep the normal 2D handoff as the primary path.
7. Save, quit normally, reopen in a fresh AE process, reload CutBridge and repeat Build/QC. End with the limitations, evidence verdict and remaining blockers rather than a broad production-readiness claim.

The spoken demonstration can use a short subset; the complete native execution sheet remains required for the corresponding release claims. Never fill missing native results or participant feedback with simulated outcomes.
