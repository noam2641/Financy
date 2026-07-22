# 02 — Current-State Reconstruction & Gap Analysis

**Artifact type:** current-state reconstruction (Phase 2 output, lead-integrated).
**Primary source:** specialist `repository-architecture-discovery` (read-only, grounded
in repository files at audit HEAD `ba20eaf`), cross-checked against the lead's own
bootstrap reading. Provenance is marked where a conclusion is specialist-originated.
**Nothing here is a recommendation** — recommendations live in `04`/`05`.

---

## 1. What Financy actually is today

A **documentation-driven scaffold**. A maximalist canonical spec (`AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md`, v4.6, 5,599 lines) was distilled through an evidence→decision pipeline into a proposed **v5 architecture draft** and then into a **Release-0 "Edge Probe"** contract set. Quantitatively (per discovery):

- **Code:** 613 LOC across 4 `.py` files. **Tests:** 581 LOC, **174 passing** (150 entity + 24 time).
- **Documentation:** ≈10,200 lines across ~30 Markdown files — a **~17:1 docs-to-code ratio**.
- **Built:** 2 of 16 build tasks (TASK-R0-01 session counting, TASK-R0-02 entity schemas). The other 14 are contracted at a 40-field function-template level but have **no code and no test files**.

### Implemented (with tests)
| Capability | Contract | File | Tests |
|---|---|---|---|
| `count_exchange_sessions` (entry-index t+1=session 1; fail-closed; pinned `calendar_id`) | FN-R0-12 / FC-R0-01 | `src/financy/core/time.py` (110) | `test_time.py` (24) |
| 21 canonical entity **schemas** (frozen/slotted/kw-only dataclasses; closed enums; opaque `NewType` placeholders; narrow null/enum validation — **no writers/persistence/hashing/logic**) | ENT-R0-01..21 / FC-R0-02 | `src/financy/core/entities.py` (494) | `test_entities.py` (150) |

### Contracted, not built
All 31 functions (FN-R0-01..31) and 21 entity writers have contracts; only FN-R0-12 has code. **TASK-R0-03** (determinism `environment_hash` + hash-chained run ledger, FN-R0-30/31) and **TASK-R0-04** (provider adapter + raw OHLCV, FN-R0-01/02/03) are the next two and remain unstarted. Pipeline S1→S6 and the acyclic module DAG (FC-R0-01..21) are fully specified.

### Out of R0 scope (maximalist v4.6 only)
News/NLP, graph/relationship modeling, LLM components, deep/sequence models, paper/live execution, counterfactual reasoning, world-model/autonomous authority — all deferred to R1B–R4 in canonical §2, and explicitly excluded by `FILE_AND_MODULE_CONTRACT.md §3`.

## 2. The documentation-vs-code asymmetry (three places docs claim more than code delivers)
*(specialist-verified)*
1. **Phantom-code coverage matrix.** `REQUIREMENT_TO_CODE_COVERAGE_MATRIX.md` cites `IMPLEMENTED`/`PARTIALLY_IMPLEMENTED` code (`Technical Analysis.py:6990`, `stock_ai_4_files/*`, `news_analysis.py`, `lstmfinancy.py`, …) that **does not exist in the repo** (conflict CFL-04).
2. **Half-migrated enum.** PR #5 closed `RunLedgerEvent.event_type` to a six-value `RunLedgerEventType` in the *contract*, but `entities.py:113,472` still carries the open `RunLedgerEventTypeValue` `NewType`; substitution waits on the unbuilt TASK-R0-03. (Clean, honest state — not a defect.)
3. **Readiness gate** declares R0 "READY to begin" — true as *intent*, with 14/16 tasks unwritten.

## 3. Premature commitments the mission may need to reopen
*(each pinned in binding code or a BINDING contract — reopening any is a deliberate, test-breaking act)*
- **Horizons `{5,8,14}`** — frozen as a closed `IntEnum` (`entities.py:52-56`) and `SUPPORTED_HORIZONS` tuple (`time.py:16`).
- **Single continuous-return target** — `TargetBasis` has one member `ABSOLUTE_EXECUTABLE_RETURN` (`entities.py:59-60`); primary is BINDING continuous (MDL-R0-01).
- **Absolute (not sector/market) basis** for cost subtraction (ADR-004) — lives beside v4.6's still-untouched sector-excess default (conflict CFL-05, CRITICAL).
- **GBT-primary + closed `ModelProducer` set** (`entities.py:69-73`) — a sequence/graph challenger needs a new producer member (closed-enum change).
- **Pure fixed-horizon exit** (no barriers/MFE-MAE) — V3.3, FN-R0-13; barriers DEFERRED.
- **Interval-purge + separately-justified embargo** (§0.5) — a defensible but pinned leakage-control model.

