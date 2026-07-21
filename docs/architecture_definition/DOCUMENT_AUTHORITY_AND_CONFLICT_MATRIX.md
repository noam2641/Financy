# Document Authority and Conflict Matrix (Phase 1.5)

**Scope:** all twelve repository documentation files. Branch `claude/trading-platform-audit-iawx0v`, root docs at commit `7c4c659`, architecture-definition docs at `5d19997`/`022fb88`. Documentation-only; canonical v4.6 unmodified; root-document changes are recorded as **future patch proposals / owner decisions**, not applied here.

---

## 1. Authority Order (normative for this review)

1. Explicit owner decisions (recorded, versioned) — **none exist yet.**
2. `AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md` (v4.6) — **canonical.**
3. Approved canonical schema/contract addenda — `CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md` (present; the REQ-DOC-012 artifact; ≠ full REQ-DOC-011).
4. Approved ADRs — **none yet** (Phase-2 register is PROPOSED only).
5. Release backlog & testing architecture — `RELEASE_0_1A_IMPLEMENTATION_BACKLOG.md`, `RELEASE_0_TESTING_LOGIC_AND_ARCHITECTURE.md`.
6. Coverage & traceability matrices — `REQUIREMENT_TO_CODE_COVERAGE_MATRIX.md`, H1. **Not authoritative proof of implementation** (its cited code is absent from the repo).
7. Phase-0 research protocol.
8. Phase-1 research & evidence documents (A/D/E) + Phase-1.5 integrity docs — **evidence; may challenge but do not override canonical.**
9. Historical prototype references — external/unverified.
10. `README.md` — descriptive only (content "# Financy"); no document grants it normative authority.

**Governing rule:** a contradiction between Phase-1 research and canonical v4.6 **must become a proposed architecture decision or specification correction** (Phase-2 packet) — it must **not** be silently resolved by rewriting canonical meaning.

---

## 2. Per-Document Register

| # | Document | Authority level | Read in full | Role | Normative? |
| --- | --- | --- | --- | --- | --- |
| 1 | AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md | 2 | Yes | Canonical spec v4.6 | **Yes** |
| 2 | CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md | 3 | Yes | Schema addendum (REQ-DOC-012 artifact) | Yes (schema) |
| 3 | CLAUDE_AGENTIC_IMPLEMENTATION_AND_GIT_OPERATING_MODEL.md | 5 | Yes | Working method / Git operating model | Process-normative |
| 4 | README.md | 10 | Yes ("# Financy") | Descriptive | **No** |
| 5 | RELEASE_0_1A_IMPLEMENTATION_BACKLOG.md | 5 | Yes | Release scope/criticality | Derived-normative |
| 6 | RELEASE_0_TESTING_LOGIC_AND_ARCHITECTURE.md | 5 | Yes | Test-closure logic | Derived-normative |
| 7 | REQUIREMENT_TO_CODE_COVERAGE_MATRIX.md | 6 | Yes | Implementation evidence | **Not authoritative (code absent)** |
| 8 | RESEARCH_PROTOCOL_AND_QUESTION_MAP.md | 7 | Yes | Research control plane | Process |
| 9 | ARCHITECTURE_RESEARCH_AND_EVIDENCE_REPORT.md | 8 | Yes | Evidence report (A) | Evidence |
| 10 | MODEL_AND_METHOD_EVIDENCE_MATRIX.md | 8 | Yes | Model evidence (D) | Evidence |
| 11 | DATA_PIT_AND_VALIDATION_APPENDIX.md | 8 | Yes | Data/PIT/validation (E) | Evidence |
| 12 | REQUIREMENT_TRACEABILITY_RECONCILIATION.md | 6 | Yes | Traceability (H1) | Reconciliation |

---

## 3. Conflict Register (intra-repository)

Fields: ID · documents · sections/REQ IDs · authoritative statement · conflicting statement · type · severity · consequence · category · resolution · owner-approval · docs-to-change · mechanical/substantive.

**CFL-01 — REQ-LBL vs REQ-LAB.** Docs: backlog(R0-BL-004), testing-logic, coverage-matrix vs canonical(§8) & git-model(§8.3). Authoritative: `REQ-LAB-001..013`. Conflicting: `REQ-LBL-001..013`. Type: traceability. Severity: MAJOR. Consequence: CI ref-validator (git-model §14) would reject label blocker. Category: traceability-only. Resolution: global `REQ-LBL→REQ-LAB`. Owner-approval: no. Docs-to-change: backlog, testing-logic, coverage-matrix. **Mechanical.**

