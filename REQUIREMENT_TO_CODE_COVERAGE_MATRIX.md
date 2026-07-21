# Requirement-to-Code Coverage Matrix

This matrix separates documentation coverage from implementation evidence. It is based on the current repository contents and should be updated whenever code, tests, or generated artifacts change.

Important finding: no formal `tests/` directory or canonical test files were found in the repository during this pass. Therefore, the rows below do not claim `TESTED_RESEARCH` unless a future test run is added and recorded.

## Current Execution Directive

The planning/specification phase is sufficient for Release 0 test execution. The next phase MUST focus on building the formal Release 0 test layer and closing this matrix row by row. New product requirements, advanced model work, and additional optional capabilities SHOULD NOT be added until the Release 0 blockers below have executable tests and recorded results.

The bottleneck has moved from architecture design to implementation evidence. A component remains `PARTIALLY_IMPLEMENTED` until the matrix names its code location, test ID, latest test result, and owner.

Conceptual execution architecture: `RELEASE_0_TESTING_LOGIC_AND_ARCHITECTURE.md`.

## Release 0 Test Closure Order

The next implementation phase should not add more product requirements. It should create formal tests and close this matrix row by row.

| Priority | Test package to create | Requirements closed first | Target code area | Target test ID pattern | Required status after passing |
| --- | --- | --- | --- | --- | --- |
| 1 | Canonical OHLCV adapter and MultiIndex normalization | `REQ-CONV-DATA-001` through `REQ-CONV-DATA-006` | Single importable market-data normalization module | `tests/release0/test_ohlcv_adapter.py::*` | `TESTED_RESEARCH` |
| 2 | PIT label generation for 5/8/14 sessions | `REQ-LBL-001` through `REQ-LBL-013`, `REQ-CONV-DS-004` | Labeling module with exchange-session horizons | `tests/release0/test_labels.py::*` | `TESTED_RESEARCH` |
| 3 | `training_df` / `latest_features_df` schema parity | `REQ-CONV-DS-003` through `REQ-CONV-DS-008`, `REQ-SCH-037`, `REQ-SCH-038` | Feature snapshot and feature-column registry | `tests/release0/test_schema_parity.py::*` | `TESTED_RESEARCH` |
| 4 | Checkpoint/resume deterministic replay | `REQ-CONV-OVN-003` through `REQ-CONV-OVN-010` | Overnight checkpoint store and run manifest | `tests/release0/test_checkpoints.py::*` | `TESTED_RESEARCH` |
| 5 | Purged walk-forward and embargo | `REQ-VAL-001` through `REQ-VAL-008` | Validation splitter | `tests/release0/test_purged_walk_forward.py::*` | `TESTED_RESEARCH` |
| 6 | Baseline model and performance report | `REQ-MOD-001` through `REQ-MOD-010`, `REQ-VAL-009` through `REQ-VAL-014` | Baseline forecaster and report generator | `tests/release0/test_baseline_model.py::*` | `TESTED_RESEARCH` or `BLOCKED_NO_EDGE` |

Acceptance rule: a row in this matrix may move from `PARTIALLY_IMPLEMENTED` to `TESTED_RESEARCH` only after the named test exists, runs in CI or an equivalent reproducible local command, and records the latest result.

## Status Values

| Status | Meaning |
| --- | --- |
| `DOCUMENTED` | Requirement exists in the specification, but no code evidence was found. |
| `DESIGNED` | Schema or architecture is defined, but implementation is not complete. |
| `PARTIALLY_IMPLEMENTED` | Research/prototype code or artifacts exist, but canonical integration or tests are missing. |
| `IMPLEMENTED_UNTESTED` | Code exists for the behavior, but no formal test evidence was found. |
| `TESTED_RESEARCH` | Research code has a recorded passing test result. |
| `BLOCKED` | Cannot advance until threshold, schema, owner, or external dependency is resolved. |

## Matrix

