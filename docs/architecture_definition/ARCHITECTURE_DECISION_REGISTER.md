# Architecture Decision Register (Phase 2)

**Status of this document:** every decision below is a **PROPOSED_RECOMMENDATION** or **OWNER_APPROVAL_REQUIRED** or **EMPIRICAL_TBD**. **Nothing is `OWNER_APPROVED`** — no owner approval has been given. Documentation-only; canonical v4.6 unmodified; no root-document edits applied (only proposed). Built on the full twelve-document review (`TWELVE_DOCUMENT_CONSISTENCY_REVIEW.md`, `DOCUMENT_AUTHORITY_AND_CONFLICT_MATRIX.md`) and the Phase-1.5 evidence integrity layer.

**Status vocabulary:** PROPOSED_RECOMMENDATION · OWNER_APPROVAL_REQUIRED · EMPIRICAL_TBD · DEFERRED · REJECTED · OWNER_APPROVED (unused). **Freeze class:** ARCHITECTURAL_INVARIANT · STABLE_INTERFACE · REVERSIBLE_COMPONENT_CHOICE · POLICY_CONFIGURATION · EMPIRICAL_PARAMETER. **cross_document_consistency_status:** CONSISTENT · EXTENSION_ONLY · TENSION_REQUIRES_CLARIFICATION · CONFLICT_REQUIRES_OWNER_DECISION · EMPIRICAL_TBD · TRACEABILITY_DEFECT · STALE_REFERENCE. Owner-facing summaries (EN + HE) in `OWNER_DECISION_PACKETS.md`; experiments/assumptions in `OPEN_DECISIONS_ASSUMPTIONS_AND_EXPERIMENTS.md`.

---

### ADR-001 — Build order & edge-probe scope
- **Question:** Build the full platform first, or a rigorous Edge Probe (ARCH-A) before any §3.7–3.10 / §23 work?
- **REQ IDs:** REQ-REL0-001, REQ-REL4-003, REQ-PROD-020, R0-BL-006. **Gates:** release_0_definition, release_0_acceptance.
- **Alternatives:** (a) full-platform-first; (b) Release-0-truth-kernel-first; (c) thin edge-probe-first; (d) hybrid = **rigorous edge probe using the R0 truth-kernel machinery**.
- **Strongest support:** CLM-EDGE/COST (SRC-QUANT-001/002/003/007); A7 pre-mortem #1/#2. **Strongest counter:** a probe that skips PIT/survivorship rigor yields a false positive (A7's own twist) → the probe must be rigorous, not thin.
- **Source IDs:** SRC-QUANT-001/002/003/007, SRC-SIMP-001/002. **Grades:** SQ A, PA B, ER A, PV B, RS A.
- **Recommended:** (d) hybrid — ARCH-A rigorous edge probe first. **Provisional default (if unresolved):** proceed with R0 truth-kernel build only; do not start §3.7–3.10/§23.
- **Consequences:** fastest honest go/no-go; defers ~24 entities. **Reversibility:** high (subset of spec). **LRDP:** before R0 implementation begins.
- **Experiment:** the edge probe itself (see ADR-002). **Cost/duration:** ~2–4 weeks eng + data (est., ILLUSTRATIVE). **Decision rule:** adopt unless owner mandates platform-first with justification. **Revisit trigger:** probe passes → escalate to ARCH-B.
- **Freeze class:** ARCHITECTURAL_INVARIANT. **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION (RVC-01/CFL-11). **Docs to change on approval:** backlog (sequencing), canonical patch (thesis framing note).

### ADR-002 — Falsifiable edge thesis & kill criterion
- **Question:** What is the pre-registered, falsifiable edge hypothesis and its kill criterion?
- **REQ IDs:** REQ-PROD-004, REQ-LAB-006, REQ-VAL-004. **Gates:** release_0_acceptance, final_holdout.
- **Alternatives:** (a) no explicit thesis (status quo); (b) per-`opportunity_type` thesis w/ effect-size band, half-life, capacity, and a `BLOCKED_NO_EDGE` kill rule.
- **Strongest support:** CLM-EDGE, CLM-MULTITEST (SRC-QUANT-001/002/006/008). **Strongest counter:** effect-size priors are uncertain → set as a band, not a point.
- **Grades:** SQ A, PA B, ER A, PV B, RS A. **Recommended:** (b). **Provisional default:** assume no edge until proven; register a conservative net-of-cost hurdle from literature.
- **Consequences:** makes the whole program falsifiable. **Reversibility:** high. **LRDP:** before final-holdout access.
- **Experiment:** factor-attributed, net-of-cost, DSR-adjusted baseline vs investable benchmark on a liquid universe. **Cost/duration:** part of ADR-001 probe. **Decision rule:** promote only if net band clears with DSR-adjusted significance; else `BLOCKED_NO_EDGE`. **Revisit trigger:** any threshold change post-holdout.
- **Freeze class:** EMPIRICAL_PARAMETER. **Status:** EMPIRICAL_TBD + OWNER_APPROVAL_REQUIRED (for the pre-registered hurdle). **cross_doc_status:** EMPIRICAL_TBD (RVC-01).

