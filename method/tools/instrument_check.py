#!/usr/bin/env python3
"""instrument_check — execute an instrument against ground truth instead of trusting it.

Rationale: deviations log D-2 (`sor-vs-tor`, 2026-08-02). `score_pilot._auc` counted the
wrong tail and returned `1 - AUC`. A working correlator read as anti-informative
(0.366 / 0.401 instead of 0.634 / 0.599), the pilot was declared dead, and the paper
stalled five days. Nothing errored. That is the signature of this whole defect class:

    **a broken instrument degrades into an authentic-looking number, it does not crash.**

Four instances to date in this program (E-1; own-span binning; a fixture built in the
wrong index space; the AUC inversion). Every one came from re-deriving something that
already existed in sealed, tested form.

`design_check.py` gates the *design* at stage 03. `verify_seals.py` gates the *artefacts*
at 05/06/08. Stage 04 — where all four defects actually happened — had no executing gate.
This is that gate.

Gates
  O  ORIENTATION  every registered instrument hits its ground-truth anchors
                  (AUC family: perfect -> 1.0, inverted -> 0.0, coincident -> 0.5)
  E  EQUIVALENCE  every fast path equals the sealed implementation it claims to speed up,
                  on random AND tie-heavy input (ties are where hand-rolled ranks break)
  P  PROVENANCE   every instrument file is git-tracked and clean — an untracked scorer
                  cannot be diffed, reviewed, or attributed to a result
  B  BAND         reported values fall inside their pre-registered sanity band; outside it
                  mandates a defect hunt BEFORE interpretation (so the hunt is not a
                  post-hoc forking path)

Gate O is the one that would have caught D-2 on day one. Gate P is the one that would have
made it reviewable. Gate B is the one that would have made the hunt mandatory rather than
lucky.

The tool itself is stdlib only; the instruments it imports may use whatever they like.

Usage
  instrument_check.py <manifest.json>              run every gate, exit 1 on FAIL
  instrument_check.py <manifest.json> --gates OE   run a subset (letters)
  instrument_check.py <manifest.json> --list       list registered instruments, run nothing
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import subprocess
import sys
from pathlib import Path

# RTK rewrites bare `git`; anything load-bearing calls the binary by absolute path.
GIT = "/usr/bin/git"

TOL = 1e-9


# ------------------------------------------------------------------ anchor construction
# An anchor is (args, expected). Anchors are built here, in this file, from first
# principles -- never imported from the tree under test. An instrument may not supply
# the standard it is judged against.


def _auc_sequence_anchors() -> list[tuple[tuple, float]]:
    """pos/neg sequence form: auc(pos, neg)."""
    return [
        ((([0.9, 0.8, 0.95]), ([0.1, 0.2, 0.05, 0.3])), 1.0),   # every pos > every neg
        ((([0.1, 0.2, 0.05]), ([0.8, 0.9, 0.95])), 0.0),        # every pos < every neg
        ((([1.0, 2.0, 3.0]), ([1.0, 2.0, 3.0])), 0.5),          # identical -> all ties
    ]


def _square(diag_val: float, off_val: float, n: int = 5) -> list[list[float]]:
    m = [[float(off_val)] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = float(diag_val)
    return m


def _auc_matrix_anchors() -> list[tuple[tuple, float]]:
    """Score-matrix form: linkage_auc(S), diagonal = linked, off-diagonal = unlinked."""
    return [
        ((_square(1.0, 0.0),), 1.0),
        ((_square(0.0, 1.0),), 0.0),   # the D-2 defect returns 1.0 here
        ((_square(0.5, 0.5),), 0.5),
    ]


class _Pred:
    """Duck-typed stand-in for a prediction record.

    Deliberately NOT imported from the tree under test: an instrument may not supply the
    standard it is judged against. It only has to read the attributes it claims to read.
    """

    __slots__ = ("is_monitored", "confidence", "predicted_label", "true_label")

    def __init__(self, is_monitored, confidence, predicted_label, true_label):
        self.is_monitored = is_monitored
        self.confidence = confidence
        self.predicted_label = predicted_label
        self.true_label = true_label


def _tpr_at_fpr_anchors() -> list[tuple[tuple, float]]:
    """Open-world TPR at FPR <= 1e-2 (paper 2's primary DV).

    Monitored = positive, unmonitored = negative. An attacker that cannot operate at the
    FPR ceiling scores 0 there regardless of how many positives it eventually catches —
    that is the point of a fixed-FPR operating point (Axelsson base-rate honesty).
    """
    def mon(n, correct, conf):
        return [_Pred(True, conf, f"p{i}" if i < correct else "unmonitored", f"p{i}")
                for i in range(n)]

    def unmon(n, conf, label="unmonitored"):
        return [_Pred(False, conf, label, "unmonitored") for _ in range(n)]

    perfect = mon(100, 100, 0.9) + unmon(100, 0.1)
    blind = mon(100, 0, 0.9) + unmon(100, 0.1)
    half = mon(100, 50, 0.9) + unmon(100, 0.1)
    # Every negative is called monitored, with higher confidence than any positive:
    # the FPR ceiling is breached before a single true positive is admitted.
    flood = mon(100, 100, 0.5) + unmon(100, 1.0, label="p0")
    return [
        ((perfect,), 1.0),
        ((blind,), 0.0),
        ((half,), 0.5),
        ((flood,), 0.0),
    ]


ANCHOR_SETS = {
    "auc_sequence": _auc_sequence_anchors,
    "auc_matrix": _auc_matrix_anchors,
    "tpr_at_fpr": _tpr_at_fpr_anchors,
}


def _random_inputs(kind: str, rng: random.Random) -> list[tuple]:
    """Inputs for the equivalence gate: continuous first, then deliberately tie-heavy."""
    out: list[tuple] = []
    if kind == "auc_sequence":
        for _ in range(6):
            n, m = rng.randint(4, 30), rng.randint(4, 30)
            out.append((
                [rng.gauss(0, 1) for _ in range(n)],
                [rng.gauss(0, 1) for _ in range(m)],
            ))
        out.append((
            [float(rng.randint(0, 2)) for _ in range(20)],
            [float(rng.randint(0, 2)) for _ in range(20)],
        ))
    elif kind == "auc_matrix":
        for _ in range(6):
            n = rng.randint(4, 24)
            out.append(([[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)],))
        n = 12
        out.append(([[float(rng.randint(0, 3)) for _ in range(n)] for _ in range(n)],))
    else:
        raise ValueError(f"no random-input generator for anchor set {kind!r}")
    return out


# ------------------------------------------------------------------------------ loading


def _as_array(obj):
    import numpy as np  # only reached when an instrument declares "array": true

    return np.asarray(obj, dtype=float)


def load_callable(root: Path, spec: dict, sys_path: list[str]):
    """Import `function` out of `module` (a path relative to root), with root on sys.path.

    Imported by file location rather than package name on purpose: several of these
    instruments are top-level scripts in a worktree, not installed modules, and the
    provenance chain has to point at the file that actually produced the number.
    """
    for entry in sys_path:
        p = str((root / entry).resolve())
        if p not in sys.path:
            sys.path.insert(0, p)

    mod_path = (root / spec["module"]).resolve()
    if not mod_path.exists():
        raise FileNotFoundError(mod_path)
    name = mod_path.stem
    if name in sys.modules:
        mod = sys.modules[name]
    else:
        s = importlib.util.spec_from_file_location(name, mod_path)
        mod = importlib.util.module_from_spec(s)
        sys.modules[name] = mod
        try:
            s.loader.exec_module(mod)
        except BaseException:
            # A half-executed module left in sys.modules turns one missing dependency
            # into a cascade of misleading AttributeErrors on every later instrument.
            sys.modules.pop(name, None)
            raise

    obj = mod
    for part in spec["function"].split("."):
        obj = getattr(obj, part)
    return obj


def _call(fn, args, as_array: bool):
    if as_array:
        args = tuple(_as_array(a) for a in args)
    return float(fn(*args))


# ------------------------------------------------------------------------------- gates


def gate_orientation(manifest: dict, root: Path) -> list[tuple[str, bool | None, str]]:
    rows = []
    for inst in manifest["instruments"]:
        iid = inst["id"]
        aset = inst["anchors"]
        if aset not in ANCHOR_SETS:
            rows.append((f"O {iid}", False, f"unknown anchor set {aset!r}"))
            continue
        try:
            fn = load_callable(root, inst, manifest.get("sys_path", ["."]))
        except Exception as exc:
            ok = None if inst.get("optional") else False
            rows.append((f"O {iid}", ok, f"import failed: {type(exc).__name__}: {exc}"))
            continue

        bad = []
        for args, expect in ANCHOR_SETS[aset]():
            try:
                got = _call(fn, args, inst.get("array", False))
            except Exception as exc:
                bad.append(f"expect {expect} -> {type(exc).__name__}: {exc}")
                continue
            if abs(got - expect) > TOL:
                hint = " (returns 1-AUC: orientation inverted)" if abs(got - (1.0 - expect)) <= TOL else ""
                bad.append(f"expect {expect}, got {got:.6f}{hint}")
        if bad:
            rows.append((f"O {iid}", False, "; ".join(bad)))
        else:
            n = len(ANCHOR_SETS[aset]())
            rows.append((f"O {iid}", True, f"{aset}: all {n} ground-truth anchors hold"))
    return rows


def gate_equivalence(manifest: dict, root: Path) -> list[tuple[str, bool | None, str]]:
    by_id = {i["id"]: i for i in manifest["instruments"]}
    rows = []
    for inst in manifest["instruments"]:
        ref_id = inst.get("fast_path_of")
        if not ref_id:
            continue
        iid = inst["id"]
        ref = by_id.get(ref_id)
        if ref is None:
            rows.append((f"E {iid}", False, f"fast_path_of names unregistered instrument {ref_id!r}"))
            continue
        if not ref.get("sealed"):
            rows.append((f"E {iid}", False,
                         f"reference {ref_id!r} is not marked sealed — a fast path must be "
                         f"checked against the sealed implementation, not another fast path"))
            continue
        try:
            fast = load_callable(root, inst, manifest.get("sys_path", ["."]))
            slow = load_callable(root, ref, manifest.get("sys_path", ["."]))
        except Exception as exc:
            ok = None if inst.get("optional") else False
            rows.append((f"E {iid}", ok, f"import failed: {type(exc).__name__}: {exc}"))
            continue

        rng = random.Random(manifest.get("seed", 0xA0C))
        worst, worst_at = 0.0, None
        err = None
        for k, args in enumerate(_random_inputs(inst["anchors"], rng)):
            try:
                a = _call(fast, args, inst.get("array", False))
                b = _call(slow, args, ref.get("array", False))
            except Exception as exc:
                err = f"case {k}: {type(exc).__name__}: {exc}"
                break
            d = abs(a - b)
            if d > worst:
                worst, worst_at = d, k
        if err:
            rows.append((f"E {iid}", False, err))
        elif worst > 1e-9:
            rows.append((f"E {iid}", False,
                         f"diverges from sealed {ref_id} by {worst:.6g} (case {worst_at}); "
                         f"last case is tie-heavy by construction"))
        else:
            rows.append((f"E {iid}", True, f"== {ref_id} on random + tie-heavy input (max |Δ| {worst:.2g})"))
    return rows


def _git(repo: Path, *args: str) -> tuple[int, str]:
    p = subprocess.run([GIT, "-C", str(repo), *args], capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def gate_provenance(manifest: dict, root: Path) -> list[tuple[str, bool | None, str]]:
    repo = Path(manifest.get("repo", root)).expanduser()
    rows = []
    seen = []
    for inst in manifest["instruments"]:
        if inst["module"] not in seen:
            seen.append(inst["module"])
    for rel in seen:
        path = (root / rel).resolve()
        try:
            rel_to_repo = path.relative_to(repo.resolve())
        except ValueError:
            rows.append((f"P {rel}", False, f"{path} lies outside repo {repo}"))
            continue
        rc, _ = _git(repo, "ls-files", "--error-unmatch", str(rel_to_repo))
        if rc != 0:
            rows.append((f"P {rel}", False,
                         "UNTRACKED — this file produced numbers that cannot be diffed, "
                         "reviewed, or attributed. rigor-standards §Reproducibility: any break "
                         "in the provenance chain is a stage-08 audit failure"))
            continue
        rc, out = _git(repo, "status", "--porcelain", "--", str(rel_to_repo))
        if out:
            rows.append((f"P {rel}", False,
                         f"tracked but DIRTY ({out.splitlines()[0].strip()}) — the numbers on "
                         f"disk were produced by a revision that is not committed"))
        else:
            rc, sha = _git(repo, "log", "-1", "--format=%h", "--", str(rel_to_repo))
            rows.append((f"P {rel}", True, f"tracked, clean, at {sha or '?'}"))
    return rows


def _pluck(doc, pointer: str):
    cur = doc
    for part in pointer.split("."):
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    return cur


def gate_band(manifest: dict, root: Path) -> list[tuple[str, bool | None, str]]:
    rows = []
    for band in manifest.get("bands", []):
        label = f"B {band['id']}"
        results = (root / Path(band["results"]).expanduser()).resolve()
        if not results.exists():
            rows.append((label, None, f"no results yet at {band['results']} (pre-scoring)"))
            continue
        try:
            doc = json.loads(results.read_text())
            val = float(_pluck(doc, band["pointer"]))
        except Exception as exc:
            rows.append((label, False, f"cannot read {band['pointer']}: {type(exc).__name__}: {exc}"))
            continue
        lo, hi = float(band["low"]), float(band["high"])
        where = band.get("declared_at", "UNDECLARED")
        if lo <= val <= hi:
            rows.append((label, True, f"{val:.5f} in [{lo}, {hi}] ({where})"))
        else:
            rows.append((label, False,
                         f"{val:.5f} OUTSIDE [{lo}, {hi}] declared in {where} — mandated defect "
                         f"hunt BEFORE interpretation. Do not interpret this value."))
    return rows


GATES = {
    "O": ("ORIENTATION", gate_orientation),
    "E": ("EQUIVALENCE", gate_equivalence),
    "P": ("PROVENANCE", gate_provenance),
    "B": ("BAND", gate_band),
}


# -------------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("manifest", help="tools/instruments/<slug>.json")
    ap.add_argument("--gates", default="OEPB", help="subset of gate letters (default OEPB)")
    ap.add_argument("--list", action="store_true", help="list instruments, run nothing")
    ap.add_argument("--no-reexec", action="store_true",
                    help="do not honour the manifest's interpreter (debugging only)")
    args = ap.parse_args()

    mpath = Path(args.manifest).expanduser().resolve()
    manifest = json.loads(mpath.read_text())
    root = Path(manifest["root"]).expanduser()

    # Run under the interpreter that actually runs the instruments. Without this, a gate
    # invoked with the wrong python reports FAIL for a missing dependency, and a gate that
    # cries wolf is worse than no gate (tools/README.md).
    interp = manifest.get("interpreter")
    if interp and not args.no_reexec:
        interp = str(Path(interp).expanduser())
        if str(Path(sys.executable).resolve()) != str(Path(interp).resolve()):
            if not Path(interp).exists():
                print(f"[FAIL] manifest interpreter does not exist: {interp}")
                return 1
            import os

            os.execv(interp, [interp, str(Path(__file__).resolve()), *sys.argv[1:]])

    print(f"instrument_check — {manifest.get('slug', mpath.stem)}")
    print(f"  root {root}")
    if not root.exists():
        print(f"\n[FAIL] root does not exist: {root}")
        return 1

    if args.list:
        for inst in manifest["instruments"]:
            tag = "sealed" if inst.get("sealed") else (f"fast-path of {inst['fast_path_of']}"
                                                       if inst.get("fast_path_of") else "")
            print(f"  {inst['id']:<34} {inst['module']}::{inst['function']}  {tag}")
        return 0

    failures = 0
    for letter in args.gates.upper():
        if letter not in GATES:
            print(f"\n[FAIL] unknown gate letter {letter!r}")
            return 1
        name, fn = GATES[letter]
        rows = fn(manifest, root)
        print(f"\n=== {letter}  {name} " + "=" * (52 - len(name)))
        if not rows:
            print("  (none registered)")
            continue
        for label, ok, note in rows:
            mark = "SKIP" if ok is None else ("PASS" if ok else "FAIL")
            print(f"  [{mark}] {label}")
            print(f"         {note}")
            if ok is False:
                failures += 1

    print()
    if failures:
        print(f"RESULT: FAIL — {failures} gate row(s) failed. This blocks scoring, not just review.")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
