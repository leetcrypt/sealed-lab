# Verification, Not Generation: A Sealed, Self-Correcting AI Lab That Retracted Its Own Headline Finding on Anonymity-Network Linkability

**Pipeline stage:** 07 (research-paper draft) of the Sealed Lab discovery loop · **Study slug:** `anon-baserate` · **Date:** 2026-10-04
**Status:** DRAFT. Internal, pre-peer-review. All numeric claims are traceable to committed artifacts cited inline.

> **Agent-generated content notice.** This manuscript was drafted by an AI agent (Claude, Opus 4.8) from the
> committed artifacts of the `anon-baserate` study. It is a *report of* an AI-run lab, written *by* an AI. Every
> quantitative claim below carries a citation to a sealed or committed file in `output/anon-baserate/`; no number
> in this draft was produced by the drafting agent. Per the lab's own accountability rule (Mo 2026), agent
> authorship is declared rather than hidden. Human review of this draft has not yet occurred.

---

## Abstract

Autonomous "AI scientist" systems are fast at producing results and slow at making them trustworthy: a 2026 survey
of 24 systems found 83% release runnable code but 0% demonstrate externally validated in-loop verification (Ding et
al., arXiv:2608.05179). We built a sealed, self-correcting lab — pre-registration plus executable gates
(`design_check`, `instrument_check`, `verify_seals`) orchestrated as blocking Omnigent policies — and ran it on a
concrete security-measurement question: the end-to-end linkability of three transports (single-hop WireGuard, Tor,
and a nested-SSH onion-routing analog, "SOR") evaluated at an honest base rate (b=0.001) rather than a balanced
one. A naive correlator produced an exciting result: SOR showed zero linkage (TPR 0.00), apparently more resistant
than Tor. Three independent verification agents and an adversarial lag-search re-analysis showed this was a
measurement artifact — a relay-induced timing offset invisible to a lag-blind scorer. Under a competent
(lag-aligning) adversary the result flipped: SOR became linkable (TPR 0.275) and Tor was provisionally the most
resistant arm. We retract the original claim. A gates-on/off A/B caught 3/3 injected real-history defects before
data collection, emitting zero false findings. The contribution is the meta-result: verification caught a false
finding before it shipped.

*(176 words)*

---

## 1. Introduction

The bottleneck in autonomous science has moved from generation to verification. Ding et al. (*Autonomous Research
Agents: A Survey of AI Scientists and the Verification Gap*, arXiv:2608.05179, 2026) surveyed 24 runnable
AI-scientist systems and found a stark asymmetry: 83% release runnable code, but only 38% release execution
seeds/traces, only 38% ship any novelty-verification method, and **0% demonstrate externally validated in-loop
verification**. Their line is our thesis: an agent's "claims are often harder to verify than their code is to run."
Compounding factors — model drift, nondeterministic trajectories, prompt sensitivity (arXiv:2508.14111;
arXiv:2605.16616) — mean rerunning code no longer reproduces the discovery path. Related failures are the novelty
mirage, where LLM judges and human experts reach *opposite* novelty conclusions (arXiv:2606.12071), and the
accountability vacuum of ungrounded, unattributable claims (Mo 2026, arXiv:2607.26064, which prescribes
*observable-by-default workflows, scalable verification, and clear attribution*). See `research/field-challenges.md`.

Security evaluation sharpens this gap because it has ground truth yet routinely measures against the wrong one
(`research/cyber-eval-gaps.md`): success-rate-only scoring hides cost and variance (arXiv:2607.15263); ML-IDS shows
near-perfect in-dataset and near-chance cross-dataset accuracy (arXiv:2609.02469); and — our chosen opening —
**traffic-analysis studies fall for the base-rate fallacy**, with lab accuracy >95% collapsing once realistic
background traffic is modeled honestly (arXiv:2603.07412; Cherubin et al., USENIX Security 2022; Juarez et al. 2014).

