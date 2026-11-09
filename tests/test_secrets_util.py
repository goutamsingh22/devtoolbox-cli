from __future__ import annotations

import base64
import string

import pytest

from devtoolbox import secrets_util


def _decode_token(token: str) -> bytes:
    padded = token + "=" * (-len(token) % 4)
    return base64.urlsafe_b64decode(padded)


def test_generate_password_length() -> None:
    assert len(secrets_util.generate_password(32)) == 32


def test_generate_password_contains_every_class() -> None:
    password = secrets_util.generate_password(64)
    assert any(char in string.ascii_lowercase for char in password)
    assert any(char in string.ascii_uppercase for char in password)
    assert any(char in string.digits for char in password)
    assert any(char in secrets_util.SYMBOLS for char in password)


def test_generate_password_respects_disabled_classes() -> None:
    password = secrets_util.generate_password(64, symbols=False, digits=False, upper=False)
    assert all(char in string.ascii_lowercase for char in password)


def test_exclude_ambiguous_characters() -> None:
    password = secrets_util.generate_password(128, exclude_ambiguous=True)
    assert not set(password) & set(secrets_util.AMBIGUOUS)


def test_length_must_cover_every_enabled_class() -> None:
    with pytest.raises(ValueError, match="at least 4"):
        secrets_util.generate_password(3)


def test_no_character_classes_raises() -> None:
    with pytest.raises(ValueError, match="at least one character class"):
        secrets_util.generate_password(10, symbols=False, digits=False, upper=False, lower=False)


def test_password_entropy_grows_with_length() -> None:
    short = secrets_util.password_entropy(10)
    long = secrets_util.password_entropy(20)
    assert long == pytest.approx(short * 2)


def test_urlsafe_token_length() -> None:
    token = secrets_util.generate_token(16)
    assert len(_decode_token(token)) == 16


def test_hex_token_length() -> None:
    token = secrets_util.generate_token(16, use_hex=True)
    assert len(token) == 32
    int(token, 16)


def test_token_rejects_empty_size() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        secrets_util.generate_token(0)
