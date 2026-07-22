"""Specification tests for the canonical R0 entity schemas.

TASK-R0-02 · FC-R0-02 (financy.core.entities) · ENT-R0-01..ENT-R0-21.

Schema-only: verifies dataclass representation, exact field sets/order (pinned in
tests/fixtures/entities/r0_entity_schema_fields.json), closed-enum vocabularies,
open placeholder types, and frozen immutability. No writer/business behaviour is
exercised. Deterministic and offline.
"""

from __future__ import annotations

import dataclasses
import enum
import json
import typing
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from financy.core import entities as E

_FIXTURE = (
    Path(__file__).resolve().parents[3]
    / "tests"
    / "fixtures"
    / "entities"
    / "r0_entity_schema_fields.json"
)


def _schema() -> dict:
    return json.loads(_FIXTURE.read_text())


ENTITY_CLASS_NAMES = [
    "SourceRecord",
    "RawOHLCVBar",
    "CorporateActionRecord",
    "DerivedPriceSeriesMetadata",
    "InstrumentMasterRecord",
    "InstrumentIdentifierRecord",
    "FixedPITCohortMember",
    "TerminalEventRecord",
    "LabelRecord",
    "FeatureSnapshot",
    "InformationInterval",
    "FoldManifest",
    "TrialRecord",
    "ModelArtifactManifest",
    "CalibrationArtifactManifest",
    "BenchmarkDefinition",
    "CostModelDefinition",
    "FactorAttributionResult",
    "EvaluationReport",
    "RunLedgerEvent",
    "RuntimeEnvironmentManifest",
]


# --- representative valid instances ------------------------------------------

