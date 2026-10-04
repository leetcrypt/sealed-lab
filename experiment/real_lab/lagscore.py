"""Resolve the alignment confound: re-score every arm with a LAG-SEARCHING correlator.
If SOR's linkage stays ~0 under lag search, resistance is real; if it rises, the no-lag
result was a timing-misalignment artifact. Stdlib only."""
import importlib.util, json, sys, glob, statistics as st
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
c=importlib.util.spec_from_file_location("cor",ROOT/"config/instruments/correlator.py")
cor=importlib.util.module_from_spec(c); c.loader.exec_module(cor)
d=importlib.util.spec_from_file_location("dc",ROOT/"method/tools/design_check.py")
dc=importlib.util.module_from_spec(d); d.loader.exec_module(dc)

def corr_lag(a,b,maxlag=10):
    best=-2.0
    for L in range(-maxlag,maxlag+1):
        if L>=0: x,y=a[:len(a)-L], b[L:]
        else: x,y=a[-L:], b[:len(b)+L]
        if len(x)<4: continue
        r=cor.correlate(x,y)
        if r>best: best=r
    return best

def score(inf, egf, maxlag):
    I=json.loads(Path(inf).read_text()).get("ingress",{}); E=json.loads(Path(egf).read_text())
    cids=sorted(set(I)&set(E),key=int)
    if len(cids)<4: return None
    Iv=[I[x] for x in cids]; Ev=[E[x] for x in cids]; n=len(cids)
    S=[[(corr_lag(Iv[i],Ev[j],maxlag) if maxlag else cor.correlate(Iv[i],Ev[j])) for j in range(n)] for i in range(n)]
    diag=[S[i][i] for i in range(n)]; off=[S[i][j] for i in range(n) for j in range(n) if i!=j]
    thr=dc.empirical_threshold(off,0.01); tpr=sum(1 for v in diag if v>thr)/n
    return round(cor.linkage_auc(S),4), round(tpr,4), round(st.mean(diag),4)

# re-score campaign files for each arm: no-lag vs lag=10
def arm_files(pat): return sorted(glob.glob(f"/tmp/in-{pat}-*.json"))
for arm,inpat,egpat in [("SOR","sorg","sorg"),("Tor","tor","tor"),("WG","wg","wg")]:
    ins=arm_files(inpat)[:6]
    rows=[]
    for inf in ins:
        r=inf.split("-")[-1]
        egf=f"/tmp/eg-{egpat}-{r}"
        if not Path(egf).exists(): continue
        nolag=score(inf,egf,0); lag=score(inf,egf,10)
        if nolag and lag: rows.append((nolag,lag))
    if rows:
        import statistics
        auc0=statistics.mean(x[0][0] for x in rows); tpr0=statistics.mean(x[0][1] for x in rows)
        aucL=statistics.mean(x[1][0] for x in rows); tprL=statistics.mean(x[1][1] for x in rows)
        print(f"{arm}: no-lag AUC {auc0:.3f} TPR {tpr0:.3f}  ->  lag-search AUC {aucL:.3f} TPR {tprL:.3f}  (n={len(rows)} runs)")
    else:
        print(f"{arm}: no files found (looked for /tmp/in-{inpat}-*.json)")