Our scientific frame is the **anonymity trilemma** (Das, Meiser, Mohammadi, Kate, *Anonymity Trilemma: Strong
Anonymity, Low Bandwidth Overhead, Low Latency — Choose Two*, IEEE S&P 2018): strong anonymity, low latency, and low
bandwidth overhead cannot be achieved together. We do **not** test the theorem's constants; we use it as the
qualitative frontier against which we place three transports, and we measure an empirical lower bound on anonymity
(1 − linkage precision at an honest base rate) under one concrete passive both-ends adversary. This operationalization
limitation is pre-registered (`prereg-anon-baserate.md` §2).

This paper reports both a domain result and a methods result, and is deliberately organized around the moment the two
collided: our most exciting domain finding was **false**, and the lab's verification layer caught it. We argue that is
the stronger contribution. The 10× lever in autonomous science is not discovering faster — it is not shipping wrong.

---

## 2. Methods

### 2.1 Pre-registration and executable gates

The design was frozen before any data existed (`prereg-anon-baserate.md`, sealed `2d92bcda…`; SHA-256 committed).
Changes after seal go only into separately sealed addenda; the parent is never edited. Three executable gates act as
boolean, fail-closed pass conditions run *before* output:

- **`design_check`** — verifies the design can conclude (power, CI half-width, false-positive/null rates) from a
  frozen generative model. PASS 10/10 pre-data (`design_check-PASS.txt`).
- **`instrument_check`** — every registered correlator hits ground-truth orientation anchors, every fast path equals
  its sealed reference (equivalence), and every instrument file is git-tracked (provenance). O+E+P green
  (`instrument_check-OE-PASS.txt`).
- **`verify_seals`** — recomputes SHA-256 over the prereg and addenda; a silent post-seal edit fails the gate.

The confirmatory DV went through three pre-data iterations, each recorded for the audit trail (addenda 01/02/03):
(1) `precision@balanced − precision@base-rate` — rejected as degenerate (large for every arm at small b,
non-discriminating); (2) `precision@b(Tor) − precision@b(SOR)` — rejected as scale-mismatched (precision lives in
~[0, 0.07] at b=0.001, so δ=0.08 is unreachable); (3) **final:** the paired per-run detection-rate gap
`Δ = TPR@f(Tor) − TPR@f(SOR)`, which has full [0,1] range so the sealed margin δ=0.08 is detectable
(`addendum-03-final-dv-spec.md`). This iteration is the gate discipline catching two scale flaws *before* any compute,
not post-hoc tuning.

Frozen design arithmetic (unchanged across addenda): run is the resampling unit; n_runs=30 per arm; δ=0.08 (minimum
detectable material shift); sd_run=0.10 as an explicit assumption, re-fit at stage 05, with a **return-to-stage-03
rule if realized run-SD > 0.13**; cluster (run-level) percentile-bootstrap 95% CI; Holm correction across the
confirmatory family; stopping rule fixed (no data-dependent extension). Nulls are reported as results; no HARKing;
deviations logged, never silent (`prereg` §§7–10).

### 2.2 Threat model and scope

Adversary: a passive observer of traffic entering and leaving the network at both ends; no active injection, no
endpoint compromise. All traffic is self-generated to our own sinks on our own fleet (own-fleet only, no third-party
destinations), enforced by safety policy and human approval (`prereg` §3).

### 2.3 Three transports and the honest base rate

- **WireGuard (positive control, not a competitor):** single-hop; near-trivial linkage under a both-ends observer.
  Calibrates that the adversary fires when linkage truly exists — a low score elsewhere is then resistance, not a
  broken instrument.
- **Tor:** real 3-hop onion service (user-run, no root), the distributed-trust comparator.
- **SOR:** 2-hop nested-SSH onion-routing analog, the system under study.

