# Tech video script — grounded correction (do not treat Tech.tsx as current)

`projects/kinetic-15s/src/hacksub/Tech.tsx` still shows the pre-finding-07 split: real pilot provisional H1 (SOR > Tor, exploratory) vs frozen sim H0. That pilot card is **incomplete**. Finding-07 (`output/anon-baserate/finding-07-artifact-caught.md`, `lagscore-result.txt`) retracted SOR>Tor as a lag-alignment artifact.

Speak **teleprompter Tech A / Tech B**, not the on-screen exploratory-H1 card, until Tech.tsx is re-rendered. This pass does not re-render it and does not touch `out/sealedlab-silent.mp4`.

## Facts safe to keep from Tech.tsx

- 38% / 0% in-loop verification framing and arXiv:2608.05179 (already in VIDEO-BRIEF; not re-audited against the paper tonight).
- Loop steps and the three gate names.
- A/B table matches `ab-gates-result.txt`: 3/3 caught, 0 false findings, 0 false blocks. The "human rechecks 3 → 0" row matches finding-02.
- Sim side of the prereg card matches `result.json`: H0, gap about −0.058, CI about [−0.104, −0.014], VPN control PASS.
- Limits that are still true: SOR latency instrument was a local forward; relay confound; confirmatory paired battery not the shipped claim.

## Facts to stop showing

- "provisional H1 — SOR > Tor" as if it survived review.
- Finding-06 "confidently more resistant" (already marked overclaim inside finding-06, then superseded).
- Any 10× multiplier.

## Placeholder

`src/hacksub/data/submission.json` is still the bracket template (`[QUESTION]`, `[X.X x]`, team `[NAME]`). Tech.tsx does not import it. Do not fill it with invented numbers.
