# 06 — Technical, Market & Macro Engine

**Artifact type:** design (lead-authored; follows the recommended Alternative A and the
evidence in `03`). **Decision-label:** the *design skeleton* is `ARCHITECTURAL_INFERENCE`;
every specific indicator's inclusion is `EMPIRICAL_TBD` — admitted only by ablation that beats
a price/volume-only baseline net-of-cost, factor-residual, DSR-deflated. Do **not** assume any
traditional technical pattern is universally predictive.

---

## 1. Principle: features are hypotheses, not a checklist
A technical engine is not "a list of indicators." Each candidate feature is a trial (it enters
the trial registry and inflates the DSR hurdle — Harvey-Liu-Zhu t>3). The engine's job is to
(a) express a *small* set of economically-motivated, low-collinearity features at frozen
lookbacks, (b) let the GBT learn interactions and nonlinearities (Gu-Kelly-Xiu: the ML gains
are the interactions), and (c) refuse to add a feature that does not beat the baseline. The
default posture is **parsimony under multiple-testing**, not coverage.

## 2. Explicit feature vs learned-from-raw vs redundant vs regime-dependent
| Class | Treatment | Rationale |
|---|---|---|
| **Explicit engineered features** | returns (raw & as-of), realized & downside volatility (ATR-like), gap size, relative volume / volume z-score, VWAP-distance, range/close position, cross-sectional **rank** transforms of each, relative strength (market- and sector-relative) | cheap, interpretable, GBT-friendly; ranks are regime-robust and reduce scale drift |
| **Candidate but collinearity-pruned** | SMA/EMA family, RSI, MACD, stochastic, Bollinger-derived, ADX/DMI, OBV | heavily inter-correlated (many are monotone transforms of price/vol); keep at most one representative per correlation cluster; prune by variance-inflation before the model sees them |
| **Learn from raw sequence (challenger only)** | multi-bar structure, candlestick/multi-bar patterns, breakout/failed-breakout, higher-high/lower-low structure, support/resistance | pattern features are researcher-DoF-heavy and regime-dependent; encode as a *few* structural summaries in A, and only let a causal sequence encoder (challenger B1) produce them if it beats the summaries net-of-cost |
| **Redundant / drop** | multiple oscillators measuring the same momentum; indicators that are deterministic functions of ones already included | pure multiple-testing cost, no incremental information |

**Peer/relative features** (relative strength, market-relative, sector-relative, peer-relative
behavior) are computed as **PIT cross-sectional ranks** using only same-cutoff data — a strong,
cheap baseline (Bhojraj-Lee-Oler: GICS/industry already explains co-movement) that any graph
model must beat before inclusion (see `08`).

## 3. Lookback selection, availability, corporate actions
- **Lookbacks are frozen priors, not tuned on the backtest.** A small grid (e.g., short/medium/
long) chosen from economic reasoning; any lookback selected after viewing results is a
registered trial. Do not sweep lookbacks freely — it is the classic overfitting surface.
- **Availability:** every technical feature derives only from bars with `session_date ≤
decision_cutoff`; the feature's `feature_available_at` = the bar's availability; the sample's
`InformationInterval` widens to include the longest lookback's earliest input (this is a *purge*
concern, not automatically a forward *embargo* — VAL-R0-03: feature lookback is not auto-added
as forward embargo unless overlap analysis requires it).
- **Corporate actions:** features on **price levels / filters / support-resistance / dollar-volume
never inherit the split-only simple-return exception** (§0.6e); they use the as-of adjusted
series. Simple-return features may use the split exception only when both endpoints are on the
same side of the split (§0.6a). Volume features must be split-adjusted consistently.

## 4. Multiple-testing & regime-dependence controls
- Every feature and lookback is trial-registered; the feature set is frozen before final-holdout
access; feature-family ablations (technical-only) are mandatory (`13`).
- Regime-dependence is expected: momentum vs reversal flips by horizon and regime, and short
(≤5-session) signals are reversal-/microstructure-contaminated (Da-Engelberg-Gao; Tetlock
reversal). Represent regime as **feature columns the tree can split on**, not as a hard switch
(variant E caution: HMM/regime classifiers are OOS-fragile).

## 5. Market / sector / macro context engine
A **deterministic PIT regime vector**, not a learned world-model (A7 simplification; canonical
defers the Market World Model to R1B+). Each dimension is a PIT feature column:
- **Index regime:** SPY/market trend state, drawdown-from-high, breadth (advance/decline,
% above moving average).
- **Volatility regime:** VIX level/term-structure state, realized-vol regime.
- **Rates / credit / liquidity:** short & long rates, curve slope, credit spread state, funding/
liquidity proxies — all from **PIT macro vintages (FRED/ALFRED)**, never latest-revised
(McCracken-Ng; the ALFRED archive exists precisely for "what was known when").
- **Commodities / currencies:** broad commodity and USD state where the instrument has exposure.
- **Sector / industry state:** PIT sector/industry relative strength and dispersion (SIC-based
free-PIT; GICS is licensed and PIT-GICS is not free — the main silent look-ahead risk, so
sector classification must be as-of and its source recorded).
- **Correlation / risk-on-off regime:** rolling cross-asset correlation state, change-point flag
(soft/probabilistic, not a hard switch).

**Interaction payoff:** the regime vector is what lets the GBT model the mission's headline
interactions non-additively — e.g. `company_news_digest × sector_regime` (good news under a
hostile sector regime routes to a different leaf), `breakout × volume_confirmation ×
supplier_event`, `attention_spike × source_trust × price_already_moved`.

## 6. What this engine deliberately does NOT do
No claim that candlestick/chart patterns are universally predictive; no free lookback sweeps; no
hard regime switching; no macro data at latest-revised vintage; no indicator admitted without an
ablation that beats the price/volume-only baseline net-of-cost. Everything here is a hypothesis
the validation program (`13`) must confirm before it is trusted.
