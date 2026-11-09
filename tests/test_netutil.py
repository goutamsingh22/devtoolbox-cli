from __future__ import annotations

import pytest

from devtoolbox import netutil


def test_inspect_address() -> None:
    info = netutil.inspect("8.8.8.8")
    assert info["kind"] == "address"
    assert info["version"] == 4
    assert info["address"] == "8.8.8.8"
    assert info["is_global"] is True
    assert info["is_private"] is False
    assert info["reverse_pointer"] == "8.8.8.8.in-addr.arpa"


def test_inspect_interface() -> None:
    info = netutil.inspect("192.168.1.10/24")
    assert info["kind"] == "interface"
    assert info["network"] == "192.168.1.0/24"
    assert info["network_address"] == "192.168.1.0"
    assert info["broadcast_address"] == "192.168.1.255"
    assert info["prefixlen"] == 24
    assert info["num_addresses"] == 256
    assert info["is_private"] is True


def test_inspect_ipv6_loopback() -> None:
    info = netutil.inspect("::1")
    assert info["version"] == 6
    assert info["is_loopback"] is True


def test_invalid_value() -> None:
    with pytest.raises(ValueError, match="invalid IP"):
        netutil.inspect("not-an-ip")
