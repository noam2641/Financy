# Model and Method Evidence Matrix (Deliverable D)

**Program:** AI Trading Decision Platform for US Equities — Phase 1 (Evidence Spine). Sources: agents A3 (model-research), A4 (decision/portfolio), A1 (validation methods), with A5 (cost) on economic-value gating.
**Research cutoff:** 2026-07-21. **Status:** Evidence + graded recommendation only. **No model is selected because research exists; every learned component carries a kill criterion and a simpler comparator.** Grades A/B/C/D/UNSUPPORTED per Phase-0 rules. Statistical significance ≠ economic tradeability.

Status vocabulary: `MVP_REQUIRED` · `MVP_OPTIONAL` · `RESEARCH_CHALLENGER` · `DEFERRED` · `REJECTED (for MVP core)`.

---

## 1. Decision-Layer Options (the "super-model" question)

Effective independent sample (A4): with 14-session overlapping labels (avg uniqueness ≈ 1/14), cross-sectional factor dependence, and single-digit independent regimes/yr, the sample governing decision-layer parameters is **tens-to-low-hundreds of independent episodes**, not the six-figure row count. This governs every row below.

| Option | Use case | Evidence (grade) | Benefit | Risk / failure mode | PIT req | Sample req | Complexity | Recommendation | Kill criterion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Deterministic penalized-utility policy** (REQ-DEC-001) | MVP decision kernel | DeMiguel-Garlappi-Uppal 2009 [B]; spec internal [A] | Reproducible, auditable, ~5 hand-set λ, no meta-overfit | Mis-set λ / wrong return basis → mis-scaled utility | Consumes PIT forecasts | Minimal (λ frozen prior) | Low | **MVP_REQUIRED** | Fails to beat naive+technical comparator net-of-cost over required WF windows → `BLOCKED_NO_EDGE` |
| **Learned stacking / super-learner** | Combine experts/base learners | Super-learner oracle needs K≤n^q, large n [B/C]; Harvey-Liu-Zhu [A] | Captures nonlinear complementarity *if* data-rich | Meta-features leak across purge; overfits at this effective-n; raises multiple-testing bar | Nested purged CV mandatory | High (absent here) | High | **REJECTED (for MVP core)** / R4 challenger | Fails to beat best single base member AND frozen deterministic policy OOS under DSR/PBO |
| **Mixture-of-experts (gating)** | Regime-conditioned experts | As stacking, worse (extra params to calibrate) [B/C] | Regime adaptivity in theory | Gate overfits few regime transitions; collides with sample split | Nested purged CV | Very high | Very high | **DEFERRED (R4 fusion)** | Gate weights unstable across WF/regimes or no DSR-corrected lift over policy |
| **Bayesian decision model** | Priors-with-uncertainty λ/hurdles; state-weighted utility | Regularization-under-small-n rationale [C] | Principled uncertainty; graceful small-n; natural `worst_plausible_state_utility` | Mis-calibrated posterior; priors too tight = policy-with-overhead; replay reproducibility | Reproducible sampling | Moderate | Med-High | **RESEARCH_CHALLENGER (R2+ successor)** | Fails whole-decision calibration, or priors never update, or non-reproducible under replay |
| **Constrained optimization (MV/utility optimizer)** | Portfolio weights | DeMiguel 2009: 1/N beats optimizers OOS [B] | Theoretical optimality | Error-maximization, corner solutions, turnover | Covariance PIT | High | High | **REJECTED for weights** (greedy risk-budget allocation `MVP_REQUIRED`) | Optimized alloc fails to beat equal-risk-contribution / 1-over-N net of turnover → fall back to greedy |

**Consensus (A3+A4+A7):** MVP = deterministic penalized-utility policy; a learned super-model is neither necessary, trainable, nor testable at this effective sample size. Keep learned aggregation as a gated Research-Factory `DECISION_POLICY_CHALLENGER` (REQ-LEARN-009 / REQ-REL4-002).

---

## 2. Predictive Model Families (tabular US-equity daily-swing cross-section)

Grade = strength of evidence that the family adds *net-of-cost OOS value on this problem*.

