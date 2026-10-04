# Plan A — LOCKED FRAMING (2026-10-03)

> **Headline (decided): M1 "thermodynamics of privacy."** The study maps VPN, Tor, and SOR
> against the proven anonymity-trilemma bound (Das et al., IEEE S&P 2018) and tests whether
> AI-era end-to-end linkage pushes the low-latency arms below the strong-anonymity frontier.
> See `research/moonshot-framing.md` for the full framing and track-compliance mapping.
> **Arms (decided): VPN (WireGuard) + Tor + SOR.** I2P and real-network/real-hardware
> validation are the stated "ultimate next step," not tonight.
> The three-arm linkability mechanics below are unchanged; only the *question they answer*
> is upgraded from "which is more secure" to "where does each sit on the fundamental bound."

---

# Plan A — Anonymity-Network Linkability Under an Honest Base Rate

> The study that demonstrates our Omnigent lab for Challenge 03.
> Reads: `inputs/challenge-brief.pdf`, `research/cyber-eval-gaps.md`,
> `research/sci-method-state.md`, `docs/BUILD-PROPOSAL.md`.
> All experiments run on our own fleet only. Defensive measurement study.

## 1. The scientific question (one, measurable)

Against a passive observer who sees traffic at both the entry and exit of a network,
how reliably can an entry flow be linked to its exit flow across three transports —
**WireGuard VPN, Tor, and SOR** — and **how does that linkability change when it is
scored at a realistic (low) base rate instead of a balanced one?**

- **Primary outcome:** precision of end-to-end linkage at a **pre-registered base rate**
  (e.g. 1 true-linked pair per 1000 candidate pairs), per transport.
- **Secondary:** TPR at a fixed FPR (1e-2); latency / goodput per transport.
- **The honest-base-rate framing is the contribution.** The field's own critique is the
  base-rate fallacy: >0.9 balanced accuracy collapses operationally (Juarez 2014;
  Cherubin 2022; arXiv:2603.07412). We measure the number that actually matters.

## 2. Why this is a real discovery loop (brief, page 3)

```
Question → Literature(gap: base-rate fallacy) → Hypothesis(H: ranking at honest base
rate differs from ranking at balanced eval) → Planner picks 1 of 2 tests →
[human seals prereg] → Runner captures (our fleet) → Analysis(sealed correlator,
base-rate metric) → Result → Updated decision
```

The result **changes the next decision** by construction: if a transport that looks
strong at balanced evaluation collapses at an honest base rate, the agent reopens the
ranking and proposes the next arm/base-rate to probe. That is the brief's exact ask.

### The two competing tests the planner must choose between (required)

| Test | What it buys | Cost | Expected learning |
|---|---|---|---|
| **T1 Breadth** | 3 arms, balanced eval, strongest-observer, interactive workload | low / fast | confirms apparatus; weak on the real question |
| **T2 Depth** | honest base-rate sweep on the 2 decisive arms | higher | directly tests H; where the claim lives |

The planner scores both with `design_check` (power, MDE) against the overnight time and
compute budget and picks one. Non-trivial, auditable, pre-registered.

## 3. Arms and apparatus (all assets verified 2026-10-03)

| Arm | Build | Status |
|---|---|---|
| **VPN** | WireGuard single-hop tunnel between two fleet hosts | `wg` present on laptop — **new, cheap to stand up** |
| **Tor** | 3-hop, our own sink only | `/usr/sbin/tor` present; harness exists |
| **SOR** | 3-hop consent-gated nested SSH, isolated engines | harness exists in `hack-house/work-trees/sor-vs-tor/` |
| I2P (stretch) | add as 4th arm | partially set up (`~/.i2pd`); parked as "next experiment" |

- **Raw data = pcaps at ingress and exit.** Immutable, SHA-256 sealed. Capture and
  correlator-build are independent and parallel (the SOR program's proven discipline).
- **Instrument = the sealed correlator** `cmd_chat/sor/analysis/detectors.py::linkage_auc`,
  plus a **new base-rate metric** layered on its scores. Validated by `instrument_check`
  against ground-truth anchors **before** it scores any real pcap.
- **THE NON-NEGOTIABLE:** no one looks at a real pcap while choosing or tuning the
  correlator or the threshold. Tune only on excluded verification circuits, then freeze.

## 4. What we submit — the framework IS the product; the study PROVES it

| Submission item (brief) | What it is for us | Headline? |
|---|---|---|
| Repository | The Omnigent rigor-enforced lab + vendored sci-method method layer | — |
| Agent specs + policies | 7 agents + gate-policies that **block the loop until rigor passes** | **Yes — the 30% core** |
| 2-min demo | One loop: question→handoffs→sealed experiment→honest-base-rate result→next | Yes |
| Cited evidence | `research/*.md` + per-run bibliography | — |
| Experiment code + results | The 3-arm study, sealed prereg, pcaps, analysis | Yes — the proof |
| Measured improvement | gates-on vs gates-off A/B, "verified results per hour" | **Yes — the 20%** |
| Next experiment | honest-base-rate I2P arm, or Murena privacy study (`research/alt-murena-vs-android.md`) | Yes |

**One-line answer to "study or framework":** we submit **the framework as the product**
(a reusable lab that makes autonomous science trustworthy by construction), and **the
linkability study as the single complete loop that demonstrates it**. The moonshot
("10× faster discovery") is carried by the framework's generality; the study is the
evidence that one honest loop actually closes.

## 5. The acceleration number (brief: 20%, "report what you observe")

Run the lab twice under matched conditions on **injected defects drawn from the SOR
program's real history** — an inverted metric (D-2 AUC inversion), a mismatched time
base (the rho-pilot root cause), a tautological hypothesis, an ungrounded claim.

- **Baseline:** agents, gates OFF (a typical AI-scientist loop).
- **Proposed:** gates ON.
- **Metrics:** false findings emitted; defects caught before data collection; claims
  needing human recheck; wall-clock question→*verified* result.
- Report the honest multiplier. The headline is **verified results per hour**.

## 6. Timeline — tonight → tomorrow morning (overnight capture under /loop)

| Window | Deliverable | Exit test |
|---|---|---|
| **H0–1** | Omnigent spike: 2-agent handoff + 1 blocking policy in the UI | a policy denies a call at :6767 |
| **H1–3** | New slug `anon-baserate`: run brief + prereg draft. Vendor method layer. Stand up WireGuard arm. Smoke-test capture on laptop over SSH | one circuit each arm delivers bytes to our sink |
| **H3–5** | base-rate decision rule passes `design_check`. **Human seals prereg.** Freeze correlator; `instrument_check` PASS | seals verify; gate green |
| **H5–7** | 7 agent YAMLs + gate-policies + shared research record. Dry-run loop at tiny N | loop completes on toy data |
| **H7 → overnight** | Launch capture grid under **/loop agent oversight** (retain every pcap, honor stopping rule, keep grid alive). Agents idle-wait on data | pcaps accumulating; heartbeat healthy |
| **morning** | Score retained pcaps (one pass). Analysis (06): base-rate result. gates-off A/B. Figures. `verify_seals` clean | repo seals all OK |
| **+2h** | 2-min demo video + submission package | checklist ticked |

## 7. Scope guardrails (so we finish)

- **MVP = VPN + SOR + Tor, one sealed loop, gates on, + the gates-off A/B.** If capture
  is slow, drop to **2 arms** (VPN as positive control + SOR) and report honestly.
- The lab (framework + policies) is the product. If the science must shrink, shrink the
  science, never the rigor machinery — that is what we are showing.
- I2P and the Murena study are the "next experiment" slide, not tonight's build.
