#!/usr/bin/env python3
"""Verify every recorded SHA-256 seal against the file it claims to seal.

`_config/rigor-standards.md` says a break in the provenance chain is an audit failure at
stage 08. Nothing enforced that. A sealed pre-registration was edited in place and the
mismatch went unnoticed until `git status` happened to show the file dirty — which is luck,
not a control. This is the control.

Three distinct failures, deliberately kept distinct because they mean different things:

  MISMATCH   the file changed after it was sealed. The seal is now worthless, and an
             honest amendment is indistinguishable from tampering. This is the serious one.
  MISSING    a seal names a file that is not there.
  UNSEALED   a frozen-looking artifact (prereg) carries no seal at all, so nothing is
             pinned and there is nothing to break.

Stdlib only. Exit non-zero on any MISMATCH or MISSING.

    python3 tools/verify_seals.py              # whole repo
    python3 tools/verify_seals.py stages/03-design
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# "<64 hex>  <path>", the format `sha256sum` writes and `sha256sum -c` reads.
LINE = re.compile(r"^([0-9a-fA-F]{64})\s+\*?(.+)$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve(target: str, seal: Path) -> Path:
    """Seals record paths relative to the repo root; older ones may be relative to the seal
    itself. Accept either rather than reporting a false MISSING.

    `seal.parent / target` keeps the *whole* recorded path (not just the basename), which is
    what makes a seal portable: a study that borrows this pipeline keeps its artifacts in its
    own repo, so nothing there is relative to THIS root. Without it, a seal recording
    `rubric/checks.js` is a false MISSING the moment it lives outside sci-method — and a
    verifier that cannot check another repo's seals is a verifier people stop running."""
    for cand in (ROOT / target, seal.parent / target, seal.parent / Path(target).name):
        if cand.is_file():
            return cand
    return ROOT / target


def main(argv: list[str]) -> int:
    scope = ROOT / argv[0] if argv else ROOT
    seals = sorted(p for p in scope.rglob("*.sha256") if ".git" not in p.parts)

    ok, mismatch, missing = [], [], []
    for seal in seals:
        for raw in seal.read_text().splitlines():
            raw = raw.strip()
            if not raw or raw.startswith("#"):
                continue
            m = LINE.match(raw)
            if not m:
                mismatch.append((seal, raw, "unparseable seal line", ""))
                continue
            recorded, target = m.group(1).lower(), m.group(2).strip()
            path = resolve(target, seal)
            if not path.is_file():
                missing.append((seal, target))
                continue
            actual = sha256(path)
            (ok if actual == recorded else mismatch).append(
                (seal, target, recorded, actual))

    # Unsealed pre-registrations: pinned by nothing, so nothing can be shown to have moved.
    sealed = {resolve(t, s).resolve() for s, t, _, _ in ok + mismatch}
    unsealed = [
        p for p in sorted(scope.rglob("*.md"))
        if ".git" not in p.parts
        and "references" not in p.parts          # templates and citations, not artifacts
        and re.search(r"prereg", p.name, re.I)
        and p.resolve() not in sealed
    ]

    rel = lambda p: p.relative_to(ROOT) if ROOT in p.parents or p == ROOT else p  # noqa: E731

    print("=" * 78)
    print(f"SEAL VERIFICATION — {len(seals)} seal file(s) under {rel(scope)}")
    print("=" * 78)

    for seal, target, _, _ in ok:
        print(f"[  OK  ] {target}\n         sealed by {rel(seal)}")
    for seal, target in missing:
        print(f"[MISSING] {target}\n         named by {rel(seal)} but not on disk")
    for seal, target, recorded, actual in mismatch:
        print(f"[MISMATCH] {target}\n         seal:   {recorded}\n         actual: {actual}"
              f"\n         sealed by {rel(seal)}")
    for p in unsealed:
        print(f"[UNSEALED] {rel(p)}\n         looks like a prereg but no .sha256 records it")

    print("\n" + "=" * 78)
    print(f"verified {len(ok)}   mismatched {len(mismatch)}   missing {len(missing)}"
          f"   unsealed {len(unsealed)}")

    if mismatch:
        print("\nA MISMATCH means the sealed file changed after sealing. The seal no longer")
        print("proves anything, and an honest amendment is now indistinguishable from")
        print("tampering. Do not 're-seal to make this green' — that destroys the evidence.")
        print("Restore the sealed content and put the amendment in a separate, separately")
        print("sealed addendum, so the original stays verifiable and the change stays visible.")
    if unsealed:
        print("\nUNSEALED is not automatically a fault: a draft prereg should not be sealed.")
        print("It is a fault once the document is treated as frozen.")

    print("=" * 78)
    return 1 if (mismatch or missing) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
