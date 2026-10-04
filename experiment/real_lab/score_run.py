import importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(n,p):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
cor=L("correlator",ROOT/"config/instruments/correlator.py"); dc=L("dc",ROOT/"method/tools/design_check.py")
try:
    ing=json.loads(Path(sys.argv[1]).read_text()); egr=json.loads(Path(sys.argv[2]).read_text())
except Exception as e:
    print(json.dumps({"arm":sys.argv[3],"run":int(sys.argv[4]),"error":str(e)})); sys.exit(0)
arm=sys.argv[3]; run=int(sys.argv[4]); I=ing.get("ingress",{}); cids=sorted(set(I)&set(egr),key=int)
if len(cids)<4:
    print(json.dumps({"arm":arm,"run":run,"error":"few","n":len(cids)})); sys.exit(0)
Iv=[I[c] for c in cids]; Ev=[egr[c] for c in cids]; n=len(cids); F,B=0.01,0.001
S=[[cor.correlate(Iv[i],Ev[j]) for j in range(n)] for i in range(n)]
diag=[S[i][i] for i in range(n)]; off=[S[i][j] for i in range(n) for j in range(n) if i!=j]
thr=dc.empirical_threshold(off,F); tpr=sum(1 for d in diag if d>thr)/n
med=lambda xs: sorted(xs)[len(xs)//2] if xs else 0
print(json.dumps({"arm":arm,"run":run,"n":n,"auc":round(cor.linkage_auc(S),4),"tpr":round(tpr,4),
  "prec_b":round((B*tpr)/(B*tpr+(1-B)*F),5),"lat_ms":round(med(ing.get("latency_s",[0]))*1000,1)}))
