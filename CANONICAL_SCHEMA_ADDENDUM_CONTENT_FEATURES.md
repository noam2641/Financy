# Canonical Schema Addendum: Content, Features, and Training Artifacts

This addendum is the implementation-facing schema companion for the conversation-derived entities added to the canonical specification v4.6. It does not replace the canonical specification; it makes the new entities concrete enough for schema, migration, and test work.

## Entity Governance

| Entity | Primary key | Foreign keys | Source of truth | Allowed writer | Immutability | Unique constraints | Retention policy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `content_item` | `content_id` | `source_profile_id`, `source_record_id` | Content ingestion service | Content ingestion service | Immutable after canonicalization except append-only corrections | `source_id`, `canonical_url_hash`, `published_at`, `content_hash` | Retain decision-used metadata, hashes, timestamps, and lineage for at least 7 years; raw text follows license/privacy rules. |
| `content_enrichment` | `content_enrichment_id` | `content_id`, `model_registry_snapshot_id` | Content enrichment service | Content enrichment service | Immutable; new model versions create new rows | `content_id`, `enrichment_type`, `model_version`, `feature_available_at` | Retain decision-used enrichments for at least 7 years. |
| `content_market_link` | `content_market_link_id` | `content_id`, `instrument_id` | Content linkage service / Learning Lab | Content linkage service; outcome service may append matured outcome reference | Immutable after link computation except matured outcome reference | `content_id`, `instrument_id`, `link_method`, `event_time` | Retain links used in features, labels, or reliability learning for at least 7 years. |
| `source_profile` | `source_profile_id` | `source_id` | Source reliability service | Source reliability service | Append-only point-in-time snapshots | `source_id`, `profile_as_of_at`, `profile_version` | Retain PIT profile history for at least 7 years when used in decisions/training. |
| `feature_snapshot` | `feature_snapshot_id` | `decision_cycle_id`, `data_snapshot_id`, `feature_set_id` | Feature store service | Feature store service | Immutable after cutoff and schema hash are sealed | `entity_scope`, `entity_id`, `feature_set_id`, `feature_as_of_at`, `feature_schema_hash` | Retain decision-used feature snapshots for at least 7 years. |
| `model_training_artifact` | `model_training_artifact_id` | `feature_snapshot_id`, `model_registry_snapshot_id`, `policy_bundle_id` | Research Factory / model registry | Research Factory and model registry | Immutable after registration | `model_family`, `model_version`, `training_cutoff_at`, `training_data_hash` | Retain promoted artifacts for at least 7 years after retirement. |

## Required Field Groups

| Entity | Identity fields | Time fields | Lineage fields | Decision-safety fields |
| --- | --- | --- | --- | --- |
| `content_item` | `content_id`, `source_id`, `canonical_url_hash`, `content_hash` | `published_at`, `publicly_available_at`, `provider_ingested_at`, `system_available_at` | `source_record_id`, `ingestion_run_id`, `provider`, `raw_text_pointer` | `licensing_status`, `language`, `mentioned_instrument_ids` |
| `content_enrichment` | `content_enrichment_id`, `content_id`, `enrichment_type` | `feature_available_at`, `processed_at` | `model_registry_snapshot_id`, `model_family`, `model_version`, `input_text_hash` | calibrated probabilities, relevance, novelty, event type, output schema version |
| `content_market_link` | `content_market_link_id`, `content_id`, `instrument_id` | `event_time`, `market_observation_start_at`, `market_observation_end_at` | `link_method`, `bar_interval`, `outcome_record_id_if_matured` | `link_confidence`, `label_maturity_status`, pre/post event response fields |
| `source_profile` | `source_profile_id`, `source_id`, `profile_version` | `profile_as_of_at`, `last_updated_at` | source family, publisher, platform, author ID | reliability score, confidence interval, cold-start status |
| `feature_snapshot` | `feature_snapshot_id`, `feature_set_id`, `entity_scope`, `entity_id` | `trading_date`, `feature_as_of_at`, `feature_cutoff_at`, `feature_available_at` | `decision_cycle_id`, `data_snapshot_id`, `lineage_refs` | `feature_schema_hash`, missingness summary, row/column counts |
| `model_training_artifact` | `model_training_artifact_id`, `training_run_id`, `model_version` | `training_cutoff_at`, `created_at` | `feature_snapshot_id`, `training_data_hash`, `target_schema_version`, `walk_forward_protocol_id` | calibration method, baseline comparison IDs, promotion environment |

## Operator Tool Audit Mapping

`operator_tool_audit_event` is not a canonical entity.

Operator tool usage maps to:

```text
audit_event:
  event_type = OPERATOR_TOOL_USED
  entity_type = target entity type
  entity_id = target entity id
  actor_id = operator or service account
  event_time = UTC timestamp
  read_write_intent = READ_ONLY | WRITE_ATTEMPT | APPROVED_WRITE
  redacted_parameters = JSON object
  correlation_id = request/run correlation id
```

## Implementation Rules

1. `content_item` is created before enrichment, linkage, daily aggregation, or source-profile scoring.
2. `content_enrichment` cannot overwrite raw content identity fields.
3. `content_market_link` cannot mature labels until the market observation window is complete.
4. `source_profile` must be point-in-time; current-score lookups are forbidden in historical training.
5. `feature_snapshot` is the bridge between `training_df`, `latest_features_df`, forecast snapshots, and replay.
6. `model_training_artifact` must store hashes for the feature data, target schema, code version, and registered model artifact.
7. Production code must not create parallel `*_df`-only schemas without mapping them back to these canonical entities.

