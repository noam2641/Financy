# AI Trading System — Architecture v5 (DRAFT / PROPOSED)

**Status:** PROPOSED draft for owner review. **This does NOT replace canonical v4.6** (`AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md`), which remains authoritative until a v5 is separately approved. Documentation-only; no code.
**Basis:** the ratified Owner Decisions (Round 1) + the reconciled twelve-document review. Correction-banner and evidence-grading commentary is intentionally **omitted** — this document states only the reconciled architectural meaning; provenance lives in the Phase-1/1.5/2 documents.

**Normative-statement tag:** `[Vx.y · src ADR-### · v4.6 <REQ> · STATUS · release · class]` where STATUS ∈ {OWNER_APPROVED, EMPIRICAL_TBD, DEFERRED}; class ∈ {INVARIANT, INTERFACE, POLICY, EMPIRICAL}; release ∈ {R0, R1A, R2A, R2B, R3, R4, all}.

---

## 1. Product Thesis & Falsification Model

- **[V1.1 · ADR-001 · REQ-PROD-001..006 · OWNER_APPROVED · all · INVARIANT]** The platform is a point-in-time-safe decision system that decides / abstains / (later) executes-under-approval for long-only US equities at swing horizons of 5, 8, and 14 exchange sessions. Its deliverable value is a **disciplined, auditable go/no-go**, not model breadth.
- **[V1.2 · ADR-002 · REQ-PROD-004 · EMPIRICAL_TBD · all · EMPIRICAL]** The platform's economic premise — that a **cost-adjusted, factor-residual, out-of-sample cross-sectional edge exists and is capturable** at these horizons — is a **falsifiable hypothesis**, not an assumption. Each opportunity type must declare: mechanism, expected direction + plausible effect-size band, half-life, capacity, and an explicit falsifier.
- **[V1.3 · ADR-002 · REQ-VAL-004, R0-BL-006 · OWNER_APPROVED(structure) · R0 · POLICY]** `BLOCKED_NO_EDGE` is a first-class terminal outcome. If the Edge Probe fails its pre-registered net-of-cost, DSR-adjusted hurdle, the program stops at the probe; it does not escalate to a learned layer to rescue a negative result.
- **[V1.4 · ADR-002 · REQ-GATE-003 · EMPIRICAL_TBD · R0 · EMPIRICAL]** Numerical hurdle values (effect-size band, min matured recommendations, etc.) are **pre-registered before final-holdout access** with a conservative provisional range, source rationale, decision rule, and freeze point; they require owner approval before that access.

## 2. Build Order & Release Gates

- **[V2.1 · ADR-001 · REQ-REL0/1A..4, REQ-REL4-003 · OWNER_APPROVED · all · INVARIANT]** Hybrid build order: build a **rigorous Release-0 Edge Probe** on Truth-Kernel foundations **before** any world-model, knowledge graph, evidence-dependency graph, counterfactual factory, autonomous LLM, or broader-platform capability.
- **[V2.2 · ADR-001 · REQ-PROD-020 · OWNER_APPROVED · all · INVARIANT]** "Edge-probe first" is a **smaller build order, not a low-rigor experiment**: PIT-aware, survivorship-aware, cost-aware, deterministic, auditable.
- **[V2.3 · ADR-001 · REQ-GOV-003/004 · OWNER_APPROVED · all · POLICY]** Release gates: `R0 truth/edge → R1A decision kernel → R1B runtime memory → R2A context → R2B learning → R3 shadow/paper → R4 advanced/limited-live`. A later-release capability may not become an earlier-release blocker (v4.6 REQ-REL4-003 preserved).

## 3. Exact Release-0 Edge Probe Scope

- **[V3.1 · ADR-001/006/008 · REQ-REL0-001 · OWNER_APPROVED · R0 · INTERFACE]** R0 comprises exactly: provider adapter + raw canonical OHLCV normalization; versioned corporate-action store + as-of adjustment; PIT survivorship-safe universe; 5/8/14-session matured labels with declared `price_basis`; grouped-by-date purged walk-forward + embargo; trial registry; one named baseline (GBT) + comparators; factor-attributed, net-of-cost, DSR-adjusted report vs an investable benchmark; append-only run ledger + `feature_snapshot` manifests; deterministic replay.
- **[V3.2 · ADR-015 · REQ-REL0-003 · OWNER_APPROVED · R0 · INVARIANT]** R0 explicitly **excludes**: news/graph/LLM/deep-learning/SEC-fundamentals/options/opportunity-memory/paper-trading/counterfactual portfolios/world-model-hypotheses/evidence-dependency graph.
- **[V3.3 · ADR-005 · REQ-LAB-001/011 · OWNER_APPROVED(working default) · R0 · POLICY]** The Edge-Probe exit convention is **pure fixed-horizon exit** (label = traded return); stop/target/time-stop barriers are added only later as a validated challenger.

