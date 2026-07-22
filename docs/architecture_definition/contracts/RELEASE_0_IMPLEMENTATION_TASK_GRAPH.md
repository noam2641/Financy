# RELEASE 0 — IMPLEMENTATION TASK GRAPH (TASK-R0)

*documentation-only; canonical v4.6 unmodified; governed by v5 §0; shared ID space per PHASE4_FOUNDATION; no code/src/tests created — this is the ORDER-OF-BUILD plan, not code.*

Two-field status model (v5 §0.1) applies. Sizes: **S** = one isolated coding session · **M** = one focused day · **L** = multi-session.

---

## 1. Task cards

### TASK-R0-01 — Exchange-session counting (FIRST) · size **S** · isolation **YES**
- **slice:** shared core · **implements:** FN-R0-12 · **entities:** — (pure) · **upstream deps:** none · **produces:** FC-R0-01 (`core/time.py`) + committed exchange-session calendar fixture + golden tests · **tests to green:** T-R0-018 · **DoD:** 5/8/14 worked examples (incl. Juneteenth 2023-06-19 and Independence Day 2023-07-04) pass; entry-index convention pinned (t+1 = session 1). · **status:** OWNER_APPROVED · BINDING · **risks:** none material.
- **Why first:** pure, deterministic, **no upstream and no external/network deps**, tiny surface; unblocks labels (TASK-R0-07) and the validation splitter (TASK-R0-09). Correct seed for the whole DAG.

### TASK-R0-02 — Entity schemas · size **M** · isolation **YES**
- **slice:** shared core · **implements:** the 21 schemas (ENT-R0-01..21) · **upstream:** none · **produces:** FC-R0-02 (`core/entities.py`) + schema tests · **tests:** schema presence for all 21 · **DoD:** every entity's key fields typed; FixedPITCohortMember carries exactly the nine §0.4 fields; **InformationInterval carries its two identity/context fields (`instrument_id`, `horizon_sessions`) plus the exact six §0.5 information-time fields**; FactorAttributionResult carries `run_id` plus the 16 §0.8 attribution fields; ModelArtifactManifest carries the `producer` discriminator; closed brace-listed enums are honored as closed vocabularies and open (unbraced) enums are left for the owning writer task. · **status:** OWNER_APPROVED · BINDING · **risks:** field drift → mitigated by pinning to the entity contract.

### TASK-R0-03 — Determinism + run ledger · size **M** · isolation **YES**
- **slice:** shared core · **implements:** FN-R0-30, FN-R0-31 · **entities:** ENT-R0-20, ENT-R0-21 · **upstream:** TASK-R0-02 · **produces:** FC-R0-03, FC-R0-04 · **tests:** T-R0-036, T-R0-039 · **DoD:** `RuntimeInfo` (non-entity input) is defined; the canonical SHA-256 environment-hash composition (six-field key set + canonical UTF-8 JSON) is pinned and produces a fixed 64-hex hash; **no hidden runtime introspection** in the core function (no clock/machine/env/network/filesystem); `RunLedger = tuple[RunLedgerEvent, ...]` state is explicit and immutable; event_id and timestamp are explicit inputs (tz-aware UTC, nondecreasing); the closed six-value `RunLedgerEventType` vocabulary `{RUN_STARTED, ARTIFACT_WRITTEN, TRIAL_APPENDED, FOLD_BUILT, MODEL_FIT, REPORT_GENERATED}` replaces the open placeholder for `RunLedgerEvent.event_type` (name/order preserved); canonical event hashing + genesis hash (`"0"*64`) + complete-chain validation; append-only behavior; duplicate-event (byte-equivalent) idempotency; conflicting event-ID reuse and tampering raise `LedgerMutationError`; T-R0-036 and T-R0-039 green. · **status:** OWNER_APPROVED · BINDING · **risks:** field drift → mitigated by pinning to the entity/function contracts.

### TASK-R0-04 — Provider adapter + raw normalization · size **M** · isolation **YES**
- **slice:** R0-S1 · **implements:** FN-R0-01/02/03 · **entities:** ENT-R0-01/02 · **upstream:** TASK-R0-02 · **produces:** FC-R0-05 + fixtures · **tests:** T-R0-001..004; live T-R0-L01/L02 · **DoD:** canonical 1-D raw bars; raw-basis asserted; dup/sort/tz handled; lineage present. · **status:** OWNER_APPROVED · BINDING · **risks:** provider quirks → isolated behind the adapter.

