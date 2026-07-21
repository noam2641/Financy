# A8 — Requirements-&-Interface-Auditor — Round-1 Report (PRESERVED)

> **Provenance.** Final report preserved as delivered (cutoff 2026-07-21); substantive content faithfully retained, prose lightly condensed, nothing altered/added; complete raw = task-output JSONL. **SOURCE_REPORT_PRESERVED.** Context-isolated Claude subagent (same model family/provider). This is a pure reference/consistency audit (no external research grading). Full authoritative outputs are consolidated in `REQUIREMENT_TRACEABILITY_RECONCILIATION.md`.

---

**Method followed:** (1) extracted the authoritative REQ-ID set from canonical v4.6; (2) classified each companion-doc reference individually as VALID/INVALID/AMBIGUOUS/LIKELY_TYPO/DEPRECATED; (3) classified every cited code file; (4) checked duplicates, contracts, package status, authority consistency.

## STEP 1 — Authoritative REQ-ID inventory (per prefix, min–max present)
GEN 001–005; PROD 001–025; RELCLASS 001–008; REL0 001–003; REL1A 001–002; REL1B 001; REL2A 001; REL2B 001; REL3 001; REL4 001–003; DOM 001–036; SCH 001–039; TIME 001–010; DATA 001–007; PRICE 001–006; **LAB 001–013**; FEAT 001–005; **MOD 001–019**; COST 001–003; FILL 001–005; **DEC 001–006**; HOR 001–003; STOP 001–003; POS 001–002; **RISK 001–004**; **PORT 001–004**; **VAL 001–010**; SRC 001–007; LLM 001–005; **DQ 001–005**; EXEC 001–017; SIM 001–005; LEARN 001–034; MON 001–003; AUD 001; GOV 001–012 (009–012 = Control Plane); KILL 001; INC 001; API 001–006; NFR 001–006; SEC 001–003; TEST 001–005; GATE 001–003; DOC 001–013; CONV(bare) 001–005; CONV-ARCH 001–017; CONV-OVN 001–014; CONV-DATA 001–008; CONV-TA 001–009; CONV-MOD 001–008; CONV-GRAPH 001–007; CONV-CONT 001–012; CONV-LINK 001–008; CONV-DS 001–008; CONV-TOOL 001–005; CONV-TEST 001–005; CONV-TRACE 001–003. Contiguous per prefix; no duplicate definitions. **Absent prefixes:** REQ-LBL, REQ-DATAQ, REQ-CP.

## STEP 2 — Reference classification (each individually)
- `REQ-LBL-001..013` (BL,TL,CM) → **LIKELY_TYPO** → REQ-LAB-001..013 (13 IDs × 3 docs); GOM uses REQ-LAB correctly → cross-doc inconsistency.
- `REQ-VAL-009..014` (BL,CM) → **PARTIAL**: 009–010 VALID, 011–014 INVALID.
- `REQ-MOD-011..025` (BL) → **PARTIAL**: 011–019 VALID, 020–025 INVALID.
- `REQ-DEC-001..012` (BL) → **PARTIAL**: 001–006 VALID, 007–012 INVALID.
- `REQ-RISK-001..009` (BL) → **PARTIAL**: 001–004 VALID, 005–009 INVALID.
- `REQ-PORT-001..007` (BL) → **PARTIAL**: 001–004 VALID, 005–007 INVALID.
- `REQ-DATAQ-009..013` (BL) → **INVALID (phantom prefix)** → REQ-DQ-* (+ Control Plane); DQ max=005 so range also out of bounds.
- `REQ-CP-001..012` (BL) → **INVALID/AMBIGUOUS** → REQ-GOV-009..012 (4 IDs) + REQ-DOC-010 package.
- `REQ-DOC-007`, `REQ-GATE-003` → **VALID** (suspects cleared).
- REQ-PROD-020..025, REQ-CONV-ARCH-016, REQ-SCH-001..031/032/037/038, REQ-DATA-001..004, REQ-TIME-001..006, all REQ-CONV-* rows → **VALID**.

