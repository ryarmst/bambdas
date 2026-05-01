---
name: 403 Forbidden Bypass — Comprehensive Probe Suite
type: SCAN_CHECK_ACTIVE_PER_REQUEST
gate: bambda-active
summary: Probes eight bypass categories against any 403 base response — IP spoofing (15 headers), IP encoding variants (10 alternative loopback representations), path override headers (X-Original-URL/X-Rewrite-URL), path mutations (prefix/suffix/wrap/case), HTTP method alternatives, method override headers, Referer injection, and host/protocol spoofing — reporting any 2xx result as HIGH/FIRM.
---

## Globals

| Global | Default | Type | Purpose |
|---|---|---|---|
| `bambda-active` | `false` | `gate` | Master gate |
| `bypass-403-ip-value` | `127.0.0.1` | `sensitivity` | Primary loopback value injected into all IP-spoofing headers (Group A) |

## Notes

- Only runs when the base response is exactly 403; skips all other status codes.
- A 2xx bypass is reported HIGH/FIRM — manually verify the response body grants real access vs. returning a login redirect or error page with a 200 wrapper.
- Group A tests 15 distinct IP headers each with `bypass-403-ip-value`; Group B tests 10 alternate encodings of loopback (decimal, hex, octal, localhost, abbreviated) on `X-Forwarded-For` to bypass string-matching filters.
- Path override headers (Group C) are tested in two variants each: original path preserved (middleware-intercept pattern) and path rewritten to `/` (framework-routing pattern).
- Path mutations cover ~25 variants including Unicode fullwidth slash (`%ef%bc%8f`), double-encoded dot (`%252e`), semicolon path parameters, dot-dot semicolon (Spring bypass), null byte, and extension spoofing.
- Method override headers (Group F) skip the current request method to avoid redundant probes.
- Each scan invocation generates a unique random trailing segment for the "trailing random segment" path mutation — results will vary between scans.
