# 07 — News, Filings, Telegram & Social-Attention Engine

**Artifact type:** design (lead-authored; follows Alternative A's trust-gated ingestion layer;
grounded in `03` Q6/Q13/Q15). **Decision-label:** ingestion + PIT-trust design =
`ARCHITECTURAL_INFERENCE`; predictive value of any text/social modality = `EMPIRICAL_TBD`
(must beat the price/volume-only baseline net-of-cost before inclusion). **Legal/licensing =
`OWNER_DECISION_REQUIRED`.**

Governing evidence: news carries **short-horizon, reversal-flavored, cost-fragile** signal
(Tetlock 2007); retail attention → short-run rise then **reversal** (Da-Engelberg-Gao 2011);
Telegram-coordinated pump-and-dump is real and dissectable (Xu-Livshits 2019); LLM-derived
features are **attackable** (prompt injection / source poisoning — Zou et al. 2023).
Conclusion: text/social are **as much risk/ABSTAIN flags as buy signals.**

---

## 1. PIT ingestion (the availability-time contract)
Ingest news, company announcements, SEC filings (EDGAR as-filed, **acceptance-datetime**),
earnings/guidance/transcripts, analyst revisions, political/tax/regulatory statements, public
Telegram channels, public social media, and rumor + rumor-confirmation/rejection events. Each
item lands as the canonical `content_item` (unchanged addendum entity) with, where available:
`source_id`, publisher, author, **publication timestamp**, **first-observed timestamp**, **edit
timestamp**, **deletion status**, raw-content hash, language, affected instruments, affected
peers, extracted event, direction, magnitude, sentiment, stance, certainty, **novelty**,
urgency, expected horizon, corroboration, contradiction, engagement, **repost lineage**,
historical source reliability, manipulation-risk score.

**The one hard rule** (Alt A §0): a content feature enters a decision only through
`content_enrichment.feature_available_at`, and the sample's `InformationInterval` widens to the
**max availability-time across modalities**. Content published after close is **not** linked to
that session's close (canonical REQ-CONV-LINK-006). Estimated timestamps ⇒
`is_estimated_timestamp=true` ⇒ INFORMATION_THEORETIC replay only + trust down-weighting.
Market reactions used as labels must **mature** before updating a source's reliability.

## 2. Source reliability & attention — features, never truth
- **Source-trust is PIT.** `source_profile` is append-only with `profile_as_of_at`; a decision
uses only the reliability snapshot with `profile_as_of_at ≤ prediction_time` (using a
currently-learned reliability is look-ahead). Cold-start sources shrink to a family prior.
- **Attention/novelty are velocity features, not evidence of truth.** *"30 posts in five days"*
is an `attention_velocity` / `novelty` feature; it is **never** treated as confirmation of the
underlying claim. Because attention predicts short-run rise then reversal (Da-Engelberg-Gao),
an attention spike is modeled as a **risk flag** feeding the abstention gate, not (only) a buy
signal. The manipulation-critical interaction `attention_spike × source_trust ×
price_already_moved` is a frozen named cross-feature that routes hyped-after-the-move names to
REDUCE/ABSTAIN, not BUY.
- **Corroboration ≠ count.** Corroboration is weighted by **independent** source-trust and
de-duplicated repost lineage — N reposts of one root event count once (canonical evidence-
independence principle), preventing fake corroboration from inflating confidence.

## 3. Manipulation & security defenses (first-class, not an afterthought)
| Threat | Defense |
|---|---|
| Duplicate content / circular reporting | content-hash dedup + repost-lineage clustering; corroboration counts *independent roots* only |
| Bots / coordinated campaigns / pump-and-dump | attention-velocity + account-age/coordination signals feed a manipulation-risk score → ABSTAIN trigger (Xu-Livshits pattern); social spikes bias toward REDUCE/ABSTAIN |
| Impersonation | source identity verification; unverified-source content carries low PIT trust |
| Edited / deleted posts | edit & deletion timestamps retained; a post deleted before the cutoff is treated per policy (not silently used); edits create new versioned records |
| Uncertain timestamps | `is_estimated_timestamp` ⇒ INFORMATION_THEORETIC only + trust penalty near the cutoff |
| Fake corroboration | independence-weighted corroboration (above) |
| **Source poisoning / prompt injection in ingested text** | ingested content is **data, never instructions**; any LLM enrichment runs with untrusted-content isolation; LLM-derived features are attackable features that must pass source-trust + the probability-integrity gate (`11`) and can never be the sole basis of a probability (Zou et al. 2023) |

## 4. The LLM's permitted role here
The LLM/agent may **extract** structured events, **classify** stance/novelty/sentiment,
**identify contradictions**, **cluster** repost lineage, and **explain** — producing *features*
and *evidence links*, always PIT-stamped and source-trust-weighted. It may **not** invent or
move a probability, treat attention as truth, or place an order (`11` §5). Every LLM-derived
field records provider, model version, prompt-template version, and validation status
(canonical REQ-LLM provenance).

## 5. Licensing & legal access (owner-gated)
News APIs, social platforms, and Telegram each carry terms; some prohibit commercial use or
redistribution, and system-availability timestamps for free feeds are weak (A2 evidence). Which
sources are permissible in research vs paper vs live is an **owner decision** (`16`), and no
modality is promoted past research without a permitted-use determination. yfinance-class free
data is prototyping-only. This engine is therefore **added last** on the roadmap (`15`), behind
the free-PIT price/fundamentals/macro core, and each source is switched on only when both (a)
its ablation beats the baseline net-of-cost and (b) its licensing clears.

## 6. What this engine does NOT claim
No assumption that news/social is durably predictive (evidence says short-horizon, reversal-
flavored, cost-fragile); no treatment of attention or post-count as truth; no LLM authority over
numbers or orders; no ingestion without availability stamping and source-trust; no commercial
use of a source before a licensing determination.
