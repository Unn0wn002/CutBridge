# AE availability retry with runtime dependencies

This availability-only probe exposed the After Effects 2026 application binaries read-only inside offline Windows Sandbox, together with read-only Microsoft runtime DLLs. Their valid Microsoft signatures, versions, and SHA-256 identities are retained in `dependency-record.json`. Owner home, credentials, and Adobe license files were not exposed. The launcher checked disabled network and immutable inputs. Input manifests before/after match.

Command: `AfterFX.com -m -r C:\Inputs\probe.jsx`. The script would only write `app.version` and quit; it did **not execute**. The process did not exit within the 90-second limit. The disposable VM then shut down; no normal AE exit is claimed. Captured application events did not establish the cause. This retry does not prove a licensing fault, missing DLL, or CutBridge runtime defect.

Candidate AE runtime: **NOT_EXECUTED**. AE native verification: **INSUFFICIENT EVIDENCE**. Use a functioning licensed isolated AE host for the existing [S12 campaign](../../../S12_E2E_VALIDATION.md) and [release checklist](../../../RELEASE_CHECKLIST.md); do not replace those gates with this availability probe.

The exact candidate AE ZIP remains SHA-256 `c15b4fb6ce4891a84f205b0658a5b9bbdb8874828a99140aacdd620a9439ec6e`. Its adjacent runtime files, release-neutral guide, and automated suites are verified; native installation, Build/QC, Camera/Null reconstruction, V001→V002→V003, artist-state preservation, negative cases, and save/close/reopen still need actual host evidence. Japanese representative-user validation is unexecuted.
