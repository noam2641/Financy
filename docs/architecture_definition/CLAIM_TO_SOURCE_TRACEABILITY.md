# Claim-to-Source Traceability (Phase 1.5)

**Purpose:** give every load-bearing Phase-1 claim a stable claim ID, map it to `SOURCE_EVIDENCE_REGISTER.md` source IDs, and classify it as **EVIDENCE**, **INFERENCE** (derived from evidence + stated assumptions), or **ILLUSTRATIVE_ESTIMATE** (order-of-magnitude, not a measured value). Point estimates that cannot be page-verified are **downgraded** here and must be used only as ranges. **A claim's grade derives from source quality, applicability, and independent lines of external evidence — not from how many agents asserted it** (all agents share one model family; see `PHASE_1_EVIDENCE_INTEGRITY_REVIEW.md`).

Corroboration status vocabulary (see Round-2 doc): MULTI_AGENT_CONSENSUS · MULTI_SOURCE_CORROBORATED · SINGLE_AGENT_SUPPORTED · UNCONTRADICTED · DISPUTED · UNRESOLVED.

---

## Load-bearing claims (individually verified per mandate)

### CLM-TURN-WEEKLY — "≈100% weekly (one-way) turnover at the 5-session horizon"
- **Classification: ILLUSTRATIVE_ESTIMATE / INFERENCE (not measured).**
- **Derivation:** if average holding period ≈ 5 trading sessions and positions are fully replaced at exit, one-way turnover ≈ 1 book / 5 sessions ≈ 100% per trading week. At 14 sessions ≈ 100% per ~3 weeks.
- **Assumptions:** full replacement at horizon; **no hysteresis / minimum-holding-period / rank-band** (REQ-PORT-004 exists but is TBD). Daily re-ranking upper-bounds turnover.
- **Source:** none external (a mechanical consequence of the horizon); the *survival implication* rests on SRC-QUANT-003.
- **Scenario range:** with turnover controls, realized turnover could be **materially lower** (e.g., 20–60%/month) — the 100%/week figure is an **upper bound**, not the expected operating point.
- **Sensitivity:** high to `minimum_holding_period` / `rebalance_hysteresis` (both TBD).
- **Confidence:** medium as an *upper bound*; low as a point operating estimate.
- **Use rule:** cite as "high-turnover regime, plausibly ~100%/week absent turnover controls," never as a measured value.

### CLM-TURN — "≈50%/month is the anomaly-survival turnover boundary"
- **Classification: EVIDENCE (directional) with DOWNGRADED point precision.**
- **Source:** SRC-QUANT-003 (Novy-Marx & Velikov 2016).
- **Verified content:** costs uniformly reduce anomaly profitability and significance; **lower-turnover strategies are far more likely to retain net-significant spreads; high-turnover strategies generally do not**; buy/hold-spread mitigation is most effective. **The specific "50%/month" cutoff is a summary paraphrase and was NOT page-verified** (SRC-QUANT-003 PDF 403).
- **Scenario range / sensitivity:** the *boundary* is not a sharp universal threshold; it varies by anomaly, universe (microcap inclusion), and mitigation. Treat "~50%/month" as an **order-of-magnitude directional marker**, not a hard line.
- **Confidence:** high on the direction (higher turnover → worse net survival); **low on the exact 50% figure** → downgraded; present as "roughly half the book per month" with the caveat.
- **Corroboration:** MULTI_SOURCE_CORROBORATED (SRC-QUANT-002/007 align on net-of-cost fragility).

### CLM-COST — "≈20–100+ bps round-trip cost, exceeding a thin edge on parts of the universe"
- **Classification: EVIDENCE-INFORMED SCENARIO RANGE (point figures ILLUSTRATIVE).**
- **Sources:** SRC-QUANT-003 (mid-turnover 20–57 bps/trade), SRC-EXEC-001 (large-cap patient ~6 bps/rebalance — optimistic bound), SRC-EXEC-003 (auction impact 5.2–35.8 bps @0.5–5% ADV), SRC-EXEC-004/005/006/007.
- **Scenario range (round-trip, lead-compiled, point figures graded C, 403 caveat):** mega/large ~10–30 bps; mid ~40–100; small ~100–500; micro ~200–2000+.
- **Sensitivity:** dominated by liquidity bucket, order size / % ADV (impact ≈ √(size/ADV), SRC-EXEC-005), and execution style (patient VWAP vs aggressive MOO). The `maximum_spread`/`maximum_ADV_participation` caps (TBD) set which band applies.
- **Confidence:** high that round-trip cost is a decisive variable; **the specific per-bucket numbers are illustrative** and must be replaced by an empirical spread/ADV model.
- **Corroboration:** MULTI_SOURCE_CORROBORATED.

