# Submission checklist: Challenge 03 brief → file

The brief's submission list reads: *"The repository, agent specifications and policies, a two
minute demo, cited evidence, experiment code and results, your measured improvement and your
next experiment."* Status as of 2026-10-03/04. ✅ means it is done and in the repo. ⚠️ means it
is partly done or needs action outside the repo.

## Required deliverables

| # | Brief requirement | Satisfied by | Status |
|---|---|---|---|
| 1 | **The repository** | this repo; entry point `README.md` | ✅ built. ⚠️ **Not pushed yet.** Publish through the scrubbed orphan export in `docs/SECURITY-AUDIT.md` § "STILL TO DO", because the old history still contains the tailnet IP and author email. |
| 2 | **Agent specifications** | `agents/sealed-lab/`, `agents/sealed-lab-team/` (+ `agents/planner`, `agents/runner`), `agents/sealed-lab-deny/`, `agents/sealed-lab-verify/` (all `config.yaml`) | ✅ |
| 2b | **Policies** | `lab/policies.py` (`require_gate`, `require_gate_shell`), `config/policies/require_gate.py` + `test_require_gate.py` (offline proof, passes) | ✅ |
| 3 | **Two-minute demo** | Script/storyboard in `demo/vo-script.md`, `demo/VIDEO-BRIEF.md`, `demo/RENDER-NOTE.md`. Rendered 120 s silent master lives **outside** the repo (video-toolkit `out/sealedlab-silent.mp4`). | ⚠️ **Human VO not recorded or muxed yet** (see `demo/RENDER-NOTE.md` § "Final VO mux"). Upload the final mp4 separately: `footage/` is git-ignored and the video is not in the repo. |
| 4 | **Cited evidence** | `research/field-challenges.md` (verification gap, arXiv:2608.05179 et al.), `research/cyber-eval-gaps.md`, `research/moonshot-framing.md` (anonymity trilemma, IEEE S&P 2018); numeric claims → `output/anon-baserate/*` | ✅ |
| 5 | **Experiment code** | `experiment/run.py`, `experiment/substrate.py`, `experiment/ab_gates.py`, `experiment/defects/`, `experiment/real_lab/` (`verify_result.py`, `lagscore*.py`, `sensitivity.py`, campaign scripts) | ✅ |
| 5b | **Results** | `output/anon-baserate/` holds findings 01–08, `result.json`, `real-data/`, the verification reports, and 4 Omnigent transcripts | ✅ |
| 6 | **Measured improvement** | `output/anon-baserate/finding-02-acceleration.md` + `ab-gates-result.{txt,json}`: 3/3 defects caught pre-data, 0 false findings, 0/3 legit work blocked | ✅ The README states the multiplier honestly: none is claimed beyond what was observed. |
| 7 | **Next experiment** | `README.md` §7; `finding-07-artifact-caught.md` § "What's still true / next" | ✅ |

## Hard constraints from the brief

| Constraint | Evidence | Status |
|---|---|---|
| Omnigent orchestrates the live loop | `docs/OMNIGENT-ROLE.md`; transcripts `omnigent-{live-run,multiagent-run,deny-demo,verify-run}.txt` | ✅ |
| Multiple specialist agents exchange outputs | `finding-05-multiagent.md` (director → planner → runner via `sys_session_send`) | ✅ |
| Agents adapt the plan after a result | finding-05 (director orders a new sealed iteration); finding-07 (verify agent retracts and redirects) | ✅ |
| ≥2 candidate tests, planner picks one by learning/feasibility/cost | prereg §8 (T1 breadth / T2 depth); planner chose T2 in finding-05 | ✅ ⚠️ The choice is not yet wired to parameterize `run.py`. This limitation is disclosed. |
| Citations for every factual claim | `research/*.md`; artifacts in `output/` | ✅ |
| Agent hypotheses labeled; uncertainty preserved | finding-05 ("agent-generated, untested"); finding-07 ("provisional") | ✅ |
| Controls + human-approval gates documented | README §6; WireGuard positive control; fail-closed DENY demo | ✅ |
| Validation needed before real-world use stated | README §6 | ✅ |
| Improvement reported honestly, not inflated | README §4, finding-02 | ✅ |

## Honesty guardrails (check before submitting)

- [x] The real "SOR > Tor" result is presented as **RETRACTED** (a measurement artifact), never as a discovery.
- [x] The corrected ranking (Tor most resistant) is labeled **provisional/exploratory**.
- [x] Findings 01, 04, and 06 are marked superseded by 07.
- [x] No speed-up multiplier is claimed beyond 3/3 defects prevented.
- [x] Tracked files carry no IPs or secrets (`docs/SECURITY-AUDIT.md`; re-scanned for this commit).
- [ ] Git history scrubbed through the orphan export **before any push**.
- [ ] Final video with human VO rendered and uploaded.

## Live submission
- **Repo:** https://github.com/leetcrypt/sealed-lab (public, clean single commit, scrubbed).
- **Videos:** demo (1:00) + tech (1:00) rendered with scratch VO + music; silent masters await the founder's human VO. Team = founder bio (self-recorded).
- **Pending (founder):** record demo + tech VO; record team bio; decide the 3 flagged bio claims.
