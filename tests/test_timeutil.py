from __future__ import annotations

from datetime import timedelta, timezone

import pytest

from devtoolbox import timeutil


def test_is_epoch() -> None:
    assert timeutil.is_epoch("1704067200")
    assert timeutil.is_epoch("-5")
    assert timeutil.is_epoch("1.5")
    assert not timeutil.is_epoch("2024-01-01")
    assert not timeutil.is_epoch("abc")


def test_epoch_to_datetime_seconds() -> None:
    moment = timeutil.epoch_to_datetime(0)
    assert moment.isoformat() == "1970-01-01T00:00:00+00:00"
    assert moment.tzinfo is timezone.utc


def test_epoch_to_datetime_milliseconds() -> None:
    moment = timeutil.epoch_to_datetime(1000, milliseconds=True)
    assert moment.isoformat() == "1970-01-01T00:00:01+00:00"


def test_parse_datetime_accepts_z_suffix() -> None:
    moment = timeutil.parse_datetime("2024-01-01T00:00:00Z")
    assert moment.isoformat() == "2024-01-01T00:00:00+00:00"


def test_parse_datetime_attaches_default_timezone() -> None:
    moment = timeutil.parse_datetime("2024-01-01T00:00:00")
    assert moment.tzinfo is not None
    assert moment.utcoffset() == timedelta(0)


def test_to_epoch_round_trip() -> None:
    moment = timeutil.parse_datetime("2024-01-01T00:00:00Z")
    assert timeutil.to_epoch(moment) == 1704067200
    assert timeutil.to_epoch(moment, milliseconds=True) == 1704067200000


def test_parse_datetime_invalid() -> None:
    with pytest.raises(ValueError, match="invalid ISO-8601"):
        timeutil.parse_datetime("not-a-date")


def test_parse_datetime_empty() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        timeutil.parse_datetime("  ")
