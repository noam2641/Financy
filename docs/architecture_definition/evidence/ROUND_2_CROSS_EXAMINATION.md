# Round-2 Cross-Examination (Phase 1.5, corrected statuses)

**Provenance & independence caveat (read first).** Round 2 was a **lead-run synthesis** across the eight preserved Round-1 agent reports; there is **no separate multi-party Round-2 transcript** — the cross-examination is the lead's structured comparison, so **`ROUND_2_TRANSCRIPT: SYNTHESIS_ONLY` (SOURCE_REPORT_NOT_PRESERVED for a distinct Round-2 dialogue).** The eight agents are **context-isolated Claude subagents of the same model family/provider**; they are **not epistemically independent validators**, and **agent count does not set evidence grade** — grade derives from source quality/applicability/independent external lines (`SOURCE_EVIDENCE_REGISTER.md`, `CLAIM_TO_SOURCE_TRACEABILITY.md`).

**Status vocabulary:** `MULTI_AGENT_CONSENSUS` (≥2 same-family agents agree) · `MULTI_SOURCE_CORROBORATED` (≥2 independent external sources) · `SINGLE_AGENT_SUPPORTED` · `UNCONTRADICTED` · `DISPUTED` · `UNRESOLVED`. A finding may carry both an agent-status and a source-status.

---

| CX | Finding | Agent status | Source status | Claim IDs | Notes / dissent |
| --- | --- | --- | --- | --- | --- |
| CX-1 | Edge unproven & net-of-cost fragile | MULTI_AGENT_CONSENSUS (A1,A5,A7,A4) | MULTI_SOURCE_CORROBORATED (SRC-QUANT-001/002/003/007) | CLM-EDGE, CLM-COST | **DISPUTED on magnitude**: A7 weights "no edge" highest; A1 allows a narrow survivable regime (liquid, low-turnover, factor-neutral). Consensus: *test it*, don't assert it. |
| CX-2 | Sector-excess primary target defective (un-sourceable PIT free; not factor-neutral; absolute-vs-relative cost incoherence; contradicts R0/R1A exclusion) | MULTI_AGENT_CONSENSUS (A1,A2,A4,A5) | MULTI_SOURCE_CORROBORATED (SRC-DATA-003 official + SRC-QUANT-004/006) | CLM-GICS, CLM-SIC, CLM-STR | Highest cross-corroboration; UNCONTRADICTED. SIC framing corrected (CLM-SIC). |
| CX-3 | Fixed-horizon label ≠ traded (barrier) return | MULTI_AGENT_CONSENSUS (A1,A5) | MULTI_SOURCE (SRC-QUANT-013, SRC-EXEC-002) | CLM-LABEL | UNCONTRADICTED. |
| CX-4 | Add DSR/PBO/CPCV + trial registry + investable benchmark | MULTI_AGENT_CONSENSUS (A1,A4,A7) | MULTI_SOURCE_CORROBORATED (SRC-QUANT-008/009/014) | CLM-DSR, CLM-PBO, CLM-CPCV, CLM-BENCH | **"Universal hard gate" DOWNGRADED to applicability-conditioned** (see integrity review §Validation). |
| CX-5 | Deterministic penalized-utility MVP; no learned super-model | MULTI_AGENT_CONSENSUS (A3,A4,A7) | MULTI_SOURCE_CORROBORATED (SRC-DEC-001/002, SRC-MODEL-001/002/003/004) | CLM-DETERM, CLM-GBT | CLM-DETERM is a design-inference / **EMPIRICAL_TBD** (challenger gate decides), not a permanent ban. |
| CX-6 | Retail data not PIT-safe; use raw-basis + ALFRED + EDGAR-as-filed | MULTI_AGENT_CONSENSUS (A2,A7,A1) | MULTI_SOURCE_CORROBORATED (SRC-DATA-001/003/004/006 official) | CLM-YFIN, CLM-GICS, CLM-EDGAR, CLM-ALFRED, CLM-SURV | CLM-YFIN scope-corrected (levels/filters unsafe; simple split returns safe). |
| CX-7 | Coverage matrix cites phantom code | MULTI_AGENT_CONSENSUS (A8,A6,A7,A2) | Repo-fact (A-grade internal, `ls`) | — | UNCONTRADICTED; reset to repo-truth. |
| CX-8 | Companion-doc REQ-ID breakage | MULTI_AGENT (A8,A1) | Internal (canonical extraction) | — | Per-ID classification in H1. |
| CX-9 | R1A over-scope (evidence-DAG/world-hyp/KG/opportunity/CF-factory/LLM; event-sourcing/registries/control-plane) | MULTI_AGENT_CONSENSUS (A7,A6,A4,A3) | MULTI_SOURCE (SRC-SIMP-001/002) | CLM-PROPORTION | **Guard (A3/A6): do NOT complexify the proportionate parts** (modular monolith, kernel, feature_snapshot, ledger). |
| CX-10 | ECE gate necessary-not-sufficient; add discrimination + net-economic co-gates + whole-decision calibration | MULTI_AGENT_CONSENSUS (A1,A3,A4) | MULTI_SOURCE (SRC-MODEL-007) | CLM-CALIB | UNCONTRADICTED. |
| CX-11 | Solo operation capped at RESEARCH/SHADOW | **SINGLE_AGENT_SUPPORTED (A6 only) · UNCONTRADICTED** | SRC-OPS-001 (bank guidance — **ANALOGICAL, not legally binding**) | CLM-GOV | **RECLASSIFIED** from any "consensus" label. Recommended as INTERNAL_POLICY_CHOICE informed by best practice; a genuinely independent second analysis has NOT corroborated it. |
| CX-12 | All TBD thresholds must be frozen pre-holdout; two-tier reproducibility; `environment_hash`; overnight SLA | MULTI_AGENT (all touch) | SRC-OPS-002 + internal | CLM-REPRO | UNCONTRADICTED. |

**Meta-finding (edge unproven + build order inverted + evidence base unverifiable + retail-data-not-PIT):** MULTI_AGENT_CONSENSUS across A1/A5/A7/A2/A6/A8 + MULTI_SOURCE_CORROBORATED; the *terminal-verdict re-scoping* is a synthesis conclusion, correctly framed as a recommendation, **not** an owner-approved decision.

**Genuine disagreements (not forced to consensus):** (i) alpha-survivability magnitude (DISPUTED); (ii) locus of maximalism — A3 (not the model layer) vs A7/A6 (decision-aggregation/ops) — compatible, not contradictory. No agent contradicts another on a verifiable fact.
