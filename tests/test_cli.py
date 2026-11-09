from __future__ import annotations

import base64
import json

from devtoolbox import __version__, hashing


def _encode(value: dict) -> str:
    raw = json.dumps(value).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _jwt() -> str:
    return f"{_encode({'alg': 'HS256', 'typ': 'JWT'})}.{_encode({'sub': '42'})}.signature"


def _decode_token(token: str) -> bytes:
    padded = token + "=" * (-len(token) % 4)
    return base64.urlsafe_b64decode(padded)


def test_global_version_flag(run) -> None:
    result = run("--version")
    assert result.exit_code == 0
    assert __version__ in result.output


def test_version_command(run) -> None:
    result = run("version")
    assert result.exit_code == 0
    assert result.output.strip() == f"devtoolbox {__version__}"


def test_help_lists_commands(run) -> None:
    result = run("--help")
    assert result.exit_code == 0
    for command in ("hash", "base64", "json", "password", "jwt", "ip"):
        assert command in result.output


def test_short_help_flag(run) -> None:
    result = run("-h")
    assert result.exit_code == 0
    assert "Commands" in result.output


def test_hash_text(run) -> None:
    result = run("hash", "hello")
    assert result.exit_code == 0
    assert result.output.strip() == hashing.hash_text("hello")


def test_hash_algorithm(run) -> None:
    result = run("hash", "hello", "--algorithm", "md5")
    assert result.exit_code == 0
    assert result.output.strip() == hashing.hash_text("hello", "md5")


def test_hash_from_stdin(run) -> None:
    result = run("hash", input="hello")
    assert result.exit_code == 0
    assert result.output.strip() == hashing.hash_text("hello")


def test_hash_file(run, tmp_path) -> None:
    target = tmp_path / "data.txt"
    target.write_text("hello", encoding="utf-8")
    result = run("hash", "--file", target)
    assert result.exit_code == 0
    assert result.output.strip() == hashing.hash_text("hello")


def test_hash_all_algorithms(run) -> None:
    result = run("hash", "hello", "--all")
    assert result.exit_code == 0
    assert "sha256:" in result.output
    assert "md5:" in result.output


def test_hash_rejects_text_and_file(run, tmp_path) -> None:
    target = tmp_path / "data.txt"
    target.write_text("hello", encoding="utf-8")
    result = run("hash", "hello", "--file", target)
    assert result.exit_code != 0


def test_hash_unknown_algorithm(run) -> None:
    result = run("hash", "hello", "--algorithm", "nope")
    assert result.exit_code == 1
    assert "Error" in result.output


def test_uuid_count(run) -> None:
    result = run("uuid", "--count", "3")
    assert result.exit_code == 0
    lines = result.output.strip().splitlines()
    assert len(lines) == 3
    assert all(len(line) == 36 for line in lines)


def test_uuid_no_dashes_and_upper(run) -> None:
    result = run("uuid", "--no-dashes", "--upper")
    assert result.exit_code == 0
    value = result.output.strip()
    assert len(value) == 32
    assert value == value.upper()
    assert "-" not in value


def test_uuid_invalid_version(run) -> None:
    result = run("uuid", "--version", "5")
    assert result.exit_code != 0


def test_base64_round_trip(run) -> None:
    encoded = run("base64", "hello")
    assert encoded.exit_code == 0
    assert encoded.output.strip() == "aGVsbG8="

    decoded = run("base64", "--decode", "aGVsbG8=")
    assert decoded.exit_code == 0
    assert decoded.output.strip() == "hello"


def test_base64_urlsafe(run) -> None:
    encoded = run("base64", "???", "--urlsafe")
    assert encoded.output.strip() == "Pz8_"
    decoded = run("base64", "--decode", "Pz8_", "--urlsafe")
    assert decoded.output.strip() == "???"


def test_base64_binary_decode_fails_cleanly(run) -> None:
    result = run("base64", "--decode", "--urlsafe", input="-_8=")
    assert result.exit_code == 1
    assert "Error" in result.output


def test_base64_invalid_input(run) -> None:
    result = run("base64", "--decode", "!!!!")
    assert result.exit_code == 1
    assert "Error" in result.output


def test_base64_file(run, tmp_path) -> None:
    target = tmp_path / "data.txt"
    target.write_text("hello", encoding="utf-8")
    result = run("base64", "--file", target)
    assert result.exit_code == 0
    assert result.output.strip() == "aGVsbG8="


def test_url_encode_decode(run) -> None:
    encoded = run("url", "a b/c")
    assert encoded.exit_code == 0
    assert encoded.output.strip() == "a%20b%2Fc"

    decoded = run("url", "--decode", "a%20b%2Fc")
    assert decoded.exit_code == 0
    assert decoded.output.strip() == "a b/c"


def test_url_plus(run) -> None:
    result = run("url", "a b", "--plus")
    assert result.output.strip() == "a+b"


def test_hex_round_trip(run) -> None:
    encoded = run("hex", "hello")
    assert encoded.output.strip() == "68656c6c6f"
    decoded = run("hex", "--decode", "68656c6c6f")
    assert decoded.output.strip() == "hello"


def test_hex_invalid(run) -> None:
    result = run("hex", "--decode", "zz")
    assert result.exit_code == 1


def test_json_pretty_and_minify(run) -> None:
    pretty = run("json", '{"b": 1, "a": 2}')
    assert pretty.exit_code == 0
    assert '"a": 2' in pretty.output

    minified = run("json", '{"b": 1, "a": 2}', "--sort-keys", "--minify")
    assert minified.output.strip() == '{"a":2,"b":1}'


