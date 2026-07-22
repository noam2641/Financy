# 00 — Index & Executive Decision Memo

**Financy Architecture Refoundation — Multimodal Stock-Decision System**
**Type:** documentation-only reassessment. **Status:** *non-binding proposal for owner review.*
**Base:** branch `claude/trading-platform-audit-iawx0v` @ `ba20eaf5aa03f7a11f4dc177c271d7cc1300e26d`;
test baseline **174 passed**; TASK-R0-03 and TASK-R0-04 remain unstarted. **No production code,
contract, source, test, or CI was changed by this work** — only the Markdown documents in this
directory were added.

---

## How this was produced (one lead + five read-only specialists)
Executed in the mandated order: **Phase 0** verify + branch → **Phase 1** independent mission-first
inventory → **Phase 2** `repository-architecture-discovery` ∥ `financial-ml-literature-research` →
**Phase 3** `alternative-system-architect` → **Phase 4** `adversarial-architecture-critic` →
**Phase 5** lead integration → **Phase 6** `research-roadmap-planner` → **Phase 7** lead synthesis +
documentation. Every conclusion is attributed to its originating specialist in the relevant
document. The literature specialist verified **~40 primary sources** (peer-reviewed journals, NBER,
SSRN, arXiv, SEC/EDGAR, Federal Reserve/ALFRED) with access date 2026-07-22; none invented.

## The executive decision (finalized after red-team)
The mission asks for a broad, multimodal, cross-sectional stock-decision system. The reassessment's
central conclusion, forced by the adversarial review, is a **reframing of "how," not a rejection of
the "what":**

> **Do not crown a multimodal architecture as the "target" against a repository where 14 of 16 R0
> tasks are unbuilt and the defenses that make any verdict trustworthy (trial registry, DSR/PBO on
> the *effective* sample, a factor-residual *investable-benchmark* edge gate, a survivorship-safe
> cohort) are contracted-but-not-implemented. Build and *test* those four kernel primitives first;
> run a hardened, price/volume-only "Edge-Probe+" to a single honest, deflated, capacity-limited,
> per-regime verdict — whose most likely honest result is `BLOCKED_NO_EDGE` — and admit each
> modality into the multimodal panel only when it passes its own ablation net-of-cost,
> factor-residual, effective-sample-deflated, and licensed.**

- **Committed now (R0–R1A):** **Edge-Probe+** on a hardened, tested truth kernel (`05`, `15`).
- **Target direction (earned, not approved):** **Alternative A — Trust-Gated Tabular Multimodal
Panel** (GBT over PIT modality digests + explicit missingness + a per-modality availability-time &
source-trust ingestion layer + a rule/score abstention gate). Reached by ablation, one modality at
a time.
- **Simpler fallback:** Edge-Probe+ itself (ship it, or record `BLOCKED_NO_EDGE`).
- **Research challenger:** Alternative B1 (causal sequence-encoder), **R4-only**, behind a
byte-identical determinism proof + incremental net-edge. **Rejected for R0–R3:** B2
(sequence-as-forecaster) and the GNN form of D; **C (portfolio-optimizer spine) demoted beneath a
mandatory 1/N baseline**; social evidence weight **0** in the executable edge until manipulation
robustness is proven; **sector-excess dropped as primary target** (GICS look-ahead) in favor of a
market-excess / factor-residual basis.

**Single most important finding:** the most probable *honest* outcome is `BLOCKED_NO_EDGE` — the
short-horizon cross-sectional signal is likely real-but-already-priced after costs (replicated:
McLean-Pontiff, Chen-Velikov, Novy-Marx-Velikov, Hou-Xue-Zhang). That is the correct finding; the
real danger is a **false GO**, which the four unbuilt defenses would otherwise permit. Everything in
this reassessment is oriented to make `BLOCKED_NO_EDGE` *trustworthy* and complexity *earned*.

**What is preserved:** the entire R0 rigor (PIT, survivorship, corporate actions, purged/embargoed
validation, trial registry, DSR/PBO, effective-sample, round-trip cost, investable benchmark,
factor attribution, `environment_hash`, hash-chained ledger, `BLOCKED_NO_EDGE`, the LLM-advisory
boundary, "maximalism is a release blocker"). No existing component is REPLACE or REMOVE.

## Document map
| # | Document | What it answers |
|---|---|---|
| 00 | *this memo* | executive decision + index |
| 01 | Independent Pre-Read Question Inventory | mission-first questions/assumptions/failure-modes (written before reading the design) |
| 02 | Current-State Reconstruction & Gap Analysis | what exists, what's contracted-not-built, component verdicts, gaps, inventory-vs-design |
| 03 | Research Evidence Matrix | ~40 verified primary sources → decisions; strongest/weakest claims |
| 04 | Architecture Alternatives & Decision Matrix | A / B / C / D / E with diagrams, flows, comparison |
| 05 | **Recommended Architecture** | target direction · fallback · challenger (finalized post-red-team) |
| 06 | Technical, Market & Macro Engine | features-as-hypotheses; PIT regime vector |
| 07 | News, Filings, Telegram & Social-Attention Engine | PIT ingestion, source-trust, manipulation defenses |
| 08 | Historical Memory & Relationship-Graph | versioned evidence memory; graph/GNN as gated challenger |
| 09 | Model, Fusion & Agentic Layer | model ladder, fusion, missing-modality, autonomy boundary |
| 10 | Horizon & Target-Semantics Research | pre-registered horizon study; target-vector tiering |
| 11 | **Probability-Integrity Policy** | typed probability claims; calibration gate; `NOT_ESTIMABLE`/ABSTAIN |
| 12 | Cross-Sectional Decision & Portfolio/Risk | decision cycle, sizing invariant, 1/N floor, autonomy ladder |
| 13 | Evidence, Explanation & Validation | evidence DAG, explanation caveats, ablation program, red-team-hardened gates |
| 14 | **Red-Team Findings** | 4 CRITICAL / 6 HIGH / 6 MEDIUM + verdicts |
| 15 | **Revised Roadmap & Task Graph** | release ladder L0–L5, staged plan, migration, contract revisions |
| 16 | **Unresolved Owner Decisions** | 18 owner decisions (8 blocking the build) |
| 17 | Research References | verified bibliography |
| 18 | Illustrative Walkthrough | a fictional end-to-end ABSTAIN example (all numbers illustrative) |

## The eight decisions that block the build (see `16`)
OD-1 approve the scope freeze (Edge-Probe+ + 4 primitives only) · OD-5 drop sector-excess as
primary (GICS look-ahead) or license PIT GICS · OD-2 the investable factor set + min deflated t ·
OD-3 minimum effective-N + counting method · OD-4 which probabilities may drive ABSTAIN/sizing ·
OD-6 the one pre-registered primary (target, horizon) · OD-7 the capacity envelope (AUM/%ADV/min-$-
volume) · OD-8 regime buckets + per-regime edge requirement.

## Scope & integrity confirmations
- Documentation-only; every file added is new Markdown under `docs/architecture_reassessment/`.
- `main` unchanged; canonical v4.6 unchanged; existing contracts/source/tests/CI/`pyproject.toml`/
`.gitignore` unchanged; **TASK-R0-03 and TASK-R0-04 remain unstarted**; no `determinism.py`/
`ledger.py`/provider adapter created; no dependencies added; no models implemented or trained; no
datasets downloaded into the repo.
- This proposal is **non-binding** and awaits owner review; the resulting PR is a **draft** and must
**not** be merged, nor the proposed architecture implemented, from this task.