| Family | Contribution | Target | Min/effective data | Status | Grade | Key evidence | Kill criterion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Regularized linear / logistic | Naive interpretable comparator | sector-excess return; P(>hurdle) | low | **MVP_REQUIRED** (comparator) | A | Gu-Kelly-Xiu 2020 | Fails to beat past-return sort net-of-cost |
| Cross-sectional (Fama-MacBeth-style) regression | Per-date coef stability, IC | return_h | low | **MVP_REQUIRED** | A | Standard EAP | Mean daily IC not significant OOS (effective-N) |
| **Gradient-boosted trees (LightGBM/XGBoost)** | Primary MVP predictor; nonlinear interactions | return_h + P(>hurdle) | med | **MVP_REQUIRED (primary)** | A | Gu-Kelly-Xiu 2020; Grinsztajn 2022; Shwartz-Ziv & Armon 2022 | Does not beat elastic-net + past-return net-of-cost |
| Random forests | Robust bagged alt | return_h | med | **MVP_OPTIONAL** | B | Niculescu-Mizil & Caruana 2005 | No stability/IC edge over GBT |
| GAM / Explainable Boosting Machine | Interpretable near-GBT; explanation layer | return_h contributions | med | **MVP_OPTIONAL / interpretability** | B | Lou/Caruana InterpretML | Accuracy gap to GBT not offset by interpretability need |
| **Calibrated classifiers (Platt/isotonic)** | Usable probabilities for sizing/abstention | P(pos/cover-cost/hurdle)_h | ≥~1–2k calib rows | **MVP_REQUIRED** | A | Niculescu-Mizil & Caruana 2005 (GBT natively miscalibrated) | ECE not improved / reliability slope ≠ 1 |
| **Quantile regression (incl. GBT-quantile)** | Downside/upside quantiles, intervals | q_low/q_high return_h | med | **MVP_REQUIRED** (interval source) | A | standard | Empirical coverage ≠ nominal |
| **Conformal / CQR** | Distribution-free interval coverage | prediction interval, coverage_error | holdout calib set | **MVP_REQUIRED** (interval method) | A | Romano-Patterson-Candès 2019; conformal-for-TS | Time-series coverage fails after block validation |
| Learning-to-rank (LambdaMART) | Directly optimize cross-sectional ordering | pairwise/listwise order | med | **RESEARCH_CHALLENGER (R1A/R2)** | B | Poh et al. 2021 | No NDCG@K / rank-IC gain over GBT-regress net-of-cost |
| Survival / hazard | Time-to-stop/target | terminal-event timing | med | **DEFERRED (R2+)** | C | — | No lift over ATR/quantile stop policy |
| HMM / regime classifiers | Market-state hypotheses | regime prob vector | med (long history) | **RESEARCH_CHALLENGER / DEFERRED** | B | regime-switching literature; spurious-regime risk | Unstable OOS regimes; no conditional-utility gain |
| LSTM / GRU / TCN | Temporal encoder challenger | return_h sequence | high | **DEFERRED (R4 challenger)** | C (for beating GBT) | Grinsztajn; Avramov-Cheng-Metzker | Loses to tabular baseline net-of-cost (REQ-CONV-MOD-005) |
| Transformer / TFT | Attention/multi-horizon challenger | joint 5/8/14 return_h | very high | **DEFERRED (R4)** | C | TFT cluster (no net-of-cost vs LightGBM) | No net-of-cost win vs GBT |
| FinBERT / financial LMs | Text-sentiment evidence feature | sentiment prob → feature | high (licensed text) | **DEFERRED (R2A) / replaceable baseline** | C | FinBERT return-pred cluster (weak, cost-blind) | No marginal decision value net-of-cost; licensing fails |
| Graph neural networks | Relational/peer propagation | return_h w/ graph | very high | **DEFERRED (R4)** | C/D | GNN cluster (weak baselines, no costs) | No gain over graph-*feature* baseline |
| Knowledge graph (operational) | Entity resolution, dedup, exposure | non-predictive ops | med | **MVP_OPTIONAL (R2A ops, not model)** | B | spec REQ-DOM-034 | Non-GNN-first correct |
| Multimodal fusion | Combine price+text+graph | return_h | very high | **DEFERRED (R4)** | D | — | Each modality must pass ablation first |
| Stacking / bagging | Combine base learners / variance reduction | return_h | med | **RESEARCH_CHALLENGER / MVP_OPTIONAL(bagging)** | B | super-learner oracle | Meta-model overfits; no OOS gain |
| Deep ensembles | Epistemic uncertainty for NN | return_h + disagreement | high | **DEFERRED (R4)** | B (stability) | — | Only if NN challenger already competitive |
| Causal / uplift | Action-value / treatment effect | uplift of acting vs not | high (needs IV/experiment) | **DEFERRED / RESEARCH** | C | uplift surveys (no trading identification) | No identification strategy → not decision-grade |
| Anomaly / drift (ADWIN/DDM/PSI) | Monitoring, not forecasting | distribution-shift alarm | streaming | **MVP_OPTIONAL → REQUIRED by 2A** | B | drift-detector literature | False-alarm rate makes it ignored |

**Contradictory hypothesis (deep/graph/LLM ⊁ GBT/linear net-of-cost) — CONFIRMED at Grade A** (Gu-Kelly-Xiu; Avramov-Cheng-Metzker; Grinsztajn; Shwartz-Ziv & Armon). Sole Grade-A contrarian — Kelly-Malamud-Zhou 2024 "Virtue of Complexity" — concerns **market timing**, not cost-bearing cross-sectional selection, and does not transfer.

---