## 4. Target-Basis & Unit Flow

- **[V4.1 · ADR-003 · REQ-LAB-005/006 · OWNER_APPROVED · all · INVARIANT]** Target bases: **primary economic/trading forecast target = `ABSOLUTE_EXECUTABLE_RETURN`**; secondary research/ranking target = `MARKET_EXCESS_RETURN`; secondary non-gating diagnostic = `SECTOR_EXCESS_RETURN`. All bases are preserved explicitly and **never mixed**; sector-excess is never the primary traded objective.
- **[V4.2 · ADR-004 · REQ-DEC-001 · OWNER_APPROVED · all · INTERFACE]** `economic_edge_bps = expected_return_bps − pretrade_round_trip_cost_bps`, where `expected_return_bps` is on the **`ABSOLUTE_EXECUTABLE_RETURN_BPS`** basis. **Only** absolute-executable values may have absolute costs subtracted.
- **[V4.3 · ADR-003/004 · REQ-MOD-008/009, REQ-LAB-006 · OWNER_APPROVED · all · INTERFACE]** Canonical unit flow (bps unless noted):
  `research label (declared price_basis) → model output (same declared basis) → ranking (market-excess/sector-excess, relative ordering) → cost subtraction (ABSOLUTE-EXECUTABLE) → risk_adjusted_utility_bps → portfolio outcome (ABSOLUTE realized) → promotion metric (net-of-cost, benchmark-relative, beta-adjusted, DSR-deflated)`. Ranking may be relative; cost subtraction and utility are absolute-executable.

## 5. Price-Basis & PIT Policy

- **[V5.1 · ADR-006 · REQ-PRICE-001..006, REQ-LAB-001/007 · OWNER_APPROVED · all · INVARIANT]** Immutable **raw tradable OHLCV** is the base vintage; adjusted series are **derived as-of** using only corporate actions with `ex_date ≤ cutoff`, versioned by `corporate_action_version`. Orders/stops/fills use raw prices.
- **[V5.2 · ADR-006 · REQ-LAB-001 · OWNER_APPROVED · all · INTERFACE]** Every label and analytical series carries an explicit `price_basis` bound to `target_definition_version`.
- **[V5.3 · ADR-006 · REQ-PRICE-002/003 · OWNER_APPROVED · all · INVARIANT]** **Current-vintage back-adjusted data is prohibited** for price-level features, liquidity/min-price filters, universe construction, and labels. The **split-only simple-return exception** is preserved where mathematically valid (a split multiplies prior prices by a constant that cancels in simple returns).
- **[V5.4 · ADR-007 · REQ-TIME-006/008, REQ-DATA-001 · OWNER_APPROVED · all · INVARIANT]** Pre-go-live backtests use **INFORMATION_THEORETIC replay only**; `SYSTEM_REALISTIC` replay accrues forward once real ingestion/availability timestamps are recorded. Estimated timestamps set `is_estimated_timestamp=true`; fabricating `system_available_at` is prohibited.

## 6. Universe & Instrument Identity

- **[V6.1 · ADR-008 · REQ-DOM-015..019 · OWNER_APPROVED · all · INVARIANT]** The universe is constructed **point-in-time as-of backtest-start**, including securities later delisted/merged/bankrupt; membership is frozen from that date.
- **[V6.2 · ADR-008 · REQ-DOM-015/016 · OWNER_APPROVED · all · INTERFACE]** The canonical key is an **opaque `instrument_id`** (never derived from ticker); an `instrument_identifier_history` resolves ticker/CIK/FIGI as-of date; **ticker-only joins are prohibited**.
- **[V6.3 · ADR-008 · REQ-LAB-013 · OWNER_APPROVED · all · INTERFACE]** Delisting/merger/bankruptcy produce **terminal-event returns**; they never become silently missing labels.
- **[V6.4 · ADR-009 · REQ-LAB-006/009 · OWNER_APPROVED(deferral) · R0 · POLICY]** **No sector taxonomy is a gating dependency in R0.** PIT GICS is deferred pending an explicit value+licensing decision; SIC is not a transparent GICS substitute; SIC usability is EMPIRICAL_TBD.

