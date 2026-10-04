"""require_gate — an Omnigent FunctionPolicy that blocks a loop-advancing tool
call until a sci-method rigor gate passes.

Thesis of the whole project: rigor is ENFORCED as policy, not assumed. The gate
is an external command (the vendored sci-method tools: design_check.py /
instrument_check.py / verify_seals.py). Exit 0 = PASS -> ALLOW; non-zero = FAIL
-> DENY. Omnigent evaluates this at PHASE_TOOL_CALL, which is fail-closed, so a
DENY actually stops the agent from advancing the discovery loop.

Omnigent FunctionPolicy contract (confirmed from the installed package,
omnigent/policies/function.py): the callable receives (event, config) and returns
{"result": "ALLOW"|"DENY"|"ASK", "reason": str|None}. Factory form in YAML:

  policies:
    require_design_pass:
      function:
        path: config.policies.require_gate.require_gate
        arguments:
          gate: design_check
          guard_tools: [seal_prereg]
          cmd: ["python3", "tools/design_check.py", "config/designs/anon_baserate.json"]
"""
from __future__ import annotations

import subprocess
from collections.abc import Callable


def require_gate(
    gate: str,
    guard_tools: list[str],
    cmd: list[str],
    timeout: int = 120,
) -> Callable[[dict, dict], dict]:
    """Factory: returns the per-call evaluator (closure over the gate config)."""
    guarded = set(guard_tools)

    def evaluate(event: dict, config: dict) -> dict:
        # Only gate real tool-call attempts on the guarded loop-advancing tools.
        if event.get("type") != "tool_call":
            return {"result": "ALLOW"}
        if event.get("target") not in guarded:
            return {"result": "ALLOW"}
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except Exception as exc:  # gate itself failed to run -> fail closed
            return {"result": "DENY", "reason": f"{gate} gate could not run: {exc}"}
        if proc.returncode == 0:
            return {"result": "ALLOW", "reason": None}
        tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
        return {
            "result": "DENY",
            "reason": f"{gate} FAILED (exit {proc.returncode}); "
                      f"tool '{event.get('target')}' blocked. " + " | ".join(tail),
        }

    return evaluate
