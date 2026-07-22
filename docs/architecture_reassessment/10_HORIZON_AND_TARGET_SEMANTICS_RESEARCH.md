# 10 — Horizon & Target-Semantics Research Plan

**Artifact type:** pre-registered research-program design (lead-authored). **Decision-label:**
the *study design* is `ARCHITECTURAL_INFERENCE`; **every horizon/target conclusion is
`EMPIRICAL_TBD` and must not be asserted before the experiments exist.** The current
`{5,8,14}` sessions and the single scalar `ABSOLUTE_EXECUTABLE_RETURN` are treated as
**provisional probe values, not optimal truths.**

---

## 1. Reopen the horizons — as a pre-registered study, not a sweep
Candidate horizons to *study* (not to adopt): **1, 3, 5, 8, 10, 14, 16, 21, 42 sessions**, plus
any economically-justified alternative. **Warning built into the design:** each horizon is a
**DSR trial** (Harvey-Liu-Zhu), and sweeping horizons freely is a textbook overfitting surface.
Therefore the study **pre-registers** the candidate set, the selection rule, and the rejection
rule *before* touching the final holdout, and every horizon evaluated is trial-registered.

## 2. Forecasting structure — compare, don't assume
| Structure | When justified |
|---|---|
| Separate direct model per horizon | simplest; multiplies trials |
| **Direct multi-output** (one model, vector target) | shares data efficiency; preferred default under small sample |
| Shared encoder + horizon-specific heads | if a shared representation helps (challenger territory) |
| Dynamic horizon selection | only if a pre-registered rule picks horizon from PIT features without peeking |
| Event-conditioned horizons | horizon set by an event (earnings, catalyst) rather than a fixed count |
| Barrier-touch models | for P(touch), path decisions (reopens ADR-005) |
| Survival / time-to-target | for E[time-to-target], censored by the time barrier |
| Path-distribution models | for the full predictive path (challenger B2 only) |
| Portfolio holding-period optimization | horizon chosen to optimize portfolio utility net of turnover/cost |

**Hard rule:** do **not** use recursive one-step forecasts iterated to a horizon by default —
error compounds and leakage is easy; use **direct** multi-horizon forecasting.

## 3. The pre-registered horizon study must address
signal decay by horizon · **overlapping labels** (a 14-session label overlaps 13 neighbors) ·
purge · embargo · **effective sample size** (dependence-adjusted; block ≥ max horizon) ·
**calibration sample size** (disjoint from fit, purge/embargo-obeying) · turnover (shorter
horizons → higher turnover → cost erosion, Novy-Marx-Velikov <50%/mo) · costs (net-of-cost at
every horizon) · regime stability (does the best horizon flip across regimes?) · multiple testing
(DSR/PBO over the horizon set) · **final-holdout protection** (freeze before access) · explicit
**selection and rejection criteria** (a horizon is retained only if it beats the price/volume
baseline net-of-cost, factor-residual, DSR-deflated, on ≥2 regimes).

## 4. Possible conclusions (to be *earned*, not asserted now)
The study concludes whether `{5,8,14}` should be **retained · expanded · replaced · used only as
reporting checkpoints · made dynamic · or combined with event-driven horizons.** A defensible
*prior* (not a result): keep a small fixed set as reporting checkpoints, and let turnover/cost +
effective-sample considerations, not raw IC, drive the choice — but this is a hypothesis the
experiments must confirm. **No empirical certainty is claimed before the experiments exist.**

## 5. Target-semantics recommendation
The single scalar target is insufficient for the mission's ~16 outputs, but path quantities are
**labels computable from the historical price path** — so a *tabular target vector* delivers most
of them without a sequence model (`04` Alt A). Recommended tiering:

| Tier | Outputs | How | Label / calibration |
|---|---|---|---|
| **Primary** | (1) terminal E[return, absolute-executable], (5) P(exceeds cost), (13) cross-sectional rank | the R0 continuous head + a cost-hurdle probability head | continuous head: interval-coverage; probability head: isotonic/Platt+ECE (`11`) |
| **Core derived** | (2) median, (3) quantiles/intervals, (4) P(positive), (6) P(exceeds threshold), (12) market/sector-relative | quantile-regression heads + excess-basis heads | conformal/CQR coverage (LIMITED_SUPPORT across regimes) |
| **Path (barrier)** | (7) P(touch before H), (9) MFE, (10) MAE | triple-barrier meta-label + excursion regression on path-derived labels; **frozen, stress-tested barrier params** (reopens ADR-005) | barrier probs default `LIMITED_SUPPORT` (calibration academically unvalidated, `03` Q9) |
| **Weak / challenger** | (8) E[time-to-target], (11) drawdown *distribution* | censored/survival (approx in A); full path distribution only from challenger B2 | conservative; `LIMITED_SUPPORT` |
| **Decision** | (14) portfolio utility, (15) action, (16) size | decision/portfolio layer (`12`) | whole-decision calibration (slope≈1) |

**Schema consequence** (`04` deltas): represent each target-type as *additional `LabelRecord`
rows* per (instrument, prediction_time, horizon, target_type) with its own
`target_definition_version` encoding frozen barrier params; keep `HorizonSessions{5,8,14}`
unwidened (each horizon a trial); each head gets its own `CalibrationArtifactManifest`. Every
output carries a `claim_type` and calibration-support label per the probability-integrity policy
(`11`).
