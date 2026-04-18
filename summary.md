# Bambda Summary

Generated from bambda `.md` files. Run `./generate-summary.sh` to regenerate.

| Name | Type | Summary |
|---|---|---|
| Anomaly-Ranked Injection Probe | `SCAN_CHECK_ACTIVE_PER_INSERTION_POINT` | Sends a payload corpus per insertion point, ranks all responses with Burp's ANOMALY algorithm, and raises MEDIUM/TENTATIVE only when both an absolute rank threshold (Gate 1) and a margin-over-median ratio (Gate 2) pass — suppressing false positives from WAFs and uniformly-noisy targets. |
| 403 Forbidden Bypass — Comprehensive Probe Suite | `SCAN_CHECK_ACTIVE_PER_REQUEST` | Probes eight bypass categories against any 403 base response — IP spoofing (15 headers), IP encoding variants (10 alternative loopback representations), path override headers (X-Original-URL/X-Rewrite-URL), path mutations (prefix/suffix/wrap/case), HTTP method alternatives, method override headers, Referer injection, and host/protocol spoofing — reporting any 2xx result as HIGH/FIRM. |
