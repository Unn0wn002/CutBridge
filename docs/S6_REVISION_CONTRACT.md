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
- Required/optional **status** changes for a pass that exists in both revisions warn and require
  explicit confirmation. Pass-set changes do not use that warning path: removing either a
  required or optional pass blocks source-only revision, and adding a pass also blocks. Use a
  deliberate rebuild/migration workflow for pass-set changes. This fail-closed rule was added
  after #26 proved that retaining a removed optional layer with its prior-version ownership tag
  makes the newly migrated project internally inconsistent with the #23/#24 stale-layer rules.

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

The S6 panel must also call helpers through the exported contract boundary. The repeated
host-shaped revision lifecycle exposed a real scoping defect where outer panel code called the
private `zeroPad()` helper directly, producing `ReferenceError: zeroPad is not defined` before
V002 confirmation. The formatter is now exported as `CutBridgeContract.zeroPad`, and the outer
revision path uses the namespaced helper for replacement names, confirmation text and success
messages. Static coverage guards against reintroducing the bare out-of-scope calls.

The `ownershipKey` includes the collision-safe cut tuple, numeric version, package name
and pass. It is verification context, not a replacement tag format for existing S5
comments.

## Package structure and ownership

The package root name by itself is never ownership proof. Existing managed project structure
must be uniquely resolvable before CutBridge reuses it. The shared read-only resolver requires:

1. exactly one matching top-level package root;
2. exactly one each of `01_COMP`, `02_RENDER`, `03_PRECOMP`, and `04_OUTPUT` directly under
   that root; and
3. operation-specific managed-object ownership checks after structure resolution.

For Build reuse, exactly one item must carry the expected current managed-comp tag and that item
must be the correctly named `CompItem` inside the unique `01_COMP` folder. Missing, duplicated,
or misplaced deterministic structure is treated as package drift, not permission to repair the
project implicitly. Build fails before creating folders, comps, footage, or layers.

Revision adapter construction uses the same unique root/folder resolver rather than a first-match
lookup. Therefore duplicate current package roots or duplicate deterministic children block before
confirmation, replacement import, or `replaceSource()`. Native-host-shaped regression coverage
injects a duplicate current root and a duplicate `02_RENDER` between V002 and V003 and verifies
that layer source, footage count, replacement-call count, confirmation count, and current root name
remain unchanged.

QC preserves package-only operation when no matching managed root exists. Once a matching managed
root exists, QC also uses the strict unique resolver. A missing `03_PRECOMP` or duplicate
`02_RENDER` therefore cannot be silently evaluated through an arbitrary first match or produce a
false QC PASS. The host-shaped structure regression verifies QC remains read-only and reports the
structural error for both cases.

QC also validates the current managed-layer state for every complete pass after managed footage
has been verified. It uses the same strict `findManagedLayer()` resolver as Build, including exact
current tag, expected comp membership, exact managed footage source, duplicate-tag rejection,
cache/live-object checks, and refusal to adopt an unmanaged layer merely because its name or source
matches. A required complete pass with a deleted or de-tagged/ambiguous managed layer is a QC error.
A complete optional pass with no layer is a warning when ownership is otherwise unambiguous. If an
optional pass source sequence is unavailable, QC keeps the documented optional warning/skip path
rather than generating a separate layer hard error. #27 added this contract after a regression
proved that the previous QC could report clean PASS with valid footage and comp even after the
required BEAUTY managed layer had been deleted.

S5 did not claim the package-root `comment`, so S6 preserves unmanaged root comments during
revision. Only an exact prior CutBridge root tag is migrated; artist/studio notes remain intact.

The native adapter preserves provenance across supported same-pass-set revisions: the active layer
and replacement footage receive the candidate package/version tags, while retired CutBridge
footage retains its previous version-scoped CutBridge tag. Retired footage is removed from
current-version caches but is not converted into an unmanaged item. This allows historical footage
to remain available for artist references without weakening S5's unmanaged-collision protections.
Rollback restores the exact pre-revision root/comp/layer/footage comments and names recorded
before migration.

## Transaction and recovery

1. Prepare validates manifests, pass-set compatibility, required managed-layer coverage,
   duplicate records/handles, unique current package structure, and live ownership/source
   associations. Unsupported pass addition/removal stops here before confirmation or mutation.
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

The exact current candidate SHA and authoritative green CI run are intentionally maintained in
PR #15 and blocker issues #19/#20 rather than duplicated here, because any documentation commit
changes the candidate SHA.

Static validation includes:

- the complete pytest selection for static/release/AE contract/S5/S6 coverage;
- S5/S6 host-shaped ownership regressions;
- V001→V002→V003 revision lifecycle through the actual `CutBridge.jsx` adapter;
- Build/QC after revision and script reload;
- the #26 optional-pass lifecycle regression, which first reproduced the stale-layer failure and
  now proves optional-pass removal blocks before confirmation/import/source swap/root migration,
  leaving the original package coherent for reload, Build and QC;
- the #27 QC current-layer regression, which first reproduced a clean QC PASS after deleting a
  required managed layer and now verifies required deletion/de-tagging fails closed, a complete
  optional missing layer warns, and an unavailable optional source remains warning/skip only;
- read-only `AVLayer.source` with `replaceSource(..., false)` as the source mutation path;
- package-root artist-note preservation and same-name root collision rejection;
- Build/QC rejection of missing/duplicate deterministic folders without mutation;
- revision rejection of duplicate current root/folder before confirmation/import/source swap;
- deterministic release-package simulation and checksum verification;
- S6 Node contract checks; and
- ExtendScript/JSX syntax validation.

The Blender job includes the official bpy 5.2 registration → unregistration → re-registration
lifecycle and complete Blender integration suite. This is strong regression evidence but is not
a substitute for native After Effects execution. The final documentation review head must also
have green exact-head CI; PR #15 records that final review SHA/run.

## Remaining S6 gate

- Obtain independent clean full-PR review at the exact final head plus green CI before merge;
  verify post-merge `develop` CI.
- Execute the manual AE workflow and inspect V001→V002→V003, Build/QC after revision,
  save/reopen behavior, property preservation, fail-closed pass-set removal, and required/optional
  managed-layer QC behavior in a real supported After Effects host.

Keeping mock layer objects and their non-source properties unchanged is tested. Native AE
property preservation, real revision execution, GUI/undo behavior and Blender→AE end-to-end
remain **MANUAL NOT EXECUTED**. S7 has not started.
