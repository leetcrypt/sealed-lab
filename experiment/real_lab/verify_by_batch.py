"""Per-run lag-search re-score, split by capture batch, with a bootstrap CI on the flipped gap
TPR_lag(SOR) - TPR_lag(Tor). Checks the artifact flip holds in EACH batch, not only pooled
(the 2026-10-04 top-up batch drifted higher on WG/Tor). Reuses verify_result.tpr. Stdlib."""
import glob, json, random, statistics as st, sys, io, contextlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
with contextlib.redirect_stdout(io.StringIO()):
    import verify_result as vr  # module prints its report on import; silence it
CUT = {"wg": 15, "tor": 10, "sorg": 10}  # last run index of the original 2026-10-03 batch

def runs(pat):
    out = []
    for inf in glob.glob(f"/tmp/in-{pat}-*.json"):
        r = int(inf.rsplit("-", 1)[1].split(".")[0]); egf = f"/tmp/eg-{pat}-{r}.json"
        if r > 30 or not Path(egf).exists(): continue
        a, b = vr.tpr(inf, egf, False), vr.tpr(inf, egf, True)
        if a is not None and b is not None: out.append({"run": r, "naive": a, "lag": b})
    return sorted(out, key=lambda x: x["run"])

def boot(x, y, seed=20261004, B=5000):
    rng = random.Random(seed)
    g = sorted(st.mean(rng.choices(x, k=len(x))) - st.mean(rng.choices(y, k=len(y))) for _ in range(B))
    return [round(g[int(.025 * B)], 4), round(g[int(.975 * B)], 4)]

R = {p: runs(p) for p in CUT}
res = {"per_arm": {}, "gap_lag_SOR_minus_Tor": {}}
for p, rs in R.items():
    for lab, sel in (("orig", [x for x in rs if x["run"] <= CUT[p]]), ("new", [x for x in rs if x["run"] > CUT[p]]), ("all", rs)):
        res["per_arm"].setdefault(p, {})[lab] = {"n": len(sel), "naive": round(st.mean(x["naive"] for x in sel), 4),
                                                 "lag": round(st.mean(x["lag"] for x in sel), 4)}
for lab in ("orig", "new", "all"):
    pick = lambda p: [x["lag"] for x in R[p] if lab == "all" or (x["run"] <= CUT[p]) == (lab == "orig")]
    s, t = pick("sorg"), pick("tor")
    res["gap_lag_SOR_minus_Tor"][lab] = {"point": round(st.mean(s) - st.mean(t), 4), "CI95": boot(s, t)}
(ROOT / "output/anon-baserate/real-data/verify-by-batch.json").write_text(json.dumps(res, indent=2))
print(json.dumps(res, indent=2))
