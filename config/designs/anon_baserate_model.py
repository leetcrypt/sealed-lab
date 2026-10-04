"""Generative model + pre-registered decision rule for the `anon-baserate` design.

Confirmatory RQ-SHIFT (the falsifiable headline): on the SAME captured flows, does a
LEARNED end-to-end linkage adversary achieve higher linkage precision — at the
pre-registered honest base rate b — than a CLASSICAL one, by at least the margin delta?
If yes, the AI adversary has bent a transport's position on the anonymity trilemma inward.

Design: paired by run (the run is the resampling unit, per rigor-standards.md). Each run
yields one paired precision gap  g = precision_learned - precision_classical  at base rate
b (projected analytically from that run's TPR/FPR). The DV is the mean run-level gap.

Contract (design_check.py): simulate()/decide(); verdict in {H1, H0, inconclusive}.

Pre-registered decision rule — cluster-bootstrap 95% CI on the mean gap:
  H1  (inward shift under AI)      CI lower bound > 0
  H0  (shift negligible, reportable null)   CI upper bound < delta
  inconclusive                     otherwise
"""
from __future__ import annotations

CONF = 0.95
RESAMPLES = 500


def simulate(rq, effect, rng, HELPERS):
    """One synthetic experiment: n_runs paired precision gaps under a true mean `effect`.

    The run is the resampling unit, so a run-level draw already carries the between-run
    variance the bootstrap will see; sd_run is that run-to-run SD (a nuisance parameter
    to be re-fit from the rho-pilot before freeze)."""
    n = int(rq["n_runs"])
    sd = float(rq["sd_run"])
    gaps = [rng.gauss(effect, sd) for _ in range(n)]
    return {"gaps": gaps}


def decide(rq, obs, rng, HELPERS):
    gaps = obs["gaps"]
    delta = float(rq["delta"])
    lo, hi = HELPERS["cluster_bootstrap_ci"](gaps, CONF, RESAMPLES, rng)
    info = {"ci_halfwidth": (hi - lo) / 2.0, "ci_lo": lo, "ci_hi": hi}
    if lo > 0.0:
        return ("H1", info)          # adversary shift is confidently positive
    if hi < delta:
        return ("H0", info)          # confidently bounded below the margin => negligible
    return ("inconclusive", info)
