# AI Trading Decision Platform

Canonical Normative Specification v4.6

Status: canonical decision-operating-system, data-model, and implementation-contract specification. Numeric production thresholds remain `TBD` until frozen before final holdout access.  
Conversation coverage: v4.6 integrates the v4.4 concrete pipeline, technical-analysis, sequence-model, graph/macro, FinBERT/content, DataFrame-normalization, checkpoint/retry, and operator-tool contracts into the platform-infrastructure, Control Plane, Temporal Data, capability/plugin, bounded-context, runtime-manifest, and promotion architecture while preserving the small Decision Kernel boundary.  
Primary scope: long-only US equities, swing trading horizons of 5, 8, and 14 exchange trading sessions.  
Primary objective: operate a point-in-time-safe decision system that decides, abstains, executes under control, and learns from actual and counterfactual outcomes.

Important boundary: this document defines a software, research, and operational control system. It is not financial, legal, tax, regulatory, or investment advice. External distribution, broker connection, client-facing recommendations, or live trading require qualified legal, compliance, data-licensing, and risk review.

## 0. Authority, Language, and Traceability

REQ-GEN-001: This document is the single canonical source for the target system. Earlier files such as `TECHNICAL_REQUIREMENTS_V2`, `IMPLEMENTATION_CONTRACT_V3`, and `COMPLETE_SPECIFICATION_V3` are historical drafts.

REQ-GEN-002: If any older document conflicts with this document, this document is authoritative.

REQ-GEN-003: Requirement keywords are normative:

```text
MUST    = mandatory requirement
SHOULD  = mandatory unless a documented exception is approved
MAY     = optional capability
BLOCKER = prevents promotion to the next release
TBD     = must be finalized before the relevant gate can be passed
```

REQ-GEN-004: Each implementable requirement SHOULD be traceable using:

```text
requirement_id
design_component
implementation_task_id
test_id
release
owner
approval_status
```

REQ-GEN-005: Any threshold shown as `PLACEHOLDER_NON_NORMATIVE` MUST NOT be used for final holdout evaluation, paper trading approval, or production approval.

---

## 1. Product Scope and Non-Goals

REQ-PROD-001: The platform MUST answer:

```text
Does this instrument have enough risk-adjusted, cost-adjusted, execution-aware expected utility
to justify a portfolio action now?
```

REQ-PROD-002: The platform MUST also answer:

```text
What does the system believe about the market state?
Which independent evidence supports or contradicts the opportunity?
Should the system act, abstain, defer pending information, or learn from a non-action?
Was a poor result caused by forecast error, decision-policy error, portfolio-construction error, or execution error?
Which system component added marginal value?
What would likely have happened under approved alternative policies?
```

REQ-PROD-003: The product is a Decision Operating System with a Counterfactual Learning Factory, not only a recommendation generator.

REQ-PROD-004: The competitive advantage SHOULD come from:

```text
market world-state understanding
independent evidence generation
disciplined abstention
learning from executed and unexecuted decisions
error decomposition
counterfactual policy evaluation
module marginal-value measurement
human-system collaboration analytics
```

REQ-PROD-005: Forecasts are inputs to a decision policy that also includes uncertainty, costs, liquidity, portfolio state, risk policy, execution feasibility, governance status, data quality, market world state, evidence independence, and learning feedback.

REQ-PROD-006: `NO_ACTION` MUST be treated as a valid and valuable output.

REQ-PROD-007: Release 0-3 are long-only. Short selling is out of scope until a separate short-selling specification is approved.

REQ-PROD-008: Fully autonomous live trading without manual approval is out of scope.

REQ-PROD-009: Any client-facing or third-party recommendation workflow is out of scope until legal and regulatory classification is completed.

### 1.1 Operating Worlds

REQ-PROD-010: The platform MUST separate three operating worlds:

```text
RESEARCH_FACTORY
DECISION_RUNTIME
LEARNING_AND_COUNTERFACTUAL_LAB
```

REQ-PROD-011: `RESEARCH_FACTORY` is the only world allowed to develop features, test targets, train experimental models, tune hyperparameters, compare policies, and run exploratory experiments.

REQ-PROD-012: `DECISION_RUNTIME` MUST be deterministic and controlled. It may load only approved artifacts, produce forecasts, run decision/risk/revalidation policies, perform paper execution, and write decision ledger events.

REQ-PROD-013: `DECISION_RUNTIME` MUST NOT train experimental models, choose hyperparameters, mutate policy thresholds, or consume unapproved research artifacts.

REQ-PROD-014: `LEARNING_AND_COUNTERFACTUAL_LAB` MUST learn from:

```text
executed
approved_but_not_filled
rejected_by_human
blocked_by_risk
watchlist
no_edge
data_unavailable
NO_ACTION
```

REQ-PROD-015: Learning outputs MUST be promoted through governance before they can influence `DECISION_RUNTIME`.

### 1.2 Reference Operating Planes

REQ-PROD-016: The reference architecture MUST include the following logical planes:

```text
Point-in-Time Data and Events Plane
Market World Model Plane
Evidence Plane
Decision Plane
Opportunity Memory and Graph Plane
Portfolio Plane
Execution Digital Twin
Decision Ledger and Counterfactual Learning Plane
Control Plane
```

REQ-PROD-017: The planes are logical boundaries. Early releases SHOULD implement them as a modular monolith with strict module contracts unless physical service separation is justified.

REQ-PROD-018: The system SHOULD split a module into a separately deployed service only when at least one condition is true:

```text
independent_scaling_required
failure_isolation_required
security_boundary_required
different_deployment_cadence_required
broker_execution_isolation_required
real_team_ownership_boundary_exists
```

REQ-PROD-019: Broker execution is the strongest early candidate for physical separation. Research, forecasting, decision, risk, portfolio, learning, and governance SHOULD remain modular-monolith modules until operational evidence justifies separation.

### 1.3 Decision Kernel and Replaceable Capabilities

REQ-PROD-020: The architecture MUST define a small, stable `Decision Kernel`.

The Decision Kernel includes only:

```text
Temporal Snapshot
Decision Cycle
Forecast Distribution
Policy Evaluation
Portfolio Constraints
Execution Feasibility
Decision Ledger
```

REQ-PROD-021: The Decision Kernel MUST NOT be expanded merely because a component is operationally required. Required platform infrastructure, Control Plane components, and Temporal Data components may be mandatory for a release while remaining outside the Decision Kernel.

REQ-PROD-022: Everything outside the Decision Kernel MUST be classified as platform infrastructure, Control Plane, Temporal Data, replaceable capability, research candidate, or operator tooling unless explicitly promoted into the kernel through governance.

Initial replaceable capabilities:

```text
Technical Expert
News Expert
Market World Model
Opportunity Memory
Knowledge Graph
Options Expert
Fundamental Expert
LLM Explanation
Counterfactual Evaluator
```

REQ-PROD-023: The system MUST continue to operate in a valid degraded mode if the market world model, news model, graph model, LLM explanation layer, or forecast model implementation is replaced, disabled, or rolled back.

REQ-PROD-024: A capability MAY become required for a specific action, release, or portfolio policy, but that requirement MUST be declared in `capability_health_policy` and `runtime_manifest`.

REQ-PROD-025: The advantage of the system MUST NOT depend on lock-in to a single model family, data vendor, expert module, graph implementation, or explanation provider.

---

## 2. Release Roadmap

### 2.0 Release Criticality Taxonomy

REQ-RELCLASS-001: Every requirement, capability, module, test, and data entity MUST be assigned a per-release criticality value before it can block a release decision.

Allowed release criticality values:

```text
RELEASE_BLOCKER
REQUIRED_FOR_RELEASE
OPTIONAL_FOR_RELEASE
DEFERRED
RESEARCH_ONLY
```

REQ-RELCLASS-002: `RELEASE_BLOCKER` MUST be reserved for conditions that make the release unsafe, non-reproducible, non-auditable, or incapable of satisfying its declared release goal.

REQ-RELCLASS-003: `REQUIRED_FOR_RELEASE` MUST mean the item is needed for the declared release scope but can fail without blocking the entire program if it is explicitly removed from that release scope.

REQ-RELCLASS-004: `OPTIONAL_FOR_RELEASE` MUST mean the release may ship without the item and any disabled state is visible in `runtime_manifest`.

REQ-RELCLASS-005: `DEFERRED` MUST mean the item is intentionally postponed and MUST NOT be interpreted as missing work for the current release.

REQ-RELCLASS-006: `RESEARCH_ONLY` MUST mean the item may run only in Research Factory, Learning Lab, notebooks, or offline experiments and MUST NOT write execution-eligible runtime artifacts.

REQ-RELCLASS-007: Release 0 and Release 1A MUST NOT be blocked by FinBERT, LSTM, knowledge-graph models, graph neural networks, counterfactual portfolios, LLM explanations, options features, or SEC EDGAR fundamentals unless a governance-approved scope change explicitly promotes one of them.

REQ-RELCLASS-008: A release gate MUST distinguish `documentation_coverage`, `implementation_status`, `test_status`, and `release_criticality`; a well-described requirement is not equivalent to a working implementation.

### 2.1 Release 0: Truth Kernel

Goal: prove that data, labels, validation, replay, and baseline comparisons are not leaking or overfit.

REQ-REL0-001: Release 0 MUST include:

```text
PIT data
instrument master starter table
identifier history table
daily raw and adjusted OHLCV
static research universe
correct research labels for 5/8/14 sessions
purged walk-forward splitter
embargo
baseline forecast
transaction cost model
date-grouped ranking metrics
reproducible reports
experiment registry
golden dataset tests
research factory boundary
append-only decision ledger foundation
deterministic replay
```

REQ-REL0-002: Release 0 MUST NOT include broker execution.

REQ-REL0-003: Release 0 MAY exclude news, graph, LLMs, deep learning, SEC fundamentals, options, dynamic opportunity memory, paper trading, and counterfactual portfolios.

### 2.2 Release 1A: Decision Kernel

REQ-REL1A-001: Release 1A MUST include:

```text
historical dynamic universe
technical and market context features
multi-horizon forecasts
probability calibration
distributional forecast metadata
Alpha / Permission / Risk / Utility policy
NO_ACTION
canonical recommendation schema
portfolio state contract
portfolio-aware backtest
recommendation history
decision runtime boundary
basic evidence interface
risk sizing
basic decision dashboard
```

REQ-REL1A-002: Release 1A SHOULD prove value without news, graph, LLM, options, or advanced market-world modules.

### 2.3 Release 1B: Runtime Memory

REQ-REL1B-001: Release 1B SHOULD add:

```text
market state snapshot
standard evidence packet
opportunity object
capability health policy
dashboard memory views
```

### 2.4 Release 2A: Context Modules

REQ-REL2A-001: Release 2A SHOULD add only modules whose marginal value is measurable:

```text
PIT fundamentals
SEC EDGAR / XBRL support
earnings calendar
macro regime engine
news ingestion
source reliability
options snapshot features
drift monitoring
model registry governance reports
operational knowledge graph
```

### 2.5 Release 2B: Learning Factory

REQ-REL2B-001: Release 2B SHOULD add:

```text
counterfactual digital twin
policy challenger portfolios
human override analytics
value-of-information estimates
module marginal-value reports
decision error attribution
```

### 2.6 Release 3: Shadow and Paper Trading

REQ-REL3-001: Release 3 MUST include:

```text
shadow mode
paper broker integration
manual approval workflow
order state machine
idempotent order submission
broker reconciliation
execution simulator validation
slippage measurement
kill switch
incident runbook
append-only audit logs
execution digital twin validation
decision ledger replay verification
```

### 2.7 Release 4: Advanced Modeling and Limited Live Readiness

REQ-REL4-001: Release 4 MAY add:

```text
technical encoder
feature attention
temporal attention / TFT
graph model
event graph nodes
advanced uncertainty engine
portfolio optimizer
limited capital live trading with manual approval
adaptive expert weighting
advanced knowledge-graph models
deep ensembles
online learning candidates gated by counterfactual validation
```

REQ-REL4-002: Advanced models MUST NOT be promoted unless they beat approved baselines under the same universe, risk, cost, and execution rules.

REQ-REL4-003: Specification maximalism is a release blocker. A release MUST NOT require optional capabilities before the Decision Kernel has demonstrated value under the release gate for its phase.

---

## 3. Canonical Domain Model

### 3.1 Canonical Enums

REQ-DOM-001: The platform MUST use the following canonical status dimensions and MUST NOT create parallel enums for the same concept.

`market_stance`:

```text
STRONGLY_BULLISH
BULLISH
NEUTRAL
BEARISH
STRONGLY_BEARISH
```

`recommended_action`:

```text
OPEN_LONG
ADD_LONG
HOLD_LONG
REDUCE_LONG
CLOSE_LONG
NO_ACTION
```

`eligibility_state`:

```text
ACTIONABLE
CONDITIONAL
WATCHLIST
BLOCKED
NO_EDGE
PORTFOLIO_CONSTRAINED
DATA_UNAVAILABLE
```

`recommendation_status`:

```text
CREATED
VALID
APPROVAL_PENDING
APPROVED
REJECTED
EXECUTED
EXPIRED
SUPERSEDED
CANCELLED
```

`current_position_state`:

```text
NONE
LONG_PENDING_ENTRY
LONG_OPEN
LONG_PARTIALLY_FILLED
LONG_PENDING_EXIT
LONG_PARTIALLY_CLOSED
LONG_CLOSED
UNKNOWN_REQUIRES_RECONCILIATION
```

REQ-DOM-002: `EXPIRED` and `SUPERSEDED` MUST only appear under `recommendation_status`.

REQ-DOM-003: `NO_TRADE` MAY be a display label, but the canonical internal value MUST be:

```text
recommended_action = NO_ACTION
```

REQ-DOM-004: `UNKNOWN_REQUIRES_RECONCILIATION` MUST block new order submission for the instrument until broker, order, fill, and internal position ledger reconciliation completes.

### 3.2 Decision Cycle Contract

REQ-DOM-005: Every batch of same-day decisions MUST be attached to a `decision_cycle`.

Required `decision_cycle` fields:

```text
decision_cycle_id
trading_date
exchange_calendar_id
exchange_calendar_version
universe_id
portfolio_snapshot_id
eod_cutoff_at
preopen_cutoff_at
candidate_run_started_at
candidate_run_completed_at
candidate_run_status
revalidation_run_started_at
revalidation_run_completed_at
revalidation_run_status
execution_window_start
execution_window_end
data_snapshot_id
feature_snapshot_id
model_registry_snapshot_id
policy_bundle_id
runtime_manifest_id
code_commit_sha
environment_hash
random_seed
decision_budget_id
created_by
created_at
```

Allowed run statuses:

```text
NOT_STARTED
RUNNING
COMPLETED
COMPLETED_WITH_WARNINGS
FAILED
ABORTED
SUPERSEDED
```

REQ-DOM-006: All recommendations generated for one operational run MUST reference the same `decision_cycle_id`.

REQ-DOM-007: A `decision_cycle` MUST be immutable after completion except for appending status transition events.

### 3.3 Recommendation Versioning and Stage Lineage

REQ-DOM-008: The system MUST distinguish EOD candidates from pre-open validated and execution-ready recommendations.

Canonical recommendation stages:

```text
EOD_CANDIDATE
PREOPEN_VALIDATED
EXECUTION_READY
EXECUTION_BLOCKED
FILLED
MATURED
```

REQ-DOM-009: `recommendation_id` is the immutable record ID for exactly one recommendation record.

REQ-DOM-010: `recommendation_family_id` groups all stages and material versions of the same instrument opportunity.

REQ-DOM-011: `parent_recommendation_id` points to the immediate prior recommendation record when a new stage or version is created.

REQ-DOM-012: The canonical model MUST NOT use `candidate_recommendation_id` or `execution_recommendation_id` as bidirectional pointers. Stage lineage MUST be represented by `recommendation_family_id`, `parent_recommendation_id`, `recommendation_stage`, and append-only stage transition events.

REQ-DOM-013: A pre-open revalidation MAY change eligibility, action, position size, entry rule, blockers, or status.

REQ-DOM-014: If pre-open revalidation changes a material decision field, the system MUST create a new immutable recommendation record with a higher `recommendation_version`.

Material decision fields include:

```text
market_stance
recommended_action
eligibility_state
suggested_position_size_pct
entry_rule
entry_limit
provisional_or_final_stop
provisional_or_final_target
hard_blockers
portfolio_snapshot_id
data_snapshot_id
model_registry_snapshot_id
policy_bundle_id
```

### 3.4 Instrument Master

REQ-DOM-015: Ticker MUST NOT be treated as a stable key.

Required `instrument_master` fields:

```text
instrument_id
issuer_id
current_ticker
exchange
currency
share_class
cik
figi_optional
active_from
active_to
delisting_date
delisting_reason
successor_instrument_id
is_tradable
is_primary_listing
security_type
```

REQ-DOM-016: Identifier history MUST be stored separately:

```text
instrument_identifier_history:
  instrument_id
  identifier_type
  identifier_value
  valid_from
  valid_to
  source
```

Supported identifier types:

```text
ticker
exchange_symbol
vendor_symbol
broker_symbol
CIK
FIGI
CUSIP_if_licensed
ISIN_if_licensed
```

### 3.5 Universe Contract

REQ-DOM-017: Universe selection is itself point-in-time.

Required fields:

```text
universe_id
universe_name
instrument_id
member_from
member_to
universe_construction_rule
universe_decision_time
minimum_price
minimum_dollar_volume
minimum_listing_age
maximum_spread
included_security_types
excluded_security_types
source
source_version
```

REQ-DOM-018: Universe filters MUST use only data known at `universe_decision_time`.

REQ-DOM-019: Release 1+ production universes SHOULD default to common stocks only unless explicitly approved.

Security type handling MUST be explicit for:

```text
common_stock
ADR
ETF
REIT
preferred_share
SPAC
closed_end_fund
OTC_security
unit
warrant
```

### 3.6 Portfolio State Contract

REQ-DOM-020: Every decision run MUST receive a portfolio snapshot.

Required fields:

```text
portfolio_snapshot_id
portfolio_id
as_of_timestamp
portfolio_value
cash_available
buying_power
gross_exposure
net_exposure
long_exposure
sector_exposures
industry_exposures
factor_exposures
market_beta
volatility_target
current_drawdown
daily_loss
weekly_loss
open_risk
unrealized_pnl
realized_pnl
open_positions
open_orders
correlation_clusters
remaining_risk_budget
```

### 3.7 Market World Model Contract

REQ-DOM-021: The system MUST maintain a shared `market_state_snapshot` for each decision cycle instead of letting each module independently define market regime, volatility, liquidity, risk-on/risk-off, or cross-asset stress.

Required `market_state_snapshot` fields:

```text
market_state_snapshot_id
decision_cycle_id
as_of_timestamp
broad_market_regime
trend_strength
breadth_state
volatility_regime
dispersion_state
liquidity_regime
correlation_state
rates_regime
rates_pressure
credit_regime
credit_stress
sector_rotation_state
cross_asset_stress
event_calendar_risk
event_density
regime_confidence
regime_transition_probability
source_feature_snapshot_id
market_state_model_version
```

