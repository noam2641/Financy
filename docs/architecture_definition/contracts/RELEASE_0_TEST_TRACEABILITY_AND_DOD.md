# RELEASE 0 — TEST TRACEABILITY AND DEFINITION OF DONE (T-R0)

*documentation-only; canonical v4.6 unmodified; governed by v5 §0; shared ID space per PHASE4_FOUNDATION; no code/src/tests created.*

Convention: **`T-R0-0NN` is the primary deterministic test for `R0-REQ-NN`** (1:1), plus edge tests `T-R0-041+`. **Live-provider tests `T-R0-L##`** are network-gated, opt-in, excluded from the deterministic CI gate, and **never depend on a live ticker's current/looked-up value** — they assert adapter mechanics only. Every deterministic test uses a committed fixture.

---

## 1. Master requirement → test traceability (all 40)

| R0-REQ | requirement (short) | FN(s) | ENT(s) | Test | fixture + assertion |
|---|---|---|---|---|---|
| 01 | 1-D numeric canonical raw OHLCV | FN-R0-01/02 | ENT-R0-02 | T-R0-001 | provider-MultiIndex + flat fixtures → canonical 1-D bars |
| 02 | raw-basis only, no back-adjusted | FN-R0-02 | ENT-R0-02 | T-R0-002 | fixture asserts `auto_adjust=False`; no adjusted column emitted |
| 03 | dup/unsorted/mixed-tz handling | FN-R0-03 | ENT-R0-02 | T-R0-003 | dup-timestamp (reject), unsorted (reject/sort), mixed-tz (normalize) fixtures |
| 04 | source lineage present | FN-R0-01 | ENT-R0-01 | T-R0-004 | fixture asserts SourceRecord written with payload hash |
| 05 | versioned corp-action store | FN-R0-04 | ENT-R0-03 | T-R0-005 | append two versions; both retrievable; prior immutable |
| 06 | as-of adjustment ex_date≤cutoff | FN-R0-05/06 | ENT-R0-03/04 | T-R0-006 | split-after-feature-date fixture → as-of levels invariant to later split |
| 07 | split-only exception same-side only (§0.6a) | FN-R0-07 | ENT-R0-03 | T-R0-007 | same-side endpoints → simple return unchanged |
| 08 | raw return spanning split rejected (§0.6b) | FN-R0-06/07 | ENT-R0-04 | T-R0-008 | endpoints straddling a split without handling → raises |
| 09 | label spanning split uses as-of adj (§0.6c) | FN-R0-13 | ENT-R0-09 | T-R0-009 | label window straddling split → declared as-of adjustment applied |
| 10 | dividends explicit, no split-exception (§0.6d) | FN-R0-07 | ENT-R0-03 | T-R0-010 | dividend fixture → explicit treatment; split exception misuse raises |
| 11 | levels/filters/universe never inherit exception (§0.6e) | FN-R0-06 | ENT-R0-04 | T-R0-011 | back-adjusted level/filter/universe use → rejected |
| 12 | price_basis present on labels & series | FN-R0-06/13 | ENT-R0-04/09 | T-R0-012 | every derived series + label carries price_basis |
| 13 | FIXED_PIT_COHORT field set | FN-R0-08 | ENT-R0-07 | T-R0-013 | cohort fixture asserts all 9 §0.4 fields present |
| 14 | contains then-delisted; later IPO excluded | FN-R0-08 | ENT-R0-07 | T-R0-014 | cohort fixture contains a then-delisted name; a later IPO is excluded |
| 15 | opaque id; ticker-only join rejected; reuse→2 ids | FN-R0-09/10 | ENT-R0-05/06 | T-R0-015 | ticker-reuse fixture → 2 instrument_ids; ticker-only join raises |
| 16 | terminal-event returns, no missing labels | FN-R0-11 | ENT-R0-08 | T-R0-016 | delisting fixture → terminal return (no missing label) |
| 17 | manual enumeration only as signed manifest | FN-R0-08 | ENT-R0-07 | T-R0-017 | current-only ticker list → rejected; signed manifest → accepted |
| 18 | 5/8/14 session counting pinned | FN-R0-12 | ENT-R0-11 | T-R0-018 | worked 5/8/14 examples incl. Juneteenth & Independence Day |
| 19 | label_available_at; last-N NOT_MATURED | FN-R0-13/14 | ENT-R0-09 | T-R0-019 | last-N rows NOT_MATURED; available_at matches VAL-R0-01 |
| 20 | pure fixed-horizon exit = traded return | FN-R0-13 | ENT-R0-09 | T-R0-020 | label equals point-to-point traded return (no barriers) |
| 21 | feature_snapshot schema hash + values checksum | FN-R0-15/16 | ENT-R0-10 | T-R0-021 | snapshot carries both schema_hash and feature_values_checksum |
| 22 | fit-isolation of transforms/calibrators | FN-R0-15 | ENT-R0-10 | T-R0-022 | transform fit-indices ⊆ training window |
| 23 | interval-based purge: no overlap | FN-R0-17/18/19 | ENT-R0-11/12 | T-R0-023 | overlapping train/test information intervals → raises |
| 24 | same prediction_time → one group | FN-R0-18 | ENT-R0-12 | T-R0-024 | cross-sectional rows of one prediction_time never split |
| 25 | embargo separately justified; lookback not auto-added | FN-R0-18 | ENT-R0-12 | T-R0-025 | embargo buffer recorded with justification; lookback not auto-added |
| 26 | leakage tripwire (forward feature → IC≈0) | FN-R0-18 | ENT-R0-12 | T-R0-026 | synthetic forward-return feature at fold boundary → OOS IC ≈ 0 |
| 27 | trial registry append-only | FN-R0-20 | ENT-R0-13 | T-R0-027 | registry append-only; every config logged; mutation raises |
| 28 | batch-vs-latest value parity | FN-R0-16 | ENT-R0-10 | T-R0-028 | batch vs latest feature values equal within tolerance |
| 29 | primary = continuous regression | FN-R0-21 | ENT-R0-14 | T-R0-029 | baseline output is continuous return on ABSOLUTE_EXECUTABLE basis |
| 30 | comparator = pooled elastic-net; oracle prohibited | FN-R0-22 | ENT-R0-14 | T-R0-030, **T-R0-041** | pooled elastic-net grouped-by-test-date; per-date-oracle comparator rejected |
| 31 | output-specific calibration; ECE=NOT_APPLICABLE | FN-R0-23 | ENT-R0-15 | T-R0-031 | continuous calibration used; ECE=NOT_APPLICABLE_TO_PRIMARY_REGRESSION; Platt-on-regression raises |
| 32 | multiple-testing hurdle; DSR assessment | FN-R0-25 | ENT-R0-13/19 | T-R0-032 | hurdle from registry trial_count; DSR is a stat assessment; NOT_ESTIMABLE neither pass nor fail |
| 33 | contract-bound factor attribution | FN-R0-26 | ENT-R0-18 | T-R0-033 | all 13 §0.8 elements present; dependence-aware SEs used |
| 34 | investable benchmark beta-adj net-of-cost | FN-R0-27 | ENT-R0-16 | T-R0-034 | SPY+matched basket, beta-adjusted, net of same cost model |
| 35 | round-trip cost, exit leg, √impact | FN-R0-28 | ENT-R0-17 | T-R0-035 | round-trip cost includes exit/close-auction leg + √impact; PROXY floor |
| 36 | two-tier reproducibility + environment_hash | FN-R0-30 | ENT-R0-21 | T-R0-036 | environment_hash composition stable; symbolic BIT_EXACT, numeric tolerance |
| 37 | BLOCKED_NO_EDGE explicit path | FN-R0-29 | ENT-R0-19 | T-R0-037 | hurdle-not-cleared fixture → outcome=BLOCKED_NO_EDGE |
| 38 | effective-sample IC-IR | FN-R0-24 | ENT-R0-19 | T-R0-038 | overlapping-label fixture → effective-sample (block-bootstrap) IC-IR, not raw |
| 39 | run ledger append-only | FN-R0-31 | ENT-R0-20 | T-R0-039 | append-only hash chain; mutation raises |
| 40 | no threshold changed after results | FN-R0-29 | ENT-R0-19 | T-R0-040 | post-hoc threshold change → PreRegistrationMismatchError |

