# Addendum-02 — confirmatory DV correction (anon-baserate)

- **Parents:** `prereg-anon-baserate.md` (`2d92bcda…`), `addendum-01…` — neither edited;
  this is sealed separately. **Pre-data:** no capture or score exists yet.
- **Date:** 2026-10-03. This corrects a degenerate DV caught *before* any data — the gate
  discipline working as intended, not a post-hoc change.

## The flaw caught

Addendum-01 set the confirmatory DV to `precision@balanced − precision@base-rate`. At an
honest base rate `b=0.001`, that gap is large for **every** arm (precision at base rate is
dominated by the false-positive term regardless of the transport), so the DV cannot
discriminate transports and its null world (gap ≈ 0) never occurs in reality. It is
effectively tautological in practice. Rejected.

## Corrected confirmatory DV (RQ-RESIST)

**RQ-RESIST (confirmatory primary).** At the honest base rate `b`, is **SOR more resistant
to end-to-end linkage than Tor**, measured as the paired per-run difference in linkage
precision at a fixed FPR operating point:  `Δ = precision@b(Tor) − precision@b(SOR)`.
- H1: SOR is meaningfully more resistant (CI lower bound on mean Δ > 0, i.e. Tor is linked
  more precisely than SOR) by at least `delta`.
- H0 (reportable null): SOR is **not** meaningfully more resistant than Tor (CI upper
  bound < `delta`). Genuinely uncertain — SOR could fail to beat Tor. Falsifiable.
- **VPN** stays the **positive control**: its precision@b must be the highest of the three,
  confirming the correlator fires when linkage is trivial. VPN is not in the confirmatory test.

## Design arithmetic unchanged

Paired by run; run is the resampling unit; `n_runs=30`, `delta=0.08`, `sd_run=0.10`
(same assumption + return-to-03 rule at >0.13); same cluster-bootstrap decision rule. The
`design_check` generative model is a paired-gap model and is agnostic to which two arms the
gap is between, so the PASS 10/10 carries over (re-verified: `design_check-PASS.txt`).

## RQ-SHIFT, RQ-POS

RQ-SHIFT remains EXPLORATORY (needs the learned adversary). RQ-POS (per-arm frontier
position at base rate `b`, with CIs) remains the descriptive map.
