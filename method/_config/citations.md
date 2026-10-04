# Citation Standards (Layer 3 — canonical)

Referenced by stages 01 (Format + Source quality tiers), 07 (Format), 08 (spot-check).

## Format

- In-text citation keys: `[AuthorYEAR]` — e.g. `[Vaswani2017]`; disambiguate with
  letters (`[McKay1999a]`).
- Bibliography entry (one per key, keyed heading):

  ```
  ### [Vaswani2017]
  Vaswani, A., Shazeer, N., et al. (2017). Attention Is All You Need.
  *Advances in Neural Information Processing Systems 30*.
  DOI/URL: https://arxiv.org/abs/1706.03762
  Accessed: 2026-07-08 · Tier: 1
  ```

- Every entry MUST have: authors, year, title, venue, and a DOI or stable URL, plus
  access date and quality tier.
- Never fabricate a citation. If a source can't be located and verified (via WebSearch/
  WebFetch/API), it does not enter the bibliography. Verify title+authors match the
  actual document, not just a plausible-sounding string.

## Source quality tiers

| Tier | What | Use |
|------|------|-----|
| 1 | Peer-reviewed journals/conferences (incl. major CS venues), meta-analyses | Preferred for all key claims |
| 2 | arXiv preprints, theses, official technical reports/docs | Fine; note "preprint" where load-bearing |
| 3 | Reputable engineering blogs, benchmark leaderboards, standards docs | Supporting color only; never sole support for a scientific claim |
| 4 | Forums, social posts, marketing pages | Do not cite (background intelligence only) |

Rules of thumb: key claims rest on Tier 1–2; if a claim rests solely on Tier 3, flag it
in the lit review. Prefer the peer-reviewed version over its preprint when both exist.

## Recency

- Record publication year for every source; the lit review states the share of sources
  from the last 5 years and justifies reliance on older work (classics are fine — say why).
