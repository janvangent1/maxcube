"""Switch platform for eQ-3 MAX! integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_HEAT_DEMAND_SWITCH, DOMAIN
from .coordinator import MaxCubeCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the eQ-3 MAX! switch platform."""
    coordinator: MaxCubeCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # Create heat demand switch if enabled
    if config_entry.data.get(CONF_HEAT_DEMAND_SWITCH, False):
        entities.append(MaxCubeHeatDemandSwitch(coordinator))
    
    # Create window/door contact switches
    for device in coordinator.data["devices"]:
        cube = coordinator.data["cube"]
        
        if cube.is_windowshutter(device):
            entities.append(MaxCubeWindowShutterSwitch(coordinator, device))
    
    async_add_entities(entities)


class MaxCubeHeatDemandSwitch(SwitchEntity):
    """Representation of a MAX! heat demand switch."""

    def __init__(self, coordinator: MaxCubeCoordinator) -> None:
        """Initialize the heat demand switch."""
        self.coordinator = coordinator
        
        # Set unique ID
        self._attr_unique_id = "maxcube_heat_demand"
        
        # Set name
        self._attr_name = "Heat Demand"

    @property
    def is_on(self) -> bool:
        """Return if the switch is on."""
        return self.coordinator.data.get("heat_demand", False)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        # Heat demand switch is read-only, it's controlled by valve positions
        _LOGGER.warning("Heat demand switch is read-only")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        # Heat demand switch is read-only, it's controlled by valve positions
        _LOGGER.warning("Heat demand switch is read-only")

    async def async_update(self) -> None:
        """Update the entity."""
        await self.coordinator.async_request_refresh()


class MaxCubeWindowShutterSwitch(SwitchEntity):
    """Representation of a MAX! window/door contact switch."""

    def __init__(self, coordinator: MaxCubeCoordinator, device) -> None:
        """Initialize the window shutter switch."""
        self.coordinator = coordinator
        self.device = device
        
        # Set unique ID based on device RF address
        self._attr_unique_id = f"maxcube_contact_{device.rf_address}"
        
        # Set name
        room = coordinator.data["cube"].room_by_id(device.room_id)
        self._attr_name = f"{room.name} {device.name}" if room else device.name

    @property
    def is_on(self) -> bool:
        """Return if the switch is on (window/door is open)."""
        return self.device.is_open

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        # Window shutter switches are read-only
        _LOGGER.warning("Window shutter switch is read-only")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        # Window shutter switches are read-only
        _LOGGER.warning("Window shutter switch is read-only")

    async def async_update(self) -> None:
        """Update the entity."""
        await self.coordinator.async_request_refresh()
