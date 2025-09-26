"""Data coordinator for eQ-3 MAX! integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .maxcube.cube import MaxCube
from .maxcube.connection import MaxCubeConnection

_LOGGER = logging.getLogger(__name__)


class MaxCubeCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the eQ-3 MAX! Cube."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.cube_address = entry.data["cube_address"]
        self.cube_port = entry.data["cube_port"]
        self.debug_mode = entry.data.get("debug_mode", False)
        
        # Set up logging level based on debug mode
        if self.debug_mode:
            logging.getLogger("maxcube").setLevel(logging.DEBUG)
        
        update_interval = timedelta(seconds=entry.data.get("update_interval", 300))
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict:
        """Update data via library."""
        try:
            # Create cube connection
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
            if cube.is_thermostat(device) and device.valve_position > min_valve_position:
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