## 7. Validation-Method Applicability

- **[V7.1 · ADR-001/013 · REQ-VAL-001/002 · OWNER_APPROVED · R0 · INVARIANT]** Primary timeline = **grouped-by-date purged walk-forward**; **embargo ≥ the maximum information interval** (≥ 14 sessions + feature memory); purge is bidirectional over the cross-sectional date union.
- **[V7.2 · ADR-001/013 · REQ-VAL-008 · OWNER_APPROVED · R0 · POLICY]** A **trial registry is mandatory** (every config/seed/horizon/target/grid point; any value chosen after viewing a backtest is a trial).
- **[V7.3 · ADR-013 · REQ-VAL-008 · OWNER_APPROVED · R0 · POLICY]** **Deflated Sharpe Ratio** is required **when multiple strategy/model trials exist**; **PBO/CSCV** is required **only when enough variants and partitions exist** (`PBO_NOT_ESTIMABLE` is neither a pass nor proof of failure); **CPCV** is a robustness analysis when its assumptions/sample support it. No method is claimed estimable when its prerequisites are absent.
- **[V7.4 · ADR-013 · REQ-VAL-004/005/006 · OWNER_APPROVED · R0 · POLICY]** Edge gate = **factor-attributed residual net-of-cost significance** + outperformance of an **investable benchmark** (buy-and-hold SPY + matched basket, beta-adjusted, net of the same cost model); metrics use **effective-sample** (non-overlapping/block-bootstrap) inference, not raw row counts.
- **[V7.5 · ADR-016 · REQ-GATE-001 · EMPIRICAL_TBD · R0 · EMPIRICAL]** Numerical acceptance thresholds (max ECE, min matured recs, positive-window counts, drawdown caps) are frozen from external priors before final-holdout access.

## 8. Baseline Model Strategy

- **[V8.1 · ADR-010/011 · REQ-MOD-001/002 · OWNER_APPROVED(working default) · R0/R1A · INTERFACE]** Base forecast = **gradient-boosted trees (LightGBM/XGBoost)** as the primary learned predictor; **elastic-net + per-date cross-sectional regression** as the comparator/naive baseline.
- **[V8.2 · ADR-010 · REQ-MOD-003/005 · OWNER_APPROVED(working default) · R1A · INTERFACE]** Probability outputs pass an **isotonic/Platt calibration** layer (GBT is natively miscalibrated); intervals via **quantile regression / conformal (CQR)**, with coverage validated under time-series (non-exchangeable) conditions and calibration sets that obey purge/embargo.
- **[V8.3 · ADR-010 · REQ-MOD-008 · OWNER_APPROVED(working default) · R1A/R2 · INTERFACE]** **Learning-to-rank (LambdaMART)** is the first ranking challenger (objective is cross-sectional ordering).
- **[V8.4 · ADR-011 · REQ-CONV-MOD-005/007, REQ-REL4-002 · DEFERRED · R4 · POLICY]** All deep/sequence/graph/LLM/multimodal models are **Release-4 replaceable challengers** that must beat the calibrated tabular baseline net-of-cost under identical PIT/cost/CPCV rules; they are never MVP dependencies.

## 9. Deterministic Decision Kernel

- **[V9.1 · ADR-011 · REQ-PROD-020 · OWNER_APPROVED(working default) · R1A · INVARIANT]** The MVP decision layer is a **deterministic penalized-utility policy** + deterministic permission gate + hard-blocker rule engine + cross-sectional ranker + greedy risk-budgeted allocator. "Deterministic decision policy" does **not** imply a deterministic forecast — the forecast (§8) is learned.
- **[V9.2 · ADR-012 · REQ-DEC-002 · OWNER_APPROVED(working default) · R1A · POLICY]** Every policy weight/threshold carries a class: `FROZEN_ECONOMIC_PRIOR` / `OWNER_POLICY_PARAMETER` / `FIT_ON_TRAINING_ONLY` / `EMPIRICAL_THRESHOLD` / `PROMOTION_THRESHOLD`. Utility λ are **FROZEN_ECONOMIC_PRIOR** for the MVP; any weight chosen after viewing a backtest becomes trial-registered and enters the overfitting analysis.
- **[V9.3 · ADR-011 · REQ-CONV-MOD-004, REQ-LEARN-009 · DEFERRED · R4 · POLICY]** A learned aggregator (stacking/MoE) is a gated Research-Factory `DECISION_POLICY_CHALLENGER` that must beat the frozen policy out-of-sample under identical cost/risk/CPCV before any promotion.
- **[V9.4 · ADR-004/011 · REQ-MOD-006/011 · OWNER_APPROVED · R1A · INVARIANT]** No alpha/probability score outputs position size directly. Sizing precedence: forecast → permission → hard blockers → economic-edge gate → risk-adjusted-utility gate → per-trade risk-budget size → caps → portfolio marginal-utility allocation → turnover/hysteresis → execution feasibility → human approval; a size is produced only at the risk-budget step and may only shrink thereafter.

