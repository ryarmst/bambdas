# Bambda Summary

Generated from bambda `.md` files. Run `./generate-summary.sh` to regenerate.

| Name | Type | Gate | Summary |
|---|---|---|---|
| Anomaly-Ranked Injection Probe | `SCAN_CHECK_ACTIVE_PER_INSERTION_POINT` | `gate-fuzzing` | Sends a payload corpus per insertion point, ranks all responses with Burp's ANOMALY algorithm, and raises MEDIUM/TENTATIVE only when both an absolute rank threshold (Gate 1) and a margin-over-median ratio (Gate 2) pass — suppressing false positives from WAFs and uniformly-noisy targets. |
| 403 Forbidden Bypass — Comprehensive Probe Suite | `SCAN_CHECK_ACTIVE_PER_REQUEST` | `gate-active` | Probes eight bypass categories against any 403 base response — IP spoofing (15 headers), IP encoding variants (10 alternative loopback representations), path override headers (X-Original-URL/X-Rewrite-URL), path mutations (prefix/suffix/wrap/case), HTTP method alternatives, method override headers, Referer injection, and host/protocol spoofing — reporting any 2xx result as HIGH/FIRM. |
| Webpack Internal Chunk Name Disclosed | `SCAN_CHECK_PASSIVE_PER_REQUEST` | `gate-js-dependency-scanning` | Detects webpack bundle responses where the webpackChunk<appname> global leaks an internal application or team identifier; fires at INFORMATION/FIRM on any JavaScript response containing a non-generic chunk name. |
| Webpack Module Federation Share-Scope Manifest Exposed | `SCAN_CHECK_PASSIVE_PER_REQUEST` | `gate-js-dependency-scanning` | Detects webpack 5 Module Federation share-scope manifests and reports exposed package names and versions; elevates to MEDIUM if any @scope is absent from the known-public npm scope allowlist, flagging it as a dependency confusion candidate. |
| Webpack Bundle Likely-Internal Package Names | `SCAN_CHECK_PASSIVE_PER_REQUEST` | `gate-js-dependency-scanning` | Applies naming heuristics to unscoped packages found in webpack Module Federation share-scope manifests to surface likely-internal or proprietary package names; always reports at MEDIUM/TENTATIVE due to elevated false-positive rate. |
