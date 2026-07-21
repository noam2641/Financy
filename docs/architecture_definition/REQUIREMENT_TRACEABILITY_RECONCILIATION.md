# Requirement Traceability Reconciliation — Initial (Deliverable H1)

**Program:** AI Trading Decision Platform — Phase 1 (Evidence Spine). Seeded by agent A8 (requirements-and-interface-auditor).
**Repo audited:** `7c4c659` (docs-only). **Authoritative REQ-ID source:** `AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md` v4.6.
**Status:** Initial reconciliation. This is **not** the final H (Phase 5) and does not itself correct canonical or companion docs — it classifies references so Phase-2 owner decisions and Phase-5 corrections can act. Canonical v4.6's own REQ-set was found internally clean (contiguous per prefix, no duplicate definitions).

---

## 1. Authoritative REQ-ID Inventory (extracted from v4.6, by definition site)

Ranges are contiguous unless noted. Prefixes marked **⚠** are the ones companion docs reference out of range.

| Prefix | Range present | Count | Prefix | Range present | Count |
| --- | --- | --- | --- | --- | --- |
| REQ-GEN | 001–005 | 5 | REQ-VAL ⚠ | 001–010 | 10 |
| REQ-PROD | 001–025 | 25 | REQ-SRC | 001–007 | 7 |
| REQ-RELCLASS | 001–008 | 8 | REQ-LLM | 001–005 | 5 |
| REQ-REL0 | 001–003 | 3 | REQ-DQ ⚠ | 001–005 | 5 |
| REQ-REL1A | 001–002 | 2 | REQ-EXEC | 001–017 | 17 |
| REQ-REL1B | 001 | 1 | REQ-SIM | 001–005 | 5 |
| REQ-REL2A | 001 | 1 | REQ-LEARN | 001–034 | 34 |
| REQ-REL2B | 001 | 1 | REQ-MON | 001–003 | 3 |
| REQ-REL3 | 001 | 1 | REQ-AUD | 001 | 1 |
| REQ-REL4 | 001–003 | 3 | REQ-GOV | 001–012 (009–012 = Control Plane) | 12 |
| REQ-DOM | 001–036 | 36 | REQ-KILL | 001 | 1 |
| REQ-SCH | 001–039 | 39 | REQ-INC | 001 | 1 |
| REQ-TIME | 001–010 | 10 | REQ-API | 001–006 | 6 |
| REQ-DATA | 001–007 | 7 | REQ-NFR | 001–006 | 6 |
| REQ-PRICE | 001–006 | 6 | REQ-SEC | 001–003 | 3 |
| REQ-LAB ⚠ | 001–013 | 13 | REQ-TEST | 001–005 | 5 |
| REQ-FEAT | 001–005 | 5 | REQ-GATE | 001–003 | 3 |
| REQ-MOD ⚠ | 001–019 | 19 | REQ-DOC | 001–013 | 13 |
| REQ-COST | 001–003 | 3 | REQ-CONV (bare) | 001–005 | 5 |
| REQ-FILL | 001–005 | 5 | REQ-CONV-ARCH | 001–017 | 17 |
| REQ-DEC ⚠ | 001–006 | 6 | REQ-CONV-OVN | 001–014 | 14 |
| REQ-HOR | 001–003 | 3 | REQ-CONV-DATA | 001–008 | 8 |
| REQ-STOP | 001–003 | 3 | REQ-CONV-TA | 001–009 | 9 |
| REQ-POS | 001–002 | 2 | REQ-CONV-MOD | 001–008 | 8 |
| REQ-RISK ⚠ | 001–004 | 4 | REQ-CONV-GRAPH | 001–007 | 7 |
| REQ-PORT ⚠ | 001–004 | 4 | REQ-CONV-CONT | 001–012 | 12 |
| REQ-CONV-LINK | 001–008 | 8 | REQ-CONV-DS | 001–008 | 8 |
| REQ-CONV-TOOL | 001–005 | 5 | REQ-CONV-TEST | 001–005 | 5 |
| REQ-CONV-TRACE | 001–003 | 3 | | | |

**Prefixes that do NOT exist anywhere in canonical v4.6:** `REQ-LBL`, `REQ-DATAQ`, `REQ-CP`. No duplicate definitions found; authority order and criticality vocabulary are internally consistent.

---

## 2. Reference Classification (each reference classified individually — no whole-range invalidation)