### ADR-003 — Target basis & ranking basis
- **Question:** Which target family is primary; is ranking relative or absolute?
- **REQ IDs:** REQ-LAB-005/006, REQ-MOD-008/009. **Gates:** architecture_freeze, release_0_definition, release_1A.
- **Alternatives:** primary ∈ {sector-excess, market-excess, absolute}; ranking basis relative vs absolute.
- **Strongest support:** CLM-STR/GICS (SRC-QUANT-004/006, SRC-DATA-003); A1/A2/A4/A5 (CX-2). **Strongest counter:** sector-neutral ranking genuinely reduces sector beta — keep sector-excess as a *ranking* input.
- **Grades:** SQ A, PA B, ER A, PV A, RS A. **Recommended:** primary = **absolute-executable or market-excess**; **sector-excess retained as a secondary ranking/diagnostic input only** (ties to ADR-009). **Provisional default:** market-excess primary; sector-excess secondary.
- **Consequences:** resolves the monetizability + PIT-sourcing problems together. **Reversibility:** medium (label/target rework). **LRDP:** before R0 label implementation.
- **Experiment:** compare IC/net-edge under each basis on the probe. **Decision rule:** pick the basis with the best factor-residual net-of-cost edge. **Revisit trigger:** sector-relative objective later justified.
- **Freeze class:** ARCHITECTURAL_INVARIANT. **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION (CFL-05, RVC-02).

### ADR-004 — `expected_return_bps` basis in `economic_edge_bps`
- **Question:** Which basis feeds the cost subtraction?
- **REQ IDs:** REQ-DEC-001, REQ-LAB-005/006. **Gates:** architecture_freeze, release_0_definition.
- **Alternatives:** absolute-executable / market-excess / sector-excess / unspecified (status quo).
- **Strongest support:** A4-F-A4-01 (subtracting absolute cost from relative return is incoherent for long-only). **Strongest counter:** none material.
- **Grades:** SQ A (spec-internal logic), PA A. **Recommended:** **pin to `ABSOLUTE_RETURN` (executable)**; sector-excess never enters the subtraction. **Provisional default:** absolute-executable.
- **Consequences:** every downstream utility/rank_score becomes coherent. **Reversibility:** high (one normative clause). **LRDP:** before decision-layer design.
- **Freeze class:** STABLE_INTERFACE. **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION (CFL-06). **Docs to change:** canonical patch (REQ-DEC-001 note), D.

### ADR-005 — Research target vs executed-policy return
- **Question:** Rank/select on the fixed-horizon research label or on the executable (barrier-aware) policy return?
- **REQ IDs:** REQ-LAB-001/003/004/011, REQ-SCH-019. **Gates:** release_0_acceptance, release_1A.
- **Alternatives:** (a) rank on fixed-horizon label; (b) rank on barrier-aware policy return; (c) MVP without stops (label = traded return); (d) prove IC→PnL concordance and keep label.
- **Strongest support:** CLM-LABEL (SRC-QUANT-013, SRC-EXEC-002); A1-F07/A5-F03. **Strongest counter:** barrier labels add path-dependence & another modeling choice.
- **Grades:** SQ A, PA B, ER A. **Recommended:** (c) MVP without stops OR (d) demonstrate concordance before adding barriers. **Provisional default:** (c) pure horizon exit for the probe.
- **Reversibility:** high. **LRDP:** before R1A execution design.
- **Freeze class:** STABLE_INTERFACE. **Status:** PROPOSED_RECOMMENDATION. **cross_doc_status:** TENSION_REQUIRES_CLARIFICATION (RVC-01).

