# Pre-registration — anon-baserate

- **Slug:** `anon-baserate`  · **Status:** FROZEN on seal  · **Date:** 2026-10-03
- **Program:** M1 "thermodynamics of privacy" (Challenge 03 submission)
- **Design evidence:** `design_check` PASS 10/10 — `output/anon-baserate/design_check-PASS.txt`
- **Seed:** 20261003  · **This file is frozen on seal; changes go in a separate sealed addendum.**

## 1. Research questions

- **RQ-SHIFT (confirmatory, primary).** On the *same* captured flows, does a LEARNED
  end-to-end linkage adversary achieve higher linkage precision at the pre-registered
  honest base rate `b` than a CLASSICAL adversary, by at least the margin `delta`?
  - H1: inward frontier shift under AI (CI lower bound on the mean paired gap > 0).
  - H0 (reportable null): shift is negligible (CI upper bound < `delta`).
- **RQ-POS (estimation, secondary — NOT a hypothesis test).** For each arm, the measured
  triple (anonymity proxy, latency overhead, bandwidth overhead), reported with CIs and
  plotted against the trilemma's qualitative constraint. Descriptive; no accept/reject.

## 2. Operationalization & validity (pre-registered limitation)

The **anonymity proxy** = 1 − linkage precision at base rate `b` under one concrete passive
both-ends adversary. It is an empirical **lower bound** on anonymity, NOT the formal
δ-anonymity of the anonymity trilemma (Das, Meiser, Mohammadi, Kate, IEEE S&P 2018), and it
does NOT test that theorem's constants or assumptions. The trilemma is used as the
conceptual frame only. This limitation is restated in the paper.

## 3. Threat model & scope

- **Adversary:** passive observer of traffic entering and leaving the network at both ends;
  no active injection; no endpoint compromise.
- **Scope (enforced by safety policy + human approval):** all traffic is self-generated to
  our OWN sinks on our OWN fleet. No third-party destinations. SOR forwarders run in isolated
  engines on distinct hosts.

## 4. Arms

| Arm | Role | Note |
|---|---|---|
| WireGuard VPN | **positive control** (not a competitor) | single-hop; near-trivial linkage under a both-ends observer; trusts one provider. Calibrates that the adversary fires when linkage truly exists. |
| Tor | comparator | 3-hop, distributed trust |
| SOR | system under study | 3-hop consent-gated nested SSH |

## 5. Adversaries (applied identically to all arms; frozen before any real pcap)

- **A-classical:** the sealed statistical flow correlator `detectors.linkage_auc`
  (hack-house `work-trees/sor-vs-tor`, registered in the instrument gate).
- **A-learned:** the learned/deep-fingerprinting correlator from the same tree.

## 6. Observables / DVs

1. **Linkage precision at base rate `b`** — projected analytically from each run's measured
   TPR and FPR: `precision = b·TPR / (b·TPR + (1−b)·FPR)`. (Pre-registered assumption: the
   balanced-capture FPR estimate transfers to the rare-positive regime.) `b = 0.001`.
2. **Latency overhead** vs a direct baseline.
3. **Bandwidth overhead** vs a direct baseline.

## 7. Design arithmetic (frozen; verified by design_check)

- Unit of resampling: the **run** (not the pair). `n_runs = 30` paired runs per arm.
- `delta = 0.08` (MDE: smallest precision shift treated as a material inward move).
- `sd_run = 0.10` — **ASSUMPTION**, re-fit from the excluded verification runs at stage 05;
  **design returns to stage 03 if realized `sd_run > 0.13`.**
- Simulated: P(H1|null)=0.031 ≤0.20; P(H1|δ)=0.993 ≥0.80; P(reportable null|0)=0.971 ≥0.80;
  CI half-width 0.034 vs claimed 0.04.

## 8. The two candidate tests (planner selects ONE by expected learning vs cost)

- **T1 breadth:** all 3 arms, A-classical only, balanced eval, interactive workload. Cheap;
  establishes RQ-POS positions. Does not support RQ-SHIFT.
- **T2 depth:** the 2 decisive arms (SOR, Tor) under BOTH adversaries at base rate `b`;
  the only test that can decide RQ-SHIFT. Costlier.
- **Selection rule:** maximize expected learning per unit compute within the frozen budget;
  if T2 is infeasible, RQ-SHIFT is reported EXPLORATORY and the headline is the RQ-POS map.

## 9. Analysis plan (pre-registered)

- Mean paired gap with a **cluster (run-level) percentile bootstrap 95% CI**; decision rule
  exactly as in §1 (H1 / H0 / inconclusive). Point estimates + CIs for all DVs.
- **Holm** correction across the confirmatory family. Confirmatory vs EXPLORATORY labeled
  throughout. Null results reported as results; no HARKing; deviations logged, never silent.

## 10. Stopping rule

Capture the frozen `n_runs` per arm per selected test, then stop. No data-dependent
extension. Interim looks do not alter `n_runs`.

## 11. Instrument-validation gate (boolean; must PASS before scoring any real pcap)

Per `instrument_check`: every registered correlator hits its ground-truth anchors
(orientation), every fast path equals its sealed reference (equivalence), and every
instrument file is git-tracked (provenance) — including a **VPN known-linked / known-unlinked
anchor**. Correlator frozen before it touches a pilot pcap (no forking paths).

## 12. Reproducibility

Seeds fixed; environment pinned; raw captures immutable + SHA-256; every figure regenerable
from committed code.

## 13. Pre-registered limitations

Emulated (netem) topology is not the live Internet (external validity). The anonymity proxy
is a lower bound (see §2). VPN is a control, not a competitor (§4).

## 14. Ultimate next step (stated; not done in the hackathon window)

Validate on real deployed networks and real hardware: the live Tor network and the fleet
phones (`tril`, `fp6`) over real cellular/Wi-Fi; add I2P as a 4th arm.
SILENT POST-SEAL EDIT (HARKing a new hypothesis in)
