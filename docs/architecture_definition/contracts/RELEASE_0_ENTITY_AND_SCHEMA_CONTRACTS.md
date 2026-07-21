# RELEASE 0 — ENTITY AND SCHEMA CONTRACTS (ENT-R0)

*documentation-only; canonical v4.6 unmodified; governed by v5 §0; shared ID space per PHASE4_FOUNDATION; no code/src/tests created.*

Two-field status model (v5 §0.1) applies. Each entity contract assesses: id · name · owning_module (FC) · allowed_writer · readers · immutability · PIT role · key fields (name:type:units/basis) · identity key · versioning · determinism · lineage · leakage risks + mitigation · v5/§0 refs · v4.6 REQ · ADR · decision_status · posture · required tests. All entity **schemas** are defined in FC-R0-02 (`core/entities.py`); the "owning_module" is the runtime **writer** module.

---

### ENT-R0-01 SourceRecord
- **owning/writer:** FC-R0-05 · **readers:** FC-R0-06, FC-R0-08, FC-R0-09 · **immutability:** immutable (append-only) · **PIT role:** provenance/lineage of a raw pull.
- **key fields:** `source_id:str`, `provider:str`, `endpoint:str`, `request_params:json`, `pull_timestamp:datetime[UTC]`, `is_estimated_timestamp:bool`, `raw_payload_hash:str`.
- **identity:** `source_id` · **versioning:** `pull_timestamp` · **determinism:** BIT_EXACT · **lineage:** — (root).
- **leakage:** fabricating availability timestamps → forbidden; `is_estimated_timestamp` flags estimates (V5.4).
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-04. · **refs:** V5.4; REQ-DATA-001; ADR-007.

### ENT-R0-02 RawOHLCVBar
- **owning/writer:** FC-R0-05 · **readers:** FC-R0-07, FC-R0-09, FC-R0-11, FC-R0-20 · **immutability:** immutable raw vintage · **PIT role:** base tradable prices.
- **key fields:** `instrument_id:str`, `session_date:date`, `open/high/low/close:decimal[price]`, `volume:int`, `price_basis:enum=RAW`, `source_id:str`.
- **identity:** (`instrument_id`,`session_date`) · **versioning:** raw immutable · **determinism:** BIT_EXACT · **lineage:** ENT-R0-01.
- **leakage:** raw-basis only (`auto_adjust=False`); back-adjusted data never stored here.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-01/02/03. · **refs:** V5.1; REQ-PRICE-001..006; ADR-006.

### ENT-R0-03 CorporateActionRecord
- **owning/writer:** FC-R0-06 · **readers:** FC-R0-07 · **immutability:** append-only, versioned · **PIT role:** as-of adjustment inputs.
- **key fields:** `instrument_id:str`, `action_type:enum{SPLIT,DIVIDEND,MERGER,SPINOFF}`, `ex_date:date`, `split_adjustment_factor:decimal`, `dividend_amount:decimal[cash]`, `dividend_treatment:enum`, `corporate_action_version:str`, `source_id:str`.
- **identity:** (`instrument_id`,`action_type`,`ex_date`,`corporate_action_version`) · **versioning:** `corporate_action_version` · **determinism:** BIT_EXACT · **lineage:** ENT-R0-01.
- **leakage:** only actions with `ex_date ≤ cutoff` used downstream; dividends need explicit `dividend_treatment` (§0.6d).
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-05/06/10. · **refs:** §0.6; REQ-PRICE-002/003; ADR-006.

### ENT-R0-04 DerivedPriceSeriesMetadata
- **owning/writer:** FC-R0-07 · **readers:** FC-R0-10, FC-R0-11, FC-R0-19, FC-R0-20 · **immutability:** derived (reproducible) · **PIT role:** describes an as-of adjusted series.
- **key fields:** `instrument_id:str`, `as_of_cutoff:date`, `corporate_action_version:str`, `price_basis:enum`, `dividend_treatment:enum`, `derivation_hash:str`.
- **identity:** (`instrument_id`,`as_of_cutoff`,`corporate_action_version`) · **determinism:** BIT_EXACT (deterministic derivation) · **lineage:** ENT-R0-02, ENT-R0-03.
- **leakage:** as-of derivation binds to `ex_date ≤ as_of_cutoff`; back-adjusted vintage prohibited for levels/filters/universe/labels (§0.6e).
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-06/07/08/11/12. · **refs:** §0.6; REQ-PRICE-002/003; ADR-006.