### ADR-006 — Price basis & corporate actions
- **Question:** Which price series for which use; how are corporate actions handled?
- **REQ IDs:** REQ-PRICE-001..006, REQ-LAB-001/007. **Gates:** release_0_definition, release_0_acceptance.
- **Alternatives:** raw / split-adjusted / total-return / as-of-adjusted / current-vintage back-adjusted per use.
- **Strongest support:** CLM-YFIN (SRC-DATA-001); price-basis matrix (integrity review §5). **Strongest counter:** as-of derivation adds engineering vs trusting vendor adjustment.
- **Grades:** SQ B, PA A, PV A. **Recommended:** immutable **raw** vintage + versioned corporate-action table; derive adjusted **as-of** (`ex_date ≤ cutoff`); declare `price_basis` on labels; forbid current-vintage back-adjusted in levels/filters/universe/labels (split-only simple returns exempt). **Provisional default:** raw-basis + as-of, `auto_adjust=False`.
- **Reversibility:** medium. **LRDP:** before R0 data adapter.
- **Freeze class:** ARCHITECTURAL_INVARIANT. **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** EXTENSION_ONLY (extends REQ-PRICE) + TRACEABILITY (REQ-LAB-001 gap). **Docs to change:** canonical patch (REQ-LAB-001 `price_basis`), E.

### ADR-007 — PIT data posture & provider shortlist
- **Question:** What data posture and providers, and which replay class pre-go-live?
- **REQ IDs:** REQ-DATA-001..008, REQ-TIME-006/008, REQ-CONV-DATA-008, REQ-DATA-004. **Gates:** architecture_freeze, shadow, paper, live.
- **Alternatives:** yfinance-only proto / licensed vendor / free-PIT stack (EDGAR+ALFRED+raw prices) / hybrid.
- **Strongest support:** CLM-YFIN/GICS/EDGAR/ALFRED/SURV (SRC-DATA-001..008). **Strongest counter:** licensed vendors cost money & lead time.
- **Grades:** SQ A (official), PA A, PV A. **Recommended:** yfinance **prototyping-only**; **INFORMATION_THEORETIC replay only pre-go-live**; free-PIT stack (raw prices + EDGAR as-filed + ALFRED vintages + independent corporate-actions/delistings); licensed vendor budgeted before shadow. **Provisional default:** free-PIT stack, INFORMATION_THEORETIC, start recording ingestion timestamps forward.
- **Reversibility:** high (providers swappable behind adapters). **LRDP:** before shadow; licensing lead-time starts now.
- **Freeze class:** REVERSIBLE_COMPONENT_CHOICE (providers) + ARCHITECTURAL_INVARIANT (replay posture). **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** EXTENSION_ONLY + EMPIRICAL_TBD (licensing cost). **Docs to change:** E, backlog.

### ADR-008 — Universe, delistings, ticker history, survivorship
- **Question:** How is the universe constructed to avoid survivorship & entity-resolution corruption?
- **REQ IDs:** REQ-DOM-015..019, REQ-LAB-013, REQ-CONV-LINK-007. **Gates:** architecture_freeze, release_0_acceptance, final_holdout.
- **Strongest support:** CLM-SURV (SRC-QUANT-015, SRC-DATA-008); A2-F04/F09. **Strongest counter:** PIT constituent data is harder to source free.
- **Grades:** SQ B, PA B, PV A. **Recommended:** construct universe **as-of backtest-start including later-delisted names**; opaque `instrument_id` + `instrument_identifier_history` (CIK/FIGI); terminal-event returns; ban ticker joins. **Provisional default:** fixed enumerated PIT universe with recorded entries/exits.
- **Reversibility:** medium. **LRDP:** before R0 universe build.
- **Freeze class:** ARCHITECTURAL_INVARIANT. **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** EXTENSION_ONLY.

### ADR-009 — Sector taxonomy
- **Question:** Which sector taxonomy (if any) backs a sector-relative objective?
- **REQ IDs:** REQ-LAB-006/009/010, REQ-CONV-GRAPH-003. **Gates:** architecture_freeze, release_0_definition, release_1A.
- **Alternatives (five, integrity review §4):** paid PIT GICS / free PIT SIC-with-new-target / market-excess primary / absolute-return primary / sector-excess-secondary-diagnostic. **SIC ≠ GICS.**
- **Strongest support:** CLM-GICS/SIC (SRC-DATA-003/004). **Strongest counter:** market/absolute primary loses sector-neutrality; SIC peer groups may be too coarse to help.
- **Grades:** SQ A, PA B, PV A. **Recommended:** default **market-excess/absolute primary + sector-excess as secondary diagnostic** (options 3/4/5); GICS/SIC only if a sector-relative *objective* is later justified. **Provisional default:** no gating sector target.
- **Reversibility:** medium. **LRDP:** before R0 label build.
- **Freeze class:** POLICY_CONFIGURATION. **Status:** OWNER_APPROVAL_REQUIRED + EMPIRICAL_TBD (SIC usability). **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION (CFL-05).