### TASK-R0-05 — Corp actions + as-of + split-safe returns · size **M** · isolation **YES**
- **slice:** R0-S2 · **implements:** FN-R0-04/05/06/07 · **entities:** ENT-R0-03/04 · **upstream:** TASK-R0-02, TASK-R0-04 · **produces:** FC-R0-06, FC-R0-07 + split/dividend fixtures · **tests:** T-R0-005..012 · **DoD:** as-of levels invariant to later split; §0.6a–e each pass. · **status:** OWNER_APPROVED · BINDING.

### TASK-R0-06 — Fixed-PIT cohort + identity · size **M** · isolation **YES**
- **slice:** R0-S3 · **implements:** FN-R0-08/09/10/11 · **entities:** ENT-R0-05/06/07/08 · **upstream:** TASK-R0-02, TASK-R0-05 · **produces:** FC-R0-08, FC-R0-09 + cohort/ticker-reuse fixtures · **tests:** T-R0-013..017 · **DoD:** FIXED_PIT_COHORT field set; then-delisted retained; later-IPO excluded; ticker-only join rejected; terminal events. · **status:** OWNER_APPROVED · BINDING · **risks:** constituent-source prerequisite (readiness-gate §C) is a sourcing task, not a code blocker.

### TASK-R0-07 — Fixed-horizon labels · size **M** · isolation **YES**
- **slice:** R0-S4 · **implements:** FN-R0-13/14 · **entities:** ENT-R0-09 · **upstream:** TASK-R0-01, TASK-R0-05, TASK-R0-06 · **produces:** FC-R0-10 + labels_5_8_14 fixture · **tests:** T-R0-009/012/018/019/020 · **DoD:** matured-only labels; pure fixed-horizon exit; §0.6c label-split fixture passes. · **status:** OWNER_APPROVED · BINDING.

### TASK-R0-08 — Feature snapshot + values checksum · size **M** · isolation **YES**
- **slice:** R0-S5 · **implements:** FN-R0-15/16 · **entities:** ENT-R0-10 · **upstream:** TASK-R0-02, TASK-R0-04 · **produces:** FC-R0-11 + batch_vs_latest_parity fixture · **tests:** T-R0-021/022/028 · **DoD:** schema hash + values checksum; fit-isolation; value-parity. · **status:** OWNER_APPROVED · BINDING.

### TASK-R0-09 — Validation splitter (interval-based purge + embargo) · size **L** · isolation **YES**
- **slice:** R0-S5 · **implements:** FN-R0-17/18/19 · **entities:** ENT-R0-11/12 · **upstream:** TASK-R0-01, TASK-R0-07 · **produces:** FC-R0-12 + synthetic_forward_feature fixture · **tests:** T-R0-023/024/025/026 · **DoD:** no train/test interval overlap; same prediction_time one group; embargo justified; leakage tripwire OOS IC≈0. · **status:** OWNER_APPROVED · BINDING · **risks:** the core correctness slice — highest care.

### TASK-R0-10 — Trial registry · size **S** · isolation **YES**
- **slice:** R0-S5 · **implements:** FN-R0-20 · **entities:** ENT-R0-13 · **upstream:** TASK-R0-02, TASK-R0-03 · **produces:** FC-R0-13 · **tests:** T-R0-027 · **DoD:** append-only; every config logged. · **status:** OWNER_APPROVED · BINDING.

### TASK-R0-11 — Round-trip cost model · size **M** · isolation **YES**
- **slice:** R0-S6 · **implements:** FN-R0-28 · **entities:** ENT-R0-17 · **upstream:** TASK-R0-02, TASK-R0-04 · **produces:** FC-R0-20 · **tests:** T-R0-035 · **DoD:** round-trip cost with exit/close-auction leg + √impact; PROXY floor. · **status:** OWNER_APPROVED (structure) · BINDING; numbers EMPIRICAL_TBD (EXP-3).

### TASK-R0-12 — Models: GBT baseline + pooled elastic-net comparator · size **L** · isolation **YES**
- **slice:** R0-S6 · **implements:** FN-R0-21/22 · **entities:** ENT-R0-14 · **upstream:** TASK-R0-08, TASK-R0-09 · **produces:** FC-R0-14, FC-R0-15 + per_date_oracle_rejection fixture · **tests:** T-R0-029/030/041 · **DoD:** continuous-regression baseline; pooled elastic-net grouped-by-test-date; per-date oracle rejected. · **status:** EMPIRICAL_TBD · PROVISIONAL_DEFAULT.

