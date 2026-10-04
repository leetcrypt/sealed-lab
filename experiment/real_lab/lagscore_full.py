"""Full lag-search re-score (ALL runs) + bootstrap CI of the corrected Tor-SOR gap.
Confirms whether the artifact flip is robust beyond the n=6 spot check."""
import importlib.util, json, glob, random, statistics as st
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
c=importlib.util.spec_from_file_location("cor",ROOT/"config/instruments/correlator.py"); cor=importlib.util.module_from_spec(c); c.loader.exec_module(cor)
d=importlib.util.spec_from_file_location("dc",ROOT/"method/tools/design_check.py"); dc=importlib.util.module_from_spec(d); d.loader.exec_module(dc)
def corr_lag(a,b,m=10):
    best=-2.0
    for L in range(-m,m+1):
        x,y=(a[:len(a)-L],b[L:]) if L>=0 else (a[-L:],b[:len(b)+L])
        if len(x)>=4:
            r=cor.correlate(x,y); best=r if r>best else best
    return best
def score(inf,egf,m):
    I=json.loads(Path(inf).read_text()).get("ingress",{}); E=json.loads(Path(egf).read_text())
    cids=sorted(set(I)&set(E),key=int)
    if len(cids)<4: return None
    Iv=[I[x] for x in cids]; Ev=[E[x] for x in cids]; n=len(cids)
    S=[[(corr_lag(Iv[i],Ev[j],m) if m else cor.correlate(Iv[i],Ev[j])) for j in range(n)] for i in range(n)]
    diag=[S[i][i] for i in range(n)]; off=[S[i][j] for i in range(n) for j in range(n) if i!=j]
    thr=dc.empirical_threshold(off,0.01); return sum(1 for v in diag if v>thr)/n
arms={}
for arm,pat in [("wg","wg"),("tor","tor"),("sor","sorg")]:
    tprs=[]
    for inf in sorted(glob.glob(f"/tmp/in-{pat}-*.json")):
        r=inf.split("-")[-1]; egf=f"/tmp/eg-{pat}-{r}"
        if Path(egf).exists():
            t=score(inf,egf,10)
            if t is not None: tprs.append(t)
    arms[arm]=tprs
def stat(x): return {"n":len(x),"mean":round(st.mean(x),4),"sd":round(st.pstdev(x),4) if len(x)>1 else 0.0}
# corrected gap Tor - SOR under lag search (expect NEGATIVE now = SOR less resistant)
rng=random.Random(7); gaps=[]
for _ in range(5000):
    t=sum(rng.choice(arms["tor"]) for _ in arms["tor"])/len(arms["tor"])
    s=sum(rng.choice(arms["sor"]) for _ in arms["sor"])/len(arms["sor"])
    gaps.append(t-s)
gaps.sort(); lo,hi=gaps[125],gaps[4874]; pt=st.mean(arms["tor"])-st.mean(arms["sor"])
out={"adversary":"lag-searching (+/-10 bins)","per_arm_TPR":{a:stat(arms[a]) for a in arms},
 "gap_Tor_minus_SOR":{"point":round(pt,4),"CI95":[round(lo,4),round(hi,4)],
   "reading":"NEGATIVE => SOR MORE linkable than Tor (Tor more resistant) — opposite of the naive result"}}
(ROOT/"output/anon-baserate/lagscore-full.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
