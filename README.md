# eQ-3 MAX! Home Assistant Integration

This is a Home Assistant custom component for integrating the ELV/e-Q3 MAX! heating system. It's converted from the original Domoticz plugin by mvzut.

## Features

- **Climate Control**: Control thermostats and wall thermostats
- **Temperature Monitoring**: Read current temperatures from all devices
- **Valve Position Monitoring**: Monitor radiator valve positions (optional)
- **Window/Door Sensors**: Monitor window and door contacts
- **Heat Demand Switch**: Automatic switch that activates when valves are open (optional)
- **Configurable Polling**: Adjustable update intervals (1-30 minutes)

## Installation

### Manual Installation

1. Copy the `maxcube` folder to your Home Assistant `custom_components` directory:
   ```
   <config>/custom_components/maxcube/
   ```

2. Restart Home Assistant

3. Go to **Settings** > **Devices & Services** > **Add Integration**

4. Search for "eQ-3 MAX!" and add it

### Configuration

During setup, you can configure:

- **Cube Address**: IP address of your MAX! Cube
- **Cube Port**: Port number (default: 62910)
- **Valve Positions**: Create valve position sensors (default: enabled)
- **Thermostat Modes**: Create thermostat mode controls (default: disabled)
- **Heat Demand Switch**: Create heat demand switch (default: disabled)
- **Min Valve Position**: Minimum valve position for heat demand (default: 25%)
- **Update Interval**: How often to poll the cube (default: 5 minutes)
- **Debug Mode**: Enable debug logging (default: disabled)

## Device Types

### Climate Entities
- **Wall Thermostats**: Full climate control with temperature and mode settings
- **Radiator Valves**: Climate control only if room doesn't have wall thermostat

### Sensor Entities
- **Temperature Sensors**: Current temperature from all thermostats
- **Valve Position Sensors**: Current valve position from radiator valves (optional)

### Switch Entities
- **Heat Demand Switch**: Indicates when heating is required (optional)
- **Window/Door Contacts**: Shows if windows/doors are open

## Notes

- Radiator valves only report temperature when other parameters change
- If a room has a wall thermostat, it acts as the primary control for that room
- The heat demand switch is read-only and automatically controlled by valve positions
- Window/door contact switches are read-only

## Troubleshooting

- Ensure your MAX! Cube is accessible on the network
- Check that no other MAX! programs are running simultaneously
- Enable debug mode for detailed logging
- Verify firewall settings allow connections to the cube

## Original Credits

Based on the work of:
- mvzut: Original Domoticz plugin
- hackercowboy: Python MAX! Cube API library

## License

This integration is provided as-is for educational and personal use.
