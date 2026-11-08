# DevToolbox CLI

[![CI](https://github.com/goutamsingh22/devtoolbox-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/goutamsingh22/devtoolbox-cli/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/devtoolbox-cli.svg)](https://pypi.org/project/devtoolbox-cli/)
[![Python versions](https://img.shields.io/pypi/pyversions/devtoolbox-cli.svg)](https://pypi.org/project/devtoolbox-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

One command-line toolbox for the small tasks that interrupt real work: hashing a
file, decoding a JWT, converting a timestamp, generating a token, pretty-printing
JSON. No context switching, no throwaway snippets.

## Features

| Command | What it does |
| --- | --- |
| `hash` | Hash text, stdin or a file with any `hashlib` algorithm (or all of them). |
| `uuid` | Generate UUID v4 (random) or v1 (time-based), with formatting options. |
| `base64` | Encode/decode standard or URL-safe base64. |
| `url` | Percent-encode/decode text, with optional form (`+`) encoding. |
| `hex` | Encode/decode hexadecimal. |
| `json` | Validate, pretty-print, minify or sort JSON. |
| `timestamp` | Convert between epoch seconds/milliseconds and ISO-8601. |
| `password` | Generate secure passwords with per-class guarantees and entropy output. |
| `token` | Generate URL-safe or hexadecimal random tokens. |
| `case` | Convert between snake, kebab, dot, camel, pascal, constant, title and upper/lower. |
| `slug` | Turn text into a URL-friendly slug (Unicode-aware). |
| `color` | Convert colours between hex, RGB and HSL. |
| `jwt` | Decode JWT headers and claims (signature is **not** verified). |
| `ip` | Inspect IP addresses and CIDR interfaces. |

All randomness comes from Python's [`secrets`](https://docs.python.org/3/library/secrets.html)
module or `uuid4`, never from `random`. The text-processing commands (`hash`,
`base64`, `url`, `hex`, `json`, `case`, `slug`) accept piped stdin, and
`--json` is available where structured output makes sense.

## Installation

```bash
pip install devtoolbox-cli
```

Or install it as an isolated tool with [pipx](https://pipx.pypa.io/):

```bash
pipx install devtoolbox-cli
```

From source:

```bash
git clone https://github.com/goutamsingh22/devtoolbox-cli.git
cd devtoolbox-cli
pip install .
```

Requires Python 3.9 or newer.

## Quick start

```bash
$ devtoolbox hash hello
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

$ devtoolbox base64 --decode aGVsbG8=
hello

$ devtoolbox timestamp 1704067200
2024-01-01T00:00:00+00:00

$ devtoolbox password --length 24
x7#Qm2p!vR8@tL4nZc9wBf6K
```

Run `devtoolbox --help` or `devtoolbox <command> --help` for every option.

## Commands

### `hash`

```bash
devtoolbox hash "hello world"
devtoolbox hash --file release.tar.gz --algorithm sha512
devtoolbox hash "hello" --all          # every guaranteed hashlib algorithm
echo "hello" | devtoolbox hash         # reads stdin
```

### `uuid`

```bash
devtoolbox uuid                        # one v4 UUID
devtoolbox uuid --count 5
devtoolbox uuid --version 1            # time-based; exposes host MAC address
devtoolbox uuid --no-dashes --upper
```

### `base64`, `url`, `hex`

```bash
devtoolbox base64 "hello"              # aGVsbG8=
devtoolbox base64 --decode aGVsbG8=
devtoolbox base64 --urlsafe "???"      # Pz8_
devtoolbox url "a b/c"                 # a%20b%2Fc
devtoolbox url --decode "a%20b%2Fc"
devtoolbox url --plus "a b"            # a+b
devtoolbox hex "hello"                 # 68656c6c6f
devtoolbox hex --decode 68656c6c6f
```

Both `base64` and `hex` accept `--file` and `--encoding`.

### `json`

```bash
devtoolbox json '{"b": 1, "a": 2}' --sort-keys
devtoolbox json --file api-response.json --minify
devtoolbox json '{"a": 1}' --check     # prints "valid" or an error
cat data.json | devtoolbox json --minify
```

> Windows PowerShell 5.1 strips double quotes from native-command arguments. Use
> `--file`, pipe the JSON through stdin, or call `devtoolbox` from `cmd.exe`/PowerShell 7
> when passing inline JSON.

### `timestamp`

```bash
devtoolbox timestamp                   # current epoch seconds
devtoolbox timestamp 1704067200        # epoch -> ISO-8601
devtoolbox timestamp 2024-01-01T00:00:00Z
devtoolbox timestamp 1704067200000 --ms
devtoolbox timestamp --local 1704067200
```

### `password` and `token`

```bash
devtoolbox password --length 32 --count 5
devtoolbox password --exclude-ambiguous
devtoolbox password --no-symbols --json
devtoolbox token --bytes 32            # URL-safe token
devtoolbox token --bytes 16 --hex
```

A password is guaranteed to contain at least one character from each enabled
class. `--json` reports the theoretical entropy in bits.

### `case` and `slug`

```bash
devtoolbox case "HelloWorld" --to snake       # hello_world
devtoolbox case "hello world" --to camel      # helloWorld
devtoolbox case "hello world" --to constant   # HELLO_WORLD
devtoolbox slug "Hello, World! Café"          # hello-world-cafe
devtoolbox slug "Hello World" --separator _
```

Styles: `snake`, `kebab`, `dot`, `constant`, `camel`, `pascal`, `title`,
`upper`, `lower`.

### `color`

```bash
devtoolbox color "#3498db"
devtoolbox color "rgb(52, 152, 219)" --json
```

### `jwt`

```bash
devtoolbox jwt "$TOKEN"
devtoolbox jwt "$TOKEN" --payload-only
devtoolbox jwt "$TOKEN" --quiet        # suppress the verification warning
```

> The JWT command decodes only. It never verifies the signature and must not be
> used to make authorization decisions.

### `ip`

```bash
devtoolbox ip 8.8.8.8
devtoolbox ip 192.168.1.10/24 --json
devtoolbox ip ::1
```

## Python API

The CLI is a thin layer over importable modules:

```python
from devtoolbox import hashing, encoding, secrets_util, textcase, timeutil

assert hashing.hash_text("hello", "md5") == "5d41402abc4b2a76b9719d911017c592"
assert encoding.encode_base64(b"hello") == "aGVsbG8="
assert len(secrets_util.generate_password(24)) == 24
assert textcase.to_snake("HTTPServer") == "http_server"
assert timeutil.to_epoch(timeutil.parse_datetime("2024-01-01T00:00:00Z")) == 1704067200
```

## Development

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

python -m pip install -e ".[dev]"
python -m pytest
ruff check .
python -m build
twine check dist/*
```

The test suite covers both the pure utility modules and every CLI command via
`typer.testing.CliRunner`. CI runs linting and tests on Linux, macOS and Windows
across Python 3.9, 3.12 and 3.13, then builds and checks the distribution.

## Publishing to PyPI

Publishing uses PyPI [trusted publishing](https://docs.pypi.org/trusted-publishers/)
with GitHub Actions OIDC, so no API token is stored in the repository.

1. On PyPI, add a trusted publisher for `devtoolbox-cli`:
   - Owner: `goutamsingh22`
   - Repository: `devtoolbox-cli`
   - Workflow: `publish.yml`
   - Environment: `pypi`
2. Create a GitHub environment named `pypi` (optionally require approval).
3. Bump the version in `pyproject.toml`, commit, and push a tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The `Publish` workflow builds the sdist and wheel, checks them with `twine`, and
uploads them to PyPI.

## Project structure

```
devtoolbox-cli/
├── .github/workflows/
│   ├── ci.yml              # lint, test matrix, build + wheel smoke test
│   └── publish.yml         # build and publish to PyPI on v* tags
├── src/devtoolbox/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py              # Typer application
│   ├── hashing.py
│   ├── encoding.py
│   ├── jsonutil.py
│   ├── timeutil.py
│   ├── secrets_util.py
│   ├── textcase.py
│   ├── color.py
│   ├── jwtutil.py
│   └── netutil.py
├── tests/                  # pytest suite
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## License

MIT - see [LICENSE](LICENSE).