### ENT-R0-05 InstrumentMasterRecord
- **owning/writer:** FC-R0-09 · **readers:** FC-R0-08 · **immutability:** append-only · **PIT role:** opaque canonical identity.
- **key fields:** `instrument_id:str(opaque)`, `first_seen:date`, `asset_type:enum`, `primary_exchange:str`.
- **identity:** `instrument_id` (never derived from ticker) · **determinism:** BIT_EXACT · **lineage:** ENT-R0-01/02.
- **leakage:** ticker-only joins prohibited (identity via `instrument_id`).
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-15. · **refs:** V6.2; REQ-DOM-015/016; ADR-008.

### ENT-R0-06 InstrumentIdentifierRecord
- **owning/writer:** FC-R0-09 · **readers:** FC-R0-08 · **immutability:** append-only, as-of history · **PIT role:** resolves ticker/CIK/FIGI as-of date.
- **key fields:** `instrument_id:str`, `identifier_type:enum{TICKER,CIK,FIGI}`, `identifier_value:str`, `valid_from:date`, `valid_to:date|null`.
- **identity:** (`instrument_id`,`identifier_type`,`valid_from`) · **determinism:** BIT_EXACT · **lineage:** ENT-R0-05.
- **leakage:** ticker-reuse across time → two distinct `instrument_id`s; as-of resolution only.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-15. · **refs:** V6.2; REQ-DOM-015/016; ADR-008.

### ENT-R0-07 FixedPITCohortMember
- **owning/writer:** FC-R0-08 · **readers:** FC-R0-10 · **immutability:** immutable signed manifest · **PIT role:** the fixed PIT cohort (§0.4).
- **key fields (§0.4):** `cohort_selection_date:date`, `universe_definition_version:str`, `eligibility_rule_version:str`, `constituent_source_id:str`, `source_as_of:date`, `instrument_id:str`, `inclusion_reason:str`, `exclusion_reason:str|null`, `terminal_event_policy:enum`.
- **identity:** (`universe_definition_version`,`instrument_id`) · **versioning:** `universe_definition_version` · **determinism:** BIT_EXACT · **lineage:** ENT-R0-01, ENT-R0-05.
- **leakage:** membership uses only info available at `cohort_selection_date`; later-delisted retained, later-IPO excluded; no dynamic-universe claim; manual enumeration only as immutable signed manifest with per-instrument provenance.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-13/14/17. · **refs:** §0.4; REQ-DOM-017; ADR-008.

### ENT-R0-08 TerminalEventRecord
- **owning/writer:** FC-R0-09 · **readers:** FC-R0-10 · **immutability:** append-only · **PIT role:** delisting/merger/bankruptcy terminal returns.
- **key fields:** `instrument_id:str`, `event_type:enum{DELIST,MERGER,BANKRUPT}`, `event_date:date`, `terminal_return:decimal[bps]`, `terminal_value_source:str`.
- **identity:** (`instrument_id`,`event_type`,`event_date`) · **determinism:** BIT_EXACT · **lineage:** ENT-R0-01/05.
- **leakage:** terminal events produce returns, never silently-missing labels.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-16. · **refs:** V6.3; REQ-LAB-013; ADR-008.

### ENT-R0-09 LabelRecord
- **owning/writer:** FC-R0-10 · **readers:** FC-R0-12, FC-R0-14, FC-R0-15, FC-R0-16 · **immutability:** derived (reproducible) · **PIT role:** supervised target.
- **key fields:** `instrument_id:str`, `prediction_time:datetime`, `horizon_sessions:enum{5,8,14}`, `label_value:decimal[bps]`, `price_basis:enum`, `target_basis:enum=ABSOLUTE_EXECUTABLE_RETURN`, `maturity_status:enum{MATURED,NOT_MATURED,TERMINAL_EVENT}`, `label_available_at:datetime`, `target_definition_version:str`.
- **identity:** (`instrument_id`,`prediction_time`,`horizon_sessions`,`target_definition_version`) · **determinism:** BIT_EXACT · **lineage:** ENT-R0-04, ENT-R0-07, ENT-R0-08.
- **leakage:** label spanning a split uses declared as-of adjustment (§0.6c); last-N rows NOT_MATURED; `label_available_at` respected by the splitter.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-09/12/18/19/20. · **refs:** §0.6c, V4.1; REQ-LAB-001; ADR-005/006.

