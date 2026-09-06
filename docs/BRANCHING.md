# Branching

- `main`: stable / release-ready code.
- `develop`: integration branch.
- `feature/*` and `fix/*`: short-lived, focused work branched from current `develop`.
- `archive/*`: preserved historical state; never use as a development starting point.

Before editing, inspect live refs and compare `main` and `develop`. They may intentionally differ while integration work awaits promotion; record the exact commits and pending PRs instead of silently resetting either branch.

Merge verified changes through a PR into `develop`. Promote a tested release candidate separately to `main`. Prefer a merge commit when promoting so both branch histories remain connected; a squash merge can leave equivalent changes on divergent commit histories.

Before deleting old branches, record their exact tips and merged PRs and compare file trees with the integration commits. A merged PR alone is insufficient: later branch commits may never have been integrated. Preserve unique history in an archive before any deletion or rewrite.

Session 1 retained every old ref and recorded tree equivalence and the sole temporary-note difference in [the baseline audit](BASELINE_2026-09-06.md). No old branch needs to be merged into current `develop`.
