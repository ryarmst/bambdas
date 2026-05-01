---
name: Webpack Module Federation Share-Scope Manifest Exposed
type: SCAN_CHECK_PASSIVE_PER_REQUEST
gate: bambda-js-dependency-scanning
summary: Detects webpack 5 Module Federation share-scope manifests and reports exposed package names and versions; elevates to MEDIUM if any @scope is absent from the known-public npm scope allowlist, flagging it as a dependency confusion candidate.
---

## Globals

| Global | Default | Type | Purpose |
|---|---|---|---|
| `bambda-js-dependency-scanning` | `false` | `gate` | Master on/off switch |
| `js-dep-cluster-threshold` | `3` | `sensitivity` | Minimum distinct package matches required to fire (prevents false positives from coincidental semver-shaped strings in unrelated minified code) |
| `js-dep-max-matches` | `200` | `depth` | Cap on share-scope regex matches processed per response |

## Notes

- Fires at `LOW` when all detected scoped packages are in the allowlist; `MEDIUM` when any `@scope` is absent.
- Extend the public allowlist by adding known-safe scopes to the `PUBLIC_SCOPES` `Set` in the source.
- Raise `js-dep-cluster-threshold` to 5 or higher if the check fires on non-federation bundles at your target.
- Scoped packages whose scope is already in `PUBLIC_SCOPES` are listed in the package inventory but do not contribute to severity.
