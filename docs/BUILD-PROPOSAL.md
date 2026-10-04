# Build Proposal — A Rigor-Enforced Agentic Discovery Lab on Omnigent

> Challenge 03, Agentic Scientific Discovery (Hack-Nation × Databricks, 7th Global AI
> Hackathon). Working title: **Sealed Lab** (rename freely).
> Inputs: `research/field-challenges.md`, `research/sci-method-state.md`,
> `inputs/challenge-brief.pdf`.

## The thesis in one breath

AI-scientist systems are fast at producing science and slow at making it trustworthy.
Only 38% release seeds or traces. None demonstrate externally validated in-loop
verification (Ding et al. 2026). LLM judges inflate the novelty of their own ideas
(Sinhahajari et al. 2026). So every output needs a human redo, and **verification
becomes the bottleneck**. We port sci-method's *executable* rigor gates into Omnigent as
**blocking policies**. Every hypothesis, design, instrument and claim is checked by
running code before the loop can advance. The result is science that is
**trustworthy by construction**, and that is where the speed-up lives.

## What we build

Seven Omnigent specialist agents. Six map to the brief's suggested roles; the
cross-cutting safety agent is the brief's human-approval role. Each is backed by a
sci-method stage and guarded by an executable gate.

| Agent | sci-method stage | Decision it owns | Tools | Blocking gate (Omnigent policy) |
|---|---|---|---|---|
| **Literature** | 01 | What is known, where the gap is | OpenAlex, arXiv / Europe PMC | Every claim carries a DOI or URL |
| **Insight** | 02 | Falsifiable hypothesis + predictions | Literature output, novelty check | **Novelty-grounding** (new, G7): nearest-neighbour search against OpenAlex, not LLM vibe |
| **Planner** | 03 | Pick 1 of ≥2 candidate tests by expected learning, feasibility and cost, within a budget | `design_check.py --sweep` (power, MDE) | **`design_check` must PASS** (gates T, P, N, S, L), then seal the prereg |
| **Safety / approval** | cross-cutting | Flag risk, route consequential actions to a human | Omnigent policies | Human approves *seal* and *execute*; `ask_on_os_tools`; `cost_budget` |
| **Runner** | 04–05 | Implement and run the test; raw data with provenance | Sandbox (bubblewrap), GPU, data APIs | **`instrument_check` must PASS** (O, E, P); raw data checksummed |
| **Analysis** | 06 | Run the pre-registered analysis; label confirmatory vs exploratory | Stats | **`verify_seals` must PASS**; deviations logged |
| **Knowledge graph / record** | shared record | Update the evidence graph; propose the next loop | `kg-build` (exists, evidence-gated) | **Claim-grounding** (new, G6): every finding links to an artifact |

**The core innovation is the policy layer.** Omnigent policies are Python handlers.
We write handlers that wrap the three sci-method gates and **deny the tool call that
advances the loop** until the gate passes. The brief asks to "enforce the boundary
through tool permissions and Omnigent policies." This does exactly that, and makes the
rigor non-optional rather than a prompt the model can ignore.

### The adaptive loop, which stays ICM-compliant

```
Question → Literature → Insight(+novelty gate) → Planner(≥2 tests, budget, design_check)
  → [human seals prereg] → Runner(instrument_check) → Analysis(verify_seals)
  → Record(KG, claim gate) → next decision ──► NEW sealed addendum (loop again)
```

A surprising result reopens an assumption by starting a **new sealed iteration**. It
never edits an earlier frozen file. The brief gets its adaptivity and every turn stays
pre-registered.

## The experiment: two layers

### Science layer (the question the lab investigates)

**Recommended: materials discovery on NIST JARVIS-DFT.** No API key is needed. The
computed properties provide real ground truth. Loops run in minutes on our 8 GB GPU.
The brief names it as a source. Battery and photovoltaic materials carry the
breakthrough resonance that wins the 25% criterion.

Example question: *Which cheap structural descriptors predict wide-band-gap stability,
and does a descriptor model screen candidates as well as a full-feature baseline at a
fraction of the cost?*

