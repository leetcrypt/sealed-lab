# Deviations log — real-capture campaign

## D-real-1 — unpaired arms (vs sealed paired design)
The sealed design (prereg §7, addendum-03) specifies pairing by run: the same latent
connections scored through each transport. The real capture produced arms **sequentially and
independently** (WG, then Tor, then SOR), so runs are NOT paired. **Mitigation:** the analysis
uses the UNPAIRED two-sample gap with an independent-resample bootstrap CI — strictly more
conservative than the paired design (variance of a difference of independents ≥ paired). Logged
pre-analysis. The clean paired battery remains the stated next step.

## D-real-2 — tunneled-arm latency is a local-forward artifact
For SOR (and any `ssh -L` arm) the client connects to a LOCAL forwarded port, so the recorded
connect latency (~0.1 ms) does not reflect the real multi-hop path. Latency for SOR is therefore
NOT reported as a frontier coordinate. **Fix (next):** first-byte RTT.

## Apparatus exclusion — tril
`tril` excluded as a relay (forward setup ~21 s vs ~2 s for fp6/tab7); contributed no
measurements. See `methods-note-devices.md`.
