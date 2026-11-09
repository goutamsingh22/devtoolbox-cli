from __future__ import annotations

import hashlib

import pytest

from devtoolbox import hashing

HELLO_SHA256 = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
HELLO_MD5 = "5d41402abc4b2a76b9719d911017c592"


def test_known_digests() -> None:
    assert hashing.hash_text("hello") == HELLO_SHA256
    assert hashing.hash_text("hello", "md5") == HELLO_MD5
    assert hashing.hash_bytes(b"hello", "sha1") == hashlib.sha1(b"hello").hexdigest()


def test_algorithm_is_case_insensitive() -> None:
    assert hashing.hash_text("hello", "SHA256") == HELLO_SHA256


def test_unknown_algorithm_raises() -> None:
    with pytest.raises(ValueError, match="unknown algorithm"):
        hashing.hash_text("hello", "not-a-hash")


def test_shake_algorithms_are_rejected() -> None:
    with pytest.raises(ValueError, match="unknown algorithm"):
        hashing.hash_text("hello", "shake_128")


def test_hash_file(tmp_path) -> None:
    target = tmp_path / "data.txt"
    target.write_text("hello", encoding="utf-8")
    assert hashing.hash_file(target) == HELLO_SHA256
    assert hashing.hash_file(str(target), "md5") == HELLO_MD5


def test_hash_text_all_matches_hashlib() -> None:
    digests = hashing.hash_text_all("hello", ["sha256", "md5"])
    assert digests == {"sha256": HELLO_SHA256, "md5": HELLO_MD5}


def test_hash_text_all_defaults_to_every_algorithm() -> None:
    digests = hashing.hash_text_all("hello")
    assert set(digests) == set(hashing.ALGORITHMS)


def test_hash_file_all(tmp_path) -> None:
    target = tmp_path / "data.bin"
    target.write_bytes(b"hello" * 1000)
    digests = hashing.hash_file_all(target, ["sha256", "sha512"])
    assert digests["sha256"] == hashlib.sha256(target.read_bytes()).hexdigest()
    assert digests["sha512"] == hashlib.sha512(target.read_bytes()).hexdigest()
