"""Omnigent function tools for the Sealed Lab. Each shells out to a real, committed script
and returns a short text result the agent can read. Stdlib only."""
from __future__ import annotations
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _run(cmd: list[str], timeout: int = 300) -> str:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    out = (p.stdout + p.stderr).strip()
    return f"[exit {p.returncode}]\n{out[-2000:]}"


def check_rigor_gates(**kwargs) -> str:
    """Run the design gate then the instrument gate. Non-zero exit = gate FAIL."""
    d = _run(["python3", "method/tools/design_check.py", "config/designs/anon-baserate.json"])
    i = _run(["python3", "method/tools/instrument_check.py",
              "config/instruments/anon-baserate.json", "--gates", "OEP"])
    return f"=== design_check ===\n{d}\n\n=== instrument_check ===\n{i}"


def run_experiment(**kwargs) -> str:
    """Run the pre-registered experiment loop (gated by policy on this tool)."""
    return _run(["python3", "experiment/run.py"])


def verify_seals(**kwargs) -> str:
    """Re-hash every seal under the study output dir."""
    return _run(["python3", "method/tools/verify_seals.py", str(ROOT / "output/anon-baserate")])
