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

# Default values
DEFAULT_PORT = 62910
DEFAULT_VALVE_POSITIONS = True
DEFAULT_THERMOSTAT_MODES = False
DEFAULT_HEAT_DEMAND_SWITCH = False
DEFAULT_MIN_VALVE_POSITION = 25
DEFAULT_UPDATE_INTERVAL = 300  # 5 minutes
DEFAULT_DEBUG_MODE = False

# Update intervals in seconds
UPDATE_INTERVALS = {
    60: "1 minute",
    120: "2 minutes", 
    300: "5 minutes",
    600: "10 minutes",
    1800: "30 minutes"
}

# Device types
DEVICE_TYPE_THERMOSTAT = "thermostat"
DEVICE_TYPE_WALL_THERMOSTAT = "wall_thermostat"
DEVICE_TYPE_WINDOW_SHUTTER = "window_shutter"

# Thermostat modes
THERMOSTAT_MODE_AUTO = 0
THERMOSTAT_MODE_MANUAL = 1
THERMOSTAT_MODE_VACATION = 2
THERMOSTAT_MODE_BOOST = 3

THERMOSTAT_MODES = {
    THERMOSTAT_MODE_AUTO: "Auto",
    THERMOSTAT_MODE_MANUAL: "Manual", 
    THERMOSTAT_MODE_VACATION: "Vacation",
    THERMOSTAT_MODE_BOOST: "Boost"
}