## 4. Component verdicts — current R0 reassessment
*(specialist classification, lead-endorsed; full rationale/dependencies/invalidating-experiments in the discovery report and carried into `05`)*

**No component is REPLACE or REMOVE — the rigor is worth preserving.** Distribution:

| Verdict | Components |
|---|---|
| **KEEP_UNCHANGED** | PIT data posture; terminal events; purge (interval-overlap guard); walk-forward validation; `environment_hash` |
| **KEEP_AS_FOUNDATION** | exchange-session counting; provenance (`SourceRecord`); corporate actions (as-of/split-safe); FixedPITCohort; embargo policy; trial registry; GBT baseline; elastic-net comparator; round-trip cost; investable benchmark; run ledger |
| **EXTEND** | canonical entities (new content/source/graph entities + wider enums); identity/`instrument_master` (→ entity-resolution hub for text/social mentions); labels (richer target semantics); FeatureSnapshot (multimodal lineage + per-modality checksums); InformationInterval (per-modality `available_at` boundaries); regression calibration (add probability heads); factor attribution (add **incremental-value-over-price** test) |
| **DEFER** | Fama-MacBeth diagnostic (optional challenger, off critical path) |
| **REPLACE / REMOVE / REORDER** | *(none among existing components — reorder pressure comes only from new ingestion tasks slotting into S1/S3)* |

## 5. Constraints the refoundation must respect or explicitly revise
*(specialist-verified)*
- **Field-order pinned by fixtures** — `test_exact_ordered_fields` asserts exact field names *and order* vs `r0_entity_schema_fields.json`; any insert/reorder breaks a golden test (e.g. FixedPITCohortMember=9, InformationInterval=2+6 with forbidden `duration/embargo/feature_lookback/fold_id`, FactorAttributionResult=17).
- **Closed enums locked** by `test_closed_enum_values`; widening horizons/targets/producers/factors is a deliberate test-breaking change.
- **Open placeholders must stay opaque** (`test_open_placeholder_is_str_newtype_not_enum`); only the contracted `RunLedgerEventType` closure is authorized.
- **Audit-branch-not-`main` topology** — CI triggers only on `claude/trading-platform-audit-iawx0v`; `main` gets no CI and no merges. A refoundation branch inherits no CI unless the workflow filter is revised.
- **One-task-per-PR, test-first git operating model** — tests land before implementation; golden fixtures must not be rewritten to force a pass; `PARTIALLY_IMPLEMENTED→TESTED_RESEARCH` forbidden without a real test.
- **CI determinism gate** — offline, committed-fixtures-only, Py 3.10+3.12. New modalities (network ingestion, ML libs, GPU nondeterminism) must fit the two-tier reproducibility policy or be quarantined like the `@live_provider` job.
- **`dependencies = []`** — introducing numpy/pandas/sklearn/torch is a real dependency-and-determinism decision, not a free extension.

## 6. Valid foundations that must not be discarded
PIT correctness end-to-end · survivorship safety · leakage-safe validation (interval purge, grouping, embargo, fit-isolation, forward-feature tripwire) · honest statistics (effective-sample IC/IR, trial registry, DSR/PBO applicability, `NOT_ESTIMABLE`≠pass/fail) · economic realism (round-trip cost, investable benchmark, factor attribution) · reproducibility + audit (two-tier determinism, `environment_hash`, hash-chained ledger, pre-registration, **BLOCKED_NO_EDGE**) · governance disciplines (two-field status model, single-writer-per-entity, test-first, "maximalism is a release blocker", autonomous authority permanently REJECTED).

