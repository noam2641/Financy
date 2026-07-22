# 18 — Illustrative End-to-End Walkthrough

**Artifact type:** worked example (lead-authored). **EVERY NUMBER, TICKER, SOURCE, AND EVENT
BELOW IS ILLUSTRATIVE AND FICTIONAL** — invented to show how the recommended architecture reasons,
not a claim about any real security. It demonstrates the decision cycle (`12`), the probability-
integrity policy (`11`), the trust layer (`07`), the interaction handling (`06`/`09`), and how the
system reaches a disciplined **ABSTAIN**.

---

## Scenario (all fictional)
- **Instrument:** `NVX` (fictional mid-cap industrial), **decision time:** 2027-03-15 20:00 UTC (post-close), **candidate horizon:** 8 exchange sessions.
- **Technical (price/volume, free-PIT):** NVX printed a breakout above a 60-session range on ~2.3× relative volume today; realized-vol regime elevated. *(illustrative)*
- **Macro/policy:** a proposed **tariff/tax change** on imported inputs is in committee; a **political statement** from a committee chair signaled possible escalation. PIT macro/regime vector shows a *hostile* sector regime (industrials underperforming, credit spreads widening). *(illustrative)*
- **Peer/graph (PIT peer aggregates):** a key **supplier peer** issued a negative pre-announcement this afternoon; the SIC-peer relative-strength aggregate is **weak**. *(illustrative)*
- **News/social:** a **Telegram channel** (source-trust `LIMITED_SUPPORT`, cold-start, 4 months old) posted an unverified claim of a "$400M contract win"; **media-attention accelerated** — "30 posts in 5 days." A **reliable analyst desk** (high PIT source-trust) published a note **contradicting** the contract rumor. *(illustrative)*
- **Historical analog (as-of retrieval):** the as-of analog set returns 12 prior "breakout + hostile-sector-regime + tariff-overhang" setups at ≥ adequate sample support; **outcome dispersion is wide** and the median 8-session net return is **≈ −0.4%** *(illustrative frequency, `FREQ_ANALOG · LIMITED_SUPPORT`)*.

## Trace through the decision cycle
1. **PIT universe:** NVX is in the fixed cohort as-of the cutoff (survivorship-safe).
2. **Evidence sync (availability-time + trust):** every item stamped with `feature_available_at ≤ cutoff`; the Telegram post and analyst note enter as `content_item`s with PIT `source_profile` trust (Telegram low/cold-start, analyst high). The sample's `InformationInterval` widens to the slowest admitted modality.
3. **Regime state:** hostile sector regime (feature columns, not a hard switch).
4. **Forecast (target vector, GBT):** the price/volume+digest panel yields (illustrative) terminal E[8-session absolute-executable return] `≈ +1.1%`, quantile interval `[−6.2%, +9.0%]`, and the **gate-eligible** marginal `P(return > cost) ≈ 0.52` — barely above chance, and only `LIMITED_SUPPORT` (out-of-regime coverage for this hostile regime is thin).
5. **Peer comparison:** NVX's cross-sectional rank is middling; the supplier-peer pre-announcement drags the peer-aggregate digest negative.
6. **Gross vs net edge:** `economic_edge_bps = E[abs-exec return] − round_trip_cost`. Illustrative round-trip cost `≈ 0.31%` (spread + √impact + exit leg). Net edge `≈ +0.8%` gross-of-uncertainty.
7. **Uncertainty & disagreement:** high — model disagreement up in the elevated-vol regime; the analog set's outcome dispersion is wide; a critical modality (fundamentals freshness) is **stale** (no recent filing).
8. **Horizon:** 8 is the pre-registered diagnostic here; not the frozen primary → this decision is advisory-diagnostic.
9. **Rank:** middling.
10. **Controls:** liquidity ok; but the **interaction cross-features** fire — `company_news(rumor) × source_trust(low) × price_already_moved(breakout)` routes toward REDUCE/ABSTAIN (attention-driven, low-trust, post-move); `breakout × volume_confirmation × supplier_event(negative)` is **contradictory**; `regime(hostile) × signal(bullish)` discounts the bullish read.
11. **Size or abstain — the gate runs:**
    - **Probability integrity (`11`):** the only surfacable calibrated number is marginal `P(return>cost) = 0.52 · LIMITED_SUPPORT`. The "contract win" implies a large move but is `FREQ_ANALOG`/rumor, **not** a calibrated probability — it is **not** surfaced as one.
    - **Manipulation defense (`07`, RT-10):** the bullish thesis rests on a **low-trust, cold-start Telegram source** with **accelerating attention** and is **contradicted by a high-trust analyst**. Social weight in the executable edge is **0**; attention is a **risk flag**, not confirmation. Corroboration is a single non-independent cluster → does not count.
    - **Contradiction + missing-modality:** supplier-peer contradiction + stale fundamentals raise the uncertainty premium: `required_hurdle ≥ cost + uncertainty_premium(missingness, contradiction)`.
    - **Net vs hurdle:** net edge `+0.8%` **does not clear** the uncertainty-inflated hurdle; `P(return>cost)` is only `LIMITED_SUPPORT`; the analog median is slightly negative.