REQ-DOM-022: Market state MUST be represented as a vector of interpretable dimensions, not only as categorical labels such as `BULL`, `BEAR`, or `SIDEWAYS`.

REQ-DOM-023: Expert modules, decision policy, risk policy, and portfolio construction MUST reference the same `market_state_snapshot_id` for a decision cycle unless an approved exception is recorded.

REQ-DOM-024: `market_state_snapshot` MUST NOT be treated as one unquestionable truth. It MUST contain one or more `market_state_hypotheses`.

Required `market_state_hypothesis` fields:

```text
state_hypothesis_id
market_state_snapshot_id
state_label
state_probability
supporting_evidence
contradicting_evidence
transition_probability
historical_analogs
created_as_of
```

REQ-DOM-025: Decision policy SHOULD evaluate utility under multiple plausible world-state hypotheses.

Required hypothesis-aware decision fields:

```text
utility_by_state_hypothesis
worst_plausible_state_utility
state_weighted_expected_utility
state_sensitivity_reason
```

### 3.8 Opportunity Memory Contract

REQ-DOM-026: The system MUST model an `opportunity` as a long-lived thesis that may generate multiple daily recommendation snapshots.

Required `opportunity` fields:

```text
opportunity_id
instrument_id
opportunity_type
thesis
catalyst
expected_path
expected_duration_sessions
invalidation_conditions
first_detected_at
last_confirmed_at
strength_history
evidence_history
contradictory_evidence
opportunity_status
opportunity_model_version
supporting_evidence_score
contradictory_evidence_score
new_information_ratio
thesis_age_sessions
thesis_decay
price_realization_ratio
invalidation_distance
adversarial_review_status
```

Allowed initial `opportunity_type` values:

```text
POST_EARNINGS_DRIFT
SECTOR_RELATIVE_BREAKOUT
VOLATILITY_COMPRESSION
FUNDAMENTAL_REACCELERATION
EVENT_REVERSAL
LIQUIDITY_DISLOCATION
MARKET_PULLBACK_CONTINUATION
```

Allowed `opportunity_status` values:

```text
ACTIVE
STRENGTHENING
DECAYING
MOSTLY_PRICED_IN
UNDER_ADVERSARIAL_REVIEW
INVALIDATED
ARCHIVED
```

REQ-DOM-027: A recommendation MUST declare whether it represents a new opportunity, continuation, strengthening, weakening, invalidation, or duplicate confirmation of an existing opportunity.

REQ-DOM-028: Opportunity memory MUST support explanations about whether the thesis is strengthening, decaying, already priced in, contradicted by new evidence, or approaching invalidation.

REQ-DOM-029: Opportunity memory MUST include adversarial thesis review to prevent confirmation bias.

Required adversarial review questions:

```text
Why is this thesis wrong?
What evidence would invalidate it?
Has the market already priced it in?
Are new recommendations based on new evidence or repeated evidence?
```

### 3.9 Evidence Packet Contract

REQ-DOM-030: Expert modules MUST emit standardized `evidence_packet` records rather than only opaque scalar scores.

Required `evidence_packet` fields:

```text
evidence_id
recommendation_id
opportunity_id
expert_module
claim
direction
expected_effect
relevant_horizon_sessions
strength
confidence
freshness
independence_group
root_cause_id
derived_from_evidence_ids
dependency_strength
information_novelty
independent_information_gain
source_quality
historical_calibration
conditions_where_valid
conditions_where_invalid
supporting_records
contradicts_evidence_ids
market_state_snapshot_id
```

Initial expert modules:

```text
Technical Expert
Market Structure Expert
Sector Expert
Fundamental Expert
Event Expert
News Expert
Options Expert
Liquidity Expert
Execution Expert
```

REQ-DOM-031: The decision engine MUST evaluate evidence independence, horizon alignment, regime validity, duplicate source amplification, and contradictory evidence before aggregating evidence into utility or permission.

REQ-DOM-032: Evidence independence MUST be modeled as an `evidence_dependency_graph`, not only a binary `independence_group`.

Required evidence dependency graph fields:

```text
evidence_dependency_graph_id
recommendation_id
root_event_ids
evidence_node_ids
dependency_edges
root_cause_id
dependency_strength
information_novelty
independent_information_gain
```

REQ-DOM-033: Multiple evidence packets derived from one root event MUST NOT be counted as independent confirmations unless their independent information gain is positive under the evidence policy.

### 3.10 Operational Knowledge Graph Contract

REQ-DOM-034: The graph layer MUST first serve operational knowledge functions before being treated as an advanced GNN model input.

Minimum graph node types:

```text
Company
Instrument
Sector
Industry
ETF
Index
Executive
Supplier
Customer
Competitor
Product
Commodity
Country
News Event
Filing
Earnings Event
Source
```

Minimum graph edge types:

```text
SUPPLIES
CUSTOMER_OF
COMPETES_WITH
MEMBER_OF
EXPOSED_TO
MENTIONED_IN
CONFIRMED_BY
COPIED_FROM
CORRELATED_WITH
OWNED_BY
```

REQ-DOM-035: The knowledge graph SHOULD support entity resolution, news propagation, exposure mapping, deduplication, portfolio concentration analysis, and source lineage before any GNN promotion is considered.

REQ-DOM-036: The platform MUST separate structural knowledge graph edges from temporal market graph edges.

Structural graph edges are relatively stable:

```text
SUPPLIES
COMPETES_WITH
CUSTOMER_OF
MEMBER_OF
```

Temporal graph edges are time-varying:

```text
CORRELATED_WITH
LEADS
LAGS
CO_MOVES_WITH
CAPITAL_ROTATES_TO
NEWS_PROPAGATES_TO
```

Required temporal edge fields:

```text
valid_from
valid_to
computed_as_of
confidence
lookback
regime
```

---

## 4. Canonical Recommendation Aggregate and Data Model

REQ-SCH-001: The canonical recommendation model MUST be an aggregate composed of smaller entities, not one wide table or object containing all forecast, decision, portfolio, execution, outcome, and audit fields.

REQ-SCH-002: The aggregate MUST be implemented once and reused by API, UI, storage, backtest, paper trading, execution, outcome tracking, and audit systems.

Canonical aggregate entities:

```text
decision_cycle
decision_budget
runtime_manifest
market_state_snapshot
market_state_hypothesis
opportunity
recommendation
evidence_packet
evidence_dependency_graph
content_item
content_enrichment
content_market_link
source_profile
feature_snapshot
model_training_artifact
forecast_snapshot
forecast_distribution
joint_horizon_distribution
decision_assessment
risk_assessment
execution_plan
approval_record
execution_record
order_record
fill_record
outcome_record
explanation_package
counterfactual_run
counterfactual_portfolio
decision_error_attribution
module_value_profile
decision_ledger_event
audit_event
```

REQ-SCH-003: A denormalized recommendation view MAY exist for UI, reporting, or export, but it MUST be derived from the canonical entities and MUST NOT become the source of truth.

REQ-SCH-004: Every canonical entity MUST define:

```text
primary_key
foreign_keys
schema_version
created_at
created_by
source_of_truth
allowed_writers
immutability_rule
stage_requiredness_rule
audit_event_type_for_changes
```

### 4.0 Decision Budget

REQ-SCH-005: Every decision cycle SHOULD have a `decision_budget` controlling latency, cost, external dependencies, and human attention.

Required `decision_budget` fields:

```text
decision_budget_id
decision_cycle_id
maximum_latency
maximum_data_cost
maximum_compute_cost
maximum_human_review_capacity
maximum_external_dependencies
maximum_llm_tokens
minimum_required_confidence_gain
budget_policy_version
```

REQ-SCH-006: Expensive enrichment SHOULD be staged:

```text
Stage 1: cheap broad scan
Stage 2: medium-cost enrichment
Stage 3: expensive deep analysis only for finalists
```

Recommended funnel:

```text
Universe
  -> cheap eligibility screen
Top 300
  -> technical + market forecast
Top 50
  -> fundamentals / events / news
Top 10
  -> deep evidence / graph / execution analysis
Top actionable set
```

### 4.1 Recommendation Core

REQ-SCH-007: `recommendation` MUST contain only stable identity, lifecycle, status, and high-level decision fields.

Required `recommendation` fields:

```text
recommendation_id
recommendation_family_id
parent_recommendation_id
recommendation_version
decision_cycle_id
opportunity_id
universe_id
instrument_id
ticker_display
exchange
currency
market_timezone
market_state_snapshot_id

recommendation_stage
market_stance
recommended_action
eligibility_state
recommendation_status
current_position_state

candidate_generated_at
preopen_revalidation_at
valid_from
valid_until
status_reason_code

data_snapshot_id
feature_snapshot_id
portfolio_snapshot_id
model_registry_snapshot_id
policy_bundle_id
code_commit_sha
environment_hash
random_seed
```

REQ-SCH-008: Recommendation records MUST be immutable after creation.

REQ-SCH-009: Any material decision change MUST create a new `recommendation` record with a new `recommendation_id`, the same `recommendation_family_id`, a higher `recommendation_version`, and `parent_recommendation_id` set to the previous material record.

REQ-SCH-010: Non-material workflow changes, such as adding an operator note or recording a read receipt, MUST be stored as `audit_event` records and MUST NOT mutate the recommendation record.

### 4.2 Forecast Snapshot and Horizon Distributions

REQ-SCH-011: Forecasts MUST be stored by horizon in child records to avoid duplicated 5D, 8D, and 14D fields.

Required `forecast_snapshot` fields:

```text
forecast_snapshot_id
recommendation_id
generated_at
model_registry_snapshot_id
feature_snapshot_id
target_policy_version
probability_calibration_version
prediction_interval_method
primary_ranking_target
primary_portfolio_return_target
```

Required `forecast_distribution` fields:

```text
forecast_distribution_id
forecast_snapshot_id
horizon_sessions
target_basis
research_target_log_return_h
expected_return_bps
conditional_expected_return_if_filled_bps
prediction_interval_coverage
prediction_interval_low_bps
prediction_interval_high_bps
downside_quantile_level
downside_quantile_bps
upside_quantile_level
upside_quantile_bps
probability_positive_return_h
probability_covering_cost_h
probability_exceeding_hurdle_h
probability_positive_if_filled_h
probability_covering_cost_if_filled_h
probability_exceeding_hurdle_if_filled_h
empirical_coverage
coverage_error
calibration_quality_score
```

REQ-SCH-012: `forecast_distribution` MUST have a uniqueness constraint over:

```text
forecast_snapshot_id
horizon_sessions
target_basis
```

REQ-SCH-013: Allowed `target_basis` values are:

```text
ABSOLUTE_RETURN
MARKET_EXCESS_RETURN
SECTOR_EXCESS_RETURN
POLICY_RETURN_IF_FILLED
REALIZED_TRADE_RETURN
```

REQ-SCH-014: `joint_horizon_distribution` MUST store covariance as a matrix, not as a scalar.

Required `joint_horizon_distribution` fields:

```text
joint_horizon_distribution_id
forecast_snapshot_id
horizons_sessions
covariance_basis
covariance_matrix
matrix_units
estimation_window
estimation_method
probability_all_horizons_positive
probability_short_horizon_positive_long_horizon_negative
probability_initial_drawdown_then_recovery
```

Allowed `covariance_basis` values:

```text
FORECAST_VALUES
FORECAST_ERRORS
FUTURE_RETURNS
POSTERIOR_PREDICTIVE_DISTRIBUTION
```

### 4.3 Decision, Risk, Cost, and Explanation Entities

REQ-SCH-015: `decision_assessment` MUST own ranking, utility, permission, confidence, uncertainty, divergence, and blocker outputs.

Required `decision_assessment` fields:

```text
decision_assessment_id
recommendation_id
selected_horizon_sessions
selected_horizon_score
selected_horizon_reason
rank_score
alpha_score
risk_adjusted_utility_bps
permission_score_before_blockers
permission_score_after_soft_penalties
permission_score
decision_confidence
model_confidence
data_confidence
explanation_confidence
calibration_confidence
aleatoric_uncertainty
epistemic_uncertainty
model_disagreement_uncertainty
data_quality_uncertainty
regime_uncertainty
execution_uncertainty
combined_uncertainty_score
temporal_divergence_score
market_divergence_score
module_disagreement_score
portfolio_conflict_score
combined_divergence_score
hard_blockers
soft_penalties
invalidating_conditions
decision_policy_version
```

REQ-SCH-016: `risk_assessment` MUST own portfolio-aware risk, sizing, and exposure outputs.

Required `risk_assessment` fields:

```text
risk_assessment_id
recommendation_id
portfolio_snapshot_id
risk_model_version
risk_score
risk_score_components
risk_budget_used_pct
suggested_position_size_pct
planned_stop_distance_pct
expected_loss_if_stop_triggered_pct
stress_loss_if_gap_through_stop_pct
concentration_cost_bps
liquidity_cost_bps
event_risk_cost_bps
expected_shortfall_bps
```

REQ-SCH-017: Cost components MUST be stored in the assessment layer and joined to execution records for realized comparison.

Required cost fields:

```text
commission_bps
spread_cost_bps
market_impact_bps
open_auction_cost_bps
expected_slippage_bps
regulatory_fee_bps
borrow_cost_bps
pretrade_expected_cost_bps
simulated_cost_bps
actual_realized_cost_bps
cost_model_version
```

REQ-SCH-018: `explanation_package` MUST contain only explanation artifacts and their lineage.

Required `explanation_package` fields:

```text
explanation_package_id
recommendation_id
reason_summary
driver_objects
decision_sensitivity
feature_lineage_refs
source_record_refs
explanation_model_version
llm_provider
llm_model_version
prompt_hash
sampling_parameters
structured_schema_version
fallback_model
fallback_behavior
created_at
```

### 4.4 Execution, Approval, and Outcome Entities

REQ-SCH-019: `execution_plan` MUST own intended execution behavior before an order is submitted.

Required `execution_plan` fields:

```text
execution_plan_id
recommendation_id
entry_session_id
entry_style
reference_price
reference_price_type
estimated_entry_price
entry_rule
entry_limit
maximum_acceptable_gap_pct
open_execution_quality
provisional_stop_loss
provisional_take_profit_1
provisional_take_profit_2
final_stop_loss
final_take_profit_1
final_take_profit_2
time_stop_sessions
preopen_revalidation_deadline
approval_deadline
order_submission_earliest
order_submission_latest
market_open_buffer
late_approval_policy
execution_policy_version
stop_policy_version
target_policy_version
```

REQ-SCH-020: `approval_record` MUST own human or policy approval state.

Required `approval_record` fields:

```text
approval_id
recommendation_id
approved_recommendation_version
approved_at
approval_valid_until
approved_by
approved_max_notional
approved_entry_limit
approved_policy_bundle_id
approval_conditions
approval_status
```

REQ-SCH-021: `execution_record`, `order_record`, and `fill_record` MUST separate system intent, broker order lifecycle, and actual fills.

Required `execution_record` fields:

```text
execution_record_id
recommendation_id
execution_plan_id
approval_id
execution_preflight_check_id
submitted_at
broker_account_id
execution_status
```

Required `order_record` fields:

```text
order_id
execution_record_id
broker_order_id
idempotency_key
order_action
order_type
limit_price
quantity
time_in_force
order_state
replace_parent_order_id
created_at
last_broker_reconciled_at
```

Required `fill_record` fields:

```text
fill_id
order_id
broker_fill_id
filled_quantity
fill_price
fill_timestamp
fees
actual_realized_cost_bps
```

REQ-SCH-022: `outcome_record` MUST be created only after the relevant horizon or terminal event has matured.

Required `outcome_record` fields:

```text
outcome_record_id
recommendation_id
position_lot_id
horizon_sessions
outcome_matured_at
policy_return_h_if_filled
realized_trade_return
absolute_return_h
market_excess_return_h
sector_excess_return_h
terminal_event
exit_reason
outcome_data_snapshot_id
```

### 4.5 Stage Requiredness, Nullability, and Immutability

REQ-SCH-023: A companion matrix MUST define each field or field group as one of:

```text
required
nullable
conditionally_required
derived
immutable_after_stage
source_of_truth
```

Initial stage matrix:

| Entity / field group | EOD_CANDIDATE | PREOPEN_VALIDATED | EXECUTION_READY | FILLED | MATURED | Immutability / source of truth |
| --- | --- | --- | --- | --- | --- | --- |
| `decision_cycle` | Required | Required | Required | Immutable | Immutable | Operations scheduler |
| `recommendation` identity | Required | Required | Required | Immutable | Immutable | Recommendation service |
| `recommendation_stage` | Required | Required | Required | Derived | Derived | Stage transition event |
| `forecast_snapshot` | Required | Required or inherited | Required or inherited | Immutable | Immutable | Forecast service |
| `forecast_distribution.expected_return_bps` | Required | Required | Required | Immutable | Immutable | Forecast service |
| `forecast_distribution.*_if_filled_h` | Conditional | Conditional | Required if fill model enabled | Immutable | Immutable | Forecast/fill services |
| `decision_assessment` | Required | Required | Required | Immutable | Immutable | Decision policy service |
| `risk_assessment` | Required | Required | Required | Immutable | Immutable | Risk service |
| `execution_plan.provisional_stop_loss` | Required | Optional | Superseded by final stop | Immutable | Immutable | Execution policy |
| `execution_plan.final_stop_loss` | Null | Optional | Required | Required | Required | Execution policy |
| `approval_record` | Null | Conditional | Required before submission | Required if submitted | Required if submitted | Approval service |
| `execution_record` | Null | Null | Conditional | Required if submitted | Required if submitted | Execution service |
| `order_record` | Null | Null | Conditional | Required if order sent | Required if order sent | Broker adapter plus reconciliation |
| `fill_record.actual_realized_cost_bps` | Null | Null | Null | Required if filled | Required if filled | Broker fills plus cost reconciler |
| `outcome_record.realized_trade_return` | Null | Null | Null | Null | Required | Outcome service |
| `explanation_package` | Required | Required or inherited | Required | Immutable | Immutable | Explanation service |

REQ-SCH-024: Nullable fields MUST be nullable because the lifecycle stage does not yet know the value, not because producers are allowed to skip required work.

REQ-SCH-025: Conditionally required fields MUST name the condition in the schema registry, for example `required_when = fill_model_enabled`.

REQ-SCH-026: Each API response MUST expose stage-aware field semantics or use per-entity schemas so clients do not infer incorrect missingness from `null`.

### 4.6 Source of Truth and Ownership

REQ-SCH-027: The following ownership matrix is normative:

| Concept | Source of truth | Allowed writer |
| --- | --- | --- |
| Decision budget | `decision_budget` | Decision scheduler / Control Plane |
| Runtime manifest | `runtime_manifest` | Control Plane |
| Market world state | `market_state_snapshot` | World-state service |
| Market state hypotheses | `market_state_hypothesis` | World-state service |
| Opportunity memory | `opportunity` | Opportunity service |
| Evidence claims | `evidence_packet` | Expert modules through evidence service |
| Evidence dependencies | `evidence_dependency_graph` | Evidence service / graph service |
| Content identity and metadata | `content_item` | Content ingestion service |
| Content enrichment outputs | `content_enrichment` | Content enrichment service |
| Content-to-market linkage | `content_market_link` | Content linkage service / Learning lab |
| Source reliability profile | `source_profile` | Source reliability service |
| Feature snapshots | `feature_snapshot` | Feature store service |
| Model training artifacts | `model_training_artifact` | Research Factory / model registry |
| Forecast distributions | `forecast_snapshot` / `forecast_distribution` | Forecast service |
| Ranking and utility | `decision_assessment` | Decision policy service |
| Portfolio risk and sizing | `risk_assessment` | Risk service |
| Execution intent | `execution_plan` | Execution policy service |
| Approval | `approval_record` | Approval service |
| Broker order state | `order_record` plus broker reconciliation | Broker adapter |
| Fills and realized costs | `fill_record` | Broker adapter plus cost reconciler |
| Trade outcomes | `outcome_record` | Outcome service |
| Counterfactual outcomes | `counterfactual_run` / `counterfactual_portfolio` | Learning lab |
| Decision error attribution | `decision_error_attribution` | Learning lab / reviewer |
| Module marginal value | `module_value_profile` | Learning lab |
| Human notes and workflow events | `audit_event` | Audit service |

### 4.7 Canonical Field Type System and Relationships

REQ-SCH-028: The implementation MUST use the following canonical field type system unless a field-specific schema explicitly overrides it.

| Field pattern | Canonical type | Notes |
| --- | --- | --- |
| `*_id` | UUID or ULID string | Stable opaque identifier, never derived from ticker |
| `*_version` | immutable string | SemVer, hash, or registry version |
| `*_at` | `TIMESTAMPTZ` UTC | Store timezone metadata separately when needed |
| `*_date` | exchange-local date | Calendar ID required for trading dates |
| `*_sessions` | integer | Exchange trading sessions, not calendar days |
| `*_bps` | decimal numeric | Basis points, signed unless explicitly non-negative |
| `*_pct` | decimal numeric | Fractional percent representation must be documented |
| `*_price` | decimal numeric | Raw or adjusted basis must be explicit |
| `quantity` / `*_quantity` | decimal numeric | Fractional support governed by portfolio policy |
| `*_score` | decimal numeric | Range and direction must be defined by score version |
| `*_confidence` | decimal in `[0, 1]` | Higher means more reliable |
| `*_uncertainty` | decimal numeric | Scale defined by uncertainty score version |
| enum fields | string enum | Values only from this document or schema registry |
| arrays | typed array | Empty array differs from null |
| object fields | JSON object with schema version | Used only for structured extensibility |
| `covariance_matrix` | square numeric matrix | Shape must match `horizons_sessions` |

REQ-SCH-029: Minimum primary and foreign key constraints:

| Entity | Primary key | Required foreign keys |
| --- | --- | --- |
| `decision_cycle` | `decision_cycle_id` | `universe_id`, `portfolio_snapshot_id`, `policy_bundle_id` |
| `decision_budget` | `decision_budget_id` | `decision_cycle_id` |
| `runtime_manifest` | `runtime_manifest_id` | `decision_cycle_id`, `policy_bundle_id` |
| `market_state_snapshot` | `market_state_snapshot_id` | `decision_cycle_id` |
| `market_state_hypothesis` | `state_hypothesis_id` | `market_state_snapshot_id` |
| `opportunity` | `opportunity_id` | `instrument_id` |
| `recommendation` | `recommendation_id` | `decision_cycle_id`, `opportunity_id`, `instrument_id`, `universe_id`, `policy_bundle_id`, `market_state_snapshot_id` |
| `evidence_packet` | `evidence_id` | `recommendation_id`, `opportunity_id`, `market_state_snapshot_id` |
| `evidence_dependency_graph` | `evidence_dependency_graph_id` | `recommendation_id` |
| `content_item` | `content_id` | `source_profile_id`, `source_record_id` |
| `content_enrichment` | `content_enrichment_id` | `content_id`, `model_registry_snapshot_id` |
| `content_market_link` | `content_market_link_id` | `content_id`, `instrument_id` |
| `source_profile` | `source_profile_id` | `source_id` |
| `feature_snapshot` | `feature_snapshot_id` | `decision_cycle_id`, `data_snapshot_id`, `feature_set_id` |
| `model_training_artifact` | `model_training_artifact_id` | `feature_snapshot_id`, `model_registry_snapshot_id`, `policy_bundle_id` |
| `forecast_snapshot` | `forecast_snapshot_id` | `recommendation_id`, `model_registry_snapshot_id`, `feature_snapshot_id` |
| `forecast_distribution` | `forecast_distribution_id` | `forecast_snapshot_id` |
| `joint_horizon_distribution` | `joint_horizon_distribution_id` | `forecast_snapshot_id` |
| `decision_assessment` | `decision_assessment_id` | `recommendation_id` |
| `risk_assessment` | `risk_assessment_id` | `recommendation_id`, `portfolio_snapshot_id` |
| `execution_plan` | `execution_plan_id` | `recommendation_id` |
| `approval_record` | `approval_id` | `recommendation_id` |
| `execution_record` | `execution_record_id` | `recommendation_id`, `execution_plan_id`, `approval_id` |
| `order_record` | `order_id` | `execution_record_id` |
| `fill_record` | `fill_id` | `order_id` |
| `position_lot` | `position_lot_id` | `portfolio_id`, `instrument_id`, `opening_fill_id` |
| `outcome_record` | `outcome_record_id` | `recommendation_id`, `position_lot_id` |
| `explanation_package` | `explanation_package_id` | `recommendation_id` |
| `counterfactual_run` | `counterfactual_run_id` | `decision_cycle_id`, `policy_bundle_id` |
| `counterfactual_portfolio` | `counterfactual_portfolio_id` | `counterfactual_run_id` |
| `decision_error_attribution` | `decision_error_attribution_id` | `recommendation_id`, `outcome_record_id` |
| `module_value_profile` | `module_value_profile_id` | `module_id`, `module_version` |
| `decision_ledger_event` | `ledger_event_id` | `decision_cycle_id` |
| `audit_event` | `event_id` | `entity_type`, `entity_id` |

REQ-SCH-030: Unique constraints MUST include:

```text
recommendation(recommendation_family_id, recommendation_version)
opportunity(instrument_id, opportunity_type, first_detected_at)
evidence_packet(recommendation_id, expert_module, claim, independence_group)
forecast_distribution(forecast_snapshot_id, horizon_sessions, target_basis)
approval_record(recommendation_id, approved_recommendation_version, approval_status)
order_record(idempotency_key)
fill_record(broker_fill_id)
decision_ledger_event(decision_cycle_id, sequence_number)
content_item(source_id, canonical_url_hash, published_at, content_hash)
content_enrichment(content_id, enrichment_type, model_version, feature_available_at)
content_market_link(content_id, instrument_id, link_method, event_time)
source_profile(source_id, profile_as_of_at, profile_version)
feature_snapshot(entity_scope, entity_id, feature_set_id, feature_as_of_at, feature_schema_hash)
model_training_artifact(model_family, model_version, training_cutoff_at, training_data_hash)
```

REQ-SCH-031: Deprecated fields MUST NOT be introduced in new canonical entities, APIs, UI contracts, tests, or fixtures:

```text
decision_state
candidate_recommendation_id
execution_recommendation_id
probability_up_5d
probability_up_8d
probability_up_14d
confidence_score
divergence_score
entry_price
joint_horizon_covariance_scalar
```

### 4.8 Content, Feature, and Training Artifact Entities

REQ-SCH-032: The canonical data model MUST define the conversation-derived content, feature, and training entities with primary keys, foreign keys, source of truth, allowed writer, immutability, unique constraints, and retention policy before those entities are used by production code.

Canonical governance contract:

| Entity | Primary key | Required foreign keys | Source of truth | Allowed writer | Immutability | Unique constraints | Retention policy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `content_item` | `content_id` | `source_profile_id`, `source_record_id` | Content ingestion service | Content ingestion service only | Immutable after canonicalization except append-only correction events | `source_id`, `canonical_url_hash`, `published_at`, `content_hash` | Retain decision-used metadata, hashes, timestamps, and lineage for at least 7 years; raw text retention MUST follow license and privacy policy |
| `content_enrichment` | `content_enrichment_id` | `content_id`, `model_registry_snapshot_id` | Content enrichment service | Content enrichment service only | Immutable after creation; new model versions create new rows | `content_id`, `enrichment_type`, `model_version`, `feature_available_at` | Retain decision-used enrichments for at least 7 years; research-only enrichments MAY expire after approved research retention |
| `content_market_link` | `content_market_link_id` | `content_id`, `instrument_id` | Content linkage service / Learning Lab | Linkage service; outcome service may append matured outcome reference | Immutable after link computation except matured outcome reference | `content_id`, `instrument_id`, `link_method`, `event_time` | Retain links used in features, labels, or source reliability for at least 7 years |
| `source_profile` | `source_profile_id` | `source_id` | Source reliability service | Source reliability service only | Point-in-time snapshots are append-only | `source_id`, `profile_as_of_at`, `profile_version` | Retain PIT profile history for at least 7 years when used in decisions or training |
| `feature_snapshot` | `feature_snapshot_id` | `decision_cycle_id`, `data_snapshot_id`, `feature_set_id` | Feature store service | Feature store service only | Immutable after feature cutoff and schema hash are sealed | `entity_scope`, `entity_id`, `feature_set_id`, `feature_as_of_at`, `feature_schema_hash` | Retain decision-used feature snapshots for at least 7 years; raw licensed data pointers obey provider policy |
| `model_training_artifact` | `model_training_artifact_id` | `feature_snapshot_id`, `model_registry_snapshot_id`, `policy_bundle_id` | Research Factory / model registry | Research Factory and model registry only | Immutable after registration; replacement requires a new artifact ID | `model_family`, `model_version`, `training_cutoff_at`, `training_data_hash` | Retain promoted artifacts for at least 7 years after model retirement; research-only artifacts follow experiment retention |

REQ-SCH-033: `content_item` MUST store normalized content identity and metadata.

Required `content_item` fields:

```text
content_id
source_profile_id
source_id
source_record_id
publisher_name
platform
author_id_if_applicable
canonical_url
canonical_url_hash
title_or_headline
raw_text_pointer
content_hash
language
mentioned_instrument_ids
published_at
publicly_available_at
provider_ingested_at
system_available_at
licensing_status
ingestion_run_id
created_at
```

REQ-SCH-034: `content_enrichment` MUST store model-derived outputs separately from content identity.

Required `content_enrichment` fields:

```text
content_enrichment_id
content_id
enrichment_type
model_registry_snapshot_id
model_family
model_version
sentiment_label_if_applicable
sentiment_score_if_applicable
positive_probability_if_applicable
neutral_probability_if_applicable
negative_probability_if_applicable
relevance_score
novelty_score
urgency_score
event_type
instrument_relevance
summary_pointer_if_enabled
feature_available_at
processed_at
input_text_hash
output_schema_version
```

REQ-SCH-035: `content_market_link` MUST store the point-in-time link between content and market observations without implying causal validity.

Required `content_market_link` fields:

```text
content_market_link_id
content_id
instrument_id
event_time
market_observation_start_at
market_observation_end_at
bar_interval
link_method
link_confidence
return_before_event_bps
return_after_event_bps
volume_change_after_event
volatility_change_after_event
label_maturity_status
outcome_record_id_if_matured
created_at
```

REQ-SCH-036: `source_profile` MUST be a point-in-time reliability snapshot, not a mutable current-score table.

Required `source_profile` fields:

```text
source_profile_id
source_id
source_family
publisher_name
platform
author_id_if_applicable
profile_as_of_at
profile_version
content_count_as_of
original_content_rate
copy_rate
independent_confirmation_rate
historical_reliability
reliability_confidence_interval
average_relevance
average_novelty
average_latency
cold_start_status
last_updated_at
```

REQ-SCH-037: `feature_snapshot` MUST be the canonical bridge between data, features, research datasets, runtime forecasts, and replay.

Required `feature_snapshot` fields:

```text
feature_snapshot_id
decision_cycle_id
data_snapshot_id
feature_set_id
entity_scope
entity_id
instrument_id_if_applicable
trading_date
feature_as_of_at
feature_cutoff_at
feature_available_at
feature_schema_hash
feature_values_pointer
row_count
column_count
missingness_summary
lineage_refs
created_at
```

REQ-SCH-038: `model_training_artifact` MUST record the exact dataset, feature schema, target schema, validation protocol, calibration method, and artifact hashes used to produce a candidate or promoted model.

Required `model_training_artifact` fields:

```text
model_training_artifact_id
model_registry_snapshot_id
model_family
model_version
training_run_id
training_cutoff_at
feature_snapshot_id
training_data_hash
target_schema_version
feature_schema_hash
walk_forward_protocol_id
calibration_method
baseline_comparison_ids
artifact_uri
artifact_checksum
promotion_environment
created_at
```

REQ-SCH-039: `operator_tool_audit_event` MUST NOT be introduced as a separate canonical entity. Operator tool usage MUST be represented by `audit_event` with `event_type = OPERATOR_TOOL_USED`, the target entity in `entity_type` and `entity_id`, redacted parameters, actor identity, timestamp, and read/write intent.

---

## 5. Operating Timeline and Data Availability

REQ-TIME-001: Production decisioning MUST use the two-stage flow:

```text
Market close t
  -> EOD data finalization
  -> EOD candidate generation
  -> overnight / pre-market refresh
  -> revalidation
  -> final execution permission
  -> order submission
```

REQ-TIME-002: Any pre-market data used in revalidation MUST be modeled in historical replay, or the recommendation must be marked research-only.

REQ-TIME-003: The system MUST distinguish time fields:

```text
event_time
provider_published_at
publicly_available_at
system_available_at
feature_available_at
decision_cutoff_at
```

REQ-TIME-004: All timestamps MUST include:

```text
UTC timestamp
source timezone
timestamp precision
is_estimated_timestamp
DST policy
```

REQ-TIME-005: `availability_time` is deprecated unless qualified.

### 5.1 Information-Theoretic vs System-Realistic Replay

REQ-TIME-006: Backtests MUST explicitly choose replay mode:

```text
INFORMATION_THEORETIC_REPLAY:
  uses data publicly available by decision_cutoff_at

SYSTEM_REALISTIC_REPLAY:
  uses only data actually ingested and feature-ready by system_available_at / feature_available_at
```

REQ-TIME-007: Shadow and production reports MUST store both public availability and system availability when available.

### 5.2 Correction Replay

REQ-TIME-008: The system MUST support two replay modes for corrected provider data:

```text
research_latest_truth_replay
historical_system_state_replay
```

REQ-TIME-009: Reports MUST NOT mix these results without labeling.

### 5.3 Clock Synchronization

REQ-TIME-010: Time-sensitive systems MUST define:

```text
clock_source
NTP_sync_required
maximum_clock_drift
timestamp_ingestion_location
clock_drift_alert
```

Clock drift beyond policy threshold is a PIT safety incident.

---

## 6. Bitemporal Data and Lineage

REQ-DATA-001: Every source record used in production MUST support:

```text
event_time
provider_published_at
publicly_available_at
system_available_at
valid_from
valid_to
system_from
system_to
revision_number
supersedes_record_id
is_latest_revision
source
provider
schema_version
```

REQ-DATA-002: Every feature used in a recommendation MUST be traceable:

```text
recommendation
  -> feature value
  -> feature computation version
  -> input records
  -> provider records
```

REQ-DATA-003: Key explanation drivers MUST include lineage sufficient for audit.

### 6.1 Data Licensing

REQ-DATA-004: Data licensing review is P0/P1, not only pre-live.

Review is required before:

```text
storing article bodies
storing social posts
using options data
training models on vendor data
redistributing dashboards
showing data to another user
persisting provider-derived features
```

### 6.2 Fundamentals PIT and Restatements

REQ-DATA-005: Fundamental facts used in Release 2+ MUST preserve the filing state known at the decision time and the latest corrected state separately.

Required fields:

```text
filing_accession_number
filing_accepted_at
filing_type
amendment_flag
restatement_flag
taxonomy_version
fact_name
fact_period_start
fact_period_end
fact_value
fact_unit
fact_filed_at
fact_valid_from
fact_superseded_at
source_record_id
```

REQ-DATA-006: PIT replay MUST distinguish original 10-K/10-Q facts from amended 10-K/A or 10-Q/A facts.

REQ-DATA-007: Taxonomy remapping MUST create a new versioned fact mapping record and MUST NOT silently overwrite historical feature inputs.

---

## 7. Price Basis and Open Execution

REQ-PRICE-001: The platform MUST distinguish:

```text
raw_tradable_price
split_adjusted_price
total_return_adjusted_price
```

REQ-PRICE-002: Orders, stops, limits, fills, and broker reconciliation MUST use raw tradable prices.

REQ-PRICE-003: Technical features MAY use split-adjusted prices.

REQ-PRICE-004: Total return studies MUST declare dividend treatment.

Required fields:

```text
price_basis
corporate_action_version
split_adjustment_factor
dividend_treatment
target_return_type
```

### 7.1 Open Price Definitions

REQ-PRICE-005: For each provider, the platform MUST define:

```text
official_open_price
auction_clearing_price
first_trade_price
first_regular_session_bar_open
```

REQ-PRICE-006: If true auction data is unavailable, set:

```text
open_execution_quality = PROXY
```

and use conservative execution assumptions.

---

## 8. Labels and Outcomes

### 8.1 Research Targets

REQ-LAB-001: The fixed research targets are:

```text
research_target_log_return_5d  = ln(close[exit_session_5d]  / open[entry_session])
research_target_log_return_8d  = ln(close[exit_session_8d]  / open[entry_session])
research_target_log_return_14d = ln(close[exit_session_14d] / open[entry_session])
```

REQ-LAB-002: The research target assumes entry at the next eligible entry session open under the research execution assumption.

### 8.2 Policy and Realized Outcomes

REQ-LAB-003: Policy outcomes MUST be separate:

```text
policy_return_h_if_filled
policy_return_h_all_candidates
realized_trade_return
simulated_execution_return
actual_broker_return
```

REQ-LAB-004: Forecast reports MUST NOT mix research target performance with executed policy performance.

### 8.3 Absolute vs Excess Targets

REQ-LAB-005: The system MUST produce three target families:

```text
absolute_return_h
market_excess_return_h
sector_excess_return_h
```

REQ-LAB-006: Default recommended modeling objective:

```text
primary_ranking_target = sector_excess_return_h
portfolio_return_target = absolute executable return
```

REQ-LAB-007: The chosen primary target MUST be stored in:

```text
target_definition_version
primary_target_name
ranking_target_name
portfolio_target_name
```

REQ-LAB-008: `market_excess_return_h` MUST use a versioned benchmark contract.

Required market benchmark fields:

```text
market_benchmark_id
market_benchmark_name
market_benchmark_construction
market_benchmark_weighting
market_benchmark_return_type
market_benchmark_reinvests_dividends
market_benchmark_effective_from
market_benchmark_effective_to
benchmark_selection_approval_id
```

REQ-LAB-009: `sector_excess_return_h` MUST use point-in-time sector classification.

Required sector benchmark fields:

```text
sector_taxonomy
sector_classification_version
sector_membership_as_of
sector_benchmark_id
sector_benchmark_construction
sector_benchmark_return_type
sector_reclassification_policy
sector_benchmark_backfill_policy
```

