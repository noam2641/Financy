# 15 — Revised Roadmap & Task Graph

**Artifact type:** staged roadmap (Phase 6 output). **Primary source:** specialist
`research-roadmap-planner`, integrating the accepted direction (`05`) and every red-team gate
(`14`). **Decision-label:** the sequencing is `ARCHITECTURAL_INFERENCE`; every promotion is
`EMPIRICAL_TBD` behind its gate. Free-PIT-first; solo/small-team executable through L3.

---

## The one hard sequencing rule
> **The A/B/C/D architecture bake-off is FROZEN** — no modality, fusion, sequence model, graph,
> or optimizer may touch the executable edge — **until all four kernel primitives (`FC-R0K-*`)
> are `TESTED_RESEARCH`** (each passing a *negative control*). This is red-team RT-1/RT-6 made
> operational.

**Global invariants (respect, do not re-litigate):** work on `claude/trading-platform-audit-iawx0v`,
never `main`; one task = one branch = one PR, test-first (fixtures → impl → edge cases →
traceability); `entities.py` field order is pinned by golden fixtures — **extend only by APPEND**,
never reorder (a closed-enum addition is a deliberate, human-reviewed, test-breaking change); CI
determinism gate is offline, committed-fixtures, Py 3.10/3.12; `BLOCKED_NO_EDGE` is a correct
outcome, never move thresholds/folds/labels after seeing performance; **TASK-R0-03/04 are NOT
implemented in this reassessment** (planning only).

## §1. Release ladder
| Rung | Name | Entry | PROMOTION gate | REJECTION / STOP |
|---|---|---|---|---|
| **L0** | R0 Truth Kernel | foundations preserved | 6 truth-chain gates pass **and** all 4 `FC-R0K` primitives at `TESTED_RESEARCH` (negative controls pass) | any primitive fails its negative control → fix; bake-off stays frozen |
| **L1** | R0 **Edge-Probe+** verdict | L0 done | ONE pre-registered (target,horizon) evaluated **once** on locked holdout → deflated (DSR/PBO), factor-residual, capacity-limited, per-regime, net-of-cost result | most likely `BLOCKED_NO_EDGE` = **process pass**; STOP — do not tune to manufacture edge |
| **L2** | R1A Decision Kernel | L1 honest verdict | 7-component kernel price/volume-only, per-decision ABSTAIN, portfolio = mandatory 1/N; schema/PIT/replay gates = 0 | non-deterministic, or 1/N missing → blocked |
| **L3** | Per-modality admission | L2 exists | each modality by its **own** ablation: net-of-cost **AND** factor-residual **AND** effective-sample-deflated positive marginal value **AND** licensing | fail → `RESEARCH_ONLY`; social weight = 0 until manipulation test passes |
| **L4** | Paper | ≥1 modality admitted or price/vol edge survives | all `TBD_BLOCKER` thresholds frozen; shadow days met | any hard `TBD` unresolved → not `PAPER_READY` |
| **L5** | Monitored / limited-live | beyond solo free-PIT scope | deferred | deferred |

**Free-PIT-first:** L0–L3 run entirely on free data (yfinance/Stooq OHLCV, SEC EDGAR/XBRL, FRED,
ETF-proxy factors, delisted-ticker archives). Only L5 and the R4 sequence challenger need paid
data/GPU.