### ADR-010 — Baseline forecast models
- **Question:** What is the named MVP baseline model stack?
- **REQ IDs:** REQ-MOD-001/002, REQ-REL0-001, REQ-VAL-004. **Gates:** release_0_definition.
- **Strongest support:** CLM-GBT/CALIB/CONF (SRC-MODEL-001/002/003/004/007/008). **Strongest counter:** SRC-MODEL-005 (complexity can help — but market-timing only; does not transfer).
- **Grades:** SQ A, PA A/B, ER A. **Recommended:** **elastic-net + per-date cross-sectional regression (comparator); GBT (LightGBM/XGBoost) primary; isotonic/Platt calibration; conformal/CQR + quantile intervals; LambdaMART challenger.** All deep/graph/LLM = R4 challengers. **Provisional default:** GBT + elastic-net + isotonic.
- **Reversibility:** high (component choice). **LRDP:** before R0 baseline.
- **Freeze class:** REVERSIBLE_COMPONENT_CHOICE. **Status:** PROPOSED_RECOMMENDATION. **cross_doc_status:** EXTENSION_ONLY (names what canonical left open).

### ADR-011 — Deterministic policy vs learned aggregation
- **Question:** Is the MVP decision layer a deterministic penalized-utility policy or a learned aggregator?
- **REQ IDs:** REQ-DEC-001..006, REQ-MOD-008..019, REQ-CONV-MOD-004/007, REQ-REL4-002. **Gates:** architecture_freeze, release_1A.
- **Strongest support:** CLM-DETERM (SRC-DEC-001/002, CLM-EFFN). **Strongest counter:** if effective sample proves larger / a challenger clears the gate, a learned layer could add value (EMPIRICAL).
- **Grades:** design INFERENCE (not Grade-A evidence). **Recommended:** **deterministic penalized-utility policy for MVP**; learned stacking/MoE = gated Research-Factory challenger that must beat the frozen policy OOS under identical cost/risk/CPCV. **Provisional default:** deterministic policy.
- **Reversibility:** high (challenger path preserved). **LRDP:** before R1A decision-layer build.
- **Freeze class:** REVERSIBLE_COMPONENT_CHOICE. **Status:** PROPOSED_RECOMMENDATION + EMPIRICAL_TBD (challenger gate). **cross_doc_status:** CONSISTENT (canonical already defers learned aggregation to R4).

### ADR-012 — Policy-weight treatment (λ and score→bps)
- **Question:** Are the utility λ and mappings frozen priors or fitted?
- **REQ IDs:** REQ-DEC-002, REQ-STOP-002, REQ-VAL-008. **Gates:** architecture_freeze, final_holdout.
- **Strongest support:** A4-F-A4-02; CLM-MULTITEST. **Strongest counter:** fitted λ could improve utility — but then carry the full PBO/DSR burden.
- **Grades:** SQ A (methodological). **Recommended:** classify every weight as `FROZEN_ECONOMIC_PRIOR` / `OWNER_POLICY_PARAMETER` / `FIT_ON_TRAINING_ONLY` / `EMPIRICAL_THRESHOLD` / `PROMOTION_THRESHOLD`; **utility λ = FROZEN_ECONOMIC_PRIOR for MVP**; any value chosen after viewing backtest → trial-registered + DSR/PBO. **Provisional default:** frozen priors.
- **Reversibility:** high. **LRDP:** before any backtest that consumes λ.
- **Freeze class:** POLICY_CONFIGURATION. **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** EXTENSION_ONLY.

