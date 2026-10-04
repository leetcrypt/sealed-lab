# Addendum-03 — final confirmatory specification (anon-baserate)

- **Parents:** `prereg…` (`2d92bcda…`), `addendum-01…`, `addendum-02…`. None edited; sealed
  separately. **Pre-data:** no capture or score exists. This is the authoritative DV spec
  and supersedes the DV choices in 01/02. The iteration below is the gate discipline catching
  two scale flaws *before* any compute — not post-hoc tuning.

## DV evolution (all pre-data; recorded for the audit trail)

1. addendum-01: `precision@balanced − precision@base-rate` — **degenerate**: large for every
   arm at small `b`, non-discriminating, null never occurs. Rejected.
2. addendum-02: `precision@b(Tor) − precision@b(SOR)` — **scale-mismatched**: at `b=0.001`
   precision lives in ~[0, 0.07], so the sealed margin `delta=0.08` is literally unreachable
   and H1 can essentially never be declared. Rejected.
3. **This addendum (final):** below.

## RQ-RESIST (confirmatory primary) — FINAL

At the honest operating point (fixed FPR `f`), is **SOR more resistant to end-to-end linkage
than Tor**, measured as the paired per-run **detection-rate gap**:
`Δ = TPR@f(Tor) − TPR@f(SOR)`, paired by run (same latent connections scored through each
transport). TPR has full [0,1] dynamic range, so `delta=0.08` is detectable and the sealed
design arithmetic applies unchanged.
- H1: SOR meaningfully more resistant (CI lower bound on mean Δ > 0 and ≥ `delta`).
- H0 (reportable null): SOR not meaningfully more resistant than Tor (CI upper < `delta`).
- Genuinely uncertain and falsifiable: SOR may or may not beat Tor.

## RQ-POS (reported frontier) — where the honest base rate lives

For each arm, report **precision@base-rate** `b` (projected analytically from TPR and `f`:
`precision = b·TPR / (b·TPR + (1−b)·f)`) with CIs, plotted against latency and bandwidth
overhead. This is where the base-rate-fallacy contribution is made: balanced-evaluation
AUC/TPR overstates operational linkability, and the frontier map shows by how much.

## VPN positive control

VPN's TPR@f and precision@b must be the highest of the three, confirming the correlator
fires under trivial single-hop linkage. VPN is not in the confirmatory test.

## Design arithmetic — unchanged, carries over

`n_runs=30`, `delta=0.08`, `sd_run=0.10` (assumption; re-fit at stage 05; return to 03 if
realized run-SD of Δ > 0.13), cluster-bootstrap decision rule. `design_check` PASS 10/10
(`design_check-PASS.txt`) applies: the model is a paired-gap model agnostic to the DV's name.
