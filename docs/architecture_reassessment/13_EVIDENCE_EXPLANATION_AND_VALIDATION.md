# 13 — Evidence, Explanation & Validation

**Artifact type:** design (lead-authored; extends the R0 validation foundation with the red-team
gates in `14`). **Decision-label:** the validation *discipline* is `EVIDENCE_SUPPORTED` /
`KEEP_UNCHANGED`; the numeric thresholds are `EMPIRICAL_TBD`, frozen before final-holdout access.

---

## 1. Evidence DAG (traceable lineage per decision)
```
source ─► normalized PIT record ─► extracted event ─► feature | embedding ─► modality output
      ─► fused forecast (target vector) ─► calibration ─► cost & risk adjustment
      ─► portfolio decision ─► explanation ─► realized outcome
```
Improvement over the canonical DAG: every edge carries **`available_at`** and, for content
edges, a **PIT source-trust weight**; the realized-outcome node closes the loop into
post-decision learning (`self-knowledge` memory, `08`). Every recommendation must be traceable to:
raw **source IDs**, **timestamps**, **feature snapshots** (schema+values checksum), **model
versions**, **calibration versions**, **analog cases** (as-of), **peer context**, **supporting
evidence**, **contradictory evidence**, **missing data**, **warnings**, and the **decision-policy
version** — all already representable in the R0 ledger/snapshot/trial machinery, extended with the
content/source-trust entities.

## 2. Explanation (never causal over-claim)
Use **SHAP**, **ablation**, **counterfactuals**, **analogs**, **modality contributions**,
**model-disagreement**, and **attention inspection with explicit caveats**. **Attention is not
causal proof** and is labeled as such. Explanations are deterministic templated reason codes by
default; an LLM may render them in natural language but may not alter the underlying numbers
(`11` §5). Every explanation records which evidence supported vs contradicted the action and what
was missing.

## 3. Validation & calibration plan (retain + harden)
**Retain/improve (KEEP):** PIT data · survivorship safety · corporate-action safety · publication
& availability times · purged walk-forward · embargo · nested selection · **untouched final
holdout** · trial registry · multiple-testing adjustment · realistic round-trip costs · liquidity
& capacity · investable benchmarks · factor attribution · probability calibration · interval
calibration · regime analysis · data drift · concept drift · OOD detection · environment
reproducibility · hash-linked ledger.

**Hardening forced by the red-team (`14`):**
- **RT-2 factor-residual purity gate:** the edge must be net-of-cost alpha **residual to an
investable multi-factor benchmark**, not merely beating 1/N. An **incremental-value-over-price**
test: regress any multimodal alpha on the price-only model's residuals — a "news/graph edge" that
vanishes is disguised price/factor beta.
- **RT-3 effective sample:** every CI/PBO/DSR uses **effective N** (block-bootstrap block length;
regime/factor-date clustering), with a frozen **minimum-effective-N per horizon & regime** gate.
- **RT-4 gate-eligible probability:** only marginal **P(return > cost)** with out-of-regime
coverage may drive ABSTAIN/sizing; barrier/touch/time/MFE-MAE are `RESEARCH_ONLY` diagnostics.
- **RT-12 pre-registration:** ONE primary (target, horizon) frozen before holdout; everything else
diagnostic and counted in the deflation.
- **RT-13 per-regime gate:** positive net edge required in each regime bucket + a correlated-
drawdown cap.
- **RT-14 capacity gate:** edge must survive at a stated AUM with ≤X% ADV participation and a
spread/impact model; `minimum_dollar_volume` frozen (a hard gate, not `SHOULD`).
- **RT-15 agent-trial capture:** every agent-run experiment writes a trial-registry row; CI blocks
a holdout comparison whose trial count exceeds the pre-registration.

## 4. Mandatory ablation program (a complex model is admitted only if it wins)
Run, on the effective sample, net-of-cost, factor-residual, DSR-deflated: **technical-only ·
market-only · macro-only · fundamentals-only · news-only · social-only · graph-only · memory-only
· selected combinations · full system.** A modality/model is admitted **iff** its ablation adds
**stable, cost-adjusted, out-of-sample value beyond the cheaper alternative** across ≥2 regimes.
The default prior is that most ablations do **not** clear — and that is a valid result, recorded
honestly. This ablation gate is the operational form of "buy complexity only with evidence."

## 5. Leakage & OOD tripwires (kept and extended)
- The R0 **synthetic-forward-feature tripwire** (inject a forward-return feature → OOS IC ≈ 0)
runs on every new modality/feature family.
- **Value-parity** (batch vs latest path checksum) extends to per-modality checksums.
- **OOD / drift** detectors (feature-density, ADWIN/DDM) gate whether probabilities are emitted at
all; OOD → `OUT_OF_DISTRIBUTION` / ABSTAIN (`11`).
- **Retrieval-leakage audit** for any analog/memory use (as-of reference set + embedding not
trained on the future, `08`).

## 6. What validation refuses
No significance on raw row counts; no GO that beats only 1/N; no probability in the gate without
out-of-regime coverage; no threshold changed after holdout access (pre-registration freeze,
`PreRegistrationMismatchError`); no attention presented as causal; no modality admitted without a
passed ablation.
