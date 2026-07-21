# Research Protocol and Question Map

**Program:** AI Trading Decision & Recommendation Platform for US Equities — `ARCHITECTURE_AND_RESEARCH_DEFINITION` phase
**Deliverable:** Phase 0 (Research Control Plane)
**Status:** Normative for the Phase 1 evidence pass. Documentation-only. This document does not modify canonical v4.6.

---

## 0. Audit Metadata

| Field | Value |
| --- | --- |
| Repository audited | `noam2641/Financy` |
| Commit audited | `origin/main` → `7c4c659` ("Add files via upload"), fast-forwarded into `claude/trading-platform-audit-iawx0v` |
| Repository state | **Seven documentation files, zero implementation code** (no `.py`, `.ipynb`, `tests/`, or `src/` in any commit or branch) |
| Research cutoff date | **2026-07-21** |
| Canonical spec | `AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md` v4.6 |
| Schema addendum | `CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md` — present and reviewed (the REQ-DOC-012 named artifact; does **not** by itself constitute the full REQ-DOC-011 Conversation-Derived Capability Package) |
| Prior input | Part I six-agent pre-development audit — **evidence and a source of hypotheses only, NOT authority or ground truth**. Its findings, severity classifications, and terminal verdict must be **independently challenged**, not confirmed. |

**Authority order** (highest first): recorded/versioned owner decisions → canonical spec v4.6 → approved schema/contract addenda → approved ADRs → release backlog & testing architecture → coverage/traceability matrices → historical prototype references → informal notes. Existing documentation is **not** automatically correct and must be challenged against research and internal consistency.

**Phase constraints:** No code, notebooks, executable pseudocode, `src/`, `tests/`, migrations, CI, broker connections, secrets, or execution. Language-neutral signatures, schemas, state machines, and interface contracts are permitted as architecture artifacts.

---

## 1. Central Research Questions (Section 6 map)

These are the questions the Phase-1 evidence pass must answer with graded evidence. Each is tagged with the owning agent(s) (see §6).

**1.1 Product thesis (A1, A7)** — What exact decision is optimized? Intended user action? Prediction horizon vs holding period? Ranking target vs portfolio-return target vs executed-policy target? **What persistent market inefficiency is hypothesized, and why might it persist after transaction costs?** Expected effect-size band, half-life, capacity? Abstention conditions? **What result would falsify the thesis?** — "AI", "more data", "world understanding", "multiple agents", "continuous learning" are **not** acceptable edge theses.

**1.2 Build order (A7, A1, A6)** — full-platform-first vs Release-0-truth-kernel-first vs thin edge-probe-first vs hybrid. Which decisions are resolvable pre-evidence vs require a later experiment? The architecture must not require a large platform merely to discover no cost-adjusted edge exists; the edge experiment must not be so thin that leakage/survivorship/corporate-action/validation errors make the result meaningless.

**1.3 Target & objective alignment (A1, A4, A5)** — Resolve the relationships among absolute / market-excess / sector-excess return, rank target, calibrated probability, expected-return-bps, risk-adjusted utility, simulated-executable return, realized return. For each transformation define input basis, output basis, units, sign, price basis, cost treatment, horizon, availability time, research-vs-policy status. **No operation may subtract absolute cost from a relative or undefined return.**

**1.4 Decision architecture (A4, A3)** — deterministic penalized utility vs learned stacking vs mixture-of-experts vs Bayesian decision model vs constrained optimization. For each: sample-size need, effective independent sample size, leakage risk, calibration, explainability, stability, retraining, multiple-testing burden, operational complexity, expected incremental value, failure modes, promotion gate. **No learned component without: a clear target, valid training data, sufficient effective sample, a PIT-safe protocol, a challenger baseline, a falsifiable incremental-value gate, and a reason a deterministic method is insufficient.**

**1.5 Model strategy (A3)** — For each candidate family (§6, A3): decision contribution, appropriate target, inputs, minimum data, expected benefit, strongest supporting studies, contradictory studies, failure modes, leakage pathways, calibration needs, compute/ops cost, interpretability, release eligibility, status ∈ {MVP_REQUIRED, MVP_OPTIONAL, RESEARCH_CHALLENGER, DEFERRED, REJECTED}, explicit kill criterion.

**1.6 Data strategy (A2)** — For each provider/source: information-time capability, system-availability capability, revision history, correction behavior, licensing, retention, rate limits, expected monthly cost, replay-class support (`INFORMATION_THEORETIC_REPLAY` / `SYSTEM_REALISTIC_REPLAY`), permitted release stage. **Current-only metadata must not be described as point-in-time historical data.**

