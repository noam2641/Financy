# RELEASE 0 — MODEL AND CALIBRATION CONTRACTS (MDL-R0)

*documentation-only; canonical v4.6 unmodified; governed by v5 §0.2/§0.3/§0.7; shared ID space per PHASE4_FOUNDATION; no code/src/tests created.*

Two-field status model (v5 §0.1) is normative: `decision_status ∈ {OWNER_APPROVED, EMPIRICAL_TBD, DEFERRED, REJECTED}`, `implementation_posture ∈ {BINDING, PROVISIONAL_DEFAULT, CHALLENGER, NOT_IN_SCOPE}`. A PROVISIONAL_DEFAULT is implementable but replaceable and is **never** described as a final owner-selected component.

---

## 0. Decision settlement (the five modeling questions, resolved)

| # | Question | Resolved answer | decision_status · posture | MDL |
|---|---|---|---|---|
| 1 | Primary forecast target | `expected_absolute_executable_return_bps` — **CONTINUOUS regression**, basis `ABSOLUTE_EXECUTABLE_RETURN_BPS` | OWNER_APPROVED (target) · BINDING; numeric performance EMPIRICAL_TBD | MDL-R0-01 |
| 2 | Primary learned predictor | **GBT (LightGBM/XGBoost)** as the working default | EMPIRICAL_TBD · PROVISIONAL_DEFAULT | MDL-R0-02 |
| 3 | Deployable comparator | **Pooled historical-panel elastic-net** (fit on training dates only, evaluate grouped by test date) | EMPIRICAL_TBD · PROVISIONAL_DEFAULT | MDL-R0-03 |
| 4 | Prohibited comparator | **Per-date oracle** (fit-on-test-date) is PROHIBITED as an OOS/promotion baseline | OWNER_APPROVED (prohibition) · BINDING | MDL-R0-05 |
| 5 | ECE applicability | R0 has **no required probability head** → `ECE = NOT_APPLICABLE_TO_PRIMARY_REGRESSION` | OWNER_APPROVED · BINDING | MDL-R0-07 |

---

## MDL-R0-01 — Primary forecast target
- **name / role:** `expected_absolute_executable_return_bps` — primary economic/trading forecast target.
- **decision_status · posture:** OWNER_APPROVED (target definition) · BINDING. Numeric attainability EMPIRICAL_TBD.
- **target · basis · units:** absolute executable return · `ABSOLUTE_EXECUTABLE_RETURN_BPS` · basis points.
- **output_type:** CONTINUOUS_RETURN (regression). **Not** a probability; not a rank score.
- **fit protocol:** produced by the learned predictor (MDL-R0-02) and comparator (MDL-R0-03); fit on training-fold rows only under the interval-based splitter (VAL-R0-02).
- **evaluation protocol:** OOS, grouped by test date; effective-sample inference (VAL-R0-06).
- **prohibited usages:** must not be silently substituted by a market-excess/sector-excess basis; only absolute-executable values may have absolute costs subtracted (v5 V4.2).
- **linked FN:** FN-R0-21, FN-R0-22 (produce it), FN-R0-28 (cost subtraction), FN-R0-29 (report). **linked ENT:** ENT-R0-09 LabelRecord (target_basis=ABSOLUTE_EXECUTABLE_RETURN), ENT-R0-14 ModelArtifactManifest.
- **config parameters + class:** `horizon_sessions ∈ {5,8,14}` (OWNER_POLICY_PARAMETER); `target_definition_version` (FROZEN_ECONOMIC_PRIOR).
- **leakage risks + mitigation:** target must be computed from as-of adjusted prices (§0.6c) with `label_available_at` respected; mitigated by ENT-R0-09 carrying `price_basis` + `label_available_at`.
- **required tests:** T-R0 covering R0-REQ-29 (primary target is continuous regression on the absolute-executable basis).
- **v5 refs:** V4.1/V4.2, §0.2. **v4.6 REQ:** REQ-LAB-005/006, REQ-DEC-001. **ADR:** ADR-003/004.
- **replaceability:** the *target definition* is BINDING; the *predictor* producing it is replaceable (MDL-R0-02).