**Coverage:** all 40 requirements have ≥1 deterministic test. Corporate-action §0.6 clauses a–e map to T-R0-007 (a), T-R0-008 (b), T-R0-009 (c), T-R0-010 (d), T-R0-011 (e) — five distinct tests.

---

## 2. Live-provider tests (network-gated; excluded from the deterministic gate)

| Test | target | assertion (mechanics only — NO live value) |
|---|---|---|
| T-R0-L01 | FN-R0-01 | a live pull returns the canonical schema with the raw-basis flag set; **no assertion on any price/return value** |
| T-R0-L02 | FN-R0-03 | live frame passes dup/sort/tz validation mechanics; **no ticker-value assertion** |

**Rule (enforced):** no deterministic test may call the network or depend on a live ticker's looked-up value; all deterministic tests use committed fixtures. Live tests carry an opt-in marker (`@live_provider`) and run only in the dedicated `tests/live_provider/` job.

---

## 3. Golden fixtures (committed)
- `split_after_feature_date` (T-R0-006/009): a split whose ex_date is after the feature/prediction date.
- `dividend` (T-R0-010/012): a dividend with explicit treatment.
- `ticker_reuse` (T-R0-015): a ticker reassigned to a new entity across time → two instrument_ids.
- `then_delisted_cohort` (T-R0-014/016): a cohort containing a name delisted after `cohort_selection_date`.
- `later_ipo_exclusion` (T-R0-014): an instrument first eligible after `cohort_selection_date`.
- `labels_5_8_14` (T-R0-018/019/020): the worked-timestamp label fixture (matches VAL-R0-01).
- `overlapping_label_dependence` (T-R0-038): overlapping labels for effective-sample inference.
- `synthetic_forward_feature` (T-R0-026): forward-return feature at the fold boundary.
- `batch_vs_latest_parity` (T-R0-021/028): batch and single-row feature paths.
- `per_date_oracle_rejection` (T-R0-041): a comparator fit on test-fold rows → rejected as OOS/promotion.
- `blocked_no_edge` (T-R0-037): metrics below the pre-registered hurdle.

