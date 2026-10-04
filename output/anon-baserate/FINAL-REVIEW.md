# FINAL REVIEW — anon-baserate submission (independent adversarial, pre-submission)

- **Reviewer role:** final independent adversarial reviewer. Assumed nothing; re-ran the gates,
  re-implemented the lag-search scorer from scratch, and cross-checked findings against raw data.
- **Date:** 2026-10-04 · **Working dir:** `/home/trilltechnician/coding/hackathon`
- **Verdict: GO for submission.** The headline (verification caught a false finding) is honest
  and independently reproduced; the three rigor gates pass and demonstrably gate; the SOR>Tor
  retraction is correct. One coherence gap (missing in-file supersede banners on finding-01/04/06)
  was fixed during this review. Remaining issues are low-severity cleanups, none blocking.

---

## 1. Gates re-run independently — ALL PASS (exit 0)

| gate | command | result |
|---|---|---|
| Seals | `verify_seals.py output/anon-baserate` | **PASS** — verified 4, mismatched 0, missing 0, unsealed 0 |
| Design | `design_check.py config/designs/anon-baserate.json` | **PASS — 10 gates** (power 0.994, null 0.967, tautology 0.030) |
| Instrument | `instrument_check.py config/instruments/anon-baserate.json --gates OEP` | **PASS** — O both correlators hit 3/3 anchors; P `correlator.py` tracked+clean |

Note: `correlator.py` was committed again during this review (now `5a5d869`, adding
`correlate_lag` docstring + `linkage_auc_lag`); the provenance gate re-ran clean, so no
tracked/dirty violation. The earlier reports' hashes (`e8969ed`, `2340328`) are just older commits.

## 2. Lag-search flip — INDEPENDENTLY CONFIRMED

Re-implemented Pearson `correlate`, `correlate_lag` (max over ±10 bin shifts), Mann-Whitney AUC,
and the k-th-highest-negative empirical threshold **from scratch** (did not import
`verify_result.py` / `lagscore.py`). Scored the raw `/tmp/in-sorg-*.json` + `/tmp/eg-sorg-*.json`
(and tor/wg) pairs:

| arm | naive (lag-0) TPR | lag-search (±10) TPR | matches claim |
|---|---|---|---|
| **SOR** | **0.000** (all 10 runs) | **0.275** (all 10 runs) | ✔ = lagscore-full.json 0.275; finding-07 "~0.27" |
| Tor | 0.130 | 0.030 | ✔ Tor becomes most resistant |
| WG | 0.690 | 0.573 | ✔ stays most linkable |

**The flip reproduces exactly.** SOR goes from TPR≈0 (looks maximally resistant) to 0.275 under a
lag-aligning adversary, and the SOR/Tor ranking inverts (Tor most resistant). Confirmed, not disputed.

finding-08's robustness sweep also reproduces independently: lag-0 SOR TPR = 0.000/0.000/0.000/0.005
across FPR (exact match); lag=10 headline 0.275 at FPR=0.01 reproduces; SOR TPR ≈0 at lag=2/5 and
only rises at lag≥10 — confirming the "flip needs a lag window spanning the ~10-bin relay offset"
nuance (not a knife-edge, honestly caveated).

## 3. Headline / supersession status

- **finding-07 is the headline.** Titled "VERIFICATION CAUGHT A FALSE FINDING"; CONTEXT.md,
  docs/OMNIGENT-ROLE.md, and every live/demo teleprompter tab point to it. ✔
- **Demo is retraction-disciplined.** Stale pre-finding-07 tabs are explicitly marked
  "DO NOT READ · Superseded by finding-07"; vo-script.md marked SUPERSEDED; every live cut says
  "Do not say SOR is more resistant than Tor." ✔
- **Fixed during review:** finding-01, finding-04, and finding-06 had **no in-file supersede/
  retraction banner** — only CONTEXT.md marked them. A reader opening finding-06 directly would
  have seen a "confirmatory H1 — SOR more resistant" body with only the milder verifier-A
  downgrade. I added concise top-of-file banners pointing to finding-07 (findings are not sealed;
  no seal impact).

