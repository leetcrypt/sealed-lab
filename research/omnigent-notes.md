# Omnigent — Setup and Integration Notes

> Required platform for every submission. Open-source route chosen (no Databricks
> account needed). Repo: https://github.com/omnigent-ai/omnigent (Apache 2.0, alpha).

## Installed on trillsec (2026-10-03)

| Component | Version | Status |
|---|---|---|
| omnigent | 0.16.0 (built 2026-09-29) | `~/.local/bin/omnigent`, installed via `uv tool install --python 3.12 omnigent` |
| Python | 3.14.7 (omnigent pinned to 3.12) | ✓ |
| Node / npm | 22.23.1 / 10.9.8 | ✓ |
| pnpm | 12.9.1 | installed globally via npm |
| tmux / git / bwrap | 3.7c / 2.55 / 0.12.0 | ✓ (bwrap = Linux sandbox) |

## Still to do (H0–1 spike)

```bash
omnigent setup          # interactive: pick credentials (Claude sub / API key / Ollama)
omnigent start          # local server; web UI at http://localhost:6767
omnigent claude         # sanity: Claude Code harness under Omnigent
omnigent run agents/<agent>.yaml
```

Auth: `ANTHROPIC_API_KEY` is **not exported** in this shell. Use the Claude
subscription through `omnigent setup`, or a key from a git-ignored `secrets.env`.
Ollama fallback: Omnigent defaults to `http://localhost:11434/v1`, but ours serves on
the tailnet. Override it to `http://<trillsec-tailnet-ip>:11434/v1`.

## Concepts we use

- **Runner** wraps any agent in a sandboxed session with a uniform API. The **server**
  sits above it and handles policies and sharing.
- **Agent YAML**: `name`, `prompt`, `executor.harness` (`claude-sdk` and others),
  `tools` (`function` | `mcp` | `agent`, where sub-agents are the handoff mechanism).
- **Policies**: Python handlers referenced from YAML at three levels: server, agent,
  session. Built-ins we will use: `ask_on_os_tools`, `max_tool_calls_per_session`,
  `cost_budget` (with `ask_thresholds_usd`).
- **Our custom policies** wrap the sci-method gates (`design_check`,
  `instrument_check`, `verify_seals`) plus two new ones (novelty-grounding,
  claim-grounding). Each **denies** the loop-advancing tool call until its gate passes.

## Skeleton agent YAML (verify field names in the H0–1 spike — alpha API)

```yaml
name: planner
prompt: |
  You are the experiment planner. Given a falsifiable hypothesis, design at least
  two candidate tests, estimate expected learning (power, MDE) via design_check,
  and pick one under the budget. Never execute; hand off to the runner.
executor:
  harness: claude-sdk
tools:
  design_check:
    type: function
    callable: lab.gates.design_check
policies:
  budget:
    type: function
    handler: omnigent.policies.builtins.cost.cost_budget
    factory_params: { max_cost_usd: 5.00, ask_thresholds_usd: [3.00] }
  require_design_pass:
    type: function
    handler: lab.policies.require_gate      # ours — blocks seal_prereg until PASS
    factory_params: { gate: design_check }
```

Sources: [Omnigent README](https://github.com/omnigent-ai/omnigent),
[heise: Databricks releases Omnigent](https://www.heise.de/en/news/Meta-Harness-for-AI-Agents-Databricks-Releases-Omnigent-as-Open-Source-11335496.html),
[Addepto: Omnigent explained](https://addepto.com/blog/databricks-omnigent-multi-agent-orchestration-cost-control-and-governance-explained/).
