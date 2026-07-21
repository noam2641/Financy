# RELEASE 0 — FILE AND MODULE CONTRACT (FC-R0)

*documentation-only; canonical v4.6 unmodified; governed by v5 §0 + readiness-gate slices R0-S1..S6; shared ID space per PHASE4_FOUNDATION.*

This contract is a **Markdown deliverable only**. It creates **no code, no `src/`, and no `tests/` directories**. Every planned module, path, function, and entity below is described **logically** and reuses the IDs of `PHASE4_FOUNDATION.md` **verbatim**. Planned package root `financy/` is logical only. The v5 §0.1 two-field status model is normative throughout: `decision_status ∈ {OWNER_APPROVED, EMPIRICAL_TBD, DEFERRED, REJECTED}` and `implementation_posture ∈ {BINDING, PROVISIONAL_DEFAULT, CHALLENGER, NOT_IN_SCOPE}`. A working default = `(EMPIRICAL_TBD, PROVISIONAL_DEFAULT)` and is never described as a final owner-selected component; replaceability is preserved. Autonomous AI authority = `(REJECTED, NOT_IN_SCOPE)` and is out of R0 scope entirely.

ADR references below anchor to the ratified owner decision recorded in the cited v5 §0.x clause; the foundation does not enumerate standalone ADR IDs, so no new ADR IDs are invented here.

---

## 1. Module map

21 files: `FC-R0-01 .. FC-R0-21`. Each has exactly one coherent single responsibility (no arbitrary fragmentation). Determinism classes follow the foundation: **BIT_EXACT** for symbolic artifacts (raw data, canonical schema, corp-action store, cohort manifest, labels, fold manifest, feature-values checksum, trial registry, run ledger, calendar, environment hash, identity map); **TOLERANCE_NUMERIC** for fitted model / calibration / attribution / statistical / benchmark / cost artifacts reproduced within an approved tolerance.

### 1.1 Shared core (slice-independent foundation)

| FC id | Path | Slice | Single responsibility | Public FNs | Writes ENT | Reads ENT | Upstream FC | Downstream FC | Determinism | Status (decision · posture) | v5 refs | v4.6 REQ | ADR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FC-R0-01 | `financy/core/time.py` | shared core | Exchange-session calendar + deterministic session counting (entry-index convention pinned) | FN-R0-12 | — | — | — | FC-R0-10, FC-R0-12 | BIT_EXACT | OWNER_APPROVED · BINDING | §0 | R0-REQ-18, R0-REQ-12 | §0 owner decision (calendar convention) |
| FC-R0-02 | `financy/core/entities.py` | shared core | Canonical typed schemas for the 21 R0 entities (ENT-R0-01..21); no runtime writers | — (schema defs) | — | — | — | all FC | BIT_EXACT | OWNER_APPROVED · BINDING | §0.1 | R0-REQ-04, R0-REQ-13, R0-REQ-21 | §0.1 status-model decision |
| FC-R0-03 | `financy/core/determinism.py` | shared core | `environment_hash`, seeding, two-tier reproducibility helpers | FN-R0-30 | ENT-R0-21 | ENT-R0-02 | FC-R0-02 | FC-R0-21 (+ all runs) | BIT_EXACT | OWNER_APPROVED · BINDING | §0 (RPT-R0-05) | R0-REQ-36 | §0 reproducibility decision |
| FC-R0-04 | `financy/core/ledger.py` | shared core | Append-only run ledger | FN-R0-31 | ENT-R0-20 | — | FC-R0-02 | FC-R0-21 (+ all runs) | BIT_EXACT | OWNER_APPROVED · BINDING | §0 (RPT-R0-06) | R0-REQ-39 | §0 evidence decision |

### 1.2 Slice modules (R0-S1..S6)

