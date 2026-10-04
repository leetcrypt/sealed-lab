# Sealed Lab demo video — v2 (rendered)

**Deliverables** (in /home/trilltechnician/coding/video-toolkit/projects/kinetic-15s/out/):
- `sealedlab-silent.mp4` — 120.0s · 1920×1080 · H.264 · NO audio. **The VO slot**: drop the
  human voiceover here.
- `sealedlab-bedonly.mp4` — same video + just the ambient bed (if you want bed under the human VO).
- `sealedlab-scratch.mp4` — video + TTS-over-bed, **timing reference only** (not for submission).
  TTS is edge `en-US-GuyNeural`; the real VO is human (script: hackathon demo/vo-script.md).
- Audio stems: `out/vo-scratch.wav` (TTS), `out/bed.wav` (ambient), `out/audio-scratch.wav` (mixed).
Remotion project: `src/sealedlab/` (SealedLab.tsx + index.tsx + vo/script.txt). Palette = Sealed Lab.

## Final VO mux (when the human VO wav is ready)
```
cd ~/coding/video-toolkit/projects/kinetic-15s
# duck the bed under the human VO, master to -14 LUFS, mux onto the silent master:
ffmpeg -y -i out/human-vo.wav -i out/bed.wav -filter_complex \
  "[1][0]sidechaincompress=threshold=0.02:ratio=12:attack=15:release=320[b];[0][b]amix=inputs=2:normalize=0[m]" \
  -map "[m]" out/mix.wav
ffmpeg -y -i out/mix.wav -af "loudnorm=I=-14:TP=-1.2:LRA=11" out/audio.wav
ffmpeg -y -i out/sealedlab-silent.mp4 -i out/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac \
  -b:a 192k -movflags +faststart -shortest out/sealedlab-final.mp4
```
The human VO must match the beat timecodes in demo/vo-script.md (video is cut to them).

## Beats (timecodes match demo/vo-script.md; all numbers from output/anon-baserate/)
1. 0:00 Hook — verification is the bottleneck (38% / 0%, arXiv:2608.05179).
2. 0:15 The idea — the 7-step loop + rigor gates + a **LIVE multi-agent ticker** (finding-05:
   director→planner→gated runner; planner picks T2 citing prereg §8; director catches a
   plan↔execution mismatch → new sealed iteration). This is the orchestration (30%) proof.
3. 0:35 The science — real captures; first-pass (naive) scorer makes SOR look like it defeats
   correlation (AUC 0.47/det 0.00) — the striking, soon-to-flip result. WG fast+linkable, Tor slow+resistant.
   [0.07,0.21] excludes zero; sealed design held (spread 0.112 ≤ 0.13, design_check re-fit PASS);
   one logged deviation (D-real-1 unpaired → stricter test); caveats preserved (CI-low 0.07, n<30).
5. 1:20 Rigor, live (hero) — the REAL D-2 DENY verbatim (deny-demo lines 142-152) + gates A/B (3/3, 0 false).
6. 1:45 Close — "verified results per hour, not raw outputs per hour" + next + tagline + scoring chips.

## Status of the 4 videos
- **Demo (2:00): required — LOCKED (video), awaiting human VO.** ← the submission video.
- **Live-demo:** best source = output/anon-baserate/omnigent-multiagent-run.txt (+ web UI :6767). Stage a clean capture.
- **Tech (4:00) + Team (1:30): nice-to-have.** Team needs a human roster (names/roles/what-built) — pending from the user.
Offline gate footage captured: demo/footage/01-rigor-gates.mp4 (design_check PASS → verify_seals OK → require_gate DENY).

## CORRECTION — v6 (supersedes the confirmatory framing above)
The "SOR confidently more resistant than Tor" result was RETRACTED as a measurement artifact
(finding-07 + omnigent-verify-run.txt). Current beats:
- Beat 3: real captures; first-pass naive scorer makes SOR *look* resistant (AUC 0.47 / det 0.00) — the striking, soon-to-flip setup.
- Beat 4 (THE CATCH): an Omnigent verify-agent (sealed-lab-verify) ran the instrument gate, re-scored with a lag search, read its own 39-line scorer to confirm the artifact flag isn't hard-coded, and retracted. Flip table (naive → lag-search, **provisional**): WG 0.68→0.56 · SOR 0.00→0.275 · Tor 0.17→0.03. Retraction is firm; "Tor most resistant" is provisional (that scorer isn't gated yet). Payoff: the lab killed a false finding before it shipped. n=6/arm, directional.
- Beats 2 (live multi-agent) + 5 (real D-2 DENY + gates A/B) unchanged.
Scratch cut `sealedlab-scratch.mp4` (v6) supersedes all earlier scratch cuts on Telegram.
