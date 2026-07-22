# 12 — Cross-Sectional Decision & Portfolio / Risk Architecture

**Artifact type:** design (lead-authored; follows Alternatives A + C; preserves the R0
sizing-precedence discipline). **Decision-label:** structure = `ARCHITECTURAL_INFERENCE`;
λ-weights, caps, and thresholds = `EMPIRICAL_TBD` / `FROZEN_ECONOMIC_PRIOR` (never fit on the
backtest). Portfolio allocation = deterministic constrained policy, **not** a mean-variance
optimizer (DeMiguel-Garlappi-Uppal: 1/N beats optimizers OOS on small samples).

---

## 1. The decision cycle (per overnight/EOD run)
1. Build the eligible **PIT universe** (survivorship-safe `FixedPITCohort`).
2. Synchronize **multimodal evidence** at the cutoff (availability-time + PIT source-trust, `07`).
3. Determine **market / sector / regime** states (deterministic PIT regime vector, `06`).
4. Generate per-stock, per-horizon **forecast distributions** (the target vector, `10`).
5. Compare each stock with **peers and alternative opportunities** (cross-sectional).
6. Compute expected **gross and net edge** (`economic_edge_bps = E[absolute-executable return] −
round-trip cost`; only the absolute-executable head may have absolute cost subtracted).
7. Compute **uncertainty & model disagreement**.
8. Select or reject candidate **horizons** (pre-registered rule, `10`).
9. **Rank** opportunities by risk-adjusted utility (cross-sectional percentile).
10. Apply **liquidity, sector, beta, factor, correlation** controls.
11. Choose **position size or abstain**.
12. Preserve **supporting and contradictory** evidence (the evidence DAG, `13`).
13. Establish **invalidation and monitoring** rules for the open position.

## 2. Return-basis distinctions (never mixed in cost math)
`absolute return` · `market-relative return` · `sector-relative return` · `cross-sectional rank`
· `portfolio utility` · `final action`. Ranking may be **relative** (market/sector-excess); **cost
subtraction and utility must be absolute-executable** (ADR-004). Sector-excess never enters
`economic_edge_bps`.

## 3. Action set & the sizing invariant
Actions: **BUY · HOLD · REDUCE · EXIT · ABSTAIN.** `ABSTAIN` is first-class and cheap to reach
(the abstention gate, `13`). **No alpha/probability sizes a position directly.** Sizing precedence
(a size appears only at the risk-budget step and may only **shrink** thereafter):
`forecast → permission/eligibility → hard blockers → economic-edge gate → risk-adjusted-utility
gate → per-trade risk-budget size (size to worst-case gap, not stop distance) → caps (max
notional, ADV participation, buying-power, min-order, leverage) → portfolio marginal-utility
allocation → turnover/hysteresis → execution feasibility → (advisory/human approval)`.

## 4. Portfolio construction & risk controls
- **Greedy marginal-utility allocation** with concentration / sector / beta / factor / correlation
caps and turnover/hysteresis — **not** a mean-variance optimizer (falls back to greedy
risk-budget). λ-weights are `FROZEN_ECONOMIC_PRIOR` for the MVP; any weight chosen after viewing
a backtest becomes a registered trial and enters the overfitting analysis.
- **Turnover is a return driver, not just a risk control** (Novy-Marx-Velikov <50%/mo survives
costs); the allocator penalizes turnover explicitly.
- **Correlated-failure / concentration guard:** cap exposure to any single factor/sector/theme so
apparent alpha is not an unpriced crowded beta bet; the factor-attribution incremental-value test
(`13`) checks that portfolio alpha is residual of price/factor betas.
- **Scenario/regime robustness (Alt C overlay):** a `worst_plausible_state_utility` is computed
across PIT-weighted regime scenarios; contradictory modalities widen σ → shrink size or abstain;
missing modality raises the uncertainty premium in the hurdle (`required_hurdle ≥ cost +
uncertainty_premium(missingness)`).

## 5. The five separated decision stages (autonomy ladder)
The system distinguishes and never conflates: **research forecast → advisory recommendation →
paper trade → human-approved order → autonomous execution.** Each is a distinct record with its
own gate. **Autonomous execution is not authorized** (permanently REJECTED absent an explicit
owner decision); the highest the system reaches by default is an **advisory recommendation** (and
paper trade in a later release, human-approved only). No agent-generated code connects to a live
broker during R0/R1A.

## 6. Whole-decision calibration
Beyond per-forecast calibration, the decision layer is calibrated end-to-end: regress **realized
net return on predicted risk-adjusted utility** and require slope≈1, intercept≈0 (Alt C; A4). A
decision policy whose predicted utility does not track realized net outcome is not trusted,
regardless of forecast accuracy.

## 7. What this design refuses
No mean-variance optimizer; no size from an alpha score; no mixed-basis cost subtraction; no
autonomous execution; no position without invalidation/monitoring rules; no λ fit on the
backtest.
