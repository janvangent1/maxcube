"""Services for eQ-3 MAX! integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import DOMAIN
from .coordinator import MaxCubeCoordinator

_LOGGER = logging.getLogger(__name__)

# Service schemas
RELOAD_DEVICES_SCHEMA = vol.Schema({
    vol.Required("cube_address"): cv.string,
})

CLEAR_AND_RELOAD_SCHEMA = vol.Schema({
    vol.Required("cube_address"): cv.string,
})

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for the MAX! Cube integration."""
    
    async def reload_devices_service(call: ServiceCall) -> None:
        """Service to reload devices from the cube."""
        cube_address = call.data["cube_address"]
        
        # Find the coordinator for this cube
        coordinator = None
        for entry_id, coordinator_data in hass.data[DOMAIN].items():
            if isinstance(coordinator_data, MaxCubeCoordinator):
                if coordinator_data.cube_address == cube_address:
                    coordinator = coordinator_data
                    break
        
        if not coordinator:
            _LOGGER.error("No MAX! Cube coordinator found for address %s", cube_address)
            return
        
        try:
            await coordinator.reload_devices()
            _LOGGER.info("Successfully reloaded devices for cube %s", cube_address)
        except Exception as err:
            _LOGGER.error("Failed to reload devices for cube %s: %s", cube_address, err)
    
    async def clear_and_reload_service(call: ServiceCall) -> None:
        """Service to clear cache and reload devices from the cube."""
        cube_address = call.data["cube_address"]
        
        # Find the coordinator for this cube
        coordinator = None
        for entry_id, coordinator_data in hass.data[DOMAIN].items():
            if isinstance(coordinator_data, MaxCubeCoordinator):
                if coordinator_data.cube_address == cube_address:
                    coordinator = coordinator_data
                    break
        
        if not coordinator:
            _LOGGER.error("No MAX! Cube coordinator found for address %s", cube_address)
            return
        
        try:
            await coordinator.clear_and_reload_devices()
            _LOGGER.info("Successfully cleared cache and reloaded devices for cube %s", cube_address)
        except Exception as err:
            _LOGGER.error("Failed to clear and reload devices for cube %s: %s", cube_address, err)
    
    # Register services
    hass.services.async_register(
        DOMAIN,
        "reload_devices",
        reload_devices_service,
        schema=RELOAD_DEVICES_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "clear_and_reload_devices",
        clear_and_reload_service,
        schema=CLEAR_AND_RELOAD_SCHEMA,
    )
    
    _LOGGER.info("MAX! Cube services registered")

async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload services for the MAX! Cube integration."""
    hass.services.async_remove(DOMAIN, "reload_devices")
    hass.services.async_remove(DOMAIN, "clear_and_reload_devices")
    _LOGGER.info("MAX! Cube services unloaded")