### CLM-EFFN — "Effective independent sample ≈ tens to low-hundreds of episodes"
- **Classification: INFERENCE / DERIVATION (not a measured count).**
- **Derivation (López de Prado uniqueness, SRC-QUANT-013):** with a 14-session forward label sampled daily, average label **uniqueness ≈ 1/14**; cross-sectional rows on one date share a few common factors (not N independent bets); independent **regime episodes per year are single-digit**. Net effective sample governing *decision-layer* parameters (which operate on aggregated per-cycle utility) ≈ tens–low-hundreds, far below the six-figure ticker-day count.
- **Assumptions:** overlapping daily labels; strong cross-sectional factor dependence; regimes as the binding independence unit for the *decision policy*.
- **Scenario range:** the exact number depends on history length and how independence is counted (per-date blocks vs per-regime); could be low-hundreds (per-date, weak-dependence) down to tens (per-regime).
- **Sensitivity:** high to the independence definition; this is why it is an inference, not a datum.
- **Confidence:** high on the *order of magnitude* and its implication (insufficient for a high-parameter learned meta-model); it is not a precise figure.
- **Corroboration:** SINGLE_AGENT_SUPPORTED (A4) but grounded in SRC-QUANT-013/010; MULTI_SOURCE on the underlying uniqueness/overlap principle.

### CLM-GBT — "Deep/sequence/graph/LLM models do not reliably beat GBT/linear on cost-bearing US-equity cross-sections"
- **Classification: EVIDENCE (Grade A), with a documented non-transferring counter-result.**
- **Sources:** SRC-MODEL-001 (trees/shallow-NN best; gains from nonlinear interactions), SRC-MODEL-002 (ML edge attenuates after costs / concentrated in hard-to-arbitrage), SRC-MODEL-003 + SRC-MODEL-004 (GBDT > DL on tabular).
- **Counter-evidence (represented, not omitted):** SRC-MODEL-005 (Kelly-Malamud-Zhou "Virtue of Complexity") — but it concerns **market timing** (single-series ridgeless random-feature regression), **not** cost-bearing cross-sectional selection → PA graded C; does not transfer. Also SRC-MODEL-003 nuance: strongly-tuned MLPs (Holzmüller 2024) are *competitive not superior*.
- **Confidence:** high for *this* problem (tabular cross-section, net of cost).
- **Corroboration:** MULTI_SOURCE_CORROBORATED (three independent Grade-A lines) + MULTI_AGENT (A3, A4). Grade rests on the sources, not the agent count.

### CLM-GICS — "Point-in-time GICS sector membership is unavailable on a free basis"
- **Classification: EVIDENCE (Grade A, official).**
- **Source:** SRC-DATA-003 (MSCI/S&P: GICS is exclusive property; PIT "GICS History" is a paid product).
- **Scenario range:** free *index-membership* proxies exist (SRC-DATA-008) but are **not** GICS sector taxonomy and lack official reclassification history.
- **Sensitivity:** none to the core claim (GICS licensing is a fact); the *decision* impact depends on whether a sector-relative objective is retained (Phase-2 packet 9).
- **Confidence:** high. **License-cost figure: UNSUPPORTED** (quote-based; not published) → not stated as a number.
- **Corroboration:** SINGLE_AGENT_SUPPORTED (A2) but backed by an official primary source; UNCONTRADICTED.