### ADR-013 — Validation-method applicability
- **Question:** Which validation methods, in what role, with what applicability?
- **REQ IDs:** REQ-VAL-001..010. **Gates:** release_0_acceptance, final_holdout.
- **Strongest support:** CLM-CPCV/DSR/PBO/BENCH (SRC-QUANT-008/009/014, SRC-QUANT-012). **Strongest counter:** over-gating early stalls the probe.
- **Grades:** SQ A/B. **Recommended:** default hierarchy (integrity review §6): purged-WF (primary) → embargo ≥ max interval → **trial registry (mandatory)** → DSR (when multiple trials) → PBO (secondary; not-estimable ≠ pass/fail) → CPCV (robustness) → block bootstrap → **factor attribution + investable benchmark (edge gate)** → locked holdout → paper revalidation. **DSR/PBO/CPCV are NOT universal Release-0 starting blockers.** **Provisional default:** the hierarchy as stated.
- **Reversibility:** medium. **LRDP:** before R0 acceptance criteria are frozen.
- **Freeze class:** ARCHITECTURAL_INVARIANT (methodology) + EMPIRICAL_PARAMETER (thresholds). **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** EXTENSION_ONLY (adds DSR/CPCV/factor-attr/benchmark to canonical). **Docs to change:** canonical patch (REQ-VAL), E.

### ADR-014 — Transaction-cost & capacity framework
- **Question:** How are round-trip cost, impact, and capacity modeled and frozen?
- **REQ IDs:** REQ-COST-001..003, REQ-RISK-003, REQ-SCH-017/019, REQ-PRICE-005/006, REQ-FILL-*. **Gates:** release_0_definition, release_1A, paper, live.
- **Strongest support:** CLM-COST/IMPACT/PROXY/GAP (SRC-EXEC-001..008, SRC-QUANT-003). **Strongest counter:** exact costs unknown pre-paper (403s) → ranges.
- **Grades:** SQ B, PA B, ER A, RS B (point figures C). **Recommended:** **round-trip (two-sided)** cost incl. exit/close-auction leg; per-name impact ≈ √(size/ADV); quantify PROXY open-fill floor; freeze `maximum_ADV_participation`/`maximum_spread`/order caps; size to worst-case gap not stop distance. **Provisional default:** conservative literature bands; liquid large/mid universe only.
- **Reversibility:** medium. **LRDP:** before R0 cost model / R1A sizing.
- **Freeze class:** EMPIRICAL_PARAMETER. **Status:** EMPIRICAL_TBD + OWNER_APPROVAL_REQUIRED. **cross_doc_status:** EXTENSION_ONLY + EMPIRICAL_TBD.

### ADR-015 — Release-0 & Release-1A minimal scope
- **Question:** What is the exact minimal scope of R0 and R1A?
- **REQ IDs:** REQ-REL0-001, REQ-REL1A-001/002, REQ-SCH-001..031 (R1A-BL-002), REQ-PROD-020, REQ-DOM-032. **Gates:** release_0_definition, release_1A.
- **Strongest support:** CLM-PROPORTION (SRC-SIMP-001/002); CX-9; CFL-11/12. **Strongest counter (guard):** do NOT complexify the proportionate parts (modular monolith, kernel, feature_snapshot, ledger).
- **Grades:** SQ B, PA A. **Recommended:** R0 = truth-kernel/edge-probe (Q2 list); R1A = **~10 kernel-written entities** + frozen-policy decision kernel + calibration/abstention + risk sizing + minimal runtime_manifest + capability-health; **defer** evidence-DAG/world-hypotheses/opportunity-analytics/KG/LLM/counterfactual-factory to their producer releases; keep append-only ledger + cohort logging. **Provisional default:** ~10-entity R1A core; rest DESIGNED.
- **Reversibility:** medium. **LRDP:** before R1A schema work.
- **Freeze class:** ARCHITECTURAL_INVARIANT (release-scope). **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION (CFL-11/12, RVC-05). **Docs to change:** backlog (R1A-BL-002).

