# Paper Structure (Layer 3 — canonical)

Referenced by stage 07 (full file) and stage 08 (as review criteria).
Target venue style: generic peer-review (arXiv-ready markdown; LaTeX conversion optional).

## Required sections, in order

1. **Title** — specific, claim-bearing, no hype words ("novel", "revolutionary").
2. **Abstract** — ≤250 words: context (1–2 sentences), gap, method, key quantitative
   result(s) with effect size, implication. Written last.
3. **Introduction** — funnel: field context → SOTA in brief → the gap (cite the gap
   analysis sources) → this paper's contribution as 2–4 explicit bullets → roadmap.
4. **Related Work** — organized by theme, not by paper; each paragraph ends by
   positioning this work relative to the theme.
5. **Methods** — from the pre-registration: hypotheses (H1/H0), design, materials,
   procedure, analysis plan. State that the study was pre-registered and where the
   prereg artifact lives. Include the deviations log content.
6. **Results** — confirmatory results first, in prereg order, each with effect size +
   CI; then a clearly-marked Exploratory subsection if any. Figures/tables referenced
   in text; no interpretation here.
7. **Discussion** — interpret against H1/H0 and the literature; alternative
   explanations considered explicitly; practical + theoretical implications.
8. **Limitations** — own subsection or section; includes every accepted validity threat
   from the prereg plus anything discovered during the run.
9. **Conclusion** — ≤2 paragraphs; no new claims.
10. **References** — per `_config/citations.md` Format.
11. **Appendices** (as needed) — prompts, full configs, extended tables, reproduction
    instructions.

## Replication checklist (Methods must satisfy ALL — stage 07 audit gate)

- [ ] A competent peer could re-run the experiment from Methods + appendix alone
- [ ] All materials specified: datasets/versions, model IDs, parameters, prompt text
- [ ] Procedure stated step-by-step, including run counts and seeds policy
- [ ] Analysis: exact tests, α, corrections, exclusion rules — matching the prereg
- [ ] Compute/environment described (hardware, OS, key library versions)

## Writing rules

- Precise, plain, active voice. No hype; claims scale with evidence ("suggests" vs
  "demonstrates" chosen deliberately).
- Numbers: report exact values with units; consistent significant figures; percentages
  accompanied by absolute counts.
- Every figure/table has a self-contained caption and is cited in the text.
- Hedged language only where uncertainty is real — then quantify the uncertainty.
