# 09 — Model, Fusion & Agentic Layer

**Artifact type:** design (lead-authored; follows Alternative A; grounded in `03`).
**Decision-label:** the baseline stack = `EVIDENCE_SUPPORTED`; every challenger =
`EMPIRICAL_TBD`, admitted only by an ablation that beats the cheaper tier net-of-cost,
factor-residual, DSR-deflated, under identical PIT/cost/CPCV. The agent-autonomy boundary is
`OWNER_DECISION_REQUIRED` but the *default* (advisory-only) is `OWNER`-affirmed.

---

## 1. Model ladder (cheapest first; each tier must beat the one below)
| Tier | Models | Status | Why here |
|---|---|---|---|
| 0 Simple baselines | naive momentum, reversal, market-relative & sector-relative rules | reference | the honest floor every model must beat net-of-cost |
| 1 Linear comparator | **pooled elastic-net** (deployable comparator), Fama-MacBeth (diagnostic) | KEEP (R0) | required comparator; per-date oracle PROHIBITED |
| 2 **Primary** | **GBT (LightGBM/XGBoost)** on the multimodal digest panel | KEEP/EXTEND (R0 primary) | convergent A-grade evidence for tabular cross-sections (Gu-Kelly-Xiu, Grinsztajn, Shwartz-Ziv-Armon) |
| 3 Text encoders | FinBERT-as-feature / domain encoders / event-extractors / novelty / stance / source-reliability models | challenger | produce *offline PIT features*, not decisions; short-horizon reversal-flavored (Tetlock) |
| 4 Graph | PIT peer aggregates → dynamic as-of graph features → GNN/GAT | challenger ladder (`08`) | GNN must beat cheap peer aggregates (Bhojraj-Lee-Oler) first |
| 5 Sequence | GRU/LSTM/TCN/TFT (causal only) | R4 challenger | must beat GBT net-of-cost (DLinear/Zeng skeptical prior); highest leakage + sample demand |
| 6 Memory | analog outcome distributions / structured / embedding / regime-conditioned retrieval | research challenger | leakage-prone; evidence-surfacing aid, not a probability source (`08`) |

**Every learned candidate carries the "advanced-model checklist":** a measured net-of-cost
DSR-adjusted increment over GBT+calibration; ablation under identical PIT/cost/CPCV; leakage
prevention; PBO/DSR at the meta level; and a stated kill criterion. No tier is admitted on
sophistication.

## 2. Fusion — trees first, learned fusion only if it wins
| Fusion | Verdict |
|---|---|
| **GBT on concatenated digests** (implicit fusion via tree splits) | **default** — interactions are tree conjunctions, not sums; no fusion net needed |
| Small frozen **named cross-features** (`regime×signal`, `attention×trust×price_moved`) | adopt — economically-specified interactions the tree gets a hint on |
| Late / gated / stacking / blending / MoE / cross-attention | challenger — admitted only if it beats GBT-on-concatenated-features net-of-cost (the fusion falsifying test, `04` A) |
| Decision-level ensemble | usable at the decision layer with whole-decision calibration |

Fusion complexity is **earned against a GBT-on-concatenated-features baseline** (Baltrušaitis
taxonomy is solid; no finance net-alpha benefit is demonstrated for learned fusion).

## 3. Missing-modality handling (explicit; missing ≠ neutral)
Native in the tabular default: each modality contributes an `is_missing` indicator + a
`staleness_hours` column, so the GBT can route missingness to a *different* leaf than a
zero-signal. Missingness may trigger: a missingness feature (default), a specialized fallback
model, **wider uncertainty**, **reduced position size**, or **abstention** — chosen by the
decision layer (`12`) and the abstention gate (`13`), never silently coerced to "neutral."

## 4. Agentic / orchestration layer — options and the boundary
| Option | Verdict |
|---|---|
| No LLM agent | viable; the pipeline is deterministic without one |
| **Deterministic orchestrator** | **recommended default** — a deterministic DAG runner over the pipeline; reproducible, auditable |
| LLM-assisted orchestrator | permitted for *analysis/explanation/retrieval/routing* only, outside the numeric decision path |
| Multi-agent research workflow | a *research-time* tool (like this reassessment), not a runtime decision-maker |

**Autonomy boundary (mission-mandated).** The LLM/agent layer may organize evidence, identify
contradictions, retrieve as-of analogs, explain forecasts, and recommend deeper analysis. It may
**not** invent/modify/round probabilities, override calibration or portfolio constraints, change
thresholds, fabricate timestamps/sources, or place orders (`11` §5). The numeric decision path
(features → model → calibration → cost/risk → allocation) is **deterministic and LLM-free**;
any LLM output that would enter it is an attackable feature subject to source-trust + the
probability-integrity gate. **Autonomous execution is REJECTED** absent an explicit future owner
decision.

## 5. What this layer refuses
No model admitted on sophistication; no fusion net before it beats concatenated-features; no
sequence/graph/RAG on the MVP critical path; no LLM in the numeric decision path; missing
modality never treated as neutral; no autonomous execution.
