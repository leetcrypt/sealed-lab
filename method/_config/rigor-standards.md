# Rigor Standards (Layer 3 — canonical)

Referenced by stages 03 (Design + Statistics), 04/05 (Reproducibility), 06 (Statistics),
08 (all sections, as audit criteria). One rule, one home: cite these sections, don't copy.

## Design

- Every hypothesis test needs an explicit **comparison**: control condition, baseline
  method, or null model. "We ran X and it worked" is not an experiment.
- **Variables ledger**: every design names its IVs (manipulated), DVs (measured),
  and confounds. Each confound gets one of: hold constant · randomize ·
  measure-and-model · accept-with-rationale (goes to the paper's Limitations).
- **Threats to validity** — address all four every time:
  - *Internal*: could something other than the IV explain the effect?
  - *External*: to what populations/settings/models do results generalize?
  - *Construct*: does the metric actually measure the concept in H1?
  - *Statistical conclusion*: power, assumption violations, fishing.
- Randomize order/assignment wherever feasible; when infeasible, counterbalance and say so.
- Prefer the **simplest design that can falsify H1**; complexity needs justification.

## Statistics

- **Analysis plan precedes data.** Tests, α (default 0.05), sidedness, effect size
  measure, and multiple-comparison correction are fixed in the pre-registration.
- **Report effect sizes + 95% CIs** for every comparison; a p-value alone is never a result.
- Multiple comparisons: Holm–Bonferroni by default; FDR (Benjamini–Hochberg) acceptable
  for large exploratory families — but then it's labeled exploratory.
- Check test assumptions (normality, variance homogeneity, independence); if violated,
  use the pre-registered fallback (non-parametric / bootstrap / permutation).
- For stochastic systems (incl. LLMs): ≥ the pre-registered number of repeated runs per
  condition; report mean/median with dispersion, never a single run.
- Null results are reported with the same prominence as positive results. Consider
  equivalence testing (TOST) when claiming "no difference".
- Forbidden: optional stopping without a pre-registered sequential design, p-hacking,
  dropping conditions post-hoc, rounding p to cross thresholds, HARKing.

## Design arithmetic (mandatory at stage 03)

Rationale and the incident that produced these rules: `shared/honesty-assessment-and-solutions.md`.
Pre-registration prevents HARKing; it does **not** prevent an underpowered design or an
unfalsifiable hypothesis whose defects the prose conceals from its own author. Fluent
methodological writing is cheap. **Do not audit prose — execute arithmetic.**

- **No asserted numbers.** Every committed quantity (sample size, CI half-width, MDE, power,
  detectable effect) must be the **output of committed code**, cited by path, with the output
  pasted into the design notes. A stated number with no producing script is an audit failure.
- **Prefer a generative simulation to a closed form.** Not for accuracy — because a simulation
  forces the model to be written down, so confounds become **required function parameters**
  instead of terms that can be silently omitted. Closed forms are where missing terms hide.
- **Clustered designs: the cluster is the sample.** If observations share state (same run,
  session, host, VM, subject), effective n is the number of **clusters**, not rows.
  DEFF = 1 + (m − 1)·ρ; precision is bought with **more clusters**, never a bigger cluster.
  Any precision claim must be stated **conditional on ρ**, with ρ declared as an assumption and
  measured before the confirmatory battery.
- **Rates at a fixed operating point.** A DV of the form "TPR at fixed FPR" has its threshold set
  by an empirical quantile of the negative set. Declare the negative-set size and either fix the
  threshold on a large pooled held-out set, or carry the quantile's instability in the model.
- **Run the null-simulation gate before freezing.** Execute the pre-registered decision rule
  against synthetic worlds and report:
  - `P(declare H1 | null world)` — **≈ 1.0 means the hypothesis is a tautology**; above α means
    the test is liberal.
  - `P(declare H1 | effect = MDE)` — below the power floor means **underpowered**.
  - `P(deliver the reportable null | a world where the null is true)` — below the floor means the
    design **cannot deliver its own null**, so "null results are reported with equal prominence"
    is unimplementable rather than merely unfulfilled.
- **Beware equivalence bands inside the H1 rule.** A rule of the form *"CI excludes 0 **and** both
  CI bounds are beyond ±MDE"* reaches the power floor only at roughly **MDE + one CI half-width**,
  not at MDE. Either restate the MDE as the effect where power actually reaches the floor, or relax
  the rule to a point-estimate criterion — and say which.
- **Two-axis (Pareto / dominance) verdicts:** name the single adjudicating axis, and pre-register
  what is concluded when one axis is worse and the other tied. If "dominated" requires a
  disadvantage on *both* axes, that state is permanently inconclusive and must be declared as such.
- **Pre-register the assumptions, not only the tests.** Each assumed parameter carries the stage at
  which it will be **measured**. Divergence from the assumed value requires a written deviation and
  a re-run of the design check with the measured value. *A simulation lies confidently when its
  generative model is wrong* — this is the only mechanism that closes that hole.
- **Gates refuse, they do not warn.** A design-check FAIL blocks the freeze. Advisory warnings get
  clicked through, which defeats the purpose for exactly the non-specialist users this pipeline
  exists to serve.
- **A gate that cannot be satisfied is worse than no gate**, because it trains people to click
  through FAIL. A design may retain a disqualified RQ to demonstrate its defect numerically; mark it
  `"expect_fail": ["T","N"]` with a written `rejected_because`. The named gates are then *required* to
  fail — the failure becomes a positive test, and a counter-example that stops failing is a real
  FAIL because the demonstration it exists to provide is void. `expect_fail` without
  `rejected_because` is a silenced gate and is itself a failure.

## Reproducibility

- **Determinism**: all seeds fixed, stored in config files, and echoed into run logs.
- **Environment pinning**: exact dependency versions (lockfile or `pip freeze`) live
  with the experiment code; record OS, hardware, and model/API versions where relevant.
- **Raw data is immutable**: written once by stage 05, checksummed (SHA-256), never
  edited. All cleaning happens in analysis code, on copies, driven by pre-registered rules.
- **Everything regenerable**: every number, table, and figure in the paper must be
  producible by re-running committed code on the raw data.
- **Provenance chain**: brief → gaps → hypothesis → prereg (hashed) → code → run log →
  raw data → analysis → paper. Any break in the chain is an audit failure in stage 08.
- **Seals are verified by a script, not by trust**: `python3 tools/verify_seals.py` checks every
  recorded SHA-256 against its file. Run it at stages 05, 06 and 08, and after any amendment.
  A sealed prereg was once edited in place here and the break was found only because `git status`
  happened to show the file dirty — luck is not a control.
- **A sealed file is never edited in place.** Amendments go in a **separate, separately sealed
  addendum** so the original stays verifiable and the change stays visible. Re-hashing a modified
  prereg to make the check pass destroys the only evidence that it moved, and makes an honest
  amendment indistinguishable from tampering.
- **Seal only committed content, and verify in the same session.** Hash the file, commit file and
  seal **together**, then run `python3 tools/verify_seals.py` immediately and paste the `[  OK  ]`
  line into the design notes. A seal computed before the content is under version control pins
  nothing: `PREREG-loop-efficacy-002` was hashed at freeze, amended in place while still
  uncommitted, then committed alongside its now-stale seal — so the seal had **never** verified,
  the sealed text was never in git, and it was unrecoverable by the time the break was found.
  An unverified seal is not a seal.
- **A freeze is a commit, not a timestamp in prose.** "Frozen: <date>" is an assertion; the commit
  hash of the sealed file is the evidence. Freeze IDs cite the commit. When a seal is unrecoverable,
  the honest move is a **declared re-baseline** — retain the broken hash as a comment, label the new
  line a re-baseline rather than a verification, and write down which claims it can no longer
  support. Never a silent re-hash.

## LLM / agent experiments (this workspace's common case)

- Pin model IDs and sampling parameters (temperature, top_p, max tokens) in config.
- Treat prompt text as experimental material: version it, include it in Methods/appendix.
- Account for non-determinism even at temperature 0: repeated runs, report variance.
- Guard against contamination: note whether test items could plausibly be in training
  data, and say how that was checked or why it's accepted.
