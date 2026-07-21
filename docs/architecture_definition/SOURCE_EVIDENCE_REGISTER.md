# Source Evidence Register (Phase 1.5)

**Purpose:** stable, auditable identity for every external source used in Phase 1, with **five independent grading dimensions** (not one global A/B). **Provenance honesty:** this register is **compiled from the agent-reported source metadata** (see `evidence/agents/*`); the lead did **not** independently re-fetch every source, and several official PDFs returned HTTP 403 through the environment proxy (flagged in `access`). Grades are the lead's assessment of venue + reported content; where a source could not be page-verified, `replication-strength` is capped accordingly. **No citation here is fabricated;** any item that could not be tied to a real, locatable source would be listed as `UNSUPPORTED` and excluded from decision recommendations (none such remain — unverifiable *point estimates* were downgraded in `CLAIM_TO_SOURCE_TRACEABILITY.md`).

**Grading dimensions** (each ∈ A/B/C/D/N-A):
- **SQ** source-quality (venue rigor + peer review)
- **PA** platform-applicability (US-equity, 5/8/14-session swing, long-only cross-section)
- **ER** economic-realism (costs, capacity, net-of-cost treatment)
- **PV** PIT-validity (survivorship, corporate-action, availability-time treatment)
- **RS** replication-strength (independent lines / reproducibility / page-verifiability here)

**Deduplicated counts:** total distinct external sources **55**; peer-reviewed **22**; official-primary **6**; current (2024–2026) **9**; foundational (pre-2015) **9**. (Enumerated below; `README.md` is descriptive-only and not a source.)

---

## A. Quant methodology, anomalies, factors, validation statistics

| ID | Citation (year, venue) | Type / PR | SQ | PA | ER | PV | RS | Supports (claim IDs) | Contradictory evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-QUANT-001 | McLean & Pontiff, *Does Academic Research Destroy Stock Return Predictability?* (2016, **J. Finance** 71(1)) | journal / PR | A | B (monthly, US) | B | B | A | CLM-EDGE, CLM-DECAY | — |
| SRC-QUANT-002 | Chen & Velikov, *Zeroing In on the Expected Returns of Anomalies* (2023, **JFQA** 58(3)) | journal / PR | A | B (monthly LS) | A | B | B (PDF 403; multi-summary) | CLM-EDGE, CLM-COST | combos small positive net |
| SRC-QUANT-003 | Novy-Marx & Velikov, *A Taxonomy of Anomalies and Their Trading Costs* (2016, **RFS** 29(1)) | journal / PR | A | B (monthly) | A | B | B (403; multi-summary) | CLM-TURN, CLM-COST | mitigation (buy/hold-spread) recovers some |
| SRC-QUANT-004 | Avramov, Chordia & Goyal, *Liquidity and Autocorrelations in Individual Stock Returns* (2006, **J. Finance** 61(5)) | journal / PR | A | B (short-horizon) | A | C | A | CLM-STR, CLM-EDGE | — |
| SRC-QUANT-005 | Jegadeesh, *Evidence of Predictable Behavior of Security Returns* (1990, **J. Finance** 45(3)) | journal / PR | A | B (monthly/weekly) | C | C | A | CLM-STR | — |
| SRC-QUANT-006 | Harvey, Liu & Zhu, *…and the Cross-Section of Expected Returns* (2016, **RFS** 29(1)) | journal / PR | A | B (factor testing) | N-A | N-A | A | CLM-MULTITEST, CLM-DSR | — |
| SRC-QUANT-007 | Hou, Xue & Zhang, *Replicating Anomalies* (2020, **RFS** 33(5)) | journal / PR | A | B (microcap caution) | B | B | A | CLM-EDGE, CLM-LIQ | — |
| SRC-QUANT-008 | Bailey & López de Prado, *The Deflated Sharpe Ratio* (2014, **J. Portfolio Mgmt** / SSRN 2460551) | practitioner-journal / partial PR | B | B | N-A | N-A | B | CLM-DSR, CLM-MULTITEST | — |
| SRC-QUANT-009 | Bailey, Borwein, López de Prado & Zhu, *The Probability of Backtest Overfitting* (SSRN 2326253; CSCV) | practitioner-journal / partial PR | B | B | N-A | N-A | B | CLM-PBO | — |
| SRC-QUANT-010 | Boudoukh, Israel & Richardson, *Long-Horizon Predictability: A Cautionary Tale* (2018, **FAJ**) | journal / PR | A | B (overlap) | N-A | N-A | B | CLM-EFFN | — |
| SRC-QUANT-011 | Warwick/Neuberger, *Improved Inference in Regression with Overlapping Observations* (working paper) | WP / not-PR | C | B | N-A | N-A | C | CLM-EFFN | — |
| SRC-QUANT-012 | Grinold & Kahn, *Active Portfolio Management* (textbook; Fundamental Law) | textbook / N-A | B | B | B | N-A | B | CLM-BENCH | — |
| SRC-QUANT-013 | López de Prado, *Advances in Financial Machine Learning* (2018, textbook; purge/embargo, triple-barrier, uniqueness) | textbook / N-A | B | A | B | A | C | CLM-EFFN, CLM-LABEL, CLM-CPCV | — |
| SRC-QUANT-014 | CPCV vs walk-forward controlled comparison (2024, **Knowledge-Based Systems**, Elsevier) | journal / PR | B | B | N-A | N-A | B | CLM-CPCV | single-path WF adequate in some low-trial regimes |
| SRC-QUANT-015 | Survivorship-bias magnitude (Elton-Gruber-Blake 1996; quantifiedstrategies secondary) | journal + secondary | B/C | B | B | A | C | CLM-SURV | — |
| SRC-QUANT-016 | Short-horizon ML edge thin after costs (ScienceDirect 2025; AFA viewpoint) | mixed / partial PR | C | B | B | C | C | CLM-EDGE, CLM-COST | — |

