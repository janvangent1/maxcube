"""Data coordinator for Jan MAX! integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .cube import MaxCube
from .connection import MaxCubeConnection

_LOGGER = logging.getLogger(__name__)


class MaxCubeCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Jan MAX! Cube."""

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
                    "gpio_status": self.data.get("gpio_status", "Ready") if self.data else "Ready",
                    "last_gpio_command": self.data.get("last_gpio_command", "None") if self.data else "None",
                    "last_gpio_result": self.data.get("last_gpio_result", "None") if self.data else "None",
                    "last_gpio_timestamp": self.data.get("last_gpio_timestamp", "None") if self.data else "None",
                    "gpio_command_count": self.data.get("gpio_command_count", 0) if self.data else 0,
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

    async def reload_devices(self) -> None:
        """Reload all devices by scanning the cube again."""
        try:
            _LOGGER.info("Reloading MAX! Cube devices...")
            
            # Force a fresh connection and scan
            connection = MaxCubeConnection(self.cube_address, self.cube_port)
            cube = MaxCube(connection)
            cube.update()
            
            # Update the coordinator data
            await self.async_request_refresh()
            
            _LOGGER.info("Successfully reloaded %s devices and %s rooms", 
                        len(cube.devices), len(cube.rooms))
            
        except Exception as err:
            _LOGGER.error("Error reloading devices: %s", err)
            raise

    async def clear_and_reload_devices(self) -> None:
        """Clear all cached data and reload devices from cube."""
        try:
            _LOGGER.info("Clearing cached data and reloading MAX! Cube devices...")
            
            # Clear any cached data
            self.data = None
            
            # Force a fresh scan
            await self.reload_devices()
            
            _LOGGER.info("Successfully cleared cache and reloaded devices")
            
        except Exception as err:
            _LOGGER.error("Error clearing and reloading devices: %s", err)
            raise

    async def update_gpio_status(self, command: str, result: str, success: bool) -> None:
        """Update GPIO status information."""
        from datetime import datetime
        
        if self.data is None:
            self.data = {}
        
        self.data["gpio_status"] = "Success" if success else "Failed"
        self.data["last_gpio_command"] = command
        self.data["last_gpio_result"] = result
        self.data["last_gpio_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data["gpio_command_count"] = self.data.get("gpio_command_count", 0) + 1
        
        _LOGGER.info("GPIO command '%s' %s: %s", command, "succeeded" if success else "failed", result)
        
        # Trigger entity update
        await self.async_request_refresh()
