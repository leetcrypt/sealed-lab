# hackathon — Agentic Scientific Discovery Lab (ICM Layer 0)

<!-- Layer 0: identity + immutable rules. Always loaded. Keep lean; detail lives in docs/ + research/. -->

## What this is

Our entry for **Challenge 03: Agentic Scientific Discovery**, part of the 7th Global AI
Hackathon (Hack-Nation × Databricks, with the MIT Clubs of N. California and Germany).
It is a 24-hour build of an AI lab that runs one complete discovery loop:
**Question → Evidence → Hypothesis → Experiment → Result → Updated decision.**

**Thesis.** Verification, not generation, is the bottleneck in AI-driven science. We
port sci-method's *executable* rigor gates into **Omnigent** as blocking policies.
The lab's output is then trustworthy by construction. Full rationale is in
`docs/BUILD-PROPOSAL.md`.

## Hard constraints (from the brief — non-negotiable)

- **Omnigent must orchestrate the live loop.** It must show multiple specialist agents
  exchanging outputs, using tools, and adapting their plan after a result. No
  orchestration that bypasses Omnigent counts.
- **Design ≥2 candidate tests; the planner picks one** by expected learning,
  feasibility and cost, within a budget.
- **Citations for every factual claim.** Label agent-generated hypotheses as such.
  Preserve uncertainty. Document controls and human-approval gates. State the
  validation still needed before real-world use.
- **Report the improvement actually observed.** Never inflate the multiplier.
- Scoring: Omnigent orchestration 30% · breakthrough 25% · acceleration and learning
  20% · rigor 15% · creativity and responsibility 10%.

## Scientific integrity rules (inherited from sci-method — immutable)

- **Pre-registration is law.** Freeze hypothesis, design and analysis plan *before*
  data exists. A surprising result opens a **new sealed iteration**. Never edit a
  frozen file.
- **Do not audit prose. Execute arithmetic.** A design is valid when `design_check`
  passes, not when its paragraph sounds careful.
- **Null results are results.** Confirmatory and exploratory work are always labeled.
- **Every claim is traceable** to a DOI or URL, or to a checksummed artifact here.
- **Reproducibility by construction.** Fix seeds, pin environments, keep raw data
  immutable and checksummed.

## Environment (trillsec)

- `omnigent` 0.16.0 at `~/.local/bin/omnigent`. Web UI at `http://localhost:6767`.
  Setup notes are in `research/omnigent-notes.md`.
- Python via **`uv`** (omnigent is pinned to 3.12). Node 22. GPU is an RTX 2060 SUPER
  with **8 GB** of VRAM, so models must stay small.
- Ollama serves on the tailnet: `http://<trillsec-tailnet-ip>:11434`, **not** localhost.
- The sci-method method layer is canonical on `laptop:~/coding/sci-method`. Vendor a
  pinned snapshot with the source commit recorded. Don't fork silently.
- `ANTHROPIC_API_KEY` is not exported. Use `omnigent setup` or a git-ignored
  `secrets.env`. Never print keys.

## Working rules

- Read `CONTEXT.md` to route. Load only the files the current task needs.
- Git is local to this dir. Use conventional commits. **Don't push without
  confirming** the remote and scope, because pushing publishes the submission.
- `output/` is the run record. Commit it after runs, never seed the repo with it.
- `inputs/*.pdf` is the third-party brief. Keep it local and out of the public repo.
