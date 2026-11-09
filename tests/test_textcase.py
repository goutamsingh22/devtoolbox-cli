from __future__ import annotations

import pytest

from devtoolbox import textcase


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("hello world", ["hello", "world"]),
        ("helloWorld", ["hello", "World"]),
        ("HelloWorld", ["Hello", "World"]),
        ("HTTPServer", ["HTTP", "Server"]),
        ("hello_world-again", ["hello", "world", "again"]),
        ("  spaced   out  ", ["spaced", "out"]),
    ],
)
def test_split_words(value: str, expected: list[str]) -> None:
    assert textcase.split_words(value) == expected


def test_convert_styles() -> None:
    assert textcase.convert("HelloWorld", "snake") == "hello_world"
    assert textcase.convert("HelloWorld", "kebab") == "hello-world"
    assert textcase.convert("HelloWorld", "dot") == "hello.world"
    assert textcase.convert("HelloWorld", "constant") == "HELLO_WORLD"
    assert textcase.convert("hello world", "camel") == "helloWorld"
    assert textcase.convert("hello world", "pascal") == "HelloWorld"
    assert textcase.convert("hello world", "title") == "Hello World"
    assert textcase.convert("hello", "upper") == "HELLO"
    assert textcase.convert("HELLO", "lower") == "hello"


def test_convert_handles_acronyms() -> None:
    assert textcase.to_snake("HTTPServer") == "http_server"
    assert textcase.to_camel("HTTP_server") == "httpServer"


def test_convert_unknown_style() -> None:
    with pytest.raises(ValueError, match="unknown case style"):
        textcase.convert("hello", "weird")


def test_slugify() -> None:
    assert textcase.slugify("Hello, World!") == "hello-world"
    assert textcase.slugify("Café déjà vu") == "cafe-deja-vu"
    assert textcase.slugify("Hello World", separator="_") == "hello_world"


def test_slugify_empty_separator() -> None:
    with pytest.raises(ValueError, match="separator"):
        textcase.slugify("hello", separator="")
