# VIDEO BRIEF — 2-minute demo for Hackathon Challenge 03 (delegated to video-toolkit)

> **⚠ SUPERSEDED HEADLINE (2026-10-04) — read with RENDER-NOTE.md § "CORRECTION v6".** This brief
> predates finding-07. The HEADLINE is no longer the H0 sim null; it is **"verification caught a
> false finding before it shipped."** The real campaign *looked* like "SOR more resistant than
> Tor," but the lab's own verify stage proved that was a lag-alignment MEASUREMENT ARTIFACT and
> RETRACTED it; under a competent adversary SOR is linkable and Tor is (provisionally) most
> resistant. Beats 3-4 and 6 below are superseded by the retraction arc in `demo/vo-script.md`,
> `demo/live-demo-script.md`, and RENDER-NOTE v6 — the sim-null framing is NOT the shipped story.

**Deliverable:** a ~2:00 demo video for our submission to the 7th Global AI Hackathon,
Challenge 03 "Agentic Scientific Discovery" (Hack-Nation × Databricks). Mostly PROGRAMMATIC
motion graphics (Remotion/Opus 5.5 pipeline); live footage is accent, not the backbone.

**Project name:** Sealed Lab. **One-line thesis:** in AI-driven science the bottleneck is
VERIFICATION, not generation — so we built an Omnigent agentic lab where rigor is ENFORCED by
policy (an agent cannot advance the discovery loop until executable rigor gates pass).

## The 2-minute story (beats → timing)

1. **Hook (0:00–0:15).** AlphaFold mapped protein-structure space and won a Nobel. The next
   bottleneck: AI science is fast to produce, slow to trust. Only 38% of AI-scientist systems
   release reproducibility artifacts; 0% do in-loop verification (cite arXiv:2608.05179).
2. **The idea (0:15–0:35).** Sealed Lab = Omnigent orchestrating specialist agents through one
   discovery loop (Question→Evidence→Hypothesis→Experiment→Result→Decision), where sci-method
   rigor gates run as blocking POLICIES. Use the animated pipeline (see artifacts).
3. **The science (0:35–0:55).** We map real privacy transports (VPN, Tor, SOR) onto the
   anonymity trilemma (Das et al., IEEE S&P 2018) at an HONEST base rate. Show the frontier plot.
4. **The loop runs live (0:55–1:20).** The Omnigent agent runs the gates, then the experiment.
   Result: H0 reportable null — SOR not more resistant than Tor; balanced eval overstates
   linkability ~10× at the honest base rate; VPN positive control confirmed.
5. **Rigor enforced, live (1:20–1:45).** The HERO moment: we inject the real D-2 inverted-scorer
   defect; the policy BLOCKS the experiment; the agent refuses to bypass and diagnoses it.
   Then the acceleration A/B: gates ON caught 3/3 real-history defects, 0 false findings;
   gates OFF emitted 3.
6. **Close (1:45–2:00).** The lever is "verified results per hour, not raw outputs per hour."
   Next: real captures + timing-defense arm. "Our world needs breakthroughs — trustworthy ones."

## Scoring to hit (put these on screen subtly)
Omnigent orchestration 30% · breakthrough 25% · acceleration+learning 20% · rigor 15% ·
creativity+responsibility 10%.

## Artifacts (all in /home/trilltechnician/coding/hackathon)
- **Animated diagram:** `demo/pipeline-visual.html` (self-contained SVG/CSS; screen-record it
  playing one 14s loop, OR re-implement the same design in Remotion for crisp motion).
- **Hero transcripts (live footage source):** `output/anon-baserate/omnigent-deny-demo.txt`
  (the policy DENY + agent refusing to bypass) and `output/anon-baserate/omnigent-live-run.txt`
  (the clean run; agent self-catches 3 gaps). Quote these on screen.
- **Result numbers:** `output/anon-baserate/result.json`, `finding-01.md` (the null + next step),
  `finding-02-acceleration.md` + `ab-gates-result.txt` (the A/B table).
- **Citations for the references card:** `research/field-challenges.md`, `research/cyber-eval-gaps.md`,
  `research/moonshot-framing.md`.
- **Palette:** dark #0d1117; cyan #38bdf8 (loop), purple #a78bfa (agents), green #34d399 (gate
  PASS), red #f87171 (gate DENY). Match `demo/pipeline-visual.html`.

## Live footage
Only the two transcripts above are "live" so far (terminal + web UI at :6767). Treat them as
accent b-roll (typewriter/terminal styling of the DENY quote lands hardest). The rest is
programmatic. If the user provides screen-recording mp4s later, slot them into beats 4–5.

## Output
A rendered ~2:00 mp4 + the Remotion project. Keep it legible, no AI-slop. Save the mp4 path and
tell us where it is. Coordinate back here (hackathon repo) if you need more numbers or assets.
