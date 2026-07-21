# Phase 1 Evidence Integrity Review (Phase 1.5)

**Purpose:** make the Phase-1 evidence base auditable, correct overstatement, and impose precision on target/data/validation/model/governance/AI before any owner decision. Documentation-only. Canonical v4.6 unmodified.

---

## 1. Independence Terminology Correction (applies everywhere)

The eight Round-1 reviewers were **context-isolated Claude subagents** — separate context windows, no cross-visibility in Round 1, each assigned a contradictory hypothesis. They are **NOT fully epistemically independent validators**:
- **all agents used the same model family/provider**; shared-model priors can produce **correlated errors** (they may agree *because they reason alike*, not because a claim is true);
- **agent count does not determine evidence grade**;
- **evidence grade derives from source quality, platform-applicability, and independent lines of external evidence** — see `SOURCE_EVIDENCE_REGISTER.md` (five-dimensional grades) and `CLAIM_TO_SOURCE_TRACEABILITY.md`.
Deliverable A and the Round-2 doc were updated to use `MULTI_AGENT_CONSENSUS` / `MULTI_SOURCE_CORROBORATED` / `SINGLE_AGENT_SUPPORTED` / `UNCONTRADICTED` / `DISPUTED` / `UNRESOLVED`, and to stop calling context-isolation "genuine independence."

## 2. Consensus Reclassifications
- **CX-11 (solo governance cap): reclassified SINGLE_AGENT_SUPPORTED / UNCONTRADICTED** (A6 only) — previously written as "Consensus." A second genuinely independent analysis has not corroborated it.
- All other CX clusters retain ≥2-agent support **and** were re-checked for independent external corroboration (Round-2 doc). Where support is a single external line (e.g., CLM-EFFN derivation), the item is labeled INFERENCE, not evidence.

## 3. Governance-Source Applicability (SR 11-7 / SR 26-2)
Relevance classification (per mandate): **INDUSTRY_BEST_PRACTICE / ANALOGICAL_GUIDANCE — NOT LEGALLY_APPLICABLE** to this project on the evidence gathered. SR 11-7 / SR 26-2 are US Federal Reserve / OCC **bank** supervisory expectations; no legal-applicability determination for a private, non-bank research project has been made. Independent validation and two-person kill-switch controls are therefore recommended as **INTERNAL_POLICY_CHOICE informed by best practice**, and the solo→RESEARCH/SHADOW cap is an internal policy recommendation, **not** a legal requirement. (Legal applicability is itself an owner/counsel decision — Phase-2 packet 17.)

## 4. Target Precision — GICS vs SIC and Five Distinct Options
**SIC is NOT a transparent replacement for GICS** (CLM-SIC downgraded). The following are **five separate decisions**, each with different semantics/consequences (feeds Phase-2 packet 9):

| Option | Target semantics | Data availability | PIT validity | Peer-group construction | Expected statistical effect | Cost / licensing | Migration impact | Reversibility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **1. Paid PIT GICS** | `sector_excess` vs GICS sector-of-the-day | Commercial (MSCI/S&P "GICS History") | High (from/thru-dated) | Market-oriented, revised | Cleanest sector-relative signal | License required; cost UNSUPPORTED (quote) | Full sector module; licensing lead-time | Reversible (drop license) |
| **2. Free PIT SIC (new taxonomy + target)** | **SIC-excess** (a *different* target) vs SIC group-of-the-day | Free via EDGAR accepted-datetime | High (as-filed) | Legacy, self-reported, coarse/slow | Noisier peer groups; weaker/possibly-different signal (EMPIRICAL_TBD) | $0 | Redefine target + peer construction; new label tests | Reversible but target changes |
| **3. Market-excess primary** | `market_excess` vs a versioned market benchmark (SPY) | Free (SPY) | High | Single benchmark | Removes sector confound only partially; simplest | $0 | Re-designate primary; least sector data | Reversible |
| **4. Absolute-return primary** | `absolute_return` (executable) | Free (raw prices) | High | None (per-name) | Highest beta exposure; simplest to trade | $0 | Re-designate primary; **beta cap required** | Reversible |
| **5. Sector-excess as secondary diagnostic only** | Ranking/diagnostic, never gating | Whatever sector source is available | Depends on source | As available | Sector-neutral *ranking* input without a gating claim | $0–license | Keep as `alpha_score` input; not in `economic_edge_bps` | Reversible |

