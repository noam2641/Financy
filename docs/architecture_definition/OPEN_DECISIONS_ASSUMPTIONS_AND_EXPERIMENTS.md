# Open Decisions, Assumptions, and Experiments (Phase 2)

Companion to `ARCHITECTURE_DECISION_REGISTER.md` (ADR-###) and `OWNER_DECISION_PACKETS.md` (PKT-###). Documentation-only; nothing OWNER_APPROVED. Separates what can be settled now from what needs the owner and what needs an experiment.

---

## 0. Owner Ratification Round 1 (status update)
Per explicit owner decision: **OWNER_APPROVED** — ADR-001 (build order + validation clarification), ADR-003 (target bases: absolute-executable primary / market-excess secondary-ranking / sector-excess diagnostic), ADR-004 (`expected_return_bps`=absolute-executable), ADR-006 (raw+as-of price basis), ADR-008 (PIT survivorship-safe universe); **structure OWNER_APPROVED** — ADR-002; **partial** — ADR-007; **with deferral** — ADR-009; **in principle** — ADR-015; **methodology owner-approved (via PKT-1)** — ADR-013. **Still EMPIRICAL_TBD (numbers/values):** ADR-002 hurdles, ADR-009 SIC usability, ADR-011 learned-challenger gate, ADR-014 cost/capacity, ADR-016 thresholds, ADR-018 AI value — all carry the provisional defaults in §5 and the experiments in §6. Non-blocking items (§ADR-005/010/011/012/017/018) carried with owner-accepted working defaults. **Phase-3 blocker set (§8) is now cleared** for the ratified decisions; residual EMPIRICAL_TBDs proceed on provisional defaults + decision rules.

## 1. Decisions resolvable NOW by evidence + existing authority (recommend, then confirm)
These are low-ambiguity given canonical authority + Phase-1 evidence; the owner can ratify quickly.
- **Mechanical traceability corrections** (ADR-none / H1): `REQ-LBL→REQ-LAB`; truncate over-range VAL/MOD/DEC/RISK/PORT tokens; coverage-matrix status reset to repo-truth. *(mechanical; CFL-01/02/04)*
- **Reproducibility framing** (ADR-016): two-tier hash policy (align backlog to canonical "0 or approved tolerance"). *(CFL-07)*
- **`environment_hash` composition + resume inclusion** (ADR-016). *(CFL-10)*
- **Baseline model stack naming** (ADR-010): GBT + elastic-net + isotonic + conformal + LambdaMART challenger.
- **Validation default hierarchy** (ADR-013): purged-WF primary; DSR/PBO/CPCV applicability-conditioned.

## 2. Decisions requiring OWNER approval (leverage-ordered)
ADR-001 build order · ADR-003 target/ranking basis · ADR-004 `expected_return_bps` basis · ADR-002 edge thesis+kill · ADR-009 sector taxonomy · ADR-007 PIT data posture · ADR-006 price basis · ADR-008 universe/survivorship · ADR-015 R0/R1A scope · ADR-012 policy-weight treatment · ADR-013 validation gates · ADR-016 threshold classes · ADR-017 governance cap + legal-applicability · ADR-018 AI/LLM boundaries.

## 3. Decisions that are EMPIRICAL_TBD (cannot be resolved before an experiment)
| ID | Question | Provisional default | Decision rule | Revisit trigger |
| --- | --- | --- | --- | --- |
| ADR-002 | Does a net-of-cost, factor-residual, DSR-adjusted edge exist? | assume NO (`BLOCKED_NO_EDGE`) | promote only if net band clears w/ DSR significance across ≥2 regimes | any post-holdout threshold change |
| ADR-009 | Is a free-PIT SIC sector signal usable? | no gating sector target | adopt SIC-excess only if it beats market-excess net-of-cost | GICS license considered |
| ADR-011 | Does learned aggregation beat the frozen policy OOS? | deterministic policy | promote challenger only if it beats policy under identical cost/risk/CPCV | challenger clears gate |
| ADR-014 | What round-trip cost/capacity does the target universe incur? | conservative literature bands | freeze caps from measured spread/ADV | paper-trading realized costs (R3) |
| ADR-016 | What are the frozen threshold values? | conservative external-prior seeds | freeze before holdout; re-validate vs realized | post-holdout change policy |
| ADR-018 | Does an LLM analysis layer add measurable value? | templated explanations + optional advisory RAG | add learned-evidence LLM only on positive module-value | module-value proof in paper |

## 4. Working assumptions (explicit, so they can be challenged)
- **AS-1** A liquid, low-turnover, factor-neutral cross-section is the *most likely* place any net edge survives — else none does (base-rate from CLM-EDGE). *Confidence: medium.*
- **AS-2** Free-PIT data (raw prices + EDGAR + ALFRED) can support **INFORMATION_THEORETIC** replay honestly; **SYSTEM_REALISTIC** is impossible pre-go-live. *Confidence: high.*
- **AS-3** Effective independent sample is small (tens–low-hundreds), so high-parameter learned decision layers are unjustified for MVP. *Confidence: medium (INFERENCE, CLM-EFFN).*
- **AS-4** Team may be solo/small → governance independence must be external before paper/live. *Confidence: depends on ADR-017 owner input.*
- **AS-5** Round-trip cost is a decisive variable; the target universe must stay liquid enough that cost < gross edge. *Confidence: high on direction.*

## 5. Provisional defaults (used if a decision remains open at its last responsible point)
Market-excess primary + sector-excess secondary (ADR-003/009) · `expected_return_bps`=ABSOLUTE (ADR-004) · raw-basis + as-of CAs (ADR-006) · free-PIT stack + INFORMATION_THEORETIC (ADR-007) · as-of PIT universe incl. delisted (ADR-008) · GBT+elastic-net+isotonic+conformal (ADR-010) · deterministic policy, λ frozen prior (ADR-011/012) · validation hierarchy §6 (ADR-013) · ~10-entity R1A (ADR-015) · conservative threshold seeds (ADR-016) · solo cap at SHADOW (ADR-017) · templated explanations, no autonomous AI (ADR-018).

## 6. Experiments required (cost/duration are ILLUSTRATIVE estimates, not commitments)
| Exp | Purpose | Feeds | Rough cost/duration | Decision rule |
| --- | --- | --- | --- | --- |
| **EXP-1 Edge Probe** | net-of-cost factor-residual DSR edge on a liquid universe | ADR-001/002/003/013 | ~2–4 wks eng + free data | pass→ARCH-B; fail→`BLOCKED_NO_EDGE` |
| **EXP-2 Label↔PnL concordance** | does fixed-horizon IC map to barrier PnL? | ADR-005 | ~3–5 days on EXP-1 data | rank on executable objective if weak |
| **EXP-3 Cost/liquidity calibration** | empirical spread/ADV/impact bands | ADR-014 | ~1 wk (needs intraday/L1 or vendor) | freeze caps from measured bands |
| **EXP-4 SIC-vs-market-excess signal** | is SIC-excess usable & better? | ADR-009 | ~1 wk on EXP-1 data | adopt SIC only if it beats market-excess net |
| **EXP-5 Overnight funnel latency** | measure stage_durations at target universe | ADR-016 SLA | ~few dry-runs | freeze SLA from p95 |
| **EXP-6 (later) Learned-challenger** | does stacking beat the frozen policy OOS? | ADR-011 | post-MVP | promote only if beats under CPCV |

## 7. Revisit triggers (architecture reconsideration)
- `BLOCKED_NO_EDGE` on EXP-1 → **stop the platform build**; do not escalate to a learned layer to rescue.
- Post-holdout threshold change → trigger REQ-GOV-006 post-holdout policy + re-deflate.
- Team size ≠ solo → re-open ADR-017 governance cap.
- Licensed PIT data acquired → re-open ADR-007/009 (GICS/SYSTEM_REALISTIC).
- Any challenger (learned aggregation / deep model / LLM evidence) clears its module-value gate → re-open ADR-011/018.

## 8. Blockers for Phase 3 (architecture spec draft)
Phase 3 must not begin until ADR-001, ADR-003, ADR-004, ADR-002, ADR-009, ADR-006, ADR-007, ADR-008, ADR-015 are **either OWNER_APPROVED or explicitly marked EMPIRICAL_TBD with the provisional default + decision rule above**. The remaining ADRs (010/011/012/013/014/016/017/018) can carry provisional defaults into Phase 3 as `EMPIRICAL_TBD` without blocking the draft, provided their defaults are recorded here.
