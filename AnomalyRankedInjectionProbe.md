---
name: Anomaly-Ranked Injection Probe
type: SCAN_CHECK_ACTIVE_PER_INSERTION_POINT
gate: gate-fuzzing
summary: Sends a payload corpus per insertion point, ranks all responses with Burp's ANOMALY algorithm, and raises MEDIUM/TENTATIVE only when both an absolute rank threshold (Gate 1) and a margin-over-median ratio (Gate 2) pass — suppressing false positives from WAFs and uniformly-noisy targets.
---

## Globals

| Global | Default | Type | Purpose |
|---|---|---|---|
| `gate-fuzzing` | `false` | `gate` | Master gate |
| `anomaly-probe-wordlist` | _(empty)_ | `resource` | Path to newline-delimited payload file; falls back to built-in %-encoded ASCII specials |
| `anomaly-probe-rank-threshold` | `5` | `sensitivity` | Gate 1: minimum anomaly rank to raise a finding |
| `anomaly-probe-margin` | `2.0` | `sensitivity` | Gate 2: top rank must be ≥ this multiple of the corpus median |
| `anomaly-probe-max-payloads` | `25` | `depth` | Payload cap per insertion point |
| `anomaly-probe-url-encode` | `false` | `encoding` | Set `true` to pass payloads raw (skip URL-decode step) |

## Notes

- Requires ≥3 corpus entries (baseline + 2 payloads) to run the ranker; silently skips otherwise.
- Baseline is always index 0 in the corpus — a baseline-wins result means no payload stood out.
- Gate 1 filters noise on uniform targets; Gate 2 collapses to ~1.0x when a WAF blocks most payloads, suppressing the finding.
- Payloads are URL-decoded before insertion by default so %-encoded wordlists aren't double-encoded; set `anomaly-probe-url-encode: true` to pass raw.
- Each insertion point logs one line to Extensions → Output: `topRank`, `median`, `margin`, and `raised`.
- Raise `anomaly-probe-margin` toward `3.0` to reduce false positives on noisy targets; lower toward `1.5` if confirmed-vulnerable parameters are being missed.
