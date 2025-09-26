#!/bin/bash

echo "🔄 ROLLBACK TO WORKING VERSION"
echo "=============================="

# Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop homeassistant

# Remove the broken integration
echo "🗑️ Removing broken integration..."
docker exec homeassistant rm -rf /config/custom_components/maxcube

# Create the working integration structure
echo "📁 Creating working integration structure..."
docker exec homeassistant mkdir -p /config/custom_components/maxcube

# Create manifest.json (back to original working version)
echo "📝 Creating manifest.json..."
docker exec homeassistant tee /config/custom_components/maxcube/manifest.json > /dev/null << 'EOF'
{
  "domain": "maxcube",
  "name": "eQ-3 MAX!",
  "documentation": "https://github.com/janvangent1/maxcube",
  "issue_tracker": "https://github.com/janvangent1/maxcube/issues",
  "dependencies": [],
  "codeowners": ["@janvangent1"],
  "config_flow": true,
  "requirements": [],
  "version": "0.6.6",
  "iot_class": "local_polling"
}
EOF

# Create __init__.py
echo "📝 Creating __init__.py..."
docker exec homeassistant tee /config/custom_components/maxcube/__init__.py > /dev/null << 'EOF'
"""The eQ-3 MAX! integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import MaxCubeCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up eQ-3 MAX! from a config entry."""
    coordinator = MaxCubeCoordinator(hass, entry)
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
EOF

# Create const.py
echo "📝 Creating const.py..."
docker exec homeassistant tee /config/custom_components/maxcube/const.py > /dev/null << 'EOF'
"""Constants for the eQ-3 MAX! integration."""

DOMAIN = "maxcube"

# Configuration keys
CONF_CUBE_ADDRESS = "cube_address"
CONF_CUBE_PORT = "cube_port"
CONF_VALVE_POSITIONS = "valve_positions"
CONF_THERMOSTAT_MODES = "thermostat_modes"
CONF_HEAT_DEMAND_SWITCH = "heat_demand_switch"
CONF_MIN_VALVE_POSITION = "min_valve_position"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_DEBUG_MODE = "debug_mode"
EOF

# Create config_flow.py
echo "📝 Creating config_flow.py..."
docker exec homeassistant tee /config/custom_components/maxcube/config_flow.py > /dev/null << 'EOF'
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
EOF

# Create coordinator.py (simplified working version)
echo "📝 Creating coordinator.py..."
docker exec homeassistant tee /config/custom_components/maxcube/coordinator.py > /dev/null << 'EOF'
"""Data coordinator for eQ-3 MAX! integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .cube import MaxCube
from .connection import MaxCubeConnection

_LOGGER = logging.getLogger(__name__)


class MaxCubeCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the eQ-3 MAX! Cube."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.cube_address = entry.data["cube_address"]
        self.cube_port = entry.data["cube_port"]
        self.update_interval_seconds = entry.data.get("update_interval", 300)
        self.debug_mode = entry.data.get("debug_mode", False)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=self.update_interval_seconds),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from MAX! Cube."""
        try:
            if self.debug_mode:
                _LOGGER.debug("Fetching data from MAX! Cube at %s:%s", 
                              self.cube_address, self.cube_port)
            
            connection = MaxCubeConnection(self.cube_address, self.cube_port)
            cube = MaxCube(connection)
            
            # Update cube data
            cube.update()
            
            # Prepare data for platforms
            data = {
                "cube": cube,
                "devices": cube.devices,
                "rooms": cube.rooms,
                "heat_demand": self._calculate_heat_demand(cube),
            }
            
            if self.debug_mode:
                _LOGGER.debug("Updated MAX! Cube data: %s devices, %s rooms", 
                            len(cube.devices), len(cube.rooms))
            
            return data
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with MAX! Cube: {err}")

    def _calculate_heat_demand(self, cube: MaxCube) -> bool:
        """Calculate if there's heat demand based on valve positions."""
        min_valve_position = self.entry.data.get("min_valve_position", 25)
        
        for device in cube.devices:
            if (cube.is_thermostat(device) and 
                device.valve_position is not None and 
                device.valve_position > min_valve_position):
                return True
        
        return False

    async def set_target_temperature(self, device_rf_address: str, temperature: float) -> None:
        """Set target temperature for a device."""
        try:
            connection = MaxCubeConnection(self.cube_address, self.cube_port)
            cube = MaxCube(connection)
            cube.update()
            
            device = cube.device_by_rf(device_rf_address)
            if device:
                cube.set_target_temperature(device, temperature)
                _LOGGER.info("Set temperature %s for device %s", temperature, device_rf_address)
            else:
                _LOGGER.error("Device %s not found", device_rf_address)
                
        except Exception as err:
            _LOGGER.error("Error setting temperature: %s", err)

    async def set_mode(self, device_rf_address: str, mode: int) -> None:
        """Set mode for a device."""
        try:
            connection = MaxCubeConnection(self.cube_address, self.cube_port)
            cube = MaxCube(connection)
            cube.update()
            
            device = cube.device_by_rf(device_rf_address)
            if device:
                cube.set_mode(device, mode)
                _LOGGER.info("Set mode %s for device %s", mode, device_rf_address)
            else:
                _LOGGER.error("Device %s not found", device_rf_address)
                
        except Exception as err:
            _LOGGER.error("Error setting mode: %s", err)
EOF

# Set correct permissions
echo "🔐 Setting correct permissions..."
docker exec homeassistant chown -R root:root /config/custom_components/maxcube
docker exec homeassistant chmod -R 755 /config/custom_components/maxcube

# Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start homeassistant

echo "⏳ Waiting for Home Assistant to start..."
sleep 30

# Check status
echo "🔍 Checking Home Assistant status..."
docker ps | grep homeassistant

echo ""
echo "✅ Rollback to working version completed!"
echo "📋 Next steps:"
echo "   1. Wait for Home Assistant to fully start (2-3 minutes)"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Add the eQ-3 MAX! integration (not jan_max)"
echo "   4. Configure with IP: 192.168.1.26, Port: 62910"
echo ""
echo "🔍 To check logs: docker logs homeassistant"
echo "🔍 To check if integration is working: docker logs homeassistant | grep -i 'maxcube'"
