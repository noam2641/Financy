# 01 — Independent Pre-Read Question Inventory

**Artifact type:** architecture-reassessment pre-read (Phase 1).
**Status:** written from the *target product mission alone*, before integrating any
specialist-agent findings and before re-reading the repository's forward-looking
model recommendations. Its purpose is to fix an independent baseline of what the
mission demands, so the existing R0 design cannot silently anchor the target
architecture. This is an inventory of questions, assumptions, and failure modes —
not a reasoning transcript and not a set of answers.

A later artifact (`02_CURRENT_STATE_RECONSTRUCTION_AND_GAP_ANALYSIS.md`) compares
this inventory against the as-built design and marks each question **answered
well / partially answered / ignored / decided too early**, and flags **new
questions discovered during inspection**.

Every question below is tagged with the decision-label it will ultimately carry:
`EVIDENCE_SUPPORTED · ARCHITECTURAL_INFERENCE · EMPIRICAL_TBD · OWNER_DECISION_REQUIRED · REJECTED_ALTERNATIVE · DEFERRED`.

---

## A. Product questions

- **P1.** What is the atomic deliverable — a per-instrument decision, a ranked cross-sectional action set per cycle, or both? At what cadence (overnight/EOD)? *(OWNER_DECISION_REQUIRED)*
- **P2.** Who consumes the output and with what authority — advisory only, paper, or human-approved live? The mission states autonomous execution is **not** authorized; where exactly is the autonomy boundary drawn? *(OWNER_DECISION_REQUIRED)*
- **P3.** What is "success" for the *product*, distinct from model accuracy? A disciplined, auditable, net-of-cost go/no-go with honest abstention — or breadth of coverage? *(ARCHITECTURAL_INFERENCE)*
- **P4.** What must the system be structurally *incapable* of doing (fabricating confidence, look-ahead, silent threshold changes, autonomous orders)? *(OWNER_DECISION_REQUIRED)*
- **P5.** What is the minimum configuration that delivers real value, and how do we avoid building a large multimodal platform *around an unproven premise*? Is there a value-bearing product if the edge probe returns "no edge"? *(EMPIRICAL_TBD)*
- **P6.** What universe breadth is in scope (large/mid liquid vs full broad market incl. small/micro), given cost and data realities? *(OWNER_DECISION_REQUIRED)*

## B. Forecast questions

- **F1.** *What exactly is predicted?* The mission lists ≥16 target semantics (terminal expected/median return, quantiles/intervals, P(positive), P(exceeds cost), P(exceeds threshold), P(touch before horizon), expected time-to-target, MFE, MAE, drawdown distribution, market/sector-relative, rank, portfolio utility, action, size). Which are **primary**, which **derived**, which **out of scope for a first probe**? *(OWNER_DECISION_REQUIRED + EMPIRICAL_TBD)*
- **F2.** Point estimate vs full predictive **distribution** vs **path** object? A single expected-return scalar is almost certainly insufficient for the mission's probability/barrier/MAE claims. *(ARCHITECTURAL_INFERENCE)*
- **F3.** Which **basis** is primary — absolute-executable, market-excess, sector-excess, cross-sectional rank — and can they be mixed without corrupting cost subtraction? *(EVIDENCE_SUPPORTED that they must not be mixed in cost math; basis choice EMPIRICAL_TBD)*
- **F4.** What **horizon(s)**? 5/8/14 sessions are inherited probe values; are fixed horizons even the right frame vs **dynamic / event-conditioned / barrier-touch / survival** horizons? *(EMPIRICAL_TBD)*
- **F5.** How are modalities **fused into interactions**, not summed as independent scores? (e.g., good company news *conditioned on* a hostile sector regime.) What fusion mechanism, and how is it validated to add value over additive baselines? *(EMPIRICAL_TBD)*
- **F6.** How is **uncertainty** represented and propagated (aleatoric/epistemic/model-disagreement/data-quality/regime/execution), and how does it reach the decision? *(ARCHITECTURAL_INFERENCE)*
- **F7.** How is a **missing modality** represented in the forecast — never as "neutral," possibly as a missingness feature, a fallback model, widened intervals, shrinkage, or abstention? *(ARCHITECTURAL_INFERENCE)*

## C. Decision questions

