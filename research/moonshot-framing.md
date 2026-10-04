# Moonshot Framing — A Nobel-Caliber Breakthrough in Security + AI

> Ideation, 2026-10-03. The brief's north star is AlphaFold: an AI system that cracked a
> decades-old grand challenge (protein structure) and enabled discovery at 200M scale.
> Question: what is the cyber + AI equivalent, and which version can OUR lab actually
> produce evidence for in one night, through Omnigent, with real rigor?

## What "Nobel-caliber" means here (calibration)

A breakthrough of this class is not a better tool. It is one of:
1. **A fundamental limit** established or mapped (Shannon, Landauer, thermodynamics).
2. **A grand challenge** cracked that unlocks a field (AlphaFold, the human genome).
3. **A phase change** in a long-standing asymmetry (a defense that provably outpaces attack).

The brief rewards *ambition with evidence*: "an ambitious question and a meaningful,
reproducible result," and "the strength of your evidence matters more than the multiplier."
So the win is a grand-challenge *framing* wrapped around a loop we can actually close.

## Four candidate moonshots

### M1 — "The thermodynamics of privacy": mapping the anonymity trilemma  ★ recommended
There is a proven impossibility theorem: an anonymous-communication protocol can achieve at
most two of {strong anonymity, low bandwidth overhead, low latency overhead}
(Das, Meiser, Mohammadi, Kate, *Anonymity Trilemma*, IEEE S&P 2018, eprint 2017/954;
extended PoPETs 2020). It is a fundamental bound, like a second law for privacy.

**The grand challenge:** nobody has *empirically mapped where real deployed systems sit*
relative to this theoretical frontier, nor established whether modern **AI-driven traffic
analysis is bending the achievable frontier inward** — i.e. whether low-latency privacy is
on borrowed time. That is the AlphaFold-shaped move: turn a theorem into a measured map.

- **The lab's output:** for each system (VPN, Tor, SOR, I2P, +dummy-traffic variants),
  a measured triple (anonymity = resistance to end-to-end linkage; latency overhead;
  bandwidth overhead), plotted against the theorem's predicted constraint — with the
  honest-base-rate correction (`research/cyber-eval-gaps.md` gap #5) applied.
- **Why Nobel-shaped:** it is about a fundamental trade-off and its limit, falsifiable,
  with stakes (if AI correlation moves the frontier, every low-latency anonymity system
  must add overhead or lose its guarantee).
- **Why feasible tonight:** the theorem *predicts* where each arm should fall, so even one
  clean loop yields a real data point ON the frontier map. Uses exactly our assets.
- **Result that changes the next decision:** an arm landing far from its predicted frontier
  position reopens the question (measurement artifact, or genuine anomaly worth the next arm).
- **"Ultimate next step" (brief blesses skipping it):** validate on **real deployed
  networks and real hardware** — the live Tor network, the fleet phones `tril`/`fp6` over
  real cellular/WiFi — instead of emulation. This is our "wet-lab equivalent."

### M2 — Autonomous vulnerability discovery + proof (the AIxCC lineage)
DARPA's AI Cyber Challenge concluded Aug 2025: 7 systems patched 43/54 synthetic vulns,
found 18 new real-world flaws, ~45 min/patch; four systems open-sourced
(darpa.mil/news/2025/aixcc-results; SoK arXiv:2602.07666). The moonshot: AI that renders
whole bug classes extinct and flips the offense-defense asymmetry.
- **Prestige:** highest. This is the field's actual moonshot.
- **Feasibility tonight:** low. Cyber-reasoning systems are multi-year builds; we have none.
- **Our honest slice:** a *rigor/reproducibility audit* of autonomous-patching claims
  (do reported patch rates replicate under fixed seeds?). Real, but less "breakthrough,"
  more "meta-science." Weaker fit to our anonymity assets.

### M3 — Provable security for AI agents (neuro-symbolic verification)
Grand challenge: prove a black-box agent's action sequence satisfies safety invariants
*before* execution (arXiv:2609.13731, 2605.29251, 2309.01933). Deep and timely.
- **Feasibility tonight:** low; theoretical, little measurable evidence in 24h.
- **Fit to assets:** weak. But note: our own gate-policy layer is a *practical* instance of
  "provable-ish" pre-execution guarantees — worth one slide, not the whole study.

### M4 — Making security an empirical science (the meta-moonshot)
The deepest gap: security claims are rarely reproducible or falsifiable the way physics is.
The breakthrough = pre-registration + reproducible measurement as the norm. This is literally
what our lab embodies.
- **Risk:** too meta for a "domain breakthrough" judge. Best used as the *lab's identity*,
  not the headline question.

## Recommendation: M1 as the question, M4 as the lab's identity

Frame the study as **M1** (map the anonymity trilemma against its theoretical limit, and
test whether AI traffic analysis is moving the frontier), executed by an Omnigent lab that
embodies **M4** (every result pre-registered, sealed, reproducible). This:
- Upgrades Plan A from "which is more secure" (incremental) to "where do real privacy
  systems sit on a fundamental trade-off, and is the ground shifting" (grand-challenge).
- Keeps every verified asset: VPN/Tor/SOR/I2P arms, the sealed correlator, the rigor gates.
- Gives a crisp AlphaFold analogy for the 2-minute demo.
- Has a genuine, brief-blessed "ultimate next step": real-network / real-hardware validation.

## Track-compliance calibration (re-read of challenge-03-brief.pdf)

| Brief requirement | How M1 satisfies it |
|---|---|
| **Omnigent orchestrates the LIVE loop** (not described — run) | The capture→score→decide-next loop is driven by Omnigent agents exchanging structured outputs, adapting after each frontier data point |
| One complete loop: Q→Evidence→Hypothesis→Experiment→Result→Updated decision | Q: where on the frontier? → lit (trilemma papers via arXiv/OpenAlex) → H: AI-era linkage pushes low-latency arms below the strong-anonymity bound → planner picks test → capture → base-rate-corrected linkability → reopen |
| ≥2 tests; planner picks by expected learning / feasibility / cost under budget | breadth (all arms, balanced) vs depth (honest base-rate on decisive arms); scored by `design_check` power/MDE |
| Experiment = reproducible computational test producing evidence | "data you generate yourself" (captures) + analysis against a theoretical bound |
| Human approval + safety agent | human seals prereg + approves execute; safety policy pins scope to our own fleet |
| Citations; label agent hypotheses; preserve uncertainty; document controls + approval; **state validation still needed before real-world use** | trilemma + eval-gap citations; frontier positions carry CIs; the "real-network validation" is the stated remaining step |
| Show 10× on ONE bottleneck; report observed multiplier | bottleneck = *trustworthy* evaluation; gates-on vs gates-off A/B → verified results per hour |
| Scoring 30 orch / 25 breakthrough / 20 accel / 15 rigor / 10 creativity+resp | M1 lifts the 25 (breakthrough) and 10 (creativity) without weakening the 30/15 we already own |

## Open decision for the user

1. **Headline question:** M1 (anonymity-trilemma map) — recommended — or stay with plain
   Plan A (three-arm linkability), or attempt an M2 slice?
2. **Arms for tonight:** VPN + Tor + SOR (+ I2P as the 4th if the partial setup cooperates)?
3. **"Ultimate next step" to feature:** real deployed Tor + fleet phones over real radio?
