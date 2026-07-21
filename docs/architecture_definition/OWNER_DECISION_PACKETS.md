# Owner Decision Packets (Phase 2)

**For the owner.** Each packet is a decision **you** must make. **Nothing here is approved** — all are `PROPOSED_RECOMMENDATION` / `OWNER_APPROVAL_REQUIRED` / `EMPIRICAL_TBD`. Full technical fields: `ARCHITECTURE_DECISION_REGISTER.md` (ADR-###). Experiments/defaults: `OPEN_DECISIONS_ASSUMPTIONS_AND_EXPERIMENTS.md`. Documentation-only; canonical v4.6 unmodified. Ordered by leverage. Each packet ends with a Hebrew owner summary (סיכום לבעלים).

`cross_document_consistency_status` ∈ {CONSISTENT, EXTENSION_ONLY, TENSION_REQUIRES_CLARIFICATION, CONFLICT_REQUIRES_OWNER_DECISION, EMPIRICAL_TBD, TRACEABILITY_DEFECT, STALE_REFERENCE}.

---

## OWNER RATIFICATION — ROUND 1 (authoritative status per packet)
Recorded per explicit owner decision (full binding notes in `ARCHITECTURE_DECISION_REGISTER.md` → "OWNER RATIFICATION — ROUND 1").
- **PKT-1 OWNER_APPROVED** (+ validation clarification: trial registry & purged WF mandatory; DSR when multiple trials; PBO when enough variants/partitions; CPCV robustness; nothing "estimable" without prerequisites).
- **PKT-2 STRUCTURE OWNER_APPROVED; VALUES EMPIRICAL_TBD** (thesis required; numeric hurdles not frozen).
- **PKT-3 OWNER_APPROVED** (primary=ABSOLUTE_EXECUTABLE_RETURN; secondary ranking=MARKET_EXCESS_RETURN; diagnostic=SECTOR_EXCESS_RETURN; never mixed).
- **PKT-4 OWNER_APPROVED** (`expected_return_bps`=ABSOLUTE_EXECUTABLE_RETURN_BPS).
- **PKT-6 OWNER_APPROVED** (raw immutable OHLCV + versioned CAs + as-of adjustment + explicit price_basis; split-only simple-return exception preserved).
- **PKT-7 PARTIALLY OWNER_APPROVED** (posture approved; licensed vendor NOT an automatic SHADOW blocker; provider-promotion decision rule; production-authorized source before PAPER/LIVE).
- **PKT-8 OWNER_APPROVED** (PIT universe incl. delisted; opaque instrument_id; no ticker joins).
- **PKT-9 OWNER_APPROVED WITH DEFERRAL** (no gating sector taxonomy R0; sector-excess secondary; GICS deferred; SIC not a substitute; SIC usability EMPIRICAL_TBD).
- **PKT-15 OWNER_APPROVED IN PRINCIPLE** (minimal kernel-owned set; do NOT freeze "~10"; Phase-3 producer/consumer/entity matrix; preserve monolith/kernel/feature_snapshot/ledger/cohort-logging; defer evidence-DAG/world-hypothesis/opportunity-analytics/KG/counterfactual-factory/autonomous-LLM).
- **Non-blocking, carried with working defaults (not elevated):** PKT-5 (pure fixed-horizon exit) · PKT-10 (GBT+elastic-net) · PKT-11 (deterministic policy, learned forecast) · PKT-12 (λ FROZEN_ECONOMIC_PRIOR MVP) · PKT-13 (methodology owner-approved via PKT-1; thresholds EMPIRICAL_TBD) · PKT-14/16 (EMPIRICAL_TBD) · PKT-17 (INTERNAL_POLICY_CHOICE) · PKT-18 (advisory-only; autonomous authority REJECTED — owner-affirmed; value EMPIRICAL_TBD).
The per-packet bodies below retain their original analysis; this banner is the authoritative post-ratification status.

---

## PKT-1 — Build order & edge-probe (ADR-001)
- **Canonical position:** a full Decision-OS with a Counterfactual Learning Factory as the product identity (REQ-PROD-003); baseline forecast is built last (R0-BL-006/Stage-6).
- **Phase-1 research position:** build a *rigorous Edge Probe* (survivorship-safe PIT universe → labels → purged WF → cost model → one GBT baseline → DSR/PBO vs an investable benchmark) **before** any world-model/graph/opportunity/counterfactual work.
- **Contradiction/gap:** the make-or-break question (does edge exist?) is answered last; risk of spending the runway on infrastructure around an unproven premise.
- **Strongest evidence:** CLM-EDGE/COST (SRC-QUANT-001/002/003/007, A-grade). **Strongest counter:** a *thin* probe that skips PIT rigor gives a false positive — so the probe must be rigorous, not quick.
- **Recommended resolution:** adopt the rigorous Edge Probe; freeze §3.7–3.10/§23 as an un-built appendix until it passes.
- **Impact on documents:** backlog (sequencing), canonical note (thesis framing), A/A7. **Root spec amended later?** Yes (a clarifying note, not a redesign). **Reversible?** High. **LRDP:** before R0 implementation.
- **cross_document_consistency_status:** CONFLICT_REQUIRES_OWNER_DECISION. **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** לפני שבונים את כל הפלטפורמה — לבנות "בדיקת-קצה" קפדנית שתשיב על השאלה היחידה שקובעת: האם יש בכלל יתרון-מסחר אחרי עלויות? כל שאר המערכת מוקפאת עד שהבדיקה עוברת. זו החלטה על **סדר הבנייה**, לא עיצוב מחדש.

## PKT-2 — Falsifiable edge thesis & kill criterion (ADR-002)
- **Canonical:** advantage "should come from" world-state/abstention/learning (REQ-PROD-004) — an aspiration, no effect-size or falsifier.
- **Research:** register a per-`opportunity_type` thesis (claimed inefficiency, expected IC/return band, half-life, capacity) + a `BLOCKED_NO_EDGE` kill rule.
- **Contradiction/gap:** no falsifiable hypothesis exists → leakage undetectable, gates arbitrary.
- **Evidence:** CLM-MULTITEST/EDGE (SRC-QUANT-001/002/006/008). **Counter:** priors are uncertain → use a band.
- **Recommended:** pre-register a conservative net-of-cost hurdle before any holdout. **Docs:** A, backlog, canonical note. **Amend?** Yes (add thesis+falsifier). **Reversible?** High. **LRDP:** before final-holdout access.
- **cross_doc_status:** EMPIRICAL_TBD. **Status:** EMPIRICAL_TBD + OWNER_APPROVAL_REQUIRED (hurdle value).
- **סיכום לבעלים:** לנסח מראש השערת-יתרון שניתן להפריך (כמה, לכמה זמן, באיזה קיבולת) וקריטריון-כישלון ברור. בלי זה אי-אפשר לדעת אם "הצלחה" בבדיקה היא אמת או דליפת-מידע.

## PKT-3 — Target basis & ranking basis (ADR-003)
- **Canonical:** default primary ranking target = `sector_excess_return_h` (REQ-LAB-006).
- **Research:** primary = **absolute-executable or market-excess**; keep sector-excess only as a **secondary ranking/diagnostic** input.
- **Contradiction/gap:** sector-excess is (a) not factor-neutral, (b) un-sourceable PIT free, (c) not monetizable long-only.
- **Evidence:** CLM-STR/GICS (SRC-QUANT-004/006 + SRC-DATA-003). **Counter:** sector-neutral ranking genuinely reduces sector beta — hence keep it as a ranking input, not the traded objective.
- **Recommended:** market-excess (or absolute) primary; sector-excess secondary. **Docs:** canonical (REQ-LAB-006 patch), backlog, D/E. **Amend?** Yes. **Reversible?** Medium. **LRDP:** before R0 label build.
- **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION. **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** לדרג מניות יחסית-לסקטור זה בסדר כ**קלט-דירוג**, אבל היעד שנסחר בו והעלויות חייבים להיות בתשואה **מוחלטת** (ספר long-only לא יכול "לממש" תשואה יחסית-לסקטור בלי שורט). בנוסף, נתוני-סקטור PIT חינמיים של GICS אינם קיימים.

## PKT-4 — `expected_return_bps` basis (ADR-004)
- **Canonical:** `economic_edge_bps = expected_return_bps − cost` (REQ-DEC-001), basis unspecified across three target families.
- **Research:** pin `expected_return_bps` to **ABSOLUTE_RETURN (executable)**; sector-excess never enters the subtraction.
- **Contradiction/gap:** subtracting absolute cost from a relative return is incoherent → corrupts every downstream utility/rank_score.
- **Evidence:** A4-F-A4-01 (spec-internal logic). **Counter:** none material.
- **Recommended:** one normative clause pinning the basis. **Docs:** canonical (REQ-DEC-001 note), D. **Amend?** Yes. **Reversible?** High. **LRDP:** before decision-layer design.
- **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION. **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** להגדיר חד-משמעית שהמספר שממנו מחסירים עלויות הוא תשואה **מוחלטת ברת-ביצוע**. תיקון של משפט אחד שמונע קלקול שקט של כל חישוב התועלת.

## PKT-5 — Research target vs executed-policy return (ADR-005)
- **Canonical:** research label is fixed-horizon `ln(close_exit/open_entry)` (REQ-LAB-001); execution uses stops/targets/time-stops (REQ-SCH-019); separation of research/policy/realized returns exists (REQ-LAB-003/004, credit).
- **Research:** rank/select on an **executable** objective, or prove IC→post-barrier-PnL concordance; simplest MVP = no stops (label = traded return).
- **Contradiction/gap:** optimized on a quantity that is not the traded return.
- **Evidence:** CLM-LABEL (SRC-QUANT-013, SRC-EXEC-002). **Counter:** barrier labels add path-dependence.
- **Recommended:** MVP without stops for the probe; add barriers only as a validated challenger. **Docs:** A/E, backlog. **Amend?** Possibly. **Reversible?** High. **LRDP:** before R1A execution design.
- **cross_doc_status:** TENSION_REQUIRES_CLARIFICATION. **Status:** PROPOSED_RECOMMENDATION.
- **סיכום לבעלים:** המודל מדורג לפי תשואה עד-אופק קבוע, אבל בפועל נסחרים עם סטופ/טייק-פרופיט — אלה לא אותו דבר. ל-MVP: להתחיל בלי סטופים (כך שהתווית = התשואה הנסחרת), ולהוסיף סטופים רק כ-challenger מאומת.

## PKT-6 — Price basis & corporate actions (ADR-006)
- **Canonical:** distinguishes raw/split/total-return (REQ-PRICE-001..006); but REQ-LAB-001 declares **no** `price_basis`.
- **Research:** immutable **raw** vintage + versioned corporate-action table; derive adjusted **as-of** (`ex_date ≤ cutoff`); forbid current-vintage back-adjusted in levels/filters/universe/labels (split-only simple returns exempt).
- **Contradiction/gap:** yfinance default back-adjusts (future-leak into levels/filters/labels); label price-basis undeclared.
- **Evidence:** CLM-YFIN + price-basis matrix (integrity review §5). **Counter:** as-of derivation adds engineering vs trusting the vendor.
- **Recommended:** as above; **not all adjusted data is invalid** (splits cancel in simple returns). **Docs:** canonical (REQ-LAB-001 `price_basis`), E. **Amend?** Yes. **Reversible?** Medium. **LRDP:** before R0 data adapter.
- **cross_doc_status:** EXTENSION_ONLY + TRACEABILITY_DEFECT (REQ-LAB-001 gap). **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** לשמור מחירים **גולמיים** בלתי-משתנים ולגזור התאמות רק לפי מידע שהיה ידוע באותו יום. לא כל מחיר מותאם פסול — פיצול-מניה "מתקזז" בתשואות פשוטות, אבל מזייף רמות-מחיר ומסנני-נזילות.

## PKT-7 — PIT data posture & provider shortlist (ADR-007)
- **Canonical:** yfinance research adapter allowed w/ later licensing review (REQ-CONV-DATA-008); bitemporal fields required (REQ-DATA-001); two replay classes (REQ-TIME-006).
- **Research:** yfinance **prototyping-only**; **INFORMATION_THEORETIC replay only pre-go-live**; free-PIT stack = raw prices + **EDGAR as-filed** + **ALFRED vintages** + independent corporate-actions/delistings; budget a licensed vendor before shadow.
- **Contradiction/gap:** yfinance has no vintages (no SYSTEM_REALISTIC), back-adjusts, drops delisted names; SYSTEM_REALISTIC is impossible pre-go-live for any source.
- **Evidence:** CLM-YFIN/EDGAR/ALFRED/SURV (SRC-DATA-001..008, official). **Counter:** licensed data has cost + lead time.
- **Recommended:** free-PIT stack now; start recording ingestion timestamps forward; licensing lead-time begins now. **Docs:** E, backlog. **Amend?** No (extends). **Reversible?** High (adapters). **LRDP:** before shadow.
- **cross_doc_status:** EXTENSION_ONLY + EMPIRICAL_TBD (licensing cost). **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** yfinance רק לפרוטוטייפ. לגיבוי-אמת היסטורי אמיתי צריך מקורות עם "גרסאות" (ALFRED למאקרו, EDGAR למידע פונדמנטלי/סקטור, מחירים גולמיים). לפני מסחר-נייר צריך ספק מורשה בתקציב.

## PKT-8 — Universe, delistings, ticker history, survivorship (ADR-008)
- **Canonical:** PIT universe + instrument_master + identifier history + terminal events exist (REQ-DOM-015..019, REQ-LAB-013).
- **Research:** construct the universe **as-of backtest-start including later-delisted names**; opaque `instrument_id`; ban ticker joins.
- **Contradiction/gap:** a "static" universe from currently-resolvable tickers is survivorship-biased.
- **Evidence:** CLM-SURV (SRC-QUANT-015, SRC-DATA-008). **Counter:** free PIT constituents are harder to source.
- **Recommended:** fixed enumerated PIT universe with recorded entries/exits. **Docs:** E, backlog. **Amend?** No (extends). **Reversible?** Medium. **LRDP:** before R0 universe build.
- **cross_doc_status:** EXTENSION_ONLY. **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** לבנות את היקום נכון-לתאריך-ההתחלה כולל חברות שנמחקו/מוזגו אחר-כך, ולעולם לא לזהות נייר לפי טיקר (טיקרים ממוחזרים). אחרת הבק-טסט מנופח על-ידי "הישרדות".

## PKT-9 — Sector taxonomy (ADR-009)
- **Canonical:** sector-excess default target needs PIT GICS (REQ-LAB-006/009); R0/R1A exclude sector modules (REQ-REL0-003/REQ-REL1A-002).
- **Research:** five distinct options (paid GICS / free SIC-with-new-target / market-excess primary / absolute primary / sector-excess-secondary). **SIC ≠ GICS.**
- **Contradiction/gap:** the default target depends on data the early releases exclude and that isn't free PIT.
- **Evidence:** CLM-GICS/SIC (SRC-DATA-003/004). **Counter:** market/absolute primary loses sector-neutrality; SIC may be too coarse.
- **Recommended:** market-excess/absolute primary + sector-excess secondary; GICS/SIC only if a sector-relative objective is later justified. **Docs:** canonical (REQ-LAB-006), E. **Amend?** Yes. **Reversible?** Medium. **LRDP:** before R0 label build.
- **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION + EMPIRICAL_TBD (SIC usability). **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** יש חמש אפשרויות נפרדות לטקסונומיית-סקטור. **SIC אינו תחליף שקוף ל-GICS** — הוא מגדיר יעד אחר. מומלץ יעד מוחלט/עודף-שוק כברירת-מחדל, וסקטור רק ככלי-אבחון משני.

## PKT-10 — Baseline forecast models (ADR-010)
- **Canonical:** "shared cross-sectional model" (REQ-MOD-002), baseline family unnamed.
- **Research:** elastic-net + per-date regression (comparator); **GBT primary**; isotonic/Platt calibration; conformal/CQR intervals; LambdaMART challenger; deep/graph/LLM = R4 challengers.
- **Contradiction/gap:** none — an extension naming what canonical left open.
- **Evidence:** CLM-GBT/CALIB/CONF (SRC-MODEL-001/002/003/004/007/008, A). **Counter:** SRC-MODEL-005 (complexity helps — market-timing only; does not transfer).
- **Recommended:** as above. **Docs:** D, backlog. **Amend?** No (extends). **Reversible?** High. **LRDP:** before R0 baseline.
- **cross_doc_status:** EXTENSION_ONLY. **Status:** PROPOSED_RECOMMENDATION.
- **סיכום לבעלים:** מודל-הבסיס ל-MVP: עצי-גרדיאנט (GBT) כמנבא ראשי + כיול הסתברויות + רגרסיה-לינארית כמשווה. מודלים עמוקים/גרפים/LLM נשארים challengers ל-Release 4 בלבד.

## PKT-11 — Deterministic policy vs learned aggregation (ADR-011)
- **Canonical:** deterministic permission score (REQ-MOD-012); learned "adaptive expert weighting" deferred to R4 (REQ-REL4-001).
- **Research:** **deterministic penalized-utility policy for MVP**; learned stacking/MoE = gated challenger only.
- **Contradiction/gap:** none (aligned); research adds the effective-sample rationale.
- **Evidence:** CLM-DETERM (SRC-DEC-001/002, INFERENCE via CLM-EFFN). **Counter:** larger effective sample or a passing challenger could justify learning later (EMPIRICAL).
- **Recommended:** deterministic MVP; keep the challenger path. **Note:** "deterministic policy" ≠ "deterministic forecast" (forecast is a learned GBT). **Docs:** D. **Amend?** No. **Reversible?** High. **LRDP:** before R1A decision-layer build.
- **cross_doc_status:** CONSISTENT (+ EMPIRICAL_TBD for the challenger gate). **Status:** PROPOSED_RECOMMENDATION.
- **סיכום לבעלים:** שכבת-ההחלטה ל-MVP תהיה **דטרמיניסטית** (מדיניות-תועלת עם משקלים קבועים), לא "מודל-על" נלמד — אין מספיק דגימות עצמאיות כדי לאמן אחד. ה**מנבא** עצמו כן נלמד (GBT). מודל-על נלמד יישאר challenger שחייב לנצח את המדיניות במבחן חוץ-מדגם.

## PKT-12 — Policy-weight treatment (ADR-012)
- **Canonical:** λ/mappings versioned (REQ-DEC-002) but no fitting protocol (contrast REQ-STOP-002).
- **Research:** classify every weight (FROZEN_ECONOMIC_PRIOR / OWNER_POLICY_PARAMETER / FIT_ON_TRAINING_ONLY / EMPIRICAL_THRESHOLD / PROMOTION_THRESHOLD); **utility λ = FROZEN_ECONOMIC_PRIOR** for MVP; anything chosen after seeing a backtest is trial-registered.
- **Contradiction/gap:** un-validated hand-fit λ = silent decision-policy overfit.
- **Evidence:** A4-F-A4-02; CLM-MULTITEST. **Counter:** fitted λ could help — but then carries the PBO/DSR burden.
- **Recommended:** frozen priors for MVP. **Docs:** canonical (REQ-DEC-002 note), D. **Amend?** Yes. **Reversible?** High. **LRDP:** before any backtest consuming λ.
- **cross_doc_status:** EXTENSION_ONLY. **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** המשקלים בפונקציית-התועלת חייבים להיקבע **מראש מתוך היגיון כלכלי** ולא "להיתפר" על הבק-טסט; כל ערך שנבחר אחרי שראית תוצאות נחשב "ניסוי" ונכנס לספירת ההתאמה-יתר.

## PKT-13 — Validation-method applicability (ADR-013)
- **Canonical:** purged WF + embargo + PBO + block bootstrap + capacity/half-life (REQ-VAL-001..010) — strong.
- **Research:** add a **trial registry (mandatory)**, **DSR (when multiple trials)**, **factor attribution + investable benchmark (edge gate)**, **CPCV (robustness)**; **DSR/PBO/CPCV are applicability-conditioned, not universal starting blockers**.
- **Contradiction/gap:** DSR/factor-attribution/investable-benchmark missing; single-path WF under-powered.
- **Evidence:** CLM-CPCV/DSR/PBO/BENCH (SRC-QUANT-008/009/012/014). **Counter:** over-gating early stalls the probe.
- **Recommended:** the default hierarchy (integrity review §6). **Docs:** canonical (REQ-VAL), E. **Amend?** Yes. **Reversible?** Medium. **LRDP:** before R0 acceptance criteria frozen.
- **cross_doc_status:** EXTENSION_ONLY. **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** להוסיף מרשם-ניסויים, Deflated Sharpe, ייחוס-פקטורים ובנצ'מרק בר-השקעה — אבל **לא** להפוך את DSR/PBO/CPCV לחסמי-פתיחה אוניברסליים; הציר הראשי נשאר walk-forward מטוהר לפי תאריכים.

## PKT-14 — Transaction-cost & capacity framework (ADR-014)
- **Canonical:** cost decomposition + caps exist (REQ-COST, REQ-RISK-003) but entry-centric and TBD.
- **Research:** **round-trip** cost incl. exit/close-auction leg; impact ≈ √(size/ADV); quantify PROXY open-fill; freeze ADV/spread/order caps; size to worst-case gap.
- **Contradiction/gap:** one-sided cost model + undefined gap sizing bias net edge upward.
- **Evidence:** CLM-COST/IMPACT/PROXY/GAP (SRC-EXEC-001..008). **Counter:** exact costs unknown pre-paper → ranges.
- **Recommended:** round-trip model + conservative bands + liquid universe. **Docs:** canonical (REQ-COST), E. **Amend?** Yes. **Reversible?** Medium. **LRDP:** before R0 cost model / R1A sizing.
- **cross_doc_status:** EXTENSION_ONLY + EMPIRICAL_TBD. **Status:** EMPIRICAL_TBD + OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** לחשב עלות **הלוך-ושוב** (כולל יציאה), להוסיף השפעת-שוק לפי גודל/ADV, ולתמחר "פתיחה" בזהירות. לגדל פוזיציה לפי תרחיש-הגאפ הגרוע, לא לפי מרחק-הסטופ. המספרים המדויקים — ניסוי (EMPIRICAL_TBD).

## PKT-15 — Release-0 & Release-1A minimal scope (ADR-015)
- **Canonical:** 7-component kernel (REQ-PROD-020) + "maximalism = release blocker" (REQ-REL4-003); yet R1A-BL-002 makes ~34 entities a blocker.
- **Research:** R1A = **~10 kernel-written entities**; defer evidence-DAG/world-hypotheses/opportunity-analytics/KG/LLM/counterfactual-factory; keep append-only ledger + cohort logging + feature_snapshot.
- **Contradiction/gap:** R1A pulls entities whose producers are deferred (evidence-DAG has one expert).
- **Evidence:** CLM-PROPORTION (SRC-SIMP-001/002); CFL-11/12. **Counter (guard):** do **not** complexify the proportionate parts (monolith, kernel, feature_snapshot, ledger).
- **Recommended:** ~10-entity R1A core; rest DESIGNED. **Docs:** backlog (R1A-BL-002). **Amend?** Yes (backlog). **Reversible?** Medium. **LRDP:** before R1A schema work.
- **cross_doc_status:** CONFLICT_REQUIRES_OWNER_DECISION. **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** לצמצם את חסם Release-1A מ-~34 ישויות ל-~10 שהליבה באמת כותבת. גרף-תלות-הראיות, מודל-עולם-היפותזות, מפעל-הקאונטרפקטואל ו-LLM נדחים — אבל **לא** לפרק את מה שכן פרופורציונלי (מונוליט מודולרי, ליבה קטנה, יומן append-only).

## PKT-16 — Threshold classes & freeze protocol (ADR-016)
- **Canonical:** thresholds TBD; REQ-GATE-003 self-blocks readiness; governance metadata (REQ-GOV-005/006).
- **Research:** classify each threshold; **seed provisional values from external priors before holdout**; two-tier reproducibility; define `environment_hash`; freeze overnight SLA from measured durations.
- **Contradiction/gap:** freeze-before-holdout is circular; bit-exact reproducibility infeasible (CFL-07/10).
- **Evidence:** A7-F06; CLM-REPRO (SRC-OPS-002). **Counter:** priors are imperfect → conservative.
- **Recommended:** external-prior seeds, signed; separate learning vs acceptance thresholds. **Docs:** backlog, canonical (REQ-GATE/OVN notes). **Amend?** Yes. **Reversible?** High (until frozen). **LRDP:** before final-holdout access.
- **cross_doc_status:** EXTENSION_ONLY + EMPIRICAL_TBD. **Status:** OWNER_APPROVAL_REQUIRED + EMPIRICAL_TBD.
- **סיכום לבעלים:** לקבוע ערכי-סף זמניים **מראש** מתוך ספרות/פריורים לפני ה-holdout (אחרת יש מעגליות או "כיול לאחור"). לאמץ שחזור דו-שכבתי (מדויק-לביט לנתונים; בטולרנס למודלים) ולהגדיר `environment_hash`.

## PKT-17 — Governance & human approval (ADR-017)
- **Canonical:** roles incl. independent_validator; solo `independence_exception_policy`; two-person kill-switch reset (REQ-GOV-001/002, REQ-KILL-001).
- **Research (SINGLE_AGENT_SUPPORTED):** solo operation caps at RESEARCH/SHADOW; PAPER/LIVE require a named external reviewer + a second kill-switch resetter.
- **Contradiction/gap:** a solo operator cannot self-provide "effective challenge"; **but SR 11-7/26-2 is best-practice, not legally binding here.**
- **Evidence:** CLM-GOV (SRC-OPS-001, INDUSTRY_BEST_PRACTICE). **Counter:** the cap is a policy choice, not an evidence-derived necessity.
- **Recommended (INTERNAL_POLICY_CHOICE):** cap solo at SHADOW; obtain a **legal-applicability determination** (counsel) before assuming any regulatory regime binds. **Docs:** backlog/canonical governance notes. **Amend?** Possibly. **Reversible?** High. **LRDP:** before any PAPER promotion.
- **cross_doc_status:** TENSION_REQUIRES_CLARIFICATION. **Status:** OWNER_APPROVAL_REQUIRED.
- **סיכום לבעלים:** מפעיל-יחיד לא יכול לאמת את עצמו — מומלץ לתקרה של SHADOW ולדרוש מבקר חיצוני + מאשר-שני ל-kill-switch לפני נייר/חי. חשוב: הנחיות-הבנקאות (SR 11-7/26-2) הן **פרקטיקה מיטבית, לא חובה חוקית** כאן — כדאי חוות-דעת משפטית.

## PKT-18 — AI/LLM advisory & analysis layer (ADR-018)
- **Canonical:** REQ-LLM guardrails (structured-output-only, no tool-execution from article text, deterministic metadata) + conversation-derived FinBERT/content requirements.
- **Research:** **AI is an analysis/interaction layer, NOT a source of numerical truth or trading authority.** MVP default: deterministic templated explanations from reason codes + optional advisory NL query / RAG over approved artifacts; structured extraction & learned evidence = challengers; **autonomous decision authority REJECTED**.
- **Contradiction/gap:** current LLM-for-finance value evidence is thin (FinBERT dated/low-grade).
- **Evidence:** integrity review §9 + REQ-LLM. **Counter:** LLMs may add analyst-productivity value later (EMPIRICAL).
- **Hard boundary:** AI must NOT modify risk limits, portfolio state, promote models, alter policy, submit orders, or rewrite audit history; every AI response preserves as_of/source-IDs/provider/model-version/prompt-version/tool-calls/claims/uncertainty/validation-status.
- **Recommended:** as above. **Docs:** canonical (REQ-LLM tightening), D. **Amend?** Yes (tighten). **Reversible?** High. **LRDP:** before any LLM enters a runtime path.
- **cross_doc_status:** EXTENSION_ONLY + EMPIRICAL_TBD (value). **Status:** PROPOSED_RECOMMENDATION + EMPIRICAL_TBD.
- **סיכום לבעלים:** בינה מלאכותית/LLM = שכבת **ניתוח והסבר בלבד**, לא מקור לאמת-מספרית ולא סמכות-מסחר. ברירת-מחדל: הסברים דטרמיניסטיים מקודי-נימוק + (אופציונלי) שאילתה-מייעצת/RAG על מסמכים מאושרים. **אסור** ל-AI לשנות מגבלות-סיכון, תיק, מדיניות, לשלוח הוראות או לשכתב יומן-ביקורת. סוכן-החלטה אוטונומי — נדחה.

---

## Owner review order (highest leverage first)
PKT-1 → PKT-3 → PKT-4 → PKT-2 → PKT-9 → PKT-6 → PKT-7 → PKT-8 → PKT-15 → PKT-13 → PKT-16 → PKT-5 → PKT-10 → PKT-11 → PKT-12 → PKT-14 → PKT-17 → PKT-18.

**Reminder:** none of these is approved. Phase 3 (the v5 architecture draft) must not begin until PKT-1/3/4/2/9/6/7/8/15 are OWNER_APPROVED or explicitly marked EMPIRICAL_TBD with their provisional defaults.
