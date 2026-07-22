# 04 — Architecture Alternatives & Decision Matrix

**Artifact type:** alternatives + decision matrix (Phase 3 output).
**Primary source:** specialist `alternative-system-architect`. The recommendation summarized
at the end is **preliminary** — it is stress-tested by the red-team (`14`) and finalized in
`05_RECOMMENDED_TARGET_ARCHITECTURE.md`. Illustrative structure only; no numbers here are
empirical claims.

---

## 0. Invariants preserved across ALL alternatives
No alternative touches the R0 truth kernel. Every design inherits unchanged: raw-vintage
OHLCV + as-of corporate actions; survivorship-safe `FixedPITCohort` with terminal-event
returns; round-trip cost with proxy floor; interval-based purge + separately-justified
embargo; trial registry → DSR/PBO on the **effective** sample; factor-residual net-of-cost
gate vs an investable benchmark; first-class `BLOCKED_NO_EDGE`; append-only ledger +
`environment_hash` + deterministic replay; and the AI/LLM advisory boundary.

**The cross-cutting mechanism that makes multimodality cheap (used by every alternative).**
The canonical content addendum already carries per-item availability timestamps
(`published_at`, `publicly_available_at`, `provider_ingested_at`, `system_available_at`) and
`content_enrichment.feature_available_at`; `source_profile` is an append-only **PIT** trust
snapshot (`profile_as_of_at`, reliability, cold-start). This *is* the "per-modality
availability-time + source-trust layer." Its payoff is structural: **a new modality inherits
the existing leakage machinery for free iff (a) its `feature_available_at` is honestly
stamped, and (b) the sample's `InformationInterval.information_interval` is widened to the
max availability-time across all modalities feeding that sample** — so §0.5 interval-purge/
embargo automatically covers the slowest modality. No new embargo concept; the only delta is
honest per-modality stamping (estimated timestamps ⇒ INFORMATION_THEORETIC replay only +
trust down-weighting). **Source-trust must itself be PIT** (`profile_as_of_at ≤
prediction_time`) — using a currently-learned reliability score is look-ahead.

**Two target-semantics facts shaping every alternative.**
1. The single scalar `TargetBasis.ABSOLUTE_EXECUTABLE_RETURN` is insufficient for the ~16
mission outputs — but path quantities (P(touch), time-to-target, MFE, MAE, drawdown) are
**labels computable from the historical price path**, which *any tabular model can regress
on*. A sequence model is justified only if it *predicts* them better net-of-cost. (This
separates A from B.)
2. Richer path targets **require barrier geometry** (triple-barrier/meta-labeling), reopening
deferred ADR-005; barrier params are researcher DoF that must be frozen + stress-tested, and
every extra head/horizon/target-type is a **DSR trial**. "Richer semantics" trades
scalar-poverty for multiple-testing burden.

**The 16 target outputs** each alternative is mapped against: (1) terminal E[return] · (2)
median · (3) quantiles/intervals · (4) P(positive) · (5) P(exceeds cost) · (6) P(exceeds
threshold) · (7) P(touch before H) · (8) E[time-to-target] · (9) MFE · (10) MAE · (11)
drawdown distribution · (12) market/sector-relative · (13) cross-sectional rank · (14)
portfolio utility · (15) action · (16) size.

---