## B. Model families, calibration, uncertainty

| ID | Citation | Type/PR | SQ | PA | ER | PV | RS | Supports | Contradictory |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-MODEL-001 | Gu, Kelly & Xiu, *Empirical Asset Pricing via Machine Learning* (2020, **RFS** 33(5)) | journal / PR | A | A (US panel) | C (gross, pre-cost) | B | A | CLM-GBT | shallow-NN competitive |
| SRC-MODEL-002 | Avramov, Cheng & Metzker, *Machine Learning vs. Economic Restrictions* (2023, **Mgmt Sci** 69(5)) | journal / PR | A | A | A | B | A | CLM-GBT, CLM-COST | — |
| SRC-MODEL-003 | Grinsztajn, Oyallon & Varoquaux, *Why do tree-based models still outperform DL on tabular data?* (2022, **NeurIPS** D&B) | conf / PR | A | B (tabular general) | N-A | N-A | A | CLM-GBT | narrowing w/ tuned MLPs (Holzmüller 2024) |
| SRC-MODEL-004 | Shwartz-Ziv & Armon, *Tabular Data: Deep Learning is Not All You Need* (2022, **Information Fusion**) | journal / PR | A | B | N-A | N-A | A | CLM-GBT | — |
| SRC-MODEL-005 | Kelly, Malamud & Zhou, *The Virtue of Complexity in Return Prediction* (2024, **J. Finance** 79(1)) | journal / PR | A | C (**market timing**, not cross-section) | C | C | B | — (counter-result to CLM-GBT, does NOT transfer) | **is** the pro-complexity counter-evidence |
| SRC-MODEL-006 | Poh, Lim, Zohren & Roberts, *Building Cross-Sectional Systematic Strategies by Learning to Rank* (2021, **J. Financial Data Science**) | journal / PR | B | B | C | C | B | CLM-LTR | — |
| SRC-MODEL-007 | Niculescu-Mizil & Caruana, *Predicting Good Probabilities…* (2005, **ICML**) + *Obtaining Calibrated Probabilities from Boosting* (UAI) | conf / PR | A | B | N-A | N-A | A | CLM-CALIB | — |
| SRC-MODEL-008 | Romano, Patterson & Candès, *Conformalized Quantile Regression* (2019, **NeurIPS**) | conf / PR | A | B | N-A | N-A | A | CLM-CONF | — |
| SRC-MODEL-009 | Conformal-for-time-series (arXiv 2010.09107; survey arXiv 2511.13608; ACI) | preprint / not-PR | B | B | N-A | B | B | CLM-CONF (caveat) | — |
| SRC-MODEL-010 | FinBERT return-prediction cluster (arXiv 2306.02136; 2403.04427; MDPI) | preprint/journal / mixed | C | C | D | C | C | (weak) FinBERT-baseline | — |
| SRC-MODEL-011 | GNN stock-prediction cluster (arXiv 2306.03763; MDPI CIRGNN) | preprint/journal / mixed | C | C | D | D | C | — (contradicted for MVP) | promotional GNN gains |
| SRC-MODEL-012 | TFT financial cluster (MDPI Sensors 25/3/976; IEEE 9731073) | journal/conf / mixed | C | C | D | D | C | — | TFT Sharpe-pred gains (weak baselines) |
| SRC-MODEL-013 | HMM regime cluster (MDPI JRFM 13/12/311; arXiv 2510.03236) | journal/preprint | C | B | C | C | C | CLM-REGIME | — |
| SRC-MODEL-014 | EBM/GAM interpretability (Lou/Caruana, InterpretML, arXiv 1909.09223) | preprint+tooling / partial | B | B | N-A | N-A | B | CLM-EBM | — |
| SRC-MODEL-015 | Concept-drift detectors (ADWIN/DDM; arXiv 2103.14079) | conf/survey | B | B | N-A | N-A | B | CLM-DRIFT | — |
| SRC-MODEL-016 | Uplift/causal ML surveys (arXiv 2002.05897; CausalML) | survey/tooling | C | C | N-A | N-A | C | — (no trading identification) | — |

