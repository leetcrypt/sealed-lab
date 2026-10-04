"""Offline proof of the gate-enforcement mechanism. NO Omnigent runtime, NO LLM,
NO network — pure Python, zero subscription cost. Uses /bin/true and /bin/false
as stand-in gates to prove ALLOW-on-pass / DENY-on-fail before the real
sci-method tools are vendored in.
"""
from require_gate import require_gate

passing = require_gate("demo-gate", ["seal_prereg"], ["true"])
failing = require_gate("demo-gate", ["seal_prereg"], ["false"])

checks = [
    ("pass-gate allows guarded tool",
     passing({"type": "tool_call", "target": "seal_prereg"}, {})["result"] == "ALLOW"),
    ("fail-gate denies guarded tool",
     failing({"type": "tool_call", "target": "seal_prereg"}, {})["result"] == "DENY"),
    ("fail-gate ignores non-guarded tool",
     failing({"type": "tool_call", "target": "read_file"}, {})["result"] == "ALLOW"),
    ("fail-gate ignores non-tool phases",
     failing({"type": "input", "target": None}, {})["result"] == "ALLOW"),
    ("missing-gate command fails closed",
     require_gate("x", ["seal_prereg"], ["/no/such/cmd"])
         ({"type": "tool_call", "target": "seal_prereg"}, {})["result"] == "DENY"),
]

ok = True
for name, passed in checks:
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    ok = ok and passed
# show a real DENY reason string
print("\n  sample DENY reason:",
      failing({"type": "tool_call", "target": "seal_prereg"}, {})["reason"])
print("\nRESULT:", "ALL OFFLINE POLICY CHECKS PASSED" if ok else "FAILURES ABOVE")
raise SystemExit(0 if ok else 1)