def test_json_check(run) -> None:
    result = run("json", '{"a": 1}', "--check")
    assert result.exit_code == 0
    assert result.output.strip() == "valid"


def test_json_invalid(run) -> None:
    result = run("json", "{", "--check")
    assert result.exit_code == 1
    assert "Error" in result.output


def test_json_file(run, tmp_path) -> None:
    target = tmp_path / "data.json"
    target.write_text('{"a": 1}', encoding="utf-8")
    result = run("json", "--file", target, "--minify")
    assert result.output.strip() == '{"a":1}'


def test_timestamp_epoch_to_iso(run) -> None:
    result = run("timestamp", "0")
    assert result.exit_code == 0
    assert result.output.strip() == "1970-01-01T00:00:00+00:00"


def test_timestamp_iso_to_epoch(run) -> None:
    result = run("timestamp", "1970-01-01T00:00:00Z")
    assert result.exit_code == 0
    assert result.output.strip() == "0"


def test_timestamp_milliseconds(run) -> None:
    result = run("timestamp", "1000", "--ms")
    assert result.exit_code == 0
    assert result.output.strip() == "1970-01-01T00:00:01+00:00"


def test_timestamp_now(run) -> None:
    result = run("timestamp")
    assert result.exit_code == 0
    value = int(result.output.strip())
    assert value > 1_600_000_000


def test_timestamp_invalid_unit(run) -> None:
    result = run("timestamp", "0", "--unit", "weeks")
    assert result.exit_code != 0


def test_timestamp_invalid_date(run) -> None:
    result = run("timestamp", "not-a-date")
    assert result.exit_code == 1


def test_password_length(run) -> None:
    result = run("password", "--length", "32")
    assert result.exit_code == 0
    assert len(result.output.strip()) == 32


def test_password_count(run) -> None:
    result = run("password", "--count", "3", "--length", "16")
    assert len(result.output.strip().splitlines()) == 3


def test_password_json(run) -> None:
    result = run("password", "--length", "16", "--json")
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert len(payload) == 1
    assert len(payload[0]["password"]) == 16
    assert payload[0]["entropy_bits"] > 0


def test_password_too_short(run) -> None:
    result = run("password", "--length", "2")
    assert result.exit_code == 1


def test_password_no_classes(run) -> None:
    result = run(
        "password",
        "--no-symbols",
        "--no-digits",
        "--no-upper",
        "--no-lower",
    )
    assert result.exit_code == 1
    assert "Error" in result.output


def test_token_urlsafe(run) -> None:
    result = run("token", "--bytes", "16")
    assert result.exit_code == 0
    assert len(_decode_token(result.output.strip())) == 16


def test_token_hex(run) -> None:
    result = run("token", "--bytes", "8", "--hex")
    assert result.exit_code == 0
    value = result.output.strip()
    assert len(value) == 16
    int(value, 16)


def test_token_count(run) -> None:
    result = run("token", "--count", "2")
    assert len(result.output.strip().splitlines()) == 2


def test_case_default_snake(run) -> None:
    result = run("case", "HelloWorld")
    assert result.exit_code == 0
    assert result.output.strip() == "hello_world"


def test_case_camel(run) -> None:
    result = run("case", "hello world", "--to", "camel")
    assert result.output.strip() == "helloWorld"


def test_case_multiple_lines_and_file(run, tmp_path) -> None:
    target = tmp_path / "names.txt"
    target.write_text("HelloWorld\nfoo_bar\n", encoding="utf-8")
    result = run("case", "--file", target, "--to", "kebab")
    assert result.output.strip().splitlines() == ["hello-world", "foo-bar"]


def test_slug(run) -> None:
    result = run("slug", "Hello, World! Café")
    assert result.exit_code == 0
    assert result.output.strip() == "hello-world-cafe"


def test_slug_custom_separator(run) -> None:
    result = run("slug", "Hello World", "--separator", "_")
    assert result.output.strip() == "hello_world"


def test_color_plain(run) -> None:
    result = run("color", "#ff0000")
    assert result.exit_code == 0
    assert "hex: #ff0000" in result.output
    assert "rgb: 255, 0, 0" in result.output


def test_color_json(run) -> None:
    result = run("color", "rgb(0, 128, 255)", "--json")
    payload = json.loads(result.output)
    assert payload["hex"] == "#0080ff"
    assert payload["rgb"] == [0, 128, 255]


def test_color_invalid(run) -> None:
    result = run("color", "#12")
    assert result.exit_code == 1


def test_jwt_decode(run) -> None:
    result = run("jwt", _jwt(), "--quiet")
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["header"]["alg"] == "HS256"
    assert payload["payload"]["sub"] == "42"
    assert payload["signature"] == "signature"


def test_jwt_payload_only(run) -> None:
    result = run("jwt", _jwt(), "--payload-only", "--quiet")
    assert json.loads(result.output) == {"sub": "42"}


def test_jwt_warns_by_default(run) -> None:
    result = run("jwt", _jwt())
    assert result.exit_code == 0
    assert "NOT verified" in result.output


def test_jwt_invalid(run) -> None:
    result = run("jwt", "not-a-jwt", "--quiet")
    assert result.exit_code == 1


def test_ip_json(run) -> None:
    result = run("ip", "192.168.1.10/24", "--json")
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["network"] == "192.168.1.0/24"
    assert payload["num_addresses"] == 256


def test_ip_plain(run) -> None:
    result = run("ip", "::1")
    assert result.exit_code == 0
    assert "version: 6" in result.output
    assert "is_loopback: yes" in result.output


def test_ip_invalid(run) -> None:
    result = run("ip", "not-an-ip")
    assert result.exit_code == 1
