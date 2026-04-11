# bambdas

Custom Burp Suite Bambda scripts (scan checks, filters, actions). All `.bambda` files are kept at the root level for bulk import compatibility — Burp's importer does not recurse into subdirectories.

**Bulk import:** Extensions → Custom scan checks → (gear) → Import → select this directory.

---

## Scan Checks

| File | Description |
|---|---|
| [AnomalyRankedInjectionProbe.bambda](AnomalyRankedInjectionProbe.bambda) | Active, per insertion point. Sends a payload corpus, ranks responses with `RankingAlgorithm.ANOMALY`, and raises MEDIUM/TENTATIVE only when two gates pass: absolute rank threshold and margin over median. Payloads loaded from a file via system property `anomaly.probe.wordlist`, falling back to URL-encoded ASCII specials. See [AnomalyRankedInjectionProbe.md](AnomalyRankedInjectionProbe.md). |
