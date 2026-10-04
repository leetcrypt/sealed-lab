# Finding-03 — REAL data: the VPN arm on actual WireGuard (hybrid substrate)

> Per the hybrid-substrate decision (addendum-01): the VPN arm is REAL capture, Tor/SOR sim.
> Captured 2026-10-03 over the Tailscale tailnet (Tailscale IS WireGuard) between `laptop`
> (client/ingress observer) and `trillsec` (sink/egress observer). Own-fleet only, no root.
> Harness: `experiment/real_lab/`. Result: `real-vpn-result.json`.

## Real measurement (20 connections, real network timing)

| metric | real WireGuard | sim VPN (finding-01) |
|---|---|---|
| linkage AUC | **0.916** | — |
| TPR @ 1% FPR | **0.70** | 0.98 |
| precision @ base rate 1e-3 | **0.0655** | 0.0895 |
| median connect latency | **7.8 ms** | (assumed) |
| median goodput | **7.2 KB/s** | (assumed) |

## What it shows

- **Instrument validated on real traffic.** The correlator links real single-hop WireGuard
  flows end-to-end at AUC 0.92 — the positive control fires when linkage is genuinely present,
  on real data, not just on anchors.
- **Honest calibration.** Real WireGuard carries more timing jitter than the sim assumed
  (sim jitter=0.3 gave TPR 0.98; real TPR is 0.70), so the sim slightly over-stated single-hop
  linkability. This is exactly the kind of parameter the prereg says to re-fit from real
  capture (sd_run / transport jitter), and now we have a real anchor for it.
- **The base-rate contribution holds on real data.** A balanced-looking AUC of 0.92 collapses
  to 0.066 precision at the honest base rate — a ~14× overstatement, measured on real traffic.

## Scope / honesty

Real for the VPN arm only (hybrid plan). Tor and SOR remain grounded simulations: routing real
Tor to our own sink needs an onion service (Tor control socket is root/group-gated here), and
a full SOR circuit capture is the next build. Both are the stated "ultimate next step"
(prereg §14) — this finding completes a real slice of it.
