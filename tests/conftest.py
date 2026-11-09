from __future__ import annotations

import pytest
from typer.testing import CliRunner

from devtoolbox.cli import app


@pytest.fixture()
def run():
    runner = CliRunner()

    def _run(*args, **kwargs):
        return runner.invoke(app, [str(arg) for arg in args], **kwargs)

    return _run
