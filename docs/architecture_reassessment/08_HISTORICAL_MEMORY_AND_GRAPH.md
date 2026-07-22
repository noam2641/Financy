# 08 — Historical Memory & Relationship-Graph Intelligence

**Artifact type:** design (lead-authored; follows Alternative A / D-rule-form; grounded in `03`
Q7/Q8). **Decision-label:** memory-as-versioned-evidence and PIT-peer-aggregates =
`ARCHITECTURAL_INFERENCE`/`KEEP_AS_FOUNDATION`-adjacent; **GNN, learned graph, and analog/RAG
retrieval = `EMPIRICAL_TBD` / research challengers** that must beat a cheap PIT baseline
net-of-cost before inclusion. **Do not recommend a GNN merely because a graph can be built.**

---

## 1. Historical memory = a versioned evidence system, not vague LLM memory
Memory is a **PIT, append-only, queryable store**, not model weights or free-text recall. It
records: structured events; company-specific event history; market-regime, crisis, war/sanctions
memory; earnings-reaction memory; social-hype memory; **source-reliability history**; and the
system's own **prediction history, decision history, realized outcomes, model-error history,
false-high-confidence forecasts, and missed opportunities**. The last group is the most valuable
and the cheapest to make honest: it is exactly the R0 run-ledger + trial-registry + evaluation-
report lineage, extended with realized outcomes — self-knowledge the system already has the
machinery to store tamper-evidently.

## 2. Retrieval is evidence, not proof — and it is a leakage surface
Case-based reasoning / nearest-neighbor / vector / graph / sequence / **regime-conditioned**
retrieval can *surface analogs* ("this setup resembles these prior setups"). But:
- **Historical similarity is evidence, not causal proof** of a future outcome.
- **Retrieval leakage is first-order** (`03` Q8): a decision at time *t* may retrieve only cases
whose full information (including the *neighbor's own outcome*) was available **as-of *t***, and
the embedding/index must not be trained on post-*t* text. Retrieval that returns neighbors
postdating the decision, or an embedding model trained on the future, silently leaks.
- Analog **frequencies are calibratable only** if the reference set is strictly as-of and the
metric is regime-stable; otherwise they are `FREQ_ANALOG · LIMITED_SUPPORT` at most (`11`) — never
a calibrated model probability, and never surfaced as one.
- There is **no replicated evidence** that analog/RAG delivers net-of-cost cross-sectional alpha
(FinSeer 2025 is single-study). → retrieval is an **experimental evidence-surfacing aid** with
mandatory as-of filtering, not a probability source. It is a research challenger, gated on
demonstrated marginal net-of-cost value.

**Similarity is defined** over: company similarity, sector similarity, event similarity, macro
similarity, volatility-regime compatibility, temporal distance, recency decay, **sample
support**, and **outcome dispersion** — and a retrieval is only trustworthy when sample support
is adequate and outcome dispersion is not so wide that the analog set says nothing.

## 3. Relationship intelligence — start with the cheap strong baseline
Cover competitors, suppliers, customers, sector/industry, ETFs, ownership (where legally
available), commodity/currency/rate/geographic exposure, news co-mentions, correlations, dynamic
correlations, lead-lag, event contagion, and supply-chain dependencies. But **model them in
increasing order of cost/leakage, admitting each only if it beats the previous:**

| Tier | Representation | Note |
|---|---|---|
| 0 (baseline) | **PIT peer aggregates** — sector/industry (SIC free-PIT) rolling means, relative strength, dispersion | Bhojraj-Lee-Oler: industry classification already explains co-movement well. Cheap, deterministic, low-leakage. |
| 1 | rolling correlation / lead-lag features, ETF-membership and factor exposures as columns | additive features the GBT can use; still tabular |
| 2 (challenger) | dynamic **as-of** relationship graph → peer-aggregate features (graph as a *feature builder*, not a model) | construction must be strictly as-of (future constituents/correlations are look-ahead) |
| 3 (research challenger) | **GNN / graph-attention** | admitted only if it beats Tier 0–2 net-of-cost under identical PIT/cost/CPCV. Feng 2019 (the pro-graph result) is single-study, gross-of-cost, with no peer-aggregate baseline; graph construction is a documented leakage surface. |

**Graph contamination guard:** any relationship known only later (a supply-chain link disclosed
after *t*, a correlation estimated on a window straddling *t*, a hindsight sector reclassification)
is prohibited; graph edges carry `edge_available_at` and inherit the §0 availability machinery.

## 4. What this design deliberately refuses
No vague LLM "memory"; no retrieval without as-of filtering; no analog frequency presented as a
calibrated probability; no GNN/graph adopted before it beats PIT peer aggregates net-of-cost; no
relationship edge used before its `edge_available_at`. Memory's first, safe, high-value use is the
system's **own** prediction/outcome/error history (self-calibration and drift detection), which is
cheap and leakage-free.
