# Alternative Idea — Privacy Study: /e/OS (Murena) vs Stock Android (Fairphone 6)

> Parked alternative, documented 2026-10-03 at user request. Not the chosen Plan A,
> but a strong standalone study and a possible post-hackathon paper.
> Assets: `tril` (Android/Termux phone) and `fp6` (Fairphone 6) on the tailnet.

## The question people actually want answered

"Does a de-Googled OS like Murena /e/OS measurably reduce background data exfiltration
versus stock Android, and by how much — on the *same* hardware and usage?"

Prior art this would extend: Leith (2021) "Mobile Handset Privacy: Measuring The
Data iOS and Android Send to Apple and Google"; ExodusPrivacy tracker analysis;
Trinity College Dublin Android-vs-variants telemetry work. The gap: few controlled,
*same-device, same-workload* comparisons of a de-Googled ROM against stock, with a
pre-registered metric.

## Measurable outcomes (pick one primary, pre-register it)

| Observable | How measured (on-device, our own phones) | What it shows |
|---|---|---|
| Distinct telemetry endpoints contacted at idle (24h) | On-device DNS / connection logging | Background "phone-home" surface |
| Bytes to known-tracker ASNs per app session | Passive capture of our own device traffic | Exfiltration volume |
| Trackers per installed app | Static analysis (ExodusPrivacy-style) | Baseline tracker load |
| Connections before first user action (cold boot) | Timed capture window | Out-of-box data posture |

## Why it fits sci-method well

- Pre-registration kills the obvious bias (cherry-picking apps/time windows).
- Matched-pairs design: same apps, same scripted workload, two OSes.
- `instrument_check` validates the endpoint classifier against a known-tracker fixture
  before it scores real data — same discipline as Plan A's correlator gate.
- Null result is publishable ("no significant difference at idle" is itself useful).

## Why it is NOT Plan A for a 24h hackathon

- Needs clean, matched measurement environments on two phones and a scripted workload.
- Idle-telemetry windows want hours-to-days to be credible, which is tight for one night.
- "Agentic discovery loop" is thinner: fewer natural competing-experiment decisions than
  the three-arm linkability sweep in Plan A.

**Verdict:** excellent second paper for the sci-method SOR/privacy program; keep as the
headline "next experiment" slide in the hackathon demo to show the lab generalizes.