| FC id | Path | Slice | Single responsibility | Public FNs | Writes ENT | Reads ENT | Upstream FC | Downstream FC | Determinism | Status (decision · posture) | v5 refs | v4.6 REQ | ADR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FC-R0-05 | `financy/io/provider_adapter.py` | R0-S1 | Provider adapter + raw OHLCV normalization to canonical (raw-basis only, `auto_adjust=False`) | FN-R0-01, FN-R0-02, FN-R0-03 | ENT-R0-01, ENT-R0-02 | — | FC-R0-02 | FC-R0-06, FC-R0-07, FC-R0-08, FC-R0-09, FC-R0-11, FC-R0-20 | BIT_EXACT | OWNER_APPROVED · BINDING | §0 | R0-REQ-01, R0-REQ-02, R0-REQ-03, R0-REQ-04 | §0 raw-basis decision |
| FC-R0-06 | `financy/corpactions/store.py` | R0-S2 | Versioned corporate-action store (append-only, versioned) | FN-R0-04 | ENT-R0-03 | ENT-R0-01 | FC-R0-02, FC-R0-05 | FC-R0-07 | BIT_EXACT | OWNER_APPROVED · BINDING | §0.6 | R0-REQ-05 | §0.6 corp-action decision |
| FC-R0-07 | `financy/corpactions/asof.py` | R0-S2 | As-of adjustment factor + split-safe simple returns + derived adjusted series | FN-R0-05, FN-R0-06, FN-R0-07 | ENT-R0-04 | ENT-R0-02, ENT-R0-03 | FC-R0-02, FC-R0-05, FC-R0-06 | FC-R0-10, FC-R0-11, FC-R0-19, FC-R0-20 | BIT_EXACT | OWNER_APPROVED · BINDING | §0.6a–e | R0-REQ-06, R0-REQ-07, R0-REQ-08, R0-REQ-09, R0-REQ-10, R0-REQ-11, R0-REQ-12 | §0.6a–e split-exception decision |
| FC-R0-08 | `financy/universe/fixed_pit_cohort.py` | R0-S3 | FIXED_PIT_COHORT construction (immutable signed manifest; then-delisted retained, later-IPO excluded) | FN-R0-08 | ENT-R0-07 | ENT-R0-01, ENT-R0-05 | FC-R0-02, FC-R0-05, FC-R0-09 | FC-R0-10 | BIT_EXACT | OWNER_APPROVED · BINDING | §0.4 | R0-REQ-13, R0-REQ-14, R0-REQ-17 | §0.4 cohort decision |
| FC-R0-09 | `financy/identity/instrument_master.py` | R0-S3 | Opaque `instrument_id` + identifier history + terminal-event records (ticker-only join rejected; ticker-reuse → 2 ids) | FN-R0-09, FN-R0-10, FN-R0-11 | ENT-R0-05, ENT-R0-06, ENT-R0-08 | ENT-R0-01, ENT-R0-02 | FC-R0-02, FC-R0-05 | FC-R0-08, FC-R0-10 | BIT_EXACT | OWNER_APPROVED · BINDING | §0 | R0-REQ-15, R0-REQ-16 | §0 identity decision |
| FC-R0-10 | `financy/labels/fixed_horizon.py` | R0-S4 | Pure 5/8/14-session fixed-horizon labels + `label_available_at` (traded-return exit) | FN-R0-13, FN-R0-14 | ENT-R0-09 | ENT-R0-04, ENT-R0-07, ENT-R0-08 | FC-R0-01, FC-R0-07, FC-R0-08, FC-R0-09 | FC-R0-12, FC-R0-14, FC-R0-15, FC-R0-16 | BIT_EXACT | OWNER_APPROVED · BINDING | §0.6c | R0-REQ-16, R0-REQ-18, R0-REQ-19, R0-REQ-20, R0-REQ-12 | §0.6c label-adjustment decision |
| FC-R0-11 | `financy/features/snapshot.py` | R0-S5 | `feature_snapshot` schema-hash + values-checksum + fit-isolation of scalers/imputers/calibrators/meta-learners | FN-R0-15, FN-R0-16 | ENT-R0-10 | ENT-R0-02, ENT-R0-04 | FC-R0-02, FC-R0-05, FC-R0-07 | FC-R0-12, FC-R0-14, FC-R0-15 | BIT_EXACT | OWNER_APPROVED · BINDING | §0 | R0-REQ-21, R0-REQ-22, R0-REQ-28 | §0 fit-isolation decision |
| FC-R0-12 | `financy/validation/splitter.py` | R0-S5 | Information intervals + interval-based purged walk-forward split + embargo + no-overlap assertion | FN-R0-17, FN-R0-18, FN-R0-19 | ENT-R0-11, ENT-R0-12 | ENT-R0-09, ENT-R0-10 | FC-R0-01, FC-R0-10, FC-R0-11 | FC-R0-14, FC-R0-15, FC-R0-16 | BIT_EXACT | OWNER_APPROVED · BINDING | §0.5 | R0-REQ-23, R0-REQ-24, R0-REQ-25, R0-REQ-26 | §0.5 interval/embargo decision |
| FC-R0-13 | `financy/registry/trial_registry.py` | R0-S5 | Append-only trial registry (every config a logged trial) | FN-R0-20 | ENT-R0-13 | — | FC-R0-02, FC-R0-03 | FC-R0-17 | BIT_EXACT | OWNER_APPROVED · BINDING | §0 (VAL-R0-04) | R0-REQ-27 | §0 trial-registry decision |
| FC-R0-14 | `financy/models/baseline.py` | R0-S6 | GBT baseline forecast of `expected_absolute_executable_return_bps` (primary learned predictor) | FN-R0-21 | ENT-R0-14 | ENT-R0-09, ENT-R0-10, ENT-R0-12 | FC-R0-10, FC-R0-11, FC-R0-12 | FC-R0-16, FC-R0-17, FC-R0-18, FC-R0-21 | TOLERANCE_NUMERIC | EMPIRICAL_TBD · PROVISIONAL_DEFAULT | §0 (MDL-R0-01, MDL-R0-02) | R0-REQ-29 | MDL-R0-02 provisional-default decision |
| FC-R0-15 | `financy/models/comparator.py` | R0-S6 | Pooled historical-panel elastic-net comparator (+ Fama-MacBeth diagnostic; per-date-oracle guard) | FN-R0-22 | ENT-R0-14 | ENT-R0-09, ENT-R0-10, ENT-R0-12 | FC-R0-10, FC-R0-11, FC-R0-12 | FC-R0-16, FC-R0-21 | TOLERANCE_NUMERIC | EMPIRICAL_TBD · PROVISIONAL_DEFAULT | §0 (MDL-R0-03, MDL-R0-04, MDL-R0-05) | R0-REQ-30 | MDL-R0-03/05 comparator & oracle-prohibition decision |
| FC-R0-16 | `financy/calibration/regression_calibration.py` | R0-S6 | Output-specific regression calibration + conformal/CQR intervals (ECE=NOT_APPLICABLE_TO_PRIMARY_REGRESSION) | FN-R0-23 | ENT-R0-15 | ENT-R0-09, ENT-R0-12, ENT-R0-14 | FC-R0-12, FC-R0-14, FC-R0-15 | FC-R0-21 | TOLERANCE_NUMERIC | EMPIRICAL_TBD · PROVISIONAL_DEFAULT | §0 (MDL-R0-06, MDL-R0-07, MDL-R0-08) | R0-REQ-31 | MDL-R0-06/07 calibration & ECE decision |
| FC-R0-17 | `financy/stats/multiple_testing.py` | R0-S6 | Effective-sample IC/IR + `applicable_multiple_testing_adjusted_hurdle` + DSR/PBO/CPCV applicability | FN-R0-24, FN-R0-25 | — (feeds ENT-R0-19 via FC-R0-21) | ENT-R0-13, ENT-R0-14 | FC-R0-13, FC-R0-14 | FC-R0-21 | TOLERANCE_NUMERIC | OWNER_APPROVED · BINDING | §0 (VAL-R0-04, VAL-R0-05, VAL-R0-06) | R0-REQ-32, R0-REQ-38 | §0 multiple-testing decision |
| FC-R0-18 | `financy/attribution/factor_attribution.py` | R0-S6 | Contract-bound factor attribution (§0.8 13-element table; dependence-aware SEs) | FN-R0-26 | ENT-R0-18 | ENT-R0-14, ENT-R0-16, ENT-R0-17 | FC-R0-14, FC-R0-19, FC-R0-20 | FC-R0-21 | TOLERANCE_NUMERIC | OWNER_APPROVED · BINDING | §0.8 (RPT-R0-02) | R0-REQ-33 | §0.8 attribution-contract decision |
| FC-R0-19 | `financy/benchmark/investable_benchmark.py` | R0-S6 | SPY + matched-basket investable benchmark (beta-adjusted, net of same cost model) | FN-R0-27 | ENT-R0-16 | ENT-R0-04, ENT-R0-17 | FC-R0-07, FC-R0-20 | FC-R0-18, FC-R0-21 | TOLERANCE_NUMERIC | OWNER_APPROVED · BINDING | §0 (RPT-R0-03) | R0-REQ-34 | §0 benchmark decision |
| FC-R0-20 | `financy/cost/round_trip_cost.py` | R0-S6 | Round-trip cost model (exit/close-auction leg, √impact) | FN-R0-28 | ENT-R0-17 | ENT-R0-02, ENT-R0-04 | FC-R0-02, FC-R0-05, FC-R0-07 | FC-R0-18, FC-R0-19, FC-R0-21 | TOLERANCE_NUMERIC | OWNER_APPROVED · BINDING | §0 | R0-REQ-35 | §0 cost-model decision |
| FC-R0-21 | `financy/report/evaluation_report.py` | R0-S6 | Reproducible evaluation report + BLOCKED_NO_EDGE terminal outcome (two-tier repro evidence) | FN-R0-29 | ENT-R0-19 | ENT-R0-14, ENT-R0-15, ENT-R0-16, ENT-R0-17, ENT-R0-18, ENT-R0-20 | FC-R0-03, FC-R0-16, FC-R0-17, FC-R0-18, FC-R0-19 | — (terminal) | TOLERANCE_NUMERIC (BIT_EXACT symbolic fields + TOLERANCE_NUMERIC embedded metrics) | OWNER_APPROVED · BINDING | §0 (RPT-R0-01/04/05/07) | R0-REQ-37, R0-REQ-40 | §0 pre-registration & BLOCKED_NO_EDGE decision |

