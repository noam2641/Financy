# Architecture Research and Evidence Report (Deliverable A)

**Program:** AI Trading Decision & Recommendation Platform for US Equities — `ARCHITECTURE_AND_RESEARCH_DEFINITION`, Phase 1 (Evidence Spine)
**Repo audited:** `noam2641/Financy` @ `7c4c659` (docs-only) on branch `claude/trading-platform-audit-iawx0v`; Phase-0 protocol at `5d19997`.
**Research cutoff:** 2026-07-21. **Method:** eight genuinely independent Round-1 research agents (separate context windows, live web search) per `RESEARCH_PROTOCOL_AND_QUESTION_MAP.md`, then a lead-run Round-2 cross-examination.
**Status:** Evidence only. **This report does NOT freeze the architecture, write function contracts, or select a model because research exists.** It separates facts, inferences, owner choices, and empirical TBDs.

> **PHASE 1.5 CORRECTION BANNER (authoritative over any residual wording below).** (1) **Independence:** the eight reviewers were **context-isolated Claude subagents of the same model family/provider** — *not* epistemically independent validators; shared-model priors can cause correlated errors; **agent count does not set evidence grade** (grade derives from source quality/applicability/independent external lines — `SOURCE_EVIDENCE_REGISTER.md`). Any phrase like "genuinely independent" below should be read as "context-isolated." (2) **CX-11 (solo governance cap) is reclassified SINGLE_AGENT_SUPPORTED / UNCONTRADICTED**, and its regulatory basis (SR 11-7/26-2) is **INDUSTRY_BEST_PRACTICE / ANALOGICAL, not legally binding** (`CLAIM_TO_SOURCE_TRACEABILITY.md` CLM-GOV). (3) **Exact deduplicated source counts** supersede the "≈" figures in §3: **55 external / 22 peer-reviewed / 6 official-primary / 9 current (2024–2026) / 9 foundational.** (4) DSR/PBO/CPCV are **applicability-conditioned, not universal Release-0 starting hard gates** (`PHASE_1_EVIDENCE_INTEGRITY_REVIEW.md` §6). (5) "Deterministic MVP" = the **decision policy**; the **forecast model is a learned GBT** (integrity review §7). (6) SIC is **not** a transparent GICS replacement (five-option comparison, integrity review §4). See `PHASE_1_EVIDENCE_INTEGRITY_REVIEW.md`, `SOURCE_EVIDENCE_REGISTER.md`, `CLAIM_TO_SOURCE_TRACEABILITY.md`, `evidence/ROUND_2_CROSS_EXAMINATION.md`, `TWELVE_DOCUMENT_CONSISTENCY_REVIEW.md`, `DOCUMENT_AUTHORITY_AND_CONFLICT_MATRIX.md`.

---

## 1. Executive Findings

1. **The architecture is unusually disciplined; the prior terminal verdict ("development should not begin") was independently RE-SCOPED, not confirmed, by all eight agents.** The evidence-based reframe: *build the rigorous Release-0 edge probe first, gate the edge claim behind added statistical controls, de-scope Release-1A, freeze thresholds, and fix the data-basis and traceability defects* — not a universal stop, and not a fundamental redesign.
2. **The single load-bearing risk is edge-existence, and it is unproven and net-of-cost-fragile** (A1, A5, A7 converge; Grade A/B). At 5/8/14-session horizons the strategy is high-turnover (~100%/week), sitting far above the ~50%/month turnover threshold above which anomalies historically stop surviving costs. This is a *hypothesis to be tested by the Truth Kernel*, not a proven defect — but the spec currently *permits the alpha claim without forcing its disproof*.
3. **The default primary target `sector_excess_return_h` is the most cross-corroborated problem** (A1, A2, A4, A5). It is (a) not factor-neutral (disguised short-term-reversal/beta), (b) un-sourceable point-in-time on the free tier (PIT GICS is MSCI/S&P proprietary) and contradicts R0/R1A's own exclusion of sector modules, and (c) incoherent in the utility formula, which subtracts *absolute* cost from a *relative* return a long-only book cannot harvest.
4. **A learned "super-model" is not justified for the MVP** (A3, A4, A7; Grade A). Deep/sequence/graph/LLM models do not reliably beat well-tuned gradient-boosted-trees/linear on cost-bearing US-equity cross-sections, and the *effective* independent sample (tens-to-low-hundreds of episodes, not the six-figure row count) cannot safely fit a meta-learner. **Recommended MVP decision layer: a frozen, interpretable deterministic penalized-utility policy.**
5. **Retail/free data is not point-in-time-safe by default** (A2, A7; Grade A/B). yfinance back-adjusts prices (future-leak), exposes no vintages (no `SYSTEM_REALISTIC` replay), and drops delisted names (survivorship). *Genuine* free PIT exists for macro (**FRED/ALFRED vintages**) and fundamentals/sector (**SEC EDGAR as-filed accepted-datetime; SIC as a free PIT sector taxonomy**) — if loaders are built correctly.
6. **The evidence base is unverifiable and several R1A subsystems are over-scoped** (A6, A7, A8). The coverage matrix cites ~25 code files absent from the repo; the evidence-dependency graph models zero independent experts in a one-expert R1A; the ~34-entity aggregate, event-sourcing hash-chain, four registries, and full Control Plane are phased too early. The genuinely proportionate parts (modular monolith, small kernel, `feature_snapshot` contract, append-only ledger) must **not** be complexified.
7. **Every numeric go/no-go threshold is TBD**, and the gate statistic is under-powered (single-path walk-forward). The pass must add **Deflated Sharpe Ratio + Probability of Backtest Overfitting + CPCV + a trial registry + factor attribution + an investable net-of-cost benchmark**, all frozen before holdout access.

