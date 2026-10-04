# Sealed Lab — live-demo script (2026-10-03 PT)

Grounded in `~/coding/hackathon` as of finding-07. This replaces the short live-a / live-b tabs that were not tied to commands or files.
Teleprompter tab: **Live C**. File URL: `file:///home/trilltechnician/coding/hackathon/demo/teleprompter.html`.
Also symlinked at `~/coding/video-toolkit/hackathon/demo/teleprompter.html` because LibreWolf was opened with the relative path `hackathon/demo/teleprompter.html` from the video-toolkit cwd.

## What the demo is

Omnigent 0.16.0 orchestrates one discovery loop. The showable surface is:

1. Offline gates on `demo/footage/01-rigor-gates.mp4` (18.8s): `design_check.py` PASS 10/10, `verify_seals.py`, `config/policies/test_require_gate.py` DENY.
2. Multi-agent run: `export PYTHONPATH="$PWD"; omnigent run agents/sealed-lab-team --no-session` from `~/coding/hackathon`. Director delegates to `planner` (picks T2 from prereg §8) then `runner` (`python3 experiment/run.py`). Transcript: `output/anon-baserate/omnigent-multiagent-run.txt`.
3. DENY run: `omnigent run agents/sealed-lab-deny --no-session`. Instrument is the D-2 inverted scorer (returns 1−AUC). Policy line: instrument_check FAILED exit 1, experiment BLOCKED. Agent did not edit the gate, bypass the policy, or run another way. Transcript: `omnigent-deny-demo.txt`.
4. A/B: `ab-gates-result.txt`. Gates ON 3/3 blocked before data, 0 false findings, 0 false blocks. Gates OFF 0/3 caught, 3 false findings.

## Numbers you may say

| source | claim |
|---|---|
| `result.json` (sim, n=30, seed 20261003) | RQ-RESIST **H0**. Gap (Tor−SOR) **−0.058**, CI **[−0.104, −0.014]**, δ=0.08. VPN precision @ b=0.001 = 0.0895 (positive control PASS). |
| `real-frontier.json` | **EXPLORATORY pilot only**, n=20 single run. WG AUC 0.916 / 7.8 ms; Tor 0.822 / 786 ms; nested-SSH 0.511. Not the shipped claim. |
| `lagscore-result.txt` + finding-07 | n=6. SOR naive TPR 0.000 → lag-search **0.267**. Tor 0.167 → **0.025**. WG 0.683 → 0.558. **SOR>Tor is retracted.** Tor is the most resistant arm under a lag-aligning adversary. |

## Do not say

- SOR is more resistant than Tor, or gap 0.13 as a confirmatory win (finding-06, corrected by finding-07).
- That `experiment/run.py` executed the planner's T2. The director caught a T1-shaped run.
- A numeric 10× acceleration. Observed improvement is 3/3 false findings prevented.
- Human names. `submission.json` team slot is still `[NAME]`.
- That agents named Literature, Hypothesis, Analysis, Reviewer, or Safety ran. The YAML wires director → planner, runner only.
- Port 6767 unless that is the port printed in the session you are filming.

## Spoken script

### BEFORE YOU ROLL · what this demo actually is

Open file:///home/trilltechnician/coding/hackathon/demo/teleprompter.html — not a relative hackathon/demo path. Repo is ~/coding/hackathon. You are on trillsec.

Sealed Lab is an Omnigent lab for Challenge 03. The live thing you can show is not a product UI tour. It is two agent runs plus three executable gates, and a result the lab itself later retracted.

Say this up front, out loud: verification caught a false finding. Do not say SOR is more resistant than Tor. Finding-07 retracted that. The naive correlator showed SOR at TPR zero. A lag-searching re-score flipped it.

### 0:00 · NAME THE MACHINE

This is the hackathon repo. Omnigent is 0.16.0. The web UI comes up on a localhost port the CLI prints. It is not always 6767. Read the port off the banner.

Three agents exist as YAML. agents/sealed-lab is the clean loop. agents/sealed-lab-deny points the instrument at an inverted scorer. agents/sealed-lab-team is the director, with two sub-agents: planner and runner. There is no literature agent and no safety agent in that config. Do not introduce them.

### 0:25 · FOOTAGE WE ALREADY HAVE

Clip demo/footage/01-rigor-gates.mp4 is eighteen seconds. It is the offline gate trio, re-runnable, not the Omnigent web UI.

On that clip, point as you talk. First, python3 method/tools/design_check.py config/designs/anon-baserate.json. That is the design gate. The recorded take printed PASS, ten of ten, before any campaign data.

