# Twelve-Document Consistency Review (Phase 1.5)

**Inventory (all read in full):** 7 root @ `7c4c659` — (1) canonical spec v4.6, (2) schema addendum, (3) git operating model, (4) README ("# Financy"), (5) release backlog, (6) testing-logic, (7) coverage matrix; 5 architecture-definition @ `5d19997`/`022fb88` — (8) research protocol, (9) evidence report A, (10) model matrix D, (11) data/PIT E, (12) traceability H1. Authority order & conflict register: `DOCUMENT_AUTHORITY_AND_CONFLICT_MATRIX.md`. This review is **reconciliation and decision-preparation, not silent normalization**; canonical v4.6 unchanged.

**Method note:** a difference is a **conflict** only where documents assert incompatible contracts — *not* merely where one is more detailed (extension) or uses different words for one concept (terminology).

---

## 1. Agreement / Extension / Terminology map (representative)
- **Agree:** research/runtime/learning separation, small kernel, purged walk-forward + embargo, PIT time-field taxonomy, NO_ACTION first-class, deferral of deep/graph/LLM to R4 — canonical, backlog, testing-logic, and Phase-1 (A/D/E) **all align**.
- **Extend (not conflict):** D extends canonical's model inventory by *naming* the MVP baseline (GBT/elastic-net/LambdaMART/conformal); E extends the PIT contracts with provider-level detail; H1 extends the coverage matrix with per-ID classification. These are extensions, not contradictions.
- **Terminology (same concept, different words):** "Truth Kernel" (backlog/testing) ≈ "Rigorous Edge Probe / ARCH-A" (A/A7); "naive comparator" (backlog) vs "investable benchmark" (A1) — **related but NOT identical** (see Q4/Q7 — this one is a genuine gap, not mere wording).

## 2. The Twelve Mandatory Cross-Document Questions

**Q1 — Product & edge thesis.** Canonical *claims* a "Decision Operating System with a Counterfactual Learning Factory" whose advantage comes from world-state understanding/abstention/learning (REQ-PROD-003/004) — a **process aspiration**, not a stated inefficiency; **no falsifiable edge thesis or effect-size band exists** anywhere. Phase-1 (A1/A7) establishes edge existence as the load-bearing *empirical hypothesis*. Backlog orders the baseline **last** (R0-BL-006/Stage-6). **Verdict:** the Edge-Probe recommendation is a **clarification + re-sequencing (a build-order correction), not a redesign** — it uses the spec's own R0 machinery. Falsifier: baseline fails to beat an investable benchmark net-of-cost with DSR-adjusted significance → `BLOCKED_NO_EDGE`. **Escalate → packet 1, 2.**

**Q2 — Release-0 definition (one minimal scope).** Reconciling canonical R0 (REQ-REL0-001), backlog R0-BL-001..007, testing-logic, and Phase-1:
- **Required to *begin* R0 implementation:** canonical OHLCV adapter (raw-basis); as-of corporate-action table; survivorship-safe PIT universe as-of start; 5/8/14 matured labels with declared `price_basis`; grouped-by-date purged walk-forward + embargo; trial registry; one named baseline (GBT + elastic-net comparator); append-only run ledger + `feature_snapshot`.
- **Required to *accept* R0:** factor-attributed, net-of-cost edge vs an **investable** benchmark; effective-sample-adjusted IC-IR; DSR (given the trial registry); leakage tests pass; reproducibility two-tier.
- **Required before *final holdout*:** frozen thresholds; PBO (if estimable); locked-holdout governance.
- **NOT required until R1A+:** decision kernel entities, calibration/ECE gate, portfolio sizing, runtime manifest, capability health.
**Guard (per mandate):** DSR/PBO/CPCV, factor attribution, provider licensing, paper-cost calibration, and later governance controls are **NOT universal Release-0 *starting* blockers** — see `PHASE_1_EVIDENCE_INTEGRITY_REVIEW.md` §6 for applicability. **Escalate → packet 1, 13, 15.**

