# CutBridge v0.2.3-beta.2 Compatibility Campaign

Status: **PLANNED / evidence incomplete**  
Release implication: **none** — this campaign does not authorize publication.

This document defines the evidence required before CutBridge expands any Blender or After Effects compatibility claim. Source inspection and automated mocks alone are insufficient for host-version support claims.

## Status vocabulary

- **TESTED / SUPPORTED** — the named host/version has the required evidence for the stated support scope.
- **TARGET / NOT YET VERIFIED** — intentionally targeted, but the required campaign has not passed.
- **LEGACY VERIFIED** — older bounded evidence exists; it does not automatically certify the current frozen candidate.
- **UNVERIFIED** — no current evidence sufficient for a support claim.
- **UNSUPPORTED** — intentionally outside the supported boundary.

## Blender matrix

| Blender | Current beta.2 status | Evidence boundary |
|---|---|---|
| 4.2 LTS | TARGET / NOT YET VERIFIED | Minimum declared runtime; exact beta.2 GUI/package campaign still required. |
| 4.5 LTS | TARGET / NOT YET VERIFIED | LTS target; exact beta.2 GUI/package campaign still required. |
| 5.2 LTS | TESTED / SUPPORTED for the currently recorded bounded scope | Official `bpy 5.2.1` automated RNA/package path plus existing bounded native 5.2.1 evidence; this does not certify every renderer/OS/end-to-end path. |
| < 4.2 | UNSUPPORTED | Below the declared minimum runtime. |

### Required Blender host campaign per target

1. install/enable exact beta.2 Blender artifact;
2. EN and JA N-panel renders correctly;
3. `Validate Cut` passes a valid cut;
4. intentional validation failures are understandable and recoverable;
5. Beauty package build succeeds;
6. Line succeeds only with an actually available Freestyle Render Layers output;
7. Line preflight blocks unsupported configuration before Build;
8. Shadow succeeds where the renderer exposes the pass;
9. Depth PNG/TIFF warning is non-blocking and actionable;
10. Depth OpenEXR path succeeds;
11. Beauty + Line + Shadow + Depth is exercised where renderer capabilities allow;
12. package collision/overwrite protection fails closed;
13. artist compositor state survives validation and failed Build;
14. V001 → V002 → V003 packages coexist;
15. save/reopen Blender file and repeat validation/build;
16. record exact OS, Blender build, renderer, SHA, artifact hash, and result.

## After Effects matrix

| After Effects | Current beta.2 status | Evidence boundary |
|---|---|---|
| 2020 | UNVERIFIED | No beta.2 native-host evidence. Do not claim support. |
| 2021 | UNVERIFIED | No beta.2 native-host evidence. Do not claim support. |
| 2022 | UNVERIFIED | No beta.2 native-host evidence. Do not claim support. |
| 2023 | UNVERIFIED | No beta.2 native-host evidence. Do not claim support. |
| 2024 | TARGET / NOT YET VERIFIED | Current target range, but beta.2 native-host evidence is required. |
| 2025 | TARGET / NOT YET VERIFIED | Current target range, but beta.2 native-host evidence is required. |
| 2026 | LEGACY VERIFIED for bounded native scopes; beta.2 exact-candidate verification still required | Existing AE 2026 Build 87 / Windows 11 evidence covers bounded S6–S8 and S10C scopes, not the changed beta.2 source as a whole. |

Do not upgrade AE 2020–2025 to **TESTED / SUPPORTED** until the named real-host campaign passes. Do not reinterpret the recorded AE 2026 Build 87 evidence as proof for a materially changed beta.2 source tree.

### Required AE host campaign for every version

For each AE version under evaluation, record all of the following against the exact frozen candidate:

1. CutBridge ScriptUI panel/script opens;
2. docked panel opens and can be reopened from the workspace;
3. undocked/palette execution if that entry path remains supported;
4. EN UI works;
5. JA UI works;
6. `cutbridge.json` loads;
7. Build succeeds;
8. imported render sequences resolve correctly;
9. QC+ succeeds on a valid package;
10. at least one controlled warning/error is triggered and recovered;
11. V001 → V002 succeeds;
12. V002 → V003 succeeds;
13. artist effects survive revision;
14. artist masks survive revision;
15. artist opacity survives revision;
16. artist-authored/manual layers survive;
17. parenting survives where the contract promises preservation;
18. save → close → reopen works;
19. panel/script reload works;
20. repeated Build does not duplicate CutBridge-managed objects;
21. Camera / 3D Null behavior is tested only if it remains release-facing for that candidate;
22. exact AE build, OS, candidate SHA, artifact hash, and evidence reference are recorded.

## Fallback policy for older AE versions

If a legacy AE version needs a compatibility fallback:

- isolate the fallback behind capability/version detection;
- keep the modern path unchanged when the fallback is not needed;
- document the exact host API/ScriptUI limitation that requires it;
- add automated regression coverage for both modern and fallback paths;
- validate the fallback in the real legacy host before claiming support;
- do **not** create seven separate product packages unless host constraints make a unified package impractical and the reason is documented.

## Candidate evidence record

When `v0.2.3-beta.2` is eventually frozen, add a new evidence record containing:

- exact source SHA;
- Blender artifact filename + SHA256;
- AE artifact filename + SHA256;
- CI run URL/ID on that exact SHA;
- each tested host build + OS;
- per-test PASS / FAIL / BLOCKED;
- evidence references;
- unresolved defects and severity.

Material source changes after that freeze invalidate the candidate evidence for release purposes and require a new frozen candidate.