# Verifier review — 16 October 2026

Verdict: **INSUFFICIENT EVIDENCE** for the trusted Linux end-to-end verifier.
This static review does not claim native-host readiness, public-release readiness,
owner authorization, or S14B completion. The reviewer worked in a separate worktree
and also authored the verifier implementation; this is not an external security audit.

## Exact scope and bindings

Reviewed candidate: `5293cd46a819debfe8ecf41f740c4e94806dd89c`.
Recorded develop and merge-base: `8cc5a4fe19e97c2f83105b888f96ccf1b423e8fd`.
Read the workflow, host orchestration, command wrapper, applicable tests, retained
Windows evidence, and GitHub's current official workflow-dispatch documentation.
No candidate executable was run in the owner's environment during this review.

Git blob identities at the reviewed candidate:

| File | Git blob ID |
| --- | --- |
| `.github/workflows/candidate-verification.yml` | `86643a130c3180806dc3ae010ff06766986d9db9` |
| `tools/candidate_checks.sh` | `aa51b185a28e4a3a8a0b5e52779dcddec71b9e86` |
| `tools/candidate_verification.py` | `ee756aef980f6a69dabe4fcb79da6414db044ccc` |

The parent's retained Windows Sandbox record binds the 385-input snapshot to that
candidate, records read-only source, disabled networking, no owner HOME/Git or
credential environment, and Windows build `10.0.26100.0`. Its full suite reports
390 passed, two POSIX-specific skips, and two subtests passed. Source and runtime
checks, all CJS checks, repeated packages, independent artifact inspection, and
the unpublished distribution simulation have zero exit codes. Those records are
Windows verification evidence, not execution of the Linux Docker orchestration.

Retained evidence SHA-256 values under the parent's `output-r3/`:

| File | SHA-256 |
| --- | --- |
| `checks.log` | `4e2e0e8a6ffb7aaec0388ee308cb405b085324848fc85e453c708381068072ee` |
| `pytest.xml` | `524cd62171b30beed2d022720e452fb84d2d4d73fc0fc016aa43c6d9af01eb21` |
| `isolation.json` | `7d8992fcb94d10ddb63365204b07d6dc58372d350b25d282bec0c79faca6f161` |

The parent's exact-head [CI run 38875347991](https://github.com/Unn0wn002/CutBridge/actions/runs/38875347991)
is completed/success for this candidate. Ordinary CI remains distinct from the
trusted offline-container verifier and native-host evidence.

## Findings and disposition

The reviewed implementation selects orchestration by an operator-reviewed SHA,
never a candidate push or PR. It checks out that trust pin, reads candidate Git
objects as data, uses the unique true merge-base, materializes exact blobs without
archive attributes/filters, rejects unsafe paths and Git symlinks/submodules, and
records complete path/type/mode/byte inventories. Candidate commands start only
after the host inspects offline, read-only, non-root container settings and a
separate trusted Python-isolated-mode probe succeeds. Credentials and the engine
socket are absent from candidate mounts/environment. Trusted logs and verdicts
remain outside candidate-writable output; containers are removed before staging.
Package comparison covers both full inventories. ZIP modes, links, unsafe names,
case aliases, prefix conflicts, checksum coverage, metadata and AE guide content
are checked independently. Decoder failures are scoped to distinguish candidate
failures from malformed trusted infrastructure output.

One active P2 was found at candidate helper lines 514–521: package comparison or
validation could throw before safe staging, losing the failing packages and both
inventories. Fix `a6ee2445f81906c024fd5b9e1689faac017f198a` adds a retention wrapper:
both inventories are written first, a primary package failure is recorded, safe
outputs are staged, then the original failure is rethrown. Unsafe staging retains
an INVALID verdict. Regressions cover repeat differences, validation failure, full
retained bytes/inventories, and an unsafe report symlink after package failure.
That fix requires a fresh isolated test run; the earlier 390/392-test evidence
must not be presented as execution of its new tests.

No other definite false-PASS or credential-boundary bypass was identified in this
bounded static review. The actual Linux build, Docker inspection/probes, execution,
failure classification, artifact staging and upload still require end-to-end evidence.

## Dispatch availability and reviewed bootstrap

