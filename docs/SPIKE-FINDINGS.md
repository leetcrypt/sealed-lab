# Omnigent Spike — Findings (confirmed from the installed package)

> Package: `~/.local/share/uv/tools/omnigent/lib/python3.12/site-packages/omnigent`
> Version 0.16.0. Recorded 2026-10-03. The policy API below is READ FROM SOURCE,
> not the README, so it is authoritative for our build.

## The thesis mechanism works, and it is pure Python (zero LLM cost)

A **FunctionPolicy** is a plain callable `(event, config) -> {"result": ..., "reason": ...}`.
- `event = {"type": "input"|"tool_call"|"tool_result"|"output", "target": "<tool>",
  "data": <payload>, "context": {"actor": {...}, "usage": {...}}, "session_state": {...},
  "llm_client": <client-or-None>, "request_data": <orig-tool-call>}`
- return `{"result": "ALLOW"|"DENY"|"ASK", "reason": str|None}` (case-insensitive result).
- Factory YAML form passes closure args:
  `function: {path: config.policies.require_gate.require_gate, arguments: {...}}`.

## Why DENY actually stops the loop
`omnigent/policies/types.py`: `FAIL_CLOSED_PHASES = ("PHASE_TOOL_CALL", "PHASE_REQUEST")`.
A policy evaluates at `PHASE_TOOL_CALL` **before** the tool runs, and that phase is
fail-closed. So a DENY on a loop-advancing tool (`seal_prereg`, `execute_capture`)
genuinely blocks the agent — exactly our "rigor enforced, not assumed" claim.

## Built-in policy handlers available (no need to write our own for these)
`omnigent/policies/builtins/`: `cost.py` (budget), `safety.py`, `_shell.py` (shell
approval), `cel.py` (CEL expression policies), `risk_score.py`, `orchestration.py`,
`routing.py`, `prompt.py`, `context.py`, `github.py`, `google.py`.
→ Use `cost.py` for the budget cap (protects the 30% subscription) and `safety.py`/
`_shell.py` for the human-approval + own-fleet-only scope. We only hand-write the
**gate** policies (`require_gate`) and the **claim-grounding** policy.

## Proven offline (config/policies/)
- `require_gate.py` — the gate-enforcement FunctionPolicy (gate = external command,
  exit 0 ALLOW / non-zero DENY, fail-closed).
- `test_require_gate.py` — 5/5 checks PASS with `/bin/true` and `/bin/false` stand-ins.
  Real gates plug in by swapping `cmd` to the vendored `tools/design_check.py` etc.

## Still to validate LIVE (will cost subscription — do once, after prereg is sealed)
1. `omnigent setup` already done (Claude subscription credential saved).
2. One `omnigent run <agent>.yaml -p "..."` to confirm a 2-agent handoff.
3. Attach the gate policy to that agent and watch a real DENY block a tool call.
   Budget: run at N=2 toy scale; low-stakes agents on local Ollama.
