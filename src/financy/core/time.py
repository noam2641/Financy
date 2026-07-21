"""Exchange-session counting.

TASK-R0-01 · FN-R0-12 (financy.core.time.count_exchange_sessions)
Covers R0-REQ-18; verified by T-R0-018; worked examples defined in VAL-R0-01.
Owner decisions: ADR-001 (build order + validation methodology), ADR-013
(validation applicability). Pure, deterministic, offline; no network, no
current-date lookup, no local-timezone use, no provider call.
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
    """Return the date of session ``t + horizon`` (FN-R0-12).

    ``start`` is decision session ``t``; entry occurs at the open of session
    ``t+1``, which counts as session 1, so a horizon ``H`` resolves to the
    ``H``-th session strictly after ``t`` (i.e. ``sessions[index(t) + H]``).

    Args:
        start: The decision session date ``t`` (must be an exchange session).
        horizon: One of :data:`SUPPORTED_HORIZONS` (5, 8, or 14).
        calendar: An :class:`ExchangeCalendar` whose ``sessions`` is the
            ascending sequence of trading-session dates. It is read only,
            never mutated.

    Returns:
        The date of session ``t + horizon``.

    Raises:
        UnsupportedHorizonError: ``horizon`` is not in SUPPORTED_HORIZONS.
        NotASessionError: ``start`` is not a session on ``calendar``.
        CalendarRangeError: the calendar does not reach session ``t+horizon``.
    """
    if horizon not in SUPPORTED_HORIZONS:
        raise UnsupportedHorizonError(
            f"horizon {horizon!r} is not supported; expected one of {SUPPORTED_HORIZONS}"
        )

    # Read once; do not mutate the caller's calendar.
    sessions: Sequence[date] = calendar.sessions

    start_index = _index_of(sessions, start)
    if start_index is None:
        raise NotASessionError(f"{start.isoformat()} is not an exchange session")

    target_index = start_index + horizon
    if target_index >= len(sessions):
        raise CalendarRangeError(
            f"calendar does not reach session t+{horizon} from {start.isoformat()}"
        )
    return sessions[target_index]


def _index_of(sessions: Sequence[date], day: date) -> int | None:
    """Return the index of ``day`` in ``sessions`` (ascending), or None."""
    for index, session in enumerate(sessions):
        if session == day:
            return index
    return None
