---
name: Webpack Internal Chunk Name Disclosed
type: SCAN_CHECK_PASSIVE_PER_REQUEST
gate: bambda-js-dependency-scanning
summary: Detects webpack bundle responses where the webpackChunk<appname> global leaks an internal application or team identifier; fires at INFORMATION/FIRM on any JavaScript response containing a non-generic chunk name.
---

## Globals

| Global | Default | Type | Purpose |
|---|---|---|---|
| `bambda-js-dependency-scanning` | `false` | `gate` | Master on/off switch |

## Notes

- Names of 4 or fewer characters and the literal `webpackJsonp` are excluded as too generic.
- Fires independently of whether a Module Federation share-scope manifest is present; the chunk name leak exists in all webpack 5 bundles, not just federation remotes.
- Severity is always `INFORMATION` — the finding is useful for recon and issue confirmation, not as a standalone vulnerability.
