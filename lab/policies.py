"""Omnigent FunctionPolicy: block a loop-advancing tool call until a sci-method rigor
gate passes. Deployed copy of config/policies/require_gate.py (proven offline 5/5).

Contract (omnigent/policies/function.py): callable(event, config) -> {"result", "reason"}.
Factory form in YAML: function: {path: lab.policies.require_gate, arguments: {...}}.
"""
from __future__ import annotations
import subprocess
from collections.abc import Callable


def require_gate(gate: str, guard_tools: list[str], cmd: list[str],
                 cwd: str | None = None, timeout: int = 180) -> Callable[[dict, dict], dict]:
    guarded = set(guard_tools)

    def evaluate(event: dict, config: dict) -> dict:
        if event.get("type") != "tool_call" or event.get("target") not in guarded:
            return {"result": "ALLOW"}
        try:
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        except Exception as exc:
            return {"result": "DENY", "reason": f"{gate} gate could not run: {exc}"}
        if p.returncode == 0:
            return {"result": "ALLOW", "reason": None}
        tail = (p.stdout + p.stderr).strip().splitlines()[-3:]
        return {"result": "DENY",
                "reason": f"{gate} FAILED (exit {p.returncode}); '{event.get('target')}' "
                          f"blocked by rigor policy. " + " | ".join(tail)}
    return evaluate


def _find_command(data) -> str:
    """Pull the shell command string out of a tool-call event payload, whatever its shape."""
    found = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("command", "cmd") and isinstance(v, str):
                    found.append(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(data)
    return " ; ".join(found)


def require_gate_shell(gate: str, match: str, cmd: list[str],
                       guard_tools: list[str] | None = None,
                       cwd: str | None = None, timeout: int = 180) -> Callable[[dict, dict], dict]:
    """Gate the SHELL tool: when the command runs the loop-advancing step (contains `match`),
    require `cmd` (a rigor gate) to pass first. DENY on gate failure, fail-closed."""
    guarded = set(guard_tools or ["sys_os_shell", "Bash", "bash", "shell", "Shell", "terminal"])

    def evaluate(event: dict, config: dict) -> dict:
        if event.get("type") != "tool_call" or event.get("target") not in guarded:
            return {"result": "ALLOW"}
        command = _find_command(event.get("data"))
        if match not in command:
            return {"result": "ALLOW"}
        try:
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        except Exception as exc:
            return {"result": "DENY", "reason": f"{gate} gate could not run: {exc}"}
        if p.returncode == 0:
            return {"result": "ALLOW", "reason": f"{gate} PASS — loop may advance"}
        tail = (p.stdout + p.stderr).strip().splitlines()[-3:]
        return {"result": "DENY",
                "reason": f"{gate} FAILED (exit {p.returncode}); experiment run BLOCKED by "
                          f"rigor policy until the gate passes. " + " | ".join(tail)}
    return evaluate
