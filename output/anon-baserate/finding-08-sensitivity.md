# Finding 08 — Is the artifact flip robust, or a knife-edge?

**Question.** Finding-07's headline is a *flip*: under the naive lag-0 correlator the SOR arm
reads TPR = 0.00 (looks maximally unlinkable), but a lag-searching adversary recovers
substantial linkage (SOR TPR 0.275). If that only shows up at one `max_lag`/FPR setting it is
an analysis knife-edge, not a finding. We swept `max_lag ∈ {0,2,5,10,15}` ×
`FPR ∈ {0.005,0.01,0.02,0.05}` and re-computed mean TPR for every arm across all runs
(WG=15, Tor=10, SOR=10 runs). Full table: `sensitivity-result.txt` / `.json`.
Script: `experiment/real_lab/sensitivity.py` (stdlib; loads the real correlator and
`empirical_threshold` by path).

## Verdict: ROBUST across FPR, and gated by adversary lag-budget (not a knife-edge)

**1. SOR stays ~0 under the naive adversary at every FPR.** lag-0 SOR TPR = 0.000 / 0.000 /
0.000 / 0.005 at FPR 0.005 / 0.01 / 0.02 / 0.05. The "SOR looks perfectly resistant" reading
is not an artifact of a single FPR choice — it holds across the whole FPR grid.

**2. The rise is robust across FPR once the lag window is wide enough.** At `max_lag=10` SOR
TPR climbs to 0.180 / 0.275 / 0.370 / 0.480 across the four FPRs; at `max_lag=15`, 0.140 /
0.175 / 0.275 / 0.435. Every FPR operating point shows a large flip. The exact headline
number (0.275 at `max_lag=10`, FPR=0.01) reproduces.

**3. Important nuance — the flip needs a *sufficient* lag window.** At `max_lag=2` and `=5`
SOR TPR is still ≈0 (0.000–0.055). The jump only appears at `max_lag≥10`. This is physically
meaningful, not fragile: the SOR relay imposes a timing offset of roughly ~10 bins, so the
adversary must search a window wide enough to span it. The flip is therefore a property of
**adversary capability (lag budget)**, not an arbitrary knob — a competent end-to-end
adversary aligns for relay offset, and when it does, SOR's apparent resistance collapses.
A referee who reads "rises for any `max_lag≥2`" would be wrong; the honest claim is "rises
once `max_lag` spans the relay offset (~10 bins), and then does so at every FPR."

## Ranking stability

- **WG is the most linkable arm in every one of the 20 settings** (TPR 0.49–0.76). Rock solid.
- **Naive adversary (all FPR): WG > Tor > SOR** — SOR reads as the *most* resistant. This is
  the measurement artifact.
- **Lag-search with adequate budget (`max_lag`∈{10,15}, all FPR): WG > SOR > Tor** — the
  SOR/Tor order *inverts*; **Tor becomes the most resistant arm** (TPR 0.015–0.185). This is
  the corrected ordering and it holds across all four FPRs at both adequate lag windows.
- At `max_lag`∈{2,5} the order is still WG > Tor > SOR because the adversary has not yet
  overcome SOR's offset — consistent with nuance #3.

## Bottom line

The flip is **not a knife-edge of one FPR setting** — it is robust across the entire FPR grid.
It *is* conditional on the adversary's lag-search budget being large enough to span the SOR
relay's ~10-bin offset, which is the correct, physically-grounded condition rather than a
fragile analysis choice. The "SOR > Tor" naive result was an artifact of an under-powered
(lag-0 / narrow-lag) adversary; with a competent adversary, **Tor is the most resistant and
SOR is more linkable than it first appeared**, across FPR operating points.
