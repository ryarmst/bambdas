---
name: Webpack Bundle Likely-Internal Package Names
type: SCAN_CHECK_PASSIVE_PER_REQUEST
gate: bambda-js-dependency-scanning
summary: Applies naming heuristics to unscoped packages found in webpack Module Federation share-scope manifests to surface likely-internal or proprietary package names; always reports at MEDIUM/TENTATIVE due to elevated false-positive rate.
---

## Globals

| Global | Default | Type | Purpose |
|---|---|---|---|
| `bambda-js-dependency-scanning` | `false` | `gate` | Master on/off switch |
| `js-dep-max-matches` | `200` | `depth` | Cap on share-scope regex matches processed per response |

## Notes

- Four independent heuristics, any one is sufficient to flag a package:
  - **H1** (lowest FP): explicit keywords — `internal-`, `private-`, `-corp`, `-platform`, etc.
  - **H2** (broad): 2–5 char acronym-style prefix not in the known-public prefix denylist.
  - **H3a**: three or more consecutive uppercase letters embedded in the name (unusual in public npm packages, which are conventionally all-lowercase).
  - **H3b**: internal-platform substrings (`shared-ui`, `design-system`, `auth-client`, etc.) combined with a non-public-looking prefix.
- The `PUBLIC_PREFIXES` denylist suppresses H2 and H3b for common public ecosystems (react-, babel-, eslint-, etc.). Add entries there to reduce noise for your specific target stack.
- H2 is intentionally broad; expect false positives on short-prefixed utility packages. The `TENTATIVE` confidence is the design-level guard.
- Complements `WebpackFederationShareScope` — that check handles scoped packages; this one handles unscoped.