## Alternative A — Trust-Gated Tabular Multimodal Panel *(no deep sequence)*
**Thesis / central bet.** Reduce every modality at the PIT cutoff to small engineered scalar
digests; concatenate into one cross-sectional panel row per (instrument, date); a single GBT
ensemble fuses them (tree splits *are* interactions). Multiple tabular heads emit the target
vector. **Bet:** modality information is compressible to PIT scalar digests without losing
tradable net-of-cost signal, and trees + a small frozen named cross-feature set capture the
needed interactions.
```
 PIT SOURCES     AVAILABILITY-TIME + TRUST LAYER        TABULAR FUSION         TARGET-VECTOR HEADS        DECISION
 (OHLCV,     ┌─────────────────────────────────┐   ┌────────────────┐   ┌──────────────────────────┐  ┌──────────┐
  EDGAR/SIC, │ content_item.feature_available_at│   │ ONE row per     │   │ quantile-reg → 1,2,3      │  │ abstain  │
  ALFRED, ──►│ source_profile(as_of) trust      ├──►│ (instrument,    │──►│ barrier meta-label → 4-7  │─►│ gate +   │─► action
  news,      │ widen InformationInterval to MAX │   │  date): price/  │   │ excursion-reg → 9,10      │  │ OOD/drift│  {BUY,HOLD,
  social)    │ availability; missingness = feat │   │  vol + modality │   │ excess-basis → 12         │  │ +contra. │   REDUCE,
             └─────────────────────────────────┘   │  digests + xfeat│   │ (each head own calibration)│  └────┬─────┘   EXIT,ABSTAIN}
                                                    └────────────────┘   └──────────────────────────┘       │       +size
                                   GBT primary + elastic-net comparator; FeatureSnapshot seals schema+values │
                        cost/factor-residual/DSR gate → cross-sectional rank(13) → portfolio-utility alloc(14,16) ◄─┘
```
- **Missing modalities:** native — GBT consumes NaN; each modality adds `is_missing` + `staleness_hours` columns; a tree can route missingness to a *different* leaf than sentiment≈0 ("missing news ≠ neutral news").
- **Target semantics:** ~14/16 directly (1,2,3,4,5,6,7,9,10,12,13,14,15,16); weak on 8 (time-to-target, censored) and 11 (drawdown *distribution* — only an MAE-quantile proxy). Point-and-quantile, not path.
- **Interactions/inheritance:** interactions inside trees + a small *frozen, named* cross-feature set (`regime×signal`; `breakout×volume×supplier-event`; `attention_spike×source_trust×price_already_moved`). Additive-free (a tree path is a conjunction). PIT/leakage inheritance automatic via §0.
- **Compute/ops:** LightGBM/XGBoost, CPU, seeded → strong two-tier determinism; minimal deps; NLP digests offline (FinBERT-as-feature/lexicon), no online LLM in the decision path. Free-PIT covers prices/fundamentals/macro; news/social gated → INFORMATION_THEORETIC only, added last. **Lowest incremental burden over R0; solo-feasible.**
- **Smallest falsifying experiment:** on one horizon + effective sample, does GBT on price/vol + **one** modality digest beat GBT on price/vol only — factor-residual, DSR-deflated, net-of-cost, on the top-2 liquidity quintiles? If no digest clears → collapses to fallback. Second: does GBT-on-concatenated-digests match a small learned fusion MLP net-of-cost? If the MLP wins materially, A's "no fusion net" bet weakens.