REQ-LAB-010: If a sector ETF benchmark did not exist for a historical period, the benchmark contract MUST define whether to use a constituent portfolio proxy, exclude the period, or mark the target unavailable.

### 8.4 Barrier Labels

REQ-LAB-011: Stop/take-profit labels require a barrier ordering policy:

```text
INTRADAY_EXACT
DAILY_CONSERVATIVE_STOP_FIRST
DAILY_OPTIMISTIC_TARGET_FIRST
DAILY_AMBIGUOUS_EXCLUDED
```

Required field:

```text
barrier_ordering_status:
  EXACT
  CONSERVATIVE_ASSUMPTION
  OPTIMISTIC_ASSUMPTION
  AMBIGUOUS
```

REQ-LAB-012: Production barrier validation SHOULD use intraday data.

### 8.5 Terminal Events

REQ-LAB-013: Delisting and mergers MUST NOT silently become missing labels.

Required terminal event fields:

```text
terminal_event_type
terminal_event_date
terminal_event_value
terminal_event_source
terminal_event_return
terminal_event_confidence
```

Required policies:

```text
delisting_return_policy
cash_merger_consideration_policy
stock_merger_consideration_policy
bankruptcy_price_policy
trading_halt_policy
missing_terminal_price_policy
```

---

## 9. Feature Engineering Contract

REQ-FEAT-001: Every feature MUST be registered with:

```text
feature_name
feature_family
formula
input_fields
source_tables
unit
value_range
availability_rule
feature_available_at_rule
missing_value_policy
stale_value_policy
criticality_level
owner
feature_version
```

REQ-FEAT-002: Cross-sectional transformations MUST be date-grouped and universe-aware:

```text
cross_section_group = trading_session_id
eligible_universe_as_of_date
minimum_cross_section_size
winsorization_policy
rank_tie_policy
```

REQ-FEAT-003: Scalers, imputers, feature selection, PCA, and other learned transforms MUST be fitted only on training windows.

REQ-FEAT-004: Any feature not traceable to records available by `decision_cutoff_at` MUST be excluded.

### 9.1 Missing and Stale Data

REQ-FEAT-005: Every feature and source MUST define:

```text
maximum_age
missing_value_policy
stale_value_policy
forward_fill_limit
imputation_method
missingness_indicator
criticality_level
fallback_provider
fail_open_or_fail_closed
```

Default for critical features:

```text
fail_closed -> recommended_action = NO_ACTION
```

Silent critical-value imputation is forbidden in production.

---

## 10. Forecasting, Scores, and Calibration

### 10.1 Modeling Pipeline

REQ-MOD-001: Not every base model must natively output probabilities, intervals, and uncertainty.

Recommended pipeline:

```text
base_predictor
  -> residual_or_distribution_wrapper
  -> probability_calibration_layer
  -> uncertainty_layer
  -> decision_layer
```

REQ-MOD-002: Release 0 and Release 1 SHOULD use a shared cross-sectional model:

```text
one row per instrument-date
sector and industry features
ticker history features
date-grouped evaluation
sample weighting
minimum-history rules
```

Per-ticker models are research-only until separately approved.

### 10.2 Probability Outputs

REQ-MOD-003: The system MUST output:

```text
probability_positive_return_h = P(return_h > 0)
probability_covering_cost_h = P(return_h > expected_cost_h)
probability_exceeding_hurdle_h = P(return_h > required_hurdle_h)
```

REQ-MOD-004: `probability_up_h` is deprecated.

### 10.3 Calibration

REQ-MOD-005: Probability calibration MUST be measured by horizon.

Required calibration metrics:

```text
Brier score
log loss
expected calibration error
maximum calibration error
reliability curve
calibration slope
calibration intercept
```

REQ-MOD-006: Position sizing MUST NOT depend on uncalibrated probabilities.

### 10.4 Prediction Intervals

REQ-MOD-007: Prediction intervals MUST include:

```text
prediction_interval_coverage
downside_quantile_level
upside_quantile_level
interval_method
interval_calibration_window
empirical_coverage
coverage_error
```

Default values are placeholders until frozen:

```text
prediction_interval_coverage = TBD
downside_quantile_level = TBD
upside_quantile_level = TBD
```

### 10.5 Scores

REQ-MOD-008: `rank_score` MUST be defined as:

```text
cross-sectional percentile of risk_adjusted_utility_bps
within the eligible universe in the same decision run
```

unless an approved `rank_score_version` defines otherwise.

REQ-MOD-009: `alpha_score` MUST be a calibrated 0-1 mapping of:

```text
expected excess return
probability_exceeding_hurdle
distribution quality
```

Calibration quality MAY affect whether an alpha score is trusted, but it MUST NOT be counted independently in alpha, utility, sizing, and blocker logic unless the `score_ownership_matrix` explicitly allows that interaction.

REQ-MOD-010: `risk_score` MUST be computed from versioned components:

```text
risk_score_components
risk_score_weights
risk_score_aggregation_method
risk_score_calibration_period
risk_score_version
```

Risk components SHOULD include:

```text
volatility
expected_shortfall
gap_risk
liquidity_risk
event_risk
model_uncertainty
portfolio_concentration
```

REQ-MOD-011: The system MUST define a `score_ownership_matrix` that assigns each concern to exactly one primary decision function and any approved secondary effects.

Minimum score ownership matrix:

| Concern | Alpha | Utility | Permission | Sizing | Hard blocker |
| --- | --- | --- | --- | --- | --- |
| Expected excess return | Primary | Input | No | No | No |
| Poor calibration | Trust gate only | Optional penalty | Yes | Yes | Severe only |
| Liquidity | No | Cost/penalty | Yes | Yes | Severe only |
| Event risk | No | Penalty | Yes | Yes | Blackout only |
| Portfolio concentration | No | Penalty | Yes | Yes | Limit breach |
| Data quality | No | Optional penalty | Yes | Yes | Critical stale/missing |

REQ-MOD-012: `permission_score` MUST be a deterministic policy score, not a model probability.

Required permission score fields:

```text
permission_score_components
permission_score_weights
permission_policy_version
permission_score_before_blockers
permission_score_after_soft_penalties
permission_score
permission_blocker_reasons
```

REQ-MOD-013: A hard blocker MUST be preserved as a separate reason code even when it forces `permission_score = 0`.

### 10.6 Uncertainty and Divergence

REQ-MOD-014: The system MUST decompose uncertainty:

```text
aleatoric_uncertainty
epistemic_uncertainty
model_disagreement_uncertainty
data_quality_uncertainty
regime_uncertainty
execution_uncertainty
combined_uncertainty_score
```

REQ-MOD-015: `combined_uncertainty_score` MUST define an aggregation contract:

```text
component_scale
component_normalization
missing_component_policy
dependency_assumption
aggregation_method
critical_component_override
uncertainty_score_version
```

REQ-MOD-016: Risk-sensitive aggregation SHOULD use:

```text
combined_uncertainty_score =
    max(critical_uncertainty_components)
    + weighted_contribution(non_critical_uncertainty_components)
```

unless an approved `uncertainty_score_version` defines a different formula.

REQ-MOD-017: A very high critical uncertainty component MUST NOT be hidden by an average across many low uncertainty components.

REQ-MOD-018: The system MUST decompose divergence:

```text
temporal_divergence_score
market_divergence_score
module_disagreement_score
portfolio_conflict_score
combined_divergence_score
```

REQ-MOD-019: `combined_divergence_score` MUST only exist if its weights and formula are defined in `decision_policy_version`.

---

## 11. Cost Model Contract

REQ-COST-001: Expected cost MUST be decomposed:

```text
commission_bps
spread_cost_bps
market_impact_bps
open_auction_cost_bps
expected_slippage_bps
regulatory_fee_bps
borrow_cost_bps
```

For long-only releases:

```text
borrow_cost_bps = 0
```

REQ-COST-002: The system MUST distinguish:

```text
pretrade_expected_cost_bps
simulated_cost_bps
actual_realized_cost_bps
```

REQ-COST-003: Cost model accuracy MUST be monitored by comparing expected, simulated, and actual costs.

---

## 12. Fill Probability and Execution Forecasting

REQ-FILL-001: Fill probability models MUST be PIT-validated.

Required fields:

```text
fill_model_version
fill_training_data
entry_style
calibration_method
calibration_window
selection_bias_control
unfilled_order_policy
orders_not_sent_policy
```

REQ-FILL-002: The system MUST document whether fill modeling uses:

```text
OHLCV only
intraday bars
auction data
order book data
broker historical fills
```

REQ-FILL-003: Fill-conditioned return forecasts MUST be evaluated separately from all-candidate forecasts.

REQ-FILL-004: Fill-conditioned probabilities MUST be horizon-specific and stored in `forecast_distribution`, not as horizonless scalar fields.

Required conditional probability fields per horizon:

```text
probability_positive_if_filled_h
probability_covering_cost_if_filled_h
probability_exceeding_hurdle_if_filled_h
```

REQ-FILL-005: Release 1 MAY omit a learned fill model, but it MUST still define a deterministic fill assumption and mark fill model outputs as unavailable rather than silently defaulting them.

---

## 13. Decision Policy and Utility

REQ-DEC-001: Net edge and utility MUST use consistent units. Canonical unit: basis points.

Economic edge:

```text
economic_edge_bps = expected_return_bps - pretrade_expected_cost_bps
```

Risk-adjusted utility:

```text
risk_adjusted_utility_bps =
    economic_edge_bps
    - lambda_tail * expected_shortfall_bps
    - lambda_uncertainty * uncertainty_equivalent_bps
    - lambda_concentration * concentration_cost_bps
    - lambda_liquidity * liquidity_cost_bps
    - lambda_event * event_risk_cost_bps
```

REQ-DEC-002: Every lambda and score-to-bps mapping MUST be versioned:

```text
decision_policy_version
lambda_tail
lambda_uncertainty
lambda_concentration
lambda_liquidity
lambda_event
score_to_bps_mapping_version
```

REQ-DEC-003: Hard blockers MUST override utility.

Examples:

```text
critical_data_stale
PIT_violation
missing_price
no_tradable_instrument
earnings_blackout
max_gap_exceeded
liquidity_below_minimum
portfolio_kill_switch_active
sector_cap_exceeded
daily_loss_limit_exceeded
duplicate_order_risk
model_suspended
calibration_failed
```

REQ-DEC-004: All example thresholds are non-normative until frozen before final holdout.

REQ-DEC-005: `policy_bundle_id` MUST identify an immutable bundle of all policy and model versions used by a recommendation.

Required `policy_bundle` fields:

```text
policy_bundle_id
decision_policy_version
risk_policy_version
execution_policy_version
cost_model_version
stop_policy_version
target_policy_version
portfolio_policy_version
universe_policy_version
feature_policy_version
model_registry_snapshot_id
created_at
approved_by
effective_from
effective_to
```

REQ-DEC-006: A recommendation MUST store `policy_bundle_id` instead of relying only on many independent version fields.

---

## 14. Horizon Selection and Joint Forecast

REQ-HOR-001: The system MUST explain selected horizon:

```text
horizon_selection_policy
selected_horizon
selected_horizon_score
selected_horizon_reason
```

REQ-HOR-002: Horizon selection SHOULD consider:

```text
risk_adjusted_utility_by_horizon
probability_exceeding_hurdle_by_horizon
temporal_agreement
tail_risk_by_horizon
execution_policy_fit
portfolio_holding_constraints
```

REQ-HOR-003: Release 2+ SHOULD estimate:

```text
joint_horizon_distribution
probability_all_horizons_positive
probability_short_horizon_positive_long_horizon_negative
probability_initial_drawdown_then_recovery
```

---

## 15. Stop, Target, and Position Lifecycle

REQ-STOP-001: Stop and target calculation MUST be governed by:

```text
stop_policy_version
target_policy_version
stop_method
target_method
risk_reward_constraint
minimum_stop_distance
maximum_stop_distance
```

Allowed methods:

```text
ATR multiple
quantile-based
support/resistance
expected shortfall
optimized barrier
hybrid
```

REQ-STOP-002: Stop/target optimization MUST receive the same overfitting controls as model and threshold selection.

REQ-STOP-003: Trailing stop is out of scope for Release 0-3 unless explicitly approved.

If later enabled, required fields:

```text
trailing_stop_enabled
activation_rule
trail_distance
update_frequency
gap_behavior
broker_native_or_system_managed
```

### 15.1 Re-Recommendation Policy

REQ-POS-001: Repeated recommendations for the same instrument MUST follow:

```text
same_ticker_open_position_policy
add_to_position_policy
maximum_adds
recommendation_refresh_policy
time_stop_reset_policy
stop_update_policy
target_update_policy
position_cooldown_policy
```

REQ-POS-002: `HOLD_LONG` MUST define whether stops, targets, and open orders remain unchanged or are updated.

---

## 16. Risk Model and Position Sizing

REQ-RISK-001: The portfolio risk model MUST define:

```text
covariance_estimation_method
correlation_lookback
shrinkage_method
factor_model
beta_estimation_method
volatility_forecast_method
cluster_construction_method
risk_model_refresh_frequency
risk_model_version
```

REQ-RISK-002: Position sizing SHOULD start from risk budget:

```text
risk_budget_amount = portfolio_value * risk_budget_per_trade_pct
raw_position_notional = risk_budget_amount / planned_stop_distance_pct
```

REQ-RISK-003: Position sizing MUST include hard caps:

```text
minimum_stop_distance_pct
maximum_position_notional
maximum_ADV_participation
maximum_buying_power_usage
minimum_order_notional
share_rounding_policy
fractional_share_policy
leverage_limit
recalculate_size_after_fill
```

REQ-RISK-004: Stop is not guaranteed loss. Required:

```text
planned_stop_distance_pct
expected_loss_if_stop_triggered_pct
stress_loss_if_gap_through_stop_pct
gap_through_stop_sizing_adjustment
```

---

## 17. Portfolio Construction Protocol

REQ-PORT-001: Portfolio construction MUST define:

```text
top_k_selection_rule
cash_reserve_policy
capital_allocation_rule
risk_allocation_rule
overlapping_trade_policy
insufficient_capital_priority_rule
rebalance_cadence
daily_weight_update_policy
partial_position_policy
unexecuted_recommendation_exposure_policy
correlated_opportunity_allocation_rule
```

REQ-PORT-002: The allocation algorithm SHOULD follow:

```text
1. Remove blocked opportunities.
2. Estimate marginal portfolio utility for each candidate.
3. Allocate to the best marginal utility candidate.
4. Recalculate portfolio utility and constraints.
5. Repeat until cash, risk budget, liquidity, or concentration caps bind.
```

REQ-PORT-003: Simple one-time Top-K allocation is not sufficient for production portfolio construction.

### 17.1 Turnover and Hysteresis

REQ-PORT-004: The system MUST control churn:

```text
minimum_rank_improvement_to_replace
minimum_utility_improvement_to_trade
turnover_penalty
minimum_holding_period
rebalance_hysteresis
```

---

## 18. Validation and Metrics

### 18.1 Purged Walk-Forward

REQ-VAL-001: Walk-forward protocol MUST specify:

```text
training_window_type
training_window_length_sessions
validation_window_length_sessions
test_window_length_sessions
retraining_frequency_sessions
embargo_length_sessions
purge_rule
minimum_history_sessions
hyperparameter_refresh_frequency
feature_selection_refresh_frequency
calibration_refresh_frequency
```

REQ-VAL-002: Purge rule MUST remove training rows whose label intervals overlap validation/test intervals.

### 18.2 Final Holdout

REQ-VAL-003: Final holdout governance MUST define:

```text
holdout_id
holdout_start_date
holdout_end_date
lock_date
authorized_openers
allowed_number_of_accesses
holdout_access_audit_log
post_holdout_change_freeze
failure_response_policy
promotion_requires_signed_report
```

### 18.3 Baseline Comparison

REQ-VAL-004: Baseline comparison MUST define:

```text
baseline_id
metric
minimum_improvement
economic_significance_threshold
statistical_confidence_interval
minimum_trade_count
minimum_positive_walk_forward_windows
cost_stress_requirement
regime_coverage_requirement
```

### 18.4 Ranking Metrics

REQ-VAL-005: Ranking metrics MUST be computed within each decision date over the eligible universe.

Required:

```text
daily_cross_sectional_spearman
mean_daily_information_coefficient
information_coefficient_IR
daily_NDCG_at_K
daily_precision_at_K
```

Global Spearman over all ticker-date rows is not acceptable as the primary ranking metric.

### 18.5 Confidence Intervals

REQ-VAL-006: Trading metrics MUST include confidence intervals:

```text
metric_point_estimate
confidence_interval_low
confidence_interval_high
bootstrap_method
number_of_bootstrap_samples
serial_dependence_adjustment
```

Time-series or block bootstrap SHOULD be used.

### 18.6 Monte Carlo

REQ-VAL-007: Monte Carlo report MUST define:

```text
monte_carlo_method
number_of_simulations
block_length
parameter_perturbations
success_definition
random_seed_policy
metric_required_positive
```

### 18.7 PBO

REQ-VAL-008: Probability of Backtest Overfitting MUST define method, or report:

```text
PBO_NOT_ESTIMABLE
```

Required if estimable:

```text
method = Combinatorially Symmetric Cross-Validation or approved alternative
number_of_variations
window_partitioning
performance_statistic
minimum_windows_required
```

### 18.8 Capacity and Stability

REQ-VAL-009: Reports SHOULD include capacity:

```text
estimated_strategy_capacity
return_by_portfolio_size
slippage_by_participation_rate
capacity_breakpoint
liquidity_constrained_trade_rate
```

REQ-VAL-010: Reports SHOULD include signal stability:

```text
day_to_day_rank_stability
signal_half_life
recommendation_flip_rate
position_churn_rate
```

---

## 19. Source Reliability, News, and LLM Safety

REQ-SRC-001: Source reliability MUST be point-in-time and outcome-matured.

Required:

```text
source_id
reliability_score_as_of_time
reliability_training_window_start
reliability_training_window_end
minimum_sample_size
sample_size
confidence_interval_low
confidence_interval_high
cold_start_status
last_outcome_available_time
```

REQ-SRC-002: Source reliability SHOULD control for:

```text
event_type
sector
market_regime
market_cap_bucket
pre_event_volatility
previous_price_movement
source_sample_size
```

REQ-SRC-003: Source scoring SHOULD use shrinkage toward source-family priors.

REQ-SRC-004: Content attribution MUST classify:

```text
original_source
first_credible_publisher
independent_confirmation
copy
commentary
reaction
social_amplification
aggregator
```

REQ-SRC-005: Content clusters MUST prevent duplicate stories from counting as independent confirmations.

REQ-SRC-006: The threat model MUST include data poisoning and source manipulation risks.

Required source-threat categories:

```text
data_poisoning
source_impersonation
coordinated_social_manipulation
vendor_feed_tampering
duplicate_amplification
malicious_ticker_mentions
metadata_manipulation
model_artifact_poisoning
feature_store_poisoning
```

REQ-SRC-007: News and social features MUST include anomaly detection for sudden source-volume, duplication, and ticker-mention spikes.

