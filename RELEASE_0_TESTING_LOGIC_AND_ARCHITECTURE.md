# Release 0 Testing Logic and Architecture

This document defines the conceptual implementation logic for closing Release 0 through tests. It sits on top of the canonical specification and the coverage matrix. It does not add product scope; it explains how implementation evidence should be produced.

Canonical inputs:

```text
AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md
REQUIREMENT_TO_CODE_COVERAGE_MATRIX.md
RELEASE_0_1A_IMPLEMENTATION_BACKLOG.md
```

## Architectural Intent

Release 0 is not a trading system yet. It is the proof layer that the system can trust its data, labels, validation, replay, and baseline reports.

The central question of Release 0 is:

```text
Can the platform generate reproducible, point-in-time-safe research evidence without leakage, schema drift, or hidden provider assumptions?
```

If the answer is not proven by tests, the component remains `PARTIALLY_IMPLEMENTED`, even if prototype code exists.

## Core Principle

The Release 0 architecture MUST be test-first and evidence-first:

```text
provider data
  -> canonical normalization
  -> point-in-time labels
  -> sealed feature snapshots
  -> training/latest schema parity
  -> deterministic checkpoints
  -> purged walk-forward validation
  -> baseline report
  -> coverage matrix update
```

No baseline model result is meaningful until all earlier layers pass.

## Conceptual Component Map

| Layer | Conceptual responsibility | Output artifact | Primary failure mode | Coverage rows closed |
| --- | --- | --- | --- | --- |
| Provider Boundary | Accept raw provider data and isolate provider-specific quirks | Raw source snapshot | Provider schema leaks downstream | `REQ-CONV-DATA-001`, `REQ-CONV-DATA-002` |
| Canonical OHLCV Adapter | Convert raw bars into one canonical OHLCV schema | Canonical bar frame | MultiIndex, duplicate timestamp, missing field, non-numeric series | `REQ-CONV-DATA-001` through `REQ-CONV-DATA-006` |
| Temporal Truth Layer | Attach event, provider, availability, and system timestamps | PIT source record | Future-aware availability or ambiguous date semantics | `REQ-DATA-001` through `REQ-DATA-004` |
| Labeling Layer | Generate 5/8/14-session labels only when matured | Label frame | Future labels available too early | `REQ-LBL-001` through `REQ-LBL-013` |
| Feature Snapshot Layer | Seal feature schemas and feature values by cutoff | `feature_snapshot` | Training/runtime schema drift | `REQ-SCH-037`, `REQ-CONV-DS-003` through `REQ-CONV-DS-008` |
| Checkpoint and Manifest Layer | Persist deterministic stage artifacts and validate resume context | Checkpoint manifest | Reusing incompatible artifact | `REQ-CONV-OVN-003` through `REQ-CONV-OVN-010` |
| Validation Splitter | Create purged walk-forward folds with embargo | Fold manifest | Overlapping label windows or leakage | `REQ-VAL-001` through `REQ-VAL-008` |
| Baseline Evidence Layer | Train/report approved baseline only after truth layers pass | Baseline report | Optimizing on invalid data | `REQ-MOD-001` through `REQ-MOD-010` |
| Coverage Control Loop | Update coverage matrix from actual evidence | Coverage row state | Documentation marked as implementation | `REQ-CONV-TRACE-001` through `REQ-CONV-TRACE-003` |

## Data Flow Logic

The Release 0 pipeline should be understood as a chain of contracts, not a chain of scripts.

```text
Raw provider payload
  -> source_record
  -> canonical_ohlcv_bar
  -> pit_label_set
  -> feature_snapshot
  -> training_df
  -> latest_features_df
  -> schema_parity_result
  -> checkpoint_manifest
  -> walk_forward_fold_manifest
  -> baseline_model_report
  -> coverage_matrix_row_update
```

Each arrow is a testable boundary. A downstream layer MUST NOT compensate for an upstream layer that failed.

## Release 0 Invariants

| Invariant | Meaning | Gate behavior |
| --- | --- | --- |
| Provider isolation | Downstream code never consumes raw provider column layouts directly. | Fail OHLCV adapter tests. |
| Canonical bars only | All OHLCV bars use one canonical schema. | Block labels and features. |
| No ambiguous MultiIndex | Provider MultiIndex columns must be selected/flattened deterministically. | Fail normalization tests. |
| PIT availability | Every label and feature knows when it became available. | Block validation and baseline. |
| Matured labels only | 5/8/14-session labels are unavailable until the horizon is complete. | Fail label tests. |
| No target leakage | `latest_features_df` cannot contain `future_*`, `target_*`, `label_*`, `actual_*`, or `pred_*` columns. | Fail schema parity. |
| Schema parity | `training_df` and `latest_features_df` share the same approved feature list and types. | Block runtime-style prediction. |
| Deterministic resume | A resumed run must validate config, code, schema, universe, date, and checksums. | Fail checkpoint/resume. |
| Purged folds | Train labels cannot overlap test windows. | Fail walk-forward validation. |
| Baseline last | Baseline model work starts only after the data truth chain passes. | Mark model work blocked, not failed. |

## Test Families

