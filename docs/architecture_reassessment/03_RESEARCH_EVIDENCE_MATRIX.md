# 03 — Research Evidence Matrix

**Artifact type:** source-to-decision evidence matrix (Phase 2 output).
**Primary source:** specialist `financial-ml-literature-research` (read-only web research;
access date **2026-07-22** for all sources). The lead reproduces the specialist's
verified findings faithfully and adds no citations of its own.
**Integrity rules honored:** EVIDENCE (empirical, ideally replicated) is separated from
ARCHITECTURAL INFERENCE; **[REPLICATED]** vs **[SINGLE-STUDY]** is marked; every source's
title/authors/year/venue was confirmed via search; paywalled full-texts are flagged where
characterization rests on abstract/secondary text; **no source was invented.** A compact
bibliography is in `17_RESEARCH_REFERENCES.md`.

---

## 1. Evidence synthesis by architectural question (condensed)

- **Q1 Cross-sectional ML forecasting.** ML (trees/shallow NN) ≈2× linear OOS R² from nonlinearity/interactions (Gu-Kelly-Xiu 2020); GBT ≥ deep nets on medium tabular data **[REPLICATED]** (Grinsztajn 2022; Shwartz-Ziv-Armon 2022) → **GBT-first core**. Gains are gross/value-weighted and concentrate in microcaps/high-friction states that fade under costs (Avramov-Cheng-Metzker 2023). "Virtue of complexity" (Kelly-Malamud-Zhou 2024) is **aggregate-timing, contested** (Nagel 2025) — does NOT transfer to the long-only cross-section.
- **Q2 Anomaly decay & net-of-cost fragility** — **best-replicated, decision-critical.** ~58% post-publication decay (McLean-Pontiff 2016); 65% of anomalies fail |t|>1.96 (Hou-Xue-Zhang 2020); <~50%/mo turnover survives costs (Novy-Marx-Velikov 2016); net avg anomaly ~4 bps/mo, combos ~20 (Chen-Velikov 2023). → turnover/cost are first-class objectives; discount gross alpha heavily. Does NOT prove *no* net alpha exists.
- **Q3 Validation for dependent data.** Purged K-fold+embargo, CPCV, PBO/CSCV, Deflated Sharpe (López de Prado 2018; Bailey et al. 2017; Bailey-López de Prado 2014) — logically sound, directly applicable, but largely **methodological**; independent proof they prevent live overfitting is thin (Arian et al. 2024 = single synthetic study). Treat as necessary hygiene + strict final holdout + effective-sample (block-bootstrap) accounting.
- **Q4 Calibration & conformal under shift.** GBT miscalibrated, fixable by Platt/isotonic **[REPLICATED, IID]** (Niculescu-Mizil-Caruana 2005). CQR gives coverage **under exchangeability** (Romano et al. 2019); coverage degrades with distance from exchangeability (Barber et al. 2023); adaptive conformal restores only **long-run average** coverage (Gibbs-Candès 2021). → calibration is achievable *on-average/in-regime*, NOT per-decision across regime breaks; barrier/touch & time-to-event calibration is academically **unvalidated**.
- **Q5 Sequence models.** Deep recurrence not shown necessary (Gu-Kelly-Xiu); linear DLinear beats TS Transformers on benchmarks **[REPLICATED in TS]** (Zeng et al. 2023); TFT credible but **no net-of-cost finance superiority over GBT shown**. Bidirectional models = look-ahead trap. → sequence models are a candidate encoder with a high, mostly-unmet burden of proof.
- **Q6 Text/NLP.** News carries **short-horizon, reversal-flavored, cost-fragile** signal (Tetlock 2007); FinBERT/BloombergGPT help NLP tasks (≠ alpha). LLM alignment is breakable (Zou et al. 2023) → **prompt-injection/source-poisoning are live threats**; treat LLM-derived features as attackable.
- **Q7 Graph/relational.** Graph relations *can* improve ranking (Feng et al. 2019, **single-study, gross-of-cost, no peer-aggregate baseline**); but GICS already explains co-movement well (Bhojraj-Lee-Oler 2003) → GNNs are **unproven net-positive** vs PIT peer aggregates; construction is leakage-prone (must be strictly as-of).
- **Q8 Analog/retrieval/RAG.** Thinnest base (FinSeer 2025, single-study). **No replicated evidence** of net-of-cost cross-sectional alpha; retrieval leakage is first-order. → experimental evidence-surfacing aid with as-of filtering, not a calibrated probability source.
- **Q9 Barrier/survival.** Triple-barrier + meta-labeling is the natural swing-decision geometry (López de Prado 2018), but labels are **highly sensitive to barrier widths**, time-barrier censors near-misses; MFE/MAE/first-passage more realistic but little replicated calibration evidence. → barrier params are researcher DoF; freeze pre-hoc and stress-test.
- **Q10 Selective prediction / ABSTAIN.** SelectiveNet reject-option and Chow's rule are principled (Geifman-El-Yaniv 2019), but abstention rides the same calibration that Q4 shows is fragile out-of-regime → well-motivated, low-regret, but **average-case** guarantees; be conservative.
- **Q11 Portfolio.** No optimizer reliably beats 1/N OOS **[REPLICATED]** (DeMiguel-Garlappi-Uppal 2009); HRP better OOS variance (López de Prado 2016, sim-based, single-ish). → **deterministic constrained allocation** on small samples; turnover control is a *return* driver.
- **Q12 Multimodal fusion.** Taxonomy solid, missing-modality a core challenge (Baltrušaitis et al. 2018); **no finance net-alpha benefit demonstrated** → explicit missing-modality handling justified, but fusion must beat GBT-on-concatenated-features.
- **Q13 Social/attention.** Retail attention → short-run rise then **reversal within the year** (Da-Engelberg-Gao 2011); Telegram pump-and-dump empirically dissected (Xu-Livshits 2019). → double-edged: predictive but manipulable and reversal-prone; treat spikes as **risk/ABSTAIN flags** as much as buy signals.
- **Q14 Macro/regime.** Regimes shift correlations/allocation (Ang-Bekaert 2002), but detection is lagged/revision-prone; use **PIT macro vintages** (FRED/ALFRED) and soft/probabilistic regime weights, not hard switches.
- **Q15 PIT data reality.** Free-PIT is real for **fundamentals** (SEC EDGAR acceptance timestamps, 5:30pm ET cutoff, ~2-min dissemination) and **macro** (FRED/ALFRED vintages); free signal data exists (Chen-Zimmermann 2022). **NOT free-PIT:** survivorship-safe index constituents and **GICS** (licensed). yfinance has documented look-ahead/survivorship problems → **universe construction & sector classification are the hard, not-free-PIT gaps** and the most likely silent look-ahead.

