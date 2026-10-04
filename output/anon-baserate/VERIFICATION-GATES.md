# VERIFICATION-GATES — independent rigor/integrity audit (anon-baserate)

- **Auditor role:** independent, adversarial rigor + pre-registration integrity check.
- **Date:** 2026-10-03 · **Working dir:** `/home/trilltechnician/coding/hackathon`
- **Verdict (one line):** Rigor chain is **INTACT and HONEST**. Seals verify, all gates
  PASS on the real configs and **actually FAIL on injected defects** (they gate). Three
  minor documentation nits found, zero integrity violations. No HARKing detected.

---

## 1. SEALS — PASS

`python3 method/tools/verify_seals.py $(pwd)/output/anon-baserate`:

```
verified 4   mismatched 0   missing 0   unsealed 0
[OK] prereg-anon-baserate.md
[OK] addendum-01-substrate-and-adversary.md
[OK] addendum-02-confirmatory-dv.md
[OK] addendum-03-final-dv-spec.md
```

Manual re-hash confirms the tool is honest:

```
prereg-anon-baserate.md.sha256 : 2d92bcda1a126949f4a2782c43d4e34ed6038ba6bfa165e075630bf7f4a94feb
sha256sum prereg-anon-baserate.md: 2d92bcda1a126949f4a2782c43d4e34ed6038ba6bfa165e075630bf7f4a94feb  (MATCH)
addendum-02 .sha256            : 8b750459846d5c21fe5f073c7f8470bb48f33be654b9fe594307796ed9161b84
sha256sum addendum-02          : 8b750459846d5c21fe5f073c7f8470bb48f33be654b9fe594307796ed9161b84  (MATCH)
```

**Seal gate actually gates:** ran it on the injected defect
`experiment/defects/tampered/prereg-tampered.md` (content altered, carries the real
prereg's seal hash) → `[MISMATCH] ... verified 0 mismatched 1`. The seal catches
post-seal edits. PASS.

## 2. DESIGN GATE — PASS (both configs, 10/10)

`design_check.py config/designs/anon-baserate.json` → **VERDICT: PASS — 10 gates**
`design_check.py config/designs/anon-baserate-refit.json` → **VERDICT: PASS — 10 gates**

Key gate values:

| gate | anon-baserate (sd_run=0.10) | refit (sd_run=0.1149) | limit |
|---|---|---|---|
| T tautology P(H1\|effect=0) | 0.030 | 0.030 | ≤ 0.20 |
| P power P(H1\|effect=0.08) | 0.994 | 0.969 | ≥ 0.80 |
| N reportable-null P(H0\|effect=0) | 0.967 | 0.955 | ≥ 0.80 |
| S scale (mde/baseline) | 0.27 | 0.27 | ≤ 0.50 |
| L CI half-width vs claim 0.04 | 0.0344 | 0.0395 | within 10% |

- **Refit uses the measured sd_run and still passes:** the refit config carries
  `sd_run = 0.1149` (vs the sealed assumption 0.10) and still clears all 10 gates
  (power 0.969 ≥ 0.80). The measured value 0.1149 < the pre-registered `0.13`
  return-to-stage-03 threshold, so the design holds without re-opening.
- **Design gate actually gates:** ran it on `experiment/defects/underpowered-design.json`
  (n_runs=4, sd_run=0.3) → **VERDICT: FAIL — 3 of 10** (P power 0.198, N null 0.209,
  CI half-width 0.2224 vs claimed 0.04 = 5.6x overstated), exit 1. Power/null/precision
  gates are not cosmetic.

## 3. INSTRUMENT GATE — PASS (and catches the defect)

- `instrument_check.py config/instruments/anon-baserate.json --gates OEP` →
  **RESULT: PASS** (O orientation: both correlators hit all 3 ground-truth anchors;
  E: none registered; P provenance: `correlator.py` git-tracked & clean at e8969ed).
- `instrument_check.py experiment/defects/inverted-instruments.json --gates O` →
  **RESULT: FAIL — 2 gate rows** (exit 1): "expect 1.0, got 0.0 (returns 1-AUC:
  orientation inverted)". The orientation gate catches a sign-flipped correlator.
  The gate gates.

## 4. PRE-REGISTRATION INTEGRITY — HONEST, no HARKing detected

**Chronology (all DV changes are pre-data).** Filesystem mtimes and git commit order
agree: prereg 20:25 < addendum-01 20:29 < addendum-02 20:35 < addendum-03 20:37, all
**before** the real captures (`real-data/*-ingress/egress.json` at 22:28) and findings
(22:40+). The DV was fixed 20:37; first byte of real data was 22:28. Git corroborates:
seal/addendum commits (`e8969ed` scaffold) precede the REAL-lab commits
(`fcac17b` pilot, `46716ee` confirmatory). The addenda's repeated "Pre-data: no capture
or score exists" claim checks out. (Note: mtimes alone are soft evidence, but git history
independently corroborates.)

