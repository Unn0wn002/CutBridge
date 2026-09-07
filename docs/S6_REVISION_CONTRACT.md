# S6 Revision Contract

The S6 manager is intentionally a preflight-and-transaction boundary, not a blind project rebuild.

## Contract

- Revision identity is the package identity (or project/episode/scene/cut/take tuple); mismatches block.
- Only schema `cutbridge-manifest` version 1 is accepted by this manager.
- A candidate must be numerically newer. V001, V002 and V003 are ordered by their numeric revision.
- FPS, frame range/count, and pixel aspect changes block because this implementation cannot safely retime an existing AE comp.
- Resolution changes are supported only as a warning and require explicit user confirmation; existing layer geometry is not rewritten.
- Removing a previously required pass blocks. Removed optional passes are not deleted.
- A replacement plan selects only objects whose CutBridge managed tag exactly matches the current package/pass. Manual footage, layers, comps, and ordering are excluded.
- Applying a plan imports replacement footage, validates it through the host adapter, swaps only the selected managed layer sources, and removes only newly imported replacements if the transaction fails.
- Preservation is achieved by retaining existing managed layer objects and changing only their source. Native AE preservation of every property is not claimed until manual validation.

The host adapter boundary is deliberately explicit so native AE behavior can be tested separately without allowing the pure contract tests to imply GUI success.
