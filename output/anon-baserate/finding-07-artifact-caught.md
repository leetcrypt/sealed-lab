# Finding-07 — VERIFICATION CAUGHT A FALSE FINDING (the headline result)

> This supersedes the "SOR more resistant than Tor" claim in finding-06. Three independent
> verification agents + a lag-search re-analysis showed that result was a **measurement
> artifact**. Reports: VERIFICATION-REPORT.md, VERIFICATION-GATES.md, VERIFICATION-CORRELATOR.md.
> Evidence: lagscore-result.txt. **This is the lab working as designed.**

## What happened (the arc)

1. **Naive analysis said SOR wins.** With our correlator, SOR showed zero end-to-end linkage
   (TPR 0.00) — apparently more resistant than Tor. Finding-06 reported this (hedged as
   suggestive after verifier A caught an overclaim).
2. **Verification dug deeper.** Verifier C found the published MECHANISM ("nested SSH collapses
   timing to ~1 bin") was FALSE on the campaign data (~8 non-zero bins, like the other arms),
   and flagged the real risk: our `correlate()` does **no lag search**, while SOR's extra relay
   hop adds a timing offset. Misalignment, not resistance, could explain TPR=0.
3. **We tested it.** A lag-searching correlator (`lagscore.py`, ±10 bins) re-scored the arms:

   | arm | naive correlator | lag-searching adversary |
   |---|---|---|
   | WireGuard | AUC 0.91 / TPR 0.68 | AUC 0.88 / TPR 0.56 |
   | **SOR** | **AUC 0.47 / TPR 0.00** | **AUC 0.76 / TPR 0.27** |
   | Tor | AUC 0.76 / TPR 0.17 | AUC 0.70 / TPR 0.03 |

4. **The result FLIPPED.** Under a competent (lag-aligning) adversary, SOR is linkable (TPR
   0.27), and **Tor is the most resistant arm (TPR 0.03)** — the opposite of the naive finding.
   SOR's "resistance" was an alignment artifact of the relay's timing offset + a lag-blind scorer.

## The honest result now

- **Frontier under a competent adversary:** WireGuard most linkable → SOR intermediate → Tor
  most resistant. (Directional; n=6 per arm in the lag re-score, large effect.)
- **The "SOR > Tor" claim is RETRACTED** as a measurement artifact.
- **The real contribution is the META result:** the lab's verification layer caught a false
  finding before it shipped — a concrete instance of the "verification gap" this challenge
  targets. Naive generation produced a plausible-but-wrong result; verification killed it.

## Why this is the strongest honest outcome

This is exactly what "verification, not generation" means. An AI lab that only generates would
have published "SOR defeats Tor." Ours didn't: three independent verifiers + an adversarial
re-analysis caught the artifact. **The 10× lever is not discovering faster — it's not shipping
wrong.** That is the demonstration.

## What's still true / next

- The RIGOR machinery is sound (verifier B: seals intact, gates gate, no HARKing).
- The correlator code is correct (verifier C); the flaw was a MISSING lag search in the attack
  model + a broken SOR latency capture (local-forward artifact).
- **Next experiment:** register the lag-searching correlator as the instrument (re-run
  `instrument_check`), fix first-byte-RTT timing, run the PAIRED battery, and re-pre-register.


## Confirmed LIVE by an Omnigent verification agent (2026-10-04)

`agents/sealed-lab-verify` (claude-sdk) ran this verification through Omnigent — transcript
`output/anon-baserate/omnigent-verify-run.txt`. It ran `instrument_check` (PASS), ran
`verify_result.py`, **read the script to confirm the artifact flag is data-driven not
hard-coded**, explained the threshold effect on WG/Tor, and RETRACTED the claim. It added a
caveat we adopt:

> **The lag-searching correlator (`correlate_lag`) is NOT yet gated** — it has no orientation
> anchors or E-gate equivalence entry. So the RETRACTION is solid (SOR's 0.00 was
> alignment-dependent, proven by the jump to 0.275), but the **corrected ranking** (Tor most
> resistant) is **provisional** until `correlate_lag` is registered and `instrument_check`
> passes on it. That gating + first-byte-RTT timing + bootstrap CIs is the next sealed iteration.

This is the Omnigent link: the platform orchestrated the VERIFY stage that produced our headline,
and the agent held even the fix to the lab's own rigor standard.

## Decisive resolution of an inter-agent disagreement (2026-10-04)

Two verification agents disagreed: the lag-search re-analysis said SOR's linkage is RECOVERED
under alignment (artifact), while the correlator-gating agent claimed SOR stays decorrelated
even under lag search (genuine resistance). A direct AUC test (`decisive-auc-test.txt`) broke
the tie: under lag search SOR's **AUC = 0.788** with linked-pair mean (0.623) clearly above
unlinked (0.368), separation **+0.255**. Lag search genuinely separates linked from unlinked
for SOR, so the naive TPR=0 WAS a timing-misalignment artifact. **The retraction/artifact
finding is CONFIRMED.** (The gating agent had cited the no-lag diagonal in error.) This
disagreement, resolved by a decisive test, is itself the verification process working.
