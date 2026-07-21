# Release-0 Implementation Readiness Gate (Phase 3)

**Status:** documentation-only. Defines exactly what is ready to implement, what remains empirical, and the first six Release-0 (Edge Probe) slices with contracts/tests/Definition-of-Done. **No code is written here.** Basis: ratified Owner Decisions (Round 1) + `AI_TRADING_SYSTEM_ARCHITECTURE_V5_DRAFT.md`.

**Status-model note (Phase 3.1).** Readiness statuses use the two-field model of v5 §0.1: `decision_status ∈ {OWNER_APPROVED, EMPIRICAL_TBD, DEFERRED, REJECTED}` and `implementation_posture ∈ {BINDING, PROVISIONAL_DEFAULT, CHALLENGER, NOT_IN_SCOPE}`. "Working default" everywhere below means `(EMPIRICAL_TBD, PROVISIONAL_DEFAULT)` — implementable now, but not a final owner-selected component; contracts must preserve replaceability. The precision corrections in v5 §0.2–§0.8 are authoritative and govern the slice contracts below.

---

## A. What MAY be implemented immediately (Release-0 Edge Probe)
All six slices below are ready on the ratified decisions: raw-basis prices (ADR-006), PIT survivorship-safe universe (ADR-008), absolute-executable primary target (ADR-003/004), the validation methodology (ADR-001/013), the GBT baseline (ADR-010, working default), INFORMATION_THEORETIC replay on prototyping data (ADR-007). **No owner decision blocks starting R0 implementation.**

## B. Decisions that remain EMPIRICAL_TBD (do NOT block implementation)
| Item | v5 ref | Blocks | Provisional default while open |
| --- | --- | --- | --- |
| Edge effect-size band + acceptance hurdles | V1.4/V7.5 | acceptance, final_holdout | assume no edge; conservative literature band |
| Cost/capacity/ADV/spread caps | V10.3/V11.3 | R1A sizing accept, paper | conservative literature bands; liquid universe |
| SIC sector usability | V6.4 | nothing in R0 (sector non-gating) | no gating sector target |
| Numeric acceptance thresholds (ECE/drawdown/…) | V7.5 | acceptance, final_holdout | external-prior seeds, signed |
| Learned-aggregator value | V9.3 | nothing in R0/MVP | deterministic policy |
| AI/LLM analysis-layer value | V13.3 | nothing in R0 | templated explanations only |

## C. Blocking classification
- **Blocks IMPLEMENTATION (must resolve to build):** none for R0 among decisions. One **data-acquisition prerequisite** for slice R0-S3: a survivorship-safe PIT constituent/delisting source must be identified (candidates: paid EODHD/Norgate, or a manually enumerated fixed PIT list). This is a sourcing task, not an owner decision; until met, S3's DoD ("contains then-delisted names") cannot be certified.
- **Blocks only ACCEPTANCE or HOLDOUT (not build):** all frozen numeric thresholds (edge hurdle, ECE, drawdown, cost/capacity caps) — they must be frozen from external priors before final-holdout access (V7.5/V1.4), but implementation and research folds proceed without them.
- **Blocks nothing now (deferred):** sector taxonomy signal (EMPIRICAL, non-gating), learned aggregation, AI value, R1A entities.

## D. First six implementation slices (Edge Probe)

Each slice: **Contracts required** (to be authored in Phase 4, not now) · **Tests required** · **Definition of Done (DoD)**.

### R0-S1 — Provider adapter & canonical raw OHLCV normalization
- **Contracts:** OHLCV adapter (raw-basis, MultiIndex flatten → 1-D numeric series, provider-symbol mapping, source_record lineage, duplicate/unsorted/mixed-timezone handling). Refs V5.1, C-04/C-06 (ADR-006/007).
- **Tests:** flat single-instrument & provider-MultiIndex fixtures; missing OHLCV field; non-numeric column; duplicate timestamp (reject); unsorted index; mixed timezone; **raw-basis (`auto_adjust=False`)**; header normalization; stable output schema; source lineage present.
- **DoD:** downstream code receives only 1-D numeric series in one canonical raw schema; all fixtures pass; deterministic; no back-adjusted data emitted.

### R0-S2 — Corporate-action store + as-of adjustment + `price_basis`
- **Contracts:** versioned corporate-action record; as-of adjustment function (`ex_date ≤ cutoff`, `corporate_action_version`, `split_adjustment_factor`); `price_basis`/`dividend_treatment` declaration. Corporate-action precision per v5 §0.6 is binding. Refs V5.1–V5.3, §0.6 (ADR-006).
- **Tests (per v5 §0.6 clauses a–e):** (a) split-only constant back-adjustment leaves a **simple return unchanged only when both endpoints are on the same side of the split**; (b) a **raw-price return spanning a split is rejected** without split handling; (c) a **label spanning a split uses the declared as-of split adjustment**; (d) **dividends require an explicit `dividend_treatment`** and do **not** inherit the split exception; (e) **price levels, filters, universe rules, support/resistance, and dollar volume never inherit** the simple-return exception (current-vintage back-adjusted rejected for all of them); `price_basis` present on labels & analytical series; re-pull idempotency for a known-split ticker.
- **DoD:** raw vintage immutable; adjusted series derived as-of and versioned; every label/series carries `price_basis`; the five §0.6 clauses each have a passing golden fixture (split-and-dividend).

