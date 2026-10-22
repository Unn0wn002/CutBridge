# AE host availability probe

The installed After Effects 2026 application binaries were mapped read-only into an offline Windows Sandbox, with only isolated probe input and writable evidence exposed. Owner home, credentials, and Adobe license files were not mapped. The launcher checked input immutability and network isolation before invoking `AfterFX.exe -m -r C:\Inputs\probe.jsx`.

The probe script was intended only to record `app.version` and quit. It did **not execute**; no host-version output was produced. The launched process returned, but no usable exit code or diagnostic log was captured. The cause of unavailable AE script execution is undetermined; this does not establish a licensing error or a CutBridge defect.

Candidate AE runtime execution: **NOT_EXECUTED**. Native AE verification verdict: **INSUFFICIENT EVIDENCE**. A functioning licensed AE host inside an approved isolated environment is still required for the exact-artifact install, Build/QC, revision, artist-state, and persistence campaign.
