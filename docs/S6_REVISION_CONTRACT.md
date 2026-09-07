# S6 Revision Contract — native integration, review pending

PR #15 remains **BLOCKED for merge** pending independent review and native AE validation.
The revision core is connected to the After Effects panel through a same-directory sidecar,
and the deterministic AE ZIP ships both executable files. Native AE GUI execution remains
MANUAL NOT EXECUTED.

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
- FPS, frame range/count, pixel-aspect **and resolution** changes block. S6 is deliberately
  source-only and does not resize/re-time an existing composition; accepting a new resolution
  while retaining old comp geometry would leave Build/QC inconsistent with the new manifest.
- Required/optional status changes warn and require explicit confirmation. Missing previously
  required passes block. Removed optional passes remain untouched. Added passes block this
  source-only operation; it does not create layers.

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
| swapManagedSource(layer, item) | Change only the verified layer's source. In the native adapter this must use `AVLayer.replaceSource(item, false)` because `AVLayer.source` is read-only. Do not change effects, masks, timing, transforms, parenting, switches, blend mode, tags or ordering. |
| restoreManagedSource(layer, oldSource) | Restore the journaled source even after a swap mutates then throws. The native adapter uses `AVLayer.replaceSource(oldSource, false)` when restoration is needed; the core verifies `readSource` afterward. |
| removeImportedReplacement(item) | Remove only this transaction's tracked new item, verify its absence, and return literal true. |
| commitRevision(current, candidate, replacements) | Persist the new package/root/version identity and managed tags only after every source swap succeeds. Throw on any failed metadata write so the core restores sources and invokes cleanup. |

`AVLayer.source` is treated strictly as an observation. The native adapter never assigns to it.
`replaceSource(..., false)` is used so CutBridge does not ask After Effects to rewrite artist
expression text while replacing managed footage; source identity is verified immediately after
each swap by the revision core. Static regression coverage rejects direct `layer.source = ...`
assignment in the S6 adapter.

The `ownershipKey` includes the collision-safe cut tuple, numeric version, package name
and pass. It is verification context, not a replacement tag format for existing S5
comments.

The native adapter preserves provenance across revisions: the active layer and replacement
footage receive the candidate package/version tags, while retired CutBridge footage retains
its previous version-scoped CutBridge tag. Retired footage is removed from current-version
caches but is not converted into an unmanaged item. This allows historical footage to remain
available for artist references without weakening S5's unmanaged-collision protections.
Rollback restores the exact pre-revision root/comp/layer/footage comments and names recorded
before migration.

## Transaction and recovery

1. Prepare validates manifests, required managed-layer coverage, duplicate records/handles,
   and live ownership/source associations.
2. Apply revalidates the managed objects, stages and validates **all** replacement imports,
   then revalidates ownership before swaps. There are no swaps on import/validation failure.
3. Record each old source before attempting its native `replaceSource()` swap, then verify the
   new live source. A missing native replacement method blocks the transaction.
4. Only after every source swap succeeds, migrate the package root, managed comp/layer tags,
   replacement-footage tags, and current-version caches. Retired footage keeps old-version
   provenance instead of becoming unmanaged.
5. On failure restore every attempted layer in reverse order, including mutate-then-throw,
   using native `replaceSource()` where a source restoration is necessary, and restore any
   partially migrated metadata from the recorded journal.
6. Only after all restores succeed, remove the tracked replacement items.
7. If restoration fails, retain all replacement footage to avoid dangling layer sources.
   Cleanup failures are also reported, including retained counts. The executor blocks
   retries after incomplete rollback; recover the project before constructing another one.

Host failures cannot be guaranteed reversible. Errors state `ROLLBACK INCOMPLETE`
when appropriate; the core never swallows recovery failures or claims unconditional
atomicity. An adapter violating its allocation/tracking contract can leak an untracked
host object and is not suitable for integration.
Error formatting is nonthrowing, including host exceptions without a usable toString;
one recovery failure cannot prevent the remaining recovery attempts. Malformed schema
types and shared-validator exceptions become incompatible-candidate diagnostics.

Revision application also fails closed when the AE confirmation function is unavailable;
there is no automatic revision mutation without a user confirmation surface.

## Automated evidence

Exact-head CI run `34144889247` on `540831f1a5b0f2dfbe58c73c277a4a66681bcc00`
passed `static-validation` and `blender-52-rna-runtime`. Static validation includes pytest,
deterministic release-package simulation/checksums, S6 Node contract checks, JSX syntax,
and the native `AVLayer.replaceSource()` regression. This is strong regression evidence but
is not a substitute for native After Effects execution.

## Remaining S6 gate

- Obtain independent clean full-PR review at the exact final head plus green CI before merge;
  verify post-merge develop CI.
- Execute the manual AE workflow and inspect V001→V002→V003, Build/QC after revision,
  save/reopen behavior, and property preservation in a real supported After Effects host.

Keeping mock layer objects and their non-source properties unchanged is tested. Native AE
property preservation, real revision execution, GUI/undo behavior and Blender→AE end-to-end
remain **MANUAL NOT EXECUTED**. S7 has not started.