## 2. Source-to-decision evidence matrix

Legend: **E** empirical · **INF** inference basis · **R** replicated · **S** single/narrow. All **VERIFIED** on 2026-07-22 (title/authors/year/venue confirmed); *Content: abstract* = characterization from abstract/secondary text (paywall).

| # | Source | Locator | Q | Supports (type) | Does NOT prove / limits | Relevance |
|---|---|---|---|---|---|---|
| 1 | Gu, Kelly, Xiu 2020 — Empirical Asset Pricing via ML — RFS 33(5) | 10.1093/rfs/hhaa009; NBER w25398 | 1,5 | ML ~2× linear OOS R²; nonlinearity/interactions (E,R) | gross, value-weighted; not net-of-cost | GBT/shallow-NN core > linear |
| 2 | Grinsztajn et al. 2022 — Why trees beat DL on tabular — NeurIPS D&B | arXiv 2207.08815 | 1 | GBT ≥ DL on medium tabular (E,R) | not finance-specific | cross-section = wide tabular → GBT-first |
| 3 | Shwartz-Ziv, Armon 2022 — DL Is Not All You Need — Information Fusion 81 | 10.1016/j.inffus.2021.11.011 | 1 | XGBoost ≥ DL, easier tuning (E,R) | benchmark datasets | reinforces GBT default |
| 4 | Kelly, Malamud, Zhou 2024 — Virtue of Complexity — J. Finance 79(1) | 10.1111/jofi.13298; NBER w30217 | 1 | over-param aids market timing (E,S) | aggregate timing, NOT cross-section; contested | cautions vs assuming complexity transfers |
| 5 | Nagel 2025 — Seemingly Virtuous Complexity — SSRN | SSRN 5386615 | 1 | VoC ≈ vol-timed momentum (E,S critique) | working paper | tempers VoC; supports simpler core |
| 6 | Avramov, Cheng, Metzker 2023 — ML vs Economic Restrictions — Mgmt Science 69(5) | 10.1287/mnsc.2022.4449 | 1,2 | ML profit in microcaps/distress; fades w/ costs (E,R-consistent) | not "ML worthless" | core net-of-cost caution |
| 7 | McLean, Pontiff 2016 — Does Research Destroy Predictability? — J. Finance 71(1) | 10.1111/jofi.12365 | 2 | 26% OOS / 58% post-pub decay (E,R) | average effect | discount published signals |
| 8 | Hou, Xue, Zhang 2020 — Replicating Anomalies — RFS 33(5) | 10.1093/rfs/hhy131; NBER w23394 | 2 | 65% fail |t|>1.96 (NYSE, VW) (E,R) | microcap-treatment debated | universe/weighting decisive |
| 9 | Harvey, Liu, Zhu 2016 — …Cross-Section of Expected Returns — RFS 29(1) | 10.1093/rfs/hhv059; NBER w20592 | 2,3 | multiple-testing → t>3.0 (E/INF) | guideline, correlation-dependent | significance bar for any signal |
| 10 | Novy-Marx, Velikov 2016 — Taxonomy of Anomalies & Trading Costs — RFS 29(1) | 10.1093/rfs/hhv063; NBER w20721 | 2,11 | <~50%/mo turnover survives costs (E,R) | cost era-specific | turnover budget first-class |
| 11 | Chen, Velikov 2023 — Zeroing in on Expected Returns of Anomalies — JFQA 58(3) | 10.1017/S0022109022000874 | 2 | net avg ~4 bps/mo; combos ~20 (E,R) | long-short; modern spreads | realistic net-alpha ceiling |
| 12 | Nikolopoulos 2026 — Spurious Predictability in Financial ML — arXiv | arXiv 2604.15531 | 2,3 | spec-search fabricates significance (E,S) | recent, unreviewed | falsification-audit idea (*Content: abstract*) |
| 13 | López de Prado 2018 — Advances in Financial ML — Wiley | ISBN 978-1-119-48208-6 | 3,9 | purged CV+embargo, CPCV, triple-barrier, meta-labeling (INF) | methodological; barrier params = DoF | validation + labeling blueprint |
| 14 | Bailey, Borwein, LdP, Zhu 2017 — Probability of Backtest Overfitting — J. Comp. Finance 20(4) | SSRN 2326253 | 3 | CSCV/PBO estimates overfit prob (INF/E) | strategy-set dependent | quantify overfitting |
| 15 | Bailey, López de Prado 2014 — Deflated Sharpe Ratio — J. Portfolio Mgmt 40(5) | SSRN 2460551 | 3 | Sharpe adj for trials/non-normality/length (INF) | needs honest trial count | deflate reported Sharpe |
| 16 | Arian, Norouzi, Seco 2024/25 — Backtest Overfitting in the ML Era — ESWA | SSRN 4686376 | 3 | CPCV > walk-forward on PBO/DSR (E,S) | single synthetic study | empirical support for CPCV (*Content: abstract*) |
| 17 | Niculescu-Mizil, Caruana 2005 — Predicting Good Probabilities — ICML | 10.1145/1102351.1102430 | 4 | GBT miscalibrated; Platt/isotonic fix (E,R) | IID | calibrate GBT before decisions |
| 18 | Romano, Patterson, Candès 2019 — Conformalized Quantile Regression — NeurIPS 32 | arXiv 1905.03222 | 4 | distribution-free intervals under exchangeability (E) | exchangeability required | regression prediction intervals |
| 19 | Gibbs, Candès 2021 — Adaptive Conformal Inference — NeurIPS 34 | arXiv 2106.00170 | 4,14 | online long-run coverage under shift (E) | only average, not conditional | online recalibration under drift |
| 20 | Barber, Candès, Ramdas, Tibshirani 2023 — Conformal Beyond Exchangeability — Ann. Statistics 51(2) | 10.1214/23-AOS2276 | 4 | coverage loss ∝ distance from exchangeability (E) | weaker under non-exchangeability | formal limit on TS conformal |
| 21 | Lim et al. 2021 — Temporal Fusion Transformers — Int. J. Forecasting 37(4) | 10.1016/j.ijforecast.2021.03.012 | 5,12 | interpretable multi-horizon attention (E) | no net-of-cost finance superiority | candidate sequence encoder only |
| 22 | Zeng et al. 2023 — Are Transformers Effective for TS Forecasting? — AAAI 37(9) | 10.1609/aaai.v37i9.26317 | 5 | linear DLinear beats TS Transformers (E,R in TS) | not finance-specific | skeptical prior on sequence Transformers |
| 23 | Araci 2019 — FinBERT — arXiv | arXiv 1908.10063 | 6 | domain LM improves sentiment (E,S) | accuracy ≠ alpha | text-feature encoder |
| 24 | Wu et al. 2023 — BloombergGPT — arXiv | arXiv 2303.17564 | 6 | large finance LM beats generic (E,S) | proprietary; benchmark not alpha | text/event-extraction ceiling |
| 25 | Tetlock 2007 — Giving Content to Investor Sentiment — J. Finance 62(3) | 10.1111/j.1540-6261.2007.01232.x | 6,13 | media pessimism → pressure + reversal (E,R dir) | short-horizon, cost-fragile | news = short/reversal-flavored |
| 26 | Zou et al. 2023 — Universal Transferable Adversarial Attacks on Aligned LMs — arXiv | arXiv 2307.15043 | 6,8 | alignment breakable, transferable (E,R) | attack, not finance | prompt-injection/poisoning threat model |
| 27 | Feng et al. 2019 — Temporal Relational Ranking — ACM TOIS 37(2) | 10.1145/3309547 | 7 | graph relations improve ranking (E,S) | gross-of-cost; no peer-agg baseline | motivates but ≠ validates GNN |
| 28 | Bhojraj, Lee, Oler 2003 — What's My Line? — J. Accounting Research 41(5) | 10.1046/j.1475-679X.2003.00122.x | 7,15 | GICS best explains co-movement (E,R) | GICS licensed/paid | strong cheap peer baseline |
| 29 | FinSeer/FinSrag 2025 — Retrieval-augmented LLMs for Financial TS — arXiv | arXiv 2502.05878 | 8 | domain retrieval for stock-movement (E,S) | new, unreplicated; leakage risk | experimental analog aid only (*Content: abstract*) |
| 30 | Geifman, El-Yaniv 2019 — SelectiveNet — ICML PMLR 97 | arXiv 1901.09192 | 10 | integrated reject option at target coverage (E) | IID/in-dist guarantees | basis for ABSTAIN gating |
| 31 | DeMiguel, Garlappi, Uppal 2009 — Optimal vs Naive Diversification — RFS 22(5) | 10.1093/rfs/hhm075 | 11 | no optimizer reliably beats 1/N OOS (E,R) | pre-ML optimizers | favor deterministic allocation |
| 32 | López de Prado 2016 — HRP — J. Portfolio Mgmt 42(4) | 10.3905/jpm.2016.42.4.059 | 11 | HRP lower OOS variance (E,S; MC) | simulation, single | alternative to unstable optimizer |
| 33 | Baltrušaitis, Ahuja, Morency 2018 — Multimodal ML Survey — IEEE TPAMI 41(2) | 10.1109/TPAMI.2018.2798607 | 12 | fusion taxonomy; missing-modality core (INF) | survey, not finance | justifies missing-modality design |
| 34 | Da, Engelberg, Gao 2011 — In Search of Attention — J. Finance 66(5) | 10.1111/j.1540-6261.2011.01679.x | 13 | retail attention → rise then reversal (E,R) | short-horizon | attention = risk flag + short signal |
| 35 | Xu, Livshits 2019 — Anatomy of a Crypto Pump-and-Dump — USENIX Security | arXiv 1811.10109 | 13 | Telegram-coordinated P&D dissected (E,S) | crypto, not equities | manipulation threat model |
| 36 | Ang, Bekaert 2002 — International Allocation w/ Regime Shifts — RFS 15(4) | 10.1093/rfs/15.4.1137 | 14 | regimes shift correlations/allocation (E,R) | detection lag unsolved | regime conditioning justified |
| 37 | McCracken, Ng 2016 — FRED-MD — JBES 34(4); + ALFRED | 10.1080/07350015.2015.1086655 | 14,15 | free PIT macro vintages (E/data) | macro only | free-PIT macro/regime inputs |
| 38 | SEC EDGAR Filer Manual / Dissemination Spec — SEC.gov | sec.gov (primary) | 15 | acceptance timestamp, 5:30pm cutoff, ~2-min dissemination (fact) | fundamentals only | free as-filed PIT fundamentals |
| 39 | Chen, Zimmermann 2022 — Open Source Cross-Sectional Asset Pricing — Critical Finance Review 11(2) | SSRN 3604626 | 2,15 | free reproducible signal data (~98% of clear predictors) (E,R) | signals, not PIT universe/GICS | free signal/data backbone |