### TASK-R0-13 — Regression calibration + intervals · size **M** · isolation **YES**
- **slice:** R0-S6 · **implements:** FN-R0-23 · **entities:** ENT-R0-15 · **upstream:** TASK-R0-09, TASK-R0-12 · **produces:** FC-R0-16 · **tests:** T-R0-031 · **DoD:** residual/quantile/interval calibration; ECE=NOT_APPLICABLE_TO_PRIMARY_REGRESSION; Platt-on-regression rejected; disjoint fit/eval. · **status:** EMPIRICAL_TBD · PROVISIONAL_DEFAULT.

### TASK-R0-14 — Stats: effective sample + multiple-testing hurdle · size **M** · isolation **YES**
- **slice:** R0-S6 · **implements:** FN-R0-24/25 · **entities:** ENT-R0-13 (read) · **upstream:** TASK-R0-10, TASK-R0-12 · **produces:** FC-R0-17 · **tests:** T-R0-032/038 · **DoD:** effective-sample IC-IR; applicable_multiple_testing_adjusted_hurdle from registry; DSR assessment; NOT_ESTIMABLE handled. · **status:** OWNER_APPROVED · BINDING.

### TASK-R0-15 — Factor attribution + investable benchmark · size **L** · isolation **YES**
- **slice:** R0-S6 · **implements:** FN-R0-26/27 · **entities:** ENT-R0-16/18 · **upstream:** TASK-R0-11, TASK-R0-12 · **produces:** FC-R0-18, FC-R0-19 · **tests:** T-R0-033/034 · **DoD:** all 13 §0.8 attribution elements; dependence-aware SEs; SPY+basket beta-adjusted net-of-cost benchmark. · **status:** OWNER_APPROVED · BINDING.

### TASK-R0-16 — Evaluation report + BLOCKED_NO_EDGE + reproducibility · size **M** · isolation **YES**
- **slice:** R0-S6 · **implements:** FN-R0-29 · **entities:** ENT-R0-19 · **upstream:** TASK-R0-03, TASK-R0-13, TASK-R0-14, TASK-R0-15 · **produces:** FC-R0-21 + blocked_no_edge fixture · **tests:** T-R0-037/040 (+ consumes 031/032/033/034/036/038) · **DoD:** reproducible report vs investable benchmark; honest BLOCKED_NO_EDGE; no threshold changed after results. · **status:** OWNER_APPROVED · BINDING.

---

## 2. DAG (adjacency + topological order)

**Adjacency (task → upstream deps):**

| TASK | upstream |
|---|---|
| 01 | — |
| 02 | — |
| 03 | 02 |
| 04 | 02 |
| 05 | 02, 04 |
| 06 | 02, 05 |
| 07 | 01, 05, 06 |
| 08 | 02, 04 |
| 09 | 01, 07 |
| 10 | 02, 03 |
| 11 | 02, 04 |
| 12 | 08, 09 |
| 13 | 09, 12 |
| 14 | 10, 12 |
| 15 | 11, 12 |
| 16 | 03, 13, 14, 15 |

**Topological build order:** 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16.
Every task's upstream deps appear strictly earlier → **no cycles** (DAG confirmed). This matches the module DAG in the file-and-module contract.

**Critical path:** 02 → 04 → 05 → 06 → 07 → 09 → 12 → 13/14/15 → 16.
**Parallelizable:** {01} ∥ {02}; after 02: {03, 04}; {08, 11} run alongside the S3/S4 chain once 04 is done; {10} runs after 03; {13, 14, 15} run in parallel after 12.

---

## 3. Gating (out of scope at the task level)
No task builds news/graph/LLM/deep-learning/paper-trading/counterfactual/world-model capability. Those are DEFERRED/REJECTED · NOT_IN_SCOPE and appear in no task, edge, or fixture above.

---

## 4. Handoff to implementation
After this task graph the next action is to implement **TASK-R0-01 only**, in isolation, against FN-R0-12 and the readiness-gate/validation contracts (worked 5/8/14 examples). **No code is written in this Phase-4 deliverable** — implementation begins in a separate, explicitly authorized coding session.
