# Exact-package native After Effects campaign (prepared; not executed)

Run only in the independently verified offline disposable Windows Sandbox. These files are retained verification inputs outside the repository; they are not a parallel project verification gate. They exercise the existing packaged public API and actual ScriptUI revision callback without editing runtime bytes.

## Boundary and dependencies

- Read-only map this folder to `C:/NativeAEInput` and retain its complete before/after SHA-256 inventory.
- Read-only map the installed AE 2026 `Support Files` directory to `C:/AfterEffects`. Do not map license stores, owner HOME, credentials, sockets, or network access. Set all temporary paths to the explicit writable output area.
- Read-only map reviewed candidate metadata to `C:/Review/candidate.json`, containing `sha` or `candidate_sha` with the exact 40-character candidate SHA.
- The launcher must record the sandbox settings, host/build/OS, process IDs, exact input hashes, script start/end/exit observations, and both source/input manifests. Missing output, initialization/activation failure, timeout, or native process crash is not a pass. Preserve `IN_PROGRESS` checkpoints and classify the infrastructure failure separately from an observed candidate assertion.
- Do not copy license files or owner credentials to make AE initialize. A host that cannot initialize this way is `INSUFFICIENT EVIDENCE`.

## Minimal availability probe first

Launch the read-only AE installation with `-m -r C:/NativeAEInput/probe.jsx`. It writes `C:/Evidence/verification-output/native-ae/availability.json`, reports exact AE version/build, then requests normal quit. It loads no CutBridge code. Expect `AVAILABLE`, not `PASS`: it proves only host script availability. If the report is absent, inspect the launcher/application logs and stop the dependent campaign as insufficient evidence.

## Installation and inputs

Before loading candidate code, the launcher must safely extract the exact built `CutBridge-AfterEffects-v0.2.5.zip` from `C:/Evidence/verification-output/dist-ci` into the configured output `ScriptUI Panels` directory. Require `CutBridge.jsx`, `revision_manager.js`, `qc_plus.js`, `localization.js`, `INSTALL.md`, and `LICENSE`; reject duplicate or unsafe archive paths and symlinks. Verify the ZIP against both checksums and release metadata and record every installed file's SHA-256 in `installation.json`, including the artifact SHA-256, exact candidate SHA, host/build, and extraction/installation method. The JSX refuses execution when this metadata or any runtime sidecar is absent. This is installation from the built package; GUI installer inspection is not claimed.

Edit the reviewed `config.json` before starting the sandbox if paths differ. `manifests` may contain the exact three V001/V002/V003 `cutbridge.json` paths. If empty, the harness recursively discovers these versions under `package_root`; duplicate versions are rejected as insufficient input. These packages must come from the separately evidenced real Blender campaign. No sample render files are invented by this harness. All three packages must have matching supported geometry, timing and pass sets; at least two passes; a required `BEAUTY`; and Camera/Null samples for the supported position/POI/zoom and position/scale channels.

## Phases

Run each file with `AfterFX.com -m -r C:/NativeAEInput/<phase>.jsx` using the sandbox launcher, and inspect the corresponding JSON before proceeding. Keep the actual AE window available for unavoidable initialization prompts, but do not supply credentials. The launcher controls process termination and must separately record process restarts.

1. `campaign.jsx` writes `campaign.json`, `artist-V001.aep` through `artist-V003.aep`, and `preservation-baseline.json`. It loads the exact installed `CutBridge.jsx`, uses real native Build/QC, performs V001 → V002 → V003 through the actual palette revision callback, repeats Build without duplicates, and checks concrete effects, mask shape/value, transforms, opacity keys/expression, parenting, timing, layer order, artist layer, unrelated folder/comp/solid, and root note. It inspects supported native Camera/Null samples separately from QC.
2. `negative.jsx` requires the saved V003. It tests deleted/de-tagged required layers; missing/duplicate managed folders across Build/revision/QC; incompatible FPS, required removal, addition and optional removal before confirmation/import/migration; supported required→optional status warning/confirmation; complete optional-layer absence; and missing optional source warning/skip. It creates labeled manifest/sequence fixture derivatives only under output and records their original Blender package input. Each blocked operation compares the native project before/after.
3. `rollback.jsx` requires the saved V003. It temporarily wraps the public JavaScript `CutBridgeContract.footageReuseErrors` seam to force an ordinary verification failure after actual native import allocation/tracking. It captures the real numeric native footage ID before removal, requires the ID absent and native `isValid(handle) === false` after cleanup, verifies original project and artist values preserved, restores the seam in `finally`, then checks Build/QC. It separately removes actual cached native footage/layer handles, establishes their invalidity, and verifies safe live rediscovery without duplicates. Installed runtime bytes remain unchanged; the fault injection is explicitly reported.
4. `reopen.jsx` requires the saved V003 and baseline. Run after closing the test project and preferably restarting AE; the report explicitly distinguishes project close/open from launcher-proven process restart. Reloads exact installed runtime, opens V003, checks concrete artist values, supported Camera/Null samples, repeated Build/QC and no duplicates, then saves `reopened-V003.aep`.

Report `PASS` only for a completed phase whose actual native checks all passed. The harness writes `IN_PROGRESS` before checks and flushes after each observation. It never promotes an unexecuted phase. Review all four reports and launcher records; no single phase is full release readiness. Native visual inspection, general AE 2024–2026 compatibility, representative-user usability, publication authorization and S14B are outside these scripted results and remain explicitly unexecuted.

If the exact native `File.openDialog` function cannot be temporarily intercepted or the real palette cannot be located, revision phases return `INSUFFICIENT EVIDENCE` instead of replacing the packaged runtime or manufacturing a native result. A manual UI campaign may then use the saved fixtures with separate retained evidence.
