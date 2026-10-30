# Dockable ScriptUI Panels install QA - 2026-10-29 (WIB)

Evidence class: **NATIVE** (After Effects 2026, 26.5x89, Windows 11), one machine, one scenario. Bounded academic evidence; **not** a release approval. Overall verdict stays `INSUFFICIENT EVIDENCE`. Closes the "dockable `ScriptUI Panels` install not exercised" gap noted in `../native-install-qa-20261028/README.md`.

## Candidate identity
- Source: `35fb9b9aede318624eea80d46b1dea3462ec4747`, LF `git archive`, Python 3.13.17 (zlib 1.3.1), tag argument `v0.2.5` (tag not published).
- `CutBridge-AfterEffects-v0.2.5.zip` SHA-256 `ae9bfb9c2aa36c6764b324ac74ef85cc5022071b04bb7b7695e64a3651f70366`; Blender ZIP `3a53f7af...a48aa48`; both match the CI record (`SHA256SUMS-built-zips.txt`).
- `tools/verify_package.py` reported `ok: true`, `content_identical: true` for both ZIPs. This build/verify ran outside the AGENTS.md isolation boundary (unavailable: Windows Sandbox fails with 0x80370106), so it is package-identity evidence, not a verification verdict.

## Procedure and observations
1. The user copied the four runtime files (`CutBridge.jsx`, `localization.js`, `qc_plus.js`, `revision_manager.js`) with an elevated PowerShell into `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\Scripts\ScriptUI Panels`. I re-hashed them: all four byte-identical to the files extracted from the verified ZIP. (Two earlier checks ran before the copy completed and correctly showed the files absent.)
2. AE was not running; it was launched fresh and a new unsaved project created.
3. `CutBridge.jsx` appeared in the **Window** menu. It opened as a panel with a tab title and menu icon (the `Panel` branch of `thisObj instanceof Panel`), initially floating.
4. The user docked it by hand (my simulated mouse drags only moved the floating window and did not dock; that is an automation limit, not a product finding). It docked in the left column beside Project: `01-docked-before-quit.jpg`.
5. AE was quit with Ctrl+Q (no save prompt, process confirmed gone), then relaunched and a new project created. The panel reappeared docked in the same position: `02-docked-after-relaunch.jpg`.

| Check | Result |
| --- | --- |
| Files installed byte-identical to verified ZIP | PASS |
| Appears in Window menu | PASS |
| Opens as a Panel (not a plain palette) | PASS |
| Docks into the workspace (done by the user) | PASS |
| Docked layout survives full AE quit and relaunch | PASS |

## Limits
- The panel rendered with some clipped/partly drawn controls in screenshots (the right edge of the panel looked cut off by the Project panel overlay); not investigated. UI language was Japanese (the panel's own locale choice), so no English-UI check was made.
- No package was imported, built or revised in this run; functional behaviour is covered by the 2026-10-28 run. Panel features were not exercised here.
- One scenario, one machine; no claim for other AE versions, Blender GUI install, or Japanese-user validation (S14B `NOT_EXECUTED`).
- The four files remain installed in the AE Program Files folder; remove them to restore the original state.