RQ-POS (descriptive): per arm, report linkage AUC, detection at 1% FPR, and precision at the honest base rate,
`precision = b·TPR / (b·TPR + (1−b)·f)` with b=0.001. This is where the base-rate-fallacy contribution is made:
balanced-evaluation TPR/AUC overstates operational linkability, and the frontier map quantifies by how much
(`addendum-03`).

### 2.4 The correlator (the failure-prone component the gate guards)

A self-contained passive flow correlator (`config/instruments/correlator.py`) scores timing-fingerprint similarity
between ingress and egress captures. It was frozen and passed `instrument_check` (orientation + equivalence +
provenance, including a VPN known-linked/known-unlinked anchor) before touching any pilot pcap, to eliminate forking
paths. **Critical limitation, central to the Results below:** the frozen correlator does **no lag search** — it
compares timing bins at zero offset. A stronger adversary (`lagscore.py`, ±10-bin lag search) was authored later
during verification; it is **not yet gated** (no orientation anchors, no equivalence entry), so results from it are
labeled provisional.

### 2.5 Substrate and real-capture campaign

Early loops used grounded simulation (Tor/SOR parameterized by measured latency/jitter/padding; VPN pending real
capture) — the brief admits simulation as a valid experiment (`addendum-01`). The study then moved to **real
captures, own-fleet only** (`finding-04`, `finding-06`). Device roster and one pre-data apparatus exclusion are
logged in `methods-note-devices.md`: the `tril` phone was excluded as a relay (forward-setup ~21 s vs ~2 s for other
phones, causing tunnel timeouts; contributed zero measurements — an operational, not results-dependent, exclusion).
SOR was relayed via a stable cloud VM (`grok-bot`) to remove the mobile-buffering confound. Topology asymmetry is
documented, not hidden: WG/Tor use client=laptop/sink=trillsec; SOR swaps ends so the relay is reachable
(`methods-note-devices.md`). Two deviations from the sealed design were logged **pre-analysis** (`deviations-real.md`):
**D-real-1** — arms were captured sequentially and are therefore *unpaired*, so the analysis uses the strictly more
conservative unpaired two-sample bootstrap; **D-real-2** — for any `ssh -L` arm the client connects to a local
forwarded port, so recorded connect latency (~0.1 ms) does not reflect the multi-hop path; SOR latency is therefore
**not** reported as a frontier coordinate (fix: first-byte RTT).

### 2.6 Omnigent orchestration of the loop

Sealed Lab is the methodology; Omnigent is the orchestration/enforcement layer that runs it (`docs/OMNIGENT-ROLE.md`).
Specialist agents exchange structured outputs through the discovery loop, and the gates run as **blocking policies** an
agent cannot pass until satisfied:

| stage | live Omnigent agent | blocking gate |
|---|---|---|
| hypothesis / plan | planner (selected test T2, citing prereg §8) | `design_check` |
| run experiment | runner (gated shell; a live DENY demo) | `design_check` + `instrument_check` |
| **verify** | **`agents/sealed-lab-verify`** (re-scores adversarially) | `instrument_check` |
| enforce | policy layer | `require_gate` (fail-closed) |

A live deny demonstration confirmed fail-closed behavior: an agent that tried to run the experiment with an injected
inverted correlator was blocked by the rigor policy, refused to bypass, and deferred the fix to a new sealed iteration
(`omnigent-deny-demo.txt`). Crucially, the **verify stage** — the one that produced this paper's headline — ran as an
Omnigent agent whose tool re-scores every arm with the stronger adversary and retracts the claim when linkage jumps
(transcript: `omnigent-verify-run.txt`).

---

## 3. Results

### 3.1 The honest base rate holds (RQ-POS, descriptive)

Across simulation and real data, balanced-looking detection collapses at the honest base rate. On the real 3-arm
pilot (`finding-04-real-frontier.md`), even WireGuard's AUC 0.916 yields only 0.066 precision at b=0.001 — roughly a
14× overstatement versus balanced evaluation. This is the base-rate-fallacy contribution: operational linkability is
far below lab linkability, consistent with the WF literature (arXiv:2603.07412).

