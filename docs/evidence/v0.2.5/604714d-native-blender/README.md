# Revised native Blender evidence: 604714d

Candidate: `604714d93627a870326a75564eba0af46e5ee957`. Blender ZIP SHA-256: `3a53f7af8420909e5ed300440df115dffef2ba1dd196688c7c99789a8a48aa48`.

The fresh scripted campaign passed in **Blender 5.2.2 LTS**, using its native GUI event loop inside offline Windows Sandbox. Candidate source and application binaries were read-only; writable outputs were separate; owner home/credentials and network were unavailable. Before/after input manifests are identical. The launcher rechecked isolation and Blender exited normally with code 0.

The campaign verified the corrected bounded handoff warning and guidance, enabled the exact candidate, built V001/V002/V003, rendered 36 real mixed PNG/OpenEXR four-pass outputs under a Japanese directory path, produced Camera/marked Empty metadata, preserved artist compositor nodes, blocked same-version overwrites while preserving payload hashes, preserved package identity across language changes, and confirmed startup update scheduling remained disabled. The report retains per-package manifest hashes and the synthetic fixture SHA-256.

Visual UI inspection, extension-manager installation, full output-mapping rollback, manual live update detection, AE execution, and representative Japanese artist validation remain **NOT_EXECUTED**. Scripted native scope passed; overall release readiness remains **INSUFFICIENT EVIDENCE**.

Generated blend/media files and candidate ZIPs remain local verification outputs. Retained report, logs, harness, launcher, and matching input manifests bind this partial native result to this exact candidate.
