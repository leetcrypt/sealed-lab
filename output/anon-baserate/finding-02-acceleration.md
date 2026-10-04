# Finding-02 — acceleration: gates-ON vs gates-OFF (challenge criterion 3, 20%)

Each injected defect is drawn from the SOR program's REAL history, so the A/B measures the
lab against defects that actually occurred, not invented ones.

| injected defect | gate | gates ON | gates OFF |
|---|---|---|---|
| inverted correlator (real D-2 AUC inversion) | instrument_check | **BLOCKED** | slips through |
| underpowered design (CI cannot conclude) | design_check | **BLOCKED** | slips through |
| tampered pre-registration (silent post-seal edit) | verify_seals | **BLOCKED** | slips through |

| metric | gates OFF | gates ON |
|---|---|---|
| defects caught before data collection | 0 / 3 | **3 / 3** |
| false findings reaching output | 3 | **0** |
| human re-verification events required | 3 | **0** |
| legitimate work falsely blocked (control) | — | **0 / 3** |

**The bottleneck we attack is verification, not generation.** Without gates, every defect
produces a plausible-but-false finding that a human must later catch and rework — the
verification tax that caps autonomous-science throughput. The gates move verification BEFORE
data collection, so trustworthy output needs no human recheck. The honest headline is
**verified results per hour, not raw outputs per hour.** This is a 1.x–Nx acceleration whose
exact multiplier scales with how many defects a real campaign would otherwise emit; here,
3/3 false findings prevented at zero cost to legitimate throughput.

Evidence: `ab-gates-result.txt` / `.json`; defects in `experiment/defects/`.