Appears-in: **BL** backlog · **TL** testing-logic · **CM** coverage-matrix · **GOM** git-operating-model.

| Reference (as written) | Appears in | Classification | Canonical target | Note |
| --- | --- | --- | --- | --- |
| `REQ-LBL-001..013` | BL (R0-BL-004), TL, CM | **LIKELY_TYPO** | `REQ-LAB-001..013` | Wrong prefix, correct range; 13 IDs × 3 docs |
| `REQ-LAB-001..013` | GOM (§8.3) | **VALID** | — | GOM is the only doc using the correct prefix → cross-doc inconsistency |
| `REQ-VAL-009..014` | BL (R0-BL-006), CM | **PARTIAL** | 009–010 VALID; 011–014 INVALID | REQ-VAL max = 010 |
| `REQ-VAL-004..010`, `REQ-VAL-001..008` | GOM, BL/TL/CM | **VALID** | — | |
| `REQ-MOD-011..025` | BL (R1A-BL-004) | **PARTIAL** | 011–019 VALID; 020–025 INVALID | REQ-MOD max = 019 |
| `REQ-MOD-001..010` | BL/TL/CM/GOM | **VALID** | — | |
| `REQ-DEC-001..012` | BL (R1A-BL-004) | **PARTIAL** | 001–006 VALID; 007–012 INVALID | REQ-DEC max = 006 |
| `REQ-RISK-001..009` | BL (R1A-BL-005) | **PARTIAL** | 001–004 VALID; 005–009 INVALID | REQ-RISK max = 004 |
| `REQ-PORT-001..007` | BL (R1A-BL-005) | **PARTIAL** | 001–004 VALID; 005–007 INVALID | REQ-PORT max = 004 |
| `REQ-DATAQ-009..013` | BL (R1A-BL-006) | **INVALID (phantom prefix)** | `REQ-DQ-*` (+ Control Plane) | Prefix absent; even as REQ-DQ, DQ max = 005 → also out of range |
| `REQ-CP-001..012` | BL (R1A-BL-006) | **INVALID (phantom prefix)** | `REQ-GOV-009..012` (4 IDs) + REQ-DOC-010 | No REQ-CP prefix; Control Plane is REQ-GOV-009..012 |
| `REQ-DOC-007` | BL (R0-BL-007) | **VALID** | — | Suspect cleared (Test & Traceability package) |
| `REQ-GATE-003` | CM | **VALID** | — | Suspect cleared (readiness-TBD blocker) |
| `REQ-PROD-020..025` | BL (R1A-BL-001) | **VALID** | — | |
| `REQ-CONV-ARCH-016` | BL (R1A-BL-001) | **VALID** | — | Seven-component kernel |
| `REQ-SCH-001..031`, `REQ-SCH-032/037/038` | BL/CM/TL/GOM | **VALID** | — | (SCH extends to 039) |
| `REQ-DATA-001..004`, `REQ-TIME-001..006` | BL/TL | **VALID** | — | |
| All `REQ-CONV-*` cited in CM/BL/TL/GOM | — | **VALID** | — | Every matrix row-ID resolves |

**Prior-audit note:** the earlier Part-I `REQ-PROD-004/066` citation is corrected to `REQ-PROD-004/006` — `066` was a **LIKELY_TYPO** for `006` (REQ-PROD max = 025). This is the classification A8's method prescribes; recorded here for traceability.

---

## 3. Code-Reference Classification (repository contains ZERO code)

| Cited artifact (coverage matrix) | Classification | Reasoning |
| --- | --- | --- |
| `Technical Analysis.py:6990/8006/5080/3876/4306/1236/1327/1526/1689/4112` | **EXTERNAL_PROTOTYPE_REFERENCE / HISTORICAL_REFERENCE_UNVERIFIED** | File absent from repo; line numbers unverifiable |
| `stock_ai_4_files/1_data_update.py`, `2_train_models.py`, `3_daily_scan.py` | EXTERNAL_PROTOTYPE_REFERENCE | Directory not in repo |
| `news_analysis.py` (146/852/886/954/1069/1172/1593) | EXTERNAL_PROTOTYPE_REFERENCE | Absent |
| `lstmfinancy.py:45/61` | EXTERNAL_PROTOTYPE_REFERENCE | Absent; RESEARCH_ONLY anyway |
| `model.py:89/138`, `coor.py:22`, `untitled1.py`, `untitled2.py` | EXTERNAL_PROTOTYPE_REFERENCE | Absent |
| `data_sources/fred_loader.py` | EXTERNAL_PROTOTYPE_REFERENCE / PLANNED_LOGICAL_COMPONENT | Absent |
| `outputs/technical_graph_system_v4/**` | HISTORICAL_REFERENCE_UNVERIFIED | Generated artifacts, not in repo |
| `data/pipeline_checkpoints/*/ml_df.csv`, `latest_row.csv` | HISTORICAL_REFERENCE_UNVERIFIED | Not in repo |
| `docs/CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md` (CM REQ-SCH-032) | **REPOSITORY_LOCAL_VERIFIED (path mismatch)** | File exists at repo **root**, not `docs/` |
| `docs/AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md` (CM REQ-GATE-003) | REPOSITORY_LOCAL_VERIFIED (path mismatch) | Exists at root, not `docs/` |