### CLM-YFIN — "yfinance back-adjustment creates future look-ahead" (PRECISION-CORRECTED)
- **Classification: EVIDENCE (Grade B) — but scope-limited; the blanket framing is corrected.**
- **Source:** SRC-DATA-001 (auto_adjust default back-adjusts OHLC for splits+dividends).
- **Precision (this is the correction the mandate requires):** back-adjustment leaks future information into **price-LEVEL** uses (52-week-high distance, support/resistance, Bollinger levels, **minimum-price and dollar-volume filters, universe construction**) and into **labels/returns that use total-return (dividend) adjustment**. It does **NOT** meaningfully leak into **simple split-only returns**, because a split multiplies all prior prices by a constant factor that **cancels** in `p_t/p_{t-1}`. So: *split back-adjustment is safe for simple returns, unsafe for price levels/filters; dividend/total-return adjustment is unsafe for returns/labels.* (Full use-by-use matrix in `PHASE_1_EVIDENCE_INTEGRITY_REVIEW.md` §Price-Basis.)
- **Confidence:** high on the level-feature/filter leakage; the corrected scoping removes the overstatement that "all adjusted data is invalid."
- **Corroboration:** MULTI_SOURCE (SRC-DATA-001 + general corporate-action look-ahead literature) + A2.

### CLM-SIC — "SIC is an acceptable alternative sector taxonomy" (DOWNGRADED)
- **Classification: DOWNGRADED — SIC is a *different* taxonomy, NOT a transparent GICS replacement.**
- **Source:** SRC-DATA-004 (SIC available free & PIT via EDGAR accepted-datetime).
- **Correction:** SIC is genuinely free and PIT, but its **semantics differ from GICS**: SIC is a legacy government classification, self-reported on filings, coarser and slower to reflect a company's current line of business; GICS is market-oriented and revised. Substituting SIC **redefines the target** (`sector_excess` becomes SIC-excess), changes peer groups, and is **not** equivalent. It is therefore a **separate decision option** (Phase-2 packet 9 option 2), not a drop-in.
- **Confidence:** high that SIC ≠ GICS; medium on whether SIC peer groups yield a usable sector-relative signal (EMPIRICAL_TBD).
- **Corroboration:** SINGLE_AGENT_SUPPORTED (A2); UNCONTRADICTED; **reclassified from the Phase-1 wording that implied substitutability.**

### CLM-DETERM — "A deterministic penalized-utility decision policy is safer than learned aggregation for the MVP"
- **Classification: INFERENCE / DESIGN-JUDGMENT (evidence-informed), partly EMPIRICAL_TBD.**
- **Sources:** SRC-DEC-001 (1/N beats optimizers OOS under estimation error), SRC-DEC-002 (super-learner oracle needs large n vs K), CLM-EFFN (small effective n), SRC-QUANT-008/006 (added complexity raises the significance bar).
- **Nature:** this is a *recommendation about robustness under small effective sample*, not a measured result on this system. The definitive test is the spec's own challenger comparison (learned aggregation must beat the frozen policy OOS under identical cost/risk/CPCV).
- **Scenario/sensitivity:** if effective sample turns out larger than inferred, or a challenger clears the gate, a learned layer could be promoted — hence EMPIRICAL_TBD with a decision rule, not a permanent architectural ban.
- **Confidence:** high that a learned super-model is *unjustified for the MVP*; the "safer" claim is a design inference, correctly framed as a recommendation.
- **Corroboration:** MULTI_SOURCE_CORROBORATED + MULTI_AGENT (A3, A4, A7).

### CLM-CPCV / CLM-DSR / CLM-PBO — "CPCV, DSR, PBO are mandatory for this use case" (APPLICABILITY-CONDITIONED)
- **Classification: EVIDENCE for the methods' validity; the "universal mandatory hard-gate" framing is DOWNGRADED to applicability-conditioned.**
- **Sources:** SRC-QUANT-008 (DSR), SRC-QUANT-009 (PBO/CSCV), SRC-QUANT-014 (CPCV), SRC-QUANT-013 (purge/embargo).
- **Correction (applicability):**
  - **DSR** applies **when multiple strategy/model trials exist**; requires a logged trial count N; below a handful of trials it adds little. Role: **primary** deflation once a trial registry exists.
  - **PBO/CSCV** requires **enough variants and CV partitions** to estimate; when not estimable it must report `PBO_NOT_ESTIMABLE` — which is **neither a pass nor proof of failure**. Role: **secondary/robustness**.
  - **CPCV** is a **robustness analysis** whose assumptions (multiple non-overlapping partitions) must be supportable; the **primary timeline remains grouped-by-date purged walk-forward** with embargo ≥ max information interval.