### 19.1 LLM Safety

REQ-LLM-001: External text MUST be treated as untrusted data.

Required:

```text
external_text_cannot_modify_system_prompt
structured_output_only
schema_validation
no_tool_execution_from_article_text
prompt_version_logged
llm_model_version_logged
evidence_spans_required
no_numeric_claim_without_source
no_fabricated_facts
```

REQ-LLM-002: User-facing explanations MUST be generated only from structured driver objects.

Driver object:

```text
driver_id
module
feature_name
feature_value
reference_value
contribution
direction
freshness
source_reference
confidence
```

REQ-LLM-003: Any LLM-assisted production explanation or classification MUST store deterministic execution metadata.

Required LLM metadata:

```text
llm_provider
llm_model_version
prompt_hash
temperature
sampling_parameters
structured_schema_version
fallback_model
fallback_behavior
regression_test_suite_version
```

REQ-LLM-004: Production recommendation workflows SHOULD use deterministic settings such as `temperature = 0` when the provider supports them.

REQ-LLM-005: Changing LLM provider, model, prompt, sampling parameters, or structured schema version MUST trigger regression tests before promotion.

---

## 20. Data Quality and Provider Reconciliation

REQ-DQ-001: Data quality MUST measure:

```text
completeness
freshness
validity
uniqueness
consistency
accuracy
lineage
coverage
revision_rate
provider_disagreement
```

Each dimension MUST define:

```text
threshold
severity
owner
automatic_response
quarantine_policy
```

REQ-DQ-002: Provider reconciliation MUST define:

```text
provider_priority
reconciliation_rule
disagreement_threshold
reconciliation_status
winning_provider
provider_values
disagreement_reason
review_required
```

Required reconciliations:

```text
OHLCV
corporate_actions
earnings_dates
fundamental_facts
delisting_events
broker_positions
broker_orders
```

### 20.1 Capability Health and Graceful Degradation

REQ-DQ-003: The platform MUST maintain `capability_health` as a first-class operational state.

Minimum capability health flags:

```text
MARKET_DATA_HEALTHY
NEWS_UNAVAILABLE
OPTIONS_STALE
FUNDAMENTALS_PARTIAL
PORTFOLIO_STATE_HEALTHY
BROKER_RECONCILED
FEATURE_STORE_HEALTHY
MODEL_REGISTRY_HEALTHY
EVENT_LEDGER_HEALTHY
```

REQ-DQ-004: Capability health policy MUST define which system actions are allowed in degraded mode.

Initial degraded-mode policy examples:

```text
technical_only_research_recommendation_allowed_when_news_unavailable
execution_blocked_without_portfolio_state
position_sizing_reduced_without_options_data
NO_ACTION_when_raw_market_data_stale
paper_execution_blocked_when_broker_not_reconciled
counterfactual_learning_allowed_when_runtime_execution_blocked
```

REQ-DQ-005: Degraded mode MUST be explicit in recommendation status reasons, logs, UI, and audit events.

---

## 21. Execution and Broker Lifecycle

### 21.1 Order State Machine

REQ-EXEC-001: Order states MUST include uncertainty states.

Canonical order states:

```text
CREATED
VALIDATED
SUBMITTED
SUBMIT_UNKNOWN
ACKNOWLEDGED
PARTIALLY_FILLED
FILLED
REPLACE_PENDING
REPLACED
CANCEL_PENDING
CANCEL_UNKNOWN
CANCELLED
EXPIRED
REJECTED
SUSPENDED
BROKER_HELD
```

REQ-EXEC-002: `SUBMIT_UNKNOWN` and `CANCEL_UNKNOWN` MUST block retry until broker reconciliation completes.

### 21.2 Idempotency

REQ-EXEC-003: Every execution attempt MUST include:

```text
client_order_id
recommendation_id
execution_attempt_id
idempotency_key
correlation_id
```

### 21.3 Approval Concurrency

REQ-EXEC-004: Approval API MUST prevent approving stale recommendations.

Required:

```text
expected_recommendation_version
ETag_or_optimistic_lock
valid_until_check
supersession_check
portfolio_snapshot_check
```

REQ-EXEC-005: Approval validity MUST be explicit.

Required approval validity fields:

```text
approval_id
approved_at
approval_valid_until
approved_recommendation_version
approved_max_notional
approved_entry_limit
approved_policy_bundle_id
approval_auto_expires_on_material_change
```

REQ-EXEC-006: If position size, entry limit, stop/target, portfolio snapshot, risk limits, or policy bundle changes after approval, the system MUST either expire the approval or run an explicit approval carry-forward policy.

### 21.4 Broker Reconciliation

REQ-EXEC-007: On every restart before submitting new orders:

```text
broker_reconciliation_required = true
```

New orders MUST be blocked until broker/database state is reconciled.

### 21.5 Open Execution Window

REQ-EXEC-008: The open execution window MUST be governed by explicit timing fields:

```text
preopen_revalidation_deadline
approval_deadline
order_submission_earliest
order_submission_latest
market_open_buffer
late_approval_policy
```

REQ-EXEC-009: `late_approval_policy` MUST define whether late approval cancels the opportunity, requires revalidation, submits a limit order after open, or creates a new recommendation version.

### 21.6 Final Atomic Preflight

REQ-EXEC-010: Human approval is not a substitute for final pre-trade validation.

REQ-EXEC-011: Immediately before order submission the system MUST run an atomic `execution_preflight_check` containing:

```text
recommendation_still_valid
approval_still_valid
latest_portfolio_snapshot_id
latest_market_price
latest_risk_limits
no_duplicate_order
no_conflicting_open_order
kill_switch_off
instrument_tradable
price_gap_within_limit
data_not_stale
broker_reconciled
```

REQ-EXEC-012: A failed final preflight MUST block order submission and append an audit event.

### 21.7 Order Replacement Contract

REQ-EXEC-013: `REPLACE_PENDING` and `REPLACED` MUST be governed by `order_replacement_contract`.

Required replacement policy fields:

```text
replace_policy_version
replace_allowed_fields
price_change_requires_new_approval
quantity_increase_requires_new_approval
quantity_decrease_requires_new_approval
cancel_replace_is_new_order_policy
partial_fill_before_replace_policy
idempotency_key_reuse_policy
replacement_timeout_policy
```

REQ-EXEC-014: Any quantity increase or entry limit relaxation MUST require either a still-valid approval that explicitly permits the new maximum or a new approval.

### 21.8 Position Ledger and Attribution Links

REQ-EXEC-015: The broker is the source of truth for executed fills, but the platform MUST maintain an internal position ledger for strategy accounting, risk, stops, and attribution.

Required `position_lot` fields:

```text
position_lot_id
portfolio_id
instrument_id
opening_fill_id
quantity_opened
quantity_remaining
cost_basis
stop_order_id
target_order_ids
realized_pnl
unrealized_pnl
position_status
opened_at
closed_at
```

REQ-EXEC-016: The system MUST support many-to-many attribution links between recommendations, orders, fills, and position lots.

Required link entities:

```text
recommendation_position_link
recommendation_order_link
recommendation_fill_link
allocation_lot_id
attribution_method
attribution_weight
entry_alpha_component
exit_quality_component
cost_attribution_component
```

REQ-EXEC-017: Attribution reports MUST state whether PnL is attributed by FIFO, average cost, specific lot, marginal add, or another approved `attribution_method`.

---

## 22. Execution Digital Twin and Simulator

REQ-SIM-001: Backtests MUST separate:

```text
signal_return
theoretical_strategy_return
simulated_execution_return
actual_broker_return
```

REQ-SIM-002: Simulator MUST support:

```text
open auction assumptions
official open proxy policy
bid-ask spread
partial fills
volume participation
limit-order non-fill
gap through stop
trading halts
missing bars
delisted securities
early closes
corporate-action days
order rejection
latency
price improvement
slippage by liquidity bucket
```

REQ-SIM-003: The execution simulator is the offline component of the Execution Digital Twin.

REQ-SIM-004: The Execution Digital Twin MUST support evaluation of alternative execution policies for the same recommendation:

```text
market_on_open
limit_at_open_proxy
limit_after_open
delay_until_spread_normalizes
split_order
do_not_execute
```

REQ-SIM-005: Counterfactual execution outcomes MUST be linked to `counterfactual_run_id` and MUST NOT be mixed with actual broker fills.

---

## 23. Decision Ledger, Counterfactual Learning, and Digital Twin

REQ-LEARN-001: The system MUST be event-sourced at the logical decision level.

Every material state transition MUST create an append-only `decision_ledger_event`.

Minimum event types:

```text
DATA_SNAPSHOT_COMPLETED
FEATURE_SNAPSHOT_CREATED
MARKET_STATE_SNAPSHOT_CREATED
OPPORTUNITY_DETECTED
OPPORTUNITY_UPDATED
EVIDENCE_PACKET_CREATED
CANDIDATE_GENERATED
PREOPEN_REVALIDATED
RECOMMENDATION_BLOCKED
HUMAN_APPROVED
HUMAN_REJECTED
ORDER_SUBMITTED
ORDER_ACKNOWLEDGED
ORDER_PARTIALLY_FILLED
ORDER_FILLED
POSITION_OPENED
POSITION_UPDATED
STOP_TRIGGERED
TARGET_TRIGGERED
OUTCOME_MATURED
MODEL_DRIFT_DETECTED
COUNTERFACTUAL_RUN_COMPLETED
```

REQ-LEARN-002: Required `decision_ledger_event` fields:

```text
ledger_event_id
decision_cycle_id
sequence_number
event_type
entity_type
entity_id
event_time
recorded_at
actor_id
source_system
causation_id
correlation_id
payload_schema_version
payload
previous_event_hash
event_hash
```

REQ-LEARN-003: The decision ledger MUST support full replay.

Given:

```text
events
snapshots
model_artifacts
policy_bundles
feature_versions
```

the system MUST reconstruct:

```text
exactly_what_the_system_believed
why_it_made_or_abstained_from_the_decision
what_the_user_saw
what_was_approved_or_rejected
what_was_sent_to_the_broker
what_happened_afterward
```

REQ-LEARN-004: Early releases SHOULD be event-driven logically and modular-monolith physically.

Recommended first implementation:

```text
modular Python application
PostgreSQL for operational state
SQLite or DuckDB for local research workflows
append-only event table
transactional outbox
Parquet for research and history exports
object storage for artifacts
```

REQ-LEARN-005: The Learning and Counterfactual Lab MUST evaluate executed and non-executed decisions.

Required learning cohorts:

```text
executed
approved_but_not_filled
rejected_by_human
blocked_by_risk
watchlist
no_edge
data_unavailable
NO_ACTION
```

REQ-LEARN-006: The system MUST decompose errors into:

```text
forecast_error
decision_policy_error
risk_policy_error
portfolio_construction_error
execution_error
human_override_error_or_value
data_quality_error
```

REQ-LEARN-007: The Counterfactual Digital Twin MUST run approved alternative worlds for each eligible decision cycle without risking capital.

Initial counterfactual policies:

```text
actual_approved_policy
no_uncertainty_penalty
stricter_abstention
top_3_instead_of_top_10
limit_entry_instead_of_open
no_human_override
equal_weight_baseline
```

REQ-LEARN-008: Counterfactual evaluation MUST maintain virtual portfolios for each challenger policy.

Required `counterfactual_run` fields:

```text
counterfactual_run_id
decision_cycle_id
challenger_type
policy_bundle_id
counterfactual_policy_name
counterfactual_method
counterfactual_support_score
policy_overlap_score
counterfactual_confidence_interval
unsupported_reason
started_at
completed_at
run_status
replay_mode
input_snapshot_ids
```

Required `counterfactual_portfolio` fields:

```text
counterfactual_portfolio_id
counterfactual_run_id
virtual_portfolio_id
initial_cash
orders_that_would_have_been_sent
fills_that_would_have_occurred
positions_that_would_have_existed
costs_that_would_have_applied
outcomes
performance_metrics
```

REQ-LEARN-009: Challenger types MUST be separated:

```text
MODEL_CHALLENGER
DECISION_POLICY_CHALLENGER
RISK_POLICY_CHALLENGER
EXECUTION_POLICY_CHALLENGER
PORTFOLIO_CONSTRUCTION_CHALLENGER
HUMAN_OVERRIDE_CHALLENGER
```

REQ-LEARN-010: Reports MUST identify whether the largest improvement opportunity comes from model quality, abstention policy, entry policy, sizing, turnover, portfolio construction, human intervention, or execution.

REQ-LEARN-011: Learning outputs MUST NOT directly mutate production models, policies, thresholds, or prompts. They MUST enter the Research Factory or governance promotion workflow.

### 23.1 Value of Information

REQ-LEARN-012: The system SHOULD estimate the value of additional information before acting when uncertainty is material.

Required fields:

```text
expected_value_of_information
expected_uncertainty_reduction
cost_of_information
decision_change_probability
information_deadline
information_source
```

REQ-LEARN-013: The decision policy MAY produce:

```text
eligibility_state = CONDITIONAL
recommended_action = NO_ACTION
status_reason_code = DEFER_PENDING_INFORMATION
```

when the expected value of waiting for additional information exceeds the expected utility of acting immediately.

### 23.2 Human Override Learning

REQ-LEARN-014: Manual approval and rejection MUST be treated as decision evidence, not only as a gate.

Required human decision reason codes:

```text
APPROVE_AS_RECOMMENDED
APPROVE_SMALLER_SIZE
REJECT_RISK_TOO_HIGH
REJECT_THESIS_NOT_CONVINCING
REJECT_EXTERNAL_INFORMATION
REJECT_PORTFOLIO_PREFERENCE
REJECT_EXECUTION_PRICE
```

REQ-LEARN-015: Human override analytics MUST compare:

```text
system_only_portfolio
human_only_changes
combined_human_system_portfolio
```

REQ-LEARN-016: The platform MUST measure but not blindly imitate human overrides.

Required analytics:

```text
human_override_value
human_override_bias
override_value_by_reason
override_value_by_regime
override_value_by_instrument_familiarity
override_value_by_recent_performance_context
```

### 23.3 Decision Sensitivity

REQ-LEARN-017: Each actionable recommendation SHOULD expose `decision_sensitivity`: the conditions that would change the decision.

Examples:

```text
pre_market_gap_exceeds_limit -> block
market_state_score_below_threshold -> reduce_size
sector_relative_strength_turns_negative -> WATCHLIST
uncertainty_falls_after_event -> reconsider
price_reaches_level_without_new_evidence -> opportunity_exhausted
```

REQ-LEARN-018: Decision sensitivity MUST be derived from policy and evidence objects, not invented as free text after the decision.

### 23.4 Module Marginal Value

REQ-LEARN-019: The platform MUST measure the marginal value of each module relative to the already-existing system.

Required module marginal-value metrics:

```text
incremental_net_return
incremental_precision
incremental_drawdown_reduction
incremental_abstention_quality
incremental_calibration_improvement
incremental_cost
incremental_operational_risk
incremental_data_licensing_risk
```

REQ-LEARN-020: Module promotion SHOULD depend on incremental system value, not only standalone AUC, standalone accuracy, or standalone feature importance.

### 23.5 Counterfactual Reliability

REQ-LEARN-021: Counterfactual outputs MUST be classified by support level.

Allowed `counterfactual_method` values:

```text
REPLAYABLE_COUNTERFACTUAL
MODEL_BASED_COUNTERFACTUAL
UNSUPPORTED_COUNTERFACTUAL
```

REQ-LEARN-022: Replayable counterfactuals are alternatives that can be computed directly from observed historical market data, such as:

```text
different_entry_limit
smaller_position_size
different_horizon_exit
different_stop_or_target_policy_when_intraday_path_is_available
```

REQ-LEARN-023: Model-based counterfactuals require explicit statistical assumptions and MUST expose support and uncertainty, such as:

```text
trading_opportunities_the_system_historically_rejected
removing_human_approval
selecting_a_different_correlated_instrument
changing_permission_policy_outside_observed_selection_region
```

REQ-LEARN-024: Unsupported counterfactuals MUST NOT be presented as performance evidence.

Required unsupported reason examples:

```text
outside_historical_support
insufficient_overlap
missing_execution_data
missing_outcome_data
policy_changes_population_too_much
```

REQ-LEARN-025: Counterfactual reports MUST display `counterfactual_support_score`, `policy_overlap_score`, `counterfactual_method`, `counterfactual_confidence_interval`, and `unsupported_reason` when applicable.

### 23.6 Decision Error Attribution

REQ-LEARN-026: The platform MUST produce `decision_error_attribution` for matured losses, major misses, and sampled successful decisions.

Allowed error categories:

```text
DATA_ERROR
WORLD_STATE_ERROR
OPPORTUNITY_IDENTIFICATION_ERROR
FORECAST_ERROR
CALIBRATION_ERROR
DECISION_POLICY_ERROR
PORTFOLIO_ALLOCATION_ERROR
EXECUTION_ERROR
HUMAN_OVERRIDE_ERROR
UNAVOIDABLE_MARKET_NOISE
```

Required `decision_error_attribution` fields:

```text
decision_error_attribution_id
recommendation_id
outcome_record_id
primary_error_source
secondary_error_sources
avoidable_loss_bps
unavoidable_loss_bps
evidence
confidence
recommended_remediation
reviewed_by
reviewed_at
```

REQ-LEARN-027: Error attribution MUST identify which architectural component should improve, not only which model feature was important.

### 23.7 Event-Triggered Decisioning

REQ-LEARN-028: Value of Information MUST support decision timing, not only data-purchase decisions.

Allowed timing actions:

```text
ACT_NOW
WAIT_FOR_PREMARKET_VOLUME
WAIT_FOR_EARNINGS
WAIT_FOR_SPREAD_NORMALIZATION
WAIT_FOR_EVENT_CONFIRMATION
DISCARD
```

Required timing fields:

```text
expected_value_of_waiting
expected_value_of_information
expected_opportunity_decay
probability_decision_changes
next_reassessment_trigger
next_reassessment_deadline
```

REQ-LEARN-029: The system SHOULD support event-triggered reassessment in addition to daily batch runs.

Initial reassessment triggers:

```text
earnings_published
gap_exceeds_threshold
new_independent_evidence_arrives
market_state_probability_changes_materially
spread_normalizes
broker_reconciliation_completed
```

### 23.8 Module Value Profile

REQ-LEARN-030: Each optional module MUST maintain a `module_value_profile`.

Required value profile fields:

```text
module_id
module_version
incremental_alpha
incremental_risk_reduction
incremental_calibration
incremental_abstention_quality
incremental_drawdown_reduction
incremental_operational_cost
incremental_latency
incremental_failure_surface
incremental_data_cost
incremental_complexity_cost
net_module_value
evaluation_window
evaluation_method
```

REQ-LEARN-031: `net_module_value` MUST account for economic contribution, risk reduction, operating cost, complexity cost, and failure risk.

REQ-LEARN-032: A module that does not add positive marginal system value SHOULD be removed, disabled, or kept research-only even if it is technically advanced.

### 23.9 Selective Adaptation

REQ-LEARN-033: The architecture MUST be selectively adaptive rather than freely self-modifying.

Allowed adaptation path:

```text
adaptive_candidate
  -> shadow_evaluation
  -> counterfactual_validation
  -> governance_promotion
```