### R0-S3 — PIT survivorship-safe universe (`FIXED_PIT_COHORT`) + instrument identity
- **Contracts:** universe posture is a **`FIXED_PIT_COHORT`** (v5 §0.4) with fields `cohort_selection_date, universe_definition_version, eligibility_rule_version, constituent_source_id, source_as_of, instrument_id, inclusion_reason, exclusion_reason, terminal_event_policy`; `instrument_master` + `instrument_identifier_history` (opaque `instrument_id`, CIK/FIGI as-of); terminal-event returns. Membership is selected using information available at `cohort_selection_date`: later delisted/merged/bankrupt names **remain**; later IPOs/newly-eligible names are **excluded by design**; R0 findings make **no dynamic-universe-robustness claim**. `DYNAMIC_PIT_ELIGIBILITY_UNIVERSE` is a later CHALLENGER (DEFERRED, NOT_IN_SCOPE for R0). Manual enumeration is permitted **only as an immutable signed manifest** (one provenance record per instrument; explicit delisting + identifier-history evidence; not constructed from a current-only ticker list; reproducible from repository-approved source artifacts). Refs V6.1–V6.3, §0.4 (ADR-008).
- **Tests:** cohort as-of `cohort_selection_date` **contains then-delisted names**; a later IPO is **excluded** from the fixed cohort; ticker-reuse resolves to two distinct `instrument_id`s; delisting/merger → terminal-event return (no missing label); ticker-only join **rejected**; membership frozen from `cohort_selection_date`; manual-enumeration path rejected unless it is a signed manifest with per-instrument provenance.
- **DoD:** survivorship-safe fixed PIT cohort with the §0.4 field set; opaque canonical key; identifier history; terminal events handled; no dynamic-universe claim asserted. *(Prerequisite: constituent/delisting source per §C.)*

### R0-S4 — PIT labels for 5/8/14 sessions (pure fixed-horizon exit)
- **Contracts:** label generation (declared `price_basis`, exchange-session counting with a pinned convention, maturity, `label_available_at`); **pure fixed-horizon exit** (label = traded return; no barriers). Refs V3.3, C-03 (ADR-005/006).
- **Tests:** 5/8/14-session labels; exchange-session counting example (entry index pinned); last-N rows remain `NOT_MATURED`; `label_available_at` correct; missing bars; split/dividend inside window; delisting terminal event; after-hours event behavior; `price_basis` present.
- **DoD:** matured-only labels on the declared basis; horizon-counting convention pinned with a worked example; golden fixtures pass.

### R0-S5 — Feature snapshot + schema/value parity + interval-based purged walk-forward + embargo + trial registry
- **Contracts:** `feature_snapshot` (schema hash **and** feature-values checksum, fit-isolation of scalers/imputers/calibrators/meta-learners); **interval-based** purged walk-forward splitter (v5 §0.5) — each sample exposes `feature_information_start, prediction_time, label_start, label_end, label_available_at, information_interval`; the splitter guarantees **no training information-interval overlaps a test information-interval**, all rows sharing a `prediction_time` stay in one group, all fit operations use training-only indices; an **additional embargo buffer is separately configured and justified** from label horizon + availability/publication delay + fold design + optional safety buffer (feature lookback alone is **not** auto-added as forward embargo unless an overlap analysis proves it necessary); append-only **trial registry**. Refs V7.1/V7.2, V14.4, §0.5 (ADR-001/006/013).
- **Tests:** batch-vs-"latest" **value parity** (not just schema hash) within tolerance for a fixed as-of date; fit-isolation (transform fit-indices ⊆ training window; calibration-fit ∩ calibration-eval = ∅); **no training information-interval overlaps any test information-interval**; same-`prediction_time` rows never split across train/test; separately-justified embargo buffer applied and recorded; **synthetic forward-return feature at the fold boundary → OOS IC ≈ 0** (leakage tripwire); trial registry append-only + every config logged.
- **DoD:** value-parity + leakage tripwire green; folds obey interval-based purge + separately-justified embargo; trial registry mandatory and exercised.

