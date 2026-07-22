# RELEASE 0 — REPORT AND EVIDENCE CONTRACTS (RPT-R0)

*documentation-only; canonical v4.6 unmodified; governed by v5 §0.7/§0.8 + V14 reproducibility; shared ID space per PHASE4_FOUNDATION; no code/src/tests created.*

Two-field status model (v5 §0.1) applies. The evaluation report is the terminal R0 evidence artifact; it is reproducible from a clean checkout under the two-tier reproducibility policy.

---

## RPT-R0-01 — EvaluationReport schema
- **produced_by:** FN-R0-29 (`generate_evaluation_report`). **linked ENT:** ENT-R0-19 EvaluationReport.
- **required content:**
  - forecast metrics on the continuous primary target (`expected_absolute_executable_return_bps`): OOS IC/IR (effective-sample, VAL-R0-06), RMSE/MAE.
  - **calibration block:** for the continuous primary, records regression-calibration/interval-coverage metrics and **`ECE = NOT_APPLICABLE_TO_PRIMARY_REGRESSION`** (MDL-R0-07); a probability head, if justified, adds Platt/isotonic + ECE.
  - **comparator block:** GBT (MDL-R0-02) vs pooled elastic-net (MDL-R0-03), net-of-cost, grouped by test date; a per-date oracle is **excluded** (MDL-R0-05).
  - **hurdle block:** `applicable_multiple_testing_adjusted_hurdle` with `trial_count`, DSR/PBO/CPCV applicability + values or `NOT_ESTIMABLE` (VAL-R0-04/05).
  - **outcome enum** ∈ {`EDGE_SUPPORTED`, `BLOCKED_NO_EDGE`, `INCONCLUSIVE`}.
- **invariants:** every metric names its basis and effective-sample method; no metric mixes target bases.
- **determinism:** symbolic fields BIT_EXACT; embedded numeric metrics TOLERANCE_NUMERIC.
- **required tests:** T-R0 for R0-REQ-31 (ECE field), R0-REQ-32 (hurdle block), R0-REQ-37 (outcome enum present).
- **v5 refs:** §0.2/§0.7. **v4.6 REQ:** REQ-VAL-004/008. **ADR:** ADR-013.

## RPT-R0-02 — Factor-attribution table (contract-bound, §0.8)
- **produced_by:** FN-R0-26 (`factor_attribution`). **linked ENT:** ENT-R0-18 FactorAttributionResult.
- **required content — all 13 §0.8 elements (checklist):**
  1. portfolio-return **frequency**;
  2. factor-regression **window**;
  3. **factor set** (Mkt, SMB, HML, UMD, ST-Rev, BAB) + **source versions**;
  4. **intercept/alpha interpretation** (residual alpha meaning);
  5. **robust / dependence-aware standard errors** (e.g. Newey–West / block);
  6. **matched-basket construction**;
  7. **long-only / short-leg policy**;
  8. **turnover matching**;
  9. **cost parity** (same round-trip cost model as the strategy);
  10. **beta matching**;
  11. **rebalance timing**;
  12. **benchmark eligibility**;
  13. **missing-factor behavior**.
- **invariants:** significance uses dependence-aware SEs; residual alpha is net-of-cost.
- **required tests:** T-R0 for R0-REQ-33 (all 13 elements present; dependence-aware SEs used).
- **v5 refs:** §0.8, V7.4. **v4.6 REQ:** REQ-VAL-004. **ADR:** ADR-013.

## RPT-R0-03 — Investable-benchmark comparison
- **produced_by:** FN-R0-27 (`build_investable_benchmark`). **linked ENT:** ENT-R0-16 BenchmarkDefinition, ENT-R0-17 CostModelDefinition.
- **required content:** SPY + matched basket, **beta-adjusted**, **net of the same round-trip cost model** (RPT links to FN-R0-28). Outperformance is reported against this investable benchmark, not a naive forecast comparator.
- **invariants:** benchmark and strategy share cost parity and beta matching (ties to RPT-R0-02 items 9–10).
- **required tests:** T-R0 for R0-REQ-34 (investable-benchmark outperformance, beta-adjusted, net-of-cost).
- **v5 refs:** §0.8, V7.4. **v4.6 REQ:** REQ-VAL-004. **ADR:** ADR-013.

## RPT-R0-04 — BLOCKED_NO_EDGE terminal outcome
- **produced_by:** FN-R0-29. **linked ENT:** ENT-R0-19.
- **required content:** `BLOCKED_NO_EDGE` is a **first-class terminal outcome** recorded honestly when the pre-registered hurdle is not cleared; the program stops at the probe (does not escalate to a learned layer to rescue). **No threshold is changed after seeing results** (ties to RPT-R0-07).
- **invariants:** the outcome is derived from the pre-registered hurdle snapshot, not a post-hoc value.
- **required tests:** T-R0 for R0-REQ-37 (BLOCKED_NO_EDGE path exercised), R0-REQ-40 (no threshold changed after results).
- **v5 refs:** V1.3. **v4.6 REQ:** R0-BL-006. **ADR:** ADR-002.

