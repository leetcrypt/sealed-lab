# Video Capture Plan — footage for the 2-minute submission

> The hackathon weights the demo heavily. Capture b-roll as we go. Most of our best
> footage is terminal output that is CHEAP TO RE-RUN, so we can stage clean takes any time
> — we don't need to have filmed the first run. Tool: the `screen-capture` skill on
> trillsec (GNOME/Wayland), which can grab the whole screen, a window, or an exact tmux
> pane (with scrollback). Browser visuals: screen-record the HTML playing.

## Footage-worthy moments (★ = headline shots for the cut)

| # | Moment | How to capture | Re-runnable? |
|---|---|---|---|
| 1 ★ | The animated pipeline visual playing one full loop | screen-record `demo/pipeline-visual.html` in a browser (~14s loop) | yes |
| 2 ★ | `design_check` printing **PASS 10/10** with the outcome distributions | re-run `python3 method/tools/design_check.py config/designs/anon-baserate.json`; capture pane | yes |
| 3 ★ | `verify_seals` printing the prereg **[ OK ]** (rigor made visible) | re-run `python3 method/tools/verify_seals.py $PWD/output/anon-baserate`; capture pane | yes |
| 4 ★ | The policy **DENY** blocking a loop-advancing tool call | `python3 config/policies/test_require_gate.py` (offline) AND the live Omnigent DENY | yes |
| 5 ★ | Live Omnigent: specialist agents handing off in the web UI (:6767) | screen-record the browser session during the live run | partial (costs tokens) |
| 6 | `instrument_check` PASS incl. the VPN anchor (orientation/equivalence/provenance) | capture pane when step 2 runs | yes |
| 7 ★ | The discovery loop "reopening": a result changing the next decision | screen-record the agent transcript + the updated record | partial |
| 8 ★ | The trilemma frontier plot filling in with the 3 arms | screen-record the analysis figure render | yes |
| 9 | Final `verify_seals` clean across the whole repo | capture pane at the end | yes |

## Capture discipline
- Prefer tmux-pane capture (exact text, scrollback) for terminal shots; full-screen only
  for the browser UI and figures.
- Name clips `NN-<slug>.mp4/png` under `demo/footage/` (git-ignored).
- Keep a 1-line log of what each clip shows, for the editor.
- Live Omnigent shots (5,7) are the only ones that cost subscription — get them in the
  single real run; everything else can be re-shot freely afterward.
