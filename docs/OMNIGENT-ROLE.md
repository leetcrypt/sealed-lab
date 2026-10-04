# How Omnigent fits Sealed Lab (and produced the headline finding)

**Sealed Lab = methodology; Omnigent = the orchestration + enforcement layer that runs it.**
The methodology (vendored sci-method) is pre-registration + executable gates + adversarial
verification. Omnigent is what turns that from a document into a running multi-agent lab:
specialist agents exchange structured outputs through the discovery loop, and the gates run as
**blocking policies** an agent cannot pass until they're satisfied.

## The discovery loop IS a team of Omnigent agents
| stage | Omnigent agent (live) | gate it must clear |
|---|---|---|
| hypothesis / plan | planner (team run) — picked test T2 citing prereg §8 | design_check |
| run experiment | runner (team run; deny-demo) — gated shell | design_check + instrument_check (policy) |
| **verify** | **sealed-lab-verify (this run)** — re-scores adversarially | instrument_check |
| enforce | policy layer — denied the loop on an injected defect | require_gate (fail-closed) |

## Omnigent produced our HEADLINE result, not just a demo
Our headline is that the lab **caught a false finding before publishing it** (finding-07): a
naive analysis said "SOR more resistant than Tor"; verification found it was a timing-alignment
artifact and the result flipped. That verification is the lab's VERIFY stage — and it runs as an
Omnigent agent (`agents/sealed-lab-verify`) whose tool re-scores every arm with a stronger
(lag-searching) adversary and RETRACTS the claim when linkage jumps. So Omnigent orchestrates
the exact plan → run → **verify → retract** process that generated the finding. The instrument
gate (orientation/provenance on the correlator) runs as the verifier's first step.

## Why this matters for the challenge
"Omnigent orchestration" (30%) is not a wrapper here: the required platform runs the specialist
agents, enforces rigor as policy (demonstrated live by a DENY), and — crucially — orchestrates
the **verification** that is our scientific contribution. Generation alone would have shipped a
false result; Omnigent's verify stage killed it. That is "verification, not generation,"
executed on the platform the challenge mandates.