## Alternative B — Causal Sequence Encoders *(feature producers / forecasters)*
**Thesis / central bet.** Static digests discard path shape (price dynamics, news arrival
pattern, attention build-up). Causal (strictly backward) per-modality encoders distill these
into embeddings that beat the static digest net-of-cost. **B1 (recommended form):**
encoder = feature producer; embeddings enter the *same* GBT panel/calibration/cost/audit as
A (the sequence net never decides). **B2:** causal TCN/TFT with quantile heads emits the full
multi-horizon path distribution directly. **Bet:** exploitable path structure beyond any
static digest survives net-of-cost, and the tiny effective sample doesn't overfit it away.
```
                     ┌── price/vol causal encoder ─┐
 PIT ─trust(§0)─►    ├── news-stream causal enc.   ├─► per-modality embeddings ─┐ + learned "MISSING" mask token
 (same layer)        ├── attention causal enc.     │                            │
                     └── filings event encoder ─────┘                            ▼
         B1: embeddings ─► GBT panel ─► [SAME tail as A: heads→calib→cost/DSR→rank→alloc→abstain]
         B2: attention fusion ─► multi-horizon quantile forecaster ─► native path dist (1,2,3,7,8,9,10,11) ─► calib→cost/DSR→rank→alloc→abstain
```
- **Missing modalities:** per-modality mask tokens / learned "missing" embeddings; fusion attention down-weights but gives absent modalities a *distinct* representation. Elegant but validation-expensive (extra params on a tiny sample).
- **Target semantics:** shares A's ~14, and is the **only** design natively producing 11 (predictive drawdown *distribution*) and sharper 7/8/9/10 — its honest reason to exist.
- **Interactions/inheritance:** cross-modal attention (news-token attends to regime-token). **Largest leakage surface** (windows straddling the cutoff); requires strict causal masking + per-window availability stamping + purge-disjoint calibration.
- **Compute/ops:** GPU; cuDNN non-determinism threatens bit-exact repro; **highest validation cost** (CPCV over a data-hungry model on the tiniest sample). Needs new `ModelProducer` members. **R4 replaceable challenger, never an MVP dependency.**
- **Smallest falsifying experiment:** freeze A; add sequence embeddings (B1) as extra columns; does A+embeddings beat A net-of-cost, factor-residual, DSR-deflated under identical CPCV? If a cheap static digest matches/beats the encoder (the DLinear prior, Zeng 2023), B is falsified.

## Alternative C — Portfolio-Utility-First *(decision is the spine)*
**Thesis / central bet.** Invert the pipeline: optimize/gate **portfolio utility net-of-cost**,
not per-stock forecast accuracy, because effective sample is tiny and net survival is
dominated by turnover/cost/sizing/regime-robustness. Forecast is a nuisance input; deliverable
is an allocation/action; evaluated at the portfolio level. **Bet:** the binding constraint is
decision/portfolio quality, so a deterministic frozen-prior constrained allocator (not a MV
optimizer, which loses to 1/N OOS) fed by a modest forecast and stress-tested across regimes
beats "improve the forecast then allocate naively."
```
                       ┌─────── SCENARIO / REGIME OVERLAY ───────┐
 forecast head (A/B) ─►│ perturb μ/σ/tail by regime deltas;      │
 (subordinate: μ,σ,q)  │ weight by PIT state_probability;        │
                       │ contradiction across modalities → widen σ│
 PIT ─trust(§0)─►digests┴────────────────┬────────────────────────┘ (regime vector: SPY trend, VIX, breadth, rates)
                                          ▼
        ║ deterministic penalized-utility allocator (frozen λ) → greedy risk-budget sizing ║
        ║ → concentration/sector/factor caps → turnover/hysteresis → worst_plausible_state_utility ║
                                          ▼
        portfolio-utility net-of-cost gate (DSR at PORTFOLIO level) → action / abstain / size
```
- **Missing modalities:** a missing modality is a missing *scenario dimension* → its regime delta defaults to prior but *raises the uncertainty premium* in the hurdle → tightens abstention (`required_hurdle ≥ cost + uncertainty_premium(missingness)`).
- **Target semantics:** consumes 1–13 from a forecaster; **native** 13,14 (incl. `worst_plausible_state_utility`),15,16. Produces robust *decisions*, not distributions.
- **Interactions/inheritance:** scenario-conditioned utility deltas (not additive). Allocator deterministic+frozen → adds **no** multiple-testing burden itself. Requires whole-decision calibration (realized net return on predicted utility: slope≈1, intercept≈0).
- **Compute/ops:** cheap, deterministic. But **effective-sample bites hardest** — portfolio-level independent episodes are the fewest (single-digit regime episodes/yr) → most sample-starved gate. Greedy marginal-utility only; **no MV optimizer** (DeMiguel).
- **Smallest falsifying experiment:** does the frozen-prior allocator + overlay beat (a) 1/N on the top-k forecast-ranked names and (b) equal-weight-top-k with no overlay, OOS net-of-cost at the portfolio level? If ≤ naive-allocation-on-a-good-forecast, C's "decision-first > forecast-first" bet is falsified.

