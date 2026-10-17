# AE 26.5x89 native campaign at 89b1dab

Candidate: `89b1dab3a82d6ddd2b1999c06de1d28e46fafc0d`. AE ZIP SHA-256: `8a1c377fa8d306df12b1c968ea7038b1947056815c8acae671470f7cba52a79c`.

Verdict: **FAIL**. The previous cached-manager/project-reload revision defect is repaired: V003 to V004 (DEPTH required to optional) succeeds after closing/reopening the project and reloading the panel with the cached manager retained. QC passes; Camera/Null samples match. FPS drift, optional-pass removal, added pass and required-pass removal are blocked before confirmation. The guarded V004 snapshot retains the prior layer IDs/order, sources, ownership tags and inspected artist properties.

A subsequent required native optional-layer test exposes a separate defect: deleting the complete optional DEPTH layer while keeping its managed footage produces `CBQ-LAYER-OWNERSHIP-ERROR`, `ReferenceError: Object is invalid`, rather than `CBQ-LAYER-OPTIONAL-MISSING` warning. Native AE comparisons of a deleted cached handle throw. Screenshot and raw report preserve the failure. A follow-up fix must check native `isValid()` before membership comparisons; verification remains pending.

Sandbox: user-installed Windows Sandbox, AE 26.5x89; network disabled, source/fixtures read-only, explicit shared output/TEMP only, no owner home or credentials. The preceding AE test process was forcibly terminated after preserving its synthetic checkpoint because normal-exit attempts did not finish. The Sandbox itself and installed apps were preserved. This campaign is not proof of normal process exit or representative Japanese artist validation. Japanese panel text renders; native alert glyphs have the recorded host font limitation.

Exact-commit CI passed: [isolated push](https://github.com/Unn0wn002/CutBridge/actions/runs/37179408217), [isolated PR](https://github.com/Unn0wn002/CutBridge/actions/runs/37179410477), [CI push](https://github.com/Unn0wn002/CutBridge/actions/runs/37179408194), [CI PR](https://github.com/Unn0wn002/CutBridge/actions/runs/37179410388). All 18 AE Node suites also passed separately in the offline Sandbox. Neither CI nor those suites detected the native deleted-handle defect.

Generated projects, ZIPs and image sequences remain ignored local verification artifacts.
