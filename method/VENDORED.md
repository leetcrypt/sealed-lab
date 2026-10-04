# Vendored sci-method method layer

Pinned copy of the rigor machinery from the canonical repo on the laptop. This repo is
the hackathon submission and must be self-contained; these files are **not forked** — they
are a pinned snapshot. Trace bugs to the source, don't diverge silently.

- **Source:** `laptop:~/coding/sci-method`
- **Source commit:** `aa33f13f6e4169a3299292db250d67123dd1d233`
- **Vendored:** 2026-10-03

| File | Role | Gate stage |
|---|---|---|
| `tools/design_check.py` | execute a pre-registered design vs synthetic worlds | 03 (before seal) |
| `tools/instrument_check.py` | execute instruments vs ground-truth anchors | 04 (before scoring real data) |
| `tools/verify_seals.py` | re-hash every SHA-256 seal | 05/06/08 |
| `_config/rigor-standards.md` | design/stats/reproducibility gates (cited by the tools) | — |
| `_config/paper-structure.md` | IMRaD template rules | 07 |
| `_config/citations.md` | citation format + source quality tiers | 01/07 |

All three tools are stdlib-only and verified to run on this box's Python 3.14.