def _instances() -> dict:
    d0 = date(2023, 6, 15)
    d1 = date(2023, 6, 16)
    d5 = date(2023, 6, 23)
    ts0 = datetime(2023, 6, 15, 16, 0, 0)
    ts1 = datetime(2023, 6, 26, 9, 0, 0)
    return {
        "SourceRecord": E.SourceRecord(
            source_id="src1", provider="fixture", endpoint="ohlcv",
            request_params={"symbol": "X"}, pull_timestamp=ts0,
            is_estimated_timestamp=False, raw_payload_hash="h",
        ),
        "RawOHLCVBar": E.RawOHLCVBar(
            instrument_id="i1", session_date=d0, open=Decimal("1"),
            high=Decimal("2"), low=Decimal("1"), close=Decimal("2"),
            volume=100, price_basis=E.PriceBasis.RAW, source_id="src1",
        ),
        "CorporateActionRecord": E.CorporateActionRecord(
            instrument_id="i1", action_type=E.ActionType.SPLIT, ex_date=d0,
            split_adjustment_factor=Decimal("2"), dividend_amount=Decimal("0"),
            dividend_treatment=E.DividendTreatmentValue("none"),
            corporate_action_version="cav1", source_id="src1",
        ),
        "DerivedPriceSeriesMetadata": E.DerivedPriceSeriesMetadata(
            instrument_id="i1", as_of_cutoff=d0, corporate_action_version="cav1",
            price_basis=E.PriceBasisValue("as_of_adjusted"),
            dividend_treatment=E.DividendTreatmentValue("none"),
            derivation_hash="dh",
        ),
        "InstrumentMasterRecord": E.InstrumentMasterRecord(
            instrument_id="i1", first_seen=d0,
            asset_type=E.AssetTypeValue("equity"), primary_exchange="XNYS",
        ),
        "InstrumentIdentifierRecord": E.InstrumentIdentifierRecord(
            instrument_id="i1", identifier_type=E.IdentifierType.TICKER,
            identifier_value="ABC", valid_from=d0, valid_to=None,
        ),
        "FixedPITCohortMember": E.FixedPITCohortMember(
            cohort_selection_date=d0, universe_definition_version="u1",
            eligibility_rule_version="e1", constituent_source_id="cs1",
            source_as_of=d0, instrument_id="i1", inclusion_reason="liquid",
            exclusion_reason=None,
            terminal_event_policy=E.TerminalEventPolicyValue("hold_to_terminal"),
        ),
        "TerminalEventRecord": E.TerminalEventRecord(
            instrument_id="i1", event_type=E.TerminalEventType.DELIST,
            event_date=d5, terminal_return=Decimal("-100"),
            terminal_value_source="vendor",
        ),
        "LabelRecord": E.LabelRecord(
            instrument_id="i1", prediction_time=ts0,
            horizon_sessions=E.HorizonSessions.FIVE, label_value=Decimal("12"),
            price_basis=E.PriceBasisValue("as_of_adjusted"),
            target_basis=E.TargetBasis.ABSOLUTE_EXECUTABLE_RETURN,
            maturity_status=E.MaturityStatus.MATURED, label_available_at=ts1,
            target_definition_version="t1",
        ),
        "FeatureSnapshot": E.FeatureSnapshot(
            snapshot_id="fs1", as_of_date=d0, schema_hash="sh",
            feature_values_checksum="fc", fitted_transform_ref="ft",
            fit_indices_ref="fi",
        ),
        "InformationInterval": E.InformationInterval(
            instrument_id="i1", horizon_sessions=E.HorizonSessions.FIVE,
            feature_information_start=date(2023, 5, 17), prediction_time=ts0,
            label_start=d1, label_end=d5, label_available_at=ts1,
            information_interval=(date(2023, 5, 17), d5),
        ),
        "FoldManifest": E.FoldManifest(
            fold_id="f1", train_prediction_times=(ts0,),
            test_prediction_times=(ts1,), embargo_buffer_sessions=14,
            embargo_justification="horizon+delay", no_overlap_asserted=True,
        ),
        "TrialRecord": E.TrialRecord(
            trial_id="tr1", config_hash="ch", seed=7, horizon=5,
            target_basis=E.TrialTargetBasisValue("absolute"),
            chosen_after_backtest=False, created_event_ref="ev1",
        ),
        "ModelArtifactManifest": E.ModelArtifactManifest(
            artifact_id="a1", producer=E.ModelProducer.BASELINE_GBT,
            model_family="gbt", train_fold_ref="f1", hyperparameters={"lr": 0.1},
            seed=7, artifact_hash="ah", environment_hash="eh", oos_eligible=True,
        ),
        "CalibrationArtifactManifest": E.CalibrationArtifactManifest(
            output_name="expected_absolute_executable_return_bps",
            output_type=E.OutputType.CONTINUOUS_RETURN, method="residual",
            target="ret", fit_set_id="fit", calibration_set_id="cal",
            eval_set_id="eval", units="bps", metric="interval_coverage",
            ece_value=E.EceNotApplicable.NOT_APPLICABLE_TO_PRIMARY_REGRESSION,
        ),
        "BenchmarkDefinition": E.BenchmarkDefinition(
            benchmark_id="b1",
            components=(E.BenchmarkComponent.SPY, E.BenchmarkComponent.MATCHED_BASKET),
            beta_adjustment=Decimal("1"), cost_model_ref="cm1",
            rebalance_timing="close", eligibility_rule="liquid",
        ),
        "CostModelDefinition": E.CostModelDefinition(
            cost_model_id="cm1", commission_bps=Decimal("1"),
            spread_bps=Decimal("2"), impact_coefficient=Decimal("0.5"),
            exit_leg=E.CLOSE_AUCTION, proxy_floor_bps=Decimal("3"), version="v1",
        ),
        "FactorAttributionResult": E.FactorAttributionResult(
            run_id="r1", return_frequency="daily", regression_window="252",
            factor_set=(E.FactorName.MKT, E.FactorName.SMB), factor_source_versions={"famafrench": "2023"},
            alpha_interpretation="residual", standard_error_method="newey_west",
            matched_basket_ref="mb", long_short_leg_policy="long_only",
            turnover_matching="matched", cost_parity_ref="cm1",
            beta_matching="matched", rebalance_timing="close",
            benchmark_eligibility="eligible", missing_factor_behavior="fail",
            residual_alpha_bps=Decimal("5"), residual_alpha_significance="NOT_ESTIMABLE",
        ),
        "EvaluationReport": E.EvaluationReport(
            run_id="r1", forecast_metrics={"ic": 0.0}, calibration_block={},
            comparator_block={}, hurdle_block={}, attribution_ref="fa1",
            benchmark_ref="b1", outcome=E.EvaluationOutcome.BLOCKED_NO_EDGE,
            pre_registration_ref="pr1", environment_hash="eh",
        ),
        "RunLedgerEvent": E.RunLedgerEvent(
            event_id="e1", event_type=E.RunLedgerEventTypeValue("REPORT_GENERATED"),
            prior_event_hash="p", payload_hash="pl", environment_hash="eh",
            timestamp=ts0,
        ),
        "RuntimeEnvironmentManifest": E.RuntimeEnvironmentManifest(
            environment_hash="eh", interpreter_version="3.12",
            dependency_lockfile_hash="lh", os_arch="linux-x86_64",
            blas_threading_flags="1", random_seeds={"global": 7},
            data_vintage_ids=("v1",),
        ),
    }


