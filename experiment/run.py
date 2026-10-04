"""Run the anon-baserate experiment: generate -> score -> project -> frozen decision rule.
Deterministic (seed from the sealed prereg). Produces output/anon-baserate/result.json."""
from __future__ import annotations
import importlib.util, json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
def _load(name, rel):
    s = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

sub   = _load("substrate", "experiment/substrate.py")
dc    = _load("design_check", "method/tools/design_check.py")
model = _load("anon_baserate_model", "config/designs/anon_baserate_model.py")
HELPERS = dc.HELPERS

# Frozen parameters (prereg + addenda).
SEED, N_RUNS, C, F, B, DELTA = 20261003, 30, 24, 0.01, 0.001, 0.08

per_arm_tpr  = {a: [] for a in sub.ARMS}
per_arm_prec = {a: [] for a in sub.ARMS}
per_arm_fpr  = {a: [] for a in sub.ARMS}

for r in range(N_RUNS):
    rng = random.Random(SEED + r)
    signals = [sub.latent_signal(rng) for _ in range(C)]
    ingress = [sub.observe(s, rng) for s in signals]            # shared entry observation
    for arm, p in sub.ARMS.items():
        egress = [sub.transport(s, p["jitter"], p["pad"], rng) for s in signals]
        tpr, fpr = sub.score(ingress, egress, F)
        per_arm_tpr[arm].append(tpr)
        per_arm_fpr[arm].append(fpr)
        per_arm_prec[arm].append(sub.precision_at_base_rate(tpr, F, B))

# RQ-RESIST confirmatory: paired TPR gap Tor - SOR, through the FROZEN decision rule.
gaps = [per_arm_tpr["Tor"][r] - per_arm_tpr["SOR"][r] for r in range(N_RUNS)]
rng = random.Random(SEED + 99)
verdict, info = model.decide({"delta": DELTA}, {"gaps": gaps}, rng, HELPERS)

def ci(vals):
    lo, hi = HELPERS["cluster_bootstrap_ci"](vals, 0.95, 2000, random.Random(SEED + 7))
    return [round(lo, 4), round(hi, 4)]

mean = lambda xs: round(sum(xs) / len(xs), 4)
result = {
    "slug": "anon-baserate", "seed": SEED, "n_runs": N_RUNS, "C": C,
    "operating_point_FPR": F, "base_rate_b": B, "delta": DELTA,
    "per_arm": {a: {
        "role": sub.ARMS[a]["role"],
        "TPR_at_f_mean": mean(per_arm_tpr[a]), "TPR_at_f_CI": ci(per_arm_tpr[a]),
        "realized_FPR_mean": mean(per_arm_fpr[a]),
        "precision_at_base_rate_mean": mean(per_arm_prec[a]),
        "precision_at_base_rate_CI": ci(per_arm_prec[a]),
        "bandwidth_overhead": sub.ARMS[a]["pad"], "hops": sub.ARMS[a]["hops"],
    } for a in sub.ARMS},
    "RQ_RESIST": {
        "dv": "paired TPR@f gap (Tor - SOR)",
        "mean_gap": mean(gaps), "gap_CI": info["ci_lo"] and [round(info["ci_lo"],4), round(info["ci_hi"],4)],
        "ci_halfwidth": round(info["ci_halfwidth"], 4),
        "verdict": verdict,
        "interpretation": {
            "H1": "SOR meaningfully more resistant than Tor (gap >= delta)",
            "H0": "SOR NOT meaningfully more resistant than Tor (gap < delta) -- reportable null",
            "inconclusive": "CI spans 0 and delta",
        }[verdict],
    },
}
out = ROOT / "output/anon-baserate/result.json"
out.write_text(json.dumps(result, indent=2))

# human summary
print("="*74); print("anon-baserate RESULT  (frozen decision rule, confirmatory RQ-RESIST)"); print("="*74)
print(f"{'arm':<6}{'TPR@1%':>10}{'prec@b=1e-3':>14}{'bw_oh':>8}  role")
for a in sub.ARMS:
    pa = result["per_arm"][a]
    print(f"{a:<6}{pa['TPR_at_f_mean']:>10.3f}{pa['precision_at_base_rate_mean']:>14.4f}"
          f"{pa['bandwidth_overhead']:>8.2f}  {pa['role']}")
vpn_top = result["per_arm"]["VPN"]["precision_at_base_rate_mean"] == max(
    result["per_arm"][a]["precision_at_base_rate_mean"] for a in sub.ARMS)
print(f"\npositive-control check: VPN most linkable? {'YES' if vpn_top else 'NO (!)'}")
rq = result["RQ_RESIST"]
print(f"\nRQ-RESIST  gap(Tor-SOR)={rq['mean_gap']:.3f}  CI={rq['gap_CI']}  (delta={DELTA})")
print(f"VERDICT: {rq['verdict']}  ->  {rq['interpretation']}")
print("="*74)
