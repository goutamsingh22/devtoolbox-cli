from __future__ import annotations

import json

import pytest

from devtoolbox import jsonutil


def test_loads_and_dumps_round_trip() -> None:
    value = {"name": "café", "items": [1, 2, 3]}
    assert jsonutil.loads(jsonutil.dumps(value)) == value


def test_unicode_is_not_escaped() -> None:
    assert "café" in jsonutil.dumps({"name": "café"})


def test_minify_removes_whitespace() -> None:
    assert jsonutil.dumps({"a": 1, "b": 2}, minify=True) == '{"a":1,"b":2}'


def test_sort_keys() -> None:
    assert jsonutil.dumps({"b": 1, "a": 2}, minify=True, sort_keys=True) == '{"a":2,"b":1}'


def test_indent_controls_layout() -> None:
    rendered = jsonutil.dumps({"a": 1}, indent=4)
    assert '\n    "a": 1' in rendered


def test_invalid_json_raises() -> None:
    with pytest.raises(json.JSONDecodeError):
        jsonutil.loads("{")
