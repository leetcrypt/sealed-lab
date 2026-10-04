# Team video script — roster still blocked

`Team.tsx` reads `submission.json` → `team[]`. Current value:

```json
{"name": "[NAME]", "role": "[ROLE]", "built": "[WHAT YOU BUILT]"}
```

No human names, roles, or "what you built" exist anywhere checked in `CLAUDE.md`, `CONTEXT.md`, or `agents/`. **Do not invent a cast.** The lower-third plate in Team.tsx already labels this `SLOT 01 · AWAITING ROSTER`. Footage slot `team-take-01.mp4` is not on disk. Only `demo/footage/01-rigor-gates.mp4` exists.

## What you can say instead (Team B)

The only team the repo can defend is the agent graph in `agents/sealed-lab-team/config.yaml`:

| on-screen name | grounded role |
|---|---|
| Director | `sealed-lab-team` prompt. Delegates; does not run the experiment. Caught plan/execution drift (finding-05). |
| Planner | sub-agent. Picks T1 or T2 from prereg §8. Recorded pick: T2 depth. |
| Runner | sub-agent. Runs exactly `python3 experiment/run.py` or reports a policy DENY. |

`submission.json` `agents` also lists Literature, Hypothesis, Analysis, Reviewer, Safety. Those names are **not** in the team YAML. Leave them off graphics.

Human approval is a brief constraint (pre-registration sealed by a person). There is no name attached.

---

## ACCURATE team/about script (evidence-based, 2026-10-04) — teleprompter: demo/team-teleprompter.html

Solo founder bio for the team/about video. Built from a laptop evidence audit; only verifiable
claims included. Repos published public this week: github.com/leetcrypt/{flash-bash,super-man,incredigo}.

> "I'm Andre, founder of OptinAmpOut — a solo team. I started in web development and marketing-system
> automation and design, for clients including the San Diego performance artist Joe Dreamz. From there
> I moved into agentic-AI R&D: scientific research on agent loop-engineering (the Sealed Lab you just
> saw), agentic red-team / bug-bounty automation, graphic-design and video-editing tooling, and open
> source — flash-bash, super-man, incredigo (all public on GitHub), and hack-house, an e2e-encrypted
> terminal with a p2p connection that forces pair-programming while keeping AI usage under Unix-like
> controls, published in the first edition of Church of Malware. I also run a pre-registered experiment
> on tmux multi-agent supervision loops that cut idle time ~10x, and this submission puts agent-to-agent
> tmux coordination to work. One team, a lot of surface area — with a bias toward building verifiable things."

## CLAIM AUDIT (what was dropped/softened and why — founder should review)
- **DROPPED — "we designed the algorithmic-art Anthropic launched as a public skill."** Chronologically
  impossible: Anthropic launched the `algorithmic-art` skill 2025-10-16; our archive holds a CLONE of
  Anthropic's skill (mtime 2025-11-15) and our own `geo-design` (a *different*, Python library) first
  committed 2026-06-05 — ~8 months later. No comparison screenshots exist. A judge could disprove this; left out.
- **SOFTENED — ltmux-gui "multi-machine tmux C2 with remote view / agent oversight."** It's an early
  React web UI that browses tmux sessions on MOCK data — no backend, no multi-machine, no agent coordination
  (earliest commit 2026-02-05). Left out of the video rather than overstate; mention only if a working build exists.
- **SOFTENED/DROPPED — "early researchers in tmux agent-to-agent, which many have now adopted" + "groundwork
  for TEAMS."** Real: a pre-registered fleet-reactor supervision-loop experiment (2026, ~10x idle cut) — kept.
  But our OWN prior-art survey (fleet-reactor/PRIOR-ART.md) lists hcom/agent-room/awslabs CAO as prior work and
  says "we're not inventing"; and there's no evidence linking us to any Anthropic "Teams" feature. Dropped those two.
- **KEPT (verified):** super-man, flash-bash, incredigo, hack-house, Joe Dreamz webdev+marketing, the sci-method/Sealed Lab research.
