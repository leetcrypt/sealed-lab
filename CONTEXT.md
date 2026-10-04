# hackathon — Routing (ICM Layer 1)

Map intent to a file, open it, follow it.

## Status (2026-10-03, evening)

- ✅ Env set up: omnigent 0.16.0 (Claude subscription credential saved), prereqs verified.
- ✅ Research saved: `field-challenges.md`, `cyber-eval-gaps.md`, `sci-method-state.md`,
  `omnigent-notes.md`, `alt-murena-vs-android.md`.
- ✅ **Framing LOCKED: M1 "thermodynamics of privacy"** — map VPN+Tor+SOR against the
  anonymity-trilemma bound; test if AI linkage bends the frontier. See `research/moonshot-framing.md`.
- ✅ **Arms LOCKED: VPN (WireGuard) + Tor + SOR.** I2P + real-network validation = next step.
- ✅ Assets verified: laptop has Docker, Tor, WireGuard+OpenVPN, the sealed correlator,
  numpy; tril + fp6 reachable.
- ✅ **Omnigent spike (core risk) RETIRED at zero subscription cost:** policy API read
  from source; `config/policies/require_gate.py` proven offline (5/5) — a DENY at the
  fail-closed tool-call phase blocks the loop. See `docs/SPIKE-FINDINGS.md`.
- ✅ **Visual fixed** (spacing/overlap) — `demo/pipeline-visual.html` (1280×800).
- ✅ Gates vendored → `method/` (source commit aa33f13; stdlib, run on py3.14).
- ✅ Run brief written → `output/run-brief-anon-baserate.md` (F1/F2/F3/F4 baked in).
- ✅ **design_check PASS (10/10)** — confirmatory RQ-SHIFT design is sound pre-data.
  Model+ledger: `config/designs/`; evidence: `output/anon-baserate/design_check-PASS.txt`.
  (Caveat printed by the tool: sd_run is an assumption; re-run after it is measured at stage 05.)
- ✅ **Prereg SEALED + verify_seals green** — `output/anon-baserate/prereg-anon-baserate.md`
  (+ `.sha256`). Design is FROZEN; changes go in a separate sealed addendum only.
- ✅ **Addendum-01 sealed** (hybrid substrate; classical-only; RQ-BASERATE promoted to
  confirmatory, RQ-SHIFT→exploratory). verify_seals green on both.
- ✅ **Instrument gate O+E PASS** — self-contained classical correlator
  (`config/instruments/correlator.py`) validated; evidence `output/anon-baserate/
  instrument_check-OE-PASS.txt`. P (provenance) gate pending a git commit.
- ✅ Committed (e8969ed); instrument_check O+E+P green.
- ✅ Addenda 01/02/03 sealed (DV finalized = paired TPR@f gap Tor−SOR; verify_seals: 4 OK).
- ✅ **FIRST COMPLETE LOOP → result (offline).** VERDICT H0 (reportable null): SOR not
  meaningfully more resistant than Tor; balanced eval overstates linkability ~10× at honest
  base rate; VPN control PASS. See `output/anon-baserate/finding-01.md` + `result.json`.
  The null REOPENS the loop (next: re-fit padding from real capture / add timing-defense arm).
