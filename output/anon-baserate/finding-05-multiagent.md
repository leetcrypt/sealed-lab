# Finding-05 — multi-agent collaboration (the brief's "specialist agents") demonstrated live

> Live Omnigent run of `agents/sealed-lab-team`: a director (claude-sdk) delegating to two
> specialist sub-agents via `sys_session_send` + inbox. Transcript:
> `output/anon-baserate/omnigent-multiagent-run.txt`.

## The handoffs (real, not simulated)

1. **Director → Planner.** The planner read `config/designs/anon-baserate.json` + prereg §8 and
   chose **T2 (depth)** by expected learning: "T2 is the only test that can settle the main
   question; T1 cannot," with conditions (A-learned passes the §11 instrument gate; sd_run re-fit
   ≤ 0.13; else report exploratory). This is the brief's "design ≥2 tests; planner picks one by
   expected learning/cost."
2. **Director → Runner (gated).** The runner ran `python3 experiment/run.py` (the rigor policy
   admitted it), returning the RQ-RESIST null (H0; gap −0.058, CI [−0.104,−0.014]).
3. **Director synthesis — adversarial rigor.** The director CAUGHT a real mismatch: *"the script
   that ran is not the test the planner chose … three arms with one attacker each looks like T1
   (breadth), not T2."* It reported the null, then prescribed a **new sealed iteration** for the
   actual T2 (check §11 on A-learned, re-fit sd_run first).

## Brief requirements this single run satisfies

- **Collaboration between specialist agents** — director + planner + runner, real `sys_session_send`
  handoffs with inbox collection.
- **Planner selects the experiment** by expected learning and cost, citing the frozen design.
- **Agent-generated hypotheses labeled** — "SOR's extra linkability may come from its 0.60
  bandwidth overhead acting as a fingerprint (agent-generated, untested)."
- **Uncertainty preserved** — "one run … the runner's output only, not an independent check."
- **Result changes the next decision** — new sealed iteration for the real T2.

## Known limitation the director surfaced (honest)

`experiment/run.py` runs a FIXED experiment; the planner's T1/T2 selection is not yet wired to
parameterize it. The director catching this is the feature — it's exactly the kind of
plan↔execution drift a human reviewer would flag. Wiring selection → run is a stated next step.
