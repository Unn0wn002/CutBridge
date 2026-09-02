# Contributing

Use `develop` for active integration and create focused `feature/*` branches for isolated work.

Before opening a pull request:

1. Run `pytest -q`.
2. Check the After Effects JSX syntax.
3. Keep changes scoped to one feature or fix.
4. Update tests and documentation when behavior changes.
5. Do not commit generated ZIPs, local output packages, client assets, or credentials.

Prefer pull requests into `develop`. Promote a tested release candidate from `develop` to `main`.