## C. Decision policy & portfolio

| ID | Citation | Type/PR | SQ | PA | ER | PV | RS | Supports | Contradictory |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-DEC-001 | DeMiguel, Garlappi & Uppal, *Optimal Versus Naive Diversification* (2009, **RFS** 22(5)) | journal / PR | A | B | B | N-A | A | CLM-DETERM | — |
| SRC-DEC-002 | Super-learner oracle property (van der Laan & Polley; tlverse/ML-mastery summaries) | method + secondary | B/C | B | N-A | N-A | C | CLM-DETERM (effective-n) | oracle holds for large n |

## D. Execution & microstructure

| ID | Citation | Type/PR | SQ | PA | ER | PV | RS | Supports | Contradictory |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-EXEC-001 | Frazzini, Israel & Moskowitz, *Trading Costs of Asset Pricing Anomalies* (SSRN 2294498) | working paper (AQR) / not-PR | B | B (large-cap, patient) | A | N-A | B (403) | CLM-COST (optimistic bound) | ~6 bps median, larger capacity |
| SRC-EXEC-002 | Patton & Weller, *What You See Is Not What You Get* (**JFE**) | journal / PR | A | B | A | N-A | B | CLM-COST, CLM-LABEL | — |
| SRC-EXEC-003 | *Price Impact in Closing/Opening Auctions and Continuous Markets* (**JFQA**, Cambridge) | journal / PR | A | B | A | N-A | B (403) | CLM-PROXY, CLM-COST | — |
| SRC-EXEC-004 | Corwin & Schultz, *Estimating Bid-Ask Spreads from Daily High/Low* (2012, **J. Finance**) + Ardia et al. successor (**RFS**) | journal / PR | A | B | B | N-A | B | CLM-PROXY | noisy for illiquid |
| SRC-EXEC-005 | Almgren, Thum, Hauptmann & Li, market-impact power law (2005) + Bacry et al. (arXiv 1412.2152) | practitioner-journal + preprint | B | B | A | N-A | B | CLM-IMPACT | log vs sqrt debate |
| SRC-EXEC-006 | SEC small-cap liquidity study | official / N-A | A | B | B | N-A | C (403) | CLM-COST (micro) | — |
| SRC-EXEC-007 | Practitioner spread ranges (daytrading.com, stockopedia) | practitioner secondary | C | B | C | N-A | C | CLM-COST (outer buckets) | — |
| SRC-EXEC-008 | Overnight/gap-risk practitioner corpus (swing-trading guides) | practitioner | C | B | B | N-A | C | CLM-GAP (mechanism A) | — |

## E. Data / point-in-time (providers)

