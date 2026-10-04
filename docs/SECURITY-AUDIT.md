# Security audit — pre-submission scan (2026-10-04)

Goal: no IPs, secrets, or sensitive data leak in the submission repo or its git history.

## Scan results (tracked files)
| Check | Result |
|---|---|
| SSH private keys / `BEGIN ... PRIVATE KEY` | **none** |
| API keys / tokens / passwords | **none** (only references to `ANTHROPIC_API_KEY` as *not exported*) |
| `.onion` addresses | **none committed** (ephemeral onion hostname lived only in `/tmp`, gitignored) |
| Public IP addresses | **none** |
| Tailnet (CGNAT 100.x) IP `<trillsec-tailnet-ip>` | **FOUND in 5 files → scrubbed (see below)** |
| Real-capture data files | clean (byte-count series only; no IPs/onion/hostnames) |

## Remediation applied (working tree)
- Tailnet IP replaced with `<trillsec-tailnet-ip>` in `CLAUDE.md`, `docs/AUDIT.md`,
  `docs/BUILD-PROPOSAL.md`, `research/omnigent-notes.md`.
- `experiment/real_lab/campaign.sh` now reads `$TRILLSEC_TS_IP` from a **git-ignored**
  `experiment/real_lab/fleet.env` (the real IP lives only there, never committed).
- `.gitignore` extended: `*.env`, `fleet.env`, `experiment/real_lab/fleet.env`.

## STILL TO DO before pushing (git HISTORY)
The scrub fixes new commits; the tailnet IP and the author email
(`<author-email>`) remain in earlier commit history. Before any `git push`:

**Recommended — clean single-commit export for the public submission:**
```bash
git checkout --orphan submission
git add -A && git commit -m "Sealed Lab — Agentic Scientific Discovery (Challenge 03)"
# optional: scrub author on the export
git commit --amend --author="hackathon-team <team@example.com>" --no-edit
# push ONLY the submission branch
```
This publishes the current (scrubbed) tree as one commit with no sensitive history.
Alternative: `git filter-repo --replace-text` (IP) + `--mailmap` (email) to rewrite history.

## Other internal identifiers (low sensitivity, NOT scrubbed)
Hostnames (`trillsec`, `laptop`, `grok-bot`, `fp6`, `tab7`), usernames, and home paths
appear in docs/scripts. These are workspace-internal, not secrets. Decide per your comfort;
the orphan-export above does not remove them. Say the word to placeholder them too.