## 4. Issues found (prioritized)

**P1 — fixed in this review:**
1. Missing in-file supersede banners on finding-01/04/06 → added, pointing to finding-07.

**P2 — low severity, recommend fixing before/at submission (none blocking):**
2. **Raw-vs-aggregate count mismatch.** `real-data/runs-sor.jsonl` has **12** SOR runs;
   `aggregate-real.json` reports **n=10** (runs 11–12, AUC 0.4676/0.4337, silently dropped).
   TPR impact = zero (all 12 SOR TPR=0); AUC mean shifts 0.4319→~0.435 (negligible). No deviation
   logged for the drop. In a now-retracted finding, but reconcile or log it.
3. **n=6 lag number provenance.** finding-07's table and the demo cite the n=6 subset (SOR 0.27).
   `lagscore.py` takes `sorted(glob(...))[:6]`, i.e. the **lexicographic** subset {1,10,2,3,4,5}
   → 0.267; numeric {1..6} → 0.250; the robust **all-10** value is 0.275 (lagscore-full.json,
   finding-08). Directionally identical, but recommend quoting the all-run 0.275 as the headline
   number rather than the glob-order-dependent n=6 0.27.
4. **sd_run drift (already flagged, unreconciled):** 0.1122 (aggregate) vs 0.1149 (refit) vs 0.112
   (finding), and 34-vs-35 run counts. All < 0.13 → no ruling impact. Reconcile to one sourced value.
5. **`result.json` (sim) has no "superseded" pointer** (VERIFICATION-GATES nit #3 unapplied). It is
   now doubly superseded (by the real campaign, itself retracted by finding-07). Add a one-line note.

**P3 — informational / correctly disclosed, no action required:**
6. `real-data/paired.jsonl` now holds 7 paired runs **scored with the naive lag-0 correlator**
   (sor_tpr all 0 = the known artifact). No finding cites it as confirmatory — good. CAUTION: the
   next-step paired battery must use the lag-searching (and *gated*) correlator, or it will
   re-manufacture the retracted artifact.
7. `correlate_lag`/`linkage_auc_lag` are **not yet gated** by instrument_check (no orientation
   anchor / E-gate entry). finding-07 discloses this and correctly marks the corrected ranking
   (Tor most resistant) as **provisional** until the lag correlator is registered. Accurate.
8. Stale commit hashes / "Tech.tsx stale" references in tech scripts — self-flagged as stale
   production notes, not shipped claims.

## 5. Integrity checks passed

- Seals verify and **actually gate** (tampered prereg → MISMATCH); design gate fails underpowered
  designs; instrument gate fails an inverted scorer. Confirmed by VERIFICATION-GATES and consistent
  with my re-runs.
- Pre-registration chronology is sound (DV frozen 20:37, first real data 22:28; git order agrees);
  DV changes each made H1 *harder* (no HARKing); confirmatory/exploratory cleanly separated;
  deviations (D-real-1 unpaired→conservative, D-real-2 latency artifact, `tril` exclusion) logged
  pre-analysis.
- The scorer is faithful: three independent re-implementations (two prior verifiers + mine) all
  reproduce the committed numbers; SOR TPR=0 is a real scoring outcome, not a divide-by-zero.
- The one "authenticity smell" (11/20 SOR flows collapsing to bin 0 in the single-file capture) is
  in `sor-egress.json`, which is NOT the campaign data and is not used for the headline; the
  campaign SOR egress carries ~8 non-zero bins (verified). Flagged by verifier C, does not touch
  the retraction (which stands on the lag re-score, not on the "~1 bin" mechanism — itself retracted).

## 6. Bottom line

**GO.** The submission's contribution is the meta-result — the lab's verification layer caught and
retracted a plausible-but-false "SOR beats Tor" finding before it shipped — and that result is
real, independently reproducible, honestly caveated, and backed by gates that demonstrably gate.
The remaining issues are documentation/reconciliation cleanups (P2/P3); none undermine the headline
or the go decision.