REQ-LEARN-034: Each component MUST declare an adaptation cadence.

Fast-adaptation candidates:

```text
calibration
cost_model
fill_model
data_freshness_thresholds
regime_priors
```

Slow-adaptation candidates:

```text
core_forecast_model
decision_utility_function
portfolio_risk_limits
universe_policy
```

---

## 24. Monitoring, Observability, and Delayed Outcomes

REQ-MON-001: Outcome monitoring MUST distinguish:

```text
pending_recommendations
partially_matured_recommendations
fully_matured_recommendations
```

Immediate monitors:

```text
data_freshness
feature_distribution
prediction_distribution
recommendation_volume
abstention_rate
portfolio_exposure
model_disagreement
hard_blocker_rate
```

Delayed monitors:

```text
calibration
precision
return
drawdown
slippage
hit_rate
barrier_ordering_quality
```

REQ-MON-002: Observability MUST include:

```text
structured_logs
distributed_traces
technical_metrics
correlation_ids
decision_cycle_id_in_all_logs
recommendation_id_in_all_execution_logs
log_retention
PII_and_secret_redaction
```

REQ-MON-003: Logs MUST support trace:

```text
API request
  -> decision run
  -> recommendation
  -> approval
  -> order
  -> broker response
  -> fill
```

---

## 25. Audit, Governance, and Organizational Exceptions

REQ-AUD-001: Audit logs MUST be append-only.

Required fields:

```text
event_id
actor_id
event_type
entity_type
entity_id
previous_value
new_value
timestamp
reason
policy_version
hash_chain_or_tamper_evidence
retention_policy
```

REQ-GOV-001: Model governance roles:

```text
model_owner
developer
independent_validator
risk_approver
production_approver
data_owner
execution_owner
```

REQ-GOV-002: For small-team or solo development, define:

```text
independence_exception_policy
self_validation_disclosure
external_review_requirement_before_live
```

REQ-GOV-003: Model status enum:

```text
DRAFT
RESEARCH
VALIDATION_PENDING
VALIDATED
SHADOW
PAPER_APPROVED
LIVE_APPROVED
SUSPENDED
RETIRED
```

REQ-GOV-004: Champion/challenger promotion MUST pass:

```text
offline validation
locked holdout
shadow mode
paper portfolio
limited promotion
full promotion
continuous comparison
```

REQ-GOV-005: Every TBD or placeholder threshold MUST have governance metadata.

Required threshold governance fields:

```text
threshold_id
threshold_owner
proposed_value
evidence_source
freeze_deadline
approved_by
effective_from
effective_to
change_reason
```

REQ-GOV-006: Threshold values MUST be frozen before final holdout access. Any threshold change after holdout access MUST trigger the documented post-holdout change policy.

REQ-GOV-007: Data, model, policy, feature, and test artifacts MUST declare their promotion environment.

Allowed environments:

```text
RESEARCH
VALIDATION
SHADOW
PAPER
LIVE
```

Required artifact promotion fields:

```text
artifact_id
artifact_type
artifact_version
artifact_environment
promotion_status
promoted_from
promoted_at
approved_by
approval_record_id
checksum
provenance_uri
```

REQ-GOV-008: A lower-environment artifact MUST NOT be loaded by a higher-environment workflow unless an explicit promotion record exists.

### 25.1 Control Plane Contract

REQ-GOV-009: The Control Plane MUST be treated as a product capability with its own contract.

The Control Plane MUST manage:

```text
artifact_registry
policy_registry
capability_flags
environment_promotion
kill_switches
threshold_governance
runtime_configuration
release_compatibility
dependency_compatibility
schema_registry
```

REQ-GOV-010: Before each decision cycle, the Control Plane MUST create a `runtime_manifest`.

Required `runtime_manifest` fields:

```text
runtime_manifest_id
decision_cycle_id
approved_model_bundle
approved_policy_bundle
enabled_capabilities
disabled_capabilities
degraded_capabilities
data_provider_versions
schema_versions
code_version
artifact_checksums
release_compatibility_status
dependency_compatibility_status
created_at
created_by
```

REQ-GOV-011: `DECISION_RUNTIME` MUST load only artifacts and capabilities included in the approved `runtime_manifest`.

REQ-GOV-012: A runtime manifest mismatch MUST block new recommendations and append a decision ledger event.

---

## 26. Kill Switch and Incident Runbook

REQ-KILL-001: Kill switch MUST define:

```text
automatic_triggers
manual_triggers
scope_new_orders_only_or_close_positions
authorized_activators
authorized_resetters
two_person_reset_required
open_order_handling
open_position_handling
audit_log_record
notification_targets
post_incident_review_required
```

REQ-INC-001: Incident runbook MUST cover:

```text
data_provider_down
model_artifact_failed_to_load
abnormal_number_of_buy_signals
broker_order_submitted_no_ack
partial_fill
service_restart_with_open_positions
broker_stop_exists_but_database_missing
database_order_exists_but_broker_missing
portfolio_state_mismatch
stale_portfolio_snapshot
duplicate_order_attempt
```

---

## 27. API Contract Requirements

REQ-API-001: API specification MUST include:

```text
authentication
authorization
API versioning
request schema
response schema
pagination
filtering
error model
idempotency
optimistic locking
rate limits
correlation ID
audit fields
```

REQ-API-002: Required core endpoints:

```text
POST /decision-cycles
GET  /decision-cycles/{id}
GET  /decision-cycles/{id}/runtime-manifest
GET  /decision-cycles/{id}/decision-budget
GET  /recommendations
GET  /recommendations/{id}
GET  /recommendations/{id}/aggregate
GET  /recommendations/{id}/forecast-snapshot
GET  /recommendations/{id}/decision-assessment
GET  /recommendations/{id}/risk-assessment
GET  /recommendations/{id}/execution-plan
GET  /recommendations/{id}/evidence
GET  /recommendations/{id}/decision-sensitivity
POST /recommendations/{id}/approve
POST /recommendations/{id}/reject
POST /recommendations/{id}/execution-preflight
GET  /opportunities
GET  /opportunities/{id}
GET  /market-state/{decision_cycle_id}
GET  /decision-ledger/{decision_cycle_id}
POST /decision-ledger/{decision_cycle_id}/replay
POST /counterfactual-runs
GET  /counterfactual-runs/{id}
GET  /capabilities
GET  /runtime-manifests/{id}
GET  /portfolio/state
GET  /positions/lots
GET  /orders/{id}
GET  /fills/{id}
GET  /outcomes/{id}
GET  /models
GET  /data-health
GET  /backtests/{id}
```

REQ-API-003: Approval endpoint MUST include optimistic concurrency:

```text
If-Match_ETag
expected_recommendation_version
approval_actor_id
approval_reason
portfolio_snapshot_id
approval_valid_until
approved_max_notional
approved_entry_limit
approved_policy_bundle_id
```

REQ-API-004: API schemas MUST be entity-specific and stage-aware. Clients MUST NOT be required to parse one wide nullable recommendation object to infer lifecycle state.

REQ-API-005: All mutating endpoints MUST return:

```text
entity_id
entity_version
ETag
correlation_id
audit_event_id
idempotency_key_if_applicable
```

REQ-API-006: Error responses MUST include:

```text
error_code
message
retryable
blocking_requirement_id
correlation_id
audit_event_id_if_created
```

---

## 28. Non-Functional and Security Requirements

REQ-NFR-001: Operational targets MUST be defined:

```text
pipeline_completion_deadline
maximum_scoring_latency
maximum_dashboard_latency
availability_target
recovery_time_objective
recovery_point_objective
backup_frequency
retention_period
maximum_monthly_infrastructure_cost
maximum_monthly_data_cost
```

REQ-NFR-002: Late pipeline policy MUST be defined. Default:

```text
BLOCK_ALL_NEW_ACTIONS
```

REQ-NFR-003: Early production architecture SHOULD be a modular monolith with strict logical boundaries.

Required bounded contexts:

```text
Temporal Data Kernel
World State and Evidence
Opportunity Memory
Decision, Risk and Portfolio
Execution and Broker
Learning, Counterfactual and Governance
```

Required modular-monolith boundaries:

```text
data
world_state
features
forecast
decision
risk
portfolio
execution
learning
governance
```

REQ-NFR-004: The modular monolith SHOULD use:

```text
separate_database_schemas_by_responsibility
schema_contract_tests
append_only_events
transactional_outbox
artifact_store
shared_observability_contract
```

REQ-NFR-005: Microservice extraction MUST require documented operational justification.

REQ-NFR-006: First implementation SHOULD use:

```text
one_modular_application
one_worker_orchestrator
one_operational_database
one_separate_execution_boundary
```

REQ-SEC-001: Security requirements:

```text
secret_manager
encryption_at_rest
encryption_in_transit
role_based_access_control
MFA_for_live_actions
separate_paper_and_live_infrastructure
broker_keys_without_withdrawal_permission
key_rotation
signed_model_artifacts
signed_config_releases
tamper_evident_audit_logs
dependency_vulnerability_scanning
broker_credential_isolation
approval_identity_and_timestamp
```

REQ-SEC-002: Secrets in source code are a hard blocker.

REQ-SEC-003: Supply-chain security MUST include:

```text
dependency_pinning
hash_verification
SBOM
signed_containers
restricted_CI_secrets
reproducible_builds
artifact_provenance
branch_protection
approval_before_deployment
```

---

## 29. Test Strategy

REQ-TEST-001: Test strategy MUST include:

```text
unit_tests
integration_tests
schema_contract_tests
temporal_invariant_tests
PIT_leakage_tests
property_based_tests
replay_tests
golden_dataset_tests
corporate_action_tests
delisting_tests
broker_simulation_tests
restart_recovery_tests
chaos_tests
security_tests
performance_tests
decision_ledger_replay_tests
counterfactual_consistency_tests
opportunity_lifecycle_tests
evidence_packet_contract_tests
market_state_snapshot_consistency_tests
capability_degradation_tests
architectural_fitness_tests
```

REQ-TEST-002: Property-based tests SHOULD include:

```text
No feature can be available after decision_cutoff_at.
Recommendation without model version cannot become VALID.
Order cannot become FILLED without broker acknowledgement or reconciliation.
Position size cannot exceed the minimum of all applicable caps.
Expired recommendation cannot be approved.
Same snapshot and seed produce same deterministic result.
Ledger replay reconstructs the same recommendation aggregate.
Counterfactual runs cannot mutate runtime recommendations.
Evidence packets with the same independence group cannot count as independent confirmation.
Runtime cannot load unpromoted research artifacts.
DECISION_RUNTIME cannot import research-only modules.
Execution cannot access unapproved artifacts.
Only Risk service can write risk_assessment.
Only Broker adapter can write fill_record.
No runtime component can mutate completed decision_cycle.
Every recommendation must reference one policy_bundle.
Every decision event must have correlation and causation IDs.
No counterfactual result can appear as actual outcome.
```

REQ-TEST-003: Golden dataset MUST include:

```text
split
dividend
delisting
merger
missing bar
after-hours earnings
pre-market filing
gap over limit
stop and target in same day
ticker change
provider disagreement
trading halt
partial fill
broker unknown state
```

REQ-TEST-004: Golden datasets MUST be versioned and immutable.

Required golden dataset metadata:

```text
golden_dataset_version
expected_output_version
approved_by
checksum
allowed_tolerance
change_request_id
review_status
```

REQ-TEST-005: Changing expected golden outputs MUST require review and MUST NOT be used to hide a bug by redefining success after failure.

---

## 30. Acceptance Gate Matrix

REQ-GATE-001: Numeric thresholds MUST be frozen before final holdout. Until then, threshold cells are `TBD`.

Each `TBD` threshold MUST have a `threshold_id` linked to the governance metadata in REQ-GOV-005.

| Area | Metric | Threshold | Gate |
|---|---:|---:|---|
| Leakage | future feature rows | 0 | Hard |
| PIT | production features without proven `feature_available_at` | 0 | Hard |
| Snapshot | recommendations without snapshot IDs | 0 | Hard |
| Reproducibility | deterministic rerun mismatch | 0 or approved tolerance | Hard |
| Universe | hindsight universe filters | 0 | Hard |
| Labels | incorrect target basis | 0 | Hard |
| Purging | overlapping train/test label windows | 0 | Hard |
| Calibration | maximum ECE by horizon | TBD | Hard |
| Edge | net excess return vs baseline | TBD | Hard |
| Costs | performance under 2x slippage | TBD | Hard |
| Drawdown | maximum drawdown | TBD | Hard |
| Stability | positive walk-forward windows | TBD | Hard |
| Monte Carlo | successful scenarios | TBD | Hard |
| Shadow | minimum shadow days | TBD | Hard |
| Shadow | minimum matured recommendations | TBD | Hard |
| Shadow | minimum executed paper trades | TBD | Hard |
| Shadow | minimum regime coverage | TBD | Hard |
| Liquidity | minimum tradable volume, spread, and capacity limits | TBD | Hard |
| Abstention | confidence, uncertainty, and NO_ACTION thresholds | TBD | Hard |
| Risk | maximum position, concentration, loss, and portfolio exposure limits | TBD | Hard |
| Overnight SLA | latest allowed completion time before pre-open validation | TBD | Hard |
| Readiness | unresolved hard `TBD` thresholds for claimed readiness level | 0 | Hard |
| Data quality | stale critical sources | 0 | Hard |
| Risk | exposure violations | 0 | Hard |
| Execution | duplicate orders | 0 | Hard |
| Recovery | broker reconciliation after restart | Pass | Hard |
| Security | secrets in repo | 0 | Hard |
| Governance | approval record for promoted model | Present | Hard |
| Ledger | replay mismatch for approved cycles | 0 or approved tolerance | Hard |
| Runtime boundary | unapproved research artifact loaded by runtime | 0 | Hard |
| Kernel boundary | plugin capability required without declaration | 0 | Hard |
| Runtime manifest | decision cycle without approved manifest | 0 | Hard |
| Counterfactual | learning lab mutates runtime policy directly | 0 | Hard |
| Counterfactual reliability | unsupported counterfactual presented as evidence | 0 | Hard |
| Counterfactual support | missing support or overlap score | 0 | Hard |
| Evidence | duplicate independent evidence counting | 0 | Hard |
| Evidence dependency | root event counted multiple times | 0 | Hard |
| Capability health | execution allowed without required capability | 0 | Hard |
| Conversation capability | missing kernel/capability classification | 0 | Hard |
| Conversation capability | optional module promoted without module value profile | 0 | Hard |
| Conversation capability | enabled runtime capability missing from manifest | 0 | Hard |
| Operator tools | diagnostic tool silently mutates canonical data | 0 | Hard |

REQ-GATE-002: High Sharpe cannot override hard failures such as drawdown breach, leakage, stale critical data, or risk limit violations.

REQ-GATE-003: The system MUST NOT be declared `PAPER_READY`, `LIVE_READY`, or equivalent while any hard threshold remains `TBD`, including maximum ECE, maximum drawdown, minimum trade count, minimum shadow days, liquidity limits, abstention thresholds, risk limits, and overnight completion SLA.

---

## 31. Required Implementation Contract Packages

REQ-DOC-001: This document is the canonical source of truth. The implementation team MUST derive the following contract packages from it before declaring the system implementation-ready.

REQ-DOC-002: The packages MAY be maintained as sections, generated schema files, or controlled companion artifacts, but their normative content MUST trace back to this document.

### 31.1 Canonical Data Model Package

REQ-DOC-003: The Canonical Data Model package MUST include:

```text
entity_relationship_diagram
entity_definitions
field_types
enum_definitions
nullability_rules
immutability_rules
foreign_keys
unique_constraints
stage_requiredness_matrix
source_of_truth_matrix
allowed_writer_matrix
schema_migration_policy
backward_compatibility_policy
```

Minimum included entities:

```text
decision_cycle
decision_budget
runtime_manifest
market_state_snapshot
market_state_hypothesis
opportunity
recommendation
evidence_packet
evidence_dependency_graph
forecast_snapshot
forecast_distribution
joint_horizon_distribution
decision_assessment
risk_assessment
execution_plan
approval_record
execution_record
order_record
fill_record
position_lot
outcome_record
explanation_package
counterfactual_run
counterfactual_portfolio
decision_error_attribution
module_value_profile
decision_ledger_event
audit_event
```

### 31.2 Labeling Specification Package

REQ-DOC-004: The Labeling Specification package MUST include:

```text
exchange_calendar
entry_convention
exit_convention
holding_period_counting
corporate_action_policy
delisting_policy
terminal_event_policy
absolute_return_definition
market_excess_return_definition
sector_excess_return_definition
benchmark_contracts
barrier_ordering_policy
outcome_maturity_policy
label_versioning_policy
```

### 31.3 Walk-Forward and Holdout Protocol Package

REQ-DOC-005: The Walk-Forward and Holdout Protocol package MUST include frozen, reviewable methods for:

```text
train_validation_test_calendar
purge_algorithm
embargo_rule
retraining_schedule
feature_selection_refresh_policy
hyperparameter_refresh_policy
calibration_protocol
bootstrap_method
PBO_method
Monte_Carlo_method
final_holdout_access_policy
post_holdout_change_policy
```

### 31.4 Decision, Risk, and Cost Policy Package

REQ-DOC-006: The Decision, Risk, and Cost Policy package MUST include:

```text
score_ownership_matrix
score_units
alpha_score_definition
rank_score_definition
permission_score_definition
utility_formula
blocker_catalog
soft_penalty_catalog
position_sizing_formula
portfolio_allocation_algorithm
turnover_and_hysteresis_policy
cost_model_formula
fill_model_policy
stop_target_policy
threshold_governance
policy_bundle_schema
```

### 31.5 Test and Traceability Package

REQ-DOC-007: The Test and Traceability package MUST include:

```text
requirement_to_design_trace
design_to_code_trace
code_to_test_trace
schema_contract_tests
PIT_invariant_tests
replay_tests
property_based_tests
broker_recovery_tests
golden_dataset
acceptance_gate_matrix
test_data_versioning
coverage_acceptance_policy
architectural_fitness_functions
```

### 31.6 Decision Learning and Counterfactual Package

REQ-DOC-008: The Decision Learning and Counterfactual package MUST include:

```text
decision_ledger_event_schema
ledger_replay_protocol
counterfactual_run_schema
counterfactual_portfolio_schema
counterfactual_reliability_policy
counterfactual_support_scoring
challenger_type_catalog
executed_and_unexecuted_outcome_cohorts
error_decomposition_taxonomy
decision_error_attribution_schema
human_override_analytics
value_of_information_policy
event_triggered_decisioning_policy
decision_sensitivity_schema
module_marginal_value_methodology
module_value_profile_schema
adaptation_cadence_policy
learning_to_research_promotion_policy
```

### 31.7 World Model, Opportunity, Evidence, and Graph Package

REQ-DOC-009: The World Model, Opportunity, Evidence, and Graph package MUST include:

