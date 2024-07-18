"""The DnDBeyond DM Screen integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import DmscreenCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]
_LOGGER = logging.getLogger(__name__)


# Typalias mit API-Objekt erstellt
class DmscreenConfigEntry(ConfigEntry):
    """Represents a configuration entry for DnDBeyond DM Screen."""

    api: DmscreenCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: DmscreenConfigEntry) -> bool:
    """Set up DnDBeyond DM Screen from a config entry."""
    logger = _LOGGER
    coordinator = DmscreenCoordinator(hass, logger, entry.data["id"])

    if not await coordinator.validate_connection():
        await coordinator.close_session()
        return False
    await coordinator.close_session()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: DmscreenConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