## 3. Validation & Statistical-Control Methods

| Method | Use case | Evidence (grade) | Status | Kill / gate criterion |
| --- | --- | --- | --- | --- |
| Purged walk-forward + embargo | Leakage-safe folds | López de Prado AFML [C]; spec REQ-VAL-001/002 [A] | **MVP_REQUIRED** | Any train-label window overlaps test in fold-manifest test |
| **Combinatorial Purged CV (CPCV)** | Multi-path robustness | CPCV-vs-WF studies [B] | **MVP_REQUIRED (upgrade)** | Single-path WF alone insufficient (high path-variance) |
| Date-grouped cross-sectional IC / IC-IR | Ranking discrimination | spec REQ-VAL-005 [A] | **MVP_REQUIRED** | Pooled global Spearman substituted, or effective-N IC-IR CI includes 0 |
| Effective-sample / overlap accounting | Honest power | Boudoukh-Israel-Richardson; overlapping-obs inference [B] | **MVP_REQUIRED** | Promote only on conservative (non-overlapping) IC-IR |
| **Deflated Sharpe Ratio + trial registry** | Multiple-testing deflation | Bailey & López de Prado 2014 [B]; Harvey-Liu-Zhu 2016 [A] | **MVP_REQUIRED** | DSR-adjusted Sharpe/IC-IR ≤ 0 on holdout, or N not logged |
| **Probability of Backtest Overfitting (CSCV)** | Rank-instability | Bailey et al. [A]; spec REQ-VAL-008 [A] | **MVP_REQUIRED** | PBO > 0.5; `PBO_NOT_ESTIMABLE` forbidden as a pass |
| Block bootstrap CIs (serial-dep adj.) | Correct inference | spec REQ-VAL-006 [A] | **MVP_REQUIRED** | Block length < max horizon |
| **Factor attribution / neutralization** | Alpha ≠ beta test | Harvey-Liu-Zhu; Avramov-Chordia-Goyal [A] | **MVP_REQUIRED** | Residual net-alpha t-stat < pre-registered hurdle after (Mkt,SMB,HML,UMD,ST-Rev,BAB) |
| **Investable net-of-cost benchmark** | Value vs passive | Grinold-Kahn [B]; Chen-Velikov [A] | **MVP_REQUIRED** | Beta-adjusted net return ≤ buy-and-hold SPY / sector-basket net |
| Whole-decision calibration | Utility realism | Niculescu-Mizil & Caruana [B] | **MVP_REQUIRED** | Realized-net vs predicted-`risk_adjusted_utility_bps` slope ≉ 1 |
| Monte Carlo report | Robustness | spec REQ-VAL-007 [A] | **MVP_OPTIONAL** | Non-deterministic seed policy |
| Capacity + half-life + churn | Net-of-cost decisive vars | Novy-Marx-Velikov; Chen-Velikov [A] | **MVP_REQUIRED (upgrade SHOULD→MUST)** | Capacity below AUM need or half-life < rebalance interval |

---

## 4. Every-Advanced-Model Checklist (per Phase-0 §12)

For each advanced (learned) candidate the following must be answered before promotion; unanswered ⇒ stays `DEFERRED`/`RESEARCH_CHALLENGER`:
1. **What does it add beyond the best simpler model?** (must be a measured net-of-cost, DSR-adjusted increment over GBT+calibration / deterministic policy)
2. **How is incremental value isolated?** (ablation under identical PIT/cost/CPCV rules — REQ-CONV-MOD-006)
3. **How is leakage prevented?** (out-of-fold meta-features; nested purged CV; calibration set obeys purge/embargo)
4. **How is overfitting measured?** (PBO at the model/meta level; DSR with the actual trial count)
5. **What evidence causes rejection?** (the kill criterion in §2/§3)

---

## 5. Top Recommendations (D)

1. **GBT + isotonic/Platt calibration = MVP_REQUIRED primary predictor** (natively miscalibrated → calibration mandatory, not optional).
2. **Elastic-net + per-date cross-sectional regression = MVP_REQUIRED comparators** (the honest naive baseline the R0 gate needs).
3. **Conformal/CQR + quantile regression = MVP_REQUIRED intervals**, coverage validated under time-series (non-exchangeable) conditions with purge/embargo-respecting calibration sets (shared leakage watch-item with E).
4. **Deterministic penalized-utility policy = MVP decision kernel**; λ FROZEN_PRIOR; learned super-model/MoE = gated R4 challengers only.
5. **CPCV + DSR + PBO + trial registry + factor attribution + investable net-of-cost benchmark = MVP_REQUIRED validation stack**, all frozen before holdout; single-path walk-forward alone is insufficient.
6. **LambdaMART = top challenger** (decision object is ordering); **all deep/graph/LLM = R4 challengers**, kill criterion = fail to beat the calibrated tabular baseline net-of-cost under identical PIT/CPCV rules.
