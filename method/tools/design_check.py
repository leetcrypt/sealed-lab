#!/usr/bin/env python3
"""design_check — execute a pre-registered design instead of reading its prose.

Rationale: `shared/honesty-assessment-and-solutions.md`.

A pre-registration can assert "CI half-width <= 0.05" with total fluency and be wrong,
because the calculation that produces 0.05 is nowhere in the document. This tool refuses
to accept asserted numbers. It requires a numbers ledger plus a *generative model* and an
*executable decision rule*, then runs the decision rule against synthetic worlds.

Gates
  L  LEDGER      every committed number has provenance; assumptions name a measurement stage
  T  TAUTOLOGY   P(declare H1 | null world) must be <= tautology_max   (a free claim is not science)
  P  POWER       P(declare H1 | effect = MDE) must be >= power_min     (can the study see it?)
  N  NULL        P(reportable null | null world) must be >= null_min   ("nulls are results" must be
                                                                       implementable, not just stated)
  S  SCALE       MDE must not swallow its own baseline (mde/baseline <= scale_max)

Stdlib only, on purpose: this must run for someone with no scientific-python stack.

Usage
  design_check.py <ledger.json>                 run every gate, print report, exit 1 on FAIL
  design_check.py <ledger.json> --ledger-only   print the bare numbers table (prose-blind review)
  design_check.py <ledger.json> --sweep         search candidate thresholds for a passing design
  design_check.py <ledger.json> --trials 4000   Monte-Carlo trials per world (default 2000)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import statistics
import sys
from pathlib import Path

# ---------------------------------------------------------------- shared sampling helpers
# Exposed to design models so every model resamples the *cluster*, never the row.


def beta_binomial_p(rng: random.Random, p: float, icc: float) -> float:
    """Draw a cluster-level rate whose induced intra-cluster correlation is exactly `icc`.

    For a beta-binomial, ICC = 1 / (a + b + 1). Solving for the concentration and splitting
    it by the target mean gives the (a, b) below. icc <= 0 means clusters are identical to
    the grand mean (no cluster-level variance at all).
    """
    if icc <= 0:
        return p
    if icc >= 1:
        return 1.0 if rng.random() < p else 0.0
    conc = 1.0 / icc - 1.0
    a, b = max(p * conc, 1e-9), max((1.0 - p) * conc, 1e-9)
    x = rng.gammavariate(a, 1.0)
    y = rng.gammavariate(b, 1.0)
    return x / (x + y)


def cluster_bootstrap_ci(
    clusters: list[float], conf: float, resamples: int, rng: random.Random
) -> tuple[float, float]:
    """Percentile CI resampling whole clusters (the run is the unit, not the row).

    Deliberately percentile, not BCa: a gate wants a defensible lower bound on interval
    width, and BCa's bias/acceleration correction shifts the interval without materially
    narrowing it. The prereg may still specify BCa for the real analysis.
    """
    if not clusters:
        return (float("nan"), float("nan"))
    n = len(clusters)
    means = []
    for _ in range(resamples):
        means.append(sum(clusters[rng.randrange(n)] for _ in range(n)) / n)
    means.sort()
    lo_i = int((1.0 - conf) / 2.0 * resamples)
    hi_i = min(resamples - 1, int((1.0 + conf) / 2.0 * resamples))
    return (means[lo_i], means[hi_i])


def empirical_threshold(negatives: list[float], fpr: float) -> float:
    """Score threshold achieving `fpr` on the *observed* negatives.

    This is where small negative sets bite: at fpr=1e-2 with 1200 negatives the threshold is
    the 12th-highest score, and that quantile's noise never appears in a bootstrap that
    resamples the positive rate at a threshold treated as fixed. Passing the real negative
    count in makes the instability materialise instead of hiding.
    """
    if not negatives:
        return float("inf")
    s = sorted(negatives, reverse=True)
    k = max(1, int(round(fpr * len(s))))
    return s[k - 1]


def deff(cluster_size: float, icc: float) -> float:
    """Design effect: 1 + (m - 1) * rho. Effective n = n / deff."""
    return 1.0 + (max(cluster_size, 1.0) - 1.0) * max(icc, 0.0)


HELPERS = {
    "beta_binomial_p": beta_binomial_p,
    "cluster_bootstrap_ci": cluster_bootstrap_ci,
    "empirical_threshold": empirical_threshold,
    "deff": deff,
}

# ---------------------------------------------------------------- verdict vocabulary
H1 = "H1"          # the design's directional / non-inferiority claim is asserted
H0 = "H0"          # the reportable null or the opposite-direction result
INCONCLUSIVE = "inconclusive"
VALID = {H1, H0, INCONCLUSIVE}


def load_model(path: Path):
    spec = importlib.util.spec_from_file_location(f"design_model_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"FATAL cannot import design model: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for fn in ("simulate", "decide"):
        if not hasattr(mod, fn):
            raise SystemExit(f"FATAL {path.name} must define {fn}()")
    return mod


def run_world(mod, rq: dict, effect: float, trials: int, seed: int) -> dict:
    """Monte-Carlo the pre-registered decision rule under a fixed true effect."""
    counts = {H1: 0, H0: 0, INCONCLUSIVE: 0}
    widths = []
    for t in range(trials):
        rng = random.Random(seed + t)
        obs = mod.simulate(rq, effect, rng, HELPERS)
        verdict, info = mod.decide(rq, obs, rng, HELPERS)
        if verdict not in VALID:
            raise SystemExit(f"FATAL decide() returned {verdict!r}; must be one of {sorted(VALID)}")
        counts[verdict] += 1
        if info and info.get("ci_halfwidth") is not None:
            widths.append(info["ci_halfwidth"])
    out = {k: v / trials for k, v in counts.items()}
    out["median_ci_halfwidth"] = statistics.median(widths) if widths else None
    return out


# ---------------------------------------------------------------- gates
def gate_ledger(ledger: dict) -> list[tuple[str, bool, str]]:
    """Mechanism A: a number with no provenance is an assertion, not a result."""
    rows = []
    for num in ledger.get("numbers", []):
        name = num.get("name", "<unnamed>")
        src = num.get("source")
        if src == "script":
            script = num.get("script")
            ok = bool(script) and (ledger["_root"] / script).exists()
            rows.append((f"L: {name} = {num.get('value')} provenance",
                         ok,
                         f"script={script}" + ("" if ok else " MISSING — number is asserted")))
        elif src == "assumption":
            ok = bool(num.get("measured_at_stage"))
            rows.append((f"L: {name} = {num.get('value')} assumption",
                         ok,
                         f"measured_at_stage={num.get('measured_at_stage')}"
                         if ok else "no measured_at_stage — unfalsifiable assumption"))
        elif src == "locked-upstream":
            ok = bool(num.get("locked_by"))
            rows.append((f"L: {name} = {num.get('value')} locked",
                         ok, f"locked_by={num.get('locked_by')}" if ok else "no locked_by"))
        else:
            rows.append((f"L: {name} provenance", False,
                         f"source={src!r} not in script|assumption|locked-upstream"))
    return rows


def gate_scale(ledger: dict) -> list[tuple[str, bool, str]]:
    """An MDE comparable to its own baseline cannot see the effect it was built for."""
    rows = []
    cfg = ledger.get("gates", {})
    limit = cfg.get("scale_max", 0.5)
    for rq in ledger.get("rqs", []):
        base = rq.get("baseline_scale")
        mde = rq.get("mde")
        if base in (None, 0) or mde is None:
            continue
        ratio = abs(mde) / abs(base)
        rows.append((f"S: {rq['id']} mde/baseline = {ratio:.2f}",
                     ratio <= limit,
                     f"mde={mde} baseline={base} limit={limit}"
                     + ("" if ratio <= limit else "  <-- MDE swallows the baseline; a real"
                                                  " effect this size would report as 'no difference'")))
    return rows


def gate_retained(ledger: dict) -> list[tuple[str, bool, str]]:
    """`expect_fail` exists to let a design keep a demonstrated counter-example. It is also
    the one field in the whole ledger that could silence an inconvenient gate, so using it
    costs something: name the gates, and say in writing why the RQ was disqualified."""
    rows, valid = [], {"T", "P", "N"}
    for rq in ledger.get("rqs", []):
        letters = rq.get("expect_fail")
        if not letters:
            continue
        rid = rq["id"]
        bad = set(letters) - valid
        rows.append((f"X: {rid} expect_fail={sorted(letters)} names real gates",
                     not bad,
                     "T/P/N" if not bad else f"  <-- unknown gate letters {sorted(bad)}"))
        why = (rq.get("rejected_because") or "").strip()
        rows.append((f"X: {rid} declares why it was disqualified", bool(why),
                     f"rejected_because={why!r}" if why else
                     "  <-- expect_fail without rejected_because is a silenced gate, not a"
                     " demonstration; state the defect this RQ exists to exhibit"))
    return rows


def gate_simulated(ledger: dict, mod, trials: int) -> tuple[list, dict]:
    rows, detail = [], {}
    cfg = ledger.get("gates", {})
    taut_max = cfg.get("tautology_max", 0.20)
    power_min = cfg.get("power_min", 0.80)
    null_min = cfg.get("null_min", 0.80)
    seed = ledger.get("seed", 20260724)

    for rq in ledger.get("rqs", []):
        rid = rq["id"]
        null_eff = rq["null_effect"]
        alt_eff = rq["alt_effect"]

        # A design may retain a disqualified RQ so that its defect is demonstrated
        # numerically rather than argued in prose. Such an RQ can never pass, which
        # without this marker makes PASS unreachable for a correct design — and a gate
        # that cannot be satisfied teaches people to click through FAIL, which is the
        # exact failure mode rigor-standards.md forbids. So: name the gates expected to
        # fail, and the expected failure becomes a positive test. If a retained
        # counter-example stops failing, its demonstration is void and that IS a real
        # failure.
        expect_fail = set(rq.get("expect_fail") or [])

        def expected(letter: str, label: str, ok: bool, note: str):
            if letter not in expect_fail:
                return (label, ok, note)
            if not ok:
                return (f"{label}   [EXPECTED FAIL — verified]", True,
                        "retained to demonstrate the defect; the failure IS the test")
            return (f"{label}   [EXPECTED FAIL — BUT DID NOT FAIL]", False,
                    "  <-- the retained counter-example no longer demonstrates its defect,"
                    " so the demonstration it exists to provide is void")

        w_null = run_world(mod, rq, null_eff, trials, seed)
        w_alt = run_world(mod, rq, alt_eff, trials, seed + 10_000)
        detail[rid] = {"null_world": w_null, "alt_world": w_alt}

        # The N gate asks "can this design deliver its reportable null?" For a
        # non-inferiority test the null world sits exactly ON the margin, where an
        # H0 verdict is legitimately ambiguous — so such RQs declare a separate,
        # unambiguously-worse world (e.g. 2*delta) to be detected.
        w_h0 = w_null
        if rq.get("null_verdict_effect") is not None:
            w_h0 = run_world(mod, rq, rq["null_verdict_effect"], trials, seed + 20_000)
            detail[rid]["h0_world"] = w_h0

        p_taut = w_null[H1]
        rows.append(expected(
            "T", f"T: {rid} P(H1 | null world, effect={null_eff}) = {p_taut:.3f}",
            p_taut <= taut_max,
            f"limit <= {taut_max}"
            + ("" if p_taut <= taut_max else
               "  <-- TAUTOLOGY/LIBERAL: the claim is asserted even when it is false")))

        p_pow = w_alt[H1]
        rows.append(expected(
            "P", f"P: {rid} P(H1 | effect={alt_eff}) = {p_pow:.3f}",
            p_pow >= power_min,
            f"limit >= {power_min}"
            + ("" if p_pow >= power_min else
               "  <-- UNDERPOWERED: the study cannot see what it was built to see")))

        h0_eff = rq.get("null_verdict_effect", null_eff)
        p_null = w_h0[H0]
        rows.append(expected(
            "N", f"N: {rid} P(reportable null | effect={h0_eff}) = {p_null:.3f}",
            p_null >= null_min,
            f"limit >= {null_min}"
            + ("" if p_null >= null_min else
               "  <-- cannot deliver its own null; 'nulls are results' is unimplementable"
               f" here (P(inconclusive)={w_h0[INCONCLUSIVE]:.3f})")))

        hw = w_alt["median_ci_halfwidth"]
        if hw is not None and rq.get("claimed_ci_halfwidth") is not None:
            claimed = rq["claimed_ci_halfwidth"]
            ok = hw <= claimed * 1.10
            rows.append((f"L: {rid} simulated CI half-width = {hw:.4f} vs claimed {claimed}",
                         ok,
                         "within 10% of the prereg claim" if ok else
                         f"  <-- the prereg overstates its precision by {hw / claimed:.2f}x"))
    return rows, detail


# ---------------------------------------------------------------- reporting
def print_ledger(ledger: dict) -> None:
    """Mechanism C: the bare table, no narrative. Adjacency is the detector."""
    print("NUMBERS LEDGER —", ledger.get("slug", "?"), "(prose withheld by design)\n")
    hdr = f"{'construct':<34}{'value':>14}  {'source':<16}{'compared against'}"
    print(hdr)
    print("-" * len(hdr))
    for n in ledger.get("numbers", []):
        print(f"{n.get('name','?'):<34}{str(n.get('value')):>14}  "
              f"{str(n.get('source')):<16}{n.get('compared_against','—')}")
    print("\nretraction conditions")
    print("-" * 21)
    for n in ledger.get("numbers", []):
        if n.get("retraction_condition"):
            print(f"  {n['name']}: {n['retraction_condition']}")
    print("\nassumptions pending measurement")
    print("-" * 31)
    pending = [n for n in ledger.get("numbers", []) if n.get("source") == "assumption"]
    if not pending:
        print("  (none)")
    for n in pending:
        print(f"  {n['name']} = {n.get('value')}  -> measure at stage "
              f"{n.get('measured_at_stage','UNDECLARED')}")


def sweep(ledger: dict, mod, trials: int) -> None:
    """Hand the designer the defensible numbers instead of letting them be asserted."""
    cfg = ledger.get("gates", {})
    taut_max, power_min = cfg.get("tautology_max", 0.20), cfg.get("power_min", 0.80)
    seed = ledger.get("seed", 20260724)
    print("SWEEP — candidate designs that pass T and P\n")
    for rq in ledger.get("rqs", []):
        grids = rq.get("sweep") or []
        if isinstance(grids, dict):
            grids = [grids]
        for grid in grids:
            key, values = grid["param"], grid["values"]
            print(f"{rq['id']}  sweeping {key}"
                  + (f"   ({grid['note']})" if grid.get("note") else ""))
            print(f"  {key:>12} {'P(H1|null)':>12} {'P(H1|alt)':>12} {'P(null-verdict)':>17}"
                  "  verdict")
            for v in values:
                trial_rq = dict(rq)
                trial_rq[key] = v
                wn = run_world(mod, trial_rq, trial_rq["null_effect"], trials, seed)
                wa = run_world(mod, trial_rq, trial_rq["alt_effect"], trials, seed + 10_000)
                h0_eff = trial_rq.get("null_verdict_effect", trial_rq["null_effect"])
                wh = (wn if h0_eff == trial_rq["null_effect"]
                      else run_world(mod, trial_rq, h0_eff, trials, seed + 20_000))
                ok = wn[H1] <= taut_max and wa[H1] >= power_min
                print(f"  {str(v):>12} {wn[H1]:>12.3f} {wa[H1]:>12.3f} {wh[H0]:>17.3f}"
                      f"  {'PASS' if ok else 'fail'}")
            print()


def main() -> int:
    ap = argparse.ArgumentParser(description="Execute a design instead of reading its prose.")
    ap.add_argument("ledger", type=Path)
    ap.add_argument("--trials", type=int, default=2000)
    ap.add_argument("--ledger-only", action="store_true",
                    help="print the bare numbers table (prose-blind arithmetic review)")
    ap.add_argument("--sweep", action="store_true",
                    help="search candidate thresholds for a design that passes T and P")
    args = ap.parse_args()

    ledger = json.loads(args.ledger.read_text())
    ledger["_root"] = args.ledger.parent

    if args.ledger_only:
        print_ledger(ledger)
        return 0

    model_path = ledger["_root"] / ledger["model"]
    mod = load_model(model_path)

    if args.sweep:
        sweep(ledger, mod, args.trials)
        return 0

    print("=" * 78)
    print(f"DESIGN CHECK — {ledger.get('slug')}   model={ledger['model']}   trials={args.trials}")
    print("=" * 78)
    print_ledger(ledger)

    rows = gate_ledger(ledger) + gate_scale(ledger) + gate_retained(ledger)
    sim_rows, detail = gate_simulated(ledger, mod, args.trials)
    rows += sim_rows

    print("\n" + "=" * 78)
    print("GATES")
    print("=" * 78)
    for label, ok, note in rows:
        print(f"[{'PASS' if ok else 'FAIL'}] {label}\n        {note}")

    print("\n" + "=" * 78)
    print("OUTCOME DISTRIBUTIONS (the pre-registered decision rule, executed)")
    print("=" * 78)
    for rid, d in detail.items():
        for world, res in d.items():
            print(f"  {rid:<10} {world:<10} "
                  + "  ".join(f"{k}={res[k]:.3f}" for k in (H1, H0, INCONCLUSIVE)))

    retained = [(rq["id"], sorted(rq["expect_fail"]), rq.get("rejected_because", "—"))
                for rq in ledger.get("rqs", []) if rq.get("expect_fail")]
    if retained:
        print("\n" + "=" * 78)
        print("RETAINED COUNTER-EXAMPLES (excluded from the verdict — read them anyway)")
        print("=" * 78)
        print("Each RQ below is REQUIRED to fail the named gates. Its failure is a positive")
        print("test, not a blemish. If one ever stops failing, that is a real FAIL. This")
        print("section is printed unconditionally so a silenced gate cannot be a quiet one.")
        for rid, letters, why in retained:
            print(f"  {rid}  expect_fail={letters}\n      because: {why}")

    failed = [label for label, ok, _ in rows if not ok]
    print("\n" + "=" * 78)
    if failed:
        print(f"VERDICT: FAIL — {len(failed)} of {len(rows)} gates")
        print("This design must not be frozen. Failing gates:")
        for f in failed:
            print(f"  - {f}")
        print("=" * 78)
        return 1
    verified = sum(1 for label, _, _ in rows if "[EXPECTED FAIL — verified]" in label)
    print(f"VERDICT: PASS — {len(rows)} gates"
          + (f" ({verified} expected failures verified)" if verified else ""))
    print("Gates passing is necessary, NOT sufficient: a simulation is only as honest as its")
    print("generative model. Every 'assumption' above must be measured at the declared stage and")
    print("this check re-run with the measured value (honesty-assessment-and-solutions.md §6).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