- **D1.** How does a forecast distribution become an action `{BUY, HOLD, REDUCE, EXIT, ABSTAIN}`? Deterministic penalized-utility policy vs learned aggregator? *(EVIDENCE_SUPPORTED lean to deterministic on small samples; EMPIRICAL_TBD)*
- **D2.** What is the **abstention** rule set — stale, contradictory, manipulated, out-of-distribution, insufficiently calibrated, insufficient effective support? Abstention must be first-class and cheap to reach. *(ARCHITECTURAL_INFERENCE)*
- **D3.** **Sizing**: how is a position size produced, and is the invariant "size is produced once and may only shrink thereafter" preserved? No alpha/probability may size a position directly. *(EVIDENCE_SUPPORTED as a discipline)*
- **D4.** Absolute thresholds vs **cross-sectional** comparison — how are opportunities compared against each other and against cash/abstention? *(ARCHITECTURAL_INFERENCE)*
- **D5.** Portfolio-level controls: concentration, sector, beta, factor, correlation, turnover/hysteresis. Greedy risk-budgeting vs optimizer? *(EVIDENCE_SUPPORTED lean away from optimizer on small samples)*
- **D6.** The **autonomy ladder**: research forecast → advisory recommendation → paper trade → human-approved order → (never, absent explicit owner decision) autonomous execution. Where are the gates? *(OWNER_DECISION_REQUIRED)*

## D. Data questions

- **DA1.** What data is *actually* PIT-available and *legally* accessible per modality — prices/volume, corporate actions, fundamentals/filings, analyst revisions, news, **public Telegram**, social attention? *(EMPIRICAL_TBD)*
- **DA2.** Where does a **survivorship-safe PIT universe / constituent-and-delisting** source come from (signed manifest vs licensed vendor)? This gates validity of the whole probe. *(OWNER_DECISION_REQUIRED / sourcing)*
- **DA3.** How trustworthy are **timestamps** across modalities — publication, first-observed, edit, deletion — and how is `system_available_at` prevented from being fabricated? Social/Telegram timestamps are the weakest. *(EMPIRICAL_TBD)*
- **DA4.** **Licensing/terms** constraints (yfinance ToS, GICS proprietary, news APIs, Telegram/social platform terms) — which modalities are usable in research vs paper vs live? *(OWNER_DECISION_REQUIRED)*
- **DA5.** How is heterogeneous multimodal content **normalized into PIT records** with provenance, dedup, and lineage? *(ARCHITECTURAL_INFERENCE)*
- **DA6.** **Source-reliability** history and **novelty/attention-velocity** as features — how tracked without becoming a truth signal? ("30 posts in 5 days" is attention, not truth.) *(ARCHITECTURAL_INFERENCE)*
- **DA7.** Data **freshness/staleness** and **drift/OOD** detection — how surfaced to the decision and to abstention? *(ARCHITECTURAL_INFERENCE)*

## E. Risk questions

- **R1.** Transaction **costs / liquidity / capacity / market impact** — round-trip, two-sided, √-impact, conservative PROXY floors; is the target universe liquid enough that cost < gross edge? *(EVIDENCE_SUPPORTED that cost is decisive; numbers EMPIRICAL_TBD)*
- **R2.** **Gap / overnight / earnings tail** risk and sizing to worst-case gap rather than stop distance. *(EVIDENCE_SUPPORTED direction)*
- **R3.** **Portfolio** risk: concentration, correlation, factor/beta exposure, drawdown; hidden factor bets disguised as alpha. *(ARCHITECTURAL_INFERENCE)*
- **R4.** **Regime instability** and **correlated model failure** across modalities in a shift. *(EMPIRICAL_TBD)*
- **R5.** **Manipulation / source-poisoning / prompt-injection** risk from social and Telegram content, and defenses. *(ARCHITECTURAL_INFERENCE)*
- **R6.** **Model risk**: overfitting, multiple testing across modalities × horizons × targets, concept drift, OOD. *(EVIDENCE_SUPPORTED as a risk class)*

## F. Research questions (the falsifiable core)

- **RQ1.** *Does a net-of-cost, factor-residual, out-of-sample, cross-sectional edge exist at these horizons at all?* This is load-bearing; default assumption **no** until shown. *(EMPIRICAL_TBD)*
- **RQ2.** Does **each modality** (technical, macro/regime, fundamentals, news, social, graph, memory) add **stable, cost-adjusted, OOS** value **beyond simpler alternatives**? Requires per-modality and combination **ablations**. *(EMPIRICAL_TBD)*
- **RQ3.** Do **interactions** add value beyond additive per-modality scores? *(EMPIRICAL_TBD)*
- **RQ4.** Are the claimed **probabilities calibratable** given the (likely small) **effective independent sample**, per target definition and regime? *(EMPIRICAL_TBD)*
- **RQ5.** Which **horizon(s)** are best; are fixed horizons the right frame vs dynamic/event/barrier? *(EMPIRICAL_TBD)*
- **RQ6.** Does a **graph** add beyond peer aggregates? Does **retrieval/analog memory** add without leakage? Do **sequence models** beat GBT net-of-cost? Is the **agent layer** useful or decorative? *(EMPIRICAL_TBD)*

