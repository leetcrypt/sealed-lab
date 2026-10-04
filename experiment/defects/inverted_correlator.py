"""INJECTED DEFECT #1: a correlator that silently returns 1-AUC (inverted orientation).
This is the real SOR-program D-2 defect. It does not crash; it returns an authentic-looking
number. The instrument gate's ORIENTATION check catches it."""
from __future__ import annotations
def auc(pos, neg):
    if not pos or not neg: return 0.5
    w=0.0
    for p in pos:
        for q in neg:
            w += 1.0 if p>q else (0.5 if p==q else 0.0)
    return 1.0 - (w/(len(pos)*len(neg)))        # <-- INVERTED
def linkage_auc(S):
    n=len(S); diag=[S[i][i] for i in range(n)]
    off=[S[i][j] for i in range(n) for j in range(n) if i!=j]
    return auc(diag, off)