## §2. Dependency-ordered task graph
```
WAVE A  Substrate (mostly done): FC-R0-00 Preserved Foundations ── reused by everything
WAVE B  R0 TRUTH KERNEL (SEQUENTIAL SPINE — gates all downstream)
   FC-R0-01 OHLCV adapter ─► FC-R0-02 PIT labels ─► FC-R0-03 schema parity
        └─► FC-R0-06 Event normalization (corp actions/delist/terminal)
   FC-R0-04 checkpoint/replay ┐ safe-parallel after schema parity (separate files/branches)
   FC-R0-05 purged split      ┘
   ▼ THE FOUR KERNEL PRIMITIVES (build+TEST before any bake-off)
   FC-R0K-01 Trial Registry ─► deflation count
   FC-R0K-04 FixedPITCohort (survivorship) ┐ parallel to registry
   FC-R0K-03 Factor-residual benchmark ────┤ needs cohort universe
   FC-R0K-02 DSR+PBO effective-sample ─────┘ needs registry + cohort
   ▼ [HARD FREEZE LIFTS HERE]
WAVE C  R0 EDGE-PROBE+ VERDICT (sequential): FC-EP-01 baselines (GBT+elastic-net+1/N & vol-scaled-1/N)
        ─► FC-EP-02 calibration (marginal P(return>cost) only) ─► FC-EP-03 min decision/ABSTAIN + capacity + per-regime
        ▼ pre-registered holdout unlock (ONE access) → VERDICT
WAVE Gcore  L2 R1A: FC-R1A-DEC decision engine · FC-R1A-PORT portfolio (1/N floor)
WAVE D  PER-MODALITY ADMISSION (each modality independent parallel track; admission serialised through the ablation harness)
   FC-DA-01 data acquisition ─► FC-DL-01 licensing ─► {TECH | MACRO | FUND | NEWS | GRAPH | MEM}
WAVE E  TARGET (earned): FC-FUSE multimodal fusion (Alt A) · FC-HZN horizon research (after ≥1 modality admitted)
WAVE F  CHALLENGER: FC-R4-SEQ sequence encoder (R4 only, determinism proof; B2 rejected)
WAVE G  RUNTIME/OPS: FC-R3-PAPER · FC-MON monitoring · FC-LEARN post-decision learning · FC-R3-EXEC execution boundary
```
**Sequential:** A→B backbone→primitives→C→L2; holdout unlock is a one-way door. **Safe-parallel**
(separate files/branches, no shared fixture edits): {FC-R0-04 vs FC-R0-05}; {FC-R0K-01 vs
FC-R0K-04}; all `FC-MOD-*` research tracks; validation notebooks (D/E/F) run `RESEARCH_ONLY` any
time but cannot write executable edge until L3.

## §3. Stages (objective · promote/reject/stop · burden)
**WAVE B — truth kernel**
- **S0 Preserved Foundations (`FC-R0-00`)** — reuse `core/time.py`, `entities.py`, 174 tests verbatim; add a field-order/enum regression tripwire. *Promote:* 174 green on 3.10+3.12. *Stop:* any downstream need to reorder a frozen entity → human governance. Burden ~0.
- **S1 Event Normalization (`FC-R0-06`)** — one deterministic OHLCV/corp-action/delisting/terminal normalization boundary. *Promote:* downstream sees only 1-D numeric Series. *Reject:* raw provider layout reaching features. Burden trivial (fixtures, no network in CI).
- **S2 The FOUR Kernel Primitives** (negative-control-first; gate the whole bake-off):
  - **`FC-R0K-01` Trial Registry** — log every config/seed/horizon/target/digest **and agent experiment**; no number reported without a registry entry. *Stop:* if agent experiments can't register, freeze the bake-off (deflation unsafe).
  - **`FC-R0K-02` DSR+PBO on effective sample** — block-bootstrap block length, regime/factor-date clusters, frozen min-effective-N per horizon/regime. *Reject:* reports edge on pure noise. *Stop:* any downstream gate reading raw Sharpe.
  - **`FC-R0K-03` Factor-residual investable-benchmark gate** — net-of-cost residual alpha vs market+MOM+STR+SMB+HML+RMW (or ETF proxies); **replaces sector-excess primary with FACTOR_RESIDUAL** (fixes GICS look-ahead). *Reject:* a factor bet survives as "alpha".
  - **`FC-R0K-04` FixedPITCohort** — includes delisted names + PIT membership, no look-ahead. *Reject:* current-membership contamination.
