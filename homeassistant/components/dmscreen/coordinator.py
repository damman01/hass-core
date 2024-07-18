"""Provides a coordinator for interacting with the Dmscreen API."""

from datetime import timedelta

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CHARACTER_URL, DOMAIN


class DmscreenCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Dmscreen data."""

    def __init__(self, hass: HomeAssistant, logger, character_id: int) -> None:
        """Initialize."""
        self.hass = hass
        self.logger = logger
        self.character_id = character_id
        self.session = aiohttp.ClientSession()
        self.close_session_task = None

        super().__init__(
            hass,
            logger,
            name=DOMAIN,
            update_interval=timedelta(minutes=360),
        )

    async def _async_update_data(self):
        """Fetch data from Dmscreen."""
        url = f"{CHARACTER_URL}{self.character_id}"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                raise UpdateFailed(
                    f"Error fetching data for {self.character_id}: {response}"
                )
        except Exception as e:
            raise UpdateFailed(f"Error fetching data: {e}") from e

    async def close_session(self):
        """Schließt die aiohttp-Session sauber."""
        if self.session:
            await self.session.close()

    async def validate_connection(self) -> bool:
        """Test the connection to the Dmscreen API."""
        try:
            await self._async_update_data()
        except UpdateFailed as e:
            await self.close_session()
            self.logger.error(e)
            return False
        else:
            return True
