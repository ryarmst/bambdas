# Anomaly-Ranked Injection Probe

Active scan check (`SCAN_CHECK_ACTIVE_PER_INSERTION_POINT`). Sends a diverse payload corpus to each insertion point, ranks every response — including the unmodified baseline — using Burp's `RankingUtils` / `RankingAlgorithm.ANOMALY`, and raises a **MEDIUM / TENTATIVE** finding only when two independent gates both pass.

## How to import

This is a `.bambda` file (YAML wrapper around a Java source body). **Do not paste the file contents into Burp's scan check editor** — the YAML header is not valid Java and will produce spurious syntax errors such as:

```
Syntax error on token "Injection", instanceof expected
Anomaly cannot be resolved to a variable
```

Import via: **Extensions → Custom scan checks → (gear icon) → Import**

To edit the source after importing, open the check in the editor and modify only the Java body.

## Two-gate design

A single absolute threshold produces two failure modes on real targets:

| Scenario | Single threshold behaviour | Two-gate behaviour |
|---|---|---|
| WAF / CDN returns a uniform block page for most payloads | Every blocked response clears the bar → false positives | Margin collapses to ~1.0x → Gate 2 suppresses |
| Consistent target with one genuinely anomalous response | Low absolute rank → silent | Gate 1 passes at a low threshold; Gate 2 confirms the outlier stands apart |

**Gate 1 — absolute:** `topRank >= RANK_THRESHOLD`  
Filters out background noise on targets where all responses are structurally similar.

**Gate 2 — margin:** `topRank >= MIN_MARGIN_OVER_MEDIAN * medianRank`  
Filters out false positives on targets where all responses are structurally unusual. When every payload triggers a weird response the margin collapses toward 1.0x and no finding fires.

## The `rank()` integer scale

`RankedHttpRequestResponse.rank()` returns an `int`. The scale is internal to Burp and is not publicly documented. Key properties:

- Higher value = more anomalous *within the current corpus*.
- Scores are corpus-relative: a `topRank` of 8 on one target does not mean the same thing as 8 on another.
- The range observed in practice varies with corpus size and application behaviour. Treat `RANK_THRESHOLD` as an empirically-tuned value, not an absolute.

## Calibrating `RANK_THRESHOLD`

`RANK_THRESHOLD` defaults to `5`. Calibrate it against your specific target:

1. Enable the check and scan a target with **no injection vulnerabilities** (a static asset server, a read-only API, a hardened staging environment).
2. Open **Extensions → Output** and observe the `topRank` values logged per insertion point.
3. Find the highest `topRank` where `raised=no` across all insertion points — this is the noise floor.
4. Set `RANK_THRESHOLD` to approximately 120–150% of that noise floor.  
   _Example: noise floor `topRank=3` → set `RANK_THRESHOLD = 4` or `5`._
5. Re-scan a known-vulnerable target and confirm `raised=YES` on the expected parameters.

Re-run this calibration if you change the payload corpus substantially or move to a very different class of target.

## Tuning `MIN_MARGIN_OVER_MEDIAN`

Default is `2.0`. Adjust based on what you see in the output log.

**Raise toward `3.0` when:**
- A WAF or CDN returns a uniform block page for most payloads, producing many false positives even though Gate 1 passes.
- The application throws exceptions or returns error pages for a wide variety of inputs by design (debug mode, immature input handling).
- `raised=YES` is frequent but manual review shows no real vulnerabilities.

**Lower toward `1.5` when:**
- You see `raised=no` on parameters you have confirmed are vulnerable. Check the log: if `topRank` passes Gate 1 but `margin` fails Gate 2, the genuine anomaly is present but the median is also elevated.
- The target returns very consistent, uniform responses for all inputs, so even a small structural difference produces a meaningfully elevated rank relative to the median.

A useful calibration sweep: run the same scan with `MIN_MARGIN_OVER_MEDIAN` set to `1.5`, `2.0`, `2.5`, and `3.0` and compare the output logs. Pick the value where `raised=YES` correlates with parameters that show interesting behaviour on manual inspection.

## Managing the payload corpus

Payloads are passed verbatim to `insertionPoint.buildHttpRequestWithPayload()`, which applies context-appropriate encoding automatically (URL-encoding for query params, JSON-escaping for body JSON fields, etc.). **Do not pre-encode payloads.**

### Adding payloads

Append entries to the `PAYLOADS` list. Group related payloads with a `// ──` category comment to keep the list readable. Increasing the corpus improves coverage but multiplies scan traffic: total requests ≈ insertion points × `min(PAYLOADS.size(), MAX_PAYLOADS_PER_INSERTION_POINT)`.

### Removing payloads

Delete the line. **Always keep at least one known-benign control entry** (`"safe_control_string"`). Without a control, the ranker compares only attack payloads against each other. If they all trigger similar responses (e.g. all blocked by a WAF), the boundary entries will appear anomalous relative to each other and inflate scores, defeating the margin gate.

### Corpus diversity

Keep the corpus **diverse rather than deep in any one category**. Thirty SQLi variants that all trigger the same WAF block page produce a uniform corpus where no entry stands out — the margin gate correctly suppresses any finding, but you also lose signal. Mix SQL, command injection, path traversal, SSTI, and structural edge cases (oversized, null byte, unicode) to maximise the chance that a genuine server-side reaction is structurally distinct from the rest of the corpus.

## Reading the output log

Each insertion point produces one log line under **Extensions → Output**:

```
[AnomalyProbe] userId                          PARAM_URL              payloads=25  topRank=12  median=2.0  margin= 6.00x  gate1=PASS gate2=PASS  raised=YES
[AnomalyProbe] csrfToken                       PARAM_BODY             payloads=25  topRank= 4  median=3.0  margin= 1.33x  gate1=fail gate2=fail  raised=no
[AnomalyProbe] X-Forwarded-For                 HEADER                 payloads=25  topRank= 6  median=3.5  margin= 1.71x  gate1=PASS gate2=fail  raised=no
```

- `gate1=PASS gate2=fail` → absolute rank is above the threshold but the anomaly is not distinct enough from the median. Common on noisy targets; consider raising `MIN_MARGIN_OVER_MEDIAN`.
- `gate1=fail gate2=PASS` → large relative spread but the absolute rank is low; consider lowering `RANK_THRESHOLD`.
- Both fail → corpus is uniform (all responses look similar). The check is working correctly; no injection signal present.