| Requirement ID | Design component | Classification | Bounded context | Release criticality | Code location | Test ID | Latest test result | Owner | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `REQ-CONV-OVN-001` | Long overnight run profile | `CONTROL_PLANE_COMPONENT` | Control Plane / Temporal Data | `REQUIRED_FOR_RELEASE` for R0 replay | `Technical Analysis.py:6990`, `Technical Analysis.py:8006` | TBD | `NO_TEST_FOUND` | Platform | `PARTIALLY_IMPLEMENTED` | `LongOvernightConfigFactory` exists, but canonical manifest/checkpoint contract needs tests. |
| `REQ-CONV-OVN-003` | Retry orchestration | `CONTROL_PLANE_COMPONENT` | Control Plane | `REQUIRED_FOR_RELEASE` | `Technical Analysis.py:5080` | TBD | `NO_TEST_FOUND` | Platform | `PARTIALLY_IMPLEMENTED` | `PipelineOrchestrator.run_with_retries` exists; idempotency and duplicate-artifact tests missing. |
| `REQ-CONV-OVN-005` | Checkpoint boundaries | `CONTROL_PLANE_COMPONENT` | Control Plane / Temporal Data | `RELEASE_BLOCKER` for deterministic replay | `Technical Analysis.py:3876`, `Technical Analysis.py:4306`, `outputs/technical_graph_system_v4/overnight_checkpoints/` | TBD | `NO_TEST_FOUND` | Platform | `PARTIALLY_IMPLEMENTED` | Some model/lab checkpoints exist; canonical stage list not fully enforced. |
| `REQ-CONV-DATA-001` | OHLCV normalization | `TEMPORAL_DATA_COMPONENT` | Temporal Data | `RELEASE_BLOCKER` | `stock_ai_4_files/1_data_update.py:89`, `Technical Analysis.py:1236`, `news_analysis.py:954` | TBD | `NO_TEST_FOUND` | Data | `PARTIALLY_IMPLEMENTED` | yfinance normalization exists in multiple places; needs one canonical adapter. |
| `REQ-CONV-DATA-002` | MultiIndex flattening | `TEMPORAL_DATA_COMPONENT` | Temporal Data | `REQUIRED_FOR_RELEASE` | `news_analysis.py:954`, `stock_ai_4_files/1_data_update.py:94`, `coor.py:22` | TBD | `NO_TEST_FOUND` | Data | `IMPLEMENTED_UNTESTED` | Behavior exists, but needs contract tests for one-dimensional downstream series. |
| `REQ-CONV-TA-001` | Baseline technical feature pack | `REQUIRED_CAPABILITY` | World State and Evidence | `REQUIRED_FOR_RELEASE` for R1A | `Technical Analysis.py:1327`, `Technical Analysis.py:1526`, `model.py:89` | TBD | `NO_TEST_FOUND` | Features | `PARTIALLY_IMPLEMENTED` | Technical indicators and OHLC geometry exist; approved baseline pack and registry tests missing. |
| `REQ-CONV-TA-002` | Candlestick baseline pack | `REQUIRED_CAPABILITY` when enabled | World State and Evidence | `OPTIONAL_FOR_RELEASE` in R1A unless scoped in | `Technical Analysis.py:1327`, `Technical Analysis.py:4112`, `outputs/technical_graph_system_v4/candle_feature_report.csv` | TBD | `NO_TEST_FOUND` | Features | `PARTIALLY_IMPLEMENTED` | Candle geometry/reporting exists; full named pattern pack not proven. |
| `REQ-CONV-MOD-002` | Sequence-model research challenger | `RESEARCH_ONLY_CANDIDATE` | Research Factory | `RESEARCH_ONLY` | `lstmfinancy.py:45`, `lstmfinancy.py:61` | TBD | `NO_TEST_FOUND` | Research | `PARTIALLY_IMPLEMENTED` | LSTM prototype exists; not PIT/canonical/replay integrated. |
| `REQ-CONV-GRAPH-001` | Graph peer features | `OPTIONAL_CAPABILITY` | World State and Evidence | `DEFERRED` for R0-1A | `stock_ai_4_files/2_train_models.py:220`, `model.py:138` | TBD | `NO_TEST_FOUND` | Research | `PARTIALLY_IMPLEMENTED` | Correlation/peer features and GAT prototype exist; not promoted. |
| `REQ-CONV-GRAPH-005` | Macro-sector context | `OPTIONAL_CAPABILITY` | World State and Evidence | `DEFERRED` for R0-1A | `stock_ai_4_files/2_train_models.py:189`, `Technical Analysis.py:1689`, `data_sources/fred_loader.py` | TBD | `NO_TEST_FOUND` | Features | `PARTIALLY_IMPLEMENTED` | Macro feature code exists; PIT and provider availability tests needed. |
| `REQ-CONV-CONT-002` | Content item construction | `OPTIONAL_CAPABILITY` | World State and Evidence | `DEFERRED` for R0-1A | `news_analysis.py:146`, `untitled1.py:144` | TBD | `NO_TEST_FOUND` | Content | `PARTIALLY_IMPLEMENTED` | DataFrame builder exists; canonical entity persistence missing. |
| `REQ-CONV-CONT-004` | Reference financial sentiment baseline | `OPTIONAL_CAPABILITY` | World State and Evidence | `DEFERRED` for R0-1A | `news_analysis.py:852`, `news_analysis.py:886`, `untitled1.py:540` | TBD | `NO_TEST_FOUND` | Content | `PARTIALLY_IMPLEMENTED` | FinBERT pipeline exists as research candidate; not a hard runtime dependency. |
| `REQ-CONV-CONT-010` | Source profiles | `OPTIONAL_CAPABILITY` | World State and Evidence | `DEFERRED` for R0-1A | `news_analysis.py:1172`, `untitled1.py:860` | TBD | `NO_TEST_FOUND` | Content | `PARTIALLY_IMPLEMENTED` | Source profile DataFrame exists; PIT canonical snapshots missing. |
| `REQ-CONV-LINK-004` | Content-market linkage | `OPTIONAL_CAPABILITY` | World State and Evidence / Learning Lab | `DEFERRED` for R0-1A | `news_analysis.py:1069`, `untitled1.py:757` | TBD | `NO_TEST_FOUND` | Content | `PARTIALLY_IMPLEMENTED` | Link builder exists; market-window maturity and leakage tests missing. |
| `REQ-CONV-DS-003` | `training_df` / `latest_features_df` schema distinction | `TEMPORAL_DATA_COMPONENT` | Temporal Data / Research Factory | `REQUIRED_FOR_RELEASE` for R0-1A replay | `stock_ai_4_files/2_train_models.py:381`, `stock_ai_4_files/3_daily_scan.py:75`, `data/pipeline_checkpoints/*/ml_df.csv`, `data/pipeline_checkpoints/*/latest_row.csv` | TBD | `NO_TEST_FOUND` | Data / Research | `PARTIALLY_IMPLEMENTED` | Artifacts exist; canonical `feature_snapshot` and schema parity tests missing. |
| `REQ-CONV-TOOL-001` | Operator inspection utilities | `OPERATOR_TOOL` | Governance / Learning | `OPTIONAL_FOR_RELEASE` | `untitled2.py:1`, `news_analysis.py:1593` | TBD | `NO_TEST_FOUND` | Ops | `PARTIALLY_IMPLEMENTED` | Inspection code exists; must map usage to `audit_event`. |
| `REQ-SCH-032` | Content/features/training schema governance | `REQUIRED_PLATFORM_INFRASTRUCTURE` | Canonical Data Model | `REQUIRED_FOR_RELEASE` when module enabled | `docs/CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md` | TBD | `NO_TEST_FOUND` | Architecture | `DESIGNED` | Schema addendum created; migrations and schema tests still required. |
| `REQ-GATE-003` | Paper/live readiness TBD blocker | `CONTROL_PLANE_COMPONENT` | Governance | `RELEASE_BLOCKER` | `docs/AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md` | TBD | `NO_TEST_FOUND` | Governance | `DESIGNED` | Readiness cannot be granted until hard thresholds are frozen and tested. |