**WAVE C — Edge-Probe+ verdict**
- **S3 Baselines (`FC-EP-01`)** — GBT primary + pooled elastic-net + **mandatory 1/N & vol-scaled-1/N**. *Reject (of a learner):* fails to beat 1/N after deflation → research-only. First stage to add model deps (§5). Burden minutes on a laptop.
- **S4 Calibration (`FC-EP-02`)** — calibrate/gate **only** marginal P(return>cost) with out-of-regime coverage; barrier/touch/time/MFE-MAE heads `RESEARCH_ONLY`, barred from gate/sizing. *Stop:* routing a research head into gate/sizing.
- **S5 Decision Engine (`FC-EP-03`→`FC-R1A-DEC`)** — economic-edge gate, per-decision ABSTAIN, **per-regime positive-net-edge + correlated-drawdown cap**, **hard capacity gate** (AUM/%ADV/spread-impact/frozen min-$-volume). *Reject:* edge only pooled-across-regime or only at infeasible ADV → `BLOCKED_NO_EDGE`. *Stop:* holdout unlocks **once**, then change-freeze.
- **S6 Portfolio (`FC-EP-04`/`FC-R1A-PORT`)** — 1/N floor, then greedy marginal-utility with caps; optimizer (Alt C) admitted only if it beats 1/N net-of-cost deflated. *Stop:* shipping an optimizer without the 1/N comparison.
**WAVE D — per-modality admission** (S7 data acquisition · S8 licensing · S9 technical · S10 macro · S11 fundamentals · S12 news/attention **[social weight 0 until manipulation test]** · S13 graph **[GNN rejected until it beats a GICS/Bhojraj-Lee-Oler peer baseline]** · S14 memory **[analog/RAG research-only]**). Each: *promote* only via its L3 ablation; *reject* → research-only. Independent parallel tracks.
**WAVE E — earned target** (S15 `FC-FUSE` Alt A multimodal panel — *reject:* fusion adds no marginal deflated value → **fall back to Edge-Probe+**; S16 `FC-HZN` horizon research — secondary/robustness only, never overrides the pre-registered primary).
**WAVE F — challenger** (S17 `FC-R4-SEQ` B1 causal encoder, R4-only, byte-identical determinism proof + incremental net-edge; **B2 rejected for R0–R3**). The only GPU-ish item; deferred, off the free-first path.
**WAVE G — runtime/ops** (S18 paper trading — blocked until all `TBD_BLOCKER` thresholds frozen; S19 monitoring/drift/capability-health; S20 post-decision learning — never mutates production; S21 execution boundary — kernel/runtime isolation, kill switch; **no live connectivity in R0–R1A**).

## §4. Smallest useful experiment per stage (negative-control-first)
| Stage | Experiment | Kills the stage if… |
|---|---|---|
| S1 | signal with/without split+delisting handling | artifact accounts for most "edge" |
| S2.1 | run agent search; count registered trials | trials go unlogged (deflation unsafe) |
| S2.2 | feed pure Gaussian-noise returns | reports DSR>0 / low PBO on noise |
| S2.3 | feed a pure high-beta then pure-MOM signal | residual net alpha ≠ 0 |
| S2.4 | add delisted names back to the universe | Sharpe unchanged (survivorship not captured) |
| S3 | GBT vs elastic-net vs vol-scaled 1/N, one pre-registered target | no learner beats 1/N deflated → `BLOCKED_NO_EDGE` (valid) |
| S4 | reliability of P(return>cost), in- vs out-of-regime | no out-of-regime coverage → abstain |
| S5 | per-regime + 2×-slippage net-edge check | edge only pooled / only at infeasible ADV |
| S6 | optimizer vs vol-scaled 1/N, deflated | optimizer ≤ 1/N → stays research |
| S9–S13 | single-modality ablation (marginal deflated factor-residual net value) | ≤ 0 marginal → research-only |
| S12 social | manipulation stress (coordinated spike, dup amplification) | social alters edge under manipulation |
| S13 GNN | GNN vs GICS/Bhojraj-Lee-Oler peer baseline | GNN ≤ peer baseline |
| S15 | fused panel vs best single modality + 1/N, deflated | no marginal value → FALLBACK to Edge-Probe+ |
| S17 | byte-identical rerun + incremental net-edge vs panel | non-deterministic or no incremental edge |