### R0-S6 — Baseline model + output-specific calibration + factor attribution + investable-benchmark + multiple-testing-adjusted hurdle + reproducible report
- **Contracts:**
  - **Primary forecast** = `expected_absolute_executable_return_bps` (continuous regression). **Comparator** = **pooled historical-panel elastic-net** (v5 §0.3-A: fit on training dates only, evaluate grouped by test date) — the required deployable comparator. A **Fama–MacBeth-style diagnostic** (§0.3-B) is optional; a **per-date oracle** (§0.3-C, fit on the test date) is **PROHIBITED** as a deployable/OOS baseline or promotion comparator.
  - **Calibration is output-specific** (v5 §0.2): the continuous primary target uses **residual/monotonic, quantile, or interval-coverage** calibration; Platt/isotonic + ECE apply **only** to a defined probability output. In R0 there is **no required probability head** → **`ECE = NOT_APPLICABLE_TO_PRIMARY_REGRESSION`**; an optional `probability_return_exceeds_cost_hurdle` head is not implicitly required and, only if a justified probability head is added, carries its own Platt/isotonic + ECE (that path is otherwise R1A).
  - **Multiple-testing** (v5 §0.7): promotion uses an **`applicable_multiple_testing_adjusted_hurdle`**; `trial_count` sourced from the append-only trial registry; DSR/PBO applicability stated explicitly; **DSR output is a statistical assessment (a deflated significance/probability), not an adjusted return amount**; `NOT_ESTIMABLE` is **never a pass and never proof of failure**.
  - **Benchmark & factor attribution are contract-bound** (v5 §0.8): portfolio-return frequency; factor-regression window; factor set (Mkt/SMB/HML/UMD/ST-Rev/BAB) + source versions; intercept/alpha interpretation; robust/dependence-aware SEs; matched-basket construction; long-only/short-leg policy; turnover matching; cost parity; beta matching; rebalance timing; benchmark eligibility; missing-factor behavior. Investable benchmark = SPY + matched basket, beta-adjusted, net of the same cost model.
  - **round-trip** cost model; two-tier reproducibility + `environment_hash`; report generator. Refs V4.3, V7.3/V7.4, V8.1, V11.1, V14.2/V14.3, §0.2/§0.3/§0.7/§0.8 (ADR-010/013/014/016).
- **Tests:** GBT vs **pooled elastic-net** comparator (net-of-cost, grouped by test date); **per-date-oracle comparator rejected** as an OOS/promotion baseline; regression-calibration metrics present and `ECE=NOT_APPLICABLE_TO_PRIMARY_REGRESSION` recorded when no probability head exists; **factor-residual net-of-cost significance** with dependence-aware SEs; **investable-benchmark outperformance** (beta-adjusted); `applicable_multiple_testing_adjusted_hurdle` computed from the logged trial count with DSR/PBO applicability recorded (`NOT_ESTIMABLE` neither pass nor fail); effective-sample IC-IR (non-overlapping/block-bootstrap); reproducibility (bit-exact symbolic artifacts; tolerance numeric); explicit **`BLOCKED_NO_EDGE`** path when the hurdle is not cleared.
- **DoD:** a factor-attributed, net-of-cost report vs an investable benchmark with the `applicable_multiple_testing_adjusted_hurdle` and output-specific calibration (ECE recorded `NOT_APPLICABLE_TO_PRIMARY_REGRESSION` absent a probability head), reproducible from a clean checkout; honest `BLOCKED_NO_EDGE` when no edge; no threshold changed after seeing results.

## E. Release-1A Producer/Consumer/Entity Matrix (starter, per PKT-15 — `~10` NOT frozen)
Include an entity in R1A only if it has a ✅ producer **and** consumer in R1A, or is required for auditability/ledger.

| Entity | R1A producer | R1A consumer | R1A? | Rationale |
| --- | --- | --- | --- | --- |
| `decision_cycle` | scheduler | all | ✅ | run identity |
| `recommendation` | recommendation svc | approval/UI/ledger | ✅ | core output |
| `forecast_snapshot` / `forecast_distribution` | forecast svc | decision policy | ✅ | forecasts feed utility |
| `decision_assessment` | decision policy | risk/portfolio/ledger | ✅ | utility/permission |
| `risk_assessment` | risk svc | portfolio/sizing | ✅ | sizing/caps |
| `execution_plan` (intent) | execution-policy | approval/outcome | ✅ | entry/stop intent |
| `outcome_record` | outcome svc | learning/ledger | ✅ | matured outcomes |
| `feature_snapshot` | feature store | forecast/replay | ✅ | PIT + replay |
| `decision_ledger_event` | all | audit/replay | ✅ | auditability |
| `audit_event` | audit svc | governance | ✅ | provenance |
| `market_state_snapshot` (minimal vector) | world-state (deterministic filter) | decision policy | ⚠️ optional | deterministic regime features only; hypotheses DEFERRED |
| `evidence_packet` | technical expert | decision policy | ⚠️ minimal | one expert; flat packet only |
| `evidence_dependency_graph` | — | — | ❌ DEFER 2A | needs ≥2 experts |
| `market_state_hypothesis` | — | — | ❌ DEFER 2A | needs regime-conditional model |
| `opportunity` (analytics) | — | — | ❌ DEFER 2A | family lineage suffices |
| `counterfactual_run/portfolio`, `module_value_profile` | — | — | ❌ DEFER 2B | needs matured volume |
| `content_*`, `source_profile` | — | — | ❌ DEFER 2A | news module deferred |
| `runtime_manifest` (minimal) | control plane | runtime load-gate | ✅ | approved-artifact gate |

Final R1A set is confirmed in Phase 4 when component contracts exist.

## F. Gate Result
Release-0 implementation is **READY to begin** on slices R0-S1…S6 (subject to the S3 data-source prerequisite), with all acceptance-affecting numeric thresholds frozen before final-holdout access. **No code is written in this phase.** Phase 4 (function/file/entity/model contract appendices) is the next step and must precede implementation.
