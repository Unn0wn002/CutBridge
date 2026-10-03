# Native Blender evidence: 3f323e1

Candidate: `3f323e1ed8c38a44affb432420f6428bb6d57677`. Blender ZIP SHA-256: `b221a759208cfd81e22218db20709f0341a4dc931ab7f0c623f74e6bc87986f6`.

The scripted native scope passed in Blender **5.2.2 LTS**, with its GUI event loop active, inside an offline Windows Sandbox. Read-only candidate inputs and application binaries were mapped separately from writable evidence. Owner home and credentials were absent; network and input-write probes failed as expected. Input manifests before and after are identical (SHA-256 `e2e7047a66394443e17646b8df0dc8790909eef762992c0de5637ae944b18aa9`). Blender exited normally with code 0.

The campaign enabled the exact unpacked candidate, validated and built V001/V002/V003, rendered 36 real Beauty/Line/Shadow/Depth outputs, produced perspective Camera/marked Empty data, preserved artist compositor nodes, rejected same-version overwrites without changing payloads, preserved identities across language changes, and confirmed startup update scheduling stayed disabled. The synthetic fixture hash and per-package manifest hashes are in `native-blender.json`; generated blend files and image sequences remain local verification outputs.

This is **historical SHA-bound evidence**, not approval of a later candidate. It exposed a stale `HANDOFF_PRODUCER_ONLY` message falsely saying AE cannot reconstruct camera/null layers; the subsequent source correction requires fresh verification.

Visual panel inspection, extension-manager installation, AE execution, full output-mapping rollback, manual live updates, and representative Japanese artist validation were **not executed**. This partial native scope does not satisfy all release gates. Overall release readiness remains **INSUFFICIENT EVIDENCE**.

Retained files include the harness and launcher, native report and log, normal-exit record, isolation probe, and matching input manifests. No generated release ZIP or project/media file is committed.
