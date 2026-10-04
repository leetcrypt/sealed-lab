> **SUPERSEDED by finding-07 (2026-10-04).** This pilot's provisional "H1 — SOR more
> resistant" was later shown to be a lag-alignment measurement artifact (the correlator did
> no lag search). Under a lag-searching adversary the ranking flips (Tor most resistant). See
> `finding-07-artifact-caught.md`. Retained as the exploratory pilot it was labeled.

# Finding-04 — REAL 3-arm frontier (pilot): WireGuard vs Tor vs SOR

> **REAL captures, all three arms**, 2026-10-03, own-fleet only. Client = `laptop` (ingress
> observer), sink = `trillsec` (egress observer). Correlator = the validated `correlator.py`.
> Run records: `output/anon-baserate/real-data/*.json`. **Status: EXPLORATORY PILOT**
> (n=20/arm, single run) — NOT the frozen confirmatory battery.

## The real frontier

| arm | transport | latency | linkage AUC | detection @1% FPR | precision @ base rate | median non-zero timing bins |
|---|---|---|---|---|---|---|
| WireGuard | 1-hop (Tailscale WG) | 7.8 ms | **0.916** | 0.70 | 0.066 | 10 / 48 |
| Tor | 3-hop onion service | 786 ms | **0.822** | 0.10 | 0.010 | 7 / 48 |
| SOR analog | 2-hop nested SSH | (see caveat) | **0.511** | 0.00 | 0.000 | **1 / 48** |

## What the real data shows

- **A real anonymity–performance trade-off.** Single-hop WireGuard is fast (7.8 ms) and
  fully linkable (AUC 0.92). Real Tor trades ~100× latency (786 ms) for materially lower
  linkability (AUC 0.82, detection 0.10). The multi-hop nested-SSH path drops to **chance**
  (AUC 0.51).
- **Mechanism, measured.** Median non-zero timing bins per connection fall 10 → 7 → 1. The
  nested-SSH path **buffered every connection into a single burst**, collapsing the timing
  fingerprint the correlator relies on. Fewer bins = less timing signal = lower linkability.
- **The base-rate correction holds on real data.** Even WireGuard's AUC 0.92 is only 0.066
  precision at the honest base rate (~14× overstatement vs balanced evaluation).

## Provisional RQ-RESIST (EXPLORATORY — labeled, not claimed)

Pilot DV: TPR@1%FPR gap (Tor − SOR) = **0.10 ≥ δ=0.08** → provisional **H1** (SOR analog more
resistant than Tor). This **flips** the simulation's H0. **It is NOT a confirmatory result** —
see caveats. The prereg's discipline applies: this is a pilot, reported EXPLORATORY.

## Caveats (preserve uncertainty — the whole point)

1. **n=20, single run per arm.** `sd_run` is not yet measured; the frozen confirmatory battery
   (per the sealed design) has not run. A pilot is not a confirmation.
2. **SOR latency is an artifact.** The client connects to a LOCAL `ssh -L` port, so the
   reported connect latency (~0 ms) does not include the path. Fix: measure first-byte RTT.
3. **Relay-buffering confound.** SOR's AUC≈0.5 is partly the mobile phone relay's buffering,
   not purely a designed SOR defense. Control: use a controlled, non-mobile relay.
4. **Asymmetry.** WG/Tor connect-latency reflect the real path; SOR's does not.

## The result CHANGES THE NEXT DECISION (new sealed iteration)

1. Measure `sd_run` from these pilot runs; re-run `design_check` (back to stage 03 if >0.13).
2. Replace the mobile relay with a controlled relay to isolate SOR's design from buffering.
3. Fix the latency instrument (first-byte RTT), register it, re-run `instrument_check`.
4. Then run the frozen confirmatory battery to turn this provisional H1 into a real verdict.

## Honesty / validation still needed

Real data, real transports, real network — a genuine slice of the prereg's "ultimate next
step." But a PILOT: no confirmatory claim until the frozen procedure runs with the confounds
controlled. This is the thesis in action: real data gave an exciting provisional result, and
rigor kept it from being overclaimed.
