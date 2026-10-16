# Isolated candidate verification

The optional `candidate-verification.yml` workflow wraps the existing commands
in [CONTRIBUTING.md](CONTRIBUTING.md). It does not change canonical CI, release
authorization, native-host requirements, or publication procedures. Its PASS is
limited to the automated scope recorded in its evidence.

## Independent trust is required before dispatch

Candidate push/PR triggers are disabled. A candidate-controlled workflow must
never provision its own sandbox, receive runner credentials, select its own
verification inputs, or stage its own trusted verdict.

An operator must independently review the workflow, `tools/candidate_verification.py`,
`tools/candidate_checks.sh`, pinned actions, and dependency preparation at an
immutable orchestration commit. Choose that reviewed commit separately from the
candidate. The trust decision comes from this review and the operator's dispatch,
not from a candidate document or a successful SHA comparison.

No reviewed trust pin or execution of this new workflow is established by merely
adding these files. Until independent review and workflow availability are
established, record **INSUFFICIENT EVIDENCE** for its execution. GitHub must also
register the dispatchable workflow on the default branch. Do not merge, promote,
create a protected tag, or alter authorization merely to enable dispatch.

With the applicable authorization and a registered workflow, record the trusted
commit and a dispatch ref resolving to it, the exact candidate commit, and the
fetched develop tip. Inspect all three before dispatch:

```bash
gh workflow run candidate-verification.yml --ref "$TRUSTED_REF" \
  -f trusted_orchestration_sha="$TRUSTED_SHA" \
  -f candidate_sha="$CANDIDATE_SHA" \
  -f develop_sha="$DEVELOP_SHA"
```

The workflow rejects a workflow commit differing from the reviewed trust pin and
rejects using the candidate itself as the trust pin. It checks out only the
trusted commit, with credentials unpersisted. Orchestration reads candidate Git
objects as data and never checks out or imports candidate code on the runner.
The actual review diff starts at the unique merge-base of the recorded develop
and candidate commits, rather than comparing an advancing develop tip directly.

## Inputs and isolation

The snapshot is built from `git ls-tree` and exact `git cat-file` blob bytes.
`export-ignore`, `export-subst`, checkout filters, and line-ending conversion
cannot omit or rewrite files. Tracked symlinks, submodules, special/unsafe paths,
case aliases, duplicate paths, and reserved mount-path collisions are rejected.
The snapshot inventory records Git object IDs, modes, sizes, and SHA-256 hashes.
No `.git`, credentials, unrelated workspace files, or broad cache exclusions are
copied. Unexpected generated cache files outside the output mount are invalid.

Dependencies are prepared with network access before candidate execution and
without candidate inputs. Retain the Dockerfile, preparation log with installed
versions, and image inspection/ID. Dependency tags are not assumed immutable:
reuse requires the recorded image ID/toolchain and exact input equivalence.

Before candidate execution the host inspects the actual container settings:
offline network, read-only root/source/input/orchestration mounts, the sole
writable output mount, UID 1000, dropped capabilities, no new privileges, private
process boundary, resource limits, and a strict environment allowlist. The owner
HOME, authentication, engine socket, and other host paths are not mounted.
Trusted isolation probes use Python isolated mode before running candidate
commands. Native GUI checks are outside this container's scope.

Before/after inventories cover the source, retained production-index bytes, and
reviewed command wrapper. They include every path, file type, mode, and file
hash; manifests exclude only the designated writable output directory.

## Outputs, evidence, and verdicts

After execution, remove the container and all its processes before reading
candidate output. Compare the complete inventories and bytes of both package
builds, including extra files/directories in either build. Independently inspect
the four expected artifacts, both checksum entries, metadata names/hashes, and
the AE ZIP installation guide.

Stage only allowlisted package/preview/report roots into a separate host-owned
directory. Reject symlinks, hardlinks, special files, unsafe paths, and oversized
files. Candidate output cannot overwrite the host's logs, manifests, command
records, identity, or verdict. The upload action reads only the staged evidence
directory, never candidate-writable mounts or globs.

Retain the complete source-input archive, exact binary diff, candidate/develop/
merge-base/trust SHAs, Git inventory, before/after manifests and inventories,
production-index bytes/hash, dependency and image records, container inspections,
command/log results, repeated-package inventory, staged artifacts, and evidence
checksums. Artifact hashes and tested scope must accompany any readiness claim.

- `PASS`: required automated commands, exact input integrity, complete repeated
  packaging, independent package checks, and safe staging all passed.
- `FAIL`: candidate commands actually ran and failed, or package behavior was
  incorrect. A real candidate exit code remains FAIL even if numerically equal
  to a Docker CLI error code.
- `INVALID`: wrong trust selection, unsupported/unsafe snapshot or output,
  isolation configuration mismatch, or changed input inventory/types/modes/bytes.
  Discard the attempt and create a fresh snapshot before rerunning.
- `INSUFFICIENT EVIDENCE`: dependency/index preparation unavailable, Docker
  launch/attach/inspect/cleanup failure, timeout, OOM, or another infrastructure
  failure. These are never presented as candidate test failures.

Regression tests in `tests/test_candidate_verification.py` exercise trust
selection before execution, exact blob copying, archive-attribute bypass,
inventory completeness, unsafe types/paths, staging, repeated-output comparison,
and infrastructure classification without Docker, network, real Git, or owner
credentials. POSIX mode/FIFO cases require Linux; unsupported symlink creation
is an explicit skip on restricted Windows hosts.
