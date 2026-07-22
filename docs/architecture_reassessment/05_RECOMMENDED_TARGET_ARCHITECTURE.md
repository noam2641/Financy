# 05 — Recommended Architecture (Target Direction · Fallback · Challenger)

**Artifact type:** finalized recommendation (Phase 5 lead integration).
**Inputs integrated:** architect alternatives (`04`), evidence (`03`), current state (`02`),
red-team (`14`). **This supersedes the architect's *preliminary* recommendation** where the
red-team forced a change; provenance of each change is recorded in §4.
**Decision-label:** the *staged program* is `ARCHITECTURAL_INFERENCE`; every GO/edge verdict is
`EMPIRICAL_TBD`; the items in `16` are `OWNER_DECISION_REQUIRED`.

---

## 1. The headline reframing (what changed after the red-team)
The architect recommended **Alternative A as the target**. The red-team showed this is premature
against a **zero-implementation baseline** (14/16 R0 tasks unbuilt) and that the defenses which
would make any verdict trustworthy — trial registry, DSR/PBO on effective sample, factor-residual
investable-benchmark gate, survivorship cohort — are **contracted but not yet built**. Therefore:

> **The committed near-term architecture is not "Alternative A." It is Edge-Probe+ on a
> hardened, *implemented-and-tested* truth kernel. Alternative A is the earned-only *direction*
> the program may grow into — one modality at a time, each admitted solely by passing its own
> ablation net-of-cost, factor-residual, effective-sample-deflated. The honest prior is that most
> will not clear, and that the first honest verdict is `BLOCKED_NO_EDGE`.**

## 2. Recommendation
### ● COMMITTED NOW (R0–R1A): "Edge-Probe+" on a hardened truth kernel
The **entire content of R0–R1A** is the price/volume-only truth chain plus four kernel primitives
that must be **built and `TESTED_RESEARCH`** before any architecture bake-off:
1. **Trial registry** (every config/seed/horizon/target/digest/agent-experiment is a logged trial).
2. **DSR + PBO on the *effective* sample** (block-bootstrap block length; cluster on regime/factor-date; a frozen **minimum-effective-N per horizon and per regime**).
3. **Factor-residual net-of-cost edge gate vs an *investable* multi-factor benchmark** (market+MOM+STR+SMB+HML+RMW or ETF proxies) — not merely beating 1/N.
4. **Survivorship-safe `FixedPITCohort`** with delisted names + terminal-event returns, and a **PIT sector/universe source** that does not depend on look-ahead membership.

Plus the red-team's hard gates: **pre-register ONE primary (target, horizon)** before holdout;
**hard capacity gate** (edge survives at a stated AUM, ≤X% ADV, spread/impact model; frozen
`minimum_dollar_volume`); **per-regime positive-net-edge gate** + correlated-drawdown cap;
**gate-eligible probability restricted to marginal `P(return > cost)`** with out-of-regime coverage
(barrier/touch/time/MFE-MAE heads are `RESEARCH_ONLY`, barred from the gate and from sizing until
coverage is proven); **1/N (and vol-scaled 1/N) as a mandatory net-of-cost portfolio baseline**.
Forecast core = **GBT primary + pooled elastic-net comparator** (per-date oracle prohibited);
per-decision **ABSTAIN** in rule/score form. Run Edge-Probe+ to an honest deflated, factor-residual,
capacity-limited verdict.

### ● TARGET DIRECTION (earned, not approved): Alternative A — Trust-Gated Tabular Multimodal Panel
The superstructure the program grows into **iff** modalities earn their way in. A adopts, as
infrastructure: the **availability-time + PIT source-trust ingestion layer** (the canonical
`content_*`/`source_profile` addendum) so each modality inherits the InformationInterval/purge/
embargo machinery; and D's **rule/score abstention-first gate** (completeness/freshness/
contradiction/OOD/drift). Admission rule per modality: it must beat the price/volume baseline
**net-of-cost, factor-residual, effective-sample-deflated**, and clear licensing. **Social
evidence weight = 0 in the executable edge for R0–R2** (advisory-only; may *raise* permission only
on independent multi-family confirmation, may not trip ABSTAIN on a single unconfirmed cluster)
until a manipulation-robustness test passes. Interactions are tree conjunctions + a *small,
trial-registered* named cross-feature set. This direction is where the mission's multimodal, richer-
target-semantics product lives — but it is reached by ablation, not by decree.