**Entity-writer coverage:** ENT-R0-01..21 each have a writer above (ENT-R0-01/02 ← FC-R0-05; 03 ← FC-R0-06; 04 ← FC-R0-07; 05/06/08 ← FC-R0-09; 07 ← FC-R0-08; 09 ← FC-R0-10; 10 ← FC-R0-11; 11/12 ← FC-R0-12; 13 ← FC-R0-13; 14 ← FC-R0-14 **and** FC-R0-15; 15 ← FC-R0-16; 16 ← FC-R0-19; 17 ← FC-R0-20; 18 ← FC-R0-18; 19 ← FC-R0-21; 20 ← FC-R0-04; 21 ← FC-R0-03). **Function coverage:** FN-R0-01..31 are each assigned to exactly one file above.

---

## 2. Dependency ordering (module DAG, no cycles)

Edges point from **upstream → downstream** (a module depends on every module listed as its upstream). Layers are topologically ordered; every edge goes strictly left-to-right / top-to-bottom, so the graph is acyclic.

```
Layer 0 (no upstream):        FC-R0-01 time        FC-R0-02 entities
Layer 1 (← entities/hash):    FC-R0-03 determinism   FC-R0-04 ledger   FC-R0-05 provider_adapter
Layer 2 (S2):                 FC-R0-06 store        FC-R0-07 asof
Layer 3 (S3):                 FC-R0-09 identity  →  FC-R0-08 universe
Layer 4 (S4):                 FC-R0-10 labels
Layer 5 (S5):                 FC-R0-11 features   FC-R0-12 validation   FC-R0-13 registry
Layer 6 (S6 models):          FC-R0-14 baseline    FC-R0-15 comparator
Layer 7 (S6 downstream):      FC-R0-20 cost → FC-R0-19 benchmark → FC-R0-18 attribution
                              FC-R0-16 calibration   FC-R0-17 stats
Layer 8 (terminal):           FC-R0-21 report
```

