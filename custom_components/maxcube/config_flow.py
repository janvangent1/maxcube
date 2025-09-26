"""Config flow for eQ-3 MAX! integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("cube_address"): str,
        vol.Required("cube_port", default=62910): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=65535)
        ),
        vol.Required("valve_positions", default=True): bool,
        vol.Required("thermostat_modes", default=False): bool,
        vol.Required("heat_demand_switch", default=True): bool,
        vol.Required("min_valve_position", default=25): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=100)
        ),
        vol.Required("update_interval", default=300): vol.In([60, 120, 300, 600, 1800]),
        vol.Required("debug_mode", default=False): bool,
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

        await self.async_set_unique_id(user_input["cube_address"])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"eQ-3 MAX! Cube ({user_input['cube_address']})",
            data=user_input,
        )
