from __future__ import annotations

import pytest

from devtoolbox import encoding


def test_base64_round_trip() -> None:
    encoded = encoding.encode_base64(b"hello")
    assert encoded == "aGVsbG8="
    assert encoding.decode_base64(encoded) == b"hello"


def test_base64_urlsafe_alphabet() -> None:
    data = b"\xfb\xff"
    assert encoding.encode_base64(data) == "+/8="
    assert encoding.encode_base64(data, urlsafe=True) == "-_8="
    assert encoding.decode_base64("-_8=", urlsafe=True) == data


def test_base64_accepts_missing_padding_and_whitespace() -> None:
    assert encoding.decode_base64("aGVs bG8") == b"hello"


def test_base64_invalid_input() -> None:
    with pytest.raises(ValueError, match="invalid base64"):
        encoding.decode_base64("!!!!")


def test_hex_round_trip() -> None:
    assert encoding.encode_hex(b"hello") == "68656c6c6f"
    assert encoding.decode_hex("68 65 6c 6c 6f") == b"hello"


def test_hex_invalid_input() -> None:
    with pytest.raises(ValueError, match="invalid hex"):
        encoding.decode_hex("zz")


def test_url_encode_decode() -> None:
    assert encoding.url_encode("a b/c") == "a%20b%2Fc"
    assert encoding.url_decode("a%20b%2Fc") == "a b/c"


def test_url_form_encoding() -> None:
    assert encoding.url_encode("a b/c", plus=True) == "a+b%2Fc"
    assert encoding.url_decode("a+b%2Fc", plus=True) == "a b/c"


def test_url_unicode_round_trip() -> None:
    assert encoding.url_decode(encoding.url_encode("café")) == "café"
