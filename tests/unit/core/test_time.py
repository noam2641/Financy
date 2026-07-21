"""Specification tests for exchange-session counting.

TASK-R0-01 · FN-R0-12 (financy.core.time.count_exchange_sessions)
Requirement R0-REQ-18 · Test T-R0-018 · worked examples VAL-R0-01.
Owner decisions ADR-001, ADR-013.

Deterministic and offline: the pinned session sequence and calendar identity
come from the committed fixture tests/fixtures/calendars/xnys_2023_sessions.json
— no network, no live calendar, no current-date lookup.

FN-R0-12 lists `calendar_id` as a reproducibility field, so the ExchangeCalendar
surface must preserve a pinned calendar identity, not only the session sequence.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Sequence

import pytest

from financy.core.time import (
    CalendarRangeError,
    InvalidCalendarDefinitionError,
    NotASessionError,
    UnsupportedHorizonError,
    count_exchange_sessions,
)

_FIXTURE = (
    Path(__file__).resolve().parents[3]
    / "tests"
    / "fixtures"
    / "calendars"
    / "xnys_2023_sessions.json"
)


def _load_payload() -> dict:
    return json.loads(_FIXTURE.read_text())


def _load_sessions() -> list[date]:
    return [date.fromisoformat(s) for s in _load_payload()["sessions"]]


class _FixtureCalendar:
    """Minimal concrete ExchangeCalendar backed by the committed fixture.

    Carries the pinned `calendar_id` (reproducibility field) alongside the
    ascending `sessions`. An anonymous/empty identity is rejected at the
    construction boundary rather than silently accepted.
    """

    def __init__(self, calendar_id: str, sessions: Sequence[date]):
        if not isinstance(calendar_id, str) or not calendar_id.strip():
            raise InvalidCalendarDefinitionError(
                "calendar_id must be a non-empty string"
            )
        self._calendar_id = calendar_id
        self._sessions = list(sessions)

    @property
    def calendar_id(self) -> str:
        return self._calendar_id

    @property
    def sessions(self) -> Sequence[date]:
        return self._sessions


@pytest.fixture
def calendar() -> _FixtureCalendar:
    payload = _load_payload()
    sessions = [date.fromisoformat(s) for s in payload["sessions"]]
    return _FixtureCalendar(payload["calendar_id"], sessions)


# --- T-R0-018 golden assertions (VAL-R0-01 worked examples) ------------------

@pytest.mark.parametrize(
    "horizon, expected",
    [
        (5, date(2023, 6, 23)),
        (8, date(2023, 6, 28)),
        (14, date(2023, 7, 7)),
    ],
)
def test_golden_horizons_from_2023_06_15(calendar, horizon, expected):
    # start = decision session t = 2023-06-15; entry at t+1 open; t+1 counts as 1.
    assert count_exchange_sessions(date(2023, 6, 15), horizon, calendar) == expected


def test_juneteenth_and_independence_day_are_skipped(calendar):
    # 2023-06-19 (Juneteenth) sits between t+1 and t+2; 2023-07-04 between +11/+12.
    assert date(2023, 6, 19) not in calendar.sessions
    assert date(2023, 7, 4) not in calendar.sessions


# --- General offset (not hard-coded to a single start) -----------------------

def test_general_offset_from_a_different_start(calendar):
    # start = 2023-06-16; +1 06-20, +2 06-21, +3 06-22, +4 06-23, +5 06-26.
    assert count_exchange_sessions(date(2023, 6, 16), 5, calendar) == date(2023, 6, 26)


# --- Fail-closed behaviour ---------------------------------------------------

@pytest.mark.parametrize("bad_horizon", [1, 6, 10, 13, 15, 0, -5])
def test_unsupported_horizon_raises(calendar, bad_horizon):
    with pytest.raises(UnsupportedHorizonError):
        count_exchange_sessions(date(2023, 6, 15), bad_horizon, calendar)


@pytest.mark.parametrize(
    "non_session",
    [date(2023, 6, 17), date(2023, 6, 19), date(2023, 7, 4)],  # weekend, Juneteenth, July 4
)
def test_non_session_start_raises(calendar, non_session):
    with pytest.raises(NotASessionError):
        count_exchange_sessions(non_session, 5, calendar)


def test_insufficient_calendar_range_fails_closed():
    # Truncate the calendar so t+14 from 2023-06-15 (2023-07-07) is unreachable.
    payload = _load_payload()
    sessions = [d for d in _load_sessions() if d <= date(2023, 6, 30)]
    calendar = _FixtureCalendar(payload["calendar_id"], sessions)
    with pytest.raises(CalendarRangeError):
        count_exchange_sessions(date(2023, 6, 15), 14, calendar)


# --- Reproducibility: pinned calendar identity (FN-R0-12 calendar_id) --------

def test_calendar_exposes_pinned_identity(calendar):
    assert calendar.calendar_id == "XNYS-2023-fixture"


def test_repeated_calls_do_not_mutate_calendar_id(calendar):
    before = calendar.calendar_id
    count_exchange_sessions(date(2023, 6, 15), 5, calendar)
    count_exchange_sessions(date(2023, 6, 15), 14, calendar)
    assert calendar.calendar_id == before == "XNYS-2023-fixture"


def test_repeated_calls_do_not_mutate_sessions(calendar):
    before = list(calendar.sessions)
    count_exchange_sessions(date(2023, 6, 15), 5, calendar)
    count_exchange_sessions(date(2023, 6, 15), 14, calendar)
    assert list(calendar.sessions) == before


@pytest.mark.parametrize("bad_id", ["", "   ", "\t"])
def test_empty_calendar_id_rejected_at_construction(bad_id):
    with pytest.raises(InvalidCalendarDefinitionError):
        _FixtureCalendar(bad_id, _load_sessions())


# --- Purity / determinism ----------------------------------------------------

def test_repeated_calls_are_identical(calendar):
    a = count_exchange_sessions(date(2023, 6, 15), 8, calendar)
    b = count_exchange_sessions(date(2023, 6, 15), 8, calendar)
    assert a == b == date(2023, 6, 28)


def test_input_calendar_is_not_mutated(calendar):
    before = list(calendar.sessions)
    count_exchange_sessions(date(2023, 6, 15), 14, calendar)
    assert list(calendar.sessions) == before
