> SUPERSEDED 2026-10-03 PT. Finding-07 retracted SOR>Tor. Speak teleprompter Demo C / Live C and live-demo-script.md. This draft is the 23:17 cut only.

# Sealed Lab — 2:00 Demo Voiceover Script

> Read at ~150 wpm (~290 words ≈ 2:00). Honest by design: the headline is that verification
> CAUGHT A FALSE FINDING — the "SOR > Tor" result was retracted as a measurement artifact
> (finding-07); the corrected ranking (Tor most resistant) is provisional, uncertainty preserved
> (brief requirement). Timecodes map to the video-toolkit beats. Swap any line freely; keep the labels.

---

**[0:00–0:15 · HOOK]** *(talking head or title cards)*
In 2024, AlphaFold mapped two hundred million protein structures and shared a Nobel Prize.
The next bottleneck in AI science isn't generating ideas — it's trusting them. Across today's
AI-scientist systems, only about a third release the records needed to verify their claims.
None verify inside the loop.

**[0:15–0:35 · THE IDEA]** *(pipeline animation)*
So we built Sealed Lab: an Omnigent lab where specialist agents run one discovery loop, and
scientific rigor is enforced as policy. An agent cannot advance the experiment until
executable gates pass. Here, rigor isn't a suggestion. It's a wall.

**[0:35–1:00 · THE SCIENCE + REAL FRONTIER]** *(frontier plot fills in)*
Our question: where do real privacy networks sit on the anonymity trilemma? We captured real
traffic through three transports. Single-hop WireGuard — fast, seven milliseconds, but fully
linkable. Real Tor, three hops — a hundred times slower, and harder to link. And a nested-SSH
path, where end-to-end correlation collapsed to chance.

**[1:00–1:20 · THE CATCH]** *(verification flips the result — artifact retracted)*
That looked like a breakthrough. But before we believed it, our verification agents dug in —
and caught a measurement artifact. Our correlator wasn't aligning for the relay's timing
offset. We fixed it, and the result flipped: SOR is actually linkable, and Tor is the most
resistant. The lab killed a false finding before it shipped.

**[1:20–1:45 · RIGOR, LIVE]** *(the real D-2 DENY clip + A/B bars)*
Here's rigor doing its job. We inject a real defect — a scorer that reads backwards. The agent
tries to run. The policy blocks it. The agent refuses to work around it. Across three planted
defects, the gates caught all three before any data. Zero false findings reached the output.

**[1:45–2:00 · CLOSE]** *(logo + next-experiment card)*
The lever isn't outputs per hour. It's verified results per hour. Next, we remove the confounds
and run the full battery. Our world needs breakthroughs — and it needs to trust them.
