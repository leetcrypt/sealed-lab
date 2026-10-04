"""Self-contained classical end-to-end linkage correlator for the anon-baserate study.

The A-classical adversary. Stdlib only, so a reviewer can run it with nothing installed.
Three functions, two of them gated by instrument_check against ground-truth anchors:

  correlate(a, b) -> float   normalized cross-correlation (Pearson r) of two per-bin
                             byte-count series; the per-pair linkage score. Higher = more
                             likely the same connection observed at ingress and egress.
  auc(pos, neg)   -> float   rank-AUC (Mann-Whitney), ties = 0.5. [anchors: auc_sequence]
  linkage_auc(S)  -> float   AUC of an n*n score matrix, diagonal = linked pairs,
                             off-diagonal = unlinked. [anchors: auc_matrix]

Two lag-searching variants model a competent end-to-end adversary that realigns for
transport/relay timing offset before scoring (orientation proven by
experiment/real_lab/test_correlate_lag.py, not by instrument_check's anchor gate):

  correlate_lag(a, b, max_lag)             max Pearson r over integer bin shifts.
  linkage_auc_lag(ingress, egress, max_lag) builds S with correlate_lag, then returns the
                                           sealed, gate-verified linkage_auc(S).

Orientation is fixed by construction (perfect -> 1.0, inverted -> 0.0, coincident -> 0.5),
which is exactly what instrument_check's orientation gate verifies — the check that would
have caught the SOR program's silent 1-AUC inversion.
"""
from __future__ import annotations


def correlate(a, b) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    a, b = a[:n], b[:n]
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    if va == 0.0 or vb == 0.0:
        return 0.0
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    return cov / (va * vb) ** 0.5


def auc(pos, neg) -> float:
    if not pos or not neg:
        return 0.5
    wins = 0.0
    for p in pos:
        for q in neg:
            if p > q:
                wins += 1.0
            elif p == q:
                wins += 0.5
    return wins / (len(pos) * len(neg))


def linkage_auc(S) -> float:
    n = len(S)
    diag = [S[i][i] for i in range(n)]
    off = [S[i][j] for i in range(n) for j in range(n) if i != j]
    return auc(diag, off)


def correlate_lag(a, b, max_lag: int = 10) -> float:
    """Lag-searching correlation: max Pearson r over integer bin shifts in [-max_lag, max_lag].
    A competent end-to-end adversary aligns for transport/relay timing offset before scoring;
    the naive lag-0 `correlate` does not, which can make an offset flow look unlinked.

    Orientation is proven by experiment/real_lab/test_correlate_lag.py (identical -> 1.0,
    shifted copy -> ~1.0 with the shift recovered, unrelated -> low). It has no scalar
    ground-truth anchor shape, so instrument_check gates the AUC *computation* it feeds
    (linkage_auc, auc_matrix anchors); the self-test gates the correlator's orientation."""
    best = -2.0
    for L in range(-max_lag, max_lag + 1):
        if L >= 0:
            x, y = a[:len(a) - L], b[L:]
        else:
            x, y = a[-L:], b[:len(b) + L]
        if len(x) >= 4:
            r = correlate(x, y)
            if r > best:
                best = r
    return best


def linkage_auc_lag(ingress_list, egress_list, max_lag: int = 10) -> float:
    """Lag-aware end-to-end linkage AUC.

    Builds the n*n score matrix S with `correlate_lag` (so a timing-offset flow is realigned
    before scoring, unlike the lag-0 `linkage_auc` path), then hands it to the sealed,
    gate-verified `linkage_auc`. S[i][j] = correlate_lag(ingress_i, egress_j); the diagonal
    is the truly-linked ingress/egress pairs, the off-diagonal is unlinked pairs. Higher AUC
    = the adversary better separates linked from unlinked. The AUC step is the sealed one;
    the correlator's orientation is proven by test_correlate_lag.py."""
    n = min(len(ingress_list), len(egress_list))
    S = [[correlate_lag(ingress_list[i], egress_list[j], max_lag) for j in range(n)]
         for i in range(n)]
    return linkage_auc(S)