**DV evolution is gate discipline, not HARKing.** The DV changed twice (addenda 02, 03),
each change justified pre-data by a *design* flaw, not a result:
1. addendum-01 DV `precision@balanced − precision@base-rate` — rejected as tautological
   (large for every arm at b=0.001; null never occurs). Caught by reasoning, consistent
   with the design_check tautology gate.
2. addendum-02 DV `precision@b(Tor) − precision@b(SOR)` — rejected as scale-mismatched
   (precision ∈ ~[0,0.07] at b=0.001, so delta=0.08 is literally unreachable).
3. addendum-03 (final) DV `TPR@f(Tor) − TPR@f(SOR)` — TPR has full [0,1] range, delta
   detectable. This is the authoritative spec.

Each rejection makes H1 *harder* to declare, not easier — the opposite of what HARKing
toward a desired result looks like. Parent §8 explicitly anticipated the
confirmatory/exploratory demotion.

**Confirmatory vs exploratory clearly separated.** RQ-RESIST is the confirmatory primary
(addendum-03). RQ-SHIFT is explicitly demoted to EXPLORATORY (needs the learned adversary,
deferred — addendum-01) and is labeled EXPLORATORY in every doc. RQ-POS is descriptive
estimation (no accept/reject). The confirmatory family is clean and singular.

**Deviations logged honestly** (`deviations-real.md`): D-real-1 (arms captured unpaired →
switched to the strictly-more-conservative unpaired two-sample bootstrap, logged
pre-analysis), D-real-2 (SOR latency is a local-forward artifact, so it is *withheld* from
the frontier map rather than reported misleadingly), and the `tril` apparatus exclusion
(~21s forward lag, contributed no measurements). These are honest, conservative, and
pre-analysis.

**Did any result drive a design choice? No.** The clearest stress test is the sim→real
direction flip (see §5) — and it is handled by DATA with the DV frozen pre-data, not by
re-labeling. The real campaign even **under-collected** (WG 15 / Tor 10 / SOR 10, all
< the pre-registered n=30), which rules out "collect until significant" p-hacking.

## 5. VERDICT — rigor chain intact and honest

The machinery is real: seals detect tampering, the design gate fails underpowered
designs, the instrument gate fails inverted correlators. The pre-registration is sealed,
its DV changes are pre-data and justified by design flaws (each making the test harder),
confirmatory vs exploratory is cleanly separated, and deviations are logged conservatively.
**No integrity violations.**

### Minor nits (documentation only; none change a verdict)

1. **sd_run provenance drift.** The refit config annotation says `sd_run = 0.1149`
   measured over "34 runs", but `real-data/aggregate-real.json` reports
   `sd_run_measured = 0.1122` and finding-06 says "0.112", over **35** runs (15+10+10).
   Three near-identical numbers (0.1149 / 0.1122 / 0.112) and a 34-vs-35 run-count
   mismatch. Impact: none on the ruling — all are < 0.13, and the refit uses the *more
   conservative* (higher) 0.1149 and still passes. Recommend reconciling to a single
   sourced value.

2. **Real H1 lower bound sits just under delta.** The real confirmatory result is
   gap = 0.13, 95% CI [0.07, 0.21]. Under the prereg §1 decision rule (H1 ⇔ CI lower
   bound > 0) this cleanly declares H1. But addendum-03's compressed phrasing
   ("CI lower bound on mean Δ > 0 and ≥ delta") could be read as requiring the CI lower
   bound ≥ delta=0.08, and 0.07 < 0.08. The two phrasings are mutually ambiguous. To its
   credit, finding-06 *discloses* exactly this ("CI lower bound (0.07) just under δ").
   Recommend pinning one decision rule verbatim. Not a violation — the headline claim is
   honestly caveated either way.

3. **Sim vs real give opposite verdicts — disclosed, not hidden.** `result.json` (sim)
   returns **H0** (gap −0.058, CI [−0.104, −0.014], "SOR NOT meaningfully more resistant").
   `finding-06` (real, 35 runs) returns **H1** (gap +0.13, CI [0.07, 0.21], "SOR more
   resistant"). finding-06 states this plainly: "The simulation returned a null (H0); the
   real repeated campaign returns H1 ... driven by DATA, not by re-labeling," and preserves
   all caveats. This is the honest way to handle a sim/real divergence, but a reader must be
   careful not to cite `result.json` as the headline — it is the sim, superseded by the real
   campaign. Recommend a pointer in `result.json` noting it is the simulation and is
   superseded by the real campaign.

4. **Paired battery is an empty stub (honest "last mile").** `real-data/paired.jsonl` is
   0 bytes and `experiment/real_lab/campaign-paired.sh` is untracked; the sealed design
   specifies pairing by run but the real data is unpaired (D-real-1). This is correctly
   framed as the stated next step, not claimed as done.