## 10. Risk & Portfolio Boundaries

- **[V10.1 · ADR-011 · REQ-RISK-001..004 · OWNER_APPROVED(working default) · R1A · INTERFACE]** Position size = `risk_budget / planned_stop_distance` **capped** by a gap-tail adjustment (size to worst-case overnight/earnings gap, not stop distance), max notional, ADV participation, buying-power, min-order, and leverage caps.
- **[V10.2 · ADR-011 · REQ-PORT-001..004 · OWNER_APPROVED(working default) · R1A · POLICY]** Portfolio construction = greedy marginal-utility allocation with concentration/sector/factor caps and turnover/hysteresis controls; **not** a mean-variance optimizer (falls back to greedy risk-budget).
- **[V10.3 · ADR-014 · REQ-RISK-003 · EMPIRICAL_TBD · R1A · EMPIRICAL]** ADV/spread/capacity/order-size caps are frozen from measured spread/ADV (EXP-3), not assumed.

## 11. Execution / Cost Modeling

- **[V11.1 · ADR-014 · REQ-COST-001..003 · OWNER_APPROVED(working default) · R0/R1A · INTERFACE]** Cost is modeled **round-trip (two-sided)** with an explicit exit/close-auction leg; per-name impact ≈ √(size/ADV); commissions, spread, impact, auction, slippage, fees decomposed.
- **[V11.2 · ADR-014 · REQ-PRICE-005/006 · OWNER_APPROVED(working default) · R0/R1A · POLICY]** When true auction data is absent, `open_execution_quality = PROXY` carries a **numeric conservative floor** (worst-of open vs first-bar + widened spread), never a clean first-bar fill.
- **[V11.3 · ADR-014 · REQ-COST-002, REQ-SIM-001 · EMPIRICAL_TBD · R1A/R3 · EMPIRICAL]** `pretrade` vs `simulated` vs `actual_realized` costs are reconciled; the edge is re-validated against realized R3 paper costs before live promotion.

## 12. Minimal Release-1A Entity Model

- **[V12.1 · ADR-015 · REQ-SCH-001..031, REQ-PROD-020 · OWNER_APPROVED(in principle) · R1A · INTERFACE]** R1A instantiates only entities that are **written by the R1A Decision Kernel, read by a required R1A component, or needed for auditability/feature-snapshots/decisions/risk/ledger persistence**. The exact set is derived by the Phase-3 **producer/consumer/entity matrix** (`RELEASE_0_IMPLEMENTATION_READINESS_GATE.md`); **no fixed count is frozen**.
- **[V12.2 · ADR-015 · REQ-LEARN-001..004, REQ-SCH-037 · OWNER_APPROVED · R1A · INVARIANT]** Preserved in R1A: modular monolith, small Decision Kernel, `feature_snapshot`, append-only decision ledger, cohort/outcome logging.
- **[V12.3 · ADR-015 · REQ-DOM-026/032/034, REQ-LEARN-007 · DEFERRED · R2A/R2B/R4 · POLICY]** Deferred (remain DESIGNED until their producer release): evidence-dependency graph, world-hypothesis engine, opportunity-analytics platform, knowledge graph, counterfactual learning factory, autonomous LLM capabilities.

## 13. AI/LLM Advisory-Layer Boundaries