```text
market_state_snapshot_schema
market_state_hypothesis_schema
market_state_vector_definitions
opportunity_schema
opportunity_type_catalog
opportunity_lifecycle_policy
adversarial_thesis_review_policy
evidence_packet_schema
evidence_dependency_graph_schema
expert_module_contracts
evidence_independence_policy
contradictory_evidence_policy
knowledge_graph_schema
graph_node_and_edge_catalog
structural_graph_schema
temporal_market_graph_schema
graph_entity_resolution_policy
graph_exposure_mapping_policy
```

### 31.8 Control Plane and Kernel Boundary Package

REQ-DOC-010: The Control Plane and Kernel Boundary package MUST include:

```text
decision_kernel_definition
replaceable_capability_catalog
capability_health_policy
runtime_manifest_schema
artifact_registry_contract
policy_registry_contract
release_compatibility_policy
dependency_compatibility_policy
plugin_promotion_policy
kernel_boundary_fitness_tests
microservice_extraction_policy
```

### 31.9 Conversation-Derived Capability Package

REQ-DOC-011: The Conversation-Derived Capability package MUST include:

```text
conversation_capability_catalog
kernel_or_capability_classification_matrix
bounded_context_mapping
canonical_entity_mapping
runtime_manifest_mapping
capability_health_mapping
overnight_pipeline_contract
market_data_normalization_contract
technical_feature_library_contract
sequence_model_research_contract
graph_macro_feature_contract
content_finbert_source_profile_contract
content_market_linkage_contract
dataset_schema_parity_contract
operator_tool_contract
conversation_specific_test_plan
conversation_traceability_matrix
```

REQ-DOC-012: The canonical package MUST be accompanied by three controlled implementation artifacts:

```text
RELEASE_0_1A_IMPLEMENTATION_BACKLOG.md
CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md
REQUIREMENT_TO_CODE_COVERAGE_MATRIX.md
```

REQ-DOC-013: The system MUST NOT be called implementation-ready until all required packages above are complete, versioned, reviewed, and linked to requirement IDs.

---

## 32. Conversation-Derived Implementation Contract

This section converts the concrete implementation work discussed during the stock-analysis project into canonical, testable requirements. It closes the gap between the platform-level architecture above and the operational Python pipelines, feature tables, model experiments, diagnostics, and overnight jobs already designed in project conversations.

### 32.0 Authority and Coverage

REQ-CONV-001: The requirements in this section are normative and have the same authority as all other requirements in this document.

REQ-CONV-002: A capability described elsewhere at a high level MUST NOT be considered implemented merely because a generic interface exists. The concrete behaviors, schemas, failure modes, and tests below MUST also be satisfied when that capability is enabled.

REQ-CONV-003: The following conversation-derived implementation areas are explicitly in scope:

```text
overnight pipeline orchestration
SEC EDGAR point-in-time build and cache lifecycle
market-data adapter and DataFrame normalization
technical indicators and candlestick-pattern features
candlestick visualization and inspection utilities
hybrid tabular-plus-sequence modeling, including LSTM candidates
cross-sectional graph features
macro and sector context features
news and social content ingestion
FinBERT sentiment and baseline sentiment comparison
content enrichment and source profiling
content-to-market linkage
training and latest-feature dataset contracts
checkpointing, retries, resumability, and operator diagnostics
```

REQ-CONV-004: Exact Python class or function names shown in examples, such as `LongOvernightConfigFactory`, `PipelineOrchestrator.run_with_retries`, or `build_content_market_link`, MAY change, but their contracts and observable behavior MUST remain traceable to stable requirement IDs and tests.

REQ-CONV-005: Conversation-derived experimental features MUST still obey the Research Factory, Decision Runtime, promotion, PIT, leakage, licensing, and governance boundaries defined elsewhere in this document.

### 32.0.1 Architectural Classification and Integration

REQ-CONV-ARCH-001: Every conversation-derived implementation area MUST be classified before implementation or promotion.

Allowed classifications:

```text
DECISION_KERNEL_COMPONENT
REQUIRED_PLATFORM_INFRASTRUCTURE
CONTROL_PLANE_COMPONENT
TEMPORAL_DATA_COMPONENT
REQUIRED_CAPABILITY
OPTIONAL_CAPABILITY
RESEARCH_ONLY_CANDIDATE
OPERATOR_TOOL
```

REQ-CONV-ARCH-002: Each conversation-derived capability MUST declare:

```text
capability_id
classification
bounded_context
release_criticality
owning_service_or_module
source_of_truth_entity
allowed_writer
required_release_phase
allowed_environments
runtime_manifest_flag
capability_health_flag
promotion_gate
module_value_profile_required
fallback_or_degraded_behavior
```

REQ-CONV-ARCH-003: The following classification matrix is normative:

| Conversation-derived area | Classification | Bounded context | Release phase | Architectural note |
| --- | --- | --- | --- | --- |
| Overnight orchestration, retries, checkpoints, run report | `CONTROL_PLANE_COMPONENT` | Control Plane / Temporal Data | Release 0 | Required platform infrastructure for deterministic replay and artifact integrity; not part of the Decision Kernel |
| Market-data adapter and DataFrame normalization | `TEMPORAL_DATA_COMPONENT` | Temporal Data | Release 0 | Required before any feature or label computation; not part of the Decision Kernel |
| `training_df` / `latest_features_df` schema parity | `TEMPORAL_DATA_COMPONENT` | Temporal Data / Research Factory | Release 0-1A | Required for reproducible research-to-runtime promotion; not part of the Decision Kernel |
| Basic technical features | `REQUIRED_CAPABILITY` | World State and Evidence | Release 1A | Required only as the first evidence capability, not as permanent model lock-in |
| Candlestick visualization and inspection | `OPERATOR_TOOL` | Learning / Governance | Release 1A | Read-only diagnostic surface |
| SEC EDGAR / XBRL PIT build | `OPTIONAL_CAPABILITY` | Temporal Data / World State and Evidence | Release 2A | Required only when fundamentals module is enabled |
| Graph and macro-sector features | `OPTIONAL_CAPABILITY` | World State and Evidence | Release 2A | Must respect structural vs temporal graph contracts |
| News/social ingestion and FinBERT | `OPTIONAL_CAPABILITY` | World State and Evidence | Release 2A | Must satisfy licensing, source, and manipulation controls |
| URL resolution | `OPTIONAL_CAPABILITY` | World State and Evidence | Release 2A | Must be isolated; failure cannot discard valid content metadata |
| Content-to-market linkage | `OPTIONAL_CAPABILITY` | World State and Evidence / Learning Lab | Release 2A-2B | Labels and source reliability must mature before learning |
| Hybrid LSTM or other sequence model | `RESEARCH_ONLY_CANDIDATE` | Research Factory | Release 4 candidate | Must not become runtime dependency before promotion |
| Reusable debugging utilities | `OPERATOR_TOOL` | Learning / Governance | Release 0+ | Read-only by default and redacted |

REQ-CONV-ARCH-004: Conversation-derived requirements MUST NOT weaken the Decision Kernel boundary. A concrete implementation detail is promoted into the kernel only if the kernel cannot remain correct, reproducible, or auditable without it.

REQ-CONV-ARCH-005: Optional capabilities MUST be loadable, disableable, and replaceable through the Control Plane. Their enabled/disabled/degraded state MUST appear in `runtime_manifest`.

REQ-CONV-ARCH-006: Any optional capability that affects recommendations MUST emit evidence packets, feature lineage, capability health, and module value metrics.

REQ-CONV-ARCH-007: Research-only candidates, including LSTM or other sequence models, MUST write research artifacts and reports but MUST NOT write runtime recommendation entities unless promoted.

REQ-CONV-ARCH-008: Operator tools MUST be read-only by default, auditable, and forbidden from silently mutating canonical datasets, recommendation records, fills, outcomes, or ledger events.

REQ-CONV-ARCH-009: Conversation-derived features MUST connect to canonical entities rather than creating parallel data models.

Required mappings:

```text
overnight run -> decision_cycle + runtime_manifest + decision_budget + decision_ledger_event
normalized OHLCV -> source_record + feature_snapshot
technical indicators -> feature_registry + evidence_packet
candlestick patterns -> evidence_packet + explanation_package
graph/macro features -> market_state_snapshot + temporal_market_graph + feature_snapshot
content items -> content_item + source_profile + evidence_packet
content market links -> content_market_link + outcome_record when matured
training_df/latest_features_df -> feature_snapshot + model_training_artifact
debugging utilities -> audit_event(event_type = OPERATOR_TOOL_USED)
```

REQ-CONV-ARCH-010: A conversation-derived module MUST NOT be considered production-ready until its classification, canonical entity mappings, capability health behavior, promotion environment, and test IDs are complete.

REQ-CONV-ARCH-011: The implementation SHOULD avoid creating a new table or object when an existing canonical entity can own the concept without ambiguity.

REQ-CONV-ARCH-012: If a conversation-derived table remains project-specific, it MUST declare whether it is:

```text
canonical_source_of_truth
derived_view
research_only_artifact
operator_diagnostic_view
temporary_migration_artifact
```

REQ-CONV-ARCH-013: All conversation-derived capabilities MUST define degraded behavior. Degraded behavior may be `disable_capability`, `research_only`, `reduce_position_size`, `block_execution`, `fallback_to_baseline`, or `NO_ACTION`.

REQ-CONV-ARCH-014: Module marginal-value evaluation is required before promoting any optional conversation-derived capability from Research Factory to Decision Runtime.

REQ-CONV-ARCH-015: The traceability matrix MUST include a column for `kernel_or_capability_classification` and a column for `bounded_context`.

REQ-CONV-ARCH-016: Only the seven components listed in `REQ-PROD-020` may be labeled `DECISION_KERNEL_COMPONENT` without a governance-approved kernel-boundary change.

REQ-CONV-ARCH-017: Technology-specific examples in this section, including FinBERT, LSTM, named indicator libraries, and named candlestick pattern packs, are reference candidates or approved baseline packs unless their release criticality and promotion gate explicitly make them required for a named release.

### 32.1 Overnight Pipeline Orchestration and Recovery

REQ-CONV-OVN-001: The platform MUST provide a first-class overnight run profile for long-only research and candidate-generation workflows.

The overnight run configuration MUST declare:

```text
run_profile_id
run_mode
trading_date
universe_id
enable_market_data
enable_technical_features
enable_graph_features
enable_macro_sector_features
enable_news_social
enable_sec_edgar
auto_build_sec_edgar
force_rebuild_raw_cache
force_rebuild_processed_cache
resume_from_checkpoint
maximum_pipeline_retries
retry_backoff_policy
per_stage_timeout
per_instrument_timeout
continue_on_instrument_failure
minimum_successful_instrument_ratio
output_root
cache_root
checkpoint_root
report_root
random_seed
runtime_manifest_id
```

REQ-CONV-OVN-002: The reference implementation SHOULD expose a configuration factory equivalent in behavior to `LongOvernightConfigFactory.build(...)` so that a complete, validated overnight configuration can be created without manually mutating many unrelated settings.

REQ-CONV-OVN-003: The orchestrator MUST support retry behavior equivalent to `PipelineOrchestrator.run_with_retries(config)`.

Retry policy MUST distinguish:

```text
retryable_network_error
retryable_provider_rate_limit
retryable_transient_storage_error
retryable_model_download_error
non_retryable_schema_error
non_retryable_PIT_violation
non_retryable_invalid_configuration
non_retryable_corrupt_artifact
```

REQ-CONV-OVN-004: Retry attempts MUST be idempotent. A repeated attempt MUST NOT duplicate source records, checkpoints, recommendations, ledger events, or model artifacts.

REQ-CONV-OVN-005: The pipeline MUST checkpoint at least the following boundaries:

```text
instrument_universe_resolved
raw_market_data_downloaded
raw_content_downloaded
SEC_filing_index_built
SEC_facts_processed
per_instrument_feature_dataset_completed
cross_sectional_dataset_assembled
training_dataset_completed
latest_feature_dataset_completed
model_training_completed
calibration_completed
report_generated
```

REQ-CONV-OVN-006: `resume_from_checkpoint = true` MUST reconstruct the run from the latest valid checkpoint after verifying:

```text
configuration_hash
code_commit_sha
schema_versions
input_snapshot_ids
artifact_checksums
universe_id
trading_date
```

REQ-CONV-OVN-007: A checkpoint from an incompatible configuration, schema, universe, date, or code version MUST be rejected or explicitly migrated; it MUST NOT be silently reused.

REQ-CONV-OVN-008: Per-instrument failures MUST be isolated. The run report MUST list successful, failed, skipped, and quarantined instruments and MUST preserve the original exception, stage, retry count, and last successful checkpoint.

REQ-CONV-OVN-009: The pipeline MUST define a minimum viable completion rule. A run that falls below `minimum_successful_instrument_ratio`, loses a critical benchmark instrument, or fails a critical dataset stage MUST be marked `FAILED` or `COMPLETED_WITH_WARNINGS` according to an approved policy and MUST NOT silently produce an execution-eligible artifact.

REQ-CONV-OVN-010: Cache behavior MUST be explicit for each artifact:

```text
cache_key
cache_scope
cache_version
source_snapshot_id
created_at
expires_at
checksum
row_count
schema_hash
cache_hit_or_miss
forced_rebuild_reason
```

REQ-CONV-OVN-011: `force_rebuild_processed_cache = true` MUST rebuild derived and processed artifacts while preserving immutable raw source snapshots unless `force_rebuild_raw_cache = true` is separately approved.

REQ-CONV-OVN-012: SEC EDGAR processing MUST support a staged command that can build only the PIT filing/fact Parquet layer before the full pipeline is run.

REQ-CONV-OVN-013: SEC requests MUST use an approved, non-placeholder user-agent identity and comply with SEC access guidance. Placeholder values such as `YourCompany contact@example.com` MUST be rejected outside local tests.

REQ-CONV-OVN-014: The overnight report MUST include:

```text
run_status
stage_durations
cache_hits_and_misses
provider_request_counts
rate_limit_events
retry_summary
instrument_success_ratio
row_counts_by_dataset
feature_counts_by_family
label_counts_by_horizon
missingness_summary
data_quality_failures
PIT_test_summary
model_and_calibration_summary
warnings
failed_instruments
artifact_paths
artifact_checksums
```

### 32.2 Market Data Adapter and DataFrame Normalization

REQ-CONV-DATA-001: Every market-data adapter, including a research adapter backed by `yfinance`, MUST normalize provider output into the canonical OHLCV schema before downstream processing.

Canonical normalized bar fields:

```text
instrument_id
ticker_display
bar_timestamp
trading_session_id
interval
open_raw
high_raw
low_raw
close_raw
close_split_adjusted
close_total_return_adjusted_if_available
volume
currency
exchange_timezone
provider
provider_symbol
source_record_id
```

REQ-CONV-DATA-002: Provider-specific column layouts, including MultiIndex columns and ticker-plus-field column pairs, MUST be flattened or selected through a deterministic adapter. Downstream indicator functions MUST receive one-dimensional numeric `Series`, never ambiguous two-dimensional frames.

REQ-CONV-DATA-003: The normalization layer MUST detect and provide actionable errors for:

```text
Data must be 1-dimensional
arg must be a list, tuple, 1-d array, or Series
missing required OHLCV field
non-numeric price column
duplicate timestamp
unsorted index
mixed timezone
MultiIndex header ambiguity
```

REQ-CONV-DATA-004: A canonical helper MUST exist to select a single series safely by logical field and optional instrument, equivalent to:

```text
get_price_series(frame, field="close", instrument_id=...)
```

The helper MUST validate dimensionality, numeric type, monotonic time ordering, and duplicate timestamps.

REQ-CONV-DATA-005: Header normalization utilities MUST support:

```text
retain_first_header_level
retain_second_header_level
join_header_levels
map_provider_headers_to_canonical_names
drop_empty_header_levels
```

REQ-CONV-DATA-006: Row deletion, header-row repair, and column renaming MUST be explicit transformations with before/after row counts, reason codes, and data-quality logging. Production pipelines MUST NOT rely on ad hoc `iloc` edits without a registered transformation.

REQ-CONV-DATA-007: Market-data downloads MUST declare inclusive/exclusive date semantics and interval support. Hourly (`1h`) and daily (`1d`) bars MUST be normalized to exchange time and tied to an exchange calendar.

REQ-CONV-DATA-008: The research `yfinance` adapter MAY be used for prototyping, but any production use MUST pass provider-quality, licensing, completeness, corporate-action, and availability-time review.

### 32.3 Technical Analysis and Candlestick Feature Library

REQ-CONV-TA-001: When the approved baseline Technical Expert capability is enabled, it MUST provide a versioned baseline feature pack covering trend, momentum, volatility, volume, market structure, relative strength, and candlestick-pattern families. The platform contract is the feature input/output schema, point-in-time behavior, tests, lineage, calibration impact, and marginal value, not permanent dependence on a specific indicator library or full indicator inventory.

Minimum trend features:

```text
simple_moving_average
exponential_moving_average
moving_average_slope
moving_average_distance
moving_average_cross_state
MACD
MACD_signal
MACD_histogram
ADX
plus_DI
minus_DI
Ichimoku_components_if_enabled
```

Minimum momentum features:

```text
RSI
stochastic_K
stochastic_D
Williams_R
rate_of_change
momentum
CCI
```

Minimum volatility features:

```text
ATR
normalized_ATR
Bollinger_mid
Bollinger_upper
Bollinger_lower
Bollinger_bandwidth
Bollinger_percent_B
realized_volatility
range_volatility
gap_size
```

Minimum volume and flow features:

```text
volume_change
volume_zscore
relative_volume
OBV
money_flow_index
accumulation_distribution
chaikin_money_flow
VWAP_if_intraday_available
price_volume_trend
```

Minimum market-structure features:

```text
rolling_support
rolling_resistance
breakout_distance
breakdown_distance
higher_high_lower_low_state
trend_persistence
drawdown_from_recent_high
distance_from_52_week_high
liquidity_and_spread_proxies
```

REQ-CONV-TA-002: When the candlestick feature pack is enabled, the approved baseline candlestick-pattern pack MUST include, at minimum:

```text
hammer
inverted_hammer
hanging_man
shooting_star
doji
dragonfly_doji
gravestone_doji
bullish_engulfing
bearish_engulfing
piercing_line
dark_cloud_cover
morning_star
evening_star
three_white_soldiers
three_black_crows
harami
inside_bar
outside_bar
marubozu
```

REQ-CONV-TA-003: Each enabled candlestick pattern MUST define its formula, tolerance parameters, required trend context, direction, confidence, horizon relevance, and invalidation conditions. Pattern presence alone MUST NOT be treated as a guaranteed reversal signal.

REQ-CONV-TA-004: Pattern and indicator calculations MUST be vectorized where practical, deterministic, point-in-time safe, and tested against known examples.

REQ-CONV-TA-005: Technical features MUST define warm-up periods. Rows without sufficient history MUST be marked unavailable rather than filled with future-aware or silent default values.

REQ-CONV-TA-006: The feature registry MUST record the implementation provider for each indicator:

```text
native_project_implementation
pandas_ta
TA_Lib
technical_analysis_library
other_approved_provider
```

Equivalent indicators from different libraries MUST NOT be mixed without a versioned equivalence test.

REQ-CONV-TA-007: A candlestick-chart utility MUST display canonical OHLCV data and MAY overlay indicators, support/resistance, identified patterns, entries, stops, targets, fills, and recommendation timestamps.

