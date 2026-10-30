# Isolated verification in Windows Sandbox - 2026-10-29 (WIB)

Candidate: PR #115 head `a1113a7` (`work/cutbridge-install-qa-20261028`). Product source is identical to the PR #112 head `35fb9b9`; commits after `c133669` change documentation only.
Reviewer: Claude (Opus 5.5), run unattended while the owner was away. This is not a release approval, merge or tag.

## Verdict

**`PASS`** under the AGENTS.md verification protocol: every required check ran inside the isolation boundary and passed, and the before/after snapshot manifests are identical.

## Isolation boundary (verified, run 5)

- Windows Sandbox (disposable VM; guest `4E7B2FAA-A2EC-4`, Windows 10.0.26100.9711), user `WDAGUtilityAccount`. No owner credentials, host HOME, `.git` or GitHub auth mapped.
- `<Networking>Disable</Networking>`; the run log records `github.com` unresolvable. Clipboard redirection disabled; vGPU disabled.
- Read-only mappings: candidate snapshot (`git archive a1113a7`, `core.autocrlf=false`, 394 files, equal to the commit tree), Python 3.13.17 (zlib 1.3.1), test dependencies (pytest, jsonschema, bpy 5.2.1), Node v24.22.1, the Microsoft VC++ runtime DLLs, the run script and the two input ZIPs.
- Writable: the mapped output folder; temp on the Sandbox's own disposable disk (`C:\vtmp`); `PYTHONPYCACHEPREFIX` in the output folder; pytest cache provider disabled.
- Snapshot manifest identical before/after, both inside the Sandbox and re-hashed on the host (`manifest-*`). Input ZIP hashes unchanged.
- Config: `sandbox-config-run5.wsb`; script: `run_qa_run5.ps1`.

## Results (run 5)

| Check | Result |
| --- | --- |
| `python -m compileall -q apps tools tests` | exit 0 |
| `python -m pytest -q -p no:cacheprovider` | 319 passed, 2 subtests passed |
| `python tests/test_blender_runtime_52.py` | bpy 5.2.1 LTS; CutBridge Blender 5.2 RNA registration PASS |
| `python tools/verify_package.py --tag v0.2.5 --source-dir <snapshot> ...` | `ok: true` for both ZIPs; content identical and ZIP bytes identical to the in-Sandbox rebuild (`run5/verify-package.json`) |
| `python -m pytest -q -p no:cacheprovider tests/test_verify_package.py` | 6 passed |

Input ZIPs (`input-zips-SHA256.txt`): Blender `3a53f7af...a48aa48`, After Effects `ae9bfb9c...f70366`, the hashes recorded for CI. `source_commit` is null in the JSON because `--source-dir` was used; the snapshot identity is the manifest above.

## How the boundary was reached (runs 1-4, `earlier-runs/`)

Same snapshot, never modified (manifests identical after every run), so reuse is allowed; no run was INVALID.

1. Run 1: `import bpy` failed with "DLL load failed": a clean Sandbox lacks the VC++ runtime. 8 collection errors. INSUFFICIENT EVIDENCE.
2. Run 2: runtime DLLs copied into the disposable Sandbox's System32 (host unchanged). 68 failures, 67 of them "Node.js is required". INSUFFICIENT EVIDENCE.
3. Run 3: Node mapped. 318 passed, 1 failed: `test_artifact_symlink_cannot_overwrite_another_file`, PermissionError while the temp area was on a host-mapped folder. Environment limit, not a product failure.
4. Run 4: temp moved to the Sandbox's own disk. 319 passed.
5. Run 5: run 4 plus `verify_package.py` on the ZIPs. All pass (above).

Earlier the same day the Sandbox itself failed with 0x80370106 (guest bugcheck 0x3B after a virtual PCI protocol mismatch); the owner reset the Windows Sandbox feature and it now boots. The launch config also had to drop `ProtectedClient` and the printer/audio/video redirection settings, which stopped the VM from starting on this host; they do not form part of the AGENTS.md boundary.

## Limits

- This covers source/tests/package identity only. Native Blender/After Effects rows (P5, N4, N5, N6, GUI install dialog) remain NOT_RUN; S14B NOT_EXECUTED.
- GitHub CI remains separate evidence; this run is the local isolated verification.
- One host, one toolchain (Python 3.13 / zlib 1.3.1).