- **[V13.1 · ADR-018 · REQ-LLM-001..005, REQ-PROD-012 · OWNER_APPROVED(boundary) · all · INVARIANT]** The AI/LLM layer is an **analysis and interaction layer only**, not a source of numerical truth or trading authority. It must NOT modify risk limits, modify portfolio state, promote models, alter policy, submit broker instructions, or rewrite audit history.
- **[V13.2 · ADR-018 · REQ-LLM-002/003 · OWNER_APPROVED(boundary) · all · INTERFACE]** Every AI response used by the system preserves: `as_of` timestamp, source IDs, model provider, model version, prompt-template version, tool calls, structured claims, uncertainty, validation status.
- **[V13.3 · ADR-018 · REQ-CONV-CONT-004 · EMPIRICAL_TBD · R1A/R2A · POLICY]** MVP default = deterministic templated explanations from reason codes + optional advisory NL query / RAG over approved artifacts; structured extraction and learned-evidence LLM are challengers admitted only on positive module-value; **autonomous decision authority is REJECTED**.

## 14. Audit, Provenance & Reproducibility

- **[V14.1 · ADR-001/015 · REQ-LEARN-001..004, REQ-AUD-001 · OWNER_APPROVED · R0/R1A · INVARIANT]** An **append-only decision/run ledger** with correlation/causation IDs and cohort/outcome logging is present from R0; cryptographic hash-chaining + transactional outbox are additive at R3 (shadow) without schema change.
- **[V14.2 · ADR-016 · REQ-GATE-001, REQ-CONV-OVN-006 · OWNER_APPROVED · R0 · POLICY]** **Two-tier reproducibility**: bit-exact for symbolic artifacts (fold manifests, feature-column registry, label frames, config, code SHA, schema hashes); seeded + documented numeric tolerance for float artifacts (model weights, calibrated probabilities, metrics). R0 runs deterministic/CPU mode where feasible.
- **[V14.3 · ADR-016 · REQ-DOM-005, REQ-SCH-007 · OWNER_APPROVED · R0/R1A · INTERFACE]** `environment_hash = H(python_version, pinned key libraries, BLAS impl+version, cuda/cudnn or "cpu", container image digest, os_release)`; included in checkpoint-resume verification and the runtime manifest.
- **[V14.4 · ADR-006 · REQ-SCH-037, REQ-CONV-DS-004 · OWNER_APPROVED · R0 · POLICY]** `feature_snapshot` seals schema hash **and** a feature-values checksum; a golden train/serve **value-parity** test asserts equality (within tolerance) between the batch and "latest" paths for a fixed as-of date.

## 15. EMPIRICAL_TBD Register (v5)

| Ref | Item | Provisional default | Freeze point |
| --- | --- | --- | --- |
| V1.2/V1.4 | Edge effect-size band + acceptance hurdles | assume no edge; conservative literature band | before final-holdout access |
| V6.4 | SIC sector usability | no gating sector target | after EXP-4 |
| V9.3 | Learned-aggregator challenger value | deterministic policy | after challenger gate |
| V10.3/V11.3 | Cost/capacity/ADV/spread caps | conservative literature bands; liquid universe | after EXP-3 / R3 paper |
| V7.5 | Numeric acceptance thresholds | external-prior seeds, signed | before final-holdout access |
| V13.3 | AI/LLM analysis-layer value | templated explanations only | after module-value proof |

## 16. Promotion & Kill States

- **[V16.1 · ADR-002 · REQ-GOV-003 · OWNER_APPROVED · all · POLICY]** Promotion ladder: `RESEARCH → VALIDATION → SHADOW → PAPER → LIMITED-LIVE`, each gated by the acceptance criteria of its phase; no readiness level is claimed while any hard threshold for that level remains TBD.
- **[V16.2 · ADR-001/002 · R0-BL-006 · OWNER_APPROVED · R0 · POLICY]** **Kill state `BLOCKED_NO_EDGE`**: Edge Probe fails its pre-registered net-of-cost DSR-adjusted hurdle → stop; do not build the platform.
- **[V16.3 · ADR-017 · REQ-GOV-001/002, REQ-KILL-001 · OWNER_APPROVED(internal-policy) · R3+ · POLICY]** Governance cap (internal policy, pending legal-applicability determination): a solo operator may reach SHADOW on self-validation-with-disclosure; PAPER/LIVE require a named external reviewer + a second kill-switch resetter.
- **[V16.4 · ADR-018 · REQ-LLM · OWNER_APPROVED · all · INVARIANT]** Autonomous AI decision/execution authority is a **permanent REJECTED state** absent an explicit future owner decision.

---
**End of v5 draft.** v4.6→v5 deltas: `V4_6_TO_V5_CHANGE_PROPOSAL.md`. Implementation readiness: `RELEASE_0_IMPLEMENTATION_READINESS_GATE.md`.