## MDL-R0-02 — GBT baseline predictor
- **name / role:** gradient-boosted trees (LightGBM or XGBoost) — primary learned predictor of MDL-R0-01.
- **decision_status · posture:** EMPIRICAL_TBD · **PROVISIONAL_DEFAULT** (working default; replaceable; not owner-final).
- **output_type:** CONTINUOUS_RETURN.
- **fit protocol:** fit on training-fold rows only; hyperparameters chosen via nested training-only selection; every configuration is a logged trial (VAL-R0-04).
- **evaluation protocol:** OOS grouped by test date; compared net-of-cost against MDL-R0-03.
- **prohibited usages:** no fitting on test-fold rows; no target/feature leakage across the fold boundary (leakage tripwire VAL-R0-07).
- **calibration:** continuous output → MDL-R0-06 residual/quantile/interval calibration (NOT Platt/isotonic).
- **linked FN:** FN-R0-21. **linked ENT:** ENT-R0-14 ModelArtifactManifest (producer=`BASELINE_GBT`).
- **config parameters + class:** learning rate / depth / n_estimators / regularization (FIT_ON_TRAINING_ONLY); random seed (FROZEN_ECONOMIC_PRIOR for reproducibility).
- **determinism:** TOLERANCE_NUMERIC (fitted artifact reproduced within approved tolerance; seed + environment_hash recorded).
- **leakage risks + mitigation:** fit-isolation via FeatureSnapshot fit-isolation (ENT-R0-10); tripwire test.
- **required tests:** T-R0 for R0-REQ-29; leakage tripwire (R0-REQ-26).
- **v5 refs:** V8.1, §0.3. **v4.6 REQ:** REQ-MOD-001/002. **ADR:** ADR-010/011.
- **replaceability:** any predictor that beats GBT net-of-cost under identical PIT/cost/CPCV rules may replace it (challenger machinery, V8.4).

## MDL-R0-03 — Pooled historical-panel elastic-net comparator
- **name / role:** pooled elastic-net over the historical training panel — the **required deployable comparator** (v5 §0.3-A).
- **decision_status · posture:** EMPIRICAL_TBD · PROVISIONAL_DEFAULT (required to be present; specific hyperparameters replaceable).
- **output_type:** CONTINUOUS_RETURN.
- **fit protocol:** **fit on training dates only** (pooled across the training panel); L1/L2 mix and penalty chosen on training folds; frozen before test dates.
- **evaluation protocol:** **evaluate grouped by test date**, OOS; net-of-cost head-to-head vs GBT (MDL-R0-02).
- **prohibited usages:** must not be fit on any test-date row; must not be replaced by a per-date oracle (MDL-R0-05).
- **linked FN:** FN-R0-22. **linked ENT:** ENT-R0-14 (producer=`COMPARATOR_ELASTICNET`).
- **config parameters + class:** `l1_ratio`, `alpha` (FIT_ON_TRAINING_ONLY).
- **determinism:** TOLERANCE_NUMERIC.
- **required tests:** T-R0 for R0-REQ-30 (comparator = pooled elastic-net; grouped-by-test-date evaluation).
- **v5 refs:** §0.3-A, V8.1. **v4.6 REQ:** REQ-MOD-002. **ADR:** ADR-010.
- **replaceability:** deployable-comparator role is BINDING; the estimator instance is a provisional default.

## MDL-R0-04 — Fama–MacBeth-style diagnostic comparator
- **name / role:** per-training-date cross-sectional coefficients aggregated over **training dates only** — **OPTIONAL diagnostic** (v5 §0.3-B).
- **decision_status · posture:** EMPIRICAL_TBD · CHALLENGER (optional; diagnostic only).
- **output_type:** diagnostic coefficient series (not a deployable forecast).
- **fit protocol:** cross-sectional regression per training date; coefficients averaged over training dates; **frozen before test dates**.
- **prohibited usages:** never used as the deployable OOS baseline (that is MDL-R0-03); never fit on test dates.
- **linked FN:** FN-R0-22 (diagnostic path). **linked ENT:** ENT-R0-18 FactorAttributionResult (diagnostic block).
- **required tests:** optional T-R0 diagnostic; not gating.
- **v5 refs:** §0.3-B. **ADR:** ADR-010/013.
- **replaceability:** optional throughout.

## MDL-R0-05 — Per-date oracle (PROHIBITED)
- **name / role:** cross-sectional model fit **on the test date itself** — diagnostic-only; **PROHIBITED** as a deployable/OOS baseline or promotion comparator (v5 §0.3-C).
- **decision_status · posture:** OWNER_APPROVED (prohibition) · BINDING (NOT_IN_SCOPE as a baseline).
- **contract guard:** FN-R0-22 MUST assert that no comparator artifact used for OOS/promotion was fit on any row whose `prediction_time` falls in the test fold; violation raises `PerDateOracleProhibitedError` and fails closed.
- **linked FN:** FN-R0-22 (guard). **linked ENT:** ENT-R0-14 (guard rejects producer=`PER_DATE_ORACLE` in any OOS/promotion context).
- **required tests:** T-R0 for R0-REQ-30 (per-date-oracle rejection fixture — a comparator fit on test rows is rejected).
- **v5 refs:** §0.3-C. **ADR:** ADR-010/013.

