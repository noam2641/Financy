# Release 0-1A Implementation Backlog

This backlog turns the canonical North Star specification into an implementation path for the first two releases. It intentionally keeps advanced capabilities out of the critical path until the Decision Kernel has demonstrated value.

Canonical source: `AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md` v4.6.

## Release Criticality Rules

| Criticality | Meaning for Release 0-1A |
| --- | --- |
| `RELEASE_BLOCKER` | The release cannot be accepted without this item. |
| `REQUIRED_FOR_RELEASE` | Required for the declared release scope, but removable by explicit scope change. |
| `OPTIONAL_FOR_RELEASE` | May be disabled and shown in `runtime_manifest`. |
| `DEFERRED` | Intentionally postponed; not a current-release failure. |
| `RESEARCH_ONLY` | May run only in research/offline contexts and cannot write execution-eligible artifacts. |

## Release 0: Truth Kernel

Goal: prove that data, labels, validation, replay, and baseline comparisons are not leaking or overfit.

| Backlog ID | Scope | Requirement refs | Criticality | Status | Acceptance gate |
| --- | --- | --- | --- | --- | --- |
| R0-BL-001 | Point-in-time OHLCV and source snapshots | `REQ-REL0-001`, `REQ-DATA-001` through `REQ-DATA-004`, `REQ-CONV-DATA-001` through `REQ-CONV-DATA-008` | `RELEASE_BLOCKER` | Partial research code exists | No future-aware features; every bar has source, timestamp, and availability metadata. |
| R0-BL-002 | Deterministic dataset generation and replay | `REQ-REL0-001`, `REQ-TIME-001` through `REQ-TIME-006`, `REQ-CONV-OVN-001` through `REQ-CONV-OVN-014` | `RELEASE_BLOCKER` | Partial orchestration exists | Same config, code hash, seed, universe, and data snapshot reproduce artifact hashes. |
| R0-BL-003 | Provider normalization and MultiIndex handling | `REQ-CONV-DATA-001` through `REQ-CONV-DATA-006` | `REQUIRED_FOR_RELEASE` | Partial code exists | Downstream feature code receives one-dimensional numeric series only. |
| R0-BL-004 | Labels for 5, 8, and 14 sessions | `REQ-LBL-001` through `REQ-LBL-013` | `RELEASE_BLOCKER` | Needs canonical test coverage | Golden examples cover terminal events, missing bars, splits, delistings, and after-hours events. |
| R0-BL-005 | Purged walk-forward validation | `REQ-VAL-001` through `REQ-VAL-008` | `RELEASE_BLOCKER` | Partial reports exist | Train/test windows are embargoed and reproducible. |
| R0-BL-006 | Baseline model and baseline comparison | `REQ-MOD-001` through `REQ-MOD-010`, `REQ-VAL-009` through `REQ-VAL-014` | `REQUIRED_FOR_RELEASE` | Partial research code exists | Baseline beats naive comparator after costs or the release is marked no-edge. |
| R0-BL-007 | Initial test and coverage matrix | `REQ-DOC-007`, `REQ-CONV-TRACE-001` through `REQ-CONV-TRACE-003` | `RELEASE_BLOCKER` | Started in companion matrix | Every Release 0 blocker has code location, test ID, owner, status, and latest result. |

## Release 1A: Decision Kernel

Goal: turn the validated research workflow into a reproducible recommendation system using the small, stable Decision Kernel.

| Backlog ID | Scope | Requirement refs | Criticality | Status | Acceptance gate |
| --- | --- | --- | --- | --- | --- |
| R1A-BL-001 | Seven-component Decision Kernel only | `REQ-PROD-020` through `REQ-PROD-025`, `REQ-CONV-ARCH-016` | `RELEASE_BLOCKER` | Spec complete | No platform infrastructure is mislabeled as `DECISION_KERNEL_COMPONENT`. |
| R1A-BL-002 | Canonical recommendation aggregate | `REQ-SCH-001` through `REQ-SCH-031` | `RELEASE_BLOCKER` | Spec complete, code TBD | Recommendation, forecast, decision, risk, execution, outcome, and audit entities pass schema tests. |
| R1A-BL-003 | Baseline technical feature pack | `REQ-CONV-TA-001` through `REQ-CONV-TA-009` | `REQUIRED_FOR_RELEASE` | Partial research code exists | Feature pack is PIT-safe, versioned, tested, and replaceable. |
| R1A-BL-004 | Calibration, uncertainty, abstention, and `NO_ACTION` policy | `REQ-MOD-011` through `REQ-MOD-025`, `REQ-DEC-001` through `REQ-DEC-012` | `RELEASE_BLOCKER` | Thresholds not frozen | ECE, confidence, uncertainty, and abstention thresholds are approved before gate. |
| R1A-BL-005 | Portfolio-aware risk and sizing | `REQ-RISK-001` through `REQ-RISK-009`, `REQ-PORT-001` through `REQ-PORT-007` | `REQUIRED_FOR_RELEASE` | Partial research code exists | Position, exposure, concentration, and liquidity limits are enforced. |
| R1A-BL-006 | Runtime manifest and capability health | `REQ-DATAQ-009` through `REQ-DATAQ-013`, `REQ-CP-001` through `REQ-CP-012` | `RELEASE_BLOCKER` | Spec complete, code TBD | Disabled/degraded capability state is visible and blocks unsafe recommendations. |

## Explicitly Deferred From Release 0-1A

| Capability | Release 0-1A criticality | Earliest target | Reason |
| --- | --- | --- | --- |
| FinBERT/reference sentiment pipeline | `DEFERRED` | Release 2A | Valuable context module, but not needed to prove the Decision Kernel. |
| LSTM or other sequence model | `RESEARCH_ONLY` | Release 4 candidate | Must beat baseline under identical PIT, cost, risk, and validation rules. |
| Knowledge graph / graph neural network | `DEFERRED` | Release 2A or Release 4 | Keep graph context optional until marginal value is measured. |
| Counterfactual portfolios | `DEFERRED` | Release 2B | Learning Factory capability, not Release 0-1A blocker. |
| Broker execution and live trading | `DEFERRED` | Release 3+ | Requires shadow, paper, reconciliation, approval, and incident controls. |

## Readiness Thresholds To Freeze

Until these are approved, the system may be described as documented or partially implemented, but not `PAPER_READY` or `LIVE_READY`.

| Threshold | Current status | Required action |
| --- | --- | --- |
| Maximum ECE by horizon | `TBD_BLOCKER` | Freeze per horizon before final holdout. |
| Maximum drawdown | `TBD_BLOCKER` | Define absolute and benchmark-relative caps. |
| Minimum number of matured recommendations | `TBD_BLOCKER` | Define per horizon and regime. |
| Minimum shadow days | `TBD_BLOCKER` | Define minimum calendar and trading-session coverage. |
| Liquidity limits | `TBD_BLOCKER` | Freeze ADV, spread, capacity, and order-size limits. |
| Abstention thresholds | `TBD_BLOCKER` | Freeze confidence, uncertainty, stale-data, and no-edge thresholds. |
| Risk limits | `TBD_BLOCKER` | Freeze position, sector, portfolio, gap, and loss limits. |
| Overnight completion SLA | `TBD_BLOCKER` | Freeze latest allowed completion time before pre-open validation. |

