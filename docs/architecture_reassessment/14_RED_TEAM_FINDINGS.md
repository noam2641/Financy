# 14 — Red-Team Findings

**Artifact type:** adversarial critique (Phase 4 output) + lead synthesis red-team pass (Phase 5).
**Primary source:** specialist `adversarial-architecture-critic` (10 professional perspectives).
Findings are reproduced faithfully; one **lead reconciliation** is marked. The design changes
these force are carried into `05_RECOMMENDED_TARGET_ARCHITECTURE.md` and `16_UNRESOLVED_OWNER_DECISIONS.md`.

**Lead reconciliation on Finding 1 (scope of "asserted, not specified").** The critic grep'd the
**canonical v4.6** spec and correctly found DSR / trial-registry / effective-sample /
factor-residual / "survivorship" absent there. Cross-checked against the *R0 contract layer*
(read by `repository-architecture-discovery`), those defenses **are** specified — trial registry
(FN-R0-20/ENT-R0-13), DSR/PBO + effective-sample (FN-R0-24/25), factor-residual gate + investable
benchmark (FN-R0-26/27/ENT-R0-18/16), survivorship-safe cohort (FN-R0-08/ENT-R0-07). So the
precise statement is: **contracted in the R0 layer, absent from canonical v4.6, and — decisively —
NOT IMPLEMENTED (only 2 of 16 tasks built).** This *strengthens* the critic's actionable core:
the A/B/C/D superstructure debate rests on an **unbuilt** foundation, and the four kernel
primitives must be **implemented and TESTED** before any architecture bake-off is meaningful.

---

## CRITICAL

**RT-1 — Load-bearing defenses are unbuilt; all proposals inherit the hole.** *(all)* Every
alternative claims to "preserve the R0 truth kernel," but 14/16 tasks (incl. trial registry,
DSR/PBO, effective-sample, factor-residual gate, survivorship cohort) are contracted-but-unbuilt.
→ **Build + TEST four kernel primitives first**, freeze the A/B/C/D comparison until they are
`TESTED_RESEARCH`. *Owner decision: approve the scope-freeze + the four gates.*

**RT-2 — No factor-residual / investable-benchmark purity gate → false edge or honest
BLOCKED_NO_EDGE.** *(all; first-order on A, Edge-Probe+)* A GBT over price/volume digests will
rediscover momentum + short-term-reversal + low-vol + size, "beat a naive 1/N baseline," and
deliver ≈0 net because those factors are already priced (McLean-Pontiff, Chen-Velikov,
Novy-Marx-Velikov, Hou-Xue-Zhang). → **Hard gate:** net-of-cost, effective-sample-deflated alpha
**residual to an investable multi-factor benchmark** (market+MOM+STR+SMB+HML+RMW or ETF proxies),
not merely beating 1/N. *Most probable honest outcome: `BLOCKED_NO_EDGE` — the correct finding.
Owner decision: the exact factor set + minimum surviving deflated t.*

**RT-3 — Effective sample is tiny and never computed; DSR/PBO/CI denominators inflated 10–50×.**
*(all; worst on C, then B)* Overlapping labels + cross-sectional factor dominance + few macro
regimes mean independent N ≪ row count. → **Compute effective N** (block-bootstrap block length;
cluster on regime/factor-date); set DSR/PBO on effective N; freeze a **minimum-effective-N per
horizon and per regime** gate. *Owner decision: the minimum effective N + counting method.*

**RT-4 — The abstention linchpin rests on per-decision calibration no one can do.** *(all;
acute for barrier/touch/time heads)* Calibration is average/in-regime, not per-decision; joint
barrier/touch/time calibration is academically unvalidated (Barber 2023; Gibbs-Candès 2021). →
**Restrict gate-eligible probability to marginal P(return > cost)** with conformal/Venn-Abers
coverage demonstrated **out-of-regime**; make barrier/touch/time/MFE-MAE heads `RESEARCH_ONLY`
and forbid them from the abstention gate and from sizing until coverage is proven. *Owner
decision: enumerate exactly which probabilities may drive ABSTAIN and sizing.*

## HIGH

**RT-5 — Licensed PIT constituents/GICS is the main silent look-ahead; the free path can't satisfy
sector-excess.** *(all)* → **Switch the frozen primary target to market-excess / factor-residual
(no GICS dependency)** and mark sector-excess `UNAVAILABLE` until licensed, OR license PIT
constituents/GICS. *Owner decision: pay for PIT classification, or drop sector-excess as primary.*

**RT-6 — Recommending A-as-target + schema deltas is premature against a zero-implementation
baseline.** *(all)* → **Freeze R0-1A scope to the Edge-Probe+ truth chain only;** defer *all*
A/B/C/D schema deltas (barrier `LabelRecord` rows, encoder producers, max-availability
`InformationInterval`) until the six R0 gates are `TESTED_RESEARCH`. Note: `InformationInterval =
max availability across modalities` also lets the *slowest* modality set the decision clock — a
timeliness cost for an unproven benefit. *Owner decision: approve the scope freeze.*

**RT-7 — Proposal C mandates an optimizer where 1/N usually wins OOS, and is the weakest
statistical gate.** *(C; portfolio layer of A)* → **Make 1/N and vol-scaled 1/N a hard
net-of-cost baseline** the allocator must beat on the effective sample (DeMiguel-Garlappi-Uppal);
otherwise ship 1/N. **Do not adopt C as the spine.** *Owner decision: adopt 1/N as mandatory
comparator.*