| Test family | Purpose | Example evidence |
| --- | --- | --- |
| Contract tests | Prove module input/output schemas and failure modes. | Canonical OHLCV adapter rejects missing volume and duplicate timestamps. |
| Golden fixture tests | Prove known edge cases stay stable. | Split, missing bar, after-hours event, MultiIndex provider frame. |
| PIT tests | Prove no information appears before `feature_available_at` or label maturity. | 14-session label is null for last 14 rows. |
| Schema tests | Prove research and runtime feature frames are compatible. | Same feature columns and numeric dtypes. |
| Replay tests | Prove same inputs produce same artifact hashes. | Uninterrupted run and resumed run match. |
| Validation tests | Prove train/test folds obey purge and embargo rules. | Max train label horizon ends before min test date. |
| Report tests | Prove metrics are generated from approved folds and baselines. | Baseline report references fold manifests and data hashes. |

## Closure Logic

A matrix row moves through these states:

```text
DOCUMENTED
  -> DESIGNED
  -> PARTIALLY_IMPLEMENTED
  -> IMPLEMENTED_UNTESTED
  -> TESTED_RESEARCH
```

Allowed transitions:

| From | To | Required evidence |
| --- | --- | --- |
| `DOCUMENTED` | `DESIGNED` | Architecture owner and target component are named. |
| `DESIGNED` | `PARTIALLY_IMPLEMENTED` | Code or artifact exists, but canonical tests are missing. |
| `PARTIALLY_IMPLEMENTED` | `IMPLEMENTED_UNTESTED` | Canonical module exists and can be called deterministically. |
| `IMPLEMENTED_UNTESTED` | `TESTED_RESEARCH` | Test ID exists, latest result is recorded, and failure modes are covered. |
| Any status | `BLOCKED` | Missing threshold, owner, schema decision, or external dependency blocks progress. |

Forbidden transition:

```text
PARTIALLY_IMPLEMENTED -> TESTED_RESEARCH
```

unless a real test ID and latest result are added to the matrix.

## Priority Architecture

### 1. Canonical OHLCV Adapter

Purpose: create one trusted market-data boundary.

Logical contract:

```text
input: raw provider frame, provider metadata, ticker/instrument identity
output: canonical OHLCV bars
failure: explicit normalization error with actionable reason
```

The adapter owns:

```text
MultiIndex resolution
column normalization
required OHLCV field validation
numeric dtype validation
timestamp normalization
duplicate timestamp rejection
provider symbol mapping
source_record lineage
```

Downstream features, labels, and model code MUST consume only canonical OHLCV bars.

### 2. PIT Labels for 5/8/14 Sessions

Purpose: prove labels are correct and mature only after the relevant horizon.

Logical contract:

```text
input: canonical OHLCV bars
output: horizon label frame for 5, 8, and 14 exchange sessions
failure: missing price basis, unsorted sessions, or insufficient horizon metadata
```

Required logic:

```text
label_return_h = future_price_at_horizon / current_price - 1
label_available_at = timestamp of horizon completion
label_status = MATURED | NOT_MATURED
```

Rows near the end of the dataset MUST remain `NOT_MATURED`.

### 3. Training/Latest Schema Parity

Purpose: prevent research-to-runtime drift.

Logical contract:

```text
input: training_df, latest_features_df, approved feature list
output: schema parity result
failure: missing columns, forbidden target columns, dtype mismatch, schema hash mismatch
```

The approved feature list is the authority. Neither `training_df` nor `latest_features_df` may invent its own runtime schema.

### 4. Checkpoint/Resume Determinism

Purpose: prove replay and recovery are real, not just operational logging.

Logical contract:

```text
input: ordered pipeline stages, run context, artifact hashes
output: checkpoint manifest and latest valid resume point
failure: context mismatch, checksum mismatch, incompatible schema, duplicate artifact
```

Checkpoint context MUST include:

```text
configuration_hash
code_commit_sha
schema_versions
input_snapshot_ids
universe_id
trading_date
artifact_checksums
```

### 5. Purged Walk-Forward and Embargo

Purpose: prove validation does not leak through overlapping label windows.

Logical contract:

```text
input: dated dataset, label horizon, train/test window policy, embargo policy
output: fold manifest
failure: overlapping label windows, empty folds, missing date grouping
```

The splitter must operate on date groups, not random rows.

### 6. Baseline Model and Report

Purpose: establish a first honest benchmark after the data truth chain is proven.

Logical contract:

```text
input: approved feature snapshots and fold manifests
output: baseline model report
failure: invalid upstream gate, no-edge result, insufficient samples
```

A weak baseline is not a failure if the test evidence is correct. It should be recorded as:

```text
BLOCKED_NO_EDGE
```

or equivalent, not hidden by changing thresholds after the fact.

## Release 0 Gate Sequence

| Gate | Must pass before | Blocks |
| --- | --- | --- |
| OHLCV adapter gate | Label generation | All downstream labels/features |
| PIT label gate | Walk-forward validation | Baseline model and metrics |
| Schema parity gate | Runtime-like scoring | Latest prediction/report generation |
| Checkpoint gate | Replay acceptance | Implementation-ready claims |
| Purged validation gate | Baseline training | Performance claims |
| Baseline report gate | Release 0 acceptance | Release 1A Decision Kernel work |

## What Must Not Be Prioritized Yet

The following remain out of the Release 0 test-critical path:

```text
FinBERT
LSTM
knowledge graph
graph neural networks
counterfactual portfolios
LLM explanations
broker execution
paper trading
live readiness
```

They may remain documented or researched, but they MUST NOT consume Release 0 closure effort before the truth chain passes.

## Matrix Update Rule

Every completed test slice must update the coverage matrix with:

```text
requirement_id
code_location
test_id
latest_test_result
owner
status
notes
```

The coverage matrix is the operational source of truth for what is actually implemented and proven.

