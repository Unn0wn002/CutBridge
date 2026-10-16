# Review triage — 16 October 2026

Inspected fetched `develop` `8cc5a4fe19e97c2f83105b888f96ccf1b423e8fd`, PR #112 head `35fb9b9aede318624eea80d46b1dea3462ec4747`, PR #103 and their review threads. Full authenticated connector responses are retained in `review-threads.json`. GitHub CLI was installed separately, but `gh auth status` reported no authenticated hosts; no authentication or permission settings were changed. The connected GitHub reader supplied the live metadata as a documented fallback.

Both PRs are open and unmerged. PR #103 has 14 resolved threads; current source contains the regex, version-neutral help, pinned packaged readiness link, template preflight, artifact run-attempt identity and complete redirected PowerShell verification repairs. Those are superseded findings, not new product defects. Focused historical Blender 4.x evidence does not establish a complete current-host campaign.

PR #112 has 22 unresolved threads. Resolution below means local implementation/disposition, not a GitHub thread-resolution or native acceptance claim.

| Review comment ID | Current finding | Disposition |
| --- | --- | --- |
| 4173907294 | Candidate-ref orchestration | Active; replace automatic candidate-ref execution with explicit independently reviewed orchestration pin and candidate input. Actual trusted Linux workflow execution remains a separate required check. |
| 4173907296 | Archived diff differs from manifest | Confirmed. `git diff 8cc5a4fe19e97c2f83105b888f96ccf1b423e8fd 0c1938aeca7815393cdcd131bb9c3cb1a3215bca` reproduces 26,071 bytes with SHA-256 `a0d6b22d6b0c20de86c0355d30f8d0504ffbf5e0f18349b0ed526a67920bb148`, exactly the original manifest. Restore those bytes and mark the evidence path `-text`. This repairs retention only; it does not establish historical orchestration trust. |
| 4173907302 | Infrastructure classified as candidate FAIL | Active; separate dependency/startup/isolation/infrastructure verdicts from correctly executed candidate check failures. |
| 4173907305 | Unsupported independent validator/index PASS | Evidence gap remains. Current-facing JSON/docs mark these claims insufficient/unsubstantiated until exact inputs, commands and outputs are retained. |
| 4173907308 | Upload follows candidate output symlinks | Active; trusted staging only after candidate processes stop, rejecting symlinks/hardlinks/special paths, and upload only staged regular copies. |
| 4173995917 | Stale candidate hashes after packaged code edits | Earlier wording changes were superseded by later candidate campaigns; current edits change packaged bytes again. Rebuild exact candidate and never use old hashes as current identity. |
| 4173995921 | Source symlinks omitted from manifests | Active; reject unsupported Git modes and inventory exact source paths/types/bytes. |
| 4173995930 | Two-endpoint diff instead of fork point | Active; record true merge-base and preserve binary diff from it. |
| 4173995937 | Repeat comparison misses extra files | Active; compare complete output inventories and bytes in both directions. |
| 4174283720 | 604714d writes outside output | Already superseded by explicit INVALID disposition. Preserve original logs; no reuse. |
| 4174283721 | Hashed diff/index not retained | Active; retain source snapshot, review diff, fetched production-index bytes, manifests and commands. |
| 4174283726 | Truthy handoff wrapper does not prove payload | Historical assertion insufficient. Fresh native harness must inspect camera/null names, types, frames/times/counts and values. No retroactive PASS. |
| 4174283729 | Orientation reconstruction overstated | Active copy defect repaired: Camera Position/Point of Interest/Zoom and Null Position/Scale only. No 3D feature expansion. |
| 4174345921 | 0e02c76 repeats unbounded output | Already explicitly INVALID; original logs preserved and not reused. |
| 4174345924 | Single endpoint is not network policy | Historical isolation evidence insufficient. Retain actual fresh Sandbox policy, read-only mappings, adapter state and credential exclusion. |
| 4174345930 | QC does not inspect Camera/Null transforms | Active copy defect repaired. Require direct native sample inspection; QC is not expected-layer completeness, transform/keyframe or projection verification. |
| 4175827598 | fef1023 has no retained offline policy | Historical release-gate verdict corrected to INSUFFICIENT EVIDENCE; fresh policy/probe retained separately. |
| 4175827603 | Superseding payload check still truthy-only | Historical producer PASS unsupported; fresh assertion requirements as above. |
| 4175827607 | TMPDIR not redirected | Historical boundary incomplete; fresh launchers set TEMP, TMP, TMPDIR and bytecode/config paths to approved output. |
| 4176263650 | Archive attributes transform candidate inputs | Active; use exact Git blobs without `git archive`, filters or attribute transformations. |
| 4176263651 | Captured-ID cleanup regression never fails import | Runtime repair already exists. Add actual JSX-adapter regressions with numeric IDs, failure after import, invalidated native handles, removal refusal, preserved state and successful retry. Host-shaped tests remain distinct from native AE evidence. |
| 4176617861 | 049c095 isolation provenance absent | Historical release-gate verdict corrected to INSUFFICIENT EVIDENCE. Post-run network restoration proves no execution-time boundary. Fresh exact-candidate native campaign remains required. |

S14B remains NOT_EXECUTED. No review comment, status label or green CI result authorizes protected promotion, publication or production distribution.