## MDL-R0-06 — Output-specific calibration
- **name / role:** calibration is **selected by output type** (v5 §0.2).
- **decision_status · posture:** OWNER_APPROVED (method-selection rule) · BINDING; specific method EMPIRICAL_TBD · PROVISIONAL_DEFAULT.
- **rule:** CONTINUOUS_RETURN output → **residual/monotonic calibration OR quantile calibration OR interval-coverage** calibration. PROBABILITY output → **Platt/isotonic + ECE**. Platt/isotonic and ECE are **never** applied to a continuous return.
- **set discipline:** every calibrated output declares `target, fit_set_id, calibration_set_id, eval_set_id, units, metric`; **calibration-fit ∩ calibration-eval = ∅**; both obey purge/embargo (VAL-R0-02/03).
- **linked FN:** FN-R0-23. **linked ENT:** ENT-R0-15 CalibrationArtifactManifest.
- **config parameters + class:** `calibration_method` (OWNER_POLICY_PARAMETER), `coverage_target` (EMPIRICAL_THRESHOLD).
- **required tests:** T-R0 for R0-REQ-31 (continuous target uses regression calibration; probability-only Platt/isotonic path; disjoint fit/eval sets).
- **v5 refs:** §0.2, V8.2. **v4.6 REQ:** REQ-MOD-003/005. **ADR:** ADR-010.

## MDL-R0-07 — ECE applicability policy
- **name / role:** governs whether Expected Calibration Error applies in R0.
- **decision_status · posture:** OWNER_APPROVED · BINDING.
- **rule:** R0 has **no required probability head** → the report records **`ECE = NOT_APPLICABLE_TO_PRIMARY_REGRESSION`**. An optional `probability_return_exceeds_cost_hurdle` head is **not implicitly required**; only if a **justified** probability head is added do Platt/isotonic + ECE apply (otherwise an R1A concern). ECE is never computed against the continuous primary target.
- **linked FN:** FN-R0-23, FN-R0-29 (report records the value). **linked ENT:** ENT-R0-15 (ECE field = `NOT_APPLICABLE_TO_PRIMARY_REGRESSION` when no probability head), ENT-R0-19 EvaluationReport.
- **required tests:** T-R0 for R0-REQ-31 (report asserts `ECE=NOT_APPLICABLE_TO_PRIMARY_REGRESSION` absent a probability head).
- **v5 refs:** §0.2. **ADR:** ADR-010.

## MDL-R0-08 — Prediction intervals (conformal / CQR)
- **name / role:** interval forecasts around the continuous target via quantile regression / conformalized quantile regression.
- **decision_status · posture:** EMPIRICAL_TBD · PROVISIONAL_DEFAULT.
- **rule:** coverage validated under **time-series (non-exchangeable)** conditions; calibration sets obey purge/embargo; report interval-coverage as the continuous-output calibration metric (feeds MDL-R0-06 interval-coverage option).
- **linked FN:** FN-R0-23. **linked ENT:** ENT-R0-15 (method=`CQR`, metric=`interval_coverage`).
- **config parameters + class:** `quantile_levels`, `target_coverage` (EMPIRICAL_THRESHOLD).
- **required tests:** T-R0 for R0-REQ-31 (interval coverage measured on OOS folds).
- **v5 refs:** §0.2, V8.2. **v4.6 REQ:** REQ-MOD-003/005. **ADR:** ADR-010.

---

## Note on ENT-R0-14 single-writer resolution
`ModelArtifactManifest` (ENT-R0-14) is produced by both FC-R0-14 (baseline) and FC-R0-15 (comparator). To preserve single-writer semantics it carries a mandatory **`producer` discriminator** ∈ {`BASELINE_GBT`, `COMPARATOR_ELASTICNET`, `COMPARATOR_FAMA_MACBETH`, `PER_DATE_ORACLE`(diagnostic-only, prohibited for OOS/promotion)}. The allowed writer is the **model-training layer** (FN-R0-21 for `BASELINE_GBT`; FN-R0-22 for the comparator producers), one manifest instance per fitted artifact. This is the canonical resolution referenced by the entity contract (ENT-R0-14).
