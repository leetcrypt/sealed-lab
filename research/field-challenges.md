# The Three Hardest Problems in Agentic Scientific Discovery

> Support material for the demo video. Every claim below is cited to a 2026 paper.
> These three problems are the backdrop against which we position our build.
> Scope: "AI scientist" systems — LLM-agent pipelines that generate hypotheses,
> design and run experiments, and write up results with little human intervention.

Framing for the pitch: the field has gotten very good at making agents *produce*
science (manuscripts, code, candidate lists). It has not solved making that output
*trustworthy*. The bottleneck has moved from generation to verification. Our lab
attacks the verification bottleneck directly, and that is where the 10× hides —
not in generating more, but in not having to redo everything a human can't trust.

---

## Problem 1 — The Verification Gap: claims are harder to verify than code is to run

The single best-supported finding in the recent literature. A 2026 survey of 24
runnable AI-scientist systems found a stark asymmetry: code gets released, but the
artifacts that would let a reviewer *check the claims* do not.

| What gets released | Share of systems |
|---|---|
| Runnable code | 83% |
| Execution seeds / traces (reproducibility) | 38% |
| Any novelty-verification method | 38% |
| Externally validated in-loop verification | 0% |

Of nine "L4" closed-loop systems, seven did only mechanical reruns and one rested on
an unverified author claim. No system in the LLM era demonstrated externally validated
in-loop verification. The authors' line is the thesis of our project:
**"their claims are often harder to verify than their code is to run."**

- Ding, Nannapaneni, Liu, Zhang (2026). *Autonomous Research Agents: A Survey of AI
  Scientists and the Verification Gap.* arXiv:2608.05179.
- Reproducibility is compounded by the stochastic nature of agent trajectories:
  model drift, nondeterministic outputs, prompt sensitivity, undocumented configs —
  rerunning code no longer reproduces the discovery path.
  (*From AI for Science to Agentic Science: A Survey on Autonomous Scientific
  Discovery*, arXiv:2508.14111.)
- Reproducibility as a first-class benchmark target:
  *MLReplicate: Benchmarking Autonomous Research Systems for ML Reproducibility*,
  arXiv:2605.16616.

**Why it blocks 10×.** If no one can verify an agent's result, a human must redo the
work before trusting it. Verification cost, not generation cost, caps throughput.

---

## Problem 2 — The Novelty Mirage: LLMs can't reliably judge or generate novelty

AI-scientist systems lean on an LLM to decide which hypotheses are worth testing.
That judge is systematically miscalibrated. On RQ-Bench, LLM judges rate
model-generated research questions as highly novel, while human domain experts prefer
the real author-anchored questions — the two reach *opposite* conclusions, and the
LLM's bias gets *stronger* in head-to-head comparisons.

- Sinhahajari, Majumder, Poria (2026). *On the Limits of LLM-as-Judge for Scientific
  Novelty Assessment.* arXiv:2606.12071. ("novelty mirage")
- Ideas an LLM rates as more novel are *less* likely to match real future papers —
  models reward novel-sounding framing over genuinely anticipatory thinking.
  *HindSight: Evaluating LLM-Generated Research Ideas via Future Impact*,
  arXiv:2603.15164.
- Grounding novelty in the literature instead of model priors:
  *Literature-Grounded Novelty Assessment of Scientific Ideas*, arXiv:2506.22026.
- Hypothesis generation under-determination and coverage:
  *HypoSpace*, arXiv:2510.15614; survey arXiv:2504.05496.

**Why it blocks 10×.** An agent that can't tell a genuinely new question from a
novel-sounding one spends its budget confirming the obvious or chasing mirages.
Worse, with no frozen plan it rationalizes whatever it found as the thing it set out
to find (HARKing), manufacturing false novelty.

---

## Problem 3 — Grounding & Accountability: hallucinated claims, no evidence chain

Even when an agent is productive, individual claims may be fabricated or mis-grounded:
"code hallucination" (plausible but wrong code), citation fabrication, and confident
restatement of things that are false or merely recalled from training data rather than
discovered. At scale, closed-loop campaigns reveal gaps in hallucination detection.
The deeper problem is structural: science's trust model assumes a human author who can
be questioned and held accountable — agents break that assumption.

- Belinda Mo (2026). *The Age of AI Agents Demands A New Scientific Paradigm To Sustain
  Trustworthy Science.* arXiv:2607.26064. Calls for **observable-by-default workflows,
  scalable verification, and clear attribution**, warning of "experimental results that
  no person can verify, optimization for metrics over understanding, and accountability
  vacuums that erode scientific trust."
- *Position: The Age of AI Agents Demands A New Scientific Paradigm*, arXiv:2607.26064.
- Distinguishing genuine discovery from training-data recall is called out as a core
  open problem in arXiv:2510.09901 and arXiv:2508.14111.

**Why it blocks 10×.** Unattributable, ungrounded claims force blanket human re-checking
and, when wrong, poison downstream decisions and the shared record.

---

## The through-line

All three problems are the *same* problem wearing three hats: **autonomous science is
fast at producing outputs and slow at making them trustworthy.** Reproducibility
(P1), honest hypothesis discipline (P2), and grounded attribution (P3) are exactly the
guarantees that a rigorous human lab enforces by protocol — pre-registration, provenance,
and citation discipline — and exactly what current agent labs skip in the rush to a
manuscript. The literature's prescription (Mo 2026: *observable-by-default, scalable
verification, clear attribution*) is a near-verbatim description of what a
pre-registration-enforced pipeline already does.

That is the opening our build walks through.

## Full source list (for the video credits / references slide)

1. Ding et al. *Autonomous Research Agents: A Survey of AI Scientists and the
   Verification Gap.* arXiv:2608.05179 (2026).
2. *From AI for Science to Agentic Science: A Survey on Autonomous Scientific
   Discovery.* arXiv:2508.14111 (2026).
3. *MLReplicate: Benchmarking Autonomous Research Systems for ML Reproducibility.*
   arXiv:2605.16616 (2026).
4. Sinhahajari, Majumder, Poria. *On the Limits of LLM-as-Judge for Scientific Novelty
   Assessment.* arXiv:2606.12071 (2026).
5. *HindSight: Evaluating LLM-Generated Research Ideas via Future Impact.*
   arXiv:2603.15164 (2026).
6. *Literature-Grounded Novelty Assessment of Scientific Ideas.* arXiv:2506.22026 (2026).
7. *HypoSpace: A Diagnostic Benchmark for Set-Valued Hypothesis Generation.*
   arXiv:2510.15614 (2026).
8. *A Survey on Hypothesis Generation for Scientific Discovery in the Era of LLMs.*
   arXiv:2504.05496 (2025).
9. Belinda Mo. *The Age of AI Agents Demands A New Scientific Paradigm To Sustain
   Trustworthy Science.* arXiv:2607.26064 (2026).
10. *Autonomous Agents for Scientific Discovery: Orchestrating Scientists, Language,
    Code, and Physics.* arXiv:2510.09901 (2026).
11. Royal Swedish Academy of Sciences. *2024 Nobel Prize in Chemistry* (AlphaFold2) —
    the challenge's own north star.