**1.7 Validation strategy (A1, A2)** — grouped-by-date folds, purged walk-forward, embargo, bidirectional interval-overlap protection, nested validation, out-of-fold calibration, multiple-testing control, Deflated Sharpe Ratio, PBO, serial-dependence adjustment, block bootstrap, regime analysis, factor attribution, capacity analysis, cost stress, locked holdout, paper revalidation, live-decay monitoring. Distinguish leakage / statistical dependence / multiple testing / distribution shift / train-serve skew / provider revision / implementation error.

**1.8 Risk & execution (A5, A4)** — risk budget, portfolio vol, concentration, sector/factor exposure, beta, liquidity, ADV participation, expected shortfall, gap risk, event risk, drawdown, turnover, stops/targets/time-stops, partial fills, cancellation, open-auction execution, exit & round-trip cost, kill switch, graduated de-risking. **No position size output directly from an alpha score.** Define precedence: forecast → permission → hard risk blockers → per-trade risk budget → portfolio marginal utility → position/liquidity caps → execution feasibility → human approval.

---

## 2. Search Terms and Date Ranges

**Date policy:** foundational methods any year (e.g., Fama-French factors, purged/embargoed CV, backtest-overfitting theory); ML/DL/LLM/graph emphasis **2015–2026**. Research cutoff **2026-07-21**. Prefer the most recent authoritative version of any evolving method.

**Representative search-term clusters** (agents expand as needed):
- *Edge/factor:* "cross-sectional stock return predictability", "short-term reversal equity", "momentum crash", "factor zoo replication", "post-earnings announcement drift persistence", "anomaly decay after publication", "transaction costs anomaly profitability".
- *Validation:* "purged cross-validation financial", "combinatorial purged cross-validation", "deflated Sharpe ratio", "probability of backtest overfitting", "block bootstrap Sharpe", "multiple testing finance".
- *Models:* "gradient boosting vs deep learning tabular", "empirical asset pricing machine learning", "LSTM stock return forecasting out-of-sample", "temporal fusion transformer finance", "graph neural network stock", "FinBERT financial sentiment", "conformal prediction time series", "probability calibration isotonic Platt", "stacking generalization leakage".
- *Data/PIT:* "point-in-time fundamentals restatement bias", "survivorship bias delisting returns", "CRSP historical index constituents", "GICS historical membership", "SEC EDGAR XBRL point in time", "FRED ALFRED vintage", "adjusted price look-ahead corporate action".
- *Execution:* "opening auction execution cost equities", "market impact model square-root law", "implementation shortfall", "bid-ask spread estimator Corwin Schultz", "fill probability limit order", "capacity strategy ADV".
- *MLOps/governance:* "model risk management SR 11-7", "reproducibility machine learning determinism", "feature store train serve skew", "champion challenger model deployment".

---

## 3. Inclusion / Exclusion Criteria

**Include (eligible for grade A/B):** peer-reviewed journals, official conference proceedings, primary research papers, official standards, official provider/exchange/regulator/vendor documentation, well-designed empirical studies with disclosed methodology; US-equity focus or credibly transferable; horizon relevant to 5–14 session swing trading; profitability claims that disclose transaction-cost, survivorship, and PIT handling.

**Downgrade or exclude (grade C or UNSUPPORTED):** marketing pages, unsourced blogs, generic tutorials, social-media claims, benchmark tables without methodology, results on crypto/FX/other markets asserted for US equities without a transfer argument, papers that cannot be connected to this platform's dataset/horizon/cost regime. High-quality preprints allowed but **labeled non-peer-reviewed**; reputable practitioner research only as supporting evidence.

---

## 4. Evidence-Grading Rules (normative)

| Grade | Meaning |
| --- | --- |
| **A** | Multiple relevant peer-reviewed/authoritative sources with aligned results |
| **B** | One strong relevant source, or several partially relevant sources |
| **C** | Limited, indirect, preprint, or practitioner evidence |
| **D** | Theoretical proposal or weak empirical support |
| **UNSUPPORTED** | No credible evidence found |

**Hard rules:** Never fabricate a citation, venue, dataset, or result. If a claim cannot be tied to a verifiable source → **UNSUPPORTED**. A statistically significant result is **not** an economically tradeable result. Always separate: prediction accuracy · ranking quality · calibration · discrimination · economic utility · cost-adjusted return · risk-adjusted return · portfolio capacity · live robustness. Do not infer live profitability from a paper unless its methodology (cost, survivorship, PIT, horizon) justifies the inference.

---

## 5. Common Extraction Fields (every cited source)

`citation` · `year` · `venue` · `source_type` · `peer_reviewed` (Y/N) · `research_question` · `dataset` · `sample_period` · `market/asset_class` · `horizon` · `target` · `validation_design` · `cost_treatment` · `survivorship_treatment` · `corporate_action_treatment` · `PIT_treatment` · `reported_result` · `limitations` · `relevance_to_platform` · `evidence_grade`.