### 3.2 The real frontier (pilot, EXPLORATORY) — `finding-04`

Real captures, all three arms, n=20/arm single run (`real-data/*.json`):

| arm | transport | latency | linkage AUC | detection @1% FPR | precision @ base rate |
|---|---|---|---|---|---|
| WireGuard | 1-hop | 7.8 ms | 0.916 | 0.70 | 0.066 |
| Tor | 3-hop onion | 786 ms | 0.822 | 0.10 | 0.010 |
| SOR analog | 2-hop nested SSH | (D-real-2 artifact) | 0.511 | 0.00 | 0.000 |

A real anonymity–performance trade-off appears (WireGuard fast and fully linkable; Tor ~100× latency for lower
linkability; SOR at chance). The pilot DV gap TPR@1%(Tor − SOR) = 0.10 ≥ δ=0.08 gave a provisional **H1** (SOR more
resistant), labeled EXPLORATORY with four caveats including the SOR latency artifact and the relay-buffering confound.

### 3.3 The naive confirmatory result: "SOR > Tor" — `finding-06` (**RETRACTED**)

> **This section records a result that the lab subsequently RETRACTED. It is retained for the audit trail; §3.4
> supersedes it.** `finding-06-real-confirmatory.md` carries a CORRECTION banner dated 2026-10-04.

A repeated real campaign (WG 15, Tor 10, SOR 10 runs; SOR via stable `grok-bot` relay) reported SOR detection
0.00 ± 0.00, Tor 0.14 ± 0.11, WireGuard 0.69 ± 0.10. The unpaired gap TPR@1%(Tor − SOR) = 0.13, 95% CI [0.07, 0.21]
(excludes zero), with a published mechanism: "nested SSH buffers each flow into ~1 timing bin, collapsing the
fingerprint." The initial write-up claimed SOR was *confidently* more resistant than Tor.

An independent verification agent first downgraded this from "confidently more resistant" to
"directional/SUGGESTIVE," because the CI lower bound 0.07 is **below the materiality margin δ=0.08** — the data could
not confirm the advantage was *material* — and flagged a power/threshold conflation (the design's power 0.965 and the
0.13 return-rule threshold are for the *planned paired precision-gap* at n=30, not an *unpaired TPR-gap* at n=10).
The sealed sd_run assumption nominally held (measured spread 0.112 ≤ 0.13), but on an apples-to-different-fruit metric.

### 3.4 The retraction: the result was a measurement artifact — `finding-07` (**headline**)

Deeper verification dismantled §3.3. Verifier C found the published mechanism was **false on the campaign data** —
SOR had ~8 non-zero timing bins, like the other arms, not ~1 — and identified the true risk: the frozen `correlate()`
does **no lag search**, while SOR's extra relay hop adds a timing offset. Misalignment, not resistance, could explain
TPR=0. We tested it directly by re-scoring with a lag-searching adversary (`lagscore.py`, ±10 bins; results in
`lagscore-result.txt`, `lagscore-full.json`):

| arm | naive correlator (no lag) | lag-searching adversary |
|---|---|---|
| WireGuard | AUC 0.91 / TPR 0.68 | AUC 0.88 / TPR 0.56 |
| **SOR** | **AUC 0.47 / TPR 0.00** | **AUC 0.76 / TPR 0.275** |
| Tor | AUC 0.76 / TPR 0.17 | AUC 0.70 / TPR 0.03 |

**The result flipped.** Under a competent, lag-aligning adversary, SOR is linkable (**TPR 0.00 → 0.275**) and Tor is
**provisionally the most resistant arm** (TPR 0.03). The lag-search gap Tor − SOR = −0.245, 95% CI [−0.32, −0.18]
(`lagscore-full.json`) — the opposite sign to §3.3. SOR's apparent "resistance" was an alignment artifact of the
relay's timing offset combined with a lag-blind scorer. **The "SOR > Tor" claim is RETRACTED.** The retraction was
confirmed live by the Omnigent verify agent (`agents/sealed-lab-verify`), which ran `instrument_check` (PASS), read
the scoring script to confirm the artifact flag is data-driven not hard-coded, and retracted the claim
(`omnigent-verify-run.txt`).

