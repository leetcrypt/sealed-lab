#!/usr/bin/env bash
# Clean single-commit submission export — removes the tailnet IP + author email from history.
# Does NOT push. Review, then push the `submission` branch to the public repo yourself.
set -euo pipefail
cd "$(dirname "$0")"
test -z "$(git status --porcelain)" || { echo "commit/stash working tree first"; exit 1; }
git branch -D submission 2>/dev/null || true
git checkout --orphan submission
git add -A
git commit -q -m "Sealed Lab — Agentic Scientific Discovery (Hack-Nation x Databricks, Challenge 03)"
# generic author on the export (comment out to keep your identity)
git commit -q --amend --no-edit --author="Sealed Lab <noreply@users.noreply.github.com>"
echo "clean 'submission' branch created (1 commit, no sensitive history)."
echo "verify:  git log --format='%an <%ae>' submission | sort -u   (should show only the generic author)"
echo "then:    git push <public-remote> submission:main   # you run this, after confirming the remote+scope"
