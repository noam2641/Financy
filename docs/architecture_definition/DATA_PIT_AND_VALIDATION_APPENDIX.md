# Data, Point-in-Time, and Validation Appendix (Deliverable E)

**Program:** AI Trading Decision Platform for US Equities — Phase 1 (Evidence Spine). Sources: agents A2 (PIT-data), A1 (validation methodology), A5 (execution/cost realism).
**Research cutoff:** 2026-07-21. **Status:** Evidence + graded assessment only. Current-only metadata is never described as point-in-time historical data. Grades A/B/C/D/UNSUPPORTED per Phase-0 rules.

> **PHASE 1.5 CORRECTION BANNER.** (1) **SIC is NOT a transparent replacement for GICS** — it is a *different* taxonomy that redefines the target and peer groups. Sector-classification is a **five-option owner decision** (paid PIT GICS / free PIT SIC-with-new-target / market-excess primary / absolute-return primary / sector-excess-as-secondary-diagnostic), fully compared in `PHASE_1_EVIDENCE_INTEGRITY_REVIEW.md` §4 (see §5 below, now scoped to that comparison). (2) **Not all adjusted data is invalid** — a **split multiplies prior prices by a constant that CANCELS in simple returns** but corrupts price *levels*; dividend/total-return adjustment corrupts *returns*. Use-by-use safe/unsafe matrix: integrity review §5. (3) **Cost figures are evidence-informed scenario ranges, not verified point estimates** (several source PDFs 403'd; `CLAIM_TO_SOURCE_TRACEABILITY.md` CLM-COST/CLM-TURN). (4) Provider claims graded on five dimensions in `SOURCE_EVIDENCE_REGISTER.md`.

---

## 1. Provider Assessment (design-time; repo has no data loaders)

| Provider | Info-time (public-avail) | System-avail | Revisions | Licensing | Rate limit | Est. cost/mo | Replay class | Release stage | Classification | Kill criterion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **yfinance (prices/CA)** | Partial; back-adj **leaks future** | **None** (single snapshot) | None | Personal/non-commercial, unofficial scrape | Undocumented/throttled | $0 (proto) | INFORMATION_THEORETIC only, *and only with raw-basis fix* | R0/R1A prototyping only | **MVP_OPTIONAL (proto) / REJECTED for production** | Any shadow+ use w/o licensed replacement; immediate if `auto_adjust=True` used for labels |
| **SEC EDGAR (as-filed + accepted-datetime)** | Yes (accepted time) | Yes (own ingest) | Yes (amendments/first-print) | Public domain | ~10 req/s fair use | $0 | Both (as-filed = genuine PIT) | R2A fundamentals; **SIC sector usable earlier** | **MVP_OPTIONAL → RESEARCH_CHALLENGER (SIC sector)** | `companyfacts`-latest used without as-filed keying |
| **FRED (plain)** | No (returns revised) | No | No | Permissive | 120 req/min | $0 | Neither for historical | — | **REJECTED for historical PIT** | Any historical macro without real-time params |
| **ALFRED (FRED vintages)** | Yes (first-release) | Modeled | Yes (vintages) | Permissive | as FRED | $0 | INFORMATION_THEORETIC (genuine) | R2A macro-sector | **MVP_OPTIONAL (required-if-macro)** | Loader ignores `realtime_start`/`vintagedates` |
| **PIT GICS sector membership** | Paid only | n/a | Paid (from/thru) | MSCI/S&P license required | vendor | commercial (quote-based; UNSUPPORTED exact) | n/a | Only if licensed | **DEFERRED / REJECTED for free tier** | Sector-excess retained as primary without license → target UNAVAILABLE |
| **SIC sector (from EDGAR)** | Yes | Yes | Yes | Public domain | ~10 req/s | $0 | Both (genuine PIT) | R0/R1A viable | **RESEARCH_CHALLENGER (free PIT sector substitute)** | Coarseness fails sector-benchmark contract tests |
| **Free index membership (EODHD/Wikipedia/ETF)** | Approx | No | Partial (from ~2000) | Mixed | vendor | $0–low | INFORMATION_THEORETIC (approx) | R0 universe (with caveats) | **MVP_OPTIONAL** | Membership-change dates unverifiable → survivorship risk |
| **Free news (GDELT/Finnhub free)** | Yes (pub time) | No | No | Restricted redistribution | tiered | $0–low | INFORMATION_THEORETIC only | R2A | **DEFERRED** | Any body persistence before licensing gate |

Fetch honesty: several official pages (SEC, Cambridge/JFQA, NBER, some SSRN) returned HTTP 403 through the environment proxy; provider *behaviors* above are well-established and corroborated across multiple search extractions (graded A/B accordingly), not fabricated.

---

## 2. Bitemporal & Replay Strategy

- **Six time fields** (REQ-TIME-003): `event_time ≤ provider_published_at ≤ publicly_available_at ≤ system_available_at ≤ feature_available_at ≤ decision_cutoff_at` — recommend this monotonic chain be made a **normative invariant + hard PIT gate** (currently undefined ordering; A2/PIT).
- **`system_available_at` does not exist before the system runs.** For any pre-go-live backtest it must be **estimated** (`is_estimated_timestamp=true`, REQ-TIME-004) or omitted. **Therefore: pre-go-live backtests are `INFORMATION_THEORETIC_REPLAY` only**; `SYSTEM_REALISTIC_REPLAY` accrues *forward* once the system records its own ingestion timestamps. Fabricating `system_available_at = publicly_available_at` makes the two replay classes identical and defeats REQ-TIME-006 — forbid it.
- **Correction replay** (REQ-TIME-008): keep `research_latest_truth_replay` vs `historical_system_state_replay` distinct; never mix without labeling.

## 3. Corporate-Action & Price-Basis Strategy

- **Ingest raw** (`auto_adjust=False, back_adjust=False`); persist raw OHLC + a **separate, versioned corporate-action table**; derive adjusted series on demand with `corporate_action_version` + `split_adjustment_factor` (REQ-PRICE-004). Orders/stops/fills use **raw** (REQ-PRICE-002); technical features may use split-adjusted **as-of `ex_date ≤ cutoff`**.
- **REQ-LAB-001 must declare `price_basis`** (recommend: raw open entry; declared split-adjusted or total-return close exit with `dividend_treatment`), bound to `target_definition_version`. Without this the research target silently inherits back-adjusted (future-leaking) prices.
- Reconcile splits/dividends against an independent source; treat Yahoo adjustments as unverified (non-deterministic across pulls).

## 4. Universe & Survivorship Strategy

- Construct even the "static" R0 universe **as-of backtest-start**, including names later delisted/merged/bankrupt (PIT constituent snapshot); freeze membership from that date. Forbid universe construction from *currently-resolvable* tickers (survivorship + look-ahead).
- Maintain `instrument_master` + `instrument_identifier_history` with opaque `instrument_id` (never derived from ticker), `delisting_date/reason/successor_instrument_id`, and terminal-event returns (REQ-LAB-013). Source CIK (SEC) / FIGI (OpenFIGI) free; **ban ticker as a join key**.

## 5. Sector-History Strategy (the primary-target dependency)

- The default `primary_ranking_target = sector_excess_return_h` (REQ-LAB-006) needs **PIT sector membership** (REQ-LAB-009), which for GICS is **proprietary/paid** and **contradicts** R0/R1A's exclusion of sector modules. Owner must choose (Phase 2): **(1)** re-designate primary to `market_excess_return_h`/`absolute_return_h` and mark sector-excess UNAVAILABLE (REQ-LAB-010 permits it); **(2)** adopt free-PIT **SIC** sector taxonomy from EDGAR (`sector_taxonomy=SIC`, coarser but genuinely PIT); or **(3)** license GICS History.

## 6. Restatement Strategy (Release 2+, schema frozen now)

- Build the fundamentals store from **as-filed submissions keyed on `accession_number` + `filing_accepted_at`**; set `fact_valid_from`/`fact_superseded_at` from accepted-datetime ordering; never overwrite (REQ-DATA-007). Add `filing_system_available_at`. The `data.sec.gov/companyfacts` convenience view returns latest-restated by default — do **not** trust it for as-of features.
- Macro: **ALFRED with `realtime_start`/`vintagedates`** for any historical series; store the vintage as `provider_published_at`/`valid_from`.

## 7. Feature Availability, Fit-Isolation & Train/Serve Parity

- Fit-isolation (REQ-FEAT-003) must cover **scalers, imputers, PCA, feature selection, the probability-calibration layer, and any meta/stacking learner** — extend the enumeration. Persist fitted-transform params + `fit_window_id` + checksum in `feature_snapshot`; require `latest_features_df` to reuse the frozen transform.
- **Schema-hash parity ≠ value parity.** Add a **golden train/serve value-parity test**: for a fixed as-of timestamp, `training_df` row == `latest_features_df` row within tolerance (not just schema-hash equal). Seal a `feature_values_checksum` on `feature_snapshot`.

## 8. Validation Protocol (consolidated)

1. Grouped-by-date cross-sectional folds; **CPCV** (combinatorial purged) in addition to purged walk-forward.
2. Purge training rows whose label intervals overlap test; **embargo ≥ max(label_horizon)=14 + feature memory**; purge **both directions** on the cross-sectional date union.
3. Nested CV for any meta-layer; **out-of-fold calibration** disjoint from the ECE-evaluation slice.
4. **Deflated Sharpe Ratio + trial registry** (every config/seed/target/horizon/barrier-grid counts as a trial; per-name horizon selection counts); **PBO/CSCV** (forbid `PBO_NOT_ESTIMABLE` as a pass).
5. Block bootstrap CIs with block length ≥ horizon; report **effective sample size** and IC autocorrelation, not raw row count.
6. **Factor attribution/neutralization** (Mkt, SMB, HML, UMD, ST-Reversal, BAB) → residual net-alpha significance drives promotion.
7. **Investable net-of-cost benchmark** (buy-and-hold SPY + sector basket, beta-adjusted) as a co-equal hurdle to the naive-forecast comparator.
8. Capacity, signal half-life, churn (upgrade SHOULD→MUST); cost-stress (empirical spread/ADV per liquidity bucket, not a flat 2×).
9. Locked holdout with frozen thresholds; paper revalidation of edge against realized R3 costs before any live promotion; live-decay monitoring.

## 9. Leakage / Realism Threat Model (distinguish the mechanism)

| Threat | Mechanism | Control |
| --- | --- | --- |
| Corporate-action look-ahead | Back-adjusted prices embed future splits/divs | Raw-basis ingest + as-of adjustment (§3) |
| Survivorship | Delisted names absent | PIT constituent snapshot (§4) |
| Sector-classification look-ahead | Today's GICS applied to history | PIT SIC / licensed GICS-history (§5) |
| Restatement leak | Latest-restated fundamentals in as-of features | As-filed keying (§6) |
| Macro revision leak | Latest-revised FRED series | ALFRED vintages (§6) |
| Fit-window leakage | Scaler/calibrator/meta fit on train+test | Extend fit-isolation; seal transforms (§7) |
| Train/serve skew | Same schema, divergent values | Value-parity test (§7) |
| Statistical dependence (not leakage) | Overlapping labels inflate IC-IR | Effective-N / block bootstrap (§8.5) |
| Multiple testing (not leakage) | Large config surface | DSR + registry + PBO (§8.4) |
| Distribution shift | Regime change | Drift monitors; walk-forward |
| Provider revision | Yahoo re-states history | Versioned corporate-action set; idempotency test |
| Implementation error | Wrong basis / off-by-one horizon | Golden fixtures; PIT invariant tests |

## 10. Execution-Cost & Realism Model (A5)

- **Round-trip, two-sided** cost: add an explicit **exit/close-auction leg**; `pretrade_expected_cost_bps` must be round-trip (REQ-COST-001 currently has one entry-side `open_auction_cost_bps` only).
- **PROXY open-fill** needs a numeric floor (worst-of open vs first-N-min bar + widened spread), not just "conservative."
- **Cost by liquidity bucket** (literature-anchored ranges; point figures graded C): large/mega ≈10–30 bps round-trip; mid ≈40–100 bps; small ≈100–500 bps; micro ≈200–2000+ bps. Impact scales ≈ √(size/ADV) (Almgren exponent ≈0.5–0.6). Freeze `maximum_ADV_participation` / `maximum_spread` / order-size caps (all TBD).
- **Gap-through-stop:** size to the **worst-case overnight/earnings gap**, not to `planned_stop_distance_pct` (REQ-RISK-002 inverts notional to stop distance → max notional on max gap risk); flag earnings-in-horizon for 5/8/14-session holds.
- **Label ↔ PnL:** gate must demonstrate concordance between fixed-horizon IC and post-stop/target/time-stop realized PnL, or rank on an executable objective.

## 11. Mandatory PIT / Leakage Tests (architecture-level obligations)

1. Split-after-feature-date: as-of features invariant to a later split.
2. Label price-basis golden fixture: split **and** dividend inside the horizon window → hand-computed label match under declared basis.
3. Sector reclassification: label for date *d* uses membership effective ≤ *d*.
4. Restatement: 10-K then 10-K/A → two rows, distinct `fact_filed_at`, as-of feature = first-print.
5. Macro vintage: revised series yields different past value under first-release vs latest.
6. Monotonic timestamp-chain invariant per `source_record` and `feature_snapshot`.
7. Fit-isolation: transform fit-indices ⊆ training window; calibration ∩ ECE-eval = ∅.
8. Train/serve value parity within tolerance on a frozen date.
9. Fold manifest: `min(test_date) − max(train_label_end) ≥ embargo (≥14 + feature memory)`.
10. Synthetic forward-return feature at fold boundary → OOS IC ≈ 0 (leakage tripwire).
11. Survivorship: R0 universe as-of start contains then-delisted names.
12. Replay: SYSTEM_REALISTIC refuses rows with null/estimated `system_available_at`.

## 12. Source Entries (consolidated for E; grades as assigned)

Provider/PIT: yfinance `auto_adjust` default + issues [B]; Yahoo API ToS [B]; MSCI/S&P GICS proprietary + paid PIT history [A]; SEC EDGAR accepted-datetime / as-filed vs companyfacts [A/B]; FRED/ALFRED real-time & vintage params [A/B]; EODHD/Wikipedia constituents [C]; GDELT/Finnhub/NewsAPI terms [C]. Validation/cost: McLean-Pontiff [A]; Chen-Velikov [A]; Novy-Marx-Velikov [A/B]; Avramov-Chordia-Goyal [A]; Hou-Xue-Zhang [A]; Harvey-Liu-Zhu [A]; Bailey & López de Prado DSR/PBO [A/B]; Boudoukh-Israel-Richardson / overlapping-obs inference [B]; Frazzini-Israel-Moskowitz [B]; Patton-Weller [B]; JFQA auction impact [B]; Corwin-Schultz [B]; Almgren impact [B]; López de Prado AFML [C]. (Full extraction fields recorded in the per-agent Round-1 reports; consolidated here by theme.)
