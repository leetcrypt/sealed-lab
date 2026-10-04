"""sensitivity.py — robustness sweep of the artifact flip (naive lag-0 vs lag-search).

The headline from finding-07 is a *flip*: under the naive lag-0 correlator the SOR arm's
TPR reads ~0 (looks maximally resistant), but a competent lag-searching adversary recovers
substantial linkage. If that flip only appears at one (max_lag, FPR) operating point it is a
knife-edge, not a finding. This script re-computes mean TPR for every arm across a grid of
analysis parameters so the flip can be judged robust or fragile.

  max_lag in {0, 2, 5, 10, 15}      (0 == the naive lag-0 correlator)
  FPR     in {0.005, 0.01, 0.02, 0.05}

For one run we build the n*n linkage-score matrix (ingress conn i vs egress conn j), take the
diagonal as the linked (positive) pairs and the off-diagonal as the unlinked (negative) pairs,
set the score threshold to the empirical FPR operating point on the negatives, and report the
fraction of positives above it (TPR@FPR). Mean TPR is averaged over all runs in the arm.

Stdlib only; the correlator and the threshold helper are loaded by path via importlib so a
reviewer runs this with nothing installed.
"""
from __future__ import annotations

import glob
import importlib.util
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cor = _load("correlator", "config/instruments/correlator.py")
dc = _load("design_check", "method/tools/design_check.py")

# arm label -> file-stem glob token
ARMS = [("WG", "wg"), ("Tor", "tor"), ("SOR", "sorg")]
MAX_LAGS = [0, 2, 5, 10, 15]
FPRS = [0.005, 0.01, 0.02, 0.05]


def load_pair(inf: str, egf: str):
    """Return (ingress_series_list, egress_series_list) over the shared connection ids."""
    I = json.loads(Path(inf).read_text()).get("ingress", {})
    E = json.loads(Path(egf).read_text())
    cids = sorted(set(I) & set(E), key=int)
    if len(cids) < 4:
        return None
    return [I[c] for c in cids], [E[c] for c in cids]


def score_matrix(Iv, Ev, max_lag: int):
    """n*n linkage scores. max_lag==0 uses the naive lag-0 correlate()."""
    n = len(Iv)
    if max_lag == 0:
        return [[cor.correlate(Iv[i], Ev[j]) for j in range(n)] for i in range(n)]
    return [[cor.correlate_lag(Iv[i], Ev[j], max_lag) for j in range(n)] for i in range(n)]


def tpr_at(S, fpr: float) -> float:
    n = len(S)
    diag = [S[i][i] for i in range(n)]
    off = [S[i][j] for i in range(n) for j in range(n) if i != j]
    thr = dc.empirical_threshold(off, fpr)
    return sum(1 for v in diag if v > thr) / n


def collect():
    """{arm: {max_lag: {fpr: [per-run TPR, ...]}}}, plus cached matrices per (arm,lag)."""
    results: dict = {}
    for arm, tok in ARMS:
        results[arm] = {lag: {f: [] for f in FPRS} for lag in MAX_LAGS}
        for inf in sorted(glob.glob(f"/tmp/in-{tok}-*.json")):
            run = inf.split("-")[-1]
            egf = f"/tmp/eg-{tok}-{run}"
            if not Path(egf).exists():
                continue
            pair = load_pair(inf, egf)
            if pair is None:
                continue
            Iv, Ev = pair
            for lag in MAX_LAGS:
                S = score_matrix(Iv, Ev, lag)
                for f in FPRS:
                    results[arm][lag][f].append(tpr_at(S, f))
    return results


def mean_table(results):
    """{arm: {lag: {fpr: (mean, n)}}}"""
    out: dict = {}
    for arm in results:
        out[arm] = {}
        for lag in MAX_LAGS:
            out[arm][lag] = {}
            for f in FPRS:
                xs = results[arm][lag][f]
                out[arm][lag][f] = (st.mean(xs) if xs else float("nan"), len(xs))
    return out


def render(tbl, results) -> str:
    L = []
    L.append("ROBUSTNESS SWEEP — artifact flip (naive lag-0 vs lag-search)")
    L.append("Cell = mean TPR across all runs in the arm, at the given max_lag x FPR.")
    L.append("max_lag=0 is the naive adversary. Arms: WG / Tor / SOR.")
    runcount = {arm: len(results[arm][0][FPRS[0]]) for arm in results}
    L.append("Runs per arm: " + ", ".join(f"{a}={runcount[a]}" for a in runcount))
    L.append("")
    header = "max_lag | " + " | ".join(f"FPR={f:<5g}" for f in FPRS)
    for arm, _ in ARMS:
        L.append(f"=== {arm} ===")
        L.append(header)
        L.append("-" * len(header))
        for lag in MAX_LAGS:
            cells = " | ".join(f"{tbl[arm][lag][f][0]:9.3f}" for f in FPRS)
            tag = " (naive)" if lag == 0 else ""
            L.append(f"{lag:>7}{tag:<8}| {cells}")
        L.append("")

    # focused flip view: SOR naive vs lag-search, per FPR
    L.append("=== KEY: SOR flip (mean TPR) ===")
    L.append("FPR     | lag0(naive) | lag>=2 range  | flip?")
    for f in FPRS:
        naive = tbl["SOR"][0][f][0]
        rises = [tbl["SOR"][lag][f][0] for lag in MAX_LAGS if lag >= 2]
        lo, hi = min(rises), max(rises)
        flip = "YES" if naive <= 0.05 and hi >= 0.15 else ("partial" if hi > naive + 0.1 else "no")
        L.append(f"{f:<7g} | {naive:11.3f} | {lo:.3f}-{hi:.3f}   | {flip}")
    L.append("")

    # ranking check per operating point
    L.append("=== RANKING across settings ===")
    L.append("Naive (lag0): expect WG linkable, SOR ~0 (looks most resistant).")
    L.append("Lag-search  : expect WG most linkable, Tor most resistant (lowest TPR).")
    L.append("")
    L.append("setting            | order (most->least linkable by mean TPR)")
    for lag in MAX_LAGS:
        for f in FPRS:
            vals = [(arm, tbl[arm][lag][f][0]) for arm, _ in ARMS]
            vals.sort(key=lambda kv: kv[1], reverse=True)
            order = " > ".join(f"{a}({v:.2f})" for a, v in vals)
            L.append(f"lag={lag:<2} FPR={f:<5g} | {order}")
    L.append("")
    return "\n".join(L)


def main():
    results = collect()
    tbl = mean_table(results)
    text = render(tbl, results)
    out_dir = ROOT / "output/anon-baserate"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "sensitivity-result.txt").write_text(text)
    print(text)

    # machine-readable companion for the finding writeup
    flat = {
        arm: {str(lag): {str(f): round(tbl[arm][lag][f][0], 4) for f in FPRS} for lag in MAX_LAGS}
        for arm, _ in ARMS
    }
    (out_dir / "sensitivity-result.json").write_text(json.dumps(flat, indent=2))
    return tbl


if __name__ == "__main__":
    main()
