# SCOPE (UPDATED): THREE videos, 1 MINUTE EACH — demo, tech, team.
# - DEMO-C and TECH-C: rendered by the video teammate (motion graphics below).
# - TEAM: the founder (human cast) records it himself; TEAM-C is the reference script.
# - LIVE-DEMO: DROPPED (out of scope). The DENY/verify beats fold into DEMO-C/TECH-C instead.

# Version C — 1-minute cuts (dense, motion-graphics-first). Tailored to the PDF scoring.

> Each ~60s. VO is lean (~100–120 words) so MOTION GRAPHICS carry it. Every beat maps to a
> scoring dimension: [O]rchestration 30 · [B]reakthrough 25 · [A]cceleration 20 · [R]igor 15 ·
> [C]reativity/responsibility 10. Palette: #0d1117 bg · #38bdf8 loop · #a78bfa agents · #34d399
> PASS · #f87171 DENY. All numbers are FINAL (retraction headline).
> MUSIC (all): one cinematic-electronic track, ~112–120 BPM, clear 3-act dynamics —
> curious intro → rising tension at "first pass: SOR defeats correlation" → a beat-drop/break
> at the RETRACTION → bright resolve on the payoff. Source a high-quality royalty-free track
> (Pixabay Music "tech/cinematic", or an original). Duck -14 LUFS under VO, full in gaps.

## DEMO-C  (REQUIRED video · the full loop + the catch · ~1:00)
| t | VO | motion graphics / SVG |
|---|----|----|
| 0:00 | AI can generate science in seconds. Trusting it is the bottleneck. Only a third of AI-scientist labs ship the records to verify a claim — and none verify in the loop. | [B] animated counters: 83% code / 38% seeds / **0%** in-loop (cite arXiv:2608.05179 small). |
| 0:12 | Sealed Lab is an Omnigent lab where specialist agents run one discovery loop — and rigor is a wall, enforced as policy. | [O] the pipeline-visual loop animates; a token travels director→planner→runner→verifier; a gate chip flips green. |
| 0:22 | The question: how linkable are real privacy networks — VPN, Tor, and SOR — at an honest base rate? We captured real traffic. First pass: SOR defeats correlation. | [B/A] trilemma frontier SVG; three arm dots drop in; SOR dot glows "0.00". |
| 0:36 | Then the verification agent caught it — a measurement artifact. A competent adversary links SOR. Tor is the most resistant. Retracted. | [R/C] a red "RETRACTED" stamp; flip table naive→lag (SOR 0.00→0.275); dots re-rank. |
| 0:48 | On injected defects, the gates caught three of three before any data — zero false findings. The lever isn't discovering faster. It's not shipping wrong. | [A] gates-on/off bars: OFF 3 false / ON 0; "verified results per hour". |
| 0:57 | Verification, not generation. | logo lockup; "next: gate the lag correlator, run the paired battery". |

## TECH-C  (architecture + rigor · ~1:00)
| t | VO | motion |
|---|----|----|
| 0:00 | Sealed Lab makes autonomous science trustworthy by construction. Four layers. | [R] 4-layer stack builds bottom-up. |
| 0:08 | Pre-registration, frozen and SHA-256 sealed before any data. No moving the goalposts. | a prereg card locks; a hash seals it. |
| 0:16 | Three executable gates — design, instrument, seals — run as blocking Omnigent policies. Fail, and the loop is denied. | [O/R] three gate chips; one flips red → a DENY blocks a flow. |
| 0:28 | Specialist agents run the loop: a planner picks the test, a gated runner executes, a verifier re-checks. | [O] agent handoff chain animates. |
| 0:38 | The verifier earned its keep — it caught our headline result as a measurement artifact, retracted it, then held the fix to the same gate. | [C] flip table + "RETRACTED"; a wrench icon re-enters the gate. |
| 0:50 | Every claim traced to an artifact. Uncertainty preserved. The next experiment named. Rigor that executes. | citation links fan out; CI bars with error whiskers. |

## TEAM-C  (AI-lab framing · honest · ~1:00)  — team-a (human cast) renders when roster arrives
| t | VO | motion |
|---|----|----|
| 0:00 | Sealed Lab runs on a team of specialist agents — and a human who sets the objective and approves every consequential step. | [O/C] agent roster fans out; a human silhouette at the head. |
| 0:12 | A planner chooses the experiment. A gated runner executes. A verifier re-checks, adversarially. | three agent cards light in sequence. |
| 0:24 | They can't advance past a failed gate. And they can't overclaim — we watched the verifier retract the team's own exciting result. | a gate denies; "RETRACTED" stamp. |
| 0:38 | The human seals the pre-registration, approves execution, and owns the objective. | human-approval checkmarks on SEAL + EXECUTE. |
| 0:48 | Specialist agents, enforced rigor, a human in command. The lab behind a result you can trust. | lockup. |

## LIVE-C  (live DENY + verification · ~1:00)
| t | VO | motion / source |
|---|----|----|
| 0:00 | This is the lab, live. We inject a real defect — a scorer that reads backwards. | terminal: the inverted-correlator injection (real D-2). |
| 0:10 | The agent tries to run the experiment. The policy blocks it — before a single number is produced. | [O/R] the DENY line from omnigent-deny-demo.txt (142-152), typewriter. |
| 0:22 | Its own words: it didn't edit the gate, didn't bypass the policy. Blocking this run is what the gate is for. | [C] quote card, agent avatar. |
| 0:36 | Then the verification agent re-scores with a stronger adversary, reads its own tool to check for cheating, and retracts a false finding. | omnigent-verify-run.txt beats; flip table. |
| 0:50 | Rigor you can watch. A lab that would rather say 'retracted' than be wrong. | lockup + 01-rigor-gates.mp4 tail. |

## EVIDENCE MAP — every on-screen number is grounded in a committed artifact
(Satisfies the brief's "require citations for factual claims; attach source evidence.")

| claim / number on screen | source artifact in the repo |
|---|---|
| 83% code / 0% in-loop verification | `research/field-challenges.md` (Ding et al., arXiv:2608.05179) |
| anonymity trilemma framing | Das et al., IEEE S&P 2018 (research/moonshot-framing.md) |
| 35 real captures, own-fleet | `output/anon-baserate/real-data/runs-{wg,tor,sor}.jsonl` + `aggregate-real.json` |
| WireGuard AUC 0.92 / 7.8 ms | `aggregate-real.json`, `real-vpn-result.json` |
| Tor AUC 0.76 / 1048 ms (most resistant) | `aggregate-real.json`, `real-tor-result.json`, `lagscore-full.json` |
| SOR 0.00 → 0.27 (artifact), AUC 0.79 | `finding-07-artifact-caught.md`, `decisive-auc-test.txt`, `lagscore-full.json` |
| robust across FPR; needs ~10-bin lag | `finding-08-sensitivity.md`, `sensitivity-result.txt` |
| 3/3 defects caught, 0 false findings | `finding-02-acceleration.md`, `ab-gates-result.txt` |
| design_check power 0.97 / PASS; seals 4 | `design_check-refit.txt`, `verify_seals` output |
| live DENY (inverted scorer blocked) | `omnigent-deny-demo.txt` lines 142-152 |
| Omnigent verification agent retraction | `omnigent-verify-run.txt`, `docs/OMNIGENT-ROLE.md` |
| independent GO review | `FINAL-REVIEW.md`, `VERIFICATION-*.md` (x4) |

Every figure in all three videos traces here. No number is invented for the video.