## §5. Migration plan (fixture-, branch-, CI-safe)
1. Branch/PR discipline unchanged (audit branch; one task/PR; four-commit test-first; golden-fixture/enum changes = human merge).
2. **`entities.py` grows only by APPEND** — new frozen entities (`TrialRegistryEntry`,
`EffectiveSampleReport`, `FactorBenchmarkSpec`, `FixedPITCohort`, `PITMembershipRecord`); enum
members appended in isolated human-reviewed PRs (`target_basis += FACTOR_RESIDUAL_RETURN`;
`ModelProducer += GBT_CROSS_SECTIONAL, ELASTIC_NET_POOLED`); a fitness test fails if any existing
field/enum index shifts.
3. **`core/time.py` reused as-is**; only appended `InformationInterval.max_available_at` (deferred to modality work).
4. **Two-tier dependency policy** (resolves `dependencies=[]`): kernel (`core/*`, primitives' pure
logic, boundary) stays dependency-free + byte-deterministic; numeric/model code behind a **pinned
`research` extra** (exact versions; single-thread BLAS; fixed seeds; sorted inputs; hash-checked
outputs) under the offline CI determinism gate. First triggered at S3.
5. Sequence: backbone (excl. TASK-R0-03/04, out of scope here) → four `FC-R0K` primitives → then unfreeze Wave C.
6. Coverage matrix is the source of truth; each slice appends code location + test ID + latest result before `TESTED_RESEARCH`.

## §6. R0 contracts needing revision — DEFERRED until the kernel is TESTED_RESEARCH
| Contract | Revision | Risk | Gate before applying |
|---|---|---|---|
| `LabelRecord` barrier rows | append barrier/touch/time/MFE-MAE label rows, `RESEARCH_ONLY` | row append (safe) | S4 proves coverage before any barrier head is gate-eligible |
| `ModelProducer` members | append `GBT_CROSS_SECTIONAL`, `ELASTIC_NET_POOLED` (later `SEQUENCE_ENCODER_R4`) | **closed-enum change** | human-reviewed PR after primitives tested |
| `InformationInterval.max_available_at` | append (modality inherits purge/embargo/max-availability) | field append (safe) | needed at S7 |
| content/source entities | instantiate `content_item/enrichment/market_link/source_profile` (PIT + license) | new entities (safe) | S12; social weight 0 until manipulation test |
| `target_basis` enum | append `FACTOR_RESIDUAL_RETURN`; set primary over `SECTOR_EXCESS_RETURN` | closed-enum change | human-reviewed; part of FC-R0K-03 |

All five are **frozen out until L0 completes**; none reorders an existing field.

## §7. Validation vs Implementation (kept separate)
- **VALIDATION** answers *"should this earn a place?"* — cheap, kill-fast, `RESEARCH_ONLY`, every
trial registered, may run in parallel any time (even during L0–L2) but **cannot write
executable-edge artifacts**. The A/B/C/D bake-off is validation, **frozen until the primitives are
tested**.
- **IMPLEMENTATION** builds an *already-admitted* thing under full test-first/PIT/replay/coverage
discipline, one task per PR. A capability crosses over **only** through its L3 admission gate.
- Consequence: the TARGET (Alt A) is **earned, not scheduled**; if no modality clears, the program
rests at the **FALLBACK = Edge-Probe+** with an honest `BLOCKED_NO_EDGE`.

## §8. Red-team gate → where encoded
Build+test 4 primitives before bake-off → §0 rule, S2, L0. Factor-residual purity (GICS fix) →
S2.3, §6. Effective-N + min-N → S2.2. Abstention = marginal P(return>cost) only → S4/S5.
Survivorship cohort → S2.4. Capacity gate → S5. Per-regime + drawdown cap → S5/S6. Mandatory 1/N →
S3/S6. Social = 0 until manipulation test → S12/S15. Pre-register one primary → S5 (one-time
unlock). Agent trials registered → S2.1, §5.6. Unfalsifiable 0-tolerance gates DEFERRED → L4/L5,
S20/S21. Challenger discipline (B1 R4-only, B2 rejected, GNN vs peer, C beneath 1/N, analog/RAG
research-only) → S17/S13/S6/S14.

**Bottom line:** build the price/volume truth-chain backbone, then the four kernel primitives
(each proven by a negative control), unfreeze the bake-off, pre-register one factor-residual
target×horizon, and run Edge-Probe+ to a single honest deflated verdict on free PIT data — most
likely `BLOCKED_NO_EDGE`. Only a modality that survives its own deflated, factor-residual,
net-of-cost, licensed ablation earns its way toward the Trust-Gated Multimodal Panel; nothing
paper-trades until every hard `TBD` threshold is frozen.