**Q3 — Release-1A scope.** Canonical 7-component kernel (REQ-PROD-020) vs backlog R1A-BL-002 (~34 entities). Entities the R1A kernel actually *writes*: `decision_cycle, recommendation, forecast_snapshot, forecast_distribution, decision_assessment, risk_assessment, execution_plan(intent), outcome_record, decision_ledger_event, audit_event` (~10). No R1A producer: `counterfactual_run/portfolio, module_value_profile, evidence_dependency_graph, market_state_hypothesis, content_*, opportunity(analytics)`. Should remain DESIGNED: world-model hypotheses, KG, opportunity-memory analytics. Capability-gated: news/fundamentals/graph (2A). Remove from R1A blocker: evidence-DAG (one expert), counterfactual factory, LLM. **Escalate → packet 15 (also CFL-11/12).**

**Q4 — Target basis (one flow).** No document may leave basis/units implicit. Canonical target-basis flow, reconciled:
```
research label (ln(close_exit/open_entry), price_basis DECLARED, sector/market/absolute)
 → model output (expected return in the SAME declared basis; probabilities per horizon)
 → ranking (alpha_score/rank_score on sector-excess OR market-excess — a RELATIVE ordering signal)
 → cost subtraction (economic_edge_bps = ABSOLUTE-EXECUTABLE expected_return_bps − round-trip cost_bps)   ⟵ basis PINNED
 → decision utility (risk_adjusted_utility_bps, bps, FROZEN_PRIOR λ)
 → portfolio outcome (policy_return_if_filled → realized_trade_return, ABSOLUTE)
 → promotion metric (net-of-cost benchmark-relative, beta-adjusted, DSR-deflated)
```
**Rule enforced:** ranking may be relative; **cost subtraction and utility must be absolute-executable**; sector-excess never enters `economic_edge_bps`. **Escalate → packet 3, 4, 5 (also CFL-06).**

**Q5 — Sector classification.** Five distinct options (paid PIT GICS / free PIT SIC-with-new-target / market-excess primary / absolute-return primary / sector-excess-secondary-diagnostic) fully compared in `PHASE_1_EVIDENCE_INTEGRITY_REVIEW.md` §4. **SIC ≠ transparent GICS replacement.** **Escalate → packet 9 (also CFL-05).**

**Q6 — Price basis & corporate actions.** Five-series use-by-use safety matrix in integrity review §5. Canonical REQ-PRICE-001..006 already distinguishes raw/split/total-return (credit); the gap is (a) REQ-LAB-001 declares **no `price_basis`**, (b) no `ex_date ≤ cutoff` as-of rule, (c) current-vintage back-adjustment implicitly permitted. Safe: raw for execution; as-of-adjusted for analytics; split-only simple returns. Unsafe: current-vintage back-adjusted for levels/filters/universe/labels; total-return for price-return labels. **Escalate → packet 6.**

**Q7 — Validation.** Per-method canonical-status vs Phase-1 recommendation vs applicability in integrity review §6. Summary: purged-WF (canonical ✓, keep primary); embargo (canonical ✓, bind ≥ max interval); **trial registry (NEW, mandatory)**; **DSR (NEW, when multiple trials)**; PBO (canonical ✓, secondary, not-estimable ≠ pass/fail); **CPCV (NEW, robustness only)**; block bootstrap (canonical ✓); **factor attribution + investable benchmark (NEW, edge gate)**; locked holdout (canonical ✓); paper revalidation (R3). Spec-change required for: trial registry, DSR, factor attribution, investable benchmark, embargo lower-bound. **Escalate → packet 13.**

