# Scientific Gaps in AI-Assisted Red-Team / Blue-Team Work

> Support material for the demo video. Framing: the science-of-security-evaluation,
> not operational attack technique. Every claim is cited. Researched 2026-10-03.

The recurring 2026 finding is not that AI security tools fail — it is that **their
reported numbers are not trustworthy**. The general "verification gap" (see
`field-challenges.md`) is sharper here because security has ground truth but routinely
measures against the wrong one.

## The gaps

1. **Success-rate-only evaluation hides cost and variance.** Offensive agent scores
   climb with inference budget; defensive scores do not follow the same curve. A bare
   success rate misrepresents both. *Beyond Success Rate: Cost-Aware Evaluation of
   Offensive and Defensive Security Agents* — Kassianik, Nelson, Singer, arXiv:2607.15263.

2. **The "illusion of efficacy" in ML intrusion detection.** Near-perfect in-dataset,
   near-chance cross-dataset. Causes: feature leakage, labeling errors, unrealistic
   train/test temporal separation, non-representative class balance.
   *Evaluating ML-based IDS: The Illusion of Model Efficacy* — Spanos, Kantzavelou,
   arXiv:2609.02469. Cross-dataset study: arXiv:2203.04686. Six design issues
   (feature diversity, interdependence, ambiguous labels, distribution collapse,
   artificial diversity, labeling errors) — ScienceDirect S1389128625001458.

3. **LLM-generated detection rules fire with high false-positive rates** and
   hallucinated fields unless grounded and validated on labeled data.
   *CTI-REALM*, arXiv:2603.13517; *Verification-Guided Specification Synthesis for
   IDS Rules*, arXiv:2608.22889; *LLMCloudHunter*, arXiv:2407.05194.

4. **AI SOC triage lacks empirical grounding.** Few studies measure trust calibration
   or false-positive fatigue; no standardized benchmark, so demo accuracy does not
   survive real conditions. *AI-Augmented SOC: A Survey*, MDPI 2624-800X/5/4/95;
   *SIABench* (first systematic eval of 11 LLMs on incident analysis, 2026).

5. **Traffic-analysis studies fall for the base-rate fallacy.** Over 0.9 accuracy in
   the lab degrades sharply once the monitored set and realistic background traffic are
   modeled honestly — accuracy drops from >95% (5 sites) to <80% (25 sites).
   *Real-world WF evaluation*, arXiv:2603.07412; Cherubin et al., USENIX Security 2022
   (online WF); Juarez et al. 2014 (critical evaluation of WF assumptions).

6. **Red/blue co-evolution claims are large and unreplicated.** Arenas report dramatic
   swings (one: attacker success 72%→5% over six iterations) with no fixed-seed
   replication. *ACEA*, arXiv:2609.08256; *Autonomous Adversary*, arXiv:2605.06486;
   survey arXiv:2505.12786.

## Why this is our opening

All six are the same shape: **security AI is measured against a convenient ground truth
instead of an honest one, with no reproducibility artifact.** sci-method's executable
gates (pre-registration seals, `design_check`, `instrument_check`, `verify_seals`) are a
direct, rare answer. Almost no security-AI paper ships in-loop verification.

## Chosen direction

**Plan A** — anonymity-network linkability under an honest base rate (gap #5), because
the test infrastructure already exists and the failure-prone component (the scorer) is
exactly what `instrument_check` guards. Fallback: gap #2 (illusion of efficacy),
pure-compute on public datasets. See `docs/PLAN-A.md`.