**CFL-02 — REQ-MOD/DEC/RISK/PORT/VAL over-ranges.** Docs: backlog(R1A-BL-004/005, R0-BL-006), coverage-matrix vs canonical. Authoritative maxima: MOD-019, DEC-006, RISK-004, PORT-004, VAL-010. Conflicting: MOD-020..025, DEC-007..012, RISK-005..009, PORT-005..007, VAL-011..014 (20+ IDs). Type: traceability. Severity: MAJOR. Consequence: references resolve to nothing. Category: traceability-only. Resolution: truncate to defined maxima **and** confirm the intended requirement each over-range token meant (some may indicate a *missing* canonical requirement → spec-gap, substantive). Owner-approval: partial (if a token implies a needed-but-absent requirement). Docs-to-change: backlog, coverage-matrix. **Mechanical for truncation; substantive if it reveals a spec gap.**

**CFL-03 — Phantom prefixes REQ-DATAQ / REQ-CP.** Docs: backlog(R1A-BL-006). Authoritative: `REQ-DQ-001..005` (data quality) + `REQ-GOV-009..012` (Control Plane) + REQ-DOC-010 package. Conflicting: `REQ-DATAQ-009..013`, `REQ-CP-001..012` (prefixes absent). Type: traceability. Severity: MAJOR (R1A-BL-006 has no canonical anchor). Category: traceability-only, but the remap is **semantic**. Resolution: remap per H1. Owner-approval: **yes** (substantive semantic mapping). Docs-to-change: backlog. **Substantive.**

**CFL-04 — Coverage matrix implemented-statuses vs absent code.** Docs: coverage-matrix vs repository reality (authority rule 6). Authoritative: repo contains zero code. Conflicting: `PARTIALLY_IMPLEMENTED`/`IMPLEMENTED_UNTESTED` rows citing `Technical Analysis.py`, `stock_ai_4_files/*`, etc. Type: implementation-status. Severity: MAJOR. Consequence: false readiness; R0-BL-007 acceptance unsatisfiable-yet-mis-satisfied. Category: traceability + governance. Resolution: reset code cells to `DOCUMENTED`/`DESIGNED` or label `EXTERNAL_PROTOTYPE_REFERENCE`. Owner-approval: no (factual correction). Docs-to-change: coverage-matrix. **Substantive (status).**

**CFL-05 — Sector-excess primary target vs R0/R1A sector-module exclusion vs free-PIT infeasibility.** Docs: canonical(REQ-LAB-006 default `sector_excess`; REQ-LAB-009 PIT sector) vs canonical(REQ-REL0-003, REQ-REL1A-002 exclude sector/graph/fundamentals) + Phase-1(E, SRC-DATA-003 GICS proprietary). Authoritative: **canonical-internal conflict** (two canonical clauses point opposite ways) compounded by a data-availability fact. Type: architectural + release-scope + PIT-data. Severity: **CRITICAL**. Consequence: the default primary objective is either un-runnable PIT-free or silently look-ahead-contaminated. Category: architectural/PIT/release-scope. Resolution: **owner decision** (Phase-2 packet 9: options 1–5). Owner-approval: **yes**. Docs-to-change: canonical (patch proposal), backlog, E. **Substantive.**

**CFL-06 — `economic_edge_bps` return-basis unspecified.** Docs: canonical(REQ-DEC-001) vs canonical(REQ-LAB-005/006 three bases). Authoritative: canonical (but ambiguous). Conflicting: no rule states which basis feeds `expected_return_bps`. Type: architectural. Severity: HIGH. Consequence: subtracting absolute cost from relative return → corrupt utility. Category: architectural/financial. Resolution: pin to absolute-executable (Phase-2 packet 4). Owner-approval: **yes**. Docs-to-change: canonical (patch), D. **Substantive.**

**CFL-07 — Reproducibility bit-exact vs tolerance.** Docs: backlog(R0-BL-002 "reproduce artifact hashes") vs canonical(REQ-GATE-001 "0 **or approved tolerance**", REQ-LEARN replay). Authoritative: canonical (tolerance allowed). Conflicting: backlog implies bit-exact. Type: statistical/architectural. Severity: MAJOR. Consequence: infeasible bit-exact chase on torch/GPU. Category: architectural. Resolution: two-tier hash policy (Phase-2 packet 16; integrity review §6-adjacent). Owner-approval: no (align backlog to canonical). Docs-to-change: backlog. **Substantive-wording.**

**CFL-08 — Addendum treated as REQ-DOC-011.** Docs: coverage-matrix/backlog references vs canonical(REQ-DOC-011 requires ~16 sub-contracts). Authoritative: canonical. Conflicting: addendum framed as the conversation package. Type: traceability. Severity: MODERATE. Resolution: addendum = REQ-DOC-012 artifact; REQ-DOC-011 remains unfulfilled. Owner-approval: no. Docs-to-change: coverage-matrix note. **Mechanical.**