## G. Working assumptions (stated so they can be challenged)

- **AS1.** A net-of-cost edge, if it survives anywhere, is most likely in a liquid, low-turnover, factor-aware cross-section — else nowhere. *(ARCHITECTURAL_INFERENCE; confidence medium)*
- **AS2.** More modalities ≠ better; added signals are often redundant/correlated and inflate multiple-testing and overfitting risk. *(ARCHITECTURAL_INFERENCE)*
- **AS3.** Fine-grained calibrated probabilities are bounded by effective sample size, which is small under overlapping labels + cross-sectional dependence + few regimes. *(ARCHITECTURAL_INFERENCE; the "small effective sample" premise is itself an inference to be tested, not a measurement.)*
- **AS4.** Historical analogs are *evidence, not causal proof*, and retrieval is a **leakage surface** unless strictly as-of. *(ARCHITECTURAL_INFERENCE)*
- **AS5.** Multimodal PIT data — especially social/Telegram — is **partially untrustworthy** (timestamps, deletions, manipulation); some modalities may be unusable in production. *(EMPIRICAL_TBD)*
- **AS6.** The R0 truth-kernel rigor (PIT, survivorship, corporate actions, purged/embargoed CV, trial registry, reproducibility, audit ledger) **transfers and must be preserved**, but the multimodal setting opens **new** leakage surfaces (retrieval, graph, text availability, future membership) that the current design does not yet guard. *(ARCHITECTURAL_INFERENCE)*
- **AS7.** Autonomous execution is **not** authorized; the LLM/agent layer may organize, retrieve, explain, and route — but may not invent, alter, or round probabilities, change thresholds, or place orders. *(OWNER-affirmed constraint)*

## H. Candidate failure modes (to be red-teamed)

- **FM1.** *No edge / edge below the cost floor* — and the program fails to stop honestly, escalating complexity to rescue a negative result.
- **FM2.** *Spec-maturity mistaken for implementation-maturity* — a large multimodal design that proves nothing on the actual effective sample.
- **FM3.** *New-modality leakage* — retrieval leakage, graph look-ahead (future constituents/correlations), text/social availability-timestamp leakage, restatement/back-adjustment leakage.
- **FM4.** *Multiple-testing / overfitting explosion* across modalities × horizons × targets × fusion variants.
- **FM5.** *Uncalibrated or fabricated probabilities* — analog frequencies or LLM outputs presented as calibrated; upward rounding; meaning-shift between "touch" and "terminal" probabilities.
- **FM6.** *Manipulation* — coordinated social/Telegram campaigns, pump-and-dump, circular reporting, impersonation, prompt injection embedded in ingested content.
- **FM7.** *Correlated model failure* in a regime shift; regime detector itself fragile/spurious.
- **FM8.** *Missing-modality treated as neutral*, silently biasing forecasts and sizes.
- **FM9.** *Data unavailability / licensing* removes whole modalities late, invalidating the design.
- **FM10.** *Operational infeasibility* — too large to validate within the effective sample, compute, or a solo/small-team budget.
- **FM11.** *Agent hallucination / decorative agent* — an orchestration layer that adds narrative but no measurable value, or that quietly assumes authority it must not have.
- **FM12.** *Portfolio concentration / disguised factor bet* — apparent alpha that is unpriced beta or a crowded exposure.

---

### Discipline notes carried into the reassessment
- Do **not** preserve a choice merely because it appears in a contract; do **not** reject a choice merely to appear creative. Creativity = simpler, stronger, more useful, more testable, more falsifiable.
- Every complex component must earn its place with **stable, cost-adjusted, out-of-sample value beyond simpler alternatives**, demonstrated by ablation.
- Every numerical probability is `NOT_ESTIMABLE / INSUFFICIENT_SUPPORT / OUT_OF_DISTRIBUTION / ABSTAIN` unless it clears the probability-integrity bar (defined in `11_PROBABILITY_INTEGRITY_POLICY.md`).
