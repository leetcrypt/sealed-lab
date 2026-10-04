# Sealed Lab — Shooting Script (multi-angle)

> For filming + screen capture that the video-toolkit edits against the VO. Each beat lists
> the SHOT, the ANGLE(S), and what's on screen / what you do. Film loosely; we cut to the VO.

## Angles (label clips so the editor can sync)
- **CAM-A — face/presenter.** Phone or webcam on you, chest-up, for hook + close.
- **CAM-B — screen (trillsec).** Clean screen recording of the terminal + web UI (:6767).
- **CAM-C — over-shoulder / device.** A phone filming the monitor or a second device — texture b-roll.

## Beats

| beat | shot | angle | on screen / action | your line (optional on-camera) |
|---|---|---|---|---|
| 0:00–0:15 Hook | presenter | CAM-A | you, plain background | the VO hook, to camera |
| 0:15–0:35 Idea | pipeline anim | B-roll (graphics) | demo/pipeline-visual.html playing | VO only |
| 0:35–1:00 Science | screen | CAM-B + CAM-C | the real frontier numbers scrolling in a terminal / the plot | VO only |
| 1:00–1:20 Honest turn | screen | CAM-B | `cat output/anon-baserate/finding-04-real-frontier.md` scrolling; EXPLORATORY label | VO only |
| 1:20–1:45 Rigor live | screen | CAM-B | the DENY in the Omnigent web UI / terminal (the hero) | VO; optional reaction on CAM-A |
| 1:45–2:00 Close | presenter | CAM-A | you, to camera | the VO close |

## Clean screen captures to stage (CAM-B)
1. `python3 method/tools/design_check.py config/designs/anon-baserate.json` → PASS 10/10
2. `python3 method/tools/verify_seals.py $(pwd)/output/anon-baserate` → 4 OK
3. The Omnigent DENY run (deny-demo) in the web UI at :6767 — the hero beat.
4. `cat output/anon-baserate/real-frontier.json` → the three-arm numbers.
(The video-toolkit already captured the offline gate trio to demo/footage/01-rigor-gates.mp4.)

## Recording triggers
- Automated fleet capture: see `demo/fleet-record.sh` (screen recordings on devices that
  support it). Face/room angles: trigger your phone camera app manually (Termux can't cleanly
  record camera video).
- Name clips `beat<N>-<cam>.mp4` and drop them in `demo/footage/`. Tell the editor the take.
