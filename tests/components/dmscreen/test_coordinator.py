"""Test the DnDBeyond DM Screen coordinator."""

import logging
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant.components.dmscreen.coordinator import DmscreenCoordinator
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


async def test_validate_connection_success(
    hass: HomeAssistant, caplog: pytest.LogCaptureFixture
) -> None:
    """Test validate_connection method success."""
    character_id = 123
    coordinator = DmscreenCoordinator(hass, AsyncMock(), character_id)

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(
            lambda: {"data": "some data"}
        )
        assert await coordinator.validate_connection() is True
        await coordinator.close_session()


async def test_validate_connection_failure(
    hass: HomeAssistant, caplog: pytest.LogCaptureFixture
) -> None:
    """Test validate_connection method failure due to UpdateFailed."""
    caplog.set_level(logging.ERROR)
    character_id = 123
    coordinator = DmscreenCoordinator(AsyncMock(), _LOGGER, character_id)

    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 500
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value={})

        result = await coordinator.validate_connection()
        assert result is False
        assert "Error fetching data:" in caplog.text
