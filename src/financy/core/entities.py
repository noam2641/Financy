"""Canonical Release-0 entity schemas.

TASK-R0-02 · FC-R0-02 · ENT-R0-01..ENT-R0-21.

Schema definitions only — frozen, slotted, keyword-only dataclasses with narrow
schema-level validation (closed-enum membership, singleton closed values, and
required (non-null) fields). No writers, persistence, serialization, hashing,
providers, labels, splitters, models, costs, reports, or ledgers live here; those
belong to later tasks. Standard library only; no network, clock, filesystem, or
current-date behaviour.

Field names, order, closed vocabularies, and nullability are governed by
docs/architecture_definition/contracts/RELEASE_0_ENTITY_AND_SCHEMA_CONTRACTS.md.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum, IntEnum
from typing import Mapping, NewType


# --- closed vocabularies (str/IntEnum) ---------------------------------------

class PriceBasis(str, Enum):
    """Closed price basis for the raw vintage (ENT-R0-02)."""
    RAW = "RAW"


class ActionType(str, Enum):
    SPLIT = "SPLIT"
    DIVIDEND = "DIVIDEND"
    MERGER = "MERGER"
    SPINOFF = "SPINOFF"


class IdentifierType(str, Enum):
    TICKER = "TICKER"
    CIK = "CIK"
    FIGI = "FIGI"


class TerminalEventType(str, Enum):
    DELIST = "DELIST"
    MERGER = "MERGER"
    BANKRUPT = "BANKRUPT"


class HorizonSessions(IntEnum):
    """Closed R0 swing horizons in exchange sessions."""
    FIVE = 5
    EIGHT = 8
    FOURTEEN = 14


class TargetBasis(str, Enum):
    ABSOLUTE_EXECUTABLE_RETURN = "ABSOLUTE_EXECUTABLE_RETURN"


class MaturityStatus(str, Enum):
    MATURED = "MATURED"
    NOT_MATURED = "NOT_MATURED"
    TERMINAL_EVENT = "TERMINAL_EVENT"


class ModelProducer(str, Enum):
    BASELINE_GBT = "BASELINE_GBT"
    COMPARATOR_ELASTICNET = "COMPARATOR_ELASTICNET"
    COMPARATOR_FAMA_MACBETH = "COMPARATOR_FAMA_MACBETH"
    PER_DATE_ORACLE = "PER_DATE_ORACLE"


class OutputType(str, Enum):
    CONTINUOUS_RETURN = "CONTINUOUS_RETURN"
    PROBABILITY = "PROBABILITY"


class EvaluationOutcome(str, Enum):
    EDGE_SUPPORTED = "EDGE_SUPPORTED"
    BLOCKED_NO_EDGE = "BLOCKED_NO_EDGE"
    INCONCLUSIVE = "INCONCLUSIVE"


class BenchmarkComponent(str, Enum):
    SPY = "SPY"
    MATCHED_BASKET = "matched_basket"


class FactorName(str, Enum):
    MKT = "Mkt"
    SMB = "SMB"
    HML = "HML"
    UMD = "UMD"
    STREV = "STRev"
    BAB = "BAB"


class EceNotApplicable(str, Enum):
    """Closed sentinel for a regression-primary ECE value (ENT-R0-15)."""
    NOT_APPLICABLE_TO_PRIMARY_REGRESSION = "NOT_APPLICABLE_TO_PRIMARY_REGRESSION"


# --- open enum placeholders (opaque str NewTypes; no invented members) -------

PriceBasisValue = NewType("PriceBasisValue", str)
DividendTreatmentValue = NewType("DividendTreatmentValue", str)
AssetTypeValue = NewType("AssetTypeValue", str)
TerminalEventPolicyValue = NewType("TerminalEventPolicyValue", str)
TrialTargetBasisValue = NewType("TrialTargetBasisValue", str)
RunLedgerEventTypeValue = NewType("RunLedgerEventTypeValue", str)
ExitLegValue = NewType("ExitLegValue", str)

#: The only exit-leg value named by the contract (`enum{CLOSE_AUCTION,...}`).
CLOSE_AUCTION: ExitLegValue = ExitLegValue("CLOSE_AUCTION")


# --- narrow schema validation helpers ----------------------------------------

def _reject_unexpected_none(instance: object, nullable: tuple[str, ...] = ()) -> None:
    for f in dataclasses.fields(instance):  # type: ignore[arg-type]
        if f.name in nullable:
            continue
        if getattr(instance, f.name) is None:
            raise ValueError(
                f"{type(instance).__name__}.{f.name} is required and must not be None"
            )


def _require_enum(value: object, enum_cls: type, field_name: str) -> None:
    if not isinstance(value, enum_cls):
        raise TypeError(
            f"{field_name} must be a {enum_cls.__name__} member, got {type(value).__name__}"
        )


def _require_enum_tuple(value: object, enum_cls: type, field_name: str) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple of {enum_cls.__name__} members")
    for element in value:
        if not isinstance(element, enum_cls):
            raise TypeError(
                f"{field_name} elements must be {enum_cls.__name__} members"
            )


# --- entity dataclasses (ENT-R0-01..21) --------------------------------------

@dataclass(frozen=True, slots=True, kw_only=True)
class SourceRecord:
    """ENT-R0-01."""
    source_id: str
    provider: str
    endpoint: str
    request_params: Mapping[str, object]
    pull_timestamp: datetime
    is_estimated_timestamp: bool
    raw_payload_hash: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class RawOHLCVBar:
    """ENT-R0-02."""
    instrument_id: str
    session_date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    price_basis: PriceBasis
    source_id: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum(self.price_basis, PriceBasis, "RawOHLCVBar.price_basis")


@dataclass(frozen=True, slots=True, kw_only=True)
class CorporateActionRecord:
    """ENT-R0-03."""
    instrument_id: str
    action_type: ActionType
    ex_date: date
    split_adjustment_factor: Decimal
    dividend_amount: Decimal
    dividend_treatment: DividendTreatmentValue
    corporate_action_version: str
    source_id: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum(self.action_type, ActionType, "CorporateActionRecord.action_type")


@dataclass(frozen=True, slots=True, kw_only=True)
class DerivedPriceSeriesMetadata:
    """ENT-R0-04."""
    instrument_id: str
    as_of_cutoff: date
    corporate_action_version: str
    price_basis: PriceBasisValue
    dividend_treatment: DividendTreatmentValue
    derivation_hash: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class InstrumentMasterRecord:
    """ENT-R0-05."""
    instrument_id: str
    first_seen: date
    asset_type: AssetTypeValue
    primary_exchange: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class InstrumentIdentifierRecord:
    """ENT-R0-06."""
    instrument_id: str
    identifier_type: IdentifierType
    identifier_value: str
    valid_from: date
    valid_to: date | None

    def __post_init__(self) -> None:
        _reject_unexpected_none(self, nullable=("valid_to",))
        _require_enum(self.identifier_type, IdentifierType, "InstrumentIdentifierRecord.identifier_type")


@dataclass(frozen=True, slots=True, kw_only=True)
class FixedPITCohortMember:
    """ENT-R0-07 — exactly the nine §0.4 fields."""
    cohort_selection_date: date
    universe_definition_version: str
    eligibility_rule_version: str
    constituent_source_id: str
    source_as_of: date
    instrument_id: str
    inclusion_reason: str
    exclusion_reason: str | None
    terminal_event_policy: TerminalEventPolicyValue

    def __post_init__(self) -> None:
        _reject_unexpected_none(self, nullable=("exclusion_reason",))


@dataclass(frozen=True, slots=True, kw_only=True)
class TerminalEventRecord:
    """ENT-R0-08."""
    instrument_id: str
    event_type: TerminalEventType
    event_date: date
    terminal_return: Decimal
    terminal_value_source: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum(self.event_type, TerminalEventType, "TerminalEventRecord.event_type")


@dataclass(frozen=True, slots=True, kw_only=True)
class LabelRecord:
    """ENT-R0-09."""
    instrument_id: str
    prediction_time: datetime
    horizon_sessions: HorizonSessions
    label_value: Decimal
    price_basis: PriceBasisValue
    target_basis: TargetBasis
    maturity_status: MaturityStatus
    label_available_at: datetime
    target_definition_version: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum(self.horizon_sessions, HorizonSessions, "LabelRecord.horizon_sessions")
        _require_enum(self.target_basis, TargetBasis, "LabelRecord.target_basis")
        _require_enum(self.maturity_status, MaturityStatus, "LabelRecord.maturity_status")


@dataclass(frozen=True, slots=True, kw_only=True)
class FeatureSnapshot:
    """ENT-R0-10."""
    snapshot_id: str
    as_of_date: date
    schema_hash: str
    feature_values_checksum: str
    fitted_transform_ref: str
    fit_indices_ref: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class InformationInterval:
    """ENT-R0-11 — two identity/context fields + the exact six §0.5 fields."""
    instrument_id: str
    horizon_sessions: HorizonSessions
    feature_information_start: date
    prediction_time: datetime
    label_start: date
    label_end: date
    label_available_at: datetime
    information_interval: tuple[date, date]

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum(self.horizon_sessions, HorizonSessions, "InformationInterval.horizon_sessions")


@dataclass(frozen=True, slots=True, kw_only=True)
class FoldManifest:
    """ENT-R0-12."""
    fold_id: str
    train_prediction_times: tuple[datetime, ...]
    test_prediction_times: tuple[datetime, ...]
    embargo_buffer_sessions: int
    embargo_justification: str
    no_overlap_asserted: bool

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class TrialRecord:
    """ENT-R0-13."""
    trial_id: str
    config_hash: str
    seed: int
    horizon: int
    target_basis: TrialTargetBasisValue
    chosen_after_backtest: bool
    created_event_ref: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class ModelArtifactManifest:
    """ENT-R0-14 — single-writer preserved by the `producer` discriminator."""
    artifact_id: str
    producer: ModelProducer
    model_family: str
    train_fold_ref: str
    hyperparameters: Mapping[str, object]
    seed: int
    artifact_hash: str
    environment_hash: str
    oos_eligible: bool

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum(self.producer, ModelProducer, "ModelArtifactManifest.producer")


@dataclass(frozen=True, slots=True, kw_only=True)
class CalibrationArtifactManifest:
    """ENT-R0-15."""
    output_name: str
    output_type: OutputType
    method: str
    target: str
    fit_set_id: str
    calibration_set_id: str
    eval_set_id: str
    units: str
    metric: str
    ece_value: EceNotApplicable | float

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum(self.output_type, OutputType, "CalibrationArtifactManifest.output_type")
        if not isinstance(self.ece_value, (EceNotApplicable, float)):
            raise TypeError(
                "CalibrationArtifactManifest.ece_value must be EceNotApplicable or float"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class BenchmarkDefinition:
    """ENT-R0-16."""
    benchmark_id: str
    components: tuple[BenchmarkComponent, ...]
    beta_adjustment: Decimal
    cost_model_ref: str
    rebalance_timing: str
    eligibility_rule: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum_tuple(self.components, BenchmarkComponent, "BenchmarkDefinition.components")


@dataclass(frozen=True, slots=True, kw_only=True)
class CostModelDefinition:
    """ENT-R0-17."""
    cost_model_id: str
    commission_bps: Decimal
    spread_bps: Decimal
    impact_coefficient: Decimal
    exit_leg: ExitLegValue
    proxy_floor_bps: Decimal
    version: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class FactorAttributionResult:
    """ENT-R0-18 — run_id plus the 16 §0.8 attribution fields (17 total)."""
    run_id: str
    return_frequency: str
    regression_window: str
    factor_set: tuple[FactorName, ...]
    factor_source_versions: Mapping[str, str]
    alpha_interpretation: str
    standard_error_method: str
    matched_basket_ref: str
    long_short_leg_policy: str
    turnover_matching: str
    cost_parity_ref: str
    beta_matching: str
    rebalance_timing: str
    benchmark_eligibility: str
    missing_factor_behavior: str
    residual_alpha_bps: Decimal
    residual_alpha_significance: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum_tuple(self.factor_set, FactorName, "FactorAttributionResult.factor_set")


@dataclass(frozen=True, slots=True, kw_only=True)
class EvaluationReport:
    """ENT-R0-19."""
    run_id: str
    forecast_metrics: Mapping[str, object]
    calibration_block: Mapping[str, object]
    comparator_block: Mapping[str, object]
    hurdle_block: Mapping[str, object]
    attribution_ref: str
    benchmark_ref: str
    outcome: EvaluationOutcome
    pre_registration_ref: str
    environment_hash: str

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
        _require_enum(self.outcome, EvaluationOutcome, "EvaluationReport.outcome")


@dataclass(frozen=True, slots=True, kw_only=True)
class RunLedgerEvent:
    """ENT-R0-20."""
    event_id: str
    event_type: RunLedgerEventTypeValue
    prior_event_hash: str
    payload_hash: str
    environment_hash: str
    timestamp: datetime

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class RuntimeEnvironmentManifest:
    """ENT-R0-21."""
    environment_hash: str
    interpreter_version: str
    dependency_lockfile_hash: str
    os_arch: str
    blas_threading_flags: str
    random_seeds: Mapping[str, int]
    data_vintage_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _reject_unexpected_none(self)
