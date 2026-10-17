# Independent release review packet — PR #113

Status: **PREPARED / REVIEW NOT_RECEIVED / SCOPE ACCEPTANCE NOT_RECEIVED**. This is a request package for an independent reviewer; it contains no approval. No review has been posted or message sent. Runtime and package bytes remain frozen.

Closeout update, 17 October 2026: review the frozen baseline below plus the later documentation/evidence diff on PR #113. The startup timebox expired without an approved initializing native environment; see [the handoff](NATIVE_VALIDATION_HANDOFF.md) and [assessment](evidence/20261017-validation-closeout/assessment.json). The README was repaired, preserving original bytes/catalog; final-639 results and release assets were not changed.

## Exact decision and baseline

Review [PR #113](https://github.com/Unn0wn002/CutBridge/pull/113) at exact source **`639374ce5f1b5f0d36847258d052c36ab21dd208`**, branch `fix/current-release-completion-20261016`, fetched develop/merge-base **`8cc5a4fe19e97c2f83105b888f96ccf1b423e8fd`**. The working target is **22 October 2026**; the official submission deadline remains **UNCONFIRMED**.

Requested decision: assess the current code/evidence and explicitly identify which demonstrated claims can be accepted, which native/manual checks remain necessary, and whether changes are requested. Submission acceptance and public-release authorization are separate. The current overall verdict is **INSUFFICIENT EVIDENCE**. `release-authorization.json` stays false, production remains v0.2.3, and S14B stays NOT_EXECUTED. Approval of this review packet cannot authorize a protected merge, tag, publication or distribution.

## Inputs to inspect

Local packet: `C:\Users\unn0w\.codex\worktrees\5d5d\CutBridge\dist\release-candidate-20261016\`.

Read `README.md`, `FINAL_HEAD_VERIFICATION.json`, `EVIDENCE_BINDING.json`, `candidate.json`, `candidate.diff`, `git-inventory.json`, `DEMO_CHECKLIST.md`, `SHA256SUMS.txt`, `release-metadata.json` and `PACKET_SHA256SUMS.txt`. `FINAL_HEAD_VERIFICATION.json` is the final-639 receipt; `EVIDENCE_BINDING.json` intentionally retains earlier a447/5293 evidence rather than reassigning it. Retained final trusted evidence is `C:\Temp\CutBridge-verification-20261016\remote-bootstrap-final\`, with artifact ZIP `bootstrap-final-evidence.zip` alongside it.

| Frozen artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| CutBridge-Blender-v0.2.5.zip | 63682 | `864131a58a1c56e4364c3e435ef1433fbda415515be7292770212bfdc4c31bfe` |
| CutBridge-AfterEffects-v0.2.5.zip | 59686 | `427a36ba8638e88940b18f9daa34537c7e41ad939f3b81fddb50a3812d691268` |
| release-metadata.json — primary Linux bytes | 674 | `a9e0d91202173cb9ad431a3f1b85ca0b8b8d4a416ad49a5e8e3c336e23a1722f` |
| SHA256SUMS.txt — primary Linux bytes | 195 | `d153d2ca56594f28ee4ed75d9b97859d4430a0950ad1385aaa6d32fedebbe4bb` |
| Frozen source-inputs.tar | — | `472a49754f0bbdfa34acd4974898d1507cd93b84dec2a55dfb5a41d418be1715` |
| Frozen candidate.diff | — | `0292a9efffa7c883cccbbb6573ac3181f992b485ea9621da8ab7e0d851d76605` |
| Final downloaded evidence ZIP | 12237082 | `06b3be67cb741e58b649fe18ff353048560508b6307e091db5d384dd434d20e7` |

Each toolchain's complete four-asset repeat builds match. Windows/Linux ZIPs match, while metadata/checksum CRLF/LF bytes differ with equivalent JSON/checksum entries. Review and preserve the primary Linux metadata/checksum bytes; do not rewrite them merely to compare platforms.

## Recorded automated acceptance

[Trusted run 38911851205](https://github.com/Unn0wn002/CutBridge/actions/runs/38911851205): **396 passed + 2 subtests, no skips**, official `bpy 5.2.1`, 18 AE Node suites, syntax, unchanged exact path/type/mode/byte inventories, complete repeated packages and safe staging/upload. Immutable bootstrap: `9d4e8eb7c03e3fd60b751bf093b57d599d446db5`. Trusted orchestration: `571f4cdb1c992124bdb35e3d089de1de1535b254`. Image: `sha256:99239f1ba80a915f7984a0932cfa8d4e841d14adcc0a9f1fd8a388c0f22264f3`.

[Ordinary CI 38911503228](https://github.com/Unn0wn002/CutBridge/actions/runs/38911503228) is separate exact-head CI evidence. Inspect bootstrap context, `verification.json`, actual container command inspections and logs: workflow HEAD is the bootstrap SHA, while the tested candidate must be 639374c. The final receipt records 48 verified inner evidence checksums. The original packet's 63 entries were verified before amendment; that original catalog is retained, and amended `PACKET_SHA256SUMS.txt` inventories the current packet. A missing host does not invalidate automated observations or establish native acceptance.

## Read-only reviewer commands

These commands inspect metadata/files; they do not execute candidate code. Use authenticated GitHub CLI in the owner/reviewer environment, keeping that authentication outside all candidate execution.

```powershell
gh pr view 113 --repo Unn0wn002/CutBridge --json number,url,headRefName,headRefOid,baseRefName,reviewDecision,statusCheckRollup
gh pr diff 113 --repo Unn0wn002/CutBridge --name-only
gh run view 38911851205 --repo Unn0wn002/CutBridge --json databaseId,headSha,headBranch,event,status,conclusion,url
git -c core.hooksPath=NUL diff --no-ext-diff --no-textconv 8cc5a4fe19e97c2f83105b888f96ccf1b423e8fd 639374ce5f1b5f0d36847258d052c36ab21dd208 -- apps tools tests .github docs/RELEASE_CHECKLIST.md
$packet = 'C:\Users\unn0w\.codex\worktrees\5d5d\CutBridge\dist\release-candidate-20261016'
Get-Content -LiteralPath "$packet\FINAL_HEAD_VERIFICATION.json"
Get-FileHash -Algorithm SHA256 -LiteralPath "$packet\CutBridge-Blender-v0.2.5.zip", "$packet\CutBridge-AfterEffects-v0.2.5.zip", "$packet\release-metadata.json", "$packet\SHA256SUMS.txt", "$packet\source-inputs.tar", "$packet\candidate.diff"
```

If PR HEAD changes, record that fact and scope this review to the frozen SHA; do not silently apply the receipt to a later head. Candidate execution, if independently requested, still requires the approved isolated environment and existing CONTRIBUTING/RELEASE_CHECKLIST procedures. There is no new review gate script.

## Review questions and claim boundaries

- Confirm active versus superseded review findings using committed `docs/evidence/20261016-release-completion/REVIEW_TRIAGE.md` and current code, particularly captured-ID cleanup, invalid native handles, trusted orchestration, exact snapshots, retained inputs, archive attributes/symlinks, merge-base, safe upload, complete repeat comparison and infrastructure classification.
- Confirm ordinary CI, trusted execution and native observations are separate. Reuse native Blender **5.2.2 `d13f752e3b9c`** only through the demonstrated unchanged ZIP: scripted V001–V003/36-output, preservation, negative/rollback and fresh-process reopen scope, with actual exits 0. GUI/dialog/manual-update acceptance is excluded.
- Accept zero current native AE assertions until the corrected campaign actually executes. Current host startup failed `0xc0e90002`; the retained assessment is an infrastructure limitation. Review `docs/evidence/20261016-release-completion/native-ae/assessment.json` and the operator handoff's harness gaps.
- Confirm the actual 3D channel claim: Camera Position/Point of Interest/Zoom and Null Position/Scale. No camera roll/Empty rotation reconstruction; QC does not verify expected 3D completeness, channel/keyframe values or projection. No expanded 3D or representative-user claim is proposed.
- Assess required native installation, EN/JA/narrow/help UI, actual AE workflow/preservation/negative/rollback/reopen and manual-update evidence against the intended submission claim. Name unresolved checks individually; do not treat a scripted harness's raw PASS as full acceptance.
- Confirm installer instructions, four adjacent AE runtime files, exact hashes, limitations and demo correspond to these packages. Confirm protected release state and production distribution remain unchanged.

## Return requested

Return `scope-acceptance.json` with actual reviewer identity/independence, timestamp, reviewed SHA/artifact hashes, inspected evidence, concrete findings, accepted/excluded claims and a decision. Leave `NOT_RECEIVED` unchanged until an actual independent review or owner scope acceptance is provided. Return evidence files or durable references with SHA-256, not an unbound “looks good.” Any native result must name host/build, inputs, isolation policy, method, actual observations and exclusions.

Independent review may request changes or decline scope. It must not manufacture missing native results, waive gates through an undocumented inference, claim S14B completion or approve publication/distribution implicitly.
