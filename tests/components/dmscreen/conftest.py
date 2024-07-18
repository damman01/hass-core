"""Common fixtures for the DnDBeyond DM Screen tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from pytest_socket import enable_socket, socket_allow_hosts


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "homeassistant.components.dmscreen.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.hookimpl(trylast=True)
def pytest_runtest_setup():
    """Set up the test environment before running each test."""
    enable_socket()
    socket_allow_hosts(["character-service.dndbeyond.com"], allow_unix_socket=True)
