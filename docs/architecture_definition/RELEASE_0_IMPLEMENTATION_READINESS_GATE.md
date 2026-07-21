# Release-0 Implementation Readiness Gate (Phase 3)

**Status:** documentation-only. Defines exactly what is ready to implement, what remains empirical, and the first six Release-0 (Edge Probe) slices with contracts/tests/Definition-of-Done. **No code is written here.** Basis: ratified Owner Decisions (Round 1) + `AI_TRADING_SYSTEM_ARCHITECTURE_V5_DRAFT.md`.

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
- **Contracts:** versioned corporate-action record; as-of adjustment function (`ex_date ≤ cutoff`, `corporate_action_version`, `split_adjustment_factor`); `price_basis`/`dividend_treatment` declaration. Refs V5.1–V5.3 (ADR-006).
- **Tests:** split-after-feature-date → as-of price **levels invariant** to the later split; **split cancels in simple returns**; dividend handled per declared treatment; `price_basis` present on labels & analytical series; current-vintage back-adjusted **rejected** for levels/filters/universe/labels; re-pull idempotency for a known-split ticker.
- **DoD:** raw vintage immutable; adjusted series derived as-of and versioned; every label/series carries `price_basis`; golden split+dividend fixture passes.

### R0-S3 — PIT survivorship-safe universe + instrument identity
- **Contracts:** universe construction (as-of backtest-start, incl. later-delisted, frozen membership); `instrument_master` + `instrument_identifier_history` (opaque `instrument_id`, CIK/FIGI as-of); terminal-event returns. Refs V6.1–V6.3 (ADR-008).
- **Tests:** universe as-of start **contains then-delisted names**; ticker-reuse resolves to two distinct `instrument_id`s; delisting/merger → terminal-event return (no missing label); ticker-only join **rejected**; membership frozen from start date.
- **DoD:** survivorship-safe PIT universe; opaque canonical key; identifier history; terminal events handled. *(Prerequisite: constituent/delisting source per §C.)*

### R0-S4 — PIT labels for 5/8/14 sessions (pure fixed-horizon exit)
- **Contracts:** label generation (declared `price_basis`, exchange-session counting with a pinned convention, maturity, `label_available_at`); **pure fixed-horizon exit** (label = traded return; no barriers). Refs V3.3, C-03 (ADR-005/006).
- **Tests:** 5/8/14-session labels; exchange-session counting example (entry index pinned); last-N rows remain `NOT_MATURED`; `label_available_at` correct; missing bars; split/dividend inside window; delisting terminal event; after-hours event behavior; `price_basis` present.
- **DoD:** matured-only labels on the declared basis; horizon-counting convention pinned with a worked example; golden fixtures pass.

### R0-S5 — Feature snapshot + schema/value parity + purged walk-forward + embargo + trial registry
- **Contracts:** `feature_snapshot` (schema hash **and** feature-values checksum, fit-isolation of scalers/imputers/calibrators/meta-learners); purged walk-forward splitter (bidirectional purge on the cross-sectional date union, **embargo ≥ 14 + feature memory**); append-only **trial registry**. Refs V7.1/V7.2, V14.4 (ADR-001/006/013).
- **Tests:** batch-vs-"latest" **value parity** (not just schema hash) within tolerance for a fixed as-of date; fit-isolation (transform fit-indices ⊆ training window; calibration ∩ ECE-eval = ∅); fold manifest `min(test_date) − max(train_label_end) ≥ embargo`; **synthetic forward-return feature at the fold boundary → OOS IC ≈ 0** (leakage tripwire); trial registry append-only + every config logged.
- **DoD:** value-parity + leakage tripwire green; folds obey purge+embargo; trial registry mandatory and exercised.

### R0-S6 — Baseline model + calibration + factor attribution + investable-benchmark + DSR + reproducible report
- **Contracts:** GBT (primary) + elastic-net/cross-sectional-regression comparator; isotonic/Platt calibration; factor-attribution regression (Mkt/SMB/HML/UMD/ST-Rev/BAB); investable benchmark (SPY + matched basket, beta-adjusted); **round-trip** cost model; DSR (from trial-registry N); two-tier reproducibility + `environment_hash`; report generator. Refs V4.3, V7.3/V7.4, V8.1, V11.1, V14.2/V14.3 (ADR-010/013/014/016).
- **Tests:** GBT vs comparator (net-of-cost); **factor-residual net-of-cost significance**; **investable-benchmark outperformance** (beta-adjusted); DSR computed from logged trial count; effective-sample IC-IR (non-overlapping/block-bootstrap); reproducibility (bit-exact symbolic artifacts; tolerance numeric); explicit **`BLOCKED_NO_EDGE`** path when the hurdle is not cleared.
- **DoD:** a factor-attributed, net-of-cost, DSR-adjusted report vs an investable benchmark, reproducible from a clean checkout; honest `BLOCKED_NO_EDGE` when no edge; no threshold changed after seeing results.

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
