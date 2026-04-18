# bambdas

Custom Burp Suite Bambda scripts (scan checks, filters, actions). All `.bambda` files are kept at the root level for bulk import compatibility — Burp's importer does not recurse into subdirectories.

**Bulk import:** Extensions → Custom scan checks → (gear) → Import → select this directory.

---

## Required extensions

| Extension | Purpose |
|---|---|
| [Extensibility Helper](https://github.com/joshspindler/extensibility-helper) | Streamlines discovery and bulk import of Bambdas and BChecks from a local Git repo directly into Burp. Use this instead of manually importing individual files. |
| [Burp Globals](https://github.com/ryarmst/Burp-Globals) | Stores named variables exposed as JVM system properties (`bg.<name>`). All Bambdas in this repo use a Burp Global gate to enable/disable execution, and read tunable parameters from globals rather than hardcoded constants. Import `globals.csv` via Burp Globals → Options → Import variables to provision all required globals at once. |

---

## Burp Globals

Import [`globals.csv`](globals.csv) to provision all required globals at once. See the CSV for the current list of globals, defaults, and types.

---

## Scan Checks

| File | Description |
|---|---|
| [AnomalyRankedInjectionProbe.bambda](AnomalyRankedInjectionProbe.bambda) | Active, per insertion point. Sends a payload corpus (from `anomaly-probe-wordlist` or built-in URL-encoded ASCII fallback), ranks responses with `RankingAlgorithm.ANOMALY`, and raises MEDIUM/TENTATIVE when both gates pass: absolute rank threshold and margin over median. Gated by `bambda-fuzzing`. See [AnomalyRankedInjectionProbe.md](AnomalyRankedInjectionProbe.md). |
