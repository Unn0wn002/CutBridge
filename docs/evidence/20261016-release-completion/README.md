# Release-completion evidence — 16 October 2026

Overall verdict: **INSUFFICIENT EVIDENCE**. This directory retains reviewable automated/native observations and unsuccessful attempts separately. The working submission target is 22 October; the official deadline is unconfirmed. Public release is not authorized and production remains v0.2.3.

`verification.json` binds the verified engineering baseline `a44792099b3b5f5b7a2f69a41061268fe59586b3` to exact artifacts, toolchains, reviewed orchestration, host builds and scope. `REVIEW_TRIAGE.md` covers all 22 unresolved PR #112 threads and superseded PR #103 findings. `review-threads.json` preserves the original connector responses. Thread states were not changed.

| Record | Verdict and scope |
| --- | --- |
| `trusted-linux/passed-r2/` | PASS: independently reviewed tools `a6ee244`, bootstrap `8d1ecef`, candidate `a447920`; 395 tests + 2 subtests, RNA, 18 Node suites, packaging, immutable input inventories, stopped-container staging/upload. Downloaded archive hash and all 48 inner evidence checksums verified. |
| `trusted-linux/attempt-r1/` | FAIL retained: four negative tests could not mutate read-only copies inside approved TEMP. The subsequent fixture-only fix left real inputs read-only. |
| `automated/`, `checks-r3/` | PASS for earlier Windows `5293cd4`: 390 tests, 2 platform skips + 2 subtests, RNA, all 18 Node suites and repeat packaging. |
| `windows-latest-attempt/` | INSUFFICIENT EVIDENCE: Application Control blocked a dependency DLL before candidate commands. |
| `native-blender/` | PASS only for recorded exact-ZIP scripted Blender 5.2.2 build `d13f752e3b9c` V001–V003, 36 outputs, preservation/negative/rollback and separate-process reopen scope; actual process exits 0. |
| `native-ae/` | INSUFFICIENT EVIDENCE: first harness scope error before assertions; subsequent startup failures, including actual AE exit `0xc0e90002` with both graphics settings. Corrected harness retained; no current native assertions or normal-exit/reopen acceptance. |
| `native-blender-visual/` | INSUFFICIENT EVIDENCE: validator startup exited `0xc0e90002` before visual harness. First launcher parse-error attempt also retained. |
| `attempts/` | Earlier infrastructure limitations and actual verifier regression failure retained without replacing their verdicts. |

One retained command-record limitation in the passing r2 helper is explicit: reusing the Docker-create argument list changed its first recorded command to `--checks`. The actual `preflight-isolation.json` proves `--preflight` ran, and its separate container exited 0. A subsequent copy-at-recording fix and main-path regression preserve exact invocation arguments; raw r2 records are unchanged. The independently reviewed corrected helper is `571f4cdb1c992124bdb35e3d089de1de1535b254`.

Complete source archives, binary diffs, downloaded Actions archives, repeated package directories and synthetic native fixtures remain outside Git. `retained-inputs.json` names their local locations and hashes. The unpublished packet is `dist/release-candidate-20261016/`. The final documentation/evidence head is checked separately after committing; its exact SHA, Actions run and downloaded-artifact hashes belong in the packet's `FINAL_HEAD_VERIFICATION.json` and the draft PR. Earlier baseline counts are not reassigned to that head.

Raw retained records preserve their original CRLF/LF and whitespace bytes under the existing `-text` evidence attribute. Source whitespace checks exclude these byte-preserved records; their integrity is checked by SHA-256 inventories rather than rewriting logs to satisfy whitespace formatting.

The two ZIPs match between Windows and Linux. Metadata/checksum text has platform CRLF/LF differences; each toolchain's two complete four-asset builds is byte-identical. Primary packet text files use Linux bytes. No native AE, installer/button/UI, manual-update, broad host compatibility, representative-user result or S14B completion is inferred. No security/authorization settings, protected refs, published releases or production distribution were changed.