## 7. Gap analysis for the multimodal mission
*(specialist-identified; entirely absent from current design/code)*
- **Ingestion** of news/filings/social/**Telegram** — no module of any kind.
- **Event normalization** — no event taxonomy, dedup/clustering, or event-time model.
- **Source-reliability / trust** — no `source_profile`; the only provenance is raw `SourceRecord`.
- **Graph / relationship intelligence** — none; `FactorName` (6 fixed factors) is the only relational structure.
- **Historical-analog retrieval / memory** — none; nothing embeds or indexes historical states.
- **Multimodal fusion** — none; FeatureSnapshot is single-checksum, price-only in practice.
- **Sequence models** — none; no producer slot beyond GBT/elastic-net/Fama-MacBeth/oracle.
- **Richer target semantics** — only one continuous basis + `{5,8,14}`; no quantile *targets*, barrier-touch, or MFE/MAE path statistics.
- **Selective prediction / abstention beyond `BLOCKED_NO_EDGE`** — the outcome enum is run-level, not per-decision; no confidence/uncertainty gating, no cost-of-abstention.
- **Drift / OOD detection** — none; material safety gap under non-stationary text/social inputs.

**Cross-cutting:** the multimodal mission multiplies leakage/manipulation/multiple-testing surfaces, yet the safeguards that would catch them are exactly the components in §6 to preserve and §4-EXTEND. The single highest-leverage addition the current design lacks is a **per-modality availability-time + source-trust layer that plugs into the existing InformationInterval / FeatureSnapshot leakage machinery**, so new modalities inherit PIT/audit guarantees rather than circumventing them. *(specialist conclusion; the lead adopts it as the organizing principle for the target architecture.)*

---

## 8. Pre-read inventory (doc 01) vs the existing design
Required by the independent-thinking mandate: comparing the mission-first inventory against what the repo actually decided.

| Inventory question(s) | Status in current design | Note |
|---|---|---|
| Data PIT/leakage integrity (DA1,DA3,DA5); validation (RQ4); reproducibility/audit | **Answered well** | The R0 truth-kernel is precisely this; best-developed part of the repo. |
| Edge existence as falsifiable hypothesis (RQ1); cost realism (R1); honest stop (FM1) | **Answered well** | `BLOCKED_NO_EDGE`, pre-registration, round-trip cost, DSR — all first-class. |
| Target basis discipline (F3); no-mixed-basis cost math | **Answered well** | ADR-004 pins absolute-executable; strong. |
| Forecast object: distribution/path/quantiles/barrier/MFE-MAE (F1,F2) | **Decided too early / narrow** | One continuous scalar target; richer semantics DEFERRED or absent. |
| Horizons (F4,RQ5) | **Decided too early** | `{5,8,14}` frozen as provisional probe values but pinned in code+enums. |
| Modality coverage & fusion & interactions (F5,RQ2,RQ3) | **Ignored (by scope)** | R0 is price-only; news/social/graph/memory not contracted. |
| Missing-modality semantics (F7) | **Ignored** | No missingness model. |
| Per-decision abstention beyond run-level (D2) | **Partially answered** | Run-level outcome enum only; per-decision abstain is an R1A concern, uncontracted. |
| Source reliability, novelty, attention (DA6); manipulation defenses (R5,FM6) | **Ignored** | No trust/attention/manipulation model anywhere. |
| Drift/OOD (DA7,FM7) | **Ignored** | No detector. |
| Decision→action→sizing policy (D1,D3,D5); portfolio controls | **Partially answered** | Specified for R1A (deterministic policy) but out of R0; not contracted in detail. |
| Autonomy ladder (D6,P2); autonomous-execution prohibition (AS7) | **Answered well** | Explicit, permanently REJECTED. |
| Small-effective-sample premise (AS3) governing model complexity | **Assumed, not measured** | Load-bearing *inference*, not a measurement — flagged for the horizon/validation study. |

**New questions discovered during inspection** (not in the mission-first inventory):
- **NQ1.** How do new modalities *inherit* (not bypass) the InformationInterval/FeatureSnapshot leakage machinery? (the organizing gap.)
- **NQ2.** How is the closed-enum + pinned-field-order fixture regime evolved without turning every schema extension into golden-test churn — i.e., is the R0 schema-immutability discipline itself a scaling constraint for a multimodal entity model?
- **NQ3.** Does the incremental-value-over-price attribution test exist to stop a "news/graph edge" from being disguised price/factor beta? (currently no.)
- **NQ4.** Is the audit-branch-not-`main` topology and CI branch filter a long-term integration plan or an artifact to resolve before the platform grows?
