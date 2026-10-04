# Lag-correlator validation — closing the `correlate_lag` gap

**Date:** 2026-10-03
**Scope:** The verification agent (`VERIFICATION-CORRELATOR.md`) validated `auc`,
`linkage_auc`, and `correlate`, but flagged that the lag-SEARCHING correlator
`correlate_lag` in `config/instruments/correlator.py` was **not** validated by the
instrument gate. This document closes that gap.

## What was done

1. **Self-test** `experiment/real_lab/test_correlate_lag.py` — proves `correlate_lag`
   orientation from first principles (stdlib only).
2. **`linkage_auc_lag(ingress_list, egress_list, max_lag=10)`** added to
   `config/instruments/correlator.py` — builds the n*n score matrix with `correlate_lag`,
   then returns AUC via the existing sealed `linkage_auc`.
3. **Manifest** `config/instruments/anon-baserate-lag.json` — registers `linkage_auc`
   (anchors `auc_matrix`, sealed) so `instrument_check` gates the AUC computation.

## 1. Self-test results — PASS

`python3 experiment/real_lab/test_correlate_lag.py` (exit 0). Full output:
`output/anon-baserate/test_correlate_lag-PASS.txt`.

| claim | result | expected |
|---|---|---|
| identical series `correlate_lag(x, x)` | **1.000000** | 1.0 |
| shifted copy (delay k=3) `correlate_lag(a, shift(a,3))` | **1.000000** | ~1.0 |
| shift recovered (winning lag) | **-3** | -3 |
| lag search is live (lag-0 r vs lag-search r) | **0.524 << 1.000** | gap > 0.3 |
| unrelated random (mean / max over 50 pairs) | **0.175 / 0.303** | low, << 1.0 |

Interpretation: `correlate_lag` is correctly oriented. It scores identical series at
exactly 1.0, recovers a time-shifted copy to ~1.0 **and** reports the exact offset
(-3), and leaves unrelated series low. The "lag search is live" check guards against a
silent regression where the lag loop degrades into a lag-0 no-op: the naive lag-0
`correlate` scores the shifted pair at only 0.524, so the >0.3 improvement from the lag
search demonstrates the realignment is actually happening. This is the lag-domain
analogue of the orientation gate that would have caught the D-2 (`sor-vs-tor`) 1-AUC
inversion.

## 2. Instrument check — PASS

`python3 method/tools/instrument_check.py config/instruments/anon-baserate-lag.json --gates OEP`
(exit 0). Full output: `output/anon-baserate/instrument_check-lag-OEP-PASS.txt`.

- **O ORIENTATION** — `correlator.linkage_auc`: all 3 `auc_matrix` ground-truth anchors
  hold (perfect -> 1.0, inverted -> 0.0, coincident -> 0.5).
- **E EQUIVALENCE** — none registered (no fast-path instruments in this manifest).
- **P PROVENANCE** — `config/instruments/correlator.py` tracked, clean, at `5a5d869`.

## 3. What IS and ISN'T gated (honest statement)

**Gated by `instrument_check` (executing gate, machine-enforced):**
- `linkage_auc` — the AUC computation that `linkage_auc_lag` feeds its score matrix into.
  Orientation is verified against from-scratch ground-truth anchors; provenance is
  verified (git-tracked + clean). This is the step that turns correlation scores into the
  reported DV, and it is the step the D-2 defect lived in.

**NOT gated by `instrument_check`, gated by the self-test instead:**
- `correlate_lag` — the lag-searching correlator itself. It does **not** fit the
  `auc_matrix` / `auc_sequence` anchor shape: its input is two per-bin byte-count series,
  not a score matrix, and its output is a single Pearson r, not an AUC. There is no
  standard anchor set in `instrument_check.py` for "max correlation over integer shifts."
  Its orientation is therefore proven by `test_correlate_lag.py` (section 1), which is an
  executable, re-runnable, stdlib-only check — not a hand audit.
- `linkage_auc_lag` as a whole — not directly registered as an instrument. Its two halves
  are each validated separately: the matrix-building half (`correlate_lag`) by the
  self-test, the scoring half (`linkage_auc`) by the OEP gate. The composition is a
  trivial `linkage_auc(S)` with no new logic beyond those two validated pieces.

**Honest limits.** The self-test proves correctness on synthetic signals with a known,
clean shift. It does not re-prove the empirical finding that SOR defeats the correlator;
`VERIFICATION-CORRELATOR.md` already showed (and `lagscore.py` confirmed) that SOR's
linked-pair correlation stays ~0 **even under lag search**, so the lag-aware variant does
not rescue linkage on the real SOR data — the decorrelation is genuine, not a
timing-misalignment artifact. The gate added here guarantees the *tool* is sound; the
empirical conclusion rests on the earlier verification run.

## Verdict

**`correlate_lag` is sound.** Orientation is correct (identical=1.0, shift recovered to
~1.0 at the right lag, unrelated low), the lag search is demonstrably active, and the AUC
computation it feeds passes the OEP instrument gate on a git-clean, provenance-tracked
source. The gap the verification agent flagged is closed.