def _cls(name: str):
    return getattr(E, name)


# --- 1-4: structural representation ------------------------------------------

def test_all_21_classes_present():
    assert len(ENTITY_CLASS_NAMES) == 21
    for name in ENTITY_CLASS_NAMES:
        assert hasattr(E, name), f"missing entity class {name}"


@pytest.mark.parametrize("name", ENTITY_CLASS_NAMES)
def test_is_dataclass(name):
    assert dataclasses.is_dataclass(_cls(name))


@pytest.mark.parametrize("name", ENTITY_CLASS_NAMES)
def test_is_frozen(name):
    assert _cls(name).__dataclass_params__.frozen is True


@pytest.mark.parametrize("name", ENTITY_CLASS_NAMES)
def test_uses_slots(name):
    cls = _cls(name)
    assert "__slots__" in cls.__dict__


# --- 5: keyword-only (positional construction rejected) ----------------------

def test_positional_construction_rejected():
    with pytest.raises(TypeError):
        E.SourceRecord("src1", "fixture", "ohlcv", {}, datetime(2023, 6, 15), False, "h")


# --- 6,7: exact ordered field set per fixture --------------------------------

@pytest.mark.parametrize("ent_id, spec", list(_schema().items()))
def test_exact_ordered_fields(ent_id, spec):
    cls = _cls(spec["class"])
    actual = [f.name for f in dataclasses.fields(cls)]
    assert actual == spec["fields"], f"{spec['class']} field mismatch"


# --- 8,9,10,11: critical field sets ------------------------------------------

def test_fixed_pit_cohort_member_nine_fields():
    fields = [f.name for f in dataclasses.fields(E.FixedPITCohortMember)]
    assert len(fields) == 9
    assert fields == [
        "cohort_selection_date", "universe_definition_version",
        "eligibility_rule_version", "constituent_source_id", "source_as_of",
        "instrument_id", "inclusion_reason", "exclusion_reason",
        "terminal_event_policy",
    ]


def test_information_interval_two_plus_six():
    fields = [f.name for f in dataclasses.fields(E.InformationInterval)]
    assert len(fields) == 8
    assert fields[:2] == ["instrument_id", "horizon_sessions"]
    assert fields[2:] == [
        "feature_information_start", "prediction_time", "label_start",
        "label_end", "label_available_at", "information_interval",
    ]
    for forbidden in ("duration", "embargo", "feature_lookback", "fold_id"):
        assert forbidden not in fields


def test_factor_attribution_seventeen_fields():
    fields = [f.name for f in dataclasses.fields(E.FactorAttributionResult)]
    assert len(fields) == 17
    assert fields[0] == "run_id"


def test_model_artifact_manifest_producer_annotation():
    ann = E.ModelArtifactManifest.__annotations__
    assert "producer" in ann
    assert ann["producer"] == "ModelProducer"


# --- 12: closed enum vocabularies --------------------------------------------

def test_closed_enum_values():
    assert {m.value for m in E.PriceBasis} == {"RAW"}
    assert {m.value for m in E.ActionType} == {"SPLIT", "DIVIDEND", "MERGER", "SPINOFF"}
    assert {m.value for m in E.IdentifierType} == {"TICKER", "CIK", "FIGI"}
    assert {m.value for m in E.TerminalEventType} == {"DELIST", "MERGER", "BANKRUPT"}
    assert {int(m) for m in E.HorizonSessions} == {5, 8, 14}
    assert {m.value for m in E.TargetBasis} == {"ABSOLUTE_EXECUTABLE_RETURN"}
    assert {m.value for m in E.MaturityStatus} == {"MATURED", "NOT_MATURED", "TERMINAL_EVENT"}
    assert {m.value for m in E.ModelProducer} == {
        "BASELINE_GBT", "COMPARATOR_ELASTICNET", "COMPARATOR_FAMA_MACBETH", "PER_DATE_ORACLE"
    }
    assert {m.value for m in E.OutputType} == {"CONTINUOUS_RETURN", "PROBABILITY"}
    assert {m.value for m in E.EvaluationOutcome} == {"EDGE_SUPPORTED", "BLOCKED_NO_EDGE", "INCONCLUSIVE"}
    assert {m.value for m in E.BenchmarkComponent} == {"SPY", "matched_basket"}
    assert {m.value for m in E.FactorName} == {"Mkt", "SMB", "HML", "UMD", "STRev", "BAB"}
    assert {m.value for m in E.EceNotApplicable} == {"NOT_APPLICABLE_TO_PRIMARY_REGRESSION"}


def test_horizon_is_intenum():
    assert issubclass(E.HorizonSessions, enum.IntEnum)


