"""anon-baserate substrate: generate per-run ingress/egress flow observations per arm and
score them with the validated correlator. Stdlib only.

A passive adversary observes each connection ENTERING the network (ingress) and LEAVING it
(egress). Entry observation is shared across arms (same user traffic); the transport only
distorts egress. Arms are therefore PAIRED by (run, connection): same latent signal, scored
through VPN / Tor / SOR. Grounded-simulation parameters per arm are ASSUMPTIONS (to be
re-fit from real capture at stage 05), mirroring sd_run.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_c = importlib.util.spec_from_file_location("correlator", _ROOT / "config/instruments/correlator.py")
correlator = importlib.util.module_from_spec(_c); _c.loader.exec_module(correlator)
_d = importlib.util.spec_from_file_location("design_check", _ROOT / "method/tools/design_check.py")
_dc = importlib.util.module_from_spec(_d); _d.loader.exec_module(_dc)
empirical_threshold = _dc.empirical_threshold

T_BINS = 48

# Grounded transport parameters (ASSUMPTIONS; re-fit from real capture at stage 05).
ARMS = {
    "VPN": {"jitter": 0.3, "pad": 0.00, "hops": 1, "role": "positive-control"},
    "Tor": {"jitter": 1.6, "pad": 0.00, "hops": 3, "role": "comparator"},
    "SOR": {"jitter": 1.6, "pad": 0.60, "hops": 3, "role": "system-under-study"},
}


def latent_signal(rng):
    s = [0.0] * T_BINS
    for _ in range(rng.randint(3, 7)):
        start = rng.randint(0, T_BINS - 1)
        size = rng.uniform(1.0, 5.0)
        for k in range(rng.randint(1, 4)):
            if start + k < T_BINS:
                s[start + k] += size * rng.uniform(0.5, 1.5)
    return s


def observe(series, rng):
    return [max(0.0, v + rng.gauss(0.0, 0.1)) for v in series]


def transport(s, jitter, pad, rng):
    e = [0.0] * T_BINS
    for t in range(T_BINS):
        tt = min(T_BINS - 1, max(0, t + int(round(rng.gauss(0.0, jitter)))))
        e[tt] += s[t]
    if pad > 0.0:
        cover = sum(e) * pad
        for t in range(T_BINS):
            e[t] += cover / T_BINS * rng.uniform(0.5, 1.5)
    return observe(e, rng)


def score(ingress, egress, f):
    """S = correlation matrix; return (TPR@f, realized FPR)."""
    C = len(ingress)
    S = [[correlator.correlate(ingress[i], egress[j]) for j in range(C)] for i in range(C)]
    diag = [S[i][i] for i in range(C)]
    off = [S[i][j] for i in range(C) for j in range(C) if i != j]
    thr = empirical_threshold(off, f)
    tpr = sum(1 for d in diag if d > thr) / C
    fpr = sum(1 for o in off if o > thr) / len(off)
    return tpr, fpr


def precision_at_base_rate(tpr, f, b):
    denom = b * tpr + (1.0 - b) * f
    return (b * tpr / denom) if denom > 0 else 0.0