### 3.5 Gates-on/off acceleration A/B — `finding-02`

Three defects drawn from this study's *real* history were injected (`experiment/defects/`; `ab-gates-result.{txt,json}`):

| injected defect | gate | gates ON | gates OFF |
|---|---|---|---|
| inverted correlator (real D-2 AUC inversion) | `instrument_check` | **BLOCKED** | slips through |
| underpowered design (CI cannot conclude) | `design_check` | **BLOCKED** | slips through |
| tampered pre-registration (silent post-seal edit) | `verify_seals` | **BLOCKED** | slips through |

With gates **on**: 3/3 caught before data collection, 0 false findings emitted, 0 human re-verification events, and
0 legitimate artifacts falsely blocked (control). With gates **off**: 0/3 caught, 3 false findings emitted, 3 human
re-checks required. The lever is trustworthy results per hour, not raw outputs per hour.

---

## 4. Discussion

**Headline: verification caught a false finding before it shipped.** A lab that only *generates* would have published
"SOR defeats Tor" (§3.3). Ours did not: three independent verifiers plus an adversarial re-analysis caught the
artifact and flipped the result (§3.4). This is a concrete, in-loop instance of exactly the verification gap Ding et
al. (arXiv:2608.05179) report is universal — no surveyed system demonstrated externally validated in-loop verification;
here the verify stage is a first-class, blocking, Omnigent-orchestrated agent, and it earned its keep by retracting the
lab's own most attractive claim. This is "verification, not generation": the 10× lever is not discovering faster, it is
not shipping wrong (reinforced by §3.5 — zero false findings reach output with gates on, at zero cost to legitimate
throughput). It also directly answers Mo (2026, arXiv:2607.26064): observable-by-default (sealed artifacts +
transcripts), scalable verification (executable gates + adversarial re-scoring), and clear attribution (agent
authorship declared, as in this draft's banner).

**Limitations (uncertainty preserved).**
- **D-real-1 (unpaired).** The sealed design specifies pairing by run; the real arms were captured sequentially, so
  the analysis used the conservative unpaired bootstrap. The clean paired n=30 battery has not run.
- **D-real-2 (latency artifact).** Tunneled-arm connect latency is a local-forward artifact; SOR latency is not a
  valid frontier coordinate until first-byte-RTT timing is implemented.
- **The lag-searching correlator is not yet gated.** `correlate_lag`/`lagscore.py` has no orientation anchors and no
  equivalence entry. The retraction is solid (SOR's 0.00 → 0.275 jump proves alignment-dependence), but the
  *corrected ranking* (Tor most resistant) is **provisional** until the lag correlator is registered and
  `instrument_check` passes on it. The Omnigent verify agent itself insisted on holding the fix to the lab's own
  rigor standard (`omnigent-verify-run.txt`).
- **Small n (<30 per arm) and large-effect, low-n lag re-score.** Confirmatory-at-margin claims require the frozen
  procedure with confounds controlled.
- **External validity.** Early arms used grounded simulation; the real campaign is own-fleet, emulated/controlled
  topology, not the open Internet at scale. The anonymity proxy is a lower bound under one passive both-ends
  adversary, not the formal δ-anonymity of the trilemma (Das et al. 2018).

**What survived verification.** The rigor machinery is sound (verifier B: seals intact, gates gate, no HARKing); the
frozen correlator code is correct (verifier C) — the flaw was a *missing capability* (lag search) in the attack model
plus the D-real-2 timing-capture bug, not a coding error. The base-rate correction (§3.1) holds on real data. The
honest frontier under a competent adversary is directional: WireGuard most linkable → SOR intermediate → Tor most
resistant (provisional).

---

## 5. Conclusion and next experiment

We ran a sealed, self-correcting AI lab end-to-end on an anonymity-linkability question and, in doing so, produced a
result, discovered it was a measurement artifact, and retracted it — inside the loop, before publication. The domain
takeaways are modest and provisional (honest base rates cut apparent linkability ~10–14×; Tor provisionally most
resistant under a lag-aligning adversary). The methods takeaway is the point: executable gates plus adversarial
verification convert "outputs per hour" into "trustworthy results per hour," and in this study that machinery caught a
false headline that naive generation would have shipped.

**Next sealed iteration** (the fix, held to the lab's own standard):
1. Register the lag-searching correlator (`correlate_lag`) as a gated instrument — add orientation anchors and an
   equivalence entry; re-run `instrument_check`. This upgrades the corrected ranking from provisional to gated.
2. Fix latency instrumentation to first-byte RTT (closes D-real-2), restoring SOR as a valid frontier coordinate.
3. Run the frozen **paired** n=30 confirmatory battery (closes D-real-1) with bootstrap CIs, re-pre-registering
   RQ-RESIST against the stronger adversary.
4. Validate toward the pre-registered ultimate step (`prereg` §14): the live Tor network and real fleet
   phones over real cellular/Wi-Fi; add I2P as a fourth arm.

---

## References

1. Ding, Nannapaneni, Liu, Zhang (2026). *Autonomous Research Agents: A Survey of AI Scientists and the Verification Gap.* arXiv:2608.05179.
2. Das, Meiser, Mohammadi, Kate (2018). *Anonymity Trilemma: Strong Anonymity, Low Bandwidth Overhead, Low Latency — Choose Two.* IEEE Symposium on Security and Privacy (S&P).
3. *From AI for Science to Agentic Science: A Survey on Autonomous Scientific Discovery.* arXiv:2508.14111 (2026).
4. *MLReplicate: Benchmarking Autonomous Research Systems for ML Reproducibility.* arXiv:2605.16616 (2026).
5. Sinhahajari, Majumder, Poria (2026). *On the Limits of LLM-as-Judge for Scientific Novelty Assessment.* arXiv:2606.12071.
6. Belinda Mo (2026). *The Age of AI Agents Demands A New Scientific Paradigm To Sustain Trustworthy Science.* arXiv:2607.26064.
7. Kassianik, Nelson, Singer (2026). *Beyond Success Rate: Cost-Aware Evaluation of Offensive and Defensive Security Agents.* arXiv:2607.15263.
8. Spanos, Kantzavelou (2026). *Evaluating ML-based IDS: The Illusion of Model Efficacy.* arXiv:2609.02469.
9. *Real-world Website-Fingerprinting Evaluation.* arXiv:2603.07412 (2026); Cherubin et al., USENIX Security 2022; Juarez et al. 2014.

### Study artifacts (all paths relative to `output/anon-baserate/`)

`prereg-anon-baserate.md` (+ `.sha256`); `addendum-01-substrate-and-adversary.md`;
`addendum-02-confirmatory-dv.md`; `addendum-03-final-dv-spec.md`; `design_check-PASS.txt`;
`design_check-refit.txt`; `instrument_check-OE-PASS.txt`; `finding-01.md`; `finding-02-acceleration.md`;
`finding-04-real-frontier.md`; `finding-06-real-confirmatory.md` (CORRECTION banner); `finding-07-artifact-caught.md`;
`deviations-real.md`; `methods-note-devices.md`; `ab-gates-result.{txt,json}`; `lagscore-result.txt`;
`lagscore-full.json`; `VERIFICATION-REPORT.md`; `VERIFICATION-GATES.md`; `VERIFICATION-CORRELATOR.md`;
`omnigent-verify-run.txt`; `omnigent-deny-demo.txt`; `../../docs/OMNIGENT-ROLE.md`;
`../../research/field-challenges.md`; `../../research/cyber-eval-gaps.md`.