12. **Evidence preserved:** supporting (breakout, volume), contradictory (supplier warning, analyst contradiction of the rumor, hostile regime, negative analog median), missing (stale fundamentals), warnings (attention manipulation risk, out-of-regime calibration).
13. **Invalidation/monitoring:** n/a (no position).

## Output (illustrative)
```
Instrument:            NVX  (FICTIONAL)
Decision time:         2027-03-15 20:00 UTC
Preferred horizon:     8 exchange sessions (diagnostic; not the pre-registered primary)
Expected terminal (abs-exec) return:   +1.1%   [illustrative]
Marginal P(return > cost):             0.52  ·  LIMITED_SUPPORT   [out-of-regime coverage thin]
P(touch +10% before session 8):        NOT_ESTIMABLE  [barrier head is RESEARCH_ONLY, barred from the gate]
Prediction interval:                   [-6.2%, +9.0%]  [illustrative; LIMITED_SUPPORT in this regime]
Estimated round-trip cost:             0.31%
Historical analog (as-of):             12 setups, wide dispersion, median 8-sess net ≈ -0.4%  (FREQ_ANALOG · LIMITED_SUPPORT)
Supporting evidence:                   range breakout on 2.3x relative volume
Contradictory evidence:                supplier-peer negative pre-announcement; high-trust analyst contradicts the contract rumor; hostile sector regime
Data-quality warnings:                 stale fundamentals; attention-manipulation risk on the Telegram source; out-of-regime calibration
Calibration support:                   LIMITED_SUPPORT
ACTION:                                ABSTAIN
Abstain reason codes:                  CONTRADICTORY_EVIDENCE · MANIPULATION_RISK · INSUFFICIENT_CALIBRATION_SUPPORT · STALE_CRITICAL_MODALITY
Suggested portfolio weight:            0.0%
```

## Why this is the right behavior
The bullish case is a **breakout amplified by an unverified, low-trust, attention-accelerated
rumor** — exactly the pattern the evidence says is **short-horizon, reversal-flavored, and
manipulable** (Da-Engelberg-Gao; Xu-Livshits) — while the reliable, high-trust evidence
(supplier warning, analyst contradiction, hostile regime, negative analog) points the other way.
The only calibrated number available is barely above chance and only `LIMITED_SUPPORT`. A naive
additive-score system might BUY on "breakout + big-contract headline + rising buzz." **This
architecture ABSTAINS**, records why, and surfaces no fabricated probability — the disciplined
professional outcome the mission demands.

*(Contrast, one line, illustrative: had the contract been confirmed by two **independent
high-trust** sources, the regime been neutral, fundamentals fresh, and marginal P(return>cost)
`WELL_SUPPORTED` above the capacity- and cost-adjusted hurdle, the same machinery would have
produced a small, size-capped **BUY** with full evidence lineage — earned, not asserted.)*