## STEP 3 — Code-reference classification (repo has ZERO code)
`Technical Analysis.py:*`, `stock_ai_4_files/*`, `news_analysis.py:*`, `lstmfinancy.py:*`, `model.py`, `coor.py`, `untitled1/2.py`, `data_sources/fred_loader.py` → **EXTERNAL_PROTOTYPE_REFERENCE / HISTORICAL_REFERENCE_UNVERIFIED**; `outputs/**`, `data/pipeline_checkpoints/*` → **HISTORICAL_REFERENCE_UNVERIFIED**; `docs/CANONICAL_SCHEMA_ADDENDUM…` and `docs/AI_TRADING_SYSTEM_…` cited by CM → **REPOSITORY_LOCAL_VERIFIED (path mismatch — files at root, not docs/)**. Net: 0 of ~25 code citations repo-local-verified as code; `PARTIALLY_IMPLEMENTED`/`IMPLEMENTED_UNTESTED` statuses unsupported by repo contents.

## STEP 4 — Duplicates / contracts / packages / authority
No duplicate definitions in canonical (CONV bare vs CONV-ARCH/OVN are distinct namespaces). REQ-DOC-003..011 all defined (§31.1–31.9); none fulfilled by a delivered artifact; REQ-DOC-011 requires ~16 sub-contracts → addendum ≠ REQ-DOC-011. REQ-DOC-012 names three controlled artifacts (backlog, addendum, coverage-matrix); testing-logic and git-operating-model are un-required companions (float outside the DOC-012 set; not a contradiction). All 8 backlog "Readiness Thresholds" + REQ-GATE-001 TBD cells unfrozen; REQ-GATE-003 hard-blocks PAPER/LIVE while any TBD persists (consistent, genuine open blocker). Only genuine cross-doc contradiction: REQ-LAB vs REQ-LBL. Authority order/criticality vocabulary/status-ladder internally consistent — no contradiction found.

## FINDINGS
- **F1** Phantom prefixes REQ-DATAQ-*/REQ-CP-* in R1A-BL-006 (no canonical anchor) → REQ-DQ-* + REQ-GOV-009..012. MAJOR · blocks release_1A (traceability).
- **F2** Over-range MOD-020..025/DEC-007..012/RISK-005..009/PORT-005..007 in R1A backlog (20 non-resolving) → truncate to defined maxima. MAJOR · blocks release_1A.
- **F3** REQ-LBL typo in BL/TL/CM (GOM correct) → global REQ-LBL→REQ-LAB. MAJOR · blocks release_0_definition, release_0_acceptance.
- **F4** REQ-VAL-011..014 over-range in R0-BL-006 + CM → ≤010. MAJOR · blocks release_0_acceptance.
- **F5** REQ-DOC-003..011 packages defined, none delivered; addendum ≠ full REQ-DOC-011 → record as unfulfilled obligations (REQ-DOC-013). MAJOR · blocks architecture_freeze, final_holdout, shadow, paper, live.
- **F6** Coverage-matrix statuses describe a non-repo codebase → reset to DOCUMENTED/DESIGNED or label EXTERNAL_PROTOTYPE_REFERENCE. MAJOR · blocks release_0_acceptance.
- **F7** Two CM rows cite `docs/…` for root files → path fix. MINOR.
- **F8** Testing-logic and git-operating-model unanchored to REQ-DOC-012. OBSERVATION.

## VERDICT
"Spec complete" **CONFIRMED-BUT-NOT-SUFFICIENT**: canonical REQ-set internally clean; "spec complete" ≠ traceable. ~40+ tokens across four companion docs don't resolve (phantom ranges MOD/DEC/RISK/PORT/VAL; phantom prefixes LBL/DATAQ/CP); 100% of code citations point outside the repo. The requirement-reference validator the operating model mandates in Stage 0 (GOM §8.1/§14.4) would reject the current backlog and matrix. **Top-5:** F4 (phantom DATAQ/CP) · F1/F2 (over-ranges) · F3 (REQ-LBL) · F6 (matrix repo-truth) · F5 (DOC packages).