### ENT-R0-10 FeatureSnapshot
- **owning/writer:** FC-R0-11 · **readers:** FC-R0-12, FC-R0-14, FC-R0-15 · **immutability:** immutable snapshot · **PIT role:** PIT feature values + fit-isolation.
- **key fields:** `snapshot_id:str`, `as_of_date:date`, `schema_hash:str`, `feature_values_checksum:str`, `fitted_transform_ref:str`, `fit_indices_ref:str`.
- **identity:** `snapshot_id` · **determinism:** BIT_EXACT · **lineage:** ENT-R0-02, ENT-R0-04.
- **leakage:** fit-isolation of scalers/imputers/calibrators/meta-learners (fit-indices ⊆ training window); schema hash **and** values checksum defend against train/serve skew (VAL-R0-08).
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-21/22/28. · **refs:** V14.4; REQ-FEAT-003; ADR-006/013.

### ENT-R0-11 InformationInterval
- **owning/writer:** FC-R0-12 · **readers:** FC-R0-12 (splitter) · **immutability:** derived · **PIT role:** per-sample information-time envelope (§0.5).
- **key fields (§0.5):** `feature_information_start:date`, `prediction_time:datetime`, `label_start:date`, `label_end:date`, `label_available_at:datetime`, `information_interval:[date,date]`.
- **identity:** (`instrument_id`,`prediction_time`,`horizon_sessions`) · **determinism:** BIT_EXACT · **lineage:** ENT-R0-09, ENT-R0-10.
- **leakage:** basis of the no-overlap guarantee (VAL-R0-02); embargo buffer separately justified (VAL-R0-03).
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-23/25. · **refs:** §0.5; REQ-VAL-001/002; ADR-013.

### ENT-R0-12 FoldManifest
- **owning/writer:** FC-R0-12 · **readers:** FC-R0-14, FC-R0-15, FC-R0-16 · **immutability:** immutable per run · **PIT role:** train/test index sets + embargo justification.
- **key fields:** `fold_id:str`, `train_prediction_times:list`, `test_prediction_times:list`, `embargo_buffer_sessions:int`, `embargo_justification:str`, `no_overlap_asserted:bool`.
- **identity:** `fold_id` · **determinism:** BIT_EXACT · **lineage:** ENT-R0-11.
- **leakage:** no train/test information-interval overlap; same-`prediction_time` rows one group.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-23/24/25/26. · **refs:** §0.5; REQ-VAL-001/002; ADR-013.

### ENT-R0-13 TrialRecord
- **owning/writer:** FC-R0-13 · **readers:** FC-R0-17 · **immutability:** append-only · **PIT role:** multiple-testing accounting.
- **key fields:** `trial_id:str`, `config_hash:str`, `seed:int`, `horizon:int`, `target_basis:enum`, `chosen_after_backtest:bool`, `created_event_ref:str`.
- **identity:** `trial_id` · **determinism:** BIT_EXACT · **lineage:** ENT-R0-20 (ledger).
- **leakage:** any value chosen after viewing a backtest is a logged trial; feeds the multiple-testing hurdle.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-27/32. · **refs:** §0.7, V7.2; REQ-VAL-008; ADR-013.