Live repository metadata confirms default branch `main`. Reading the verifier
workflow on that default branch returns 404, consistent with its absent path in
the local `origin/main` tree at `a393e409d19445c4090460b7e7b4716779161fa4`.
[GitHub's manual-run documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
requires a workflow to exist on the default branch for workflow_dispatch.
The [REST reference](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)
accepts a branch/tag ref; that ref does not establish independent trust or bypass
the documented registration prerequisite. No protected write or settings change
is authorized merely to enable this workflow.

A separate reviewed push-triggered bootstrap on an unprotected orchestration
branch can exercise the same pinned helper without default-branch changes. This
is a new reviewed orchestration entry point, not a dispatch of the absent workflow.
The prepared template is outside the repository at
`C:/Temp/CutBridge-verification-20261016/reviewed-bootstrap.yml`, SHA-256
`455e421f6e8fd6d54a9787ccdbb6242577326522e08aced02598a4e928e9439c`.

Required steps before that run:

1. Independently review helper-fix commit `a6ee2445f81906c024fd5b9e1689faac017f198a`
   and its unchanged trusted command wrapper. Select this as a trust pin only
   after that review; this report does not substitute for owner authorization.
2. Finish and push the distinct exact candidate, including the retention fix.
   Replace only `__TRUST_SHA__` and `__CANDIDATE_SHA__` in the template with literal
   reviewed commits. Develop is fixed to `8cc5a4fe19e97c2f83105b888f96ccf1b423e8fd`.
3. Create `fix/trusted-verifier-bootstrap-20261016` from the reviewed trust commit,
   add only the literal-filled bootstrap under `.github/workflows/`, and review
   the complete bootstrap diff and exact commit before pushing that branch.
   The helper checks out only the trust SHA; candidate code runs in its containers.
4. Confirm the resulting run's workflow/head SHA equals that reviewed bootstrap
   commit. Retain its bootstrap/workflow/ref/run/runner identity record alongside
   the helper evidence. Check all container settings, input comparisons, commands,
   package hashes, original failure cases and staged artifact upload.
5. Preserve ordinary CI triggered by the bootstrap's `fix/**` branch as separate
   evidence for its trusted baseline. It does not verify the distinct candidate.

The template uses contents-read permission, pinned actions, fixed branch/pins,
unpersisted checkout credentials, and host-owned artifact staging. It records
the actual bootstrap SHA and runner build without dumping secret-bearing context.
Neither this report nor the template has been pushed or executed by this reviewer.

## Follow-up binding and current execution boundary

Root integrated the retention fix into candidate
`931b4752d0dbb2df915f73d65591604486c1f1d6`. A direct Git comparison confirms that
its helper, command wrapper, manual workflow and verifier regression tests have
identical blobs to original reviewed helper commit
`a6ee2445f81906c024fd5b9e1689faac017f198a`. This establishes code equivalence for
those paths; it does not establish execution of the new retention tests.

Read and reviewed the literal-filled bootstrap staged in the parent's separate
`CutBridge-bootstrap` worktree at `.github/workflows/reviewed-release-verification.yml`.
Its SHA-256 is
`fa2758a79b106ae44a51b043a0566bced50bf7fafe1b111fb42d7787943d8f82`.
It pins trust to the original `a6ee2445f81906c024fd5b9e1689faac017f198a`, candidate
to `931b4752d0dbb2df915f73d65591604486c1f1d6`, and develop to the recorded `8cc5a4f…`.
Only that workflow was staged and the bootstrap branch HEAD was the trust commit.
No static gating issue was found in this exact literal-filled file: branch guard,
separate fixed pins, read-only permission, pinned actions, unpersisted checkout
credentials, helper invocation, host-owned upload and separately retained actual
bootstrap/run/runner identity match the reviewed design. Before accepting a run,
confirm its actual head/workflow SHA equals the exact reviewed bootstrap commit.
Any changed file, ref or pin requires renewed review. Static acceptance of this
file is not a verifier PASS or protected-release authorization.

The fresh Windows Sandbox `r4` snapshot is bound to candidate `931b475…`, with
385 inputs and the recorded merge-base. Its dependency preparation/preflight
failed before candidate execution: importing `rpds` raised an Application Control
policy DLL-block error. The retained verdict is **INSUFFICIENT EVIDENCE**, not a
candidate FAIL. The parent also reports current native AE startup blocked with
status `0xc0e90002`; no native result is inferred. Existing valid `5293cd4…`
automated evidence remains scoped to that earlier candidate and tested inputs.
No authorization, application-control policy, protection, or isolation control
was changed to bypass these blockers. The reviewed Linux bootstrap is the next
independently executable route; its actual container run and upload remain pending.