**Recommendation (PROPOSED, not approved):** MVP primary = **absolute-executable or market-excess** (options 4/3) with **sector-excess retained only as a secondary ranking/diagnostic input** (option 5); paid GICS (1) or SIC (2) considered only if a sector-relative *objective* is later justified. This resolves CX-2's absolute-vs-relative cost incoherence and the free-PIT gap simultaneously.

## 5. Price-Basis Decision Matrix (use-by-use look-ahead) — "not all adjusted data is invalid"

Distinguish five series and their **safe/unsafe** uses. Key mechanism (CLM-YFIN): a **split** multiplies all prior prices by a constant → it **cancels in simple returns** but corrupts **price levels**; **dividend/total-return** adjustment injects future dividends → corrupts **returns/labels**.

| Series | Labels | Returns | Price-level features (52w-high, S/R, Bollinger levels) | Liquidity filters (dollar-volume) | Min-price filter | Universe construction | Execution simulation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Raw tradable OHLCV** | **Safe** (declare basis) | Safe | Safe | Safe | Safe | Safe | **Required** (orders/stops/fills) |
| **Split-adjusted analytical** | Safe if consistent as-of | **Safe** (split cancels) | **Unsafe if current-vintage** (future splits leak into levels) | **Unsafe if current-vintage** | **Unsafe if current-vintage** | Unsafe if current-vintage | Unsafe |
| **Total-return series** | **Unsafe** for price-return labels (future dividends) | **Unsafe** (dividend leak) | Unsafe (level) | Unsafe | Unsafe | Unsafe | Unsafe |
| **As-of corporate-action-adjusted** (`ex_date ≤ cutoff`) | **Safe** | **Safe** | **Safe** | **Safe** | **Safe** | **Safe** | Safe (analytical) |
| **Current-vintage back-adjusted** (yfinance default) | **Unsafe** | Safe for simple split-only returns; **Unsafe** with dividends | **Unsafe** (leaks future CAs) | **Unsafe** | **Unsafe** | **Unsafe** | Unsafe |

**Rule:** derive adjusted series **as-of** (`ex_date ≤ cutoff`) from a versioned corporate-action table over an **immutable raw** vintage; forbid current-vintage back-adjusted series in any price-level feature, filter, universe screen, or label. Simple split-only returns are the one benign use of back-adjustment.

## 6. Validation-Method Applicability (not universal hard gates)

| Method | Purpose | Applicability condition | Min sample / trials | Primary/secondary | When not estimable | Gate |
| --- | --- | --- | --- | --- | --- | --- |
| Grouped-by-date **purged walk-forward** | Leakage-safe primary timeline | always for time-series cross-section | dated folds w/ min history | **Primary** | n/a | release_0_acceptance |
| **Embargo** | Remove residual serial correlation | with overlapping labels | ≥ max information interval (≥14 + feature memory) | Primary | n/a | release_0_acceptance |
| **Trial registry** | Enable deflation | always (log every config/seed/horizon/target/grid point) | n/a | **Mandatory** | n/a | release_0_acceptance |
| **DSR** | Deflate Sharpe for #trials + non-normality | **when multiple strategy/model trials exist** | trial count N logged | **Primary** (once N>~handful) | report point Sharpe + note low-trial | final_holdout |
| **PBO/CSCV** | Rank-instability across partitions | **when enough variants & CV partitions exist** | sufficient variants + partitions | **Secondary/robustness** | report `PBO_NOT_ESTIMABLE` — **not a pass, not proof of failure** | final_holdout (if estimable) |
| **CPCV** | Multi-path robustness | when non-overlapping-partition assumptions supportable | multiple partitions | **Robustness analysis** (not a replacement for WF) | fall back to WF + block bootstrap | final_holdout (robustness) |
| **Block bootstrap** | Dependence-aware CIs | overlapping/dependent data | block ≥ horizon | Primary (uncertainty) | n/a | release_0_acceptance |
| **Factor attribution** | Alpha ≠ beta | always for an alpha claim | factor returns available | Primary (edge gate) | n/a | release_0_acceptance |
| **Investable benchmark** | Value vs passive | always for a long-only book | SPY/sector basket + cost model | Primary (edge gate) | n/a | release_0_acceptance |
| **Locked holdout** | Final unbiased test | after thresholds frozen | one access | Primary | n/a | final_holdout |
| **Paper revalidation** | Realized-cost check | R3 | live paper fills | Primary | n/a | paper/live |

