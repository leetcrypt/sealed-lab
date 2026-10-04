# ⛔ RETRACTED / SUPERSEDED by finding-07 (2026-10-04)

The "SOR more resistant than Tor" claim below (even in its downgraded "suggestive/directional"
form) is **RETRACTED**. A lag-searching re-score showed SOR's TPR=0 was a timing-alignment
artifact of the extra relay hop + a lag-blind correlator; under a competent adversary SOR is
linkable (TPR 0.275) and **Tor is the most resistant arm**. The current headline is
`finding-07-artifact-caught.md`. The correction note and body below are retained for the audit
trail only — they are no longer the lab's position.

---

# ⚠ CORRECTION (verification-driven, 2026-10-04)

An independent verification agent (report: `VERIFICATION-REPORT.md`) confirmed the numbers,
the scorer, and that SOR's TPR=0 is a REAL effect — but caught an **OVERCLAIM**. Corrections:

1. **Downgrade "confidently more resistant" → "more resistant, directional/SUGGESTIVE."** The
   gap CI is [0.07, 0.21], which excludes zero (SOR *is* distinguishable from Tor), but the
   lower bound 0.07 is **below the materiality margin δ=0.08** — so the data cannot confirm the
   advantage is *material*. Verdict: SOR more resistant than Tor, directionally; NOT a settled
   confirmatory-at-margin result.
2. **Power/threshold conflation (fixed in interpretation).** `design_check`'s power 0.965 and
   the 0.13 threshold are for the PLANNED *paired precision-gap* design at n=30. The real data
   is an *unpaired TPR-gap* analysis at n=10. These are different metrics; the sd_run comparison
   is not apples-to-apples. The PAIRED campaign (running) produces the matching metric.
3. **Degenerate SOR arm.** SOR SD=0, so the CI width is driven by Tor alone (effectively a
   one-sample statement about Tor). The paired analysis addresses this.
4. **"bin-0 collapse" explained (not synthesis).** The sink bins relative to its own first-byte
   t0; nested-SSH delivers the buffered burst immediately after connect, so it lands in bin 0.
   Real artifact of first-byte-relative binning + SSH burst delivery. WG run AUCs vary (SD 0.036);
   the mean matching finding-03's single capture to 4 d.p. is coincidence.

**Net:** suggestive/directional evidence that SOR > Tor; the clean PAIRED n=30 battery (in
progress) is required before any confirmatory-at-margin claim. The body below is retained with
this correction overriding its "confidently/confirmatory" wording.

---

# Finding-06 — REAL confirmatory-grade result (repeated campaign)

> 35 real capture runs (WG 15, Tor 10, SOR 10), own-fleet, SOR relayed via grok-bot (stable,
> no mobile confound). Aggregate: `aggregate-real.json`. Deviations: `deviations-real.md`.
> **Status: confirmatory-grade under a logged deviation (D-real-1, unpaired).**

## Per-arm (mean ± SD across runs)

| arm | detection @1% FPR | linkage AUC | latency | n |
|---|---|---|---|---|
| WireGuard (1-hop) | 0.69 ± 0.10 | 0.92 ± 0.04 | 7.8 ms | 15 |
| Tor (real 3-hop onion) | 0.14 ± 0.11 | 0.76 ± 0.03 | 1048 ms | 10 |
| SOR (2-hop nested SSH) | 0.00 ± 0.00 | 0.43 ± 0.06 | — (artifact) | 10 |

## RQ-RESIST — confirmatory verdict: H1

Gap TPR@1%(Tor) − TPR@1%(SOR) = **0.13**, 95% CI **[0.07, 0.21]** (excludes zero), δ=0.08.
**SOR is confidently more resistant to end-to-end correlation than Tor** on real traffic.

- **The sealed assumption HELD.** Measured run-to-run spread = **0.112 ≤ 0.13** threshold, so
  the design does NOT return to stage 03. Re-running `design_check` with the measured spread
  still PASSES (power 0.965) — `design_check-refit.txt`.
- **Mechanism:** nested SSH buffers each flow into ~1 timing bin (TCP-over-TCP), collapsing the
  fingerprint. Survives the move to a stable relay, so it is a transport property, not a mobile
  artifact.

## This supersedes the sim and the pilot (honestly)

The simulation returned a null (H0); the real repeated campaign returns H1. The earlier n=20
pilot was exploratory; this is confirmatory-grade. The upgrade is driven by DATA, not by
re-labeling. **Caveats preserved:** D-real-1 (unpaired → conservative test used), D-real-2
(latency artifact), n<30 per arm, CI lower bound (0.07) just under δ. The clean PAIRED n=30
battery is the last mile.