Second, python3 method/tools/verify_seals.py on output/anon-baserate. Seals re-hash the frozen pre-registration. A silent edit after sealing fails this gate.

Third, python3 config/policies/test_require_gate.py. That is the offline DENY. The policy evaluates before the experiment command and fails closed.

### 1:05 · THE MULTI-AGENT LOOP · exact command

From ~/coding/hackathon, the command that actually ran is: export PYTHONPATH="$PWD"; omnigent run agents/sealed-lab-team --no-session.

The director does not run the experiment itself. It calls sys_session_send twice, then sys_read_inbox.

Handoff one. Agent planner, title pick-test. It reads config/designs/anon-baserate.json and prereg section 8. It chose T2, depth, because T2 is the only pre-registered test that can settle the main question. T1 cannot. Its conditions were: A-learned passes the section 11 instrument gate, and the sd_run re-fit stays at or below 0.13. Otherwise report exploratory.

Handoff two. Agent runner, title run-experiment. The prompt told it to run exactly python3 experiment/run.py and not to work around a deny. The rigor policy admitted that command. Exit zero.

### 2:05 · WHAT THE RUNNER ACTUALLY RETURNED

This is the simulation record in output/anon-baserate/result.json, not the later real captures. Seed 20261003. Thirty runs. Base rate b = 0.001. Delta 0.08.

RQ-RESIST verdict: H0. Mean gap, Tor minus SOR, is minus 0.058. The interval is minus 0.104 to minus 0.014. That interval sits entirely below zero, so in the sim SOR was slightly more linkable than Tor, not more resistant. Precision at the honest base rate: VPN 0.090, Tor 0.040, SOR 0.045. The VPN line is the positive control. It passed.

Then say the director's catch, because it is the point of the shot. The script that ran is three arms with one attacker each. That looks like T1 breadth, not T2. No A-learned split showed up. The director refused to paper over it and prescribed a new sealed iteration. The hypothesis it offered, SOR's extra linkability might be the 0.60 bandwidth overhead, is labeled agent-generated, untested.

### 3:00 · THE DENY · second live command

Switch agents. Same working directory. export PYTHONPATH="$PWD"; omnigent run agents/sealed-lab-deny --no-session.

What is injected is the real D-2 defect: a scorer that returns one minus AUC. On a perfectly separable case the gate expects 1.0 and got 0.0. On the reversed case it expects 0.0 and got 1.0. Transcript line, read it, do not paraphrase the numbers: Denied by policy: instrument_check FAILED, exit 1. Experiment run BLOCKED until the gate passes.

Then the agent's own limit, also from that transcript: it did not edit the gate, did not bypass the policy, and did not run the script another way. Unblock means fix the score orientation, rerun instrument_check until both rows pass, then rerun in a new sealed iteration.

### 3:40 · THE A/B · same three defects, gates on versus off

File output/anon-baserate/ab-gates-result.txt. Three defects from the program's real history, not invented ones.

Inverted correlator, instrument_check: gates on block, gates off slip. Underpowered design, design_check: block versus slip. Tampered pre-registration, verify_seals: block versus slip.

Score line: gates on caught 3 of 3 before any data, zero false findings, zero good runs falsely blocked. Gates off caught 0 of 3 and emitted 3 false findings. Human rechecks: three with gates off, zero with gates on. The lever on the card is verified results per hour, not a made-up 10×.

### 4:05 · THE RESULT YOU ARE ALLOWED TO CLAIM · finding-07

A later real campaign, finding-06, looked like SOR beat Tor: naive TPR zero on SOR, gap 0.13, interval 0.07 to 0.21. A verifier then showed the published mechanism was wrong, and the correlator did no lag search while the extra relay hop shifts time.

lagscore-result.txt, n = 6 runs per arm. SOR naive AUC 0.47, TPR 0.00, becomes lag-search AUC 0.76, TPR 0.27. Tor naive TPR 0.17 becomes 0.03. WireGuard stays the most linkable, TPR 0.68 down to 0.56.

Say the flip in one sentence. Under a lag-aligning adversary, Tor is the most resistant arm, and the SOR-wins claim was an alignment artifact. That retraction is the demo. An AI lab that only generates would have shipped the false finding.

### 4:25 · CLOSE · what you will not claim

Do not say the paired n=30 battery finished. Do not say SOR latency is a real path measurement. The client was hitting a local ssh forward. Do not say the planner's T2 choice was what experiment/run.py executed. The director caught that it was not.

Close on the file, not a slogan you cannot source. Next registered step is to make the lag-searching correlator the instrument and rerun instrument_check. Seals are intact. The gates gate. The false finding did not ship.
