# AE availability with software graphics and visual observation

This fresh offline Windows Sandbox disabled virtual GPU acceleration, exposed application binaries and signed Microsoft runtime dependencies read-only, and withheld owner home, credentials, and Adobe license files. Input manifests before/after match. Only the host-version probe was supplied; CutBridge runtime was not executed.

Native Windows visual inspection observed AE's startup screen at “Initializing MediaCore”, followed by a failed `mochashape64_ae_adobe.aex` plugin warning, “Could not load the Mocha module”, a missing-class warning, and “Invalid type conversion”. The warnings were acknowledged to observe subsequent startup state. The retained screenshot shows the actual invalid-type warning inside the sandbox; no host workspace screenshot is used as native evidence.

The version probe never executed, and the process did not exit within 180 seconds. The VM shut down at the limit; no normal AE exit is claimed. These observed host-initialization failures do not prove a CutBridge defect, a licensing fault, or a single root cause. A properly installed functioning licensed isolated AE environment remains required.

AE candidate native verdict: **INSUFFICIENT EVIDENCE**. No release gate or authorization is changed.
