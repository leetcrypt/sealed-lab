# VERIFICATION — Correlator correctness + SOR resistance mechanism

Independent adversarial audit of finding-06 (`finding-06-real-confirmatory.md`).
Scope: (1) is the correlator correct, (2) is SOR's TPR=0 / AUC 0.43 a real effect
or an artifact, (3) is the stated mechanism ("nested SSH collapses each flow to ~1
timing bin") supported by the data. Tools: python3 stdlib only.

## TL;DR verdict

- **Correlator: CORRECT.** `auc`, `linkage_auc`, `correlate` all pass. My from-scratch
  reimplementation matches the repo bit-for-bit (max |diff| = 0.0e+00 over 200 random
  matrices). Orientation gate holds (perfect 1.0 / inverted 0.0 / coincident 0.5).
- **SOR TPR=0 is REAL, not a data bug.** Egress and ingress are both non-degenerate;
  my re-scoring of the raw campaign series reproduces `runs-sor.jsonl` AUCs exactly.
  TPR=0 arises legitimately: linked-pair correlations are ~0, below the 1%-FPR threshold.
- **The STATED MECHANISM IS FALSE.** SOR egress does **not** collapse to ~1 timing bin.
  The campaign SOR egress carries ~7.5–10 non-zero bins per connection — the *same order
  as WireGuard (9.7) and Tor (7.5)*. The "~1 bin" story is contradicted by the very data
  that produced the finding's numbers.
- **AUC 0.43 is essentially chance, mildly below it.** Per run it sits within ~1 null SD
  of 0.5; the real resistance signal is "correlator reduced to a coin flip (TPR=0)," not a
  meaningful anti-correlation. AUC < 0.5 is not "more resistant than chance" — chance is the
  resistance ceiling.

---

## 1. CORRELATOR CORRECTNESS — PASS

Re-implemented `auc` (Mann–Whitney rank AUC, ties=0.5) and `linkage_auc` (diag vs
off-diagonal) from scratch and compared to `config/instruments/correlator.py`.

| test | repo | mine | expected |
|---|---|---|---|
| perfect-separation matrix (diag=1, off=0) | 1.0000 | 1.0000 | 1.0 |
| inverted (diag=0, off=1) | 0.0000 | 0.0000 | 0.0 |
| coincident (all 0.5) | 0.5000 | 0.5000 | 0.5 |
| tie handling auc([1,1,2,2],[1,2,2,3]) | 0.3125 | 0.3125 | — |
| 200 random matrices/pairs, max abs diff | — | — | **0.00e+00** |

`correlate` is a textbook Pearson r: perfect→+1.0, inverted→−1.0, constant series→0.0
(the va==0/vb==0 guard, which is what makes a collapsed/flat series score 0). No
sign-inversion, no off-by-one. **The correlator is sound.**

## 2. SOR MECHANISM — TPR=0 is real; the "~1 bin" explanation is NOT

### 2a. Non-zero bin counts per connection (series length = 48 bins)

| arm (source) | min | median | max | mean |
|---|---|---|---|---|
| **SOR campaign** `/tmp/eg-sorg-1..10` | 1–4 | **7–10** | 11–17 | **7.5–10.2** |
| SOR single file `real-data/sor-egress.json` | 1 | 1 | 14 | 4.0 (bimodal: 10 of 20 conns = 1 bin) |
| WireGuard `wg-egress.json` | 2 | 10 | 17 | 9.7 |
| Tor `tor-egress.json` | 0 | 7.5 | 13 | 7.5 |

The 10 campaign SOR egress captures — the files that actually generated the aggregate —
carry **~8 non-zero bins per flow, indistinguishable from WG and Tor**. The claim that
"nested SSH buffers each flow into ~1 timing bin, collapsing the fingerprint" is **false
for this data**. The only file that shows a collapse is the single `sor-egress.json`
(half its connections = 1 bin), which is *not* the campaign data and yields AUC 0.5106 /
TPR 0 on its own — different from the campaign's 0.43. It looks like the mechanism was
inferred from that one anomalous file and over-generalized.

### 2b. So why IS the correlator defeated? (reproduced, matches runs-sor.jsonl exactly)

Re-scoring each `/tmp/in-sorg-N` + `/tmp/eg-sorg-N` pair reproduces `runs-sor.jsonl`
AUCs to 4 decimals (0.4001, 0.4458, 0.4988, 0.513, 0.4391, 0.4196, 0.342, 0.3393,
0.4028, 0.5188). The real difference between arms is the **linked-pair correlation**,
not bin count:

| arm | diag mean (linked r) | off-diag mean | AUC | TPR@1% |
|---|---|---|---|---|
| WG | **+0.708** | +0.018 | 0.92 | 0.70 |
| Tor | +0.267 | +0.014 | 0.82 | 0.10 |
| SOR (campaign) | **−0.01 to −0.11 (≈0)** | ≈ −0.02 to −0.04 | 0.34–0.52 | 0.00 |

SOR's truly-linked ingress/egress pairs correlate **no better than random unlinked
pairs** (both ≈ 0). The fingerprint is destroyed by **decorrelation / timing reshaping**,
not by bin collapse. Mechanism as written is wrong; the *outcome* (linkage lost) is real.

### 2c. Is AUC 0.43 a real anti-correlation or noise around chance?

Null AUC SD for n=20 (20 diagonal vs 380 off-diagonal scores): **0.0663** by both 3000-draw
permutation and the analytic Mann–Whitney formula sqrt((n1+n2+1)/(12·n1·n2)).

- Per-run AUCs (0.34–0.52) scatter within ~1 null SD of 0.5 → each run is individually
  consistent with chance.
- Aggregate mean 0.4319 over 10 runs, SE ≈ 0.021 → z ≈ −3.2 vs 0.5. So the mean is
  *statistically* a hair below 0.5 — a weak, consistent **anti**-correlation (linked pairs
  slightly more negatively correlated than unlinked). Magnitude is tiny (0.07 below chance).

Interpretation: this is "the correlator is a coin flip, leaning a touch below." AUC < 0.5
does **not** mean SOR is *more* resistant than a hypothetical chance baseline — chance (0.5)
is the resistance ceiling for an end-to-end correlator; 0.43 just means the adversary does
marginally worse than guessing. The finding's framing of 0.43 as a graded resistance value
below Tor's 0.76 is defensible only as "fully defeated vs. partially defeated," not as a
mechanism-bearing number.

## 3. ALTERNATIVE EXPLANATIONS / BUG CHECK — TPR=0 is not a data bug

- **Egress not empty / not all-identical / not 1-bin degenerate** — campaign egress mean
  ~8 varied non-zero bins (§2a).
- **Ingress non-degenerate** — `ingress` key carries 20 connections, mean ~10.7–12.9
  non-zero bins per flow across runs; healthy variation.
- **Not a scoring edge case** — thresholds compute normally (~0.4–0.55); SOR diag_max
  (e.g. 0.14, 0.21, 0.46) simply falls below threshold, so TPR=0 is earned, not an
  exception/NaN path. Reproduction matches the logged `runs-sor.jsonl` exactly ⇒ aggregate
  is faithfully derived, no fabrication.
- **Unruled-out artifact (flag):** `correlate()` does element-wise bin alignment with **no
  lag/offset search**. SOR adds a 2-hop nested-SSH path via the grok-bot cloud relay; any
  latency offset ≥ 1 bin between the ingress and egress capture clocks would destroy
  correlation *purely from misalignment*, mimicking "resistance." The finding itself marks
  SOR latency as "— (artifact)" and logs `lat_ms ≈ 0.11` — an implausible value for a
  2-hop nested SSH through a cloud relay, i.e. the SOR timing capture is admittedly broken.
  If the timestamp base is unreliable, the ingress/egress bins may simply be mis-aligned.
  **This decorrelation-by-misalignment hypothesis is a live confound the study did not
  rule out**, and it is at least as consistent with the data as a genuine transport property.

## 4. VERDICT

- **Correlator: correct and well-oriented.** No bug. Safe to trust its scores.
- **SOR resistance (TPR=0): a real measured effect of the data, not a scoring/data bug** —
  linked pairs genuinely fail to correlate, and the pipeline reproduces exactly.
- **But the published MECHANISM is wrong.** SOR egress does NOT collapse to ~1 timing bin
  (it carries ~8 bins, like WG/Tor); linkage is lost via *decorrelation*, not binning.
  The "~1 bin" claim appears to come from one anomalous file (`sor-egress.json`) that is
  not the campaign data.
- **AUC 0.43 ≈ chance, slightly under** (within ~1 null SD/run; null SD=0.066). Treat it as
  "correlator defeated → coin flip," not as a graded anti-correlation signal.
- **Open confound:** the correlator has no lag tolerance and SOR's own latency capture is
  admittedly an artifact (0.11 ms). Decorrelation could be a timing-misalignment measurement
  artifact of the extra relay hop rather than a transport property. Not ruled out.

**Bottom line:** the *correlator* passes; the *claim that SOR defeats correlation* is
directionally supported (TPR=0 reproduces), but the *mechanistic explanation* in finding-06
is unsupported by the data and should be retracted/rewritten, and the no-lag-search vs.
broken-latency-capture confound should be closed before calling the resistance a transport
property.