### ● SIMPLER FALLBACK: Edge-Probe+ itself
If no modality clears its ablation, **ship Edge-Probe+** (or record `BLOCKED_NO_EDGE` and stop).
The program is a **monotone ladder**: prove edge on the cheapest possible target first; buy
complexity only with ablation evidence. `BLOCKED_NO_EDGE` is a valid, preferable outcome to a
fabricated GO.

### ● RESEARCH CHALLENGER: Alternative B1 (causal sequence-encoder), R4-gated
Admitted **only** at R4, **only** as a feature producer into A's GBT panel, **only** behind a
byte-identical **determinism proof** (CPU/pinned-kernel fixed-seed) and an **incremental net-edge**
over A's quantile heads under identical PIT/cost/CPCV/DSR. Its sole sanctioned justification is
sharper path targets. **B2 (sequence-as-forecaster) is REJECTED for R0–R3.** Second-tier, recorded
but not designated: D's **GNN form** (rejected until it beats a GICS/Bhojraj-Lee-Oler peer baseline
net-of-cost with a leakage audit) and **analog/RAG retrieval** (research-only, leakage-prone).

## 3. What is preserved, extended, and rejected
- **Preserved (KEEP):** the entire R0 rigor — PIT, survivorship, corporate actions, interval-purge
+ embargo, trial registry, DSR/PBO, effective-sample, round-trip cost, investable benchmark,
factor attribution, environment_hash, hash-chained ledger, BLOCKED_NO_EDGE, the LLM-advisory
boundary, "maximalism is a release blocker."
- **Extended (only after the kernel is tested):** entity model (content/source-trust entities,
wider enums via *additional rows* not reordered fields), labels (barrier/excursion target-types as
RESEARCH_ONLY heads), FeatureSnapshot (per-modality lineage), InformationInterval (max
availability-time — deferred until a modality is admitted), calibration (probability heads),
factor attribution (incremental-value-over-price test), per-decision ABSTAIN + OOD/drift.
- **Rejected / hard-gated:** B2 and GNN-D for R0–R3; C-as-spine (capped under 1/N); social in the
executable edge (weight 0 until proven); barrier/touch/time/MFE-MAE probabilities in the gate/sizing
(until out-of-regime coverage proven); sector-excess as primary target (until GICS licensed);
autonomous execution (permanently, absent owner decision).

## 4. Provenance of changes vs the architect's preliminary recommendation
| Change | Origin |
|---|---|
| "A is target" → "A is earned-only direction; Edge-Probe+ committed" | red-team RT-6, verdict (iii) |
| Build + test 4 kernel primitives before any bake-off | RT-1 |
| Factor-residual investable-benchmark gate (not 1/N) mandatory | RT-2 |
| Compute effective N; min-effective-N per horizon/regime gate | RT-3 |
| Gate-eligible probability = marginal P(return>cost); barrier/touch/time RESEARCH_ONLY | RT-4 |
| Primary target sector-excess → market-excess/factor-residual (GICS look-ahead) | RT-5 |
| C demoted beneath mandatory 1/N | RT-7 |
| B1 R4-only + determinism proof; B2 rejected | RT-8 |
| D GNN rejected; ship rule/score only | RT-9 |
| Social weight = 0 in executable edge until manipulation test | RT-10 |
| Pre-register ONE primary (target, horizon) | RT-12 |
| Per-regime edge gate + drawdown cap | RT-13 |
| Hard capacity gate (AUM/%ADV/min-ADV) | RT-14 |
| Retained from architect: Edge-Probe+-first ladder; A's trust-layer + abstention adoption; B1-as-encoder challenger framing | architect `04` |

**Net:** the multimodal, richer-semantics product the mission asks for is the *destination*; the
*committed step* is a hardened, tested, honestly-deflated edge probe whose most likely verdict is
`BLOCKED_NO_EDGE`. Everything beyond it is bought with ablation evidence, one modality at a time.