- ✅ **LIVE OMNIGENT RUN SUCCEEDED** — `sealed-lab` agent (claude-sdk, subscription) ran the
  full loop via shell with gate-policies guarding the experiment command. Transcript:
  `output/anon-baserate/omnigent-live-run.txt`. Config: `agents/sealed-lab/`, tools+policy
  in `lab/`. (Function-tool MCP bridge didn't load → pivoted to robust shell-guard policy.)
- ✅ Agent acted as adversarial reviewer, caught 3 real gaps; 2 fixed (verify_seals abs
  path; ledger RQ renamed RQ-SHIFT→RQ-RESIST). Refused to vouch for ungated/unsealed output.
- ✅ **LIVE DENY DEMO** — deny-demo agent tried to run the experiment; the rigor policy
  BLOCKED it (injected inverted correlator = real D-2 defect). Agent refused to bypass,
  diagnosed the inversion, said fix goes in a new sealed iteration. `omnigent-deny-demo.txt`.
- ✅ **ACCELERATION A/B (20% criterion)** — 3 real-history defects: gates ON caught 3/3
  before data, 0 false findings; gates OFF emitted 3; 0 legit work falsely blocked.
  `finding-02-acceleration.md` + `ab-gates-result.{txt,json}`.
- ✅ **REAL 3-ARM FRONTIER (pilot)** — WG(1hop) AUC 0.92/7.8ms · Tor(real 3hop onion) AUC
  0.82/786ms · SOR(2hop nested-ssh) AUC 0.51. Provisional RQ-RESIST H1 (SOR>Tor), LABELED
  EXPLORATORY. **[SUPERSEDED by finding-07]** — the apparent SOR resistance (and the "~1 timing
  bin collapse" mechanism once cited for it) was later shown to be a lag-alignment MEASUREMENT
  ARTIFACT; under a lag-searching adversary the ranking flips (Tor most resistant).
  Run records in output/anon-baserate/real-data/.
  See finding-04-real-frontier.md. User-run tor+onion (no root); nested-ssh via phone relay.
- 🎥 Video delegated to general:video (Remotion); working in parallel.
- ⏳ Next: multi-agent Omnigent loop (brief: "collaboration between specialist agents") on the
  REAL data; then re-fit sd_run + controlled-relay confirmatory battery.
- 🎥 Capture footage at each milestone — see `demo/VIDEO-CAPTURE-PLAN.md`.


- ✅ **VERIFICATION CAUGHT A FALSE FINDING (headline).** 3 independent verifier agents +
  a lag-search re-analysis showed the real "SOR>Tor" result was a MEASUREMENT ARTIFACT (relay
  timing offset + lag-blind correlator). Lag-search flips it: SOR TPR 0.00→0.27 (linkable),
  Tor most resistant (0.03). RETRACTED. See `output/anon-baserate/finding-07-artifact-caught.md`
  (+ VERIFICATION-*.md, lagscore-result.txt). findings-01/04/06 SUPERSEDED by 07.
- ✅ Verifier verdicts: numbers/scorer honest (A), rigor chain intact/no-HARKing (B),
  correlator correct but mechanism false + alignment confound (C).
- ✅ Scripts (teleprompter/vo) reframed to "the lab killed a false finding before shipping";
  video teammate alerted to re-cut. Security: tailnet IP scrubbed (history export pending push).

## Where things live

| Need | Go to |
|---|---|
| The challenge rules, scoring, submission list | `inputs/challenge-brief.pdf` (local only) · summary in `CLAUDE.md` |
| **What we're building and the 24h plan** | `docs/BUILD-PROPOSAL.md` |
| **Plan A experiment map (chosen)** | `docs/PLAN-A.md` |
| **Worklist: what to edit/create** | `docs/ENHANCEMENTS.md` |
| Cyber eval gaps + citations (video) | `research/cyber-eval-gaps.md` |
| Parked alt: Murena vs Android study | `research/alt-murena-vs-android.md` |
| The three field problems + citations (video material) | `research/field-challenges.md` |
| What sci-method has and what's missing | `research/sci-method-state.md` |
| Omnigent install, auth, YAML/policy shapes | `research/omnigent-notes.md` |
| Agent specifications (YAML) | `agents/` *(empty: built in H4–10)* |
| Policies and gate handlers, lab config | `config/` *(empty)* |
| Run record, sealed preregs, results | `output/` *(empty)* |
| Demo script, storyboard, video assets | `demo/` *(empty)* |

## Data sources (reachability checked 2026-10-03)

| Source | Key? | Status |
|---|---|---|
| OpenAlex, Europe PMC, PubChem, OpenML, arXiv | no | reachable |
| NIST JARVIS-DFT (figshare) | no | reachable |
| Materials Project | **yes** (free) | 401 without key |

## Related elsewhere

- `laptop:~/coding/sci-method`: the method we vendor (stages, `tools/`, `_config/`).
- `~/coding/ai-agents/trillsec-memory/skills/kg-build/`: knowledge-graph agent backend.
