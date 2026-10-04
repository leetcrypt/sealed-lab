"""Aggregate the repeated real-capture campaign: per-arm stats, measured sd_run, the
Tor-vs-SOR confirmatory gap with a bootstrap CI, and the verdict under the frozen rule.
Honest note: real arms were captured sequentially (independent), not paired per run as the
sealed design assumed -> we use the UNPAIRED two-sample gap (more conservative). Logged."""
from __future__ import annotations
import json, math, random, statistics as st
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DD = ROOT / "output/anon-baserate/real-data"
DELTA, F, B = 0.08, 0.01, 0.001

def load(arm):
    rows=[json.loads(l) for l in (DD/f"runs-{arm}.jsonl").read_text().splitlines() if l.strip()]
    return [r for r in rows if "error" not in r]

arms={a:load(a) for a in ("wg","tor","sor")}
def col(rows,k): return [r[k] for r in rows if k in r]
def stats(xs): 
    return {"n":len(xs),"mean":round(st.mean(xs),4),"sd":round(st.pstdev(xs),4) if len(xs)>1 else 0.0}

summary={a:{k:stats(col(arms[a],k)) for k in ("auc","tpr","prec_b","lat_ms")} for a in arms}

# unpaired bootstrap of the gap Tor.tpr - SOR.tpr
tor_tpr=col(arms["tor"],"tpr"); sor_tpr=col(arms["sor"],"tpr")
rng=random.Random(20261003); B_RES=5000; gaps=[]
for _ in range(B_RES):
    t=sum(rng.choice(tor_tpr) for _ in tor_tpr)/len(tor_tpr)
    s=sum(rng.choice(sor_tpr) for _ in sor_tpr)/len(sor_tpr)
    gaps.append(t-s)
gaps.sort(); lo=gaps[int(.025*B_RES)]; hi=gaps[int(.975*B_RES)]
point=st.mean(tor_tpr)-st.mean(sor_tpr)
verdict = "H1 (SOR more resistant than Tor)" if lo>0 and point>=DELTA else \
          ("H0 (SOR not meaningfully more resistant; gap < delta)" if hi<DELTA else "inconclusive")
# measured sd_run for an UNPAIRED difference of single runs
sd_run_meas = round(math.sqrt(st.pvariance(tor_tpr)+st.pvariance(sor_tpr)),4) if len(tor_tpr)>1 and len(sor_tpr)>1 else None

out={
 "n_runs":{a:summary[a]["tpr"]["n"] for a in arms},
 "per_arm":summary,
 "RQ_RESIST":{"dv":"UNPAIRED gap TPR@1%(Tor) - TPR@1%(SOR)",
   "point":round(point,4),"CI95":[round(lo,4),round(hi,4)],"delta":DELTA,"verdict":verdict},
 "sd_run_measured":sd_run_meas,"sd_run_threshold":0.13,
 "sd_run_ruling":("OK (<=0.13): design holds" if (sd_run_meas is not None and sd_run_meas<=0.13)
                  else "EXCEEDS 0.13: design returns to stage 03" if sd_run_meas is not None else "n/a"),
 "deviation":"Real arms captured sequentially (independent), not paired per run. Unpaired two-sample gap used (more conservative than the sealed paired design). Logged as deviation D-real-1.",
}
(DD/"aggregate-real.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
