"""Score the REAL WireGuard capture: build the linkage matrix, compute TPR@f, precision@b,
and real latency/goodput. Reuses the validated correlator. usage: score_real.py <ingress.json> <egress.json>"""
from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
_c = importlib.util.spec_from_file_location("correlator", ROOT / "config/instruments/correlator.py")
correlator = importlib.util.module_from_spec(_c); _c.loader.exec_module(correlator)
_d = importlib.util.spec_from_file_location("dc", ROOT / "method/tools/design_check.py")
dc = importlib.util.module_from_spec(_d); _d.loader.exec_module(dc)

OUT = Path(sys.argv[3]) if len(sys.argv)>3 else (ROOT/"output/anon-baserate/real-result.json")
ing = json.loads(Path(sys.argv[1]).read_text())
egr = json.loads(Path(sys.argv[2]).read_text())
ingress, lat, good = ing["ingress"], ing["latency_s"], ing["goodput_Bps"]
cids = sorted(set(ingress) & set(egr), key=int)
I = [ingress[c] for c in cids]; E = [egr[c] for c in cids]
n = len(cids); F, B = 0.01, 0.001

S = [[correlator.correlate(I[i], E[j]) for j in range(n)] for i in range(n)]
diag = [S[i][i] for i in range(n)]
off = [S[i][j] for i in range(n) for j in range(n) if i != j]
thr = dc.empirical_threshold(off, F)
tpr = sum(1 for d in diag if d > thr) / n
auc = correlator.linkage_auc(S)
prec_b = (B * tpr) / (B * tpr + (1 - B) * F) if (B*tpr+(1-B)*F) > 0 else 0.0
med = lambda xs: round(sorted(xs)[len(xs)//2], 4)
res = {
    "arm": "VPN (real WireGuard via Tailscale)", "connections": n,
    "linkage_AUC": round(auc, 4), "TPR_at_1pct_FPR": round(tpr, 3),
    "precision_at_base_rate_1e-3": round(prec_b, 4),
    "median_connect_latency_ms": round(med(lat) * 1000, 1),
    "median_goodput_Bps": med(good),
}
OUT.write_text(json.dumps(res, indent=2))
print(json.dumps(res, indent=2))
