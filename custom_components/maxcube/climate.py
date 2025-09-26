"""Climate platform for Jan MAX! integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_THERMOSTAT_MODES,
    DOMAIN,
    THERMOSTAT_MODE_AUTO,
    THERMOSTAT_MODE_MANUAL,
    THERMOSTAT_MODE_VACATION,
    THERMOSTAT_MODE_BOOST,
    THERMOSTAT_MODES,
)
from .coordinator import MaxCubeCoordinator

_LOGGER = logging.getLogger(__name__)

# Map MAX! modes to Home Assistant HVAC modes
MAX_TO_HA_MODE = {
    THERMOSTAT_MODE_AUTO: HVACMode.AUTO,
    THERMOSTAT_MODE_MANUAL: HVACMode.HEAT,
    THERMOSTAT_MODE_VACATION: HVACMode.OFF,
    THERMOSTAT_MODE_BOOST: HVACMode.HEAT,
}

HA_TO_MAX_MODE = {v: k for k, v in MAX_TO_HA_MODE.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Jan MAX! climate platform."""
    coordinator: MaxCubeCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # Check if thermostat mode devices should be created
    create_mode_devices = config_entry.data.get(CONF_THERMOSTAT_MODES, False)
    
    for device in coordinator.data["devices"]:
        cube = coordinator.data["cube"]
        
        # Create climate entities for thermostats and wall thermostats
        if cube.is_thermostat(device) or cube.is_wallthermostat(device):
            # For radiator valves, only create climate entity if room doesn't have wall thermostat
            if cube.is_thermostat(device):
                room = cube.room_by_id(device.room_id)
                has_wall_thermostat = any(
                    cube.is_wallthermostat(d) and d.room_id == device.room_id
                    for d in cube.devices
                )
                if has_wall_thermostat:
                    continue  # Skip radiator valve if room has wall thermostat
            
            entities.append(MaxCubeClimate(coordinator, device, create_mode_devices))
    
    async_add_entities(entities)


class MaxCubeClimate(ClimateEntity):
    """Representation of a MAX! thermostat."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.AUTO, HVACMode.HEAT, HVACMode.OFF]
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

    def __init__(self, coordinator: MaxCubeCoordinator, device, create_mode_devices: bool) -> None:
        """Initialize the climate entity."""
        self.coordinator = coordinator
        self.device = device
        self.create_mode_devices = create_mode_devices
        
        # Set unique ID based on device RF address
        self._attr_unique_id = f"maxcube_{device.rf_address}"
        
        # Set name
        room = coordinator.data["cube"].room_by_id(device.room_id)
        self._attr_name = f"{room.name} {device.name}" if room else device.name

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        return self.device.actual_temperature

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        return self.device.target_temperature

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        return MAX_TO_HA_MODE.get(self.device.mode, HVACMode.AUTO)

    @property
    def min_temp(self) -> float:
        """Return minimum temperature."""
        return self.device.min_temperature or 5.0

    @property
    def max_temp(self) -> float:
        """Return maximum temperature."""
        return self.device.max_temperature or 30.0

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        
        await self.coordinator.set_target_temperature(self.device.rf_address, temperature)
        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target HVAC mode."""
        if not self.create_mode_devices:
            _LOGGER.warning("Thermostat mode changes are disabled in configuration")
            return
        
        max_mode = HA_TO_MAX_MODE.get(hvac_mode)
        if max_mode is not None:
            await self.coordinator.set_mode(self.device.rf_address, max_mode)
            await self.coordinator.async_request_refresh()

    async def async_update(self) -> None:
        """Update the entity."""
        await self.coordinator.async_request_refresh()