## Alternative D — Evidence-Graph / Abstention-First *(epistemics is the spine)*
**Thesis / central bet.** Promote the abstain-on-bad-evidence requirement to the organizing
principle. The scarce, defensible object is a **calibrated, trust-weighted evidence ledger**
per decision; first-class output is {ACT, ABSTAIN}+reason; probabilities are emitted only when
evidence is complete/fresh/corroborated/in-distribution/calibrated. Modalities are nodes;
interactions are **typed edges** (`confirms`/`contradicts`/`conditions`) weighted by PIT
source-trust. **Bet:** most net-of-cost value comes from *not trading* on bad evidence, not
from sharper point forecasts.
```
 PIT ─► ┌─────── EVIDENCE / TRUST SPINE (runs FIRST) ───────┐
        │ availability-normalize · entity-resolve→instrument_id │
        │ PIT source_profile trust · dedup · staleness          │
        │ typed graph: news─contradicts→rumor;                  │
        │  earnings─confirms→breakout; regime─conditions→news   │
        │ GATE: completeness·freshness·contradiction·OOD/drift· │
        │       calibration-freshness                          │
        └───────────────┬──────────────────────────────────────┘
             NO → ABSTAIN(reason)     YES → forecast head (A/B) → calib → cost/DSR → rank → alloc → action+size
```
- **Missing modalities:** treated most seriously — missing → completeness drops → gate ABSTAINs or forecasts under an explicit `missing_component_policy` with inflated uncertainty premium (enforced *upstream* of the forecaster).
- **Target semantics:** native 15 (esp. high-quality ABSTAIN) + trust/contradiction/OOD meta-scores gating whether 1–11 are emitted; distributions come from the downstream head. Distinct contribution: abstention quality + manipulation resistance.
- **Interactions/inheritance:** most *explicit* interaction model (typed PIT-trust-weighted edges). The **GNN form is a leakage-prone research bet** (Feng 2019 single-study; cheap PIT peer aggregates à la Bhojraj-Lee-Oler are a strong baseline); the **rule/score form** is cheap, deterministic, and the part worth adopting now.
- **Compute/ops:** low in score form; high engineering burden (connectors, entity resolution, dedup, PIT source-profile). Heaviest news/social persistence + licensing. Strongest manipulation resistance.
- **Smallest falsifying experiment:** (a) are ABSTAIN-flagged decisions' realized net utility *worse* than ACT-flagged (base-rate matched)? If not, the gate is noise. (b) on labeled pump-and-dump/attention-spike episodes (Xu-Livshits; Da-Engelberg-Gao), does the gate abstain materially more than a rate-matched random abstainer? If not, the trust machinery earns nothing.

**Variant E — regime-conditioned mixture/ensemble** (route to a regime-specific GBT via a PIT
regime label): a *technique* usable inside A/C, not a full spine. HMM/regime classifiers are
OOS-fragile (A3) — keep the regime vector as **deterministic feature columns**, not a hard switch.

---

## Decision matrix
▲▲ strong / ▲ ok / ▽ weak / ▽▽ poor.

| Axis | A Tabular | B Sequence | C Portfolio-first | D Evidence/abstain |
|---|---|---|---|---|
| Net-of-cost defensibility | ▲▲ | ▽ | ▲ | ▲ |
| Leakage surface | ▲▲ | ▽▽ | ▲ | ▽ |
| Calibratability | ▲▲ | ▲ | ▲ | ▲ |
| Effective-sample demand | ▲▲ (lowest) | ▽▽ (highest) | ▽ | ▲ |
| Complexity / validation cost | ▲▲ (lowest) | ▽▽ | ▲ | ▽ |
| Data availability / licensing | ▲ | ▲ | ▲▲ | ▽ |
| Manipulation resistance | ▲ | ▲ | ▲ | ▲▲ |
| Operational burden | ▲▲ (closest to R0) | ▽ | ▲ | ▽▽ |
| Preservation of R0 foundations | ▲▲ | ▽ | ▲ | ▲▲ (extends it) |

