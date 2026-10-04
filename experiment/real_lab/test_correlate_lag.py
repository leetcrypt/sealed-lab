#!/usr/bin/env python3
"""Orientation self-test for `correlate_lag` in config/instruments/correlator.py.

`instrument_check`'s ORIENTATION gate can score the matrix-AUC family (perfect->1.0,
inverted->0.0, coincident->0.5) because those have a clean ground-truth anchor set. The
lag-SEARCHING correlator does not fit that anchor shape — its input is two per-bin byte
series, not a score matrix — so its correctness is proven HERE instead, from first
principles, with stdlib only. Three claims, each an executable assertion:

  1. correlate_lag(x, x)                -> 1.0   (identical series)
  2. correlate_lag(x, shift(x, k))      -> ~1.0  AND it RECOVERS the shift k
  3. correlate_lag(unrelated random)    -> low   (clearly separated from 1.0)

Claim 2 is the whole point of a lag-searching correlator: the naive lag-0 `correlate`
scores a time-shifted copy as nearly unlinked; `correlate_lag` must realign and recover
near-perfect correlation. We assert BOTH that it recovers ~1.0 and that lag-0 does not,
so the test fails if someone silently turns the lag search into a no-op.
"""
from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "correlator", ROOT / "config/instruments/correlator.py"
)
cor = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cor)

TOL = 1e-9


def _best_lag(a, b, max_lag=10):
    """Mirror correlate_lag's search but return the lag that wins — for reporting /
    asserting the shift was recovered. Kept separate so the module under test is
    unmodified."""
    best_r, best_L = -2.0, None
    for L in range(-max_lag, max_lag + 1):
        if L >= 0:
            x, y = a[: len(a) - L], b[L:]
        else:
            x, y = a[-L:], b[: len(b) + L]
        if len(x) >= 4:
            r = cor.correlate(x, y)
            if r > best_r:
                best_r, best_L = r, L
    return best_r, best_L


def main() -> int:
    rng = random.Random(20261003)
    failures = []
    print("correlate_lag orientation self-test")
    print(f"  module: {ROOT / 'config/instruments/correlator.py'}")
    print()

    # A non-trivial base signal so correlation is meaningful (not a flat/constant series,
    # which both correlate and correlate_lag define as 0.0 by construction).
    base = [math.sin(i / 3.0) + 0.15 * rng.gauss(0, 1) for i in range(200)]

    # --- Claim 1: identical series -> exactly 1.0 -------------------------------------
    x = base[:120]
    r1 = cor.correlate_lag(x, x, max_lag=10)
    ok1 = abs(r1 - 1.0) <= 1e-9
    print(f"[{'PASS' if ok1 else 'FAIL'}] identical series       correlate_lag = {r1:.6f}  (expect 1.0)")
    if not ok1:
        failures.append(f"identical series gave {r1}, expected 1.0")

    # --- Claim 2: shifted copy -> ~1.0 AND the shift is recovered ---------------------
    # b is x delayed: two overlapping windows of the same base signal, offset by SHIFT.
    SHIFT = 3
    a2 = base[0:120]
    b2 = base[SHIFT : 120 + SHIFT]              # b2[i] == a2[i + SHIFT] == base[i+SHIFT]
    r2 = cor.correlate_lag(a2, b2, max_lag=10)
    r2_best, r2_lag = _best_lag(a2, b2, max_lag=10)
    r2_nolag = cor.correlate(a2, b2)           # what the naive lag-0 scorer would see
    ok2a = r2 >= 0.999                           # recovered near-perfect correlation
    ok2b = r2_lag == -SHIFT                       # recovered the exact offset
    ok2c = r2 - r2_nolag > 0.3                    # lag search is NOT a silent no-op
    print(f"[{'PASS' if ok2a else 'FAIL'}] shifted copy (k={SHIFT})      correlate_lag = {r2:.6f}  (expect ~1.0)")
    print(f"[{'PASS' if ok2b else 'FAIL'}] shift recovered          best lag = {r2_lag}      (expect {-SHIFT})")
    print(f"[{'PASS' if ok2c else 'FAIL'}] lag search is live       lag-0 r = {r2_nolag:.6f} << lag-search r = {r2:.6f}")
    if not ok2a:
        failures.append(f"shifted series gave {r2}, expected >=0.999")
    if not ok2b:
        failures.append(f"shift not recovered: best lag {r2_lag}, expected {-SHIFT}")
    if not ok2c:
        failures.append(f"lag search ineffective: lag-0 {r2_nolag} vs lag-search {r2}")

    # --- Claim 3: unrelated random series -> low -------------------------------------
    # Averaged over many independent pairs so the result is not a lucky draw. Each pair is
    # the max over 21 lags, which inflates the number a little; it must still sit far below
    # the linked cases above.
    vals = []
    for _ in range(50):
        u = [rng.gauss(0, 1) for _ in range(120)]
        v = [rng.gauss(0, 1) for _ in range(120)]
        vals.append(cor.correlate_lag(u, v, max_lag=10))
    r3_mean = sum(vals) / len(vals)
    r3_max = max(vals)
    ok3 = r3_mean < 0.5 and r3_max < 0.8
    print(f"[{'PASS' if ok3 else 'FAIL'}] unrelated random         mean = {r3_mean:.6f}, max = {r3_max:.6f}  (expect low, << 1.0)")
    if not ok3:
        failures.append(f"unrelated random too high: mean {r3_mean}, max {r3_max}")

    print()
    if failures:
        print(f"RESULT: FAIL — {len(failures)} assertion(s) failed:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("RESULT: PASS — correlate_lag is correctly oriented (identical=1.0, "
          "shift recovered to ~1.0, unrelated low).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