---

## 2. Research Methodology (recap)

Per Phase 0: eight agents (A1 quant-methodology, A2 PIT-data, A3 model-research, A4 decision/portfolio, A5 execution/microstructure, A6 mlops/governance, A7 adversarial-simplification, A8 requirements/traceability). Round 1 fully independent (no agent saw another's output); each carried a verbatim anti-anchoring instruction and an assigned **contradictory hypothesis** to actively seek. Evidence graded A/B/C/D/UNSUPPORTED; no fabricated citations (unverifiable → UNSUPPORTED). Round 2 cross-examined every BLOCKER/CRITICAL, advanced-model recommendation, provider claim, PIT-safety claim, and economic-value claim.

**Anti-anchoring outcome (material):** the prior six-agent audit was treated as evidence/hypotheses. Independently, A1, A4, A6, and A7 explicitly rejected the *absolutism* of "development should not begin"; none confirmed it verbatim. The convergent, evidence-grounded posture is a **phased, gate-scoped** program — see §6.

---

## 3. Source Inventory

Across the eight agents' graded source entries: **≈55 distinct external sources reviewed; ≈22 peer-reviewed (journal/conference); ≈6 official primary (SEC EDGAR, FRED/ALFRED, Yahoo ToS, MSCI/S&P GICS, Fed/OCC SR 11-7 / SR 26-2); the remainder practitioner/secondary (graded C).** Key literature is consolidated in §8. Honesty note: several official PDFs (NBER, Cambridge/JFQA, SEC, some SSRN) returned HTTP 403 through the environment proxy; affected agents graded corroborated *ranges* at B and *point figures* at C, and marked figure-precision values UNSUPPORTED rather than fabricate — this is recorded per-source in D and E.

---

## 4. Independent-Agent Findings (Round-1 summary)

| Agent | Independent verdict (anti-anchored) | Signature finding(s) |
| --- | --- | --- |
| **A1 quant-methodology** | Reject prior absolutism; build R0 to *test* alpha, gate the *claim* behind 5 controls | No factor attribution (sector-excess ≠ factor-neutral); DSR+trial-registry missing; investable net-of-cost benchmark missing; effective-N/overlap inflation of IC-IR; net edge plausibly ≈0 without cost mitigation |
| **A2 PIT-data** | Contradictory hypothesis CONFIRMED with nuance (free data splits into PIT-capable vs not) | yfinance `auto_adjust` future-leak; no vintages → no SYSTEM_REALISTIC; **PIT GICS proprietary → sector-excess un-sourceable free**; ALFRED + EDGAR-as-filed are genuine free PIT |
| **A3 model-research** | Modeling layer is *well-reasoned*, not the risk; contradictory hypothesis CONFIRMED (Grade A) | Deep/graph/LLM ⊁ GBT/linear net-of-cost; MVP baseline family unnamed → GBT+calibration, elastic-net comparator, LambdaMART challenger, conformal/CQR intervals |
| **A4 decision/portfolio** | Decision layer spec-complete, unimplemented, unfrozen — *not* fatally flawed; contradictory hypothesis SUPPORTED | Pin `expected_return_bps` to absolute-executable; declare λ FROZEN_PRIOR vs FITTED (PBO if fitted); whole-decision calibration; 13-step sizing-precedence chain; learned super-model RESEARCH_ONLY |
| **A5 execution/microstructure** | Realism-incomplete, biases net edge upward; contradictory hypothesis directionally CONFIRMED | One-sided (entry-only) cost model; label≠traded-return; gap-through-stop sizing puts max notional on max gap risk; PROXY open-fill unquantified; capacity/ADV all TBD |
| **A6 mlops/governance** | Philosophy sound & often proportionate; three subsystems phased too early | Reset coverage matrix; two-tier reproducibility (bit-exact symbolic + tolerance numeric); solo-team governance caps at RESEARCH/SHADOW (SR 11-7/26-2); define `environment_hash`; freeze overnight SLA |
| **A7 adversarial-simplification** | Truth-kernel-first CONFIRMED (already latent in spec); re-scope, don't rewrite | Pre-mortem #1 = no edge; phantom-code matrix; evidence-DAG inert in 1-expert R1A; counterfactual factory mis-branded "product identity"; ARCH-A/ARCH-B build order |
| **A8 requirements/traceability** | "Spec complete" ≠ traceable | Canonical REQ-set is clean; companion docs break it: `REQ-LBL`→`REQ-LAB` typo, over-ranges in MOD/DEC/RISK/PORT/VAL, phantom `REQ-DATAQ`/`REQ-CP`; 100% of code citations external |

---

## 5. Round-2 Cross-Examination (convergence & dissent)

Every convergent cluster below was raised independently by ≥2 agents (satisfying the "second-teammate corroboration" rule). Format: **cluster — proposer(s) → corroborator(s) [challenger] — consensus**.

- **CX-1 Edge unproven / net-of-cost fragile.** A1 (Grade A anomaly-decay) → A5 (Grade B turnover-vs-cost), A7 (pre-mortem #1), A4 (effective-N). **Consensus: STRONG.** No agent claims a proven edge; none claims a proven *absence*. Dissent is only of *degree* (A7 weights "no edge" highest; A1 allows a small residual in liquid, low-turnover, factor-neutral form). Resolved as: *edge is the hypothesis the Truth Kernel must test under the added controls of CX-4.*
- **CX-2 Sector-excess primary target.** A2 (un-sourceable PIT / contradicts R0 exclusion) + A1 (not factor-neutral) + A4 (absolute-vs-relative cost incoherence) + A5 (round-trip on relative return). **Consensus: STRONG, four independent angles.** No challenger. Highest-corroborated single problem.
- **CX-3 Label ≠ traded return.** A1 (F-A1-07) + A5 (F03). **Consensus.** Rank/select on an executable (barrier-aware/policy) return or prove IC→PnL concordance.
- **CX-4 Multiple-testing / DSR / PBO / CPCV.** A1 (DSR+registry) + A4 (horizon selection) + A7 (single-path WF insufficient → CPCV). **Consensus: STRONG.** Forbid `PBO_NOT_ESTIMABLE` as a pass; add DSR + trial registry + CPCV, frozen pre-holdout.
- **CX-5 Deterministic MVP; no learned super-model.** A4 (DeMiguel; super-learner oracle) + A3 (GBT>deep net-of-cost, Grade A) + A7 (reject learned weighting R1A). **Consensus: STRONG.** Learned aggregation → gated Research-Factory challenger.
- **CX-6 Retail data not PIT-safe.** A2 (Grade A/B) + A7 (unbudgeted) + A1 (survivorship). **Consensus: STRONG.** yfinance prototyping-only; raw-basis + separate corporate actions; ALFRED for macro; EDGAR as-filed; SIC sector as free PIT.
- **CX-7 Coverage matrix cites phantom code.** A8 (all ~25 refs external) + A6 (reset matrix) + A7 (phantom-implementation) + A2. **Consensus: STRONG.** Reset rows to `DOCUMENTED`/`DESIGNED`.
- **CX-8 Requirement-ID breakage.** A8 (precise per-ID classification) + A1 (`REQ-LBL`). **Consensus.** See H1.
- **CX-9 R1A over-scope.** A7 (evidence-DAG/world-hypotheses/opportunity/KG/LLM/CF-factory) + A6 (event-sourcing/registries/control-plane) + A4 (utility_by_state as overlay) + A3 (uncertainty decomposition). **Consensus: STRONG** on de-scoping — **with an explicit A3/A6/A7 guard: do NOT complexify the genuinely proportionate parts** (modular monolith, 7-component kernel, `feature_snapshot`, append-only ledger + cohort logging).
- **CX-10 Calibration/ECE gate mis-prioritized.** A1 + A3 + A4. **Consensus.** ECE is necessary-not-sufficient; add discrimination + net-economic co-gates; add whole-decision (predicted-utility vs realized-net) calibration.
- **CX-11 Governance independence.** A6 only → **SINGLE_AGENT_SUPPORTED / UNCONTRADICTED** (reclassified from "Consensus"). Basis SR 11-7/26-2 is bank supervisory guidance → **INDUSTRY_BEST_PRACTICE / ANALOGICAL, not legally binding here**. Recommended as **INTERNAL_POLICY_CHOICE**: solo operation caps at RESEARCH/SHADOW; PAPER/LIVE need a named external reviewer + two-person kill-switch. No genuinely independent (non-same-model / human) analysis has corroborated it. (CF-13 inherits this status.)
- **CX-12 Thresholds all TBD.** All agents. **Consensus.** Freeze before holdout in a signed policy bundle; separate "learning thresholds" from locked "acceptance thresholds."

**Documented genuine disagreements (not forced to consensus):** (i) *degree* of alpha pessimism (A7 most pessimistic; A1/A3 allow a narrow survivable regime); (ii) *where* maximalism lives — A3 says not the model layer, A7/A6 locate it in decision-aggregation/ops; these are compatible, not contradictory. No agent contradicts another on a verifiable fact.

---

## 6. Convergent Findings — Ranked, Gate-Scoped

Blocks-which-gate uses the protocol set. **None is a universal blocker to all development**; each names its gate(s).

| ID | Finding (source cluster) | Grade | Blocks |
| --- | --- | --- | --- |
| **CF-1** | Edge-existence unproven & net-of-cost fragile; gate the *claim* behind CX-4 controls (CX-1) | A/B | release_0_acceptance, final_holdout |
| **CF-2** | Sector-excess primary target: confine to ranking; pin utility/cost to absolute-executable basis; re-designate primary (market-excess/absolute) or adopt free-PIT SIC; add factor attribution (CX-2) | A | architecture_freeze, release_0_definition, release_1A |
| **CF-3** | Add DSR + PBO + CPCV + trial registry + investable net-of-cost benchmark; forbid `PBO_NOT_ESTIMABLE` pass (CX-4, CX-1) | A/B | release_0_acceptance, final_holdout |
| **CF-4** | Retail data not PIT-safe: raw-basis ingestion, separate versioned corporate actions, survivorship-safe PIT universe, ALFRED macro, EDGAR as-filed; SYSTEM_REALISTIC barred pre-go-live (CX-6) | A/B | architecture_freeze, release_0_acceptance, shadow |
| **CF-5** | Deterministic penalized-utility policy for MVP; λ FROZEN_PRIOR; learned super-model RESEARCH_ONLY (CX-5) | A | release_1A (design), architecture_freeze |
| **CF-6** | Label≠traded-return: rank/select on executable objective or prove IC→PnL concordance (CX-3) | A | release_0_acceptance, release_1A |
| **CF-7** | Round-trip (two-sided) cost model incl. exit/close-auction leg; quantify PROXY open-fill; freeze capacity/ADV caps; gap-through-stop sizing (CX-6/execution) | A/B | release_0_definition, release_1A, paper, live |
| **CF-8** | De-scope R1A to ~10-entity core; defer evidence-DAG/world-hypotheses/opportunity/KG/LLM/CF-factory; keep append-only ledger + cohort logging + `feature_snapshot` (CX-9) | A/B | release_1A |
| **CF-9** | Reset coverage matrix to repo-truth; classify code refs as EXTERNAL_PROTOTYPE_REFERENCE (CX-7) | A | release_0_acceptance |
| **CF-10** | Fix companion-doc REQ-ID references per H1 (CX-8) | A | release_1A (traceability), release_0_definition |
| **CF-11** | Whole-decision calibration + discrimination + net-economic co-gates; ECE not sole gate (CX-10) | B | release_1A, release_0_acceptance |
| **CF-12** | Freeze all TBD thresholds pre-holdout; two-tier reproducibility; define `environment_hash`; overnight SLA (CX-12, A6) | A | final_holdout, shadow, paper, live |
| **CF-13** | Governance: solo caps at RESEARCH/SHADOW; external validation + two-person kill-switch before PAPER/LIVE (CX-11) | A | paper, live |

---

## 7. Disputed / Mixed-Evidence Findings (carried forward, not resolved here)

- **Degree of alpha survivability.** Mixed by *emphasis*, not fact. Empirical resolution = the CF-1/CF-3 baseline study on a liquid, low-turnover, factor-neutral universe. → Phase-2 EMPIRICAL_TBD.
- **Whether sector-excess can be retained at all.** A2 offers a free-PIT SIC substitute; A1/A4 would confine sector-excess to ranking only. Owner decision (Phase 2), not an evidence gap.
- **Kelly-Malamud-Zhou "Virtue of Complexity" (Grade A)** is the one serious pro-complexity result; A3 shows it addresses *market timing*, not cost-bearing cross-sectional selection, so it does not license deep models here. Recorded as a bounded, non-transferring counter-result.

---

## 8. Literature Review (consolidated, by theme; grades as assigned by agents)

**Anomaly decay & net-of-cost survival (edge existence).** McLean & Pontiff 2016 *JF* (−26% OOS, −58% post-pub) [A]; Chen & Velikov 2023 *JFQA* (post-2005 net ≈ −1 to +4 bp/mo) [A]; Novy-Marx & Velikov 2016 *RFS* (only <50%/mo turnover survives; 20–57 bp/trade) [A/B]; Hou-Xue-Zhang 2020 *RFS* (65% fail t>1.96 with microcaps out) [A]; Avramov-Chordia-Goyal 2006 *JF* (short-horizon reversal < costs) [A]; Jegadeesh 1990 *JF* (short-term reversal) [A].
**Multiple testing & backtest overfitting.** Harvey-Liu-Zhu 2016 *RFS* (t>3.0) [A]; Bailey & López de Prado 2014 Deflated Sharpe [B]; Bailey et al. Probability of Backtest Overfitting / CSCV [A]; CPCV vs single-path WF [B]; López de Prado *AFML* purge/embargo/uniqueness [C].
**Model families on tabular finance.** Gu-Kelly-Xiu 2020 *RFS* (trees/shallow-NN best; gains from nonlinear interactions) [A]; Avramov-Cheng-Metzker 2023 *Mgmt Sci* (ML edge concentrated in hard-to-arbitrage; attenuates after costs) [A]; Grinsztajn 2022 *NeurIPS* + Shwartz-Ziv & Armon 2022 (GBDT > DL on tabular) [A]; Kelly-Malamud-Zhou 2024 *JF* (virtue of complexity — *market timing only*) [A, non-transferring]; Poh et al. 2021 *JFDS* (learning-to-rank beats predict-then-sort) [B].
**Calibration & intervals.** Niculescu-Mizil & Caruana 2005 *ICML* (GBT miscalibrated; Platt small-n, isotonic large-n) [A]; Romano-Patterson-Candès 2019 *NeurIPS* CQR [A]; conformal-for-time-series (exchangeability violated; block/adaptive fixes) [A/B].
**Portfolio construction.** DeMiguel-Garlappi-Uppal 2009 *RFS* (1/N beats optimizers OOS) [B]; super-learner oracle property (needs large n vs K) [B/C].
**Execution & microstructure.** Frazzini-Israel-Moskowitz (live large-cap ~6 bp/rebalance; momentum capacity ~$2B) [B]; Patton-Weller *JFE* (paper vs realized wedge) [B]; JFQA closing/opening-auction impact benchmark [B]; Corwin-Schultz 2012 *JF* high-low spread estimator [B]; Almgren et al. 2005 square-root impact [B].
**Data/PIT (official).** SEC EDGAR accepted-datetime / as-filed vs `companyfacts` restated [A]; FRED/ALFRED vintages vs latest-revised [A/B]; MSCI/S&P GICS proprietary + paid PIT history [A]; Yahoo API ToS + yfinance `auto_adjust` default [B].
**MLOps/governance.** Fed/OCC SR 11-7 (2011) → **SR 26-2 (April 2026)** effective-challenge/independent-validation [A]; GPU/BLAS float non-associativity → bit-exact needs determinism flags [B]; feature-store schema-parity ≠ value/freshness parity [B]; Fowler MonolithFirst / YAGNI [B/C].

---

## 9. Architecture Implications (input to Phase 2 decisions — not decisions)

1. **Build order:** ARCH-A "Rigorous Edge Probe" before any §3.7–3.10 / §23 work; §3.7–3.10 and §23 treated as a *frozen, un-built appendix* until ARCH-A clears its gate. (A7, A1, A6.)
2. **Objective/basis:** ranking in excess-space, sizing/utility/cost in absolute-executable-space; sector-excess never enters the bps net-edge subtraction. (A4, A1, A5.)
3. **Decision layer:** frozen deterministic penalized-utility policy + deterministic permission + hard-blocker override + abstention-first + risk-budget-then-allocator sizing (13-step chain, A4). Learned aggregation is a gated challenger.
4. **Models:** GBT + isotonic/Platt calibration (primary), elastic-net + per-date cross-sectional regression (comparators), conformal/CQR + quantile regression (intervals), LambdaMART (first challenger); all deep/graph/LLM = R4 challengers. (A3.)
5. **Data/validation:** raw-basis prices + versioned corporate actions; survivorship-safe PIT universe; free PIT via ALFRED (macro) + EDGAR as-filed (fundamentals) + SIC (sector); CPCV + purged/embargoed WF + DSR + PBO + factor attribution + investable net-of-cost benchmark; INFORMATION_THEORETIC replay only pre-go-live. (A2, A1, A5.)
6. **Ops/governance:** minimal signed `runtime_manifest` + capability-health; append-only ledger (defer hash-chain/outbox to shadow); MLflow-style registry over four bespoke registries; two-tier reproducibility; solo cap at RESEARCH/SHADOW. (A6.)

---

## 10. Capability Classification Roll-Up

`MVP_REQUIRED`: canonical OHLCV adapter; raw-basis + corporate-action versioning; survivorship-safe PIT universe; 5/8/14 matured labels (executable-aware); purged+embargoed CPCV + DSR + PBO + trial registry; factor attribution; investable net-of-cost benchmark; `feature_snapshot`/schema-parity + value-parity; GBT + calibration; elastic-net/cross-sectional comparators; conformal/CQR intervals; deterministic penalized-utility policy; permission score; hard blockers; abstention/NO_ACTION; risk-budget sizing + caps; append-only ledger + cohort logging; minimal runtime_manifest + capability-health.
`MVP_OPTIONAL`: candlestick pack; random forests/GAM-EBM (interpretability); drift monitors (→REQUIRED by 2A); ALFRED macro (required-if-macro).
`RESEARCH_CHALLENGER`: LambdaMART; stacking; SIC-sector proxy; Bayesian decision model (R2+ successor); HMM/regime.
`DEFERRED`: FinBERT/news (2A); knowledge graph/GNN (2A/4); evidence-dependency graph (2A, needs ≥2 experts); world-model hypotheses beyond a deterministic regime vector (2A); opportunity-memory analytics (2A); counterfactual factory (2B); LSTM/TCN/Transformer/TFT/multimodal (R4); event-sourcing hash-chain + outbox + full Control Plane (shadow/R3).
`REJECTED (for MVP core)`: learned super-model / adaptive expert weighting as a decision-layer dependency; LLM in DECISION_RUNTIME; full mean-variance optimizer (falls back to greedy risk-budget); online feature-store service pre-paper.

---

## 11. Unresolved Empirical Questions (→ Phase 2 `OPEN_DECISIONS_ASSUMPTIONS_AND_EXPERIMENTS.md`)

Each needs a later experiment + decision rule + provisional default:
1. Does a factor-neutral, net-of-cost, DSR-adjusted cross-sectional edge survive on a liquid, low-turnover universe at 14 sessions? (default: assume no → `BLOCKED_NO_EDGE` unless cleared)
2. Does fixed-horizon IC correlate with post-barrier realized PnL well enough to rank on the label? (default: rank on executable objective)
3. What round-trip cost band does the target universe actually incur, and does it exceed gross edge? (default: use conservative literature bands; freeze `maximum_spread`/ADV caps)
4. Is a free-PIT SIC sector benchmark good enough to retain a sector-relative objective, or must the primary target become market-excess/absolute? (default: absolute-executable primary; sector-excess ranking-only)
5. What are the frozen values for the 8 TBD readiness thresholds, set from external priors before holdout? (default: conservative priors, signed)

---

## 12. Boundaries Honored & Phase-2 Preview

No architecture was frozen; no function or file contracts were written; no model was selected because research exists (each selection carries a kill criterion). Phase 2 will convert these convergent findings and unresolved questions into the **Architecture Decision Register (F)** and **Open-Decisions/Experiments (G)**, grouping the highest-leverage items into `OWNER_DECISION_PACKETS`. Phase 3 (System Architecture Spec v5 DRAFT) follows only after the architecture-relevant decisions are approved or explicitly labelled `EMPIRICAL_TBD` with a provisional default and decision rule. Canonical v4.6 remains unmodified.