---

## 6. Agent Roster, Overlap Boundaries, and Contradictory Hypotheses

Eight genuinely independent research agents. **Round 1 is fully independent** — no agent may see, cite, or rely on another agent's findings. Each must actively search for the **contradictory hypothesis** assigned to it (not only confirming evidence).

| ID | Agent | Core questions | Owns | Round-1 boundary | Contradictory hypothesis to actively seek |
| --- | --- | --- | --- | --- | --- |
| **A1** | quant-research-methodologist | 1.1, 1.3, 1.7 | labels, benchmarks, factor attribution, overfitting, multiple-testing (DSR/PBO), power, capacity | methodology/statistics only; PIT mechanics→A2, model families→A3 | Short-horizon US-equity cross-sectional edge is arbitraged away net of cost / is short-term-reversal or factor beta |
| **A2** | point-in-time-data-architect | 1.6 | provider capability, replay semantics, survivorship, sector/index history, restatements | data availability only; folds→A1, feature contracts→Phase 4 | Retail/free data (yfinance, FRED, free news) cannot support `SYSTEM_REALISTIC` replay or PIT sector/membership without fabricated timestamps |
| **A3** | model-research-architect | 1.4, 1.5 | model families + calibration/uncertainty/conformal | model internals only; decision aggregation→A4 | Deep/sequence/graph models do NOT beat well-tuned GBT/linear on tabular financial cross-sections OOS after costs |
| **A4** | decision-policy-and-portfolio-architect | 1.3, 1.4, 1.8 | decision policy, portfolio construction, utility/abstention, sizing precedence | microstructure/costs→A5, model internals→A3 | A learned super-model adds no OOS value over a frozen deterministic policy and cannot be trained on the effective sample |
| **A5** | execution-and-market-microstructure-critic | 1.8 | execution realism, costs, capacity | sizing policy→A4 | Realistic round-trip costs on the target liquidity band eliminate the modeled edge |
| **A6** | production-mlops-and-governance-architect | 1.2, 1.6 (ops) | ops, governance, reproducibility, registries | research validity→A1 | The full control-plane / event-sourcing / registry stack is disproportionate; off-the-shelf tooling + versioned artifacts suffice pre-paper |
| **A7** | adversarial-simplification-critic | 1.1, 1.2 | simplification, over-engineering, build-order, pre-mortem | **Round-1:** independently research simplification alternatives, over-engineering risks, build-order risks, failure scenarios **without access to other agents' findings**. **Round-2 role:** inspect, cite, challenge other agents' evidence | A thin edge-probe + deterministic harness beats the full platform on reliability, explainability, and time-to-evidence |
| **A8** | requirements-and-interface-auditor | traceability | REQ-ID integrity, interface completeness, code-reference classification → seeds H1 | pure reference/consistency; no research grading | "Spec complete" ≠ traceable; hidden contradictions and non-resolving IDs exist |

**A8 method (mandatory):** First **extract the authoritative REQ-ID set** from canonical v4.6. Then classify **each** reference individually as **VALID / INVALID / AMBIGUOUS / LIKELY_TYPO / DEPRECATED** against that set. **Do not assume any complete range is invalid** (e.g., `REQ-VAL-009..014`, `REQ-DEC-001..012`, `REQ-RISK-001..009`, `REQ-PORT-001..007`) — verify each ID. Classify every cited code file as `REPOSITORY_LOCAL_VERIFIED` / `EXTERNAL_PROTOTYPE_REFERENCE` / `HISTORICAL_REFERENCE_UNVERIFIED` / `PLANNED_LOGICAL_COMPONENT` / `MISSING_REFERENCE`.

---

## 7. Specification Claims Flagged for Active Validation (all agents)

Each must be actively challenged, not assumed correct:
- sector-excess as **primary ranking target** (REQ-LAB-006)
- calibration/ECE as a **Release-1A blocker** (R1A-BL-004)
- purged walk-forward + embargo **adequacy** (REQ-VAL-001/002)
- FinBERT as sentiment **baseline** (REQ-CONV-CONT-004)
- LSTM / graph as **Release-4 challengers** (REQ-CONV-MOD-*, REQ-CONV-GRAPH-*)
- yfinance / FRED **PIT sufficiency** (REQ-CONV-DATA-008)
- ~34-entity aggregate as a **Release-1A blocker** proportionality (R1A-BL-002)
- counterfactual factory as **product identity** (REQ-PROD-003)
- knowledge-graph **incremental value** (REQ-DOM-034)

---

## 8. Round Protocol

**Round 1 (independent):** each agent forms conclusions in isolation, with live web research, producing findings + graded source entries + capability classifications. No agent receives another's output.

