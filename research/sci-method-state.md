# sci-method — Where We Are, and the Gap to the Hackathon

> Source of truth: `laptop:~/coding/sci-method` (canonical), HEAD `aa33f13`
> as of 2026-10-03. This is an assessment, not a copy. Verify against
> `git log` + `tools/verify_seals.py` before acting on any line below.

## What sci-method already is

An **ICM scientific-method pipeline**: folder structure is the control flow,
markdown is the program, one orchestrating agent drives it. Eight one-way stages:

```
01-literature → 02-hypothesis → 03-design → 04-build
   → 05-execute → 06-analyze → 07-paper → 08-review
```

Immutable integrity rules (from its `CLAUDE.md`): pre-registration is law (no
HARKing), null results are results, every claim traceable to a citation or
artifact, confirmatory ≠ exploratory, reproducibility by construction.

### Its real differentiator: rigor that *executes*, not rigor that is *asserted*

The pipeline went past ceremony after catching its own LLM-drafted failures.
Doctrine (`shared/honesty-assessment-and-solutions.md`, 2026-07-24):

> "The vocabulary of rigor is far cheaper to produce than rigor, and it is
> *specifically* cheap for a language model to produce. … **Do not audit prose.
> Execute arithmetic.**"

Three stdlib-only executable gates enforce it:

| Tool | Stage | What it executes | Gates |
|---|---|---|---|
| `tools/design_check.py` | 03 | Runs the pre-registered decision rule against synthetic worlds (Monte Carlo) | **L** ledger provenance · **T** tautology (P(H1 \| null) ≤ max) · **P** power · **N** null-reportability · **S** scale |
| `tools/instrument_check.py` | 04 | Runs each measurement instrument against ground-truth anchors | **O** orientation · **E** fast-path equivalence · **P** git provenance |
| `tools/verify_seals.py` | 05/06/08 | Re-hashes every SHA-256 seal | MISMATCH · MISSING · UNSEALED |

### Documented catches (usable as demo case studies)

- **Underpowered design hidden by fluent prose.** An LLM-drafted pre-reg claimed
  a CI half-width of 0.05; the real figure was 0.07–0.12 (missing design effect,
  missing √2). The primary test could *never* conclude. Caught by executing
  the arithmetic, not by reading it.
- **Hypothesis true by construction.** A Pareto hypothesis ("≥2 arms mutually
  non-dominated") was guaranteed before any data — now caught by gate **T**.
- **Silent instrument inversion.** An AUC scorer counted the wrong tail and
  returned `1 − AUC`; a working model read as anti-informative and the paper
  stalled five days. "A broken instrument degrades into an authentic-looking
  number, it does not crash." Now caught by gate **O**.

### Live programs consuming it

| Program | Slugs | State |
|---|---|---|
| SOR anonymity routing | `sor-consent`, `sor-vs-tor`, `sor-quic-wf` | Preregs FROZEN + sealed; `sor-quic-wf` in execute (Phase C pilot FAIL recorded, deviations D-1..D-4) |
| Agent supervision loops | `loop-efficacy`, `reactor-a1v6`, `loop-settle`, `loop-interval-sweep` | One moved out with paper; others brief/unsealed |
| Torah ELS | `torah-els` | Prereg drafted, unsealed |

Also: `skills/sci-scout/` (stage-0 front door that makes any codebase
researchable) and `PAPER-LOOP-PLAYBOOK.md`.

## How the three field problems map onto what already exists

| Field problem (see `field-challenges.md`) | What sci-method already does | Strength |
|---|---|---|
| **P1 Verification gap.** Only 38% of AI-scientist systems release seeds/traces; 0% do externally validated in-loop verification | Sealed preregs, checksummed immutable raw data, pinned seeds/envs, `verify_seals.py`, `instrument_check.py` | **Strong.** This is in-loop verification. |
| **P2 Novelty mirage.** LLM judges overrate their own ideas; HARKing manufactures novelty | Stage-01 literature gap analysis; prereg freeze; gate **T** rejects tautologies; gate **P** rejects studies that can't see the effect | **Strong on falsifiability.** Weaker on *novelty scoring*: no literature-grounded novelty check yet. |
| **P3 Grounding & accountability** | Every claim → citation or artifact; EXPLORATORY labeling; deviations log; 08 adversarial review; git attribution | **Strong on discipline.** Enforced by contract and review, not yet by a machine gate on claims. |

**Bottom line.** sci-method already holds the hard, rare part: a working answer
to the verification gap. Almost no AI-scientist system has executable rigor gates.

## The gap to the hackathon

The challenge is scored on things sci-method was never built for.

| # | Gap | Why it matters | Score weight hit |
|---|---|---|---|
| G1 | **Not Omnigent-orchestrated.** One orchestrator plus humans driving tmux panes | Omnigent orchestration is mandatory | 30% |
| G2 | **Rigor gates are run by hand,** not wired in as agent tools or blocking policies | The core story: rigor as *enforced policy*, not prose | 30% + 15% |
| G3 | **Linear and paper-shaped.** 01→08 over weeks, human checkpoint per stage | Need one closed loop in hours where the result changes the next decision | 20% |
| G4 | **No planner choosing between ≥2 tests** by expected learning, feasibility and cost under a budget | Explicitly required by the brief | 20% + 30% |
| G5 | **No measured acceleration.** No baseline to compare against | "Report the improvement you actually observe" | 20% |
| G6 | **No machine claim-grounding gate.** Every claim must carry a citation, but nothing checks it | P3 is enforced by review only | 15% |
| G7 | **No literature-grounded novelty check** | P2 answer is half-built | 25% |
| G8 | **Domain legibility.** The live programs are anonymity networking and agent tooling | Judges score breakthrough potential | 25% |

### A design constraint we must keep

ICM forbids a later stage writing back to an earlier one. The brief wants
"surprising results reopen an earlier assumption." These do not conflict. The
adaptive loop runs as a **new sealed iteration** (new addendum and seal), never a
backward edit. Every loop turn stays pre-registered and auditable. That is a
feature to show judges, not a workaround.

### Logistics

- sci-method is canonical on `laptop`. We build on `trillsec` (GPU).
  **Vendor a pinned snapshot of the method layer** (`tools/`, `_config/`, stage
  `CONTEXT.md` contracts) into the hackathon repo, with the source commit recorded.
  Don't fork silently. The submission must be a self-contained repo.
- The gates are stdlib-only Python, so they port to the hackathon venv with zero friction.
