# Methods note — device roster + exclusion (real-data campaign)

> Pre-data operational decisions for the repeated-run campaign, recorded for the audit trail.

## Device roster (in-scope)
- **trillsec** (this box) — WG/Tor sink (egress observer); SOR client (ingress observer).
- **laptop** — WG/Tor client (ingress observer); SOR sink (egress observer).
- **grok-bot** (cloud VM) — SOR relay hop (stable, non-mobile).
- **fp6, tab7** — available phone relays (fast: ~2 s forward setup). Keepalive config applied.

## EXCLUSION: tril
`tril` (trilluminati phone) is **excluded** as a relay. Measured forward-setup latency was
**~21 s** (vs ~2 s for fp6/tab7), which caused repeated SOR tunnel timeouts and 0 captured
runs. This is an operational (apparatus) exclusion made **before** any tril data entered the
confirmatory set — tril contributed no measurements to the study. Not a results-dependent
exclusion.

## Relay reliability fix applied (all phones)
Appended to each phone's `$PREFIX/etc/ssh/sshd_config`: `ClientAliveInterval 20`,
`ClientAliveCountMax 6`, `TCPKeepAlive yes`, `AllowTcpForwarding yes`; sshd restarted and
verified. See `experiment/real_lab/PHONE-RELIABILITY.md`.

## Topology note (honest asymmetry)
WG/Tor: client=laptop, sink=trillsec. SOR: client=trillsec, sink=laptop (so grok-bot could be
the relay — laptop cannot reach grok-bot directly). The adversary model (both-ends observation
of a multi-hop path) holds for all arms; the end-swap is documented, not hidden.

## SOR mechanism (clarified on the clean relay)
SOR's correlation resistance survives the move from a mobile relay to a stable cloud relay
(TPR still 0.0), so it is **not** a mobile-buffering artifact: nested SSH tunneling inherently
buffers (TCP-over-TCP), collapsing the per-flow timing fingerprint. Latency for tunneled arms
is still a local-forward artifact (connect to a local `-L` port) — first-byte RTT is the fix,
a stated next step.