**Round 2 (cross-examination):** the lead shares relevant findings and every agent (A7 especially) may challenge/corroborate. **Mandatory cross-examination of:** every BLOCKER, every CRITICAL conclusion, every advanced-learned-model recommendation, every major-capability-removal recommendation, every point-in-time-safety claim, every expected-economic-value claim, every data-provider capability claim. For each major conclusion record: proposer · independent corroborator · challenger · consensus reached? · unresolved disagreement · owner decision required. **Do not force consensus on genuinely mixed evidence.**

### 8.1 Anti-Anchoring and Blocker-Scope Rules (normative for every Round-1 agent)

**Anti-anchoring (included verbatim in every Round-1 agent prompt):** _"The prior six-agent audit is evidence and a source of hypotheses, not ground truth. Independently challenge its findings, severity classifications, and terminal verdict."_ The prior terminal verdict ("Development should not begin until the listed blocking decisions are resolved") is a **hypothesis to test**, not a conclusion to confirm. An agent may corroborate, refute, re-scope, or re-grade any prior finding.

**Blocker-scope:** any finding classified BLOCKER/CRITICAL must name **which specific gate(s) it blocks** — {`architecture_freeze`, `release_0_definition`, `release_0_acceptance`, `release_1A`, `final_holdout`, `shadow`, `paper`, `live`} — and must **not** be treated as a universal blocker to all development unless the evidence specifically supports that. A finding may block `paper`/`live` while leaving `release_0_definition` unblocked.

**Corrected input facts (supersede any stale Part I / PIT-11 formulation):** (a) `CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md` is **present and reviewed**; (b) the addendum does **not** by itself satisfy the complete REQ-DOC-011 capability package; (c) repository-local implementation code and tests **remain absent**; (d) PIT-11 must **no longer** claim the addendum is missing.

---

## 9. Required Output Format (each agent returns)

1. **Findings** — ID · title · classification {CONFIRMED / LIKELY / UNRESOLVED / OPTIONAL / REJECTED} · severity {BLOCKER / CRITICAL / HIGH / MEDIUM / LOW} · affected REQ IDs · affected releases · internal evidence · external research evidence + grade · reasoning · failure scenario · financial/data/operational consequence · recommended correction · simpler alternative · verification method · owner-decision-required · **blocks-which-gate(s)** ∈ {architecture_freeze, release_0_definition, release_0_acceptance, release_1A, final_holdout, shadow, paper, live} — never a universal blocker unless evidence specifically supports it.
2. **Source entries** — in the §5 extraction format, each with an evidence grade.
3. **Capability classification** — every in-scope capability tagged {MVP_REQUIRED / MVP_OPTIONAL / RESEARCH_CHALLENGER / DEFERRED / REJECTED} + explicit kill criterion.
4. **Verdict + top-5 findings.**

---

## 10. Anti-Hallucination Rules

Distinguish: evidence vs inference · architecture vs implementation · research finding vs product decision · current repo state vs historical claim · statistical vs economic significance · ranking quality vs trade profitability · calibration vs value · research replay vs system-realistic replay · inability-to-validate vs evidence-of-failure · future requirement vs MVP requirement. Never invent citations, code, missing files, provider capabilities, numeric thresholds, sample sizes, or backtests. Do not assume a complex model is superior; do not assume agent agreement proves correctness; do not assume recent research transfers to US-equity swing trading without checking dataset, horizon, and cost treatment.

---

## 11. Consistency Gate (must pass before each phase is committed)

- no stale repository-state statements (verified: `origin/main` `7c4c659` = seven documentation files, zero implementation code);
- no document described as both present and missing (the schema addendum is present and reviewed);
- no agent marked both RETURNED and pending;
- no unresolved REQ-ID presented as valid (every ID classified via the A8 process);
- no Round-1 agent instructed to use another agent's findings;
- no fabricated or ungraded external citation.

---

## 12. Deliverable Mapping (Phase 1 outputs)

| Deliverable | Fed primarily by |
| --- | --- |
| **A** `ARCHITECTURE_RESEARCH_AND_EVIDENCE_REPORT.md` | all agents (Round 1 + Round 2 synthesis) |
| **D** `MODEL_AND_METHOD_EVIDENCE_MATRIX.md` | A3, A4 (+ A1 on validation methods) |
| **E** `DATA_PIT_AND_VALIDATION_APPENDIX.md` | A2, A1, A5 |
| **H1** `REQUIREMENT_TRACEABILITY_RECONCILIATION.md` (initial) | A8 |

Phase 1 explicitly does **not**: freeze the architecture, write function contracts, or select a complex model because research exists. It separates facts, inferences, owner choices, and empirical TBDs, and classifies every major capability.
