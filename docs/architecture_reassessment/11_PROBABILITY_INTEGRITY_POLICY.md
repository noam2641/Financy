# 11 — Probability-Integrity Policy

**Artifact type:** binding-proposal policy (lead-authored; grounded in the calibration
evidence from `03_RESEARCH_EVIDENCE_MATRIX.md`, Q4/Q9/Q10/Q13).
**Status:** `OWNER_DECISION_REQUIRED` for adoption as a hard interface; the *principle*
(no unsupported probability may be surfaced) is `EVIDENCE_SUPPORTED`.

This policy governs **every numerical probability, interval, or expected-value the system
displays or feeds into a decision.** It exists because the mission explicitly warns that a
claim such as *"97% probability of a 10% return within 16 sessions"* is not one statement
but several mutually-exclusive statements, and because the literature shows calibration
guarantees are **average/in-regime, not per-decision** (Barber et al. 2023; Gibbs-Candès
2021) and that **barrier-touch and time-to-event probability calibration is academically
unvalidated** (López de Prado 2018; §03 Q9).

---

## 1. A probability statement must declare its exact meaning
The following are **not interchangeable** and must be typed at the schema level. Every
probability-bearing field carries an explicit `claim_type`:

| `claim_type` | Precise meaning | Notes |
|---|---|---|
| `P_TERMINAL_POSITIVE` | P(return at horizon H > 0) | terminal, gross |
| `P_TERMINAL_GE_THRESHOLD` | P(terminal return ≥ x%) | terminal, gross |
| `P_TERMINAL_NET_GE_THRESHOLD` | P(terminal return − round-trip cost ≥ x%) | terminal, **net** |
| `P_TOUCH_BEFORE_H` | P(price touches +x% at **any time** ≤ H) | path/first-passage — always ≥ the terminal-close version |
| `P_CLOSE_ABOVE_AT_H` | P(price closes above +x% **at** session H) | terminal, distinct from touch |
| `P_CONDITIONAL_PATH` | P(event | a specified path/regime condition) | conditional |
| `FREQ_ANALOG` | empirical frequency over an as-of analog set | **frequency, not a calibrated model probability** |
| `P_MODEL_CALIBRATED` | a statistically calibrated model probability | only if it clears §3 |

**Hard rule:** a "touch" probability and a "terminal-close" probability must never be
displayed under the same label; an analog frequency must never be presented as a calibrated
model probability. Meaning-shift is treated as a correctness defect, not a wording nuance.

## 2. Illustrative scrutiny — *"97% probability of a 10% return within 16 sessions"*
*(numbers illustrative)* Before such a claim could ever be shown it must resolve to exactly
one `claim_type`, and then clear §3. In practice a 97% figure at a 16-session horizon on a
liquid US equity is **implausible for `P_TERMINAL_NET_GE_THRESHOLD`** on base rates alone,
is only conceivable for `P_TOUCH_BEFORE_H` at a small threshold, and is almost always an
artifact of an over-fit or small-sample `FREQ_ANALOG`. Absent the §3 support it is returned
as `NOT_ESTIMABLE` / `INSUFFICIENT_SUPPORT`, **not rounded, not shown as calibrated.**

## 3. Calibration gate — when a probability may be labeled `P_MODEL_CALIBRATED · WELL_SUPPORTED`
A numerical probability may be presented as calibrated **only** when **all** hold, each recorded as evidence:
1. a **precisely defined target** (`claim_type` + threshold + horizon + basis);
2. **strict out-of-sample** evaluation (purged/embargoed, final-holdout-protected);
3. **sufficient effective sample size** (dependence-adjusted / non-overlapping; block ≥ max horizon) — *not raw row counts*;
4. **calibration diagnostics** (reliability curve, ECE/Brier for probabilities; interval coverage for regression/quantile);
5. **confidence intervals** on the probability estimate itself;
6. **class-balance** and **base-rate** analysis for the event;
7. **relevant regime coverage** in the evaluation window;
8. **transaction-cost treatment** where the claim is net or feeds a decision;
9. **data-freshness** checks (no stale inputs);
10. **multiple-testing** control (trial-registered; DSR/PBO applicability);
11. **drift** checks and **out-of-distribution (OOD)** checks passing;
12. **no unsupported extrapolation** beyond the support of the calibration set.

**Calibration-support label** (recorded on every probability field):
- `WELL_SUPPORTED` — all §3 conditions met.
- `LIMITED_SUPPORT` — met on-average/in-regime but conditional/per-decision guarantee is weak (the default honest state for barrier/touch, time-to-event, and analog-derived quantities per §03 Q4/Q9); the value may be shown **with the caveat**, and it may **not** by itself justify a maximal position.
- `NOT_ESTIMABLE` — prerequisites absent (e.g., insufficient effective sample, no regime coverage). `NOT_ESTIMABLE` is **never a pass and never proof of failure** (consistent with the R0 hurdle semantics).

## 4. Fallback outcomes (when the gate is not cleared)
Return exactly one of: **`NOT_ESTIMABLE` · `INSUFFICIENT_SUPPORT` · `OUT_OF_DISTRIBUTION` · `ABSTAIN`.** These are first-class decision outcomes, not errors. A missing or `LIMITED_SUPPORT` probability propagates to **wider intervals, reduced size, or abstention** — never to a silently confident number.

## 5. The LLM / agent boundary (mission-mandated, `OWNER`-affirmed)
The LLM/agent layer **may**: organize evidence; identify contradictions; retrieve as-of analogs; explain forecasts; recommend deeper analysis or human review; route work.
The LLM/agent layer **may not**: invent probabilities; modify model probabilities; round probabilities upward (or in any direction); override calibration; override portfolio constraints; silently change thresholds; fabricate timestamps or sources. Any LLM-derived quantity that would enter a decision is treated as an **attackable feature** (prompt-injection/source-poisoning are live threats, §03 Q6) and must pass source-trust and the §3 gate like any other feature; it can never be the sole basis of a calibrated probability.

## 6. Method notes grounded in evidence
- GBT scores are **systematically miscalibrated**; apply Platt/isotonic **only to a defined probability head**, on a purge/embargo-disjoint calibration set (Niculescu-Mizil-Caruana 2005). Platt/isotonic must **never** be applied to a continuous-return regression (preserves the R0 `ECE = NOT_APPLICABLE_TO_PRIMARY_REGRESSION` invariant).
- Regression/quantile **interval coverage** via conformal/CQR (Romano et al. 2019) is valid **under exchangeability**; under time-series shift, coverage is **long-run average only** (Gibbs-Candès 2021) and degrades with distance from exchangeability (Barber et al. 2023) — so intervals carry `LIMITED_SUPPORT` across regime breaks by default.
- **Barrier-touch / time-to-event** probabilities have little validated calibration evidence → default `LIMITED_SUPPORT`, conservative, stress-tested barrier parameters frozen pre-hoc.
- **Analog frequencies** are calibratable only if the reference set is strictly as-of (no retrieval leakage) and the metric is regime-stable; otherwise `FREQ_ANALOG · LIMITED_SUPPORT` at most.

## 7. What this policy changes vs the current R0
R0 already enforces the *run-level* honesty analog (`EvaluationOutcome`, `NOT_ESTIMABLE` ≠ pass/fail, pre-registration). This policy extends the same discipline to **per-decision, per-field probabilities** the multimodal product will surface — the machinery to enforce it (effective-sample accounting, purge/embargo, trial registry, DSR/PBO, drift/OOD, source-trust) is exactly the R0 foundation to preserve and the gaps to build (`02` §4/§7).