### ENT-R0-14 ModelArtifactManifest
- **owning/writer:** **model-training layer** — FC-R0-14 (FN-R0-21) for `producer=BASELINE_GBT`; FC-R0-15 (FN-R0-22) for `producer∈{COMPARATOR_ELASTICNET,COMPARATOR_FAMA_MACBETH}`. Single-writer preserved by the **`producer` discriminator** (one manifest per fitted artifact). · **readers:** FC-R0-16, FC-R0-17, FC-R0-18, FC-R0-21 · **immutability:** immutable artifact record.
- **key fields:** `artifact_id:str`, `producer:enum{BASELINE_GBT,COMPARATOR_ELASTICNET,COMPARATOR_FAMA_MACBETH,PER_DATE_ORACLE}`, `model_family:str`, `train_fold_ref:str`, `hyperparameters:json`, `seed:int`, `artifact_hash:str`, `environment_hash:str`, `oos_eligible:bool`.
- **identity:** `artifact_id` · **determinism:** TOLERANCE_NUMERIC (fitted) · **lineage:** ENT-R0-09, ENT-R0-10, ENT-R0-12.
- **leakage:** `producer=PER_DATE_ORACLE` ⇒ `oos_eligible=false` (prohibited as OOS/promotion baseline, MDL-R0-05); comparators fit on training dates only.
- **status:** EMPIRICAL_TBD · PROVISIONAL_DEFAULT (GBT & elastic-net working defaults) · **tests:** R0-REQ-29/30. · **refs:** §0.3; REQ-MOD-001/002; ADR-010.

### ENT-R0-15 CalibrationArtifactManifest
- **owning/writer:** FC-R0-16 · **readers:** FC-R0-21 · **immutability:** immutable artifact record · **PIT role:** output-specific calibration record.
- **key fields:** `output_name:str`, `output_type:enum{CONTINUOUS_RETURN,PROBABILITY}`, `method:str`, `target:str`, `fit_set_id:str`, `calibration_set_id:str`, `eval_set_id:str`, `units:str`, `metric:str`, `ece_value:enum|float=NOT_APPLICABLE_TO_PRIMARY_REGRESSION(when no probability head)`.
- **identity:** (`output_name`,`method`,`fit_set_id`) · **determinism:** TOLERANCE_NUMERIC · **lineage:** ENT-R0-09, ENT-R0-12, ENT-R0-14.
- **invariant:** `calibration_set_id (fit) ∩ eval_set_id = ∅`; CONTINUOUS_RETURN → residual/quantile/interval metric; PROBABILITY → Platt/isotonic + ECE (MDL-R0-06/07).
- **status:** EMPIRICAL_TBD · PROVISIONAL_DEFAULT · **tests:** R0-REQ-31. · **refs:** §0.2, V8.2; REQ-MOD-003/005; ADR-010.

### ENT-R0-16 BenchmarkDefinition
- **owning/writer:** FC-R0-19 · **readers:** FC-R0-18, FC-R0-21 · **immutability:** versioned · **PIT role:** investable benchmark spec.
- **key fields:** `benchmark_id:str`, `components:list{SPY,matched_basket}`, `beta_adjustment:decimal`, `cost_model_ref:str`, `rebalance_timing:str`, `eligibility_rule:str`.
- **identity:** `benchmark_id` · **determinism:** TOLERANCE_NUMERIC · **lineage:** ENT-R0-04, ENT-R0-17.
- **leakage:** cost parity + beta matching with the strategy (§0.8 items 9–10).
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-34. · **refs:** §0.8, V7.4; REQ-VAL-004; ADR-013.

### ENT-R0-17 CostModelDefinition
- **owning/writer:** FC-R0-20 · **readers:** FC-R0-18, FC-R0-19, FC-R0-21 · **immutability:** versioned · **PIT role:** round-trip cost.
- **key fields:** `cost_model_id:str`, `commission_bps:decimal`, `spread_bps:decimal`, `impact_coefficient:decimal(√-impact)`, `exit_leg:enum{CLOSE_AUCTION,...}`, `proxy_floor_bps:decimal`, `version:str`.
- **identity:** `cost_model_id` · **determinism:** TOLERANCE_NUMERIC · **lineage:** ENT-R0-02, ENT-R0-04.
- **leakage:** round-trip (two-sided), explicit exit/close-auction leg, √impact; PROXY carries a conservative numeric floor.
- **status:** OWNER_APPROVED (structure) · BINDING; numbers EMPIRICAL_TBD · PROVISIONAL_DEFAULT · **tests:** R0-REQ-35. · **refs:** V11.1; REQ-COST-001..003; ADR-014.

