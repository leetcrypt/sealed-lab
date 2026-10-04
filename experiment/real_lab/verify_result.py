"""Verification step (Omnigent-invokable): re-score every arm with the NAIVE (lag-0) and the
LAG-SEARCHING adversary. If an arm's linkage jumps under lag search, its 'resistance' under the
naive scorer was a timing-alignment ARTIFACT. Prints a verdict. Stdlib."""
import importlib.util, json, glob, statistics as st
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
c=importlib.util.spec_from_file_location("cor",ROOT/"config/instruments/correlator.py"); cor=importlib.util.module_from_spec(c); c.loader.exec_module(cor)
d=importlib.util.spec_from_file_location("dc",ROOT/"method/tools/design_check.py"); dc=importlib.util.module_from_spec(d); d.loader.exec_module(dc)
def tpr(inf,egf,lag):
    I=json.loads(Path(inf).read_text()).get("ingress",{}); E=json.loads(Path(egf).read_text())
    cids=sorted(set(I)&set(E),key=int)
    if len(cids)<4: return None
    Iv=[I[x] for x in cids]; Ev=[E[x] for x in cids]; n=len(cids)
    f=(lambda a,b: cor.correlate_lag(a,b,10)) if lag else cor.correlate
    S=[[f(Iv[i],Ev[j]) for j in range(n)] for i in range(n)]
    diag=[S[i][i] for i in range(n)]; off=[S[i][j] for i in range(n) for j in range(n) if i!=j]
    return sum(1 for v in diag if v>dc.empirical_threshold(off,0.01))/n
print("="*66); print("VERIFICATION — naive vs lag-searching adversary"); print("="*66)
verdict_lines=[]
for arm,pat in [("WireGuard","wg"),("Tor","tor"),("SOR","sorg")]:
    nn=[];ll=[]
    for inf in sorted(glob.glob(f"/tmp/in-{pat}-*.json")):
        r=inf.split("-")[-1]; egf=f"/tmp/eg-{pat}-{r}"
        if Path(egf).exists():
            a=tpr(inf,egf,False); b=tpr(inf,egf,True)
            if a is not None and b is not None: nn.append(a); ll.append(b)
    if nn:
        mn,ml=round(st.mean(nn),3),round(st.mean(ll),3)
        flag=" <== ARTIFACT (resistance was misalignment)" if (mn<0.1 and ml-mn>0.15) else ""
        print(f"  {arm:<10} naive TPR {mn:.3f}  ->  lag-search TPR {ml:.3f}{flag}")
        verdict_lines.append((arm,mn,ml))
print("-"*66)
sor=[v for v in verdict_lines if v[0]=="SOR"]
if sor and sor[0][2]-sor[0][1]>0.15:
    print("VERDICT: SOR's naive 'resistance' is a MEASUREMENT ARTIFACT. The claim 'SOR more")
    print("resistant than Tor' is RETRACTED. Under a lag-aligning adversary Tor is most resistant.")
else:
    print("VERDICT: no artifact detected under lag search.")
print("="*66)