Two competing tests for the planner to choose between, for example:
1. A descriptor-ablation sweep.
2. A held-out chemical-family transfer test.

The choice is scored by `design_check`'s power and MDE estimates against compute cost.

Fallbacks:
- **OpenML ML-methods benchmark.** Lowest risk and fastest, with weaker breakthrough score.
- **Drug repurposing via Europe PMC and PubChem.** High resonance and the strongest
  safety-agent story, but the hardest to test credibly in 24 hours.

### Meta layer (the acceleration evidence, scored at 20%)

We run the brief's own page-3 diagram, "baseline vs proposed method, matched
conditions," on the lab itself.

- **Baseline:** the same Omnigent agents with **gates off**. This is a typical
  AI-scientist loop.
- **Proposed:** gates on.
- **Matched:** same question, model, budget and seeds.
- **Ground truth via defect injection.** We plant known flaws drawn from sci-method's
  real case studies: an underpowered design, a tautological hypothesis, an inverted
  metric, an ungrounded citation. Then we count what each lab emits as a "finding."

| Metric | Why |
|---|---|
| False findings emitted per loop | Direct measure of P1, P2 and P3 |
| Defects caught *before* data collection | Gates move verification to stage 03/04 |
| Claims needing human recheck | Proxy for verification labor |
| Wall-clock from question to *verified* result | The headline speed-up |

We report the multiplier we actually observe, as the brief demands. The honest
headline is **verified results per hour**, not raw outputs per hour.

## 24-hour plan, mapped to the brief's phases

| Window | Deliverable | Exit test |
|---|---|---|
| **H0–1** | Omnigent spike: `omnigent setup` (auth), run one 2-agent YAML handoff, and one custom policy that denies a tool call | A policy blocks a call in the web UI at :6767 |
| **H1–4** | Lock the domain and question. Vendor the sci-method method layer (with the source commit recorded). Pull a JARVIS subset. Write the run brief | `design_check` runs on a stub ledger |
| **H4–10** | Seven agent YAMLs plus the gate-policy handlers. Run one end-to-end loop with gates on | One sealed prereg; one executed test |
| **H10–18** | Second loop iteration (result changes the decision). Defect-injection harness. Gates-off baseline runs | Metrics table populated for both arms |
| **H18–22** | Analysis, figures, KG of the run record, honest multiplier, next experiment | `verify_seals` clean across the repo |
| **H22–24** | 2-minute demo video plus submission package | Checklist below all ticked |

## Submission checklist (from the brief)

- [ ] Repository
- [ ] Agent specifications and policies (`agents/*.yaml`, `config/policies`)
- [ ] 2-minute demo (question → handoffs → experiment → result → learned → next)
- [ ] Cited evidence (`research/field-challenges.md` plus a per-run bibliography)
- [ ] Experiment code and results, sealed and checksummed
- [ ] Measured improvement (meta-layer table)
- [ ] Next experiment, justified from what the lab learned

## How this scores

| Criterion | Weight | Our lever |
|---|---|---|
| Omnigent orchestration | 30% | Seven agents with real handoffs, and **policies that enforce science**, not just routing |
| Breakthrough potential | 25% | Materials screen with real DFT ground truth. A general method for trustworthy autonomous science |
| Acceleration and learning | 20% | Defect-injection A/B with an honest verified-results-per-hour multiplier |
| Scientific rigor | 15% | Pre-registration, executable gates, seals. This is sci-method's home turf |
| Creativity and responsibility | 10% | Human approval gates, safety agent, null results reported |

## Risks

- **Omnigent is alpha (0.16.0).** The policy-handler API may differ from its docs.
  The H0–1 spike exists to retire this risk first.
- **Auth.** `ANTHROPIC_API_KEY` is not exported here. Use `omnigent setup` with the
  Claude subscription or a key. The Ollama fallback lives at `<trillsec-tailnet-ip>:11434`;
  Omnigent defaults to `localhost`, so override the base URL.
- **Overclaiming.** Report the observed multiplier only. Label agent-generated
  hypotheses as such.
- **Scope.** Keep the science layer small. The rigor-gated loop is the product.