REQ-CONV-TA-008: Charts MUST use raw tradable prices for execution annotations and explicitly label any adjusted-price analytical overlays.

REQ-CONV-TA-009: Technical-feature promotion MUST be based on incremental out-of-sample value, stability, and cost-adjusted portfolio impact, not on indicator popularity or in-sample correlation.

### 32.4 Hybrid Tabular and Sequence Modeling

REQ-CONV-MOD-001: The Research Factory MAY evaluate a hybrid model that combines a tabular/cross-sectional feature model with a temporal sequence encoder such as LSTM, GRU, TCN, or Transformer/TFT.

REQ-CONV-MOD-002: A sequence-model research challenger, including any LSTM candidate, MUST consume only historical sequences ending at or before the feature cutoff and MUST declare:

```text
sequence_length_sessions
sequence_feature_set
feature_cutoff_policy
padding_policy
minimum_history
normalization_fit_window
target_definitions
output_horizons
output_schema
calibration_method
training_seed
model_family
model_version
architecture_parameters
promotion_comparison_set
```

REQ-CONV-MOD-003: Bidirectional sequence models are forbidden for causal production forecasting unless the implementation proves that no future observations enter the representation.

REQ-CONV-MOD-004: Hybrid fusion MUST be explicit. Allowed initial fusion patterns:

```text
late_fusion_weighted_average
stacked_meta_model
concatenated_embedding_plus_tabular_head
mixture_of_experts
```

REQ-CONV-MOD-005: The hybrid model MUST be compared against:

```text
naive_baseline
technical_rules_baseline
approved_tabular_baseline
sequence_only_model
tabular_only_model
hybrid_model
```

under identical data, target, universe, cost, portfolio, and walk-forward rules.

REQ-CONV-MOD-006: Model reports MUST include ablation results for candlestick features, technical indicators, graph features, macro-sector features, fundamentals, news sentiment, and social features.

REQ-CONV-MOD-007: Deep or sequence models remain replaceable Release 4 research challengers unless they pass the promotion gates in this document. Their existence in research code MUST NOT make them mandatory in Decision Runtime.

REQ-CONV-MOD-008: Multi-horizon outputs MUST cover 5, 8, and 14 exchange sessions and MAY jointly model direction, expected return, tail quantiles, and hurdle probabilities, but all outputs MUST be calibrated and stored in the canonical forecast entities.

### 32.5 Cross-Sectional Graph and Macro-Sector Features

REQ-CONV-GRAPH-001: The initial numerical market graph feature set MUST include the following conversation-derived fields when enabled:

```text
graph_degree
graph_avg_abs_corr
graph_peer_return_1d
graph_peer_return_5d
graph_peer_return_20d
graph_lead_lag_peer_return_1d
graph_relative_strength_20d
sector_peer_return_5d
sector_peer_return_20d
sector_relative_strength_20d
```

REQ-CONV-GRAPH-002: Every graph feature MUST declare:

```text
graph_snapshot_id
computed_as_of
lookback_sessions
minimum_pairwise_observations
correlation_method
edge_threshold
edge_weight_formula
peer_universe
sector_taxonomy_version
lead_lag_method
regime_conditioning_if_any
```

REQ-CONV-GRAPH-003: Graph construction MUST use only observations available by the decision cutoff. Full-sample correlation matrices, future constituent membership, or hindsight sector classifications are prohibited.

REQ-CONV-GRAPH-004: Graph features MUST define behavior for isolated nodes, missing peers, newly listed instruments, and unstable correlation estimates.

REQ-CONV-GRAPH-005: The macro-sector feature family MUST include, when available and approved:

```text
broad_market_return_1d
broad_market_return_5d
broad_market_return_20d
broad_market_trend
broad_market_volatility
market_breadth
sector_return_1d
sector_return_5d
sector_return_20d
sector_relative_strength
rates_proxy_return
long_duration_bond_proxy_return
credit_proxy_return
volatility_index_level_or_proxy
commodity_or_gold_proxy_return
US_dollar_proxy_return
cross_asset_stress
```

REQ-CONV-GRAPH-006: Reference instruments such as SPY, sector ETFs, TLT, GLD, volatility proxies, rates proxies, and credit proxies MUST be mapped through the instrument master or an approved benchmark master and MUST have PIT availability rules.

REQ-CONV-GRAPH-007: The exact produced lists `graph_feature_cols` and `macro_sector_feature_cols` MUST be saved with each feature snapshot, training artifact, and report.

### 32.6 News, Social Content, FinBERT, and Source Profiles

REQ-CONV-CONT-001: The content pipeline MUST use separate canonical datasets equivalent to the following project tables:

```text
news_df
content_items_df
content_enrichments_df
content_market_link_df
source_profiles_df
daily_features_df
training_df
```

The Python variable names MAY change, but the logical contracts MUST remain separate and traceable.

REQ-CONV-CONT-002: `content_items` MUST store normalized content identity and metadata.

Required fields:

```text
content_id
platform
content_type
canonical_url
resolved_url_if_available
provider_url
external_post_id
headline_or_title
body_or_excerpt_if_licensed
language
published_at
publicly_available_at
system_available_at
author_id
author_name
editor_name_if_available
publisher_id
publisher_name
source_id
is_repost_or_copy
root_content_id
mentioned_instrument_ids
mentioned_tickers_raw
created_at
```

REQ-CONV-CONT-003: `content_enrichments` MUST store model-derived attributes separately from raw content.

Required fields:

```text
content_enrichment_id
content_id
sentiment_model
sentiment_model_version
sentiment_label
sentiment_score
positive_probability
neutral_probability
negative_probability
relevance_score
novelty_score
urgency_score
event_type
entities
instrument_relevance
summary_if_enabled
processed_at
feature_available_at
```

REQ-CONV-CONT-004: FinBERT SHOULD be treated as the reference baseline candidate for English financial text sentiment. It MUST NOT become a hard runtime dependency unless promoted through the same calibration, PIT, licensing, robustness, and marginal-value gates as any challenger.

REQ-CONV-CONT-005: TextBlob MAY be retained only as a transparent baseline, smoke test, or fallback research comparator. TextBlob polarity MUST NOT be mixed with FinBERT probabilities as though both shared the same scale or calibration.

REQ-CONV-CONT-006: FinBERT model-loading warnings about non-task state entries, such as an unexpected `bert.embeddings.position_ids`, MAY be treated as benign only when the model architecture, classifier head, output labels, and regression tests confirm correct behavior. The warning MUST be logged and classified, not blindly suppressed.

REQ-CONV-CONT-007: Sentiment analysis MUST support batching, deterministic inference settings, device fallback, maximum token handling, empty-text handling, language gating, and model-download caching.

REQ-CONV-CONT-008: The content pipeline SHOULD ingest multiple modalities when licensed and available:

```text
financial_news
SEC_filings
company_press_releases
analyst_or_research_headlines
social_posts
market_price_and_volume_context
```

REQ-CONV-CONT-009: Social content MUST be treated as lower-trust, manipulation-prone evidence and MUST pass source, duplication, anomaly, entity-resolution, and ticker-disambiguation controls before affecting a recommendation.

REQ-CONV-CONT-010: `source_profiles` MUST include point-in-time reliability and operational metadata.

Required fields:

```text
source_id
source_family
publisher_name
platform
author_id_if_applicable
content_count_as_of
original_content_rate
copy_rate
independent_confirmation_rate
historical_reliability
reliability_confidence_interval
average_relevance
average_novelty
average_latency
cold_start_status
last_updated_at
```

REQ-CONV-CONT-011: The pipeline MUST provide an operator inspection function that displays one complete content example, including:

```text
raw post or article text
headline
author
editor if available
publisher
source/platform
publication time
mentioned instruments
FinBERT label and probabilities
relevance and novelty
event classification
content-market linkage summary
source-profile summary
```

REQ-CONV-CONT-012: Content-body storage MUST obey licensing rules. When full-body storage is not permitted, the system MUST store only allowed excerpts, hashes, embeddings if permitted, metadata, and source references.

### 32.7 URL Resolution and Content-to-Market Linkage

REQ-CONV-LINK-001: URL resolution MUST be optional and isolated from core content ingestion. Failure of `resolve_article_url` or an equivalent redirect resolver MUST NOT discard otherwise valid content.

REQ-CONV-LINK-002: The URL policy MUST support:

```text
NO_RESOLUTION
SAFE_HEAD_RESOLUTION
SAFE_GET_RESOLUTION
PROVIDER_CANONICAL_URL_ONLY
```

REQ-CONV-LINK-003: URL resolution MUST enforce timeout, redirect-count, domain allow/deny policy, private-network blocking, content-size limits, and SSRF protections.

REQ-CONV-LINK-004: `build_content_market_link` or its equivalent MUST link each content item to one or more market observation windows without temporal leakage.

Required linkage fields:

```text
content_market_link_id
content_id
instrument_id
event_timestamp
market_timezone
previous_regular_session
next_regular_session
first_eligible_bar_timestamp
link_interval
pre_event_return
post_event_return_1h_if_available
post_event_return_1d
post_event_return_5d
post_event_volume_response
post_event_volatility_response
benchmark_adjusted_response
link_quality
linkage_version
```

REQ-CONV-LINK-005: Hourly market linkage MUST normalize timezone-aware timestamps, handle pre-market and after-hours content, and explicitly define whether the first eligible bar is extended-hours or regular-session.

REQ-CONV-LINK-006: Content published after market close MUST NOT be linked to that session's close as though the information were known before the close.

REQ-CONV-LINK-007: Linkage functions MUST support empty content, empty market data, missing bars, duplicate timestamps, non-trading days, early closes, and ticker changes without uncaught type errors.

REQ-CONV-LINK-008: Market responses used as labels for source reliability or sentiment research MUST mature before they update source profiles.

### 32.8 Daily Aggregation, Training Dataset, and Latest Features

REQ-CONV-DS-001: `daily_features` MUST aggregate content and market context by instrument and decision session using only information available by the cutoff.

Minimum content-derived daily features:

```text
content_count
unique_source_count
independent_root_event_count
positive_content_count
negative_content_count
neutral_content_count
reference_sentiment_mean
reference_sentiment_weighted
sentiment_dispersion
maximum_relevance
mean_relevance
mean_novelty
source_reliability_weighted_sentiment
original_content_ratio
copy_ratio
social_volume_zscore
news_volume_zscore
bullish_bearish_imbalance
time_since_latest_content
```

REQ-CONV-DS-002: Aggregation MUST prevent multiple copies of the same root story from amplifying sentiment or source counts.

REQ-CONV-DS-003: The canonical research output MUST distinguish:

```text
training_df
latest_features_df
feature_cols
graph_feature_cols
macro_sector_feature_cols
target_cols
metadata_cols
```

REQ-CONV-DS-004: `training_df` and `latest_features_df` MUST share the same feature schema and ordering, excluding target columns and stage-specific metadata.

REQ-CONV-DS-005: The dataset builder MUST assert:

```text
no_duplicate_instrument_session_rows
no_target_columns_in_feature_cols
no_future_timestamps_in_features
same_feature_schema_for_train_and_latest
finite_values_or_registered_missingness
minimum_history_satisfied
categorical_encodings_versioned
row_count_and_feature_count_logged
```

REQ-CONV-DS-006: Every successful per-instrument dataset build SHOULD write a checkpoint with instrument ID, row count, date range, schema hash, and artifact checksum. Messages such as `Dataset OK ... checkpoint saved` MUST correspond to a verifiable artifact, not only console output.

REQ-CONV-DS-007: A cache hit MUST be validated by schema hash, source snapshot, date coverage, and checksum before reuse. Row count alone is insufficient.

REQ-CONV-DS-008: Dataset reports MUST show feature-family counts and missingness for technical, graph, macro-sector, fundamental, news, social, and metadata features.

### 32.9 Operator, Debugging, and Visualization Utilities

REQ-CONV-TOOL-001: The project MUST include reusable inspection utilities for:

```text
print_dataframe_schema
print_column_levels
show_sample_rows
show_one_content_record
show_feature_lineage
show_missingness_summary
show_duplicate_summary
show_timestamp_range
show_one_prediction_with_drivers
plot_candlestick_chart
plot_indicator_overlays
plot_sentiment_timeline
plot_content_and_price_response
```

REQ-CONV-TOOL-002: Inspection utilities MUST be read-only by default and MUST NOT mutate production datasets.

REQ-CONV-TOOL-003: Any utility that repairs a table MUST return a new object or require an explicit `inplace` flag, log the transformation, and preserve a before/after sample.

REQ-CONV-TOOL-004: Diagnostic output SHOULD include concise remedies for common errors, including ambiguous MultiIndex columns, one-dimensional-series requirements, missing field mappings, timezone mismatch, and insufficient lookback.

REQ-CONV-TOOL-005: Operator utilities MUST redact secrets, broker identifiers, restricted article bodies, and unlicensed personal data.

### 32.10 Conversation-Derived Test Additions

REQ-CONV-TEST-001: The test suite MUST add unit and integration tests for:

```text
MultiIndex_yfinance_output_to_canonical_OHLCV
single_series_selection_for_RSI
invalid_two_dimensional_indicator_input
header_level_retention_and_joining
row_repair_and_column_rename_logging
all_required_technical_indicators
all_required_candlestick_patterns
candlestick_chart_generation
LSTM_sequence_cutoff_no_future_data
hybrid_model_ablation
PIT_graph_construction
macro_benchmark_availability
FinBERT_inference_and_label_mapping
FinBERT_warning_classification
TextBlob_baseline_scale_separation
content_item_to_enrichment_lineage
source_profile_maturity
optional_URL_resolution_failure
content_market_link_hourly_timezone
pre_market_and_after_hours_linkage
copy_cluster_sentiment_deduplication
training_latest_feature_schema_equality
checkpoint_resume_after_failure
cache_invalidation_on_schema_change
SEC_processed_cache_rebuild
retry_idempotency
```

REQ-CONV-TEST-002: A golden content example MUST include author, editor when available, publisher, duplicate cluster, FinBERT output, and market linkage so the complete inspection utility can be regression-tested.

REQ-CONV-TEST-003: A golden market-data example MUST include a provider MultiIndex response, a single-ticker flat response, missing volume, duplicate timestamps, a split, and an after-hours event.

REQ-CONV-TEST-004: An overnight recovery test MUST interrupt the pipeline after at least three different checkpoint stages and prove that resume produces the same final artifact hashes as an uninterrupted deterministic run.

REQ-CONV-TEST-005: An overnight partial-failure test MUST prove that failed instruments are quarantined, successful instruments remain usable for research, the completion status follows policy, and no execution-eligible artifact is promoted when critical thresholds fail.

### 32.11 Conversation Coverage Traceability Matrix

REQ-CONV-TRACE-001: The implementation traceability package MUST include the following minimum mappings.

| Conversation-derived topic | Canonical requirements |
| --- | --- |
| Long overnight execution profile | `REQ-CONV-OVN-001` through `REQ-CONV-OVN-014` |
| `PipelineOrchestrator.run_with_retries` behavior | `REQ-CONV-OVN-003` through `REQ-CONV-OVN-009` |
| SEC EDGAR auto-build and processed-cache rebuild | `REQ-CONV-OVN-011` through `REQ-CONV-OVN-013` |
| Cache hits, per-instrument dataset completion, checkpoints | `REQ-CONV-OVN-005` through `REQ-CONV-OVN-010`, `REQ-CONV-DS-006`, `REQ-CONV-DS-007` |
| DataFrame dimensionality and MultiIndex problems | `REQ-CONV-DATA-002` through `REQ-CONV-DATA-006` |
| Full technical analysis and candlestick patterns | `REQ-CONV-TA-001` through `REQ-CONV-TA-009` |
| Candlestick visualization | `REQ-CONV-TA-007`, `REQ-CONV-TA-008`, `REQ-CONV-TOOL-001` |
| LSTM plus technical-analysis hybrid | `REQ-CONV-MOD-001` through `REQ-CONV-MOD-008` |
| Graph peer, correlation, lead-lag, and relative-strength features | `REQ-CONV-GRAPH-001` through `REQ-CONV-GRAPH-004` |
| Macro and sector context features | `REQ-CONV-GRAPH-005` through `REQ-CONV-GRAPH-007` |
| News/social multimodal ingestion | `REQ-CONV-CONT-001` through `REQ-CONV-CONT-012` |
| FinBERT sentiment and TextBlob baseline | `REQ-CONV-CONT-004` through `REQ-CONV-CONT-007` |
| Post/article sample with sentiment, author, editor, and publisher | `REQ-CONV-CONT-002`, `REQ-CONV-CONT-003`, `REQ-CONV-CONT-011` |
| Optional removal of URL resolution | `REQ-CONV-LINK-001` through `REQ-CONV-LINK-003` |
| Hourly `yfinance` market linkage | `REQ-CONV-DATA-007`, `REQ-CONV-DATA-008`, `REQ-CONV-LINK-004` through `REQ-CONV-LINK-008` |
| `content_items`, enrichments, source profiles, daily features, training dataset | `REQ-CONV-CONT-001` through `REQ-CONV-CONT-003`, `REQ-CONV-CONT-010`, `REQ-CONV-DS-001` through `REQ-CONV-DS-008` |
| `training_df`, `latest_features_df`, feature lists | `REQ-CONV-DS-003` through `REQ-CONV-DS-008` |
| Reusable debugging and inspection code | `REQ-CONV-TOOL-001` through `REQ-CONV-TOOL-005` |

REQ-CONV-TRACE-002: A conversation-derived topic MUST NOT be marked `IMPLEMENTED` in the traceability matrix until it has:

```text
requirement_id
design_component
kernel_or_capability_classification
bounded_context
capability_id
release_criticality
code_location
test_id
artifact_or_schema_version
latest_test_result
owner
promotion_environment
runtime_manifest_flag
capability_health_flag
```

REQ-CONV-TRACE-003: The report MUST distinguish documentation coverage from code completion using these statuses:

```text
DOCUMENTED
DESIGNED
PARTIALLY_IMPLEMENTED
IMPLEMENTED_UNTESTED
TESTED_RESEARCH
PROMOTED_SHADOW
PROMOTED_PAPER
PROMOTED_LIVE
BLOCKED
```

## 33. Final Implementation-Ready Definition

The system may be called implementation-ready only when each core component has:

```text
unambiguous semantics
canonical schema
data contract
time availability rule
calculation formula
edge-case policy
failure behavior
test coverage
acceptance threshold
owner
version
audit trail
traceability ID
```

The system may not be called implementation-ready if:

```text
the Decision Kernel is not explicitly separated from replaceable capabilities
counterfactual results can be mistaken for observed outcomes
unsupported counterfactuals are presented as evidence
market state is represented as one unquestioned truth
optional plugins are required before they prove marginal value
DECISION_RUNTIME can load research-only artifacts
runtime manifests are missing or unenforced
```

The system's advantage must come from disciplined alignment:

```text
World Hypotheses -> Opportunity -> Evidence Dependency -> Forecast -> Candidate -> Pre-open Revalidation
-> Portfolio Decision -> Execution -> Outcome -> Counterfactual Learning -> Governance
```

not from adding more models before the decision, data, validation, execution, learning, and governance contracts are sound.
