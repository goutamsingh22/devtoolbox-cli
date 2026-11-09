from __future__ import annotations

import base64
import json

import pytest

from devtoolbox import jwtutil


def _encode(value: dict) -> str:
    raw = json.dumps(value).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def make_token(header: dict, payload: dict, signature: str = "signature") -> str:
    return f"{_encode(header)}.{_encode(payload)}.{signature}"


def test_decode_three_segment_token() -> None:
    token = make_token({"alg": "HS256", "typ": "JWT"}, {"sub": "123", "admin": True})
    decoded = jwtutil.decode(token)
    assert decoded.header == {"alg": "HS256", "typ": "JWT"}
    assert decoded.payload == {"sub": "123", "admin": True}
    assert decoded.signature == "signature"


def test_decode_two_segment_token() -> None:
    token = f"{_encode({'alg': 'none'})}.{_encode({'sub': '123'})}"
    decoded = jwtutil.decode(token)
    assert decoded.signature is None
    assert decoded.payload == {"sub": "123"}


def test_wrong_segment_count() -> None:
    with pytest.raises(ValueError, match="two or three"):
        jwtutil.decode("only-one-segment")


def test_invalid_base64_segment() -> None:
    with pytest.raises(ValueError, match="not valid base64url"):
        jwtutil.decode("!!!.???")


def test_invalid_json_segment() -> None:
    with pytest.raises(ValueError, match="not valid JSON"):
        jwtutil.decode("bm90LWpzb24.e30")


def test_non_object_payload() -> None:
    token = f"{_encode({'alg': 'none'})}.{_encode_list([1, 2, 3])}"
    with pytest.raises(ValueError, match="JSON objects"):
        jwtutil.decode(token)


def _encode_list(value: list) -> str:
    raw = json.dumps(value).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
