# 16 — Unresolved Owner Decisions

**Artifact type:** owner-decision register. **Sources:** red-team (`14`), recommendation (`05`),
pre-read inventory (`01`), current-state (`02`). **Nothing here is approved.** Each item is
`OWNER_DECISION_REQUIRED`; the "recommended default" is a `PROVISIONAL_DEFAULT` the program can
run on if the owner defers, except where marked **BLOCKING** (must be decided before the named
gate). This proposal is non-binding.

Ordered by leverage.

| # | Decision | Options | Recommended default | Blocks | Origin |
|---|---|---|---|---|---|
| **OD-1** | Approve the **scope freeze**: R0–R1A = Edge-Probe+ + the four kernel primitives only; defer ALL A/B/C/D multimodal schema deltas until the six R0 gates are `TESTED_RESEARCH`. | freeze / proceed multimodal now / other | **freeze** | **BLOCKING** (start of build) | RT-1, RT-6 |
| **OD-2** | The **investable factor benchmark** the edge must beat residual-of, net-of-cost, and the **minimum surviving deflated t-stat**. | {market+MOM+STR+SMB+HML+RMW} vs ETF-proxy set; t ∈ {2.5, 3.0, 3.5} | 6-factor academic set; **t ≥ 3.0** (Harvey-Liu-Zhu) | **BLOCKING** (edge gate) | RT-2 |
| **OD-3** | **Minimum effective-N** per horizon and per regime, and the effective-N counting method. | block-bootstrap (Politis-White) / regime-factor clustering / both; N-min value | both methods; conservative N-min, frozen pre-holdout | **BLOCKING** (any significance claim) | RT-3 |
| **OD-4** | Exactly **which probabilities may drive ABSTAIN and sizing.** | marginal P(return>cost) only / + barrier/touch/time / all | **marginal P(return>cost) only**, out-of-regime coverage proven; barrier/touch/time/MFE-MAE `RESEARCH_ONLY` | **BLOCKING** (abstention gate) | RT-4 |
| **OD-5** | **Sector classification / PIT universe:** license PIT GICS+constituents, or drop sector-excess as primary and use market-excess/factor-residual + free-PIT SIC. | license (paid) / free-PIT market-excess | **free-PIT market-excess/factor-residual**; sector-excess `UNAVAILABLE` until licensed | **BLOCKING** (primary target) | RT-5 |
| **OD-6** | The single **pre-registered primary (target, horizon)** for the edge gate, named before the holdout opens. | one of {5,8,14} × {abs-exec, market-excess} | frozen before holdout; all others diagnostic, counted in deflation | **BLOCKING** (holdout access) | RT-12 |
| **OD-7** | **Capacity envelope:** stated AUM, max %ADV participation, and frozen `minimum_dollar_volume` (universe floor). | AUM/%ADV/min-$ADV values | conservative liquid-only floor; edge must survive at size | **BLOCKING** (capacity gate) | RT-14 |
| **OD-8** | **Regime buckets** and the **per-regime positive-net-edge** requirement + correlated-drawdown cap. | bucket definitions; per-regime pass rule | ≥2 regimes must show positive net edge; drawdown cap frozen | **BLOCKING** (GO verdict) | RT-13 |
| **OD-9** | **1/N (and vol-scaled 1/N)** adopted as the mandatory net-of-cost portfolio comparator; the allocator ships only if it beats 1/N OOS. | adopt / optimizer-only | **adopt 1/N as hard comparator**; do not adopt C as the spine | before portfolio layer | RT-7 |
| **OD-10** | **Social evidence weight = 0** in the executable edge for R0–R2 (advisory-only) until a manipulation-robustness test passes; social may only *raise* permission on independent multi-family confirmation, never trip ABSTAIN alone. | 0-until-proven / weighted now | **0 until proven** | before any social modality is executable | RT-10 |
| **OD-11** | **B (sequence):** require a byte-identical determinism proof + incremental net-edge, else B stays off; **B2 rejected for R0–R3.** | R4-gated B1 / off / B2 too | **R4-gated B1 only; B2 off** | before any sequence model | RT-8 |
| **OD-12** | **GNN / graph:** confirm out of R0–R3; admit only if it beats a GICS/Bhojraj-Lee-Oler peer baseline net-of-cost with a leakage audit. | rule/score only / GNN now | **rule/score only** | before any graph model | RT-9 |
| **OD-13** | Confirm the **unfalsifiable "0-tolerance" evidence gates** (unsupported-counterfactual=0, duplicate-independent-evidence=0, positive information-gain) stay `DEFERRED`/non-blocking for R0–1A. | non-blocking / enforce now | **non-blocking until estimable** | R0–1A acceptance | RT-16 |
| **OD-14** | **Data licensing per modality** (news APIs, social, Telegram, vendor prices): which sources are permitted in research vs paper vs live. | per-source determination | free-PIT (EDGAR/ALFRED/raw prices) first; each source gated on permitted-use | before promoting any gated modality | `01` DA4, `07` §5 |
| **OD-15** | **Autonomy boundary / execution ladder:** confirm the system stops at advisory (and later human-approved paper); autonomous execution remains REJECTED. | advisory-cap / paper / live | **advisory-cap; autonomous REJECTED** | before any paper/live | `01` P2/D6, `12` §5 |
| **OD-16** | **Universe breadth:** broad market (incl. small/micro) vs liquid large/mid only, given cost/data realities. | broad / liquid-only | **liquid large/mid first**; broaden only if edge survives capacity | universe build | `01` P6, RT-14 |
| **OD-17** | **Document governance:** whether canonical v4.6 or the v5 draft governs, and when v5 is formally adopted (currently v5 is DRAFT; only ~10 ADR *principles* owner-ratified). | adopt v5 / keep v4.6 authoritative / hybrid | ratify v5 principles already relied on; keep v4.6 change-controlled | before contract edits | `02` §1, ADR register |
| **OD-18** | **Dependency & determinism policy:** approve adding numpy/pandas/sklearn (and the two-tier reproducibility tolerance) for the modeling stages, given today's `dependencies=[]`. | approve / stdlib-only | approve for S5/S6 modeling only, quarantined behind two-tier repro | before model/stats stages | `02` §5 |

**Highest-leverage first (blocking the build):** OD-1 → OD-5 → OD-2 → OD-3 → OD-4 → OD-6 →
OD-7 → OD-8. These eight gate whether the edge verdict is *trustworthy*; the rest can run on
provisional defaults. The single most consequential is **OD-1**: without the scope freeze, the
multimodal superstructure gets built around an unbuilt, un-deflated foundation — the exact failure
the red-team ranks most likely to produce a false GO.
