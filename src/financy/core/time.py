"""Exchange-session counting.

TASK-R0-01 · FN-R0-12 (financy.core.time.count_exchange_sessions)
Covers R0-REQ-18; verified by T-R0-018; worked examples defined in VAL-R0-01.
Owner decisions: ADR-001 (build order + validation methodology), ADR-013
(validation applicability). Pure, deterministic, offline; no network, no
current-date lookup, no local-timezone use, no provider call.

NOTE: scaffold commit — `count_exchange_sessions` is a stub raising
NotImplementedError so the specification tests fail first; the implementation
lands in the following commit.
"""

from __future__ import annotations

from datetime import date
from typing import Protocol, Sequence, runtime_checkable

#: Exactly the Release-0 swing horizons (readiness gate R0-S4; FN-R0-12).
SUPPORTED_HORIZONS: tuple[int, ...] = (5, 8, 14)


@runtime_checkable
class ExchangeCalendar(Protocol):
    """Smallest calendar surface FN-R0-12 requires.

    `sessions` is the ascending sequence of trading-session dates. The counting
    function reads it and never mutates it. Adapters from an approved live
    calendar source are a later task, not TASK-R0-01.
    """

    @property
    def sessions(self) -> Sequence[date]:
        ...


class CalendarRangeError(Exception):
    """Raised when the calendar does not reach session t+H (fail closed)."""


class NotASessionError(ValueError):
    """Raised when `start` is not an exchange session on the calendar."""


class UnsupportedHorizonError(ValueError):
    """Raised when `horizon` is not one of SUPPORTED_HORIZONS."""


def count_exchange_sessions(
    start: date,
    horizon: int,
    calendar: ExchangeCalendar,
) -> date:
    """Return the date of session t+H (stub — see module note)."""
    raise NotImplementedError("TASK-R0-01: implemented in the following commit")