**Default hierarchy (unless evidence supports otherwise):** WF (primary timeline) → embargo (max information interval) → trial registry (mandatory) → DSR (when multiple trials) → PBO (only when enough variants/partitions) → CPCV (robustness where assumptions hold) → block bootstrap → locked holdout → paper revalidation. **DSR/PBO/CPCV must NOT be universal Release-0 *starting* blockers** (CLM-CPCV/DSR/PBO downgrade).

## 7. Model & Decision-Layer Separation (nine layers) + Policy-Weight Classes

"Deterministic MVP" refers to the **decision policy**, **not** the forecast model. The forecast model is a **learned** GBT+calibration stack. Separate concerns:

| Layer | MVP nature | Learned? |
| --- | --- | --- |
| 1 Base forecast model | GBT (LightGBM/XGBoost); elastic-net comparator | **Learned** |
| 2 Ranking model | within-date percentile of utility; LambdaMART = challenger | Deterministic (challenger learned) |
| 3 Calibration model | isotonic/Platt | **Learned (fit train-only)** |
| 4 Uncertainty model | quantile/conformal (CQR) intervals | **Learned** |
| 5 Decision policy | penalized-utility + permission + hard blockers | **Deterministic** |
| 6 Risk gate | risk-budget sizing + caps | Deterministic |
| 7 Portfolio allocator | greedy marginal-utility (not MV optimizer) | Deterministic |
| 8 Fill/cost model | deterministic assumption (R1); learned fill later | Deterministic (R1) |
| 9 AI/LLM analysis layer | advisory only (see §9) | Learned, **non-authoritative** |

**Policy-weight / threshold classification** (every weight/threshold must carry one):
- `FROZEN_ECONOMIC_PRIOR` — hand-set from economic reasoning, never data-fit (e.g., λ_tail from a stated risk-aversion). **Recommended for MVP utility λ.**
- `OWNER_POLICY_PARAMETER` — an owner choice (e.g., max sector exposure, abstention risk-appetite).
- `FIT_ON_TRAINING_ONLY` — learned inside the training window (scaler, calibrator, model params).
- `EMPIRICAL_THRESHOLD` — set from research-fold statistics (e.g., embargo length).
- `PROMOTION_THRESHOLD` — locked before holdout (ECE cap, drawdown cap, min matured recs).
**Rule:** if any value is selected **after viewing backtest outcomes**, it becomes a trial → counted in the trial registry and DSR/PBO analysis. This is the concrete resolution of A4-F-A4-02 (λ FROZEN_PRIOR vs FITTED).

## 8. Traceability Corrections Posture
Per-reference corrections (H1) carry: original ID, source document, authoritative candidate, semantic justification, mapping **confidence**, mechanical-vs-substantive class, affected documents, owner-approval requirement. **Ambiguous mappings are NOT auto-applied** (e.g., `REQ-DATAQ`/`REQ-CP` → REQ-DQ/REQ-GOV is *substantive* and owner-gated; `REQ-LBL→REQ-LAB` is *mechanical*). Code references classified individually (H1 §3), not by count. Useful historical prototype references are **preserved** (they seed the Phase-4 function/file contract appendix), labeled `EXTERNAL_PROTOTYPE_REFERENCE`.

## 9. AI/LLM Layer — Boundaries (analysis, not authority)
The AI/LLM layer is an **analysis and interaction layer**, **not a source of numerical truth or trading authority**. **Hard boundary — the AI layer must NOT directly:** modify risk limits · modify portfolio state · promote models · alter policy · submit broker instructions · rewrite audit history. **Every AI response used by the system must preserve:** `as_of` timestamp, source IDs, model provider, model version, prompt-template version, tool calls, structured claims, uncertainty, validation status. Options (no-LLM → advisory NL query → RAG over approved artifacts → structured extraction → explanation-from-reason-codes → tool-calling analyst → learned evidence producer → autonomous agent) are compared and defaulted in **Phase-2 packet 18**. Note: current LLM-for-finance empirical evidence here is thin (FinBERT cluster dated/low-grade), so this packet is graded conservatively and marked EMPIRICAL_TBD.

