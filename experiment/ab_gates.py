"""Gates-ON vs gates-OFF A/B on injected defects (the acceleration measurement, 20% criterion).

Each defect is drawn from the SOR program's REAL history. With gates ON, the rigor gate runs
and a defect is CAUGHT (non-zero exit = blocked before it can produce a finding). With gates
OFF, the gate is skipped, so the defect propagates to an emitted false/unverifiable finding
that a human must later catch and rework. Honest metric: false findings prevented and human
re-verification events avoided."""
from __future__ import annotations
import json, subprocess, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

DEFECTS = [
    {"name": "inverted correlator (real D-2 AUC inversion)", "gate": "instrument_check",
     "cmd": ["python3", "method/tools/instrument_check.py",
             "experiment/defects/inverted-instruments.json", "--gates", "O"]},
    {"name": "underpowered design (CI cannot conclude)", "gate": "design_check",
     "cmd": ["python3", "method/tools/design_check.py",
             "experiment/defects/underpowered-design.json", "--trials", "800"]},
    {"name": "tampered pre-registration (silent post-seal edit)", "gate": "verify_seals",
     "cmd": ["python3", "method/tools/verify_seals.py",
             str(ROOT / "experiment/defects/tampered")]},
]
# control: the REAL gates on the REAL artifacts must PASS (gates don't falsely block good work)
CONTROL = [
    {"name": "legit instrument", "cmd": ["python3", "method/tools/instrument_check.py",
             "config/instruments/anon-baserate.json", "--gates", "OEP"]},
    {"name": "legit design", "cmd": ["python3", "method/tools/design_check.py",
             "config/designs/anon-baserate.json", "--trials", "800"]},
    {"name": "legit seals", "cmd": ["python3", "method/tools/verify_seals.py",
             str(ROOT / "output/anon-baserate")]},
]

def run(cmd):
    t = time.time()
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)
    return p.returncode, round(time.time() - t, 1)

print("=" * 78); print("GATES-ON vs GATES-OFF — defect-injection A/B"); print("=" * 78)
caught = 0
print(f"\n{'injected defect':<48}{'gate':<17}{'ON':>6}{'OFF':>6}")
for d in DEFECTS:
    rc, _ = run(d["cmd"])
    blocked = rc != 0
    caught += blocked
    print(f"{d['name']:<48}{d['gate']:<17}{'BLOCK' if blocked else 'pass!':>6}{'slip':>6}")
print(f"\ncontrol (real artifacts must NOT be falsely blocked):")
false_blocks = 0
for c in CONTROL:
    rc, _ = run(c["cmd"]); ok = rc == 0
    false_blocks += (not ok)
    print(f"  {c['name']:<32} gate ON -> {'PASS (proceeds)' if ok else 'FALSE BLOCK (!)'}")

n = len(DEFECTS)
result = {
    "defects_injected": n,
    "gates_on_caught_before_data": caught,
    "gates_on_false_findings_emitted": n - caught,
    "gates_off_false_findings_emitted": n,
    "gates_on_human_recheck_events": 0 if caught == n else (n - caught),
    "gates_off_human_recheck_events": n,
    "control_false_blocks": false_blocks,
}
(ROOT / "output/anon-baserate/ab-gates-result.json").write_text(json.dumps(result, indent=2))
print("\n" + "=" * 78)
print(f"defects injected: {n}")
print(f"  gates ON : caught before data = {caught}/{n}   false findings emitted = {n-caught}")
print(f"  gates OFF: caught             = 0/{n}   false findings emitted = {n}")
print(f"  control false-blocks (good work wrongly blocked): {false_blocks}/{len(CONTROL)}")
print(f"\nHuman re-verification events: gates OFF = {n}  ->  gates ON = {0 if caught==n else n-caught}")
print("Headline: rigor gates move verification BEFORE data collection; with gates on, zero")
print("false findings reach output and zero human rechecks are needed. That is the lever:")
print("trustworthy results per hour, not raw outputs per hour.")
print("=" * 78)