## RPT-R0-05 — Reproducibility evidence (two-tier + environment_hash)
- **produced_by:** FN-R0-30 (`environment_hash`), FN-R0-29. **linked ENT:** ENT-R0-21 RuntimeEnvironmentManifest (from the non-entity `RuntimeInfo` input — see FN-R0-30).
- **required content:** **two-tier reproducibility** — **BIT_EXACT** for symbolic artifacts (raw data, canonical schema, corp-action store, cohort manifest, labels, fold manifest, feature-values checksum, trial registry, run ledger) and **TOLERANCE_NUMERIC** for fitted model/calibration/attribution artifacts (reproduced within an approved tolerance). `environment_hash` composition: the exact key set `{interpreter_version, dependency_lockfile_hash, os_arch, blas_threading_flags, random_seeds, data_vintage_ids}`, canonical UTF-8 JSON (sort_keys, `(",",":")`, ensure_ascii=False, allow_nan=False, no whitespace), SHA-256 lowercase 64-hex (see FN-R0-30).
- **invariants:** the report is reproducible from a clean checkout; `environment_hash` is recorded on every run; no clock/machine/env-var/secret value contributes.
- **required tests (T-R0-036 precision):** a **fixed `RuntimeInfo` fixture**; an **exact pinned 64-character** environment hash; repeated identical input returns the **same manifest and hash**; every one of the **six** composition fields is present; **changing one field changes the hash**; **duplicate data-vintage IDs are rejected**; **no clock/network/filesystem access**.
- **v5 refs:** V14.2/V14.3. **v4.6 REQ:** REQ-GATE-001. **ADR:** ADR-016.

## RPT-R0-06 — Run-ledger evidence
- **produced_by:** FN-R0-31 (`append_run_event`). **linked ENT:** ENT-R0-20 RunLedgerEvent. **state type:** the non-entity `RunLedger = tuple[RunLedgerEvent, ...]` (explicit, immutable; no process-global ledger).
- **required content:** append-only, hash-linked run events over the **closed** `RunLedgerEventType` vocabulary `{RUN_STARTED, ARTIFACT_WRITTEN, TRIAL_APPENDED, FOLD_BUILT, MODEL_FIT, REPORT_GENERATED}`; each event carries `environment_hash` and `prior_event_hash`; genesis prior hash = 64 zero chars; each later event links to the canonical SHA-256 of its predecessor (canonical event object keys `{event_id, event_type, prior_event_hash, payload_hash, environment_hash, timestamp}`, timestamp ISO-8601 UTC `…ffffffZ`).
- **invariants:** append-only; tamper-evident hash chain; explicit event_id + tz-aware UTC nondecreasing timestamps supplied by the caller; BIT_EXACT.
- **required tests (T-R0-039 precision):** empty-ledger genesis append; a second append linked to the **exact first-event hash**; the original tuple remains unchanged; the resulting tuple contains both events in timestamp order; identical event-ID replay is **idempotent**; conflicting reuse of an event ID raises **`LedgerMutationError`**; tampering with `payload_hash`, `prior_event_hash`, `environment_hash`, `timestamp`, or event ordering is detected; a raw string / unsupported event type is rejected; **no clock, UUID, random, filesystem, database, or network access**.
- **v5 refs:** V14.4. **v4.6 REQ:** REQ-SCH-027. **ADR:** ADR-016.

## RPT-R0-07 — Pre-registration record
- **produced_by:** FN-R0-29 (records the pre-registration snapshot). **linked ENT:** ENT-R0-19.
- **required content:** all acceptance-affecting numeric hurdles (effect-size band, min matured recommendations, max ECE for any probability head, drawdown caps) are **pre-registered before final-holdout access**, with a conservative provisional range, source rationale, decision rule, **freeze point**, and **owner approval** before that access.
- **invariants:** the final-holdout outcome (RPT-R0-04) is evaluated only against the frozen pre-registration snapshot; any post-holdout change triggers re-deflation and is itself logged (no silent change).
- **required tests:** T-R0 for R0-REQ-40 (pre-registration freeze; no threshold changed after results).
- **v5 refs:** V1.4/V7.5. **v4.6 REQ:** REQ-GATE-003, REQ-GOV-006. **ADR:** ADR-002/016.

---

## Evidence summary
The R0 evidence chain is: **RunLedgerEvent (RPT-R0-06) → EvaluationReport (RPT-R0-01)** carrying the **factor-attribution table (RPT-R0-02)**, **investable-benchmark comparison (RPT-R0-03)**, **multiple-testing hurdle**, **reproducibility evidence (RPT-R0-05)**, and either `EDGE_SUPPORTED` or **`BLOCKED_NO_EDGE` (RPT-R0-04)** — all evaluated against the frozen **pre-registration record (RPT-R0-07)**. Methodology is OWNER_APPROVED · BINDING; numeric hurdles are EMPIRICAL_TBD · PROVISIONAL_DEFAULT and pre-registered.