## 10. Quality Verdict (the nine mandated questions)
1. **Are all source counts exact and deduplicated?** Yes — 55 distinct external; 22 peer-reviewed; 6 official-primary; 9 current (2024–2026); 9 foundational (pre-2015). Enumerated in `SOURCE_EVIDENCE_REGISTER.md`.
2. **Does every Grade-A claim have multiple directly applicable sources?** Mostly. CLM-GBT (3 A-lines), CLM-EDGE/COST (multi), CLM-GICS (1 official — SINGLE but authoritative). CLM-EFFN and CLM-DETERM are **INFERENCE**, not Grade-A evidence, and are labeled so.
3. **Are all numerical claims reproducible?** The *derivable* ones (CLM-TURN-WEEKLY, CLM-EFFN) have explicit derivations + assumptions; the *measured* point figures behind 403'd sources (CLM-TURN 50%, CLM-COST bps) are **downgraded to ranges/illustrative**. No numeric point estimate is presented as verified when it is not.
4. **Are all consensus labels justified?** Yes — reclassified per §1–2; CX-11 corrected to SINGLE_AGENT_SUPPORTED.
5. **Are all agent-output provenance claims auditable?** Yes — 8 final reports preserved (`evidence/agents/`), labeled SOURCE_REPORT_PRESERVED; the distinct Round-2 dialogue is SYNTHESIS_ONLY; raw web fetches live in per-agent task-output JSONL (backstop).
6. **Are current 2024–2026 sources included for every evolving area?** Tabular-DL, conformal-TS, reproducibility, governance (SR 26-2), feature-store skew — **yes**. **LLM-for-finance — GAP flagged**; AI/LLM packet marked EMPIRICAL_TBD.
7. **Are older foundational sources distinguished from current empirical evidence?** Yes (`SOURCE_EVIDENCE_REGISTER.md` §Foundational-vs-current).
8. **Are contrary studies represented?** Yes — SRC-MODEL-005 (Virtue of Complexity) and SRC-EXEC-001 (optimistic FIM costs) are recorded as counter-evidence, not omitted.
9. **Are unsupported claims excluded from decision recommendations?** Yes — downgraded/removed items (GICS license number, 50%/month precision, per-bucket bps precision, "all adjusted invalid," universal-gate framing, "genuine independence") are excluded or re-scoped before Phase-2 packets.

## 11. Corrections Applied to A / D / E / H1 (factual/terminology/scope only — no style rewrites)
- **A** — independence terminology corrected; CX-11 reclassified; "no fabricated citations" retained; source counts made exact.
- **D** — DSR/PBO/CPCV re-scoped to applicability-conditioned (not universal MVP_REQUIRED hard gates); "deterministic MVP" clarified to mean the *decision policy* (forecast model is learned GBT).
- **E** — CLM-YFIN scope-corrected (price-basis matrix); SIC presented as a distinct taxonomy/option (not a GICS replacement).
- **H1** — mechanical-vs-substantive classification + mapping-confidence + owner-approval flag added to the reference table.

## 12. Provenance & Auditability Assessment
- Documents read in full: all **12** (7 root at commit `7c4c659` incl. README="# Financy"; 5 architecture-definition authored at `5d19997`/`022fb88`).
- Raw Round-1 agent reports: **PRESERVED** (final reports) in `evidence/agents/`; complete machine transcripts = task-output JSONL (not in repo; the ultimate backstop).
- Round-2 transcript: **NOT a distinct artifact** — synthesis only (recorded honestly).
- Reproducibility from repository artifacts alone: **partial** — conclusions trace to the preserved agent reports + source register + claim traceability; the lowest-level web fetches are external to the repo. Auditability assessment: **MODERATE-HIGH for claims tied to external sources; LOWER for INFERENCE-class claims** (labeled as such).
