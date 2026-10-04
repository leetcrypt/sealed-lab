#!/usr/bin/env python3
"""Render Sealed Lab support assets. Does not mux or touch kinetic-15s/out."""
import json, shutil, subprocess, os
from pathlib import Path

ROOT = Path("/home/trilltechnician/coding/video-toolkit")
DEST = Path("/home/trilltechnician/coding/hackathon/demo/assets/support-20261003")
MUSIC = ROOT / "assets/music"
(DEST / "music").mkdir(parents=True, exist_ok=True)
(DEST / "sfx").mkdir(parents=True, exist_ok=True)
(DEST / "motion").mkdir(parents=True, exist_ok=True)
(DEST / "props").mkdir(parents=True, exist_ok=True)

beds = {
    "bed-demo-anguish.mp3": MUSIC / "dark-tension/anguish.mp3",
    "bed-live-anxiety.mp3": MUSIC / "dark-tension/anxiety.mp3",
    "bed-tech-aitech.mp3": MUSIC / "tech-driving/aitech.mp3",
    "bed-team-air-prelude.mp3": MUSIC / "calm-ambient/air-prelude.mp3",
}
for name, src in beds.items():
    if not src.exists():
        raise SystemExit(f"missing bed {src}")
    shutil.copy2(src, DEST / "music" / name)

env = os.environ.copy()
# caller is expected to have sourced vt-env; VT_PY may be set
py = os.environ.get("VT_PY", "python3")
sfx_kinds = ["whoosh", "whoosh-out", "impact", "riser", "sub", "pop", "tick", "glitch", "shimmer"]
for kind in sfx_kinds:
    out = DEST / "sfx" / f"{kind}.wav"
    if out.exists() and out.stat().st_size > 1000:
        print("sfx skip", kind)
        continue
    subprocess.check_call([py, str(ROOT / "bin/sfx-synth.py"), kind, "-o", str(out), "--seed", "20261003"], cwd=ROOT)
    print("sfx", out.name, out.stat().st_size)

BG, FG, INK = "#0d1117", "#e6edf3", "#8b98a9"
LOOP, AGENT, PASS, DENY = "#38bdf8", "#a78bfa", "#34d399", "#f87171"

renders = []

def add(template, outfile, props, duration, fmt):
    renders.append((template, outfile, props, duration, fmt))

add("swiss-grid", "chapter-demo.mp4", {
    "lines": ["The false finding", "did not ship."],
    "label": "SEALED LAB · DEMO",
    "index": "01",
    "bg": BG, "fg": LOOP, "ink": FG,
    "size": 120,
}, 3.2, "mp4")
add("swiss-grid", "chapter-live.mp4", {
    "lines": ["Policy denies", "the run."],
    "label": "SEALED LAB · LIVE",
    "index": "02",
    "bg": BG, "fg": DENY, "ink": FG,
    "size": 140,
}, 3.0, "mp4")
add("swiss-grid", "chapter-tech.mp4", {
    "lines": ["Execute the gate.", "Don't audit prose."],
    "label": "SEALED LAB · TECH",
    "index": "03",
    "bg": BG, "fg": PASS, "ink": FG,
    "size": 110,
}, 3.2, "mp4")
add("swiss-grid", "chapter-team.mp4", {
    "lines": ["Director.", "Planner.", "Runner."],
    "label": "SEALED LAB · TEAM · NO HUMAN ROSTER",
    "index": "04",
    "bg": BG, "fg": AGENT, "ink": FG,
    "size": 120,
}, 3.4, "mp4")
add("kinetic-title", "kinetic-verified.mov", {
    "title": "Verified results per hour",
    "subtitle": "not a faster wrong paper",
    "accent": LOOP, "color": FG, "size": 92,
}, 4.0, "mov")
add("kinetic-title", "kinetic-retracted.mov", {
    "title": "SOR greater than Tor",
    "subtitle": "retracted · lag search · finding-07",
    "accent": DENY, "color": FG, "size": 84,
}, 4.0, "mov")
add("lower-third", "lt-director.mov", {
    "name": "Director",
    "role": "delegates · does not run the experiment",
    "accent": LOOP, "plate": "#121a24", "color": FG, "size": 46,
}, 5.0, "mov")
add("lower-third", "lt-planner.mov", {
    "name": "Planner",
    "role": "picked T2 depth · prereg §8",
    "accent": AGENT, "plate": "#121a24", "color": FG, "size": 46,
}, 5.0, "mov")
add("lower-third", "lt-runner.mov", {
    "name": "Runner",
    "role": "python3 experiment/run.py · or report DENY",
    "accent": PASS, "plate": "#121a24", "color": FG, "size": 42,
}, 5.0, "mov")
add("lower-third", "lt-deny.mov", {
    "name": "instrument_check",
    "role": "DENY · orientation inverted · 1 − AUC",
    "accent": DENY, "plate": "#121a24", "color": FG, "size": 42,
}, 5.0, "mov")
add("stat-counter", "stat-gates-on.mov", {
    "value": 3, "decimals": 0, "suffix": "/3",
    "label": "defects caught before data · gates ON",
    "accent": PASS, "color": FG, "size": 200,
}, 3.5, "mov")
add("stat-counter", "stat-tor-tpr.mov", {
    "value": 0.03, "decimals": 2, "prefix": "", "suffix": "",
    "label": "Tor TPR @ 1% FPR after lag search · n=6",
    "accent": LOOP, "color": FG, "size": 200,
}, 3.5, "mov")
add("stat-counter", "stat-sor-tpr.mov", {
    "value": 0.27, "decimals": 2, "suffix": "",
    "label": "SOR TPR after lag search · was 0.00 naive",
    "accent": DENY, "color": FG, "size": 200,
}, 3.5, "mov")

hf = [py, str(ROOT / "bin/hyperframe-render.py")]
for template, outfile, props, duration, fmt in renders:
    out = DEST / "motion" / outfile
    prop_path = DEST / "props" / (Path(outfile).stem + ".json")
    prop_path.write_text(json.dumps(props))
    if out.exists() and out.stat().st_size > 5000:
        print("motion skip", outfile)
        continue
    cmd = hf + [
        "--template", template,
        "--props-file", str(prop_path),
        "--duration", str(duration),
        "--resolution", "1920x1080",
        "--fps", "30",
        "--format", fmt,
        "-o", str(out),
    ]
    print("RENDER", outfile, flush=True)
    subprocess.check_call(cmd, cwd=ROOT)
    print("ok", outfile, out.stat().st_size, flush=True)

print("DONE")
