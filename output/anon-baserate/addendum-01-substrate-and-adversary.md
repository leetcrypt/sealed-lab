# Addendum-01 — substrate + adversary decision (anon-baserate)

- **Parent prereg:** `prereg-anon-baserate.md` (sealed `2d92bcda…`). The parent is **not
  edited**; this addendum is sealed separately. Both verify.
- **Date:** 2026-10-03 · **Pre-data:** no capture or score has been produced. This is a
  resource/feasibility decision made before any data exists, not a response to results.

## Decisions

1. **Substrate = hybrid.** Real capture for the **VPN arm** (cheapest, the positive
   control) as a proof-of-concept; **grounded simulation** for Tor and SOR, parameterized by
   each transport's latency / jitter / padding characteristics (from measurement + literature).
   The brief explicitly admits simulation and self-generated data as valid experiments.
2. **Adversary = classical only, self-contained.** A clean normalized cross-correlation
   scorer authored in this repo and validated by `instrument_check`. The learned adversary
   (A-learned) is **deferred**.

## Consequence for the research questions (per parent §8 selection rule)

- **RQ-SHIFT → EXPLORATORY.** It requires two adversaries; with classical-only it cannot be
  confirmatory. The parent §8 rule anticipated exactly this.
- **RQ-BASERATE → confirmatory primary (new).** *Does evaluating at the honest base rate
  materially change a transport's apparent linkability vs balanced evaluation, by at least
  `delta`?* DV per arm = `precision@balanced − precision@base-rate`, paired by run.
  - H1: balanced evaluation overstates linkability by ≥ `delta` (the base-rate fallacy bites).
  - H0 (reportable null): the overstatement is bounded below `delta` (a highly resistant arm
    with near-zero FPR shows little base-rate gap) — this is why RQ-BASERATE is **not**
    tautological: the sign is expected, the *magnitude* discriminates transports.
- **RQ-POS** unchanged (descriptive frontier map).

## Design arithmetic is unchanged

RQ-BASERATE reuses the parent's paired-gap design exactly: run is the resampling unit,
`n_runs=30`, `delta=0.08`, `sd_run=0.10` (same assumption + same return-to-03 rule at >0.13),
same cluster-bootstrap decision rule. The generative model is interpretation-agnostic, so the
`design_check` PASS 10/10 (`design_check-PASS.txt`) carries over. Re-verified this addendum.

## Validation still needed (unchanged)

Real captures for all three arms on real networks/hardware; the learned adversary for
RQ-SHIFT. Stated as the ultimate next step in the parent §14.