- **Confidence:** high on validity; the correction prevents these from becoming universal Release-0 *starting* blockers.
- **Corroboration:** MULTI_SOURCE_CORROBORATED + MULTI_AGENT (A1, A4, A7). Default hierarchy in `PHASE_1_EVIDENCE_INTEGRITY_REVIEW.md` §Validation.

### CLM-GOV — "Solo operation must be capped at RESEARCH/SHADOW" (RECLASSIFIED)
- **Classification: SINGLE_AGENT_SUPPORTED (A6 only); governance basis is INDUSTRY_BEST_PRACTICE / ANALOGICAL_GUIDANCE, NOT legally binding.**
- **Source:** SRC-OPS-001 (SR 11-7 / SR 26-2). **This is US bank supervisory guidance; it is not, on the evidence gathered, legally applicable to this project** (no verified legal-applicability determination). It supports independent validation & two-person controls as **strong internal-policy recommendations**, not legal requirements.
- **Correction:** reclassify CX-11 from any "consensus" label to **SINGLE_AGENT_SUPPORTED / UNCONTRADICTED**; recommend the cap as an **INTERNAL_POLICY_CHOICE** informed by best practice, with the basis stated correctly.
- **Confidence:** high that self-validation is weak; the *cap* is a policy recommendation, not an evidence-derived necessity.
- **Corroboration:** SINGLE_AGENT_SUPPORTED. Not to be labeled CONSENSUS.

---

## Other supporting claims (mapped, not individually re-derived)
CLM-DECAY→SRC-QUANT-001 · CLM-STR→SRC-QUANT-004/005 · CLM-MULTITEST→SRC-QUANT-006/008 · CLM-EDGE→SRC-QUANT-001/002/007/016 (EVIDENCE, base-rate) · CLM-BENCH→SRC-QUANT-012/002 · CLM-SURV→SRC-QUANT-015/SRC-DATA-008 · CLM-LTR→SRC-MODEL-006 · CLM-CALIB→SRC-MODEL-007 · CLM-CONF→SRC-MODEL-008/009 · CLM-REGIME→SRC-MODEL-013 · CLM-EBM→SRC-MODEL-014 · CLM-DRIFT→SRC-MODEL-015 · CLM-EDGAR→SRC-DATA-004/005 · CLM-ALFRED→SRC-DATA-006 · CLM-NEWS→SRC-DATA-007 · CLM-PROXY→SRC-EXEC-003/004 · CLM-IMPACT→SRC-EXEC-005 · CLM-GAP→SRC-EXEC-008 (mechanism Grade A) · CLM-LABEL→SRC-QUANT-013/SRC-EXEC-002 · CLM-REPRO→SRC-OPS-002 · CLM-SKEW→SRC-OPS-003 · CLM-PROPORTION→SRC-SIMP-001/002.

## Claims downgraded or removed in Phase 1.5
| Claim | Action | Reason |
| --- | --- | --- |
| CLM-TURN-WEEKLY (~100%/week) | **Downgraded** to ILLUSTRATIVE upper-bound | mechanical inference, sensitive to TBD turnover controls |
| CLM-TURN (50%/month boundary) | **Point precision downgraded** | summary paraphrase; source PDF 403; direction retained |
| CLM-COST (per-bucket bps) | **Point figures → ILLUSTRATIVE ranges** | 403s; graded C; must be replaced by empirical model |
| CLM-EFFN (tens–low-hundreds) | **Labeled INFERENCE** | derivation, not measurement |
| CLM-SIC (acceptable alternative) | **Downgraded** to "different taxonomy, separate option" | SIC ≠ GICS semantics |
| CLM-GICS license cost | **Removed as a number → UNSUPPORTED** | quote-based, not published |
| CLM-CPCV/DSR/PBO (universal gate) | **Downgraded** to applicability-conditioned | not universal Release-0 starting blockers |
| CLM-GOV (solo cap) | **Reclassified** SINGLE_AGENT + INDUSTRY_BEST_PRACTICE | not legally binding; not consensus |
| CLM-YFIN (all adjusted invalid) | **Scope-corrected** | split-adj safe for simple returns; unsafe for levels/filters |