# --- 13,14: closed-enum fields reject bad values -----------------------------

def test_unsupported_horizon_value_rejected():
    with pytest.raises(ValueError):
        E.HorizonSessions(6)


def test_closed_enum_field_rejects_raw_string():
    with pytest.raises((TypeError, ValueError)):
        E.CorporateActionRecord(
            instrument_id="i1", action_type="SPLIT", ex_date=date(2023, 6, 15),
            split_adjustment_factor=Decimal("2"), dividend_amount=Decimal("0"),
            dividend_treatment=E.DividendTreatmentValue("none"),
            corporate_action_version="cav1", source_id="src1",
        )


def test_closed_enum_field_rejects_wrong_enum_type():
    with pytest.raises((TypeError, ValueError)):
        E.RawOHLCVBar(
            instrument_id="i1", session_date=date(2023, 6, 15), open=Decimal("1"),
            high=Decimal("2"), low=Decimal("1"), close=Decimal("2"), volume=1,
            price_basis=E.ActionType.SPLIT, source_id="src1",
        )


def test_horizon_field_rejects_plain_int():
    with pytest.raises((TypeError, ValueError)):
        E.InformationInterval(
            instrument_id="i1", horizon_sessions=6,
            feature_information_start=date(2023, 5, 17),
            prediction_time=datetime(2023, 6, 15, 16),
            label_start=date(2023, 6, 16), label_end=date(2023, 6, 23),
            label_available_at=datetime(2023, 6, 26, 9),
            information_interval=(date(2023, 5, 17), date(2023, 6, 23)),
        )


# --- 15: open placeholders carry no invented vocabulary ----------------------

OPEN_PLACEHOLDERS = [
    "PriceBasisValue", "DividendTreatmentValue", "AssetTypeValue",
    "TerminalEventPolicyValue", "TrialTargetBasisValue",
    "RunLedgerEventTypeValue", "ExitLegValue",
]


@pytest.mark.parametrize("name", OPEN_PLACEHOLDERS)
def test_open_placeholder_is_str_newtype_not_enum(name):
    placeholder = getattr(E, name)
    assert getattr(placeholder, "__supertype__", None) is str
    assert not (isinstance(placeholder, type) and issubclass(placeholder, enum.Enum))


def test_close_auction_constant_only():
    assert str(E.CLOSE_AUCTION) == "CLOSE_AUCTION"
    # No ExitLeg enum exists (exit_leg is an open placeholder).
    assert not hasattr(E, "ExitLeg")


# --- 16: None only for explicitly nullable fields ----------------------------

def test_nullable_fields_accept_none():
    inst = _instances()
    assert inst["InstrumentIdentifierRecord"].valid_to is None
    assert inst["FixedPITCohortMember"].exclusion_reason is None


def test_non_nullable_field_rejects_none():
    with pytest.raises((TypeError, ValueError)):
        E.SourceRecord(
            source_id=None, provider="fixture", endpoint="ohlcv",
            request_params={}, pull_timestamp=datetime(2023, 6, 15),
            is_estimated_timestamp=False, raw_payload_hash="h",
        )


# --- 17,18: decimal / collection representations -----------------------------

def test_decimal_fields_accept_decimal():
    bar = _instances()["RawOHLCVBar"]
    assert isinstance(bar.close, Decimal)
    assert isinstance(_instances()["TerminalEventRecord"].terminal_return, Decimal)


def test_collection_fields_use_tuple_and_mapping():
    inst = _instances()
    assert isinstance(inst["FoldManifest"].train_prediction_times, tuple)
    assert isinstance(inst["BenchmarkDefinition"].components, tuple)
    assert isinstance(inst["InformationInterval"].information_interval, tuple)
    assert isinstance(inst["RuntimeEnvironmentManifest"].data_vintage_ids, tuple)
    assert isinstance(inst["SourceRecord"].request_params, typing.Mapping)
    assert isinstance(inst["FactorAttributionResult"].factor_source_versions, typing.Mapping)
    assert isinstance(inst["RuntimeEnvironmentManifest"].random_seeds, typing.Mapping)


# --- 19,20: construct & immutability -----------------------------------------

@pytest.mark.parametrize("name", ENTITY_CLASS_NAMES)
def test_representative_instance_constructs(name):
    assert isinstance(_instances()[name], _cls(name))


@pytest.mark.parametrize("name", ENTITY_CLASS_NAMES)
def test_instance_is_immutable(name):
    inst = _instances()[name]
    first_field = dataclasses.fields(inst)[0].name
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(inst, first_field, "mutated")