**RT-8 — Proposal B collides with the hard reproducibility gate and maximizes leakage surface.**
*(B)* Rolling-window sequence encoders leak (window-normalization, scaler bleed, overlapping-window
target leakage); GPU nondeterminism breaks the deterministic-rerun + hash-chained-replay gate. →
**B1 only as a gated R4 challenger** behind a byte-identical determinism proof + incremental
net-edge; **B2 REJECTED for R0–R3.** *Owner decision: require the determinism proof + net edge or
B stays off.*

**RT-9 — Proposal D GNN form invites graph contamination + retrieval look-ahead; even the cheap
form may not beat a GICS peer baseline.** *(D)* → **Ship only the rule/score abstention-first
form;** the GNN form is rejected until it beats a GICS/Bhojraj-Lee-Oler peer baseline net-of-cost
with a leakage audit. *Owner decision: confirm GNN out of R0–R3.*

**RT-10 — Source poisoning & coordinated manipulation can weaponize the abstention gate both
ways.** *(A social cross-feature; D contradiction edges; all social)* Attack (a): flood low-trust
duplicates → forced ABSTAIN (denial-of-decision); attack (b): aged/hijacked high-trust source
injects a false claim that passes the gate. Source-trust is cold-start-thin exactly for the burner
accounts used in pump-and-dumps (Xu-Livshits; Da-Engelberg-Gao). → **Set social evidence weight =
0 in the executable edge for R0–R2 (advisory-only);** require independent confirmation across
*uncorrelated source families* before social may **raise** (never lower) permission; a single
unconfirmed cluster may not trip ABSTAIN. *Owner decision: freeze social weight = 0 until a
manipulation-robustness test passes.*

## MEDIUM

**RT-11 — Digest reduction (A) is where subtle look-ahead + researcher DoF hide.** Each bespoke
digest and each hand-picked named cross-feature is a silent trial. → **Register every digest and
cross-feature in the trial registry; count them in DSR; add a PIT unit test per digest asserting
availability-time.** *(subsumed by RT-1.)*

**RT-12 — Horizon × target × head multiplicity silently multiplies the trial count.** {5,8,14} ×
{absolute, market-, sector-excess} × {quantile, barrier, MFE/MAE, meta-label} = dozens of
gate-eligible outputs; "select best horizon" is itself selection. → **Pre-register ONE primary
(target, horizon) for the edge gate before holdout;** all else is diagnostic and counted in the
deflation. *Owner decision: name the single primary target × horizon before the holdout opens.*

**RT-13 — One fused GBT + one utility policy → correlated book-wide failure when the regime
turns.** *(A, C)* → **Make positive net edge in each regime bucket a hard gate + add a portfolio
correlated-drawdown cap.** *Owner decision: freeze regime buckets + per-regime edge requirement.*

**RT-14 — Next-open entry with soft capacity leaves microcap concentration unpoliced.** *(all)* ML
equity anomalies concentrate in microcaps where paper edge evaporates at size
(Avramov-Cheng-Metzker). → **Hard capacity gate:** edge must survive at a stated AUM with
participation ≤ X% ADV + a spread/impact model; freeze `minimum_dollar_volume`. *Owner decision:
freeze AUM, %ADV, min-ADV.*

**RT-15 — The agentic Git model can launder unbounded multiple testing.** Agents trying many
feature/digest variants feed the same holdout unlogged. → **Every agent-run experiment writes a
trial-registry row; DSR counts agent trials; CI blocks a holdout comparison whose trial count
exceeds the registered pre-registration.** *(subsumed by RT-1.)*

**RT-16 — Several evidence-layer "0-tolerance" gates are unfalsifiable on this sample.**
(unsupported-counterfactual=0, duplicate-independent-evidence=0, positive `independent_information_gain`)
→ **Keep DEFERRED/RESEARCH_ONLY, non-blocking for R0-1A** until the sample supports estimation.
*Owner decision: confirm non-blocking.*

---

## Verdicts (specialist, lead-endorsed)
- **(i) Most likely failure mode:** after an honest factor-residual, net-of-cost, effective-sample-
deflated evaluation, the price/volume+digest signal is **statistically indistinguishable from
cheap investable factors — edge real-but-already-priced.** It lands first on Edge-Probe+ — which
is exactly why building Edge-Probe+ first is right; `BLOCKED_NO_EDGE` is the true finding. The
danger is a **false GO**, *more* likely here than at a mature shop because the four defenses that
make `BLOCKED_NO_EDGE` trustworthy are unbuilt.
- **(ii) Reject outright:** **B2** (sequence-as-forecaster path distributions) for R0–R3, and the
**GNN form of D**. Keep **B1** only as a strictly-gated R4 challenger; keep **D** rule/score only;
**demote C beneath a mandatory 1/N** net-of-cost baseline. A and C are not rejected outright.
- **(iii) On "A-as-target + Edge-Probe+-first":** *partially endorse with reframing.* Edge-Probe+
first is correct and should be the **entire content of R0–1A**. **A must not be labeled "target"**
— it is a not-yet-earned candidate, admissible only if a specific modality clears its ablation
net-of-cost, factor-residual, on the effective sample; the honest prior is that it will not.
Reorder to: **(1)** build + test the four kernel primitives; **(2)** build Edge-Probe+ → deflated,
factor-residual, capacity-limited verdict; **(3)** admit a single modality into A only on a passed
ablation; **(4)** cap C under 1/N; **(5)** hold B1 at R4, reject B2/GNN-D. Until the kernel gaps
close, the ranking A>B>C>D is **unmeasurable**.