**Q8 — Model strategy.** Nine-layer separation (integrity review §7). "Deterministic decision policy" does **NOT** imply a deterministic forecast model — the forecast model is a **learned GBT** stack. Already canonical: cross-sectional model, calibration/uncertainty wrapper, deep/graph as R4 challengers. Optional challenger: LambdaMART, Bayesian decision model, HMM. Deferred: LSTM/TCN/Transformer/TFT/GNN/FinBERT/multimodal/MoE. Unsupported/contradicted for MVP: learned super-model as decision-layer dependency; MV optimizer. Retained only behind module-value proof: all optional capabilities. **Escalate → packet 10, 11.**

**Q9 — AI/LLM role.** Canonical REQ-LLM-001..005 + conversation-derived (§32.6) already impose structured-output-only, no-tool-execution-from-article-text, deterministic metadata (credit). Phase-1 adds the **advisory-not-authoritative** framing + hard boundaries + required response provenance fields (integrity review §9). Default recommendation: **AI as analysis/interaction layer, NOT a source of numerical truth or trading authority.** **Escalate → packet 18.**

**Q10 — Traceability.** Canonical REQ-set clean; companion-doc references broken per H1 (CFL-01/02/03). Every invalid mapping carries original ID, source doc, authoritative candidate, semantic justification, confidence, mechanical/substantive class, owner-approval flag (H1 §2 + integrity review §8). Ambiguous mappings **not auto-applied**. **Escalate → packet (traceability corrections, Phase-5) + owner approval for substantive remaps.**

**Q11 — Code & function references.** All ~25 code references across the twelve docs classified individually in H1 §3 (0 REPOSITORY_LOCAL_VERIFIED as code; all EXTERNAL_PROTOTYPE_REFERENCE / HISTORICAL_REFERENCE_UNVERIFIED; two .md path-mismatches). Absent prototype code is **not** implementation evidence; references **preserved** as inputs to the Phase-4 function/file contract appendix. **Escalate → coverage-matrix reset (CFL-04).**

**Q12 — Working method.** Git operating model (§) vs Phase-0 protocol vs actual Phase-1 execution. **Rules followed:** branch-per-phase, documentation-only, separate commits, test-first *intent*, requirement extraction. **Rules not yet evidenced:** CI ref-validator, coverage-matrix validator, hooks, independent human review. **Rules that proved impractical / need change:** (a) "reproduce artifact hashes" bit-exact (CFL-07); (b) same-model multi-agent "independence" is context-isolation only — **not** epistemic independence (integrity review §1); (c) **raw-agent-report preservation was not a defined control** — added in Phase 1.5 (`evidence/agents/`); (d) **no Round-2 multi-party transcript** — synthesis-only. **Required before Phase 3 / implementation:** freeze the twelve-document reconciliation into owner decisions; add the CI ref-validator; add a genuinely-independent (human or different-provider) review for load-bearing financial claims; define provenance controls in the operating model. **Escalate → packet 17 + Phase-5 operating-model patch proposal.**

## 3. Provenance & Review Limitations
- Documents read from the repository: all **12** (branch `claude/trading-platform-audit-iawx0v`; root `7c4c659`; arch-def `022fb88`).
- Prior six-agent audit (Part I): exists **only in the internal session plan file**, **not** in the repository — treated as evidence/hypotheses, not authority.
- Eight raw Round-1 agent reports: **PRESERVED** (final reports, `evidence/agents/`); complete transcripts = task-output JSONL (not in repo).
- Round-2 transcript: **NOT preserved as a distinct artifact** — synthesis only.
- Reproducibility from repository artifacts alone: **partial** (traces to preserved agent reports + source register + claim traceability; lowest-level web fetches external).

## 4. Consistency Gate Result (Phase 1.5)
No document is described as both present and missing; the addendum is present-and-reviewed (≠ REQ-DOC-011); no agent is both RETURNED and pending; no unresolved REQ-ID is presented as valid; no Round-1 agent used another's findings; no fabricated citation; independence terminology corrected; CX-11 reclassified. **Gate: PASS.** Phase 2 may proceed on the full twelve-document basis.