## 3. Strongest- and weakest-supported claims for Financy

**Strongest (replicated, decision-critical):** (1) net-of-cost fragility dominates → turnover/cost first-class, discount gross alpha; (2) GBT-first for the tabular cross-section; (3) naïve 1/N is a hard benchmark → deterministic constrained allocation; (4) multiple-testing/overfitting discipline mandatory (t>3, purged CV, PBO, DSR); (5) free-PIT real for fundamentals+macro but **not** constituents/GICS (main silent look-ahead).

**Weakest (single-study / contested / inference — treat as hypotheses to earn inclusion via net-of-cost ablation):** (1) sequence Transformers beat GBT net-of-cost; (2) "virtue of complexity" transfers to the cross-section; (3) GNN/graph beats PIT peer/GICS aggregates; (4) analog/RAG yields calibratable tradable probabilities; (5) per-decision calibrated probabilities (incl. barrier/touch, time-to-event) hold under regime shift; (6) learned multimodal fusion beats GBT-on-concatenated-features.

**Cross-cutting integrity note (specialist):** almost all positive ML-alpha results here are gross-of-cost, value-weighted, in-sample-selected; the replicated finding is that realistic costs, turnover, universe/weighting, and multiple testing erode most of it. The evidence most strongly supports a **conservative, low-turnover, GBT-cored, calibration-gated, PIT-disciplined design with an explicit ABSTAIN**, treating sequence/graph/RAG/fusion as unproven enhancements that must beat cheap baselines net-of-cost before inclusion.
