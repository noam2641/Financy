# RELEASE 0 — VALIDATION AND STATISTICS CONTRACTS (VAL-R0)

*documentation-only; canonical v4.6 unmodified; governed by v5 §0.5/§0.7; shared ID space per PHASE4_FOUNDATION; no code/src/tests created.*

Two-field status model (v5 §0.1) applies. Interval-based purge/embargo (§0.5) and multiple-testing terminology (§0.7) are authoritative.

---

## VAL-R0-01 — InformationInterval definition + worked 5/8/14-session examples
- **purpose:** define the per-sample information-time fields and demonstrate them concretely for each horizon.
- **normative rule:** every sample exposes six fields (ENT-R0-11): `feature_information_start, prediction_time, label_start, label_end, label_available_at, information_interval`, where `information_interval = [feature_information_start, label_end]`.
- **linked FN:** FN-R0-17 (build), FN-R0-12 (session counting). **linked ENT:** ENT-R0-11 InformationInterval, ENT-R0-09 LabelRecord.
- **conventions pinned:** `prediction_time` = **close of decision session t**; the position is entered on the **open of session t+1**; a horizon of H sessions ends at the **close of session t+H** (entry session t+1 counts as session 1). `label_available_at` = the timestamp at which the matured return is knowable = after the close of `label_end` session plus EOD finalization (next-morning availability). Exchange-session calendar excludes weekends and listed U.S. market holidays; the examples below include **Juneteenth (2023-06-19)** and **Independence Day (2023-07-04)** as skipped sessions to exercise holiday handling.

**Anchor:** decision session `t` = **2023-06-15 (Thu)**; `prediction_time` = 2023-06-15 close. Feature lookback window = 20 sessions → `feature_information_start` = start of the session 20 trading days before t (illustratively **2023-05-17**).

Horizon **H = 5**:

| field | value |
|---|---|
| prediction_time | 2023-06-15 (close) |
| entry (t+1 open) | 2023-06-16 (Fri) |
| session count | +1 06-16, +2 06-20 (06-19 Juneteenth skipped), +3 06-21, +4 06-22, +5 06-23 |
| label_start | 2023-06-16 (open basis) |
| label_end | 2023-06-23 (close) |
| label_available_at | 2023-06-26 (Mon) pre-open (after 06-23 EOD finalization) |
| information_interval | [2023-05-17, 2023-06-23] |

Horizon **H = 8**:

| field | value |
|---|---|
| prediction_time | 2023-06-15 (close) |
| session count | … +6 06-26, +7 06-27, +8 06-28 |
| label_start | 2023-06-16 (open basis) |
| label_end | 2023-06-28 (close) |
| label_available_at | 2023-06-29 (Thu) pre-open |
| information_interval | [2023-05-17, 2023-06-28] |

Horizon **H = 14**:

| field | value |
|---|---|
| prediction_time | 2023-06-15 (close) |
| session count | … +9 06-29, +10 06-30, +11 07-03, +12 07-05 (07-04 Independence Day skipped), +13 07-06, +14 07-07 |
| label_start | 2023-06-16 (open basis) |
| label_end | 2023-07-07 (close) |
| label_available_at | 2023-07-10 (Mon) pre-open |
| information_interval | [2023-05-17, 2023-07-07] |

- **dependence note (feeds VAL-R0-06):** because the 5/8/14 labels from the same `prediction_time` (and adjacent prediction_times) share overlapping `[label_start, label_end]` windows, their errors are serially dependent; raw row counts overstate the effective sample and inflate IC-IR by up to ~√H. Effective-sample inference is mandatory (VAL-R0-06).
- **required tests:** T-R0 for R0-REQ-18 (5/8/14 session counting with the two holidays), R0-REQ-19 (`label_available_at` correctness; last-N rows NOT_MATURED).
- **v5 refs:** §0.5. **v4.6 REQ:** REQ-VAL-001/002, REQ-LAB-001. **ADR:** ADR-001/013.

## VAL-R0-02 — Interval-based purged walk-forward split
- **purpose:** guarantee no train/test information leakage across folds.
- **normative rule:** (a) **no training information-interval overlaps any test information-interval**; (b) all cross-sectional rows sharing a `prediction_time` remain in **one group** (never split across train/test); (c) all fit operations (scalers, imputers, model, calibrator) use **training-only indices**.
- **linked FN:** FN-R0-18 (split), FN-R0-19 (assert_no_interval_overlap). **linked ENT:** ENT-R0-11, ENT-R0-12 FoldManifest.
- **failure policy:** overlap or split-group violation raises `IntervalOverlapError` and fails closed (no fold emitted).
- **config parameters + class:** `n_folds`, `scheme` (OWNER_POLICY_PARAMETER).
- **required tests:** T-R0 for R0-REQ-23 (no interval overlap), R0-REQ-24 (same prediction_time → one group).
- **v5 refs:** §0.5, V7.1. **v4.6 REQ:** REQ-VAL-001/002. **ADR:** ADR-001/013.