**Cross-cutting:** every alternative faces the same base rate — net short-horizon
cross-sectional edge is likely ≈0 after costs outside liquid low-turnover names — and each
added head/horizon/modality/target-type is a DSR trial. Complexity does not relax the gate; it
raises the trial count the gate must overcome.

## Preliminary recommendation *(finalized in `05` after red-team `14`)*
- **TARGET → Alternative A.** Only design that preserves R0 nearly verbatim, gets multimodal
fusion + non-additive interactions ~free from tree splits, delivers ~14/16 outputs (MFE/MAE/
touch as *labels*), and has the smallest leakage surface / lowest sample demand / best
determinism / best solo feasibility. A *adopts* D's availability-time + trust ingestion layer
and D's rule/score abstention gate, and is *evaluated* on C's portfolio-utility net-of-cost
gate with whole-decision calibration. The genuinely-new-vs-V5 content is the trust-layer
ingestion contract, the multi-head target vector (reopening ADR-005 barrier geometry with
frozen params), and per-decision abstention with OOD/drift.
- **SIMPLER FALLBACK → "Edge-Probe+"** = A with all modalities off (price/volume-only GBT +
quantile/barrier heads + abstention). Built **first**; shipped if no modality clears its
ablation. Each modality switched on only when its ablation beats this baseline net-of-cost,
factor-residual, DSR-deflated, on effective sample. If even Edge-Probe+ fails → `BLOCKED_NO_EDGE`.
- **RESEARCH CHALLENGER → Alternative B1** (sequence-as-encoder), R4-gated; sanctioned only for
the path targets A approximates weakly (drawdown distribution; sharper touch/time/MFE/MAE), and
admitted only if it beats A net-of-cost under identical PIT/cost/CPCV/DSR. Second-tier
(recorded, not designated): D's GNN form (must beat cheap PIT peer aggregates first) and
analog/RAG retrieval (thin, leakage-prone).

## Concrete schema-level deltas to the frozen R0 *(least-invasive unpinning)*
- **`TargetBasis` + `LabelRecord`:** keep the schema; add enum members (`MARKET_EXCESS_RETURN`,
`SECTOR_EXCESS_RETURN`) and **barrier/excursion target-types** as *multiple `LabelRecord` rows*
per (instrument, prediction_time, horizon, target_type), each with its own
`target_definition_version` encoding frozen barrier params. Reopens ADR-005.
- **`HorizonSessions{5,8,14}`:** do **not** widen (each horizon = a DSR trial); add barrier
target-types *at the same horizons*; count every head/target-type in the trial registry.
- **`ModelProducer`:** admit modality-encoder/sequence-encoder producers as trial-registered
CHALLENGERs; keep `BASELINE_GBT` primary, `PER_DATE_ORACLE` diagnostic-only.
- **`OutputType{CONTINUOUS_RETURN,PROBABILITY}`:** sufficient; quantile heads = CONTINUOUS_RETURN
(interval-coverage), barrier/meta-label heads = PROBABILITY (isotonic/Platt+ECE); each head its
own `CalibrationArtifactManifest`.
- **`InformationInterval`:** the single most important delta — compute `information_interval` as
the **max availability-time across all modalities** feeding the sample.
- **Adopt the addendum entities** (`content_item`, `content_enrichment`, `content_market_link`,
`source_profile`, PIT append-only) as the ingestion contract, unchanged.
- **Per-decision abstention:** add a per-decision abstain reason-code + OOD/drift score to the
decision/forecast records (distinct from run-level `BLOCKED_NO_EDGE`).