---

## 4. Definition of Done

### Per-slice DoD
- **R0-S1:** downstream receives only 1-D numeric canonical raw bars; raw-basis asserted; SourceRecord lineage present; T-R0-001..004 green.
- **R0-S2:** raw vintage immutable; as-of adjusted series versioned; every label/series carries price_basis; the five §0.6 clauses each pass (T-R0-005..012).
- **R0-S3:** survivorship-safe FIXED_PIT_COHORT with the §0.4 field set; opaque instrument_id + identifier history; terminal events handled; no dynamic-universe claim; T-R0-013..017 green. *(Data-source prerequisite per readiness-gate §C.)*
- **R0-S4:** matured-only labels on the declared basis; session-counting convention pinned with worked example; T-R0-018..020 green.
- **R0-S5:** value-parity + leakage tripwire green; folds obey interval-based purge + separately-justified embargo; trial registry exercised; T-R0-021..028 green.
- **R0-S6:** factor-attributed, net-of-cost report vs an investable benchmark with the multiple-testing-adjusted hurdle and output-specific calibration (ECE=NOT_APPLICABLE_TO_PRIMARY_REGRESSION), reproducible from a clean checkout; honest BLOCKED_NO_EDGE; T-R0-029..041 green.

### Global R0 DoD
All deterministic tests green · leakage tripwire green (T-R0-026) · value-parity green (T-R0-028) · two-tier reproducibility green (T-R0-036) · BLOCKED_NO_EDGE path exercised (T-R0-037) · no threshold changed after results (T-R0-040) · every R0-REQ traced to ≥1 deterministic test · every cited FN/ENT id resolves.

---

## 5. CI gate
- **Deterministic gate (required):** T-R0-001..T-R0-041 — no network, committed fixtures only. Blocks merge on any failure.
- **Live-provider job (opt-in, non-blocking):** T-R0-L01..L02 — network-gated, `@live_provider` marker, never asserts a live ticker value.
- **Reference-existence check:** every FN-R0/ENT-R0/T-R0 id cited across the contract set resolves to a defined contract (mirror of gate items G6/G7).
