> **SUPERSEDED by finding-07 (2026-10-04).** This is the simulation loop (verdict H0). The
> RQ-RESIST question was later re-settled on real data under a lag-searching adversary; see
> `finding-07-artifact-caught.md` for the current headline. Retained for the audit trail.

# Finding-01 — anon-baserate, first complete loop (confirmatory RQ-RESIST)

> Simulated substrate (Tor/SOR grounded sim; VPN sim pending real capture). Parameters are
> ASSUMPTIONS to be re-fit from real capture at stage 05. Decision rule is the FROZEN one.

## Result (seed 20261003, n_runs=30, FPR=1%, base rate b=1e-3)

| arm | TPR@1% | precision@b | bw overhead | role |
|---|---|---|---|---|
| VPN | 0.982 | 0.0895 | 0.00 | positive control |
| Tor | 0.415 | 0.0398 | 0.00 | comparator |
| SOR | 0.474 | 0.0452 | 0.60 | system under study |

- **Positive-control check PASS:** VPN is the most linkable arm — the correlator fires when
  linkage is trivial, so a low score elsewhere is resistance, not a broken instrument.
- **Base-rate contribution (RQ-POS):** every arm's balanced-looking detection (TPR 0.4–0.98)
  collapses to precision < 0.09 at the honest base rate. Balanced evaluation overstates
  operational linkability by ~10×. This is the frontier-map point.
- **RQ-RESIST (confirmatory): VERDICT = H0 (reportable null).** Paired gap TPR(Tor)−TPR(SOR)
  = −0.058, 95% CI [−0.104, −0.014], margin delta = 0.08. SOR is **not** meaningfully more
  resistant than Tor; the point estimate even trends slightly worse.

## Why this is a result, not a failure (nulls are results)

SOR's volume padding (bw overhead 0.60) did **not** buy resistance over Tor against a
timing-structured correlator. This aligns with the traffic-analysis literature: volume-only
defenses are weak against timing-based attacks; effective defenses perturb *timing*, not just
*volume*. The sim's padding is a constant-ish volume offset, which Pearson timing correlation
largely sees through.

## The result CHANGES THE NEXT DECISION (loop reopens -> new sealed iteration)

The lab's next experiment, justified by this result:
1. **Re-fit the padding model from real SOR captures** (stage 05) — is the null a model
   artifact or real?
2. **Add a timing-perturbation defense arm** (delay jitter, not just volume padding) and test
   whether *that* moves SOR's frontier position — the hypothesis this null points to.
Both are a NEW sealed iteration, never a backward edit of this one.

## Honesty / validation still needed

Simulated data; VPN not yet real-captured; parameters are assumptions. Real-network and
real-hardware validation is the stated ultimate next step (prereg §14).