### ADR-016 — Threshold classes & freeze protocol
- **Question:** How are the 8+ TBD thresholds classified and frozen?
- **REQ IDs:** REQ-GATE-001/003, REQ-GOV-005/006, backlog "Readiness Thresholds". **Gates:** final_holdout, shadow, paper, live.
- **Strongest support:** A7-F06; REQ-GATE-003 (self-blocks readiness). **Strongest counter:** thresholds need data → circularity; resolved by external-prior seeding.
- **Grades:** SQ A (spec-internal). **Recommended:** classify each threshold (`EMPIRICAL_THRESHOLD` vs `PROMOTION_THRESHOLD` vs `OWNER_POLICY_PARAMETER`); **seed provisional values from external priors before holdout**, separate "learning thresholds" from locked "acceptance thresholds"; two-tier reproducibility; define `environment_hash`; freeze overnight SLA from measured stage_durations. **Provisional default:** conservative external-prior seeds, signed.
- **Reversibility:** high (until frozen); post-holdout change triggers REQ-GOV-006 policy. **LRDP:** before final-holdout access.
- **Freeze class:** POLICY_CONFIGURATION + EMPIRICAL_PARAMETER. **Status:** OWNER_APPROVAL_REQUIRED + EMPIRICAL_TBD. **cross_doc_status:** EXTENSION_ONLY + EMPIRICAL_TBD (CFL-07/10).

### ADR-017 — Governance & human approval
- **Question:** What governance/independence controls, and how far can a solo operator go?
- **REQ IDs:** REQ-GOV-001..012, REQ-KILL-001, REQ-EXEC (approval). **Gates:** paper, live.
- **Strongest support:** CLM-GOV (SRC-OPS-001, **INDUSTRY_BEST_PRACTICE not legal**). **Strongest counter:** solo teams cannot staff independent roles.
- **Grades:** SINGLE_AGENT_SUPPORTED. **Recommended (INTERNAL_POLICY_CHOICE):** solo operation caps at RESEARCH/SHADOW; PAPER/LIVE require a named external reviewer (effective challenge) + a second kill-switch resetter; do not weaken two-person reset. **Also:** obtain a legal-applicability determination (counsel) rather than assuming SR 11-7/26-2 binds. **Provisional default:** cap at SHADOW for a solo operator.
- **Reversibility:** high (policy). **LRDP:** before any PAPER promotion.
- **Freeze class:** POLICY_CONFIGURATION. **Status:** OWNER_APPROVAL_REQUIRED. **cross_doc_status:** TENSION_REQUIRES_CLARIFICATION (CX-11 SINGLE_AGENT).

### ADR-018 — AI/LLM advisory & analysis layer
- **Question:** What role may an LLM play, and with what boundaries?
- **REQ IDs:** REQ-LLM-001..005, REQ-CONV-CONT-004..007, REQ-PROD-012/022. **Gates:** release_1A (boundaries), paper, live.
- **Alternatives (eight):** no-LLM / advisory NL query / RAG over approved artifacts / structured extraction / explanation-from-reason-codes / tool-calling analyst / learned evidence producer / autonomous agent.
- **Strongest support:** integrity review §9; REQ-LLM guardrails. **Strongest counter:** current LLM-for-finance value evidence is thin (FinBERT dated) → conservative.
- **Grades:** SQ C (thin current evidence). **Recommended:** **AI as an analysis/interaction layer, NOT a source of numerical truth or trading authority.** MVP default: **deterministic templated explanations from reason codes + (optional) advisory NL query / RAG over approved artifacts**; structured extraction & learned evidence = challenger; autonomous decision authority = **REJECTED**. Hard boundary: AI must not modify risk limits, portfolio state, promote models, alter policy, submit orders, or rewrite audit history; every AI response preserves as_of/source-IDs/provider/model-version/prompt-version/tool-calls/claims/uncertainty/validation-status.
- **Reversibility:** high. **LRDP:** before any LLM enters a runtime path.
- **Freeze class:** STABLE_INTERFACE (boundaries) + REVERSIBLE_COMPONENT_CHOICE (provider). **Status:** PROPOSED_RECOMMENDATION + EMPIRICAL_TBD (value). **cross_doc_status:** EXTENSION_ONLY (tightens REQ-LLM).

---

## Summary
18 decisions. **Status counts:** OWNER_APPROVAL_REQUIRED 11 · PROPOSED_RECOMMENDATION 4 · EMPIRICAL_TBD (primary or joint) 6 (ADR-002/009/011/014/016/018) · DEFERRED 0 · REJECTED 0 (autonomous-AI-authority rejected within ADR-018) · **OWNER_APPROVED 0**. **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION 5 (ADR-001/003/004/009/015) · EXTENSION_ONLY 8 · TENSION_REQUIRES_CLARIFICATION 2 · EMPIRICAL_TBD (as joint) 5 · CONSISTENT 1. Highest-leverage first: ADR-001, ADR-003/004, ADR-002, ADR-009, ADR-007, ADR-015 (see OWNER_DECISION_PACKETS.md ordering).