Adjacency (upstream → downstream) confirming acyclicity:

| FC | Depends on (upstream) |
|---|---|
| FC-R0-01 | — |
| FC-R0-02 | — |
| FC-R0-03 | FC-R0-02 |
| FC-R0-04 | FC-R0-02 |
| FC-R0-05 | FC-R0-02 |
| FC-R0-06 | FC-R0-02, FC-R0-05 |
| FC-R0-07 | FC-R0-02, FC-R0-05, FC-R0-06 |
| FC-R0-08 | FC-R0-02, FC-R0-05, FC-R0-09 |
| FC-R0-09 | FC-R0-02, FC-R0-05 |
| FC-R0-10 | FC-R0-01, FC-R0-07, FC-R0-08, FC-R0-09 |
| FC-R0-11 | FC-R0-02, FC-R0-05, FC-R0-07 |
| FC-R0-12 | FC-R0-01, FC-R0-10, FC-R0-11 |
| FC-R0-13 | FC-R0-02, FC-R0-03 |
| FC-R0-14 | FC-R0-10, FC-R0-11, FC-R0-12 |
| FC-R0-15 | FC-R0-10, FC-R0-11, FC-R0-12 |
| FC-R0-16 | FC-R0-12, FC-R0-14, FC-R0-15 |
| FC-R0-17 | FC-R0-13, FC-R0-14 |
| FC-R0-18 | FC-R0-14, FC-R0-19, FC-R0-20 |
| FC-R0-19 | FC-R0-07, FC-R0-20 |
| FC-R0-20 | FC-R0-02, FC-R0-05, FC-R0-07 |
| FC-R0-21 | FC-R0-03, FC-R0-16, FC-R0-17, FC-R0-18, FC-R0-19 |

