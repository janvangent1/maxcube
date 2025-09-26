#!/bin/bash

echo "🐳 INSTALLING INTEGRATION INSIDE DOCKER CONTAINER"
echo "================================================="

# 1. Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop homeassistant

# 2. Remove ALL old integration directories INSIDE the container
echo "🗑️ Removing ALL old integration directories INSIDE container..."
docker exec homeassistant rm -rf /config/custom_components/maxcube
docker exec homeassistant rm -rf /config/custom_components/jan_max
docker exec homeassistant rm -rf /config/custom_components/jan_eq3_max

# 3. Clean up old config entries INSIDE the container
echo "🧹 Cleaning up old config entries INSIDE container..."
docker exec homeassistant rm -f /config/.storage/core.config_entries
docker exec homeassistant rm -f /config/.storage/core.registry
docker exec homeassistant rm -f /config/.storage/core.restore_state
docker exec homeassistant rm -f /config/.storage/core.entity_registry

# 4. Create minimal working configuration INSIDE the container
echo "📝 Creating minimal working configuration INSIDE container..."
cat <<EOF | docker exec -i homeassistant tee /config/configuration.yaml > /dev/null
# Configure a default setup of Home Assistant
default_config:

# Text to speech
tts:
  - platform: google_translate

# Include other YAML files
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
EOF

# Create empty include files INSIDE the container
echo "# No automations defined yet" | docker exec -i homeassistant tee /config/automations.yaml > /dev/null
echo "# No scripts defined yet" | docker exec -i homeassistant tee /config/scripts.yaml > /dev/null
echo "# No scenes defined yet" | docker exec -i homeassistant tee /config/scenes.yaml > /dev/null

# 5. Ensure the custom_components directory exists INSIDE the container
echo "📁 Ensuring custom_components directory exists INSIDE container..."
docker exec homeassistant mkdir -p /config/custom_components

# 6. Create the integration directory INSIDE the container
echo "📂 Creating jan_eq3_max directory INSIDE container..."
docker exec homeassistant mkdir -p /config/custom_components/jan_eq3_max

# 7. Create manifest.json INSIDE the container
echo "📋 Creating manifest.json INSIDE container..."
cat <<EOF | docker exec -i homeassistant tee /config/custom_components/jan_eq3_max/manifest.json > /dev/null
{
  "domain": "jan_eq3_max",
  "name": "Jan eQ-3 MAX!",
  "documentation": "https://github.com/janvangent1/maxcube",
  "issue_tracker": "https://github.com/janvangent1/maxcube/issues",
  "dependencies": [],
  "codeowners": ["@janvangent1"],
  "config_flow": true,
  "requirements": [],
  "version": "0.6.8",
  "iot_class": "local_polling"
}
EOF

# 8. Create const.py INSIDE the container
echo "📄 Creating const.py INSIDE container..."
cat <<EOF | docker exec -i homeassistant tee /config/custom_components/jan_eq3_max/const.py > /dev/null
"""Constants for the Jan eQ-3 MAX! integration."""

DOMAIN = "jan_eq3_max"

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

# 9. Create __init__.py INSIDE the container
echo "📄 Creating __init__.py INSIDE container..."
cat <<EOF | docker exec -i homeassistant tee /config/custom_components/jan_eq3_max/__init__.py > /dev/null
"""The Jan eQ-3 MAX! integration."""
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
    """Set up Jan eQ-3 MAX! from a config entry."""
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

# 10. Create config_flow.py INSIDE the container
echo "📄 Creating config_flow.py INSIDE container..."
cat <<EOF | docker exec -i homeassistant tee /config/custom_components/jan_eq3_max/config_flow.py > /dev/null
"""Config flow for Jan eQ-3 MAX! integration."""
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
    """Handle a config flow for Jan eQ-3 MAX!."""

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
            title=f"Jan eQ-3 MAX! Cube ({user_input['cube_address']})",
            data=user_input,
        )
EOF

# 11. Set correct permissions INSIDE the container
echo "🔐 Setting correct permissions INSIDE container..."
docker exec homeassistant chown -R root:root /config/custom_components/jan_eq3_max
docker exec homeassistant chmod -R 755 /config/custom_components/jan_eq3_max

# 12. Verify the files are there INSIDE the container
echo "✅ Verifying integration files INSIDE container..."
docker exec homeassistant ls -la /config/custom_components/jan_eq3_max/

# 13. Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start homeassistant

# 14. Wait for Home Assistant to start
echo "⏳ Waiting for Home Assistant to start..."
sleep 30

# Check status
echo "🔍 Checking Home Assistant status..."
docker ps | grep homeassistant

# Check if integration is loaded
echo "🔍 Checking if integration is loaded..."
sleep 10
docker logs homeassistant 2>&1 | grep -i "jan_eq3_max" | tail -5

echo ""
echo "✅ Installation completed INSIDE Docker container!"
echo "📋 Next steps:"
echo "   1. Wait for Home Assistant to fully start (3-5 minutes)"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Complete the initial setup if prompted"
echo "   4. Go to Settings > Devices & Services"
echo "   5. Click 'Add Integration'"
echo "   6. Search for 'Jan eQ-3 MAX!'"
echo "   7. Configure with IP: 192.168.1.26, Port: 62910"
echo ""
echo "🔍 To check logs: docker logs homeassistant"
echo "🔍 To check if integration is working: docker logs homeassistant | grep -i 'jan_eq3_max'"
echo ""
echo "⚠️  If you still don't see the integration, restart Home Assistant:"
echo "   docker restart homeassistant"
