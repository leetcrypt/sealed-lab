# Enhancements — What to Edit / Create for a Clean Submission

> Concrete worklist for Plan A. Grouped by component. "Create" = new file here.
> "Vendor" = pinned copy from laptop with source commit recorded. "Edit" = change
> an existing asset (on a branch, never the frozen artifacts).

## A. Omnigent layer — NEW (the 30% core; biggest build)

| Item | File | Notes |
|---|---|---|
| 7 agent specs | `agents/{literature,insight,planner,runner,analysis,kg,safety}.yaml` | `executor.harness: claude-sdk`; sub-agents = handoffs; tools per `BUILD-PROPOSAL.md` table |
| Gate policies | `config/policies/require_gate.py` | wraps `design_check` / `instrument_check` / `verify_seals`; **denies the loop-advancing tool call until PASS**. The headline innovation |
| Cost + approval | `config/policies/*.yaml` | built-ins `cost_budget`, `ask_on_os_tools`; human approves `seal` and `execute` |
| Claim-grounding | `config/policies/claim_grounding.py` | every emitted finding must cite a DOI/URL or a checksummed artifact (answers field-problem P3). Lightweight, high value |
| Novelty-grounding | `config/policies/novelty_check.py` | embed hypothesis (local `bge-m3`), nearest-neighbour vs retrieved abstracts; flag "novel-sounding but matched" (P2). Optional for MVP |
| Shared research record | `output/<slug>/record.jsonl` | append-only; the brief's "shared research record so every decision can be reconstructed" |

**First hour risk-retire:** confirm the real policy-handler signature in Omnigent 0.16.0
(alpha — the README YAML may differ). Build one deny-policy and watch it block at :6767.

## B. sci-method method layer — VENDOR + small additions

| Item | Action | Notes |
|---|---|---|
| `tools/design_check.py`, `instrument_check.py`, `verify_seals.py` | **Vendor** (pin commit) | stdlib-only; port as-is. Record source commit `aa33f13` in a `VENDORED.md` |
| `_config/rigor-standards.md`, `paper-structure.md`, `citations.md` | **Vendor** | the canonical rules the gates cite |
| Stage `CONTEXT.md` contracts (01–08) | **Vendor** (trim) | the pipeline contract the orchestrator follows |
| Base-rate decision rule | **Create** `config/designs/anon_baserate.py` + `.json` ledger | `design_check` runs it: precision@base-rate as the decision statistic; power/MDE under the overnight budget |
| New run brief | **Create** `output/anon-baserate/run-brief.md` | topic → stage 01 |
| New prereg | **Create** `output/anon-baserate/prereg.md` | fresh SHA-256 seal, human-approved. **Does NOT reuse the frozen `sor-vs-tor` seal** |

## C. Test assets (hack-house `sor-vs-tor` tree) — EDIT on a branch

| Item | Action | Why |
|---|---|---|
| WireGuard VPN arm | **Create** a bring-up + capture adapter | Tor + SOR exist; VPN is the new, cheap positive-control arm |
| Arm-agnostic capture→extract path | **Edit** to parameterize transport | currently SOR/Tor-shaped; add a thin transport adapter |
| Base-rate metric | **Create** on top of sealed `detectors.linkage_auc` | precision at pre-registered base rate via negative subsampling |
| Register new instrument | **Edit** `tools/instruments/<slug>.json` | so `instrument_check` gates the new metric (registering it is itself the control) |
| SSH-driven runner | **Create** wrapper so the runner agent on trillsec drives capture on laptop | laptop has Docker/Tor/wg; trillsec orchestrates |

**Do not touch** the frozen `sor-vs-tor` prereg, its sealed correlator, or its pilot
pcaps. New slug, new branch, new captures.

## D. Demo + submission — CREATE

| Item | File |
|---|---|
| 2-min demo script/storyboard | `demo/script.md` |
| Figures (base-rate curves, A/B bars) | `output/anon-baserate/figures/` (regenerable from committed code) |
| Per-run bibliography | `output/anon-baserate/references.md` |
| Submission checklist (from brief) | track in `docs/BUILD-PROPOSAL.md` |

## E. Overnight execution

- Long pole = capture grid (arms × runs × workload). Run under a **/loop agent** that
  retains every pcap, honors the pre-registered stopping rule, keeps the grid alive, and
  halts on failure. Correlator frozen **before** any real pcap is scored.
- Score in **one pass** in the morning. One capture, no re-run (the SOR discipline).

## Priority order (if the night runs short)

1. Omnigent: 3 agents (literature→planner→runner) + the `require_gate` deny-policy. **(30%)**
2. Seal a real prereg; `design_check` + `instrument_check` + `verify_seals` all green. **(15%)**
3. One capture loop, 2 arms minimum, honest base-rate result. **(25%)**
4. gates-off A/B on injected defects → the multiplier. **(20%)**
5. Claim-grounding policy + safety/approval gate. **(10%)**
6. Stretch: full 3 arms, novelty-grounding, I2P arm.