**Cycle check:** every edge increases layer index; there is no back-edge. The graph is a DAG. This is consistent with the foundation task graph (TASK-R0-01..16), whose first node `FC-R0-01` (via TASK-R0-01) is single-session-sized with no unmet dependencies.

---

## 3. Boundaries — explicitly OUT of R0 at the module level

No R0 module is defined for any of the following. Each maps to `decision_status = REJECTED or DEFERRED` with `implementation_posture = NOT_IN_SCOPE`; none appear anywhere in the module map, DAG, or slice mapping above.

| Excluded capability | R0 module? | Posture |
|---|---|---|
| News / event ingestion & NLP | none | NOT_IN_SCOPE |
| Graph / relationship modeling | none | NOT_IN_SCOPE |
| LLM-based components | none | NOT_IN_SCOPE |
| Deep-learning models | none | NOT_IN_SCOPE (GBT baseline is the primary learned predictor; a deep-learning model is only a future CHALLENGER, not R0) |
| Paper-trading / live execution | none | NOT_IN_SCOPE |
| Counterfactual reasoning | none | NOT_IN_SCOPE |
| World-model / autonomous AI authority | none | REJECTED · NOT_IN_SCOPE (per §0.1) |

R0 remains a **modular monolith** confined to data integrity, PIT-correct labeling/features, leakage-safe validation, a GBT baseline + pooled elastic-net comparator, calibration, honest statistics, attribution, investable benchmark, cost, and a reproducible evaluation report.

---

## 4. Slice → FC mapping

| Slice | Scope | FC ids |
|---|---|---|
| shared core | slice-independent foundation | FC-R0-01, FC-R0-02, FC-R0-03, FC-R0-04 |
| R0-S1 | provider adapter + raw normalization | FC-R0-05 |
| R0-S2 | corporate actions store + as-of/split-safe | FC-R0-06, FC-R0-07 |
| R0-S3 | fixed-PIT cohort + instrument identity/terminal events | FC-R0-08, FC-R0-09 |
| R0-S4 | fixed-horizon labels | FC-R0-10 |
| R0-S5 | features + validation splitter + trial registry | FC-R0-11, FC-R0-12, FC-R0-13 |
| R0-S6 | models, calibration, stats, attribution, benchmark, cost, report | FC-R0-14, FC-R0-15, FC-R0-16, FC-R0-17, FC-R0-18, FC-R0-19, FC-R0-20, FC-R0-21 |

All 21 files are covered exactly once across the seven rows.

---

## 5. Notes on determinism & status consistency

- FN-R0-12 (`count_exchange_sessions`) is authored in **FC-R0-01 (shared core / time)**, not in the S4 label file, even though S4 is its primary consumer — matching the foundation, which lists it under S4 functions but places the module first in the task graph (TASK-R0-01) as the tiny, pure, no-upstream seed.
- Only FC-R0-14, FC-R0-15, FC-R0-16 carry `(EMPIRICAL_TBD, PROVISIONAL_DEFAULT)`; they are challenger-replaceable and never described as final owner-selected components. All symbolic/infrastructure files carry `(OWNER_APPROVED, BINDING)`.
- FC-R0-17 owns no entity of its own; its outputs (effective-sample statistics + hurdle) are recorded into ENT-R0-19 by FC-R0-21.
