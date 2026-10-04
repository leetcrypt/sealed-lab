# Pre-Compute Audit — Logical Flaws, Safeguards, Peer-Review Readiness

> "Measure twice, cut once." Run before any Omnigent compute. 2026-10-03.
> Verdict per item: KEEP / FIX / CUT. Budget: ~30% subscription left — flaws that
> waste compute are flagged $$.

## A. Logical / methodological flaws found

### F1 — Apples-to-oranges: measured linkability is NOT the theorem's anonymity metric  [FIX — critical]
The anonymity trilemma (Das et al. 2018) bounds a **formal δ-anonymity** against a global
adversary under specific assumptions (synchronized rounds, a noise/dummy model, a count of
compromised nodes). Our observable is **empirical end-to-end correlation AUC** on captured
flows. These are not the same quantity. Claiming we "validate the theorem" would be false
and a reviewer would reject it immediately.
- **Safeguard:** use the trilemma as the **conceptual frame**, not a claim under test.
  Pre-register three *concrete, measurable* observables per arm — (i) linkage resistance
  = 1 − correlator performance, (ii) latency overhead, (iii) bandwidth overhead — and plot
  the empirical trade-off surface. State explicitly, in the prereg and the paper, that the
  measured anonymity proxy is a lower bound on formal anonymity and does not test the
  theorem's constants. This is honest, novel, and peer-reviewable.

### F2 — "AI bends the frontier" needs TWO adversaries, or the claim is unsupported  [FIX]
To say anything about *AI's* effect we must compare a **classical correlation attack**
against an **ML/learned attack** on the same flows. With a single correlator we can only
report *a* frontier position, not a shift. The SOR tree already has both: a statistical
correlator and a deep-fingerprinting CNN.
- **Safeguard + bonus:** make "classical vs learned adversary" the **two candidate tests
  the planner chooses between** (a brief requirement we needed anyway). If budget is tight,
  scope the headline to "frontier position under the strongest available adversary" and
  demote "is AI moving it" to a pre-registered secondary / next-experiment. Do not assert
  the shift without the contrast.

### F3 — Honest base rate does NOT require 1000:1 physical capture  [KEEP — saves $$]
Precision at base rate b is analytic: precision = b·TPR / (b·TPR + (1−b)·FPR). We measure
TPR and FPR on balanced captures and **project** precision at the pre-registered b.
- **Safeguard:** pre-register b and the projection, and its assumption (the balanced FPR
  estimate transfers to the rare-positive regime). Report a CI on the projection. This is a
  real compute saving — no need to generate enormous negative sets.

### F4 — VPN is a positive control, not a competitor  [FIX — framing]
A single-hop VPN passes timing straight through; under a both-ends adversary its linkage is
near-trivial (~1.0). That is exactly why it belongs — as the **calibration anchor / positive
control** proving the correlator fires when linkage truly exists. Presenting VPN as
"competing on anonymity" would misrepresent its threat model (it trusts one provider;
Tor/SOR distribute trust).
- **Safeguard:** label VPN explicitly as the positive control in prereg, figure, and script.

### F5 — Agent LLM calls, not capture, are the subscription cost  [FIX — budget $$]
Packet capture + correlation run on the **laptop/local GPU — free of subscription**. The
subscription burn is **Omnigent agent reasoning**. A loop that polls the overnight capture
with an LLM call each tick would drain the 30%.
- **Safeguard:** (1) runner invokes capture **once** as a tool, then monitors via a cheap
  shell poll with **no LLM in the loop**; (2) route low-stakes agents (literature triage,
  record-keeping) to **local Ollama** (`<trillsec-tailnet-ip>:11434`), reserve Claude for
  planner + analysis + review; (3) enforce an Omnigent `cost_budget` policy with a hard cap
  and an ask-threshold; (4) dry-run the whole loop at N=2 before the real run.

### F6 — Instrument anchors must cover the new VPN arm  [FIX]
`instrument_check` validates the correlator against ground-truth anchors. Adding the VPN arm
and the base-rate metric without extending the anchors would leave an unguarded path — the
exact defect class this gate exists to catch.
- **Safeguard:** register the VPN arm and the base-rate projection in
  `tools/instruments/<slug>.json`; add a known-linked and known-unlinked VPN fixture.

### F7 — Scope creep: a half-finished second loop iteration  [CUT risk]
The demo must show **one complete loop** plus the *start* of the decision it triggers — not
two half-done loops.
- **Safeguard:** MVP = one sealed loop, 3 arms (or 2 under F5 pressure), gates on, + the
  gates-off A/B. The "reopen" is shown as the *next decision stated*, not a second full run.

### F8 — External validity: emulation ≠ real networks  [KEEP — disclose]
netem topology is not the live Internet. Handled honestly by making real-network /
real-hardware the stated "ultimate next step" (brief explicitly allows deferring it).

## B. Peer-review safeguards (leverage + enhance sci-method)

Already provided by sci-method (reuse as-is):
- Pre-registration frozen + SHA-256 sealed before data (`verify_seals.py`).
- `design_check.py` gates: tautology, power, null-reportability, scale, ledger provenance.
- `instrument_check.py` gates: orientation, fast-path equivalence, git provenance.
- Confirmatory vs exploratory labels; deviations log; null-results-are-results.
- Every figure regenerable from committed code; raw pcaps immutable + checksummed.
- Adversarial stage-08 review.

Enhancements this study needs (create):
- **Operationalization-validity section** (answers F1): the measured proxy vs the formal
  metric, stated as a pre-registered limitation.
- **Threat-model statement** (answers F4): adversary = passive both-ends observer; trust
  assumptions per arm; what is and isn't in scope.
- **Base-rate projection note** (answers F3): formula, chosen b, CI, transfer assumption.
- **Adversary-pair protocol** (answers F2): classical vs learned, applied identically.

## C. Go / no-go checklist before Omnigent compute

- [ ] Prereg drafted with F1 operationalization + F4 threat model + F3 base-rate note.
- [ ] `design_check` PASS on the base-rate decision rule.
- [ ] Correlator frozen; `instrument_check` PASS incl. VPN anchors (F6).
- [ ] `cost_budget` policy set; low-stakes agents on local Ollama (F5).
- [ ] Loop dry-run at N=2 green before the real capture.
- [ ] One-loop MVP scope agreed; "reopen" is a stated next decision, not a 2nd run (F7).

**Overall verdict:** plan is sound after F1, F2, F4 are fixed in the prereg framing and F5
safeguards protect the budget. No fatal flaw. Proceed to the visual, then the spike.