**Net:** 0 of ~25 code citations are repository-local-verified as code. Coverage-matrix `PARTIALLY_IMPLEMENTED` / `IMPLEMENTED_UNTESTED` statuses on those rows are unsupported by repo contents.

---

## 4. Contract-Package (REQ-DOC) Status

REQ-DOC-003…011 are all **defined** (§31.1–31.9) as normative MUST-include manifests; **none is fulfilled by a delivered artifact.** `CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md` supplies a partial `canonical_entity_mapping` + `operator_tool_contract` fragment for six content/feature entities — it is the **REQ-DOC-012 named artifact**, and does **not** by itself satisfy the REQ-DOC-011 Conversation-Derived Capability Package (which requires ~16 sub-contracts). Per REQ-DOC-013, no "implementation-ready" claim is permissible until the packages are complete. `RELEASE_0_TESTING_LOGIC_AND_ARCHITECTURE.md` and `CLAUDE_AGENTIC_IMPLEMENTATION_AND_GIT_OPERATING_MODEL.md` exist but are not anchored to any REQ-DOC requirement (un-required companions; not a contradiction).

---

## 5. Findings (H1)

| ID | Finding | Severity | Blocks |
| --- | --- | --- | --- |
| **H1-F1** | Phantom prefixes `REQ-DATAQ-*` / `REQ-CP-*` in R1A-BL-006 have no canonical anchor → correct to `REQ-DQ-*` + `REQ-GOV-009..012` | MAJOR | release_1A (traceability) |
| **H1-F2** | Over-range IDs in R1A backlog: `REQ-MOD-020..025`, `REQ-DEC-007..012`, `REQ-RISK-005..009`, `REQ-PORT-005..007` (20 non-resolving) → truncate to defined maxima | MAJOR | release_1A |
| **H1-F3** | `REQ-LBL-*` typo in BL/TL/CM (GOM correct) → global `REQ-LBL→REQ-LAB` | MAJOR | release_0_definition, release_0_acceptance |
| **H1-F4** | `REQ-VAL-011..014` over-range in R0-BL-006 + CM → correct to ≤010 | MAJOR | release_0_acceptance |
| **H1-F5** | Coverage-matrix statuses describe a non-repo codebase → reset all code rows to `DOCUMENTED`/`DESIGNED` or label EXTERNAL_PROTOTYPE_REFERENCE | MAJOR | release_0_acceptance |
| **H1-F6** | REQ-DOC-003..011 packages defined, none delivered; addendum ≠ full REQ-DOC-011 → record as unfulfilled obligations gating readiness (REQ-DOC-013) | MAJOR | architecture_freeze, final_holdout, shadow, paper, live |
| **H1-F7** | Two CM rows cite `docs/…` for files at repo root → path fix | MINOR | none (hygiene) |
| **H1-F8** | Testing-logic and git-operating-model unanchored to REQ-DOC-012 | OBSERVATION | none |

**Recommended action (Phase 5 corrections; not applied now):** add the CI reference-existence validator the operating model already mandates (GOM §8.1/§14.4) — it would currently reject the backlog and matrix. Do **not** modify canonical v4.6; corrections target companion docs only, under owner approval.

---

## 6. Traceability Skeleton (to be completed in Phases 2–5)

Research source → Finding → Architecture decision (Phase 2 F) → Requirement ID (this doc) → Entity contract (Phase 4) → File contract (Phase 4) → Function contract (Phase 4) → Model contract (Phase 4) → Future verification obligation (Phase 5 H/I). This initial H1 populates the **Requirement-ID** column and its validity classification; downstream columns are filled as later phases produce contracts.
