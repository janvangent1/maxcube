"""Sensor platform for eQ-3 MAX! integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_VALVE_POSITIONS, DOMAIN
from .coordinator import MaxCubeCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the eQ-3 MAX! sensor platform."""
    coordinator: MaxCubeCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # Check if valve position devices should be created
    create_valve_devices = config_entry.data.get(CONF_VALVE_POSITIONS, True)
    
    for device in coordinator.data["devices"]:
        cube = coordinator.data["cube"]
        
        # Create temperature sensors for all thermostats and wall thermostats
        if cube.is_thermostat(device) or cube.is_wallthermostat(device):
            entities.append(MaxCubeTemperatureSensor(coordinator, device))
            
            # Create valve position sensor for radiator valves if enabled
            if cube.is_thermostat(device) and create_valve_devices:
                entities.append(MaxCubeValveSensor(coordinator, device))
    
    async_add_entities(entities)


class MaxCubeTemperatureSensor(SensorEntity):
    """Representation of a MAX! temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator: MaxCubeCoordinator, device) -> None:
        """Initialize the temperature sensor."""
        self.coordinator = coordinator
        self.device = device
        
        # Set unique ID based on device RF address
        self._attr_unique_id = f"maxcube_temp_{device.rf_address}"
        
        # Set name
        room = coordinator.data["cube"].room_by_id(device.room_id)
        self._attr_name = f"{room.name} {device.name} Temperature" if room else f"{device.name} Temperature"

    @property
    def native_value(self) -> float | None:
        """Return the current temperature."""
        return self.device.actual_temperature

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_update(self) -> None:
        """Update the entity."""
        await self.coordinator.async_request_refresh()


class MaxCubeValveSensor(SensorEntity):
    """Representation of a MAX! valve position sensor."""

    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, coordinator: MaxCubeCoordinator, device) -> None:
        """Initialize the valve position sensor."""
        self.coordinator = coordinator
        self.device = device
        
        # Set unique ID based on device RF address
        self._attr_unique_id = f"maxcube_valve_{device.rf_address}"
        
        # Set name
        room = coordinator.data["cube"].room_by_id(device.room_id)
        self._attr_name = f"{room.name} {device.name} Valve Position" if room else f"{device.name} Valve Position"

    @property
    def native_value(self) -> int | None:
        """Return the current valve position."""
        return self.device.valve_position

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_update(self) -> None:
        """Update the entity."""
        await self.coordinator.async_request_refresh()