**CFL-09 — REQ-DOC-003..011 packages defined, none delivered.** Docs: canonical(§31, REQ-DOC-013 blocks readiness). Authoritative: canonical. Type: governance/traceability. Severity: MAJOR (blocks readiness claims). Category: governance. Resolution: record as unfulfilled obligations; produce in later phases. Owner-approval: no (factual). Docs-to-change: H1/coverage-matrix. **Substantive (status).**

**CFL-10 — `environment_hash` required but undefined/omitted from resume.** Docs: canonical(REQ-DOM-005, REQ-SCH-007 require it; REQ-CONV-OVN-006 resume set omits it). Type: architectural. Severity: MEDIUM. Resolution: define composition; add to resume + runtime_manifest (Phase-2 packet 16). Owner-approval: yes (schema addition). Docs-to-change: canonical (patch). **Substantive.**

**CFL-11 — R1A blocker scope vs small-kernel / anti-maximalism.** Docs: backlog(R1A-BL-002 makes REQ-SCH-001..031 a RELEASE_BLOCKER) vs canonical(REQ-PROD-020 7-component kernel; REQ-REL1A-002 prove value w/o advanced modules; REQ-REL4-003 maximalism = release blocker). Authoritative: canonical principles. Conflicting: backlog pulls ~34 entities (incl. evidence-DAG/world-hypotheses/counterfactual/content) whose producers are deferred. Type: release-scope. Severity: HIGH. Consequence: months of schema work on empty entities before edge proven. Category: release-scope/architectural. Resolution: reduce R1A blocker to the ~10 kernel-written entities (Phase-2 packet 15). Owner-approval: **yes**. Docs-to-change: backlog. **Substantive.**

**CFL-12 — Evidence-dependency graph as R1A contract vs one-expert R1A.** Docs: canonical(REQ-DOM-032 `independent_information_gain`) vs canonical(REQ-REL1A-002 technical-only). Authoritative: canonical-internal tension. Severity: MEDIUM. Consequence: DAG models zero independent experts. Resolution: defer evidence-DAG to 2A (Phase-2 packet 15). Owner-approval: yes. Docs-to-change: backlog/canonical (patch). **Substantive.**

**CFL-13 — Testing-logic & git-operating-model unanchored to REQ-DOC-012.** Docs: canonical(REQ-DOC-012 lists 3 controlled artifacts) vs presence of two extra companions. Type: traceability. Severity: OBSERVATION. Resolution: note as un-required companions or extend REQ-DOC-012. Owner-approval: optional. **Mechanical.**

**No-conflict notes:** README normative status (rule 10 — descriptive only); overnight-SLA/threshold TBDs are consistent *open blockers* across canonical/backlog (not conflicts); authority order, criticality vocabulary, and status-ladder are internally consistent (A8).

---

## 4. Research-vs-Canonical Tensions (route to Phase-2 packets — NOT silent overrides)

| ID | Research position (Phase-1/1.5) | Canonical position | Route |
| --- | --- | --- | --- |
| RVC-01 | Edge is the load-bearing empirical question; build order inverted; edge-probe first | Product thesis asserts a Decision-OS advantage; baseline is Stage-6/last | Packet 1, 2 |
| RVC-02 | Primary = absolute/market-excess; sector-excess secondary | Default primary = sector-excess (REQ-LAB-006) | Packet 3, 9 (also CFL-05) |
| RVC-03 | Name MVP baseline: GBT+calibration/elastic-net; deterministic decision policy | Spec unnamed baseline; defers learned aggregation to R4 (aligned) | Packet 10, 11 |
| RVC-04 | Add DSR/CPCV/factor-attribution/investable-benchmark (applicability-conditioned) | Purged-WF + PBO present; DSR/CPCV/factor-attr not mandated | Packet 13 |
| RVC-05 | De-scope R1A to ~10 entities | R1A-BL-002 ~34 entities (also CFL-11) | Packet 15 |
| RVC-06 | Raw-basis + as-of CAs + ALFRED + EDGAR + survivorship-safe universe | Price/label/universe contracts don't pin provider posture | Packet 6, 7, 8 |
| RVC-07 | AI/LLM = advisory analysis layer with hard boundaries | REQ-LLM + conversation-derived requirements | Packet 18 |

**Discipline:** every RVC becomes a `PROPOSED_RECOMMENDATION` / `OWNER_APPROVAL_REQUIRED` / `EMPIRICAL_TBD` decision; none is applied to canonical in this pass.
