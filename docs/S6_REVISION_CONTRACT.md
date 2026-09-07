# S6 Revision Contract — core repair, integration incomplete

PR #15 remains **BLOCKED for integration**. The revision core has executable Node/pytest
regressions; it is not connected to the After Effects panel or included in the AE ZIP.
The earlier S6 implementation-complete claim was premature.

## Compatibility and discovery

- Both manifests pass the existing `CutBridgeContract.validateManifest` gate, including
  finite integer versions/frames, safe paths/patterns, unique passes and valid required flags.
- S6 additionally requires non-empty project, episode, scene, cut and take fields.
  This is a stricter revision preflight; the existing S5 importer is unchanged.
- Compare each identity field exactly. Length-prefixed identity encoding prevents delimiter
  collisions. Never use package name as a substitute for the cut tuple.
- Blender-generated package names include V###, so names may differ between revisions.
  The adapter must bind each live package to its full manifest and filesystem root.
- Manifest versions remain positive integer numbers. `revisionNumber` additionally parses
  canonical display tokens V001…V999, V1000, etc.; it rejects strings such as V002draft,
  V2 and V0002, negative/fractional numbers and unsafe integers.
- `discover` returns diagnostic rows in input order. `selectLatest` selects the highest
  compatible newer numeric revision. Duplicate newer revisions for the same cut are
  ambiguous; selection returns null regardless of their order or package names.
- FPS, frame range/count and pixel-aspect changes block. Resolution and required/optional
  status changes warn and require explicit confirmation. Source geometry can change the
  visual result even when layer properties are retained.
- Missing previously required passes block. Removed optional passes remain untouched.
  Added passes block this source-only operation; it does not create layers.

## Trusted host-adapter boundary

`createExecutor(adapter)` captures mandatory callbacks and returns `prepare(current,
candidate)` and `apply(ticket, confirmed)`. The public ticket is only a display/confirmation
handle. Actions and manifest snapshots remain private; a forged, expired, reused or
another executor's ticket cannot authorize a write. Public ticket edits cannot bypass
warnings. A new prepare invalidates the previous ticket.

Callbacks are trusted, receiver-independent host code, never manifest data. This API
does not sandbox a malicious adapter. All callbacks must exist before preparing a plan:

| Callback | Required behavior |
|---|---|
| listManagedLayers(current) | Read-only discovery returning only live layer handles and pass names for this package. Never rely on caller-provided managed flags. |
| validateManagedLayer(layer, current, passName, ownershipKey) | Read-only, literal true only after proving live host type/membership, exact comp/render folders, persistent package/tuple/version metadata and tags, uniqueness, source path and conform FPS. |
| readSource(layer) | Return the actual live source handle; throw if unreadable. |
| importReplacement(candidate, passName, track) | Allocate exactly one new item, immediately call track(item), then configure it and return it. Track before any fallible setup so allocation-then-throw is recoverable. Never return or track existing artist footage. |
| validateReplacement(item, candidate, passName) | Literal true only after filesystem containment, exact sequence coverage, source identity, type and conform FPS validation. |
| swapManagedSource(layer, item) | Change only the verified layer's source. Do not change effects, masks, timing, transforms, parenting, switches, blend mode, tags or ordering. |
| restoreManagedSource(layer, oldSource) | Restore the journaled source even after a swap mutates then throws. The core verifies readSource afterward. |
| removeImportedReplacement(item) | Remove only this transaction's tracked new item, verify its absence, and return literal true. |

The `ownershipKey` includes the collision-safe cut tuple, numeric version, package name
and pass. It is verification context, not a replacement tag format for existing S5
comments. A native adapter needs a reliable persisted manifest/root association and an
explicit migration policy before it can attest ownership. No silent S5 tag adoption is
implemented.

## Transaction and recovery

1. Prepare validates manifests, required managed-layer coverage, duplicate records/handles,
   and live ownership/source associations.
2. Apply revalidates the managed objects, stages and validates **all** replacement imports,
   then revalidates ownership before swaps. There are no swaps on import/validation failure.
3. Record each old source before attempting its swap, then verify the new live source.
4. On failure restore every attempted layer in reverse order, including mutate-then-throw.
   Only after all restores succeed, remove the tracked replacement items.
5. If restoration fails, retain all replacement footage to avoid dangling layer sources.
   Cleanup failures are also reported, including retained counts. The executor blocks
   retries after incomplete rollback; recover the project before constructing another one.

Host failures cannot be guaranteed reversible. Errors state `ROLLBACK INCOMPLETE`
when appropriate; the core never swallows recovery failures or claims unconditional
atomicity. An adapter violating its allocation/tracking contract can leak an untracked
host object and is not suitable for integration.
Error formatting is nonthrowing, including host exceptions without a usable toString;
one recovery failure cannot prevent the remaining recovery attempts. Malformed schema
types and shared-validator exceptions become incompatible-candidate diagnostics.

## Outstanding before S6 integration

- Implement and test a real AE adapter, including persistent current-package/version/root
  association, safe S5 migration and metadata updates with rollback.
- Add package-directory discovery and the panel preview/confirmation/update flow.
- Preserve Build/QC behavior after revision and script reload, and test V001→V002→V003
  against producer-generated manifests and mock native host objects.
- Include the executable revision path in deterministic release ZIPs and validate installation.
- Obtain independent clean full-PR review plus green CI before merge; verify post-merge CI.

Keeping mock layer objects and their non-source properties unchanged is tested. Native AE
property preservation, real revision execution, GUI/undo behavior and Blender→AE end-to-end
remain **MANUAL NOT EXECUTED**. S7 has not started.
