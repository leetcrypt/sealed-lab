# Run brief — anon-baserate  (stage-01 input)

> Slug: `anon-baserate`. New program, NEW seal. Does **not** reuse the frozen
> `sor-vs-tor` prereg or its captures. Framing locked: M1 "thermodynamics of privacy."
> Audit fixes F1/F2/F3/F4 (`docs/AUDIT.md`) are baked in below.

## Topic

Where do real, deployed low-latency privacy transports sit relative to the **anonymity
trilemma** (Das, Meiser, Mohammadi, Kate, IEEE S&P 2018) — the proven result that an
anonymous-communication protocol can achieve at most two of {strong anonymity, low
bandwidth overhead, low latency overhead} — and does a **learned** traffic-analysis
adversary move a transport's position relative to a **classical** one?

## Measurable question

For WireGuard VPN, Tor, and SOR, measure the triple:
1. **Anonymity proxy** = 1 − end-to-end flow-linkage performance of a passive both-ends
   observer, reported as **precision at a pre-registered base rate b** (not balanced AUC).
2. **Latency overhead** vs a direct baseline.
3. **Bandwidth overhead** vs a direct baseline.
Plot each transport on the (overhead, anonymity) plane against the trilemma's qualitative
constraint curve.

## Operationalization validity  (F1 — critical, pre-registered limitation)

The measured anonymity proxy is an **empirical lower bound** on anonymity under one
concrete adversary. It is **not** the theorem's formal δ-anonymity and does **not** test
the theorem's constants or assumptions (synchronized rounds, specific noise model, count
of compromised nodes). We use the trilemma as the **conceptual frame**, not a hypothesis
under test. This limitation is stated in the prereg and the paper.

## Adversary pair  (F2 — required for any "AI moves the frontier" claim)

Two adversaries, applied **identically** to all arms, pre-frozen:
- **A-classical:** statistical flow correlation (the sealed `detectors.linkage_auc`).
- **A-learned:** the deep-fingerprinting / learned correlator from the SOR tree.
The two candidate tests the planner chooses between (expected learning vs cost):
- **T1 breadth:** all 3 arms, A-classical, balanced eval, interactive workload. Cheap.
- **T2 depth:** the 2 decisive arms under BOTH adversaries at the honest base rate. Costly,
  but the only test that can support a frontier-shift statement.
If budget forbids T2, the frontier-shift is reported EXPLORATORY / next-experiment; the
headline is then "frontier position under the strongest available adversary."

## Base-rate projection  (F3 — saves compute, pre-registered)

Precision at base rate b is analytic: `precision = b·TPR / (b·TPR + (1−b)·FPR)`. Measure
TPR and FPR on balanced captures; **project** precision at the frozen b with a CI. Assumption
(stated): the balanced FPR estimate transfers to the rare-positive regime. b is frozen in
the prereg.

## Arms  (F4 — VPN is the positive control, not a competitor)

| Arm | Role | Threat-model note |
|---|---|---|
| WireGuard VPN | **positive control** | single-hop; near-trivial linkage under a both-ends observer; trusts one provider. Calibrates that the correlator fires when linkage truly exists. |
| Tor | comparator | 3-hop, distributed trust |
| SOR | system under study | 3-hop consent-gated nested SSH, isolated engines |

## Scope & safety  (own fleet only)

All capture is self-generated traffic to **our own sinks on our own fleet**. No third-party
destinations. A safety policy + human approval gate enforce this (brief's human-approval
requirement).

## Outcome that changes the next decision

If a transport lands far from its predicted trilemma position, OR if A-learned moves it
materially vs A-classical, the lab reopens: is it a measurement artifact (re-check the
instrument gate) or a genuine anomaly worth the next arm / next base rate? That decision
is the loop's "result → updated decision."

## Done = (per `method/_config/paper-structure.md`)

Prereg frozen + SHA-256 sealed (human-approved) with: the two RQs (position; shift),
arms, both adversaries, frozen b, overhead DVs, the design arithmetic passing
`design_check`, the instrument-validation gate on all arms incl. the VPN anchor, the
pre-registered analysis (effect sizes + CIs; base-rate projection; confirmatory vs
exploratory), and the stopping rule. IMRaD draft + adversarial stage-08 review. Every
figure regenerable; raw captures immutable + SHA-256.

## Ultimate next step (stated, not done tonight — brief allows deferring)

Validate on **real deployed networks and real hardware**: the live Tor network and the
fleet phones (`tril`, `fp6`) over real cellular/Wi-Fi, instead of emulation. Add I2P as a
4th arm. This is the "physical/wet-lab equivalent" the challenge says teams need not complete.