### ENT-R0-18 FactorAttributionResult
- **owning/writer:** FC-R0-18 · **readers:** FC-R0-21 · **immutability:** immutable per run · **PIT role:** residual-alpha evidence.
- **key fields (§0.8):** `return_frequency`, `regression_window`, `factor_set:list{Mkt,SMB,HML,UMD,STRev,BAB}`, `factor_source_versions`, `alpha_interpretation`, `standard_error_method(dependence-aware)`, `matched_basket_ref`, `long_short_leg_policy`, `turnover_matching`, `cost_parity_ref`, `beta_matching`, `rebalance_timing`, `benchmark_eligibility`, `missing_factor_behavior`, `residual_alpha_bps`, `residual_alpha_significance`.
- **identity:** (`run_id`,`factor_source_versions`) · **determinism:** TOLERANCE_NUMERIC · **lineage:** ENT-R0-14, ENT-R0-16, ENT-R0-17.
- **leakage:** residual alpha is net-of-cost; dependence-aware SEs.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-33. · **refs:** §0.8, V7.4; REQ-VAL-004; ADR-013.

### ENT-R0-19 EvaluationReport
- **owning/writer:** FC-R0-21 · **readers:** owner/governance · **immutability:** immutable per run · **PIT role:** terminal evidence artifact.
- **key fields:** `run_id:str`, `forecast_metrics:json`, `calibration_block:json`, `comparator_block:json`, `hurdle_block:json`, `attribution_ref:str`, `benchmark_ref:str`, `outcome:enum{EDGE_SUPPORTED,BLOCKED_NO_EDGE,INCONCLUSIVE}`, `pre_registration_ref:str`, `environment_hash:str`.
- **identity:** `run_id` · **determinism:** BIT_EXACT symbolic + TOLERANCE_NUMERIC metrics · **lineage:** ENT-R0-14/15/16/17/18/20.
- **leakage:** outcome derived from the frozen pre-registration snapshot; ECE recorded `NOT_APPLICABLE_TO_PRIMARY_REGRESSION` absent a probability head.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-31/32/37/40. · **refs:** §0.2/§0.7; REQ-VAL-004/008; ADR-013.

### ENT-R0-20 RunLedgerEvent
- **owning/writer:** FC-R0-04 · **readers:** FC-R0-13, FC-R0-21, audit · **immutability:** append-only, hash-linked · **PIT role:** tamper-evident run trail.
- **key fields:** `event_id:str`, `event_type:enum`, `prior_event_hash:str`, `payload_hash:str`, `environment_hash:str`, `timestamp:datetime`.
- **identity:** `event_id` · **determinism:** BIT_EXACT · **lineage:** ENT-R0-21.
- **leakage:** append-only hash chain (no mutation).
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-39. · **refs:** V14.4; REQ-SCH-027; ADR-016.

### ENT-R0-21 RuntimeEnvironmentManifest
- **owning/writer:** FC-R0-03 · **readers:** FC-R0-04, FC-R0-21 · **immutability:** immutable per run · **PIT role:** reproducibility key.
- **key fields:** `environment_hash:str`, `interpreter_version:str`, `dependency_lockfile_hash:str`, `os_arch:str`, `blas_threading_flags:str`, `random_seeds:json`, `data_vintage_ids:list`.
- **identity:** `environment_hash` · **determinism:** BIT_EXACT · **lineage:** — (root of repro).
- **leakage:** two-tier reproducibility anchor.
- **status:** OWNER_APPROVED · BINDING · **tests:** R0-REQ-36. · **refs:** V14.2/V14.3; REQ-GATE-001; ADR-016.

---

## Entity coverage & single-writer note
All 21 entities (ENT-R0-01..21) are contracted above with a single allowed_writer, **except** ENT-R0-14 whose two candidate writers are disambiguated by the mandatory `producer` discriminator (one manifest per fitted artifact), preserving single-writer-per-instance semantics. Every ENT is referenced by ≥1 FN (reads/writes) and ≥1 test.