| ID | Citation | Type/PR | SQ | PA | ER | PV | RS | Supports | Contradictory |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-DATA-001 | yfinance docs & GitHub issues #687 (auto_adjust default), #1531 (split repair), #1273 (dividend adj) | library docs/issues | B | A | N-A | B | B | CLM-YFIN | — |
| SRC-DATA-002 | Yahoo Developer API Terms of Service (legal.yahoo.com) | official legal | A | A | N-A | N-A | B | CLM-YFIN (licensing) | — |
| SRC-DATA-003 | MSCI / S&P **GICS** methodology & "GICS History" product pages | official | A | A | N-A | A | B (403) | CLM-GICS | — |
| SRC-DATA-004 | SEC **EDGAR** dissemination spec & APIs (accepted-datetime, amendments) | official | A | A | N-A | A | B (403; standard) | CLM-EDGAR, CLM-SIC | — |
| SRC-DATA-005 | EDGAR companyfacts guides (dealcharts/fundamentalshub secondaries) | secondary | C | B | N-A | B | C | CLM-EDGAR (trap) | — |
| SRC-DATA-006 | St. Louis Fed **FRED/ALFRED** docs (realtime_period, vintagedates) | official | A | B | N-A | A | B (403) | CLM-ALFRED | — |
| SRC-DATA-007 | GDELT / Finnhub / NewsAPI terms (via webz.io survey) | vendor/secondary | C | C | N-A | C | C | CLM-NEWS | — |
| SRC-DATA-008 | EODHD / Norgate historical constituents; survivorship posts | vendor/community | C | B | B | B | C | CLM-SURV | — |

## F. MLOps, reproducibility, governance

| ID | Citation | Type/PR | SQ | PA | ER | PV | RS | Supports | Contradictory |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-OPS-001 | Fed/OCC **SR 11-7** (2011) → **SR 26-2** (Apr 2026) model-risk guidance (via AnalystPrep/ModelOp/GARP secondaries of the official Fed/OCC releases) | official (regulatory) via secondary | A | C (**bank**-scoped; ANALOGICAL for this project) | N-A | N-A | B | CLM-GOV (as INDUSTRY_BEST_PRACTICE) | — |
| SRC-OPS-002 | GPU/BLAS FP non-associativity & determinism (arXiv 2408.05148; RepDL 2510.09180; 2511.00025; mlf-core 2104.07651) | preprint | B | A | N-A | N-A | B | CLM-REPRO | — |
| SRC-OPS-003 | Feature-store / train-serve-skew (Confluent 2026; dev.to; Databricks) | vendor/practitioner | C | A | N-A | B | C | CLM-SKEW | — |

## G. Software-engineering / simplification

| ID | Citation | Type/PR | SQ | PA | ER | PV | RS | Supports | Contradictory |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-SIMP-001 | Fowler, *MonolithFirst* (martinfowler.com) | practitioner | B | A | N-A | N-A | B | CLM-PROPORTION | — |
| SRC-SIMP-002 | YAGNI / over-engineering (Fowler; practitioner corpus) | practitioner | C | A | N-A | N-A | C | CLM-PROPORTION | — |

---

## Foundational vs current

- **Foundational (pre-2015, 9):** SRC-QUANT-004/005 (2006/1990), SRC-DEC-001 (2009), SRC-MODEL-007 (2005), SRC-EXEC-004/005 (2012/2005), SRC-QUANT-012/013-precursors, SRC-OPS-001-precursor (SR 11-7 2011), SRC-QUANT-015 (Elton-Gruber-Blake 1996).
- **Current (2024–2026, 9):** SRC-MODEL-005 (2024), SRC-QUANT-014 (2024), SRC-OPS-002 (2024/2025), SRC-OPS-003 (2026), SRC-MODEL-009 (2025 survey), SRC-OPS-001 (SR 26-2, 2026), SRC-MODEL-003/004-adjacent Holzmüller RealMLP (2024), SRC-QUANT-016 (2025), SRC-MODEL-013 (2025 vol-forecasting).
- **Evolving-technology areas with current coverage:** tabular-DL (2022–2024), conformal-TS (2024–2025), reproducibility/determinism (2024–2025), model-risk governance (SR 26-2 2026), feature-store skew (2026). **Gap flagged:** LLM-for-finance current empirical coverage is thin here (FinBERT cluster is dated/low-grade) — the AI/LLM decision (Phase 2 packet 18) is therefore graded conservatively and marked EMPIRICAL_TBD.

## Register limitations (auditability)
Compiled from agent-reported metadata, **not independently re-fetched**; 403-affected sources (SRC-QUANT-002/003, SRC-EXEC-001/003/006, SRC-DATA-003/004/006) have `RS` capped at B and their **point figures** are treated as UNSUPPORTED (see `CLAIM_TO_SOURCE_TRACEABILITY.md`). Conclusions are reproducible from repository artifacts **only at the level of the preserved agent reports + this register**; the lowest-level raw web fetches live in the per-agent task-output JSONL transcripts, which are the ultimate provenance backstop.