## VAL-R0-03 — Embargo buffer (separately justified)
- **purpose:** apply a justified embargo beyond raw interval non-overlap.
- **normative rule:** the embargo buffer is **separately configured and justified** from: label horizon + availability/publication delay + fold design + optional safety buffer. **Feature lookback alone is NOT auto-added as a forward embargo** unless an explicit overlap analysis proves it necessary. The justification is recorded in the FoldManifest (ENT-R0-12).
- **linked FN:** FN-R0-18. **linked ENT:** ENT-R0-12 (`embargo_buffer_sessions`, `embargo_justification`).
- **config parameters + class:** `embargo_buffer_sessions` (EMPIRICAL_THRESHOLD, justified), `safety_buffer_sessions` (OWNER_POLICY_PARAMETER).
- **required tests:** T-R0 for R0-REQ-25 (embargo buffer recorded with justification; lookback not auto-added).
- **v5 refs:** §0.5. **v4.6 REQ:** REQ-VAL-002. **ADR:** ADR-013.

## VAL-R0-04 — Trial registry + multiple-testing-adjusted hurdle
- **purpose:** control the garden of forking paths.
- **normative rule:** every config/seed/horizon/target/grid point is an append-only `TrialRecord` (ENT-R0-13); **any value chosen after viewing a backtest is a trial**. Promotion uses an **`applicable_multiple_testing_adjusted_hurdle`** whose `trial_count` is sourced from the registry.
- **linked FN:** FN-R0-20 (append_trial), FN-R0-25 (hurdle). **linked ENT:** ENT-R0-13 TrialRecord.
- **failure policy:** a promotion computed without a registry-sourced trial_count fails closed.
- **required tests:** T-R0 for R0-REQ-27 (registry append-only, every config logged), R0-REQ-32 (hurdle from registry).
- **v5 refs:** §0.7, V7.2. **v4.6 REQ:** REQ-VAL-008. **ADR:** ADR-013.

## VAL-R0-05 — DSR / PBO / CPCV applicability
- **purpose:** apply deflation/robustness methods only where their prerequisites hold.
- **normative rule:** **DSR** required when multiple strategy/model trials exist; **PBO/CSCV** required only when enough variants and partitions exist; **CPCV** is a robustness analysis when assumptions/sample support it. **DSR output is a statistical assessment (a deflated significance / probability), NOT an adjusted return amount.** `NOT_ESTIMABLE` is **never a pass and never proof of failure** — it records that prerequisites are absent. No method is claimed estimable when its prerequisites are missing.
- **linked FN:** FN-R0-25. **linked ENT:** ENT-R0-19 EvaluationReport (records applicability + values or `NOT_ESTIMABLE`).
- **required tests:** T-R0 for R0-REQ-32 (DSR is a statistical assessment; `NOT_ESTIMABLE` neither pass nor fail).
- **v5 refs:** §0.7, V7.3. **v4.6 REQ:** REQ-VAL-008. **ADR:** ADR-013.

## VAL-R0-06 — Effective-sample inference
- **purpose:** avoid overstating significance from overlapping labels.
- **normative rule:** IC/IR and significance use **effective sample** methods — non-overlapping blocks or block-bootstrap — not raw row counts (see VAL-R0-01 dependence note).
- **linked FN:** FN-R0-24 (effective_sample_ic_ir). **linked ENT:** ENT-R0-19.
- **config parameters + class:** `block_length_sessions` (EMPIRICAL_THRESHOLD, ≥ max horizon), `bootstrap_reps` (OWNER_POLICY_PARAMETER).
- **required tests:** T-R0 for R0-REQ-38 (effective-sample IC-IR via non-overlapping/block-bootstrap).
- **v5 refs:** V7.4. **v4.6 REQ:** REQ-VAL-005/006. **ADR:** ADR-013.

## VAL-R0-07 — Leakage tripwire
- **purpose:** detect any residual look-ahead across the fold boundary.
- **normative rule:** inject a **synthetic forward-return feature** at the fold boundary; a correct splitter yields **OOS IC ≈ 0** (within tolerance). A materially non-zero OOS IC fails the gate.
- **linked FN:** FN-R0-18 (exercised by the test). **linked ENT:** ENT-R0-12.
- **required tests:** T-R0 for R0-REQ-26 (synthetic forward feature → OOS IC ≈ 0).
- **v5 refs:** §0.5. **v4.6 REQ:** REQ-TEST-002. **ADR:** ADR-013.

## VAL-R0-08 — Value-parity (batch vs latest)
- **purpose:** defend against train/serve skew that schema-hash parity misses.
- **normative rule:** for a fixed as-of date, the **batch** feature path and the **"latest"** single-row path produce **equal feature values within tolerance**; a matching schema hash alone is insufficient — a `feature_values_checksum` (ENT-R0-10) must also match.
- **linked FN:** FN-R0-16 (values_checksum), FN-R0-15. **linked ENT:** ENT-R0-10 FeatureSnapshot.
- **required tests:** T-R0 for R0-REQ-28 (batch-vs-latest value parity), R0-REQ-21 (schema hash + values checksum).
- **v5 refs:** V14.4. **v4.6 REQ:** REQ-FEAT-003. **ADR:** ADR-006/013.

---

## Statistics summary
- Primary inference is effective-sample (VAL-R0-06); promotion hurdle is multiple-testing-adjusted (VAL-R0-04/05); leakage is defended by the interval splitter (VAL-R0-02), the tripwire (VAL-R0-07), and value-parity (VAL-R0-08). All statuses use the two-field model; the methodology is OWNER_APPROVED · BINDING while numeric thresholds remain EMPIRICAL_TBD · PROVISIONAL_DEFAULT and are pre-registered before final-holdout access (RPT-R0-07).
