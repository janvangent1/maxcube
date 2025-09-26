"""Config flow for eQ-3 MAX! integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_CUBE_ADDRESS,
    CONF_CUBE_PORT,
    CONF_VALVE_POSITIONS,
    CONF_THERMOSTAT_MODES,
    CONF_HEAT_DEMAND_SWITCH,
    CONF_MIN_VALVE_POSITION,
    CONF_UPDATE_INTERVAL,
    CONF_DEBUG_MODE,
    DEFAULT_PORT,
    DEFAULT_VALVE_POSITIONS,
    DEFAULT_THERMOSTAT_MODES,
    DEFAULT_HEAT_DEMAND_SWITCH,
    DEFAULT_MIN_VALVE_POSITION,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_DEBUG_MODE,
    DOMAIN,
    UPDATE_INTERVALS,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CUBE_ADDRESS): str,
        vol.Required(CONF_CUBE_PORT, default=DEFAULT_PORT): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=65535)
        ),
        vol.Required(CONF_VALVE_POSITIONS, default=DEFAULT_VALVE_POSITIONS): bool,
        vol.Required(CONF_THERMOSTAT_MODES, default=DEFAULT_THERMOSTAT_MODES): bool,
        vol.Required(CONF_HEAT_DEMAND_SWITCH, default=DEFAULT_HEAT_DEMAND_SWITCH): bool,
        vol.Required(CONF_MIN_VALVE_POSITION, default=DEFAULT_MIN_VALVE_POSITION): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=100)
        ),
        vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.In(
            list(UPDATE_INTERVALS.keys())
        ),
        vol.Required(CONF_DEBUG_MODE, default=DEFAULT_DEBUG_MODE): bool,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for eQ-3 MAX!."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        # Check if already configured
        await self.async_set_unique_id(user_input[CONF_CUBE_ADDRESS])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"eQ-3 MAX! Cube ({user_input[CONF_CUBE_ADDRESS]})",
            data=user_input,
        )
