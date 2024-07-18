"""Test the DnDBeyond DM Screen config flow."""

from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.components.dmscreen.const import DOMAIN
from homeassistant.const import CONF_ID, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_form(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "homeassistant.components.dmscreen.coordinator.DmscreenCoordinator._async_update_data",
        return_value={
            "data": {
                "id": 114328408,
                "userId": 119177546,
                "username": "Wiwaka",
                "name": "Wiwaka",
            }
        },
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_ID: 114328408, CONF_NAME: ""},
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Character: Wiwaka"
    assert result["data"] == {CONF_ID: 114328408, CONF_NAME: "Wiwaka"}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_with_connect(hass: HomeAssistant) -> None:
    """Test connection."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_ID: 91417889, CONF_NAME: ""},
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Character: Kitural"
    assert result["data"] == {CONF_ID: 91417889, CONF_NAME: "Kitural"}
