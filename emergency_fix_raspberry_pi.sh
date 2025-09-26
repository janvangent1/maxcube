#!/bin/bash

echo "🚨 EMERGENCY FIX - MAX! Cube Integration"
echo "========================================"

# Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop homeassistant

# Remove the old broken integration
echo "🗑️ Removing old broken integration..."
sudo rm -rf /home/pi/ha/custom_components/maxcube

# Create a minimal working configuration.yaml
echo "📝 Creating minimal configuration.yaml..."
sudo tee /home/pi/ha/configuration.yaml > /dev/null << 'EOF'
# Loads default set of integrations. Do not remove.
default_config:

# Load frontend themes from the themes folder
frontend:
  themes: !include_dir_merge_named themes

# Text to speech
tts:
  - platform: google_translate

# Group configuration
group: !include groups.yaml

# Automation configuration
automation: !include automations.yaml

# Script configuration
script: !include scripts.yaml

# Scene configuration
scene: !include scenes.yaml

# REST Commands for GPIO control
rest_command:
  gpio_control:
    url: "http://192.168.1.190/control?cmd={{ command }}"
    method: GET
    timeout: 10
EOF

# Set correct permissions
sudo chown root:root /home/pi/ha/configuration.yaml
sudo chmod 644 /home/pi/ha/configuration.yaml

# Create groups.yaml with correct syntax
echo "📝 Creating groups.yaml..."
sudo tee /home/pi/ha/groups.yaml > /dev/null << 'EOF'
# Groups configuration
default_view:
  entities:
    - group.all_lights
    - group.all_switches
    - group.all_sensors
    - group.all_climate
    - group.all_automations

all_lights:
  name: All Lights
  entities:

all_switches:
  name: All Switches
  entities:

all_sensors:
  name: All Sensors
  entities:

all_climate:
  name: All Climate
  entities:

all_automations:
  name: All Automations
  entities:
EOF
sudo chown root:root /home/pi/ha/groups.yaml
sudo chmod 644 /home/pi/ha/groups.yaml

# Create scripts.yaml
echo "📝 Creating scripts.yaml..."
sudo tee /home/pi/ha/scripts.yaml > /dev/null << 'EOF'
# Scripts configuration
# Add your custom scripts here
EOF
sudo chown root:root /home/pi/ha/scripts.yaml
sudo chmod 644 /home/pi/ha/scripts.yaml

# Create scenes.yaml
echo "📝 Creating scenes.yaml..."
sudo tee /home/pi/ha/scenes.yaml > /dev/null << 'EOF'
# Scenes configuration
# Add your custom scenes here
EOF
sudo chown root:root /home/pi/ha/scenes.yaml
sudo chmod 644 /home/pi/ha/scenes.yaml

# Create automations.yaml
echo "📝 Creating automations.yaml..."
sudo tee /home/pi/ha/automations.yaml > /dev/null << 'EOF'
# Automations configuration
# Add your custom automations here
EOF
sudo chown root:root /home/pi/ha/automations.yaml
sudo chmod 644 /home/pi/ha/automations.yaml

# Create themes directory
sudo mkdir -p /home/pi/ha/themes
sudo chown root:root /home/pi/ha/themes
sudo chmod 755 /home/pi/ha/themes

# Download and install the fixed integration
echo "📥 Downloading fixed integration..."
cd /home/pi/ha/custom_components
sudo git clone https://github.com/janvangent1/maxcube.git maxcube
sudo chown -R root:root maxcube
sudo chmod -R 755 maxcube

# Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start homeassistant

echo "⏳ Waiting for Home Assistant to start..."
sleep 30

# Check status
echo "🔍 Checking Home Assistant status..."
docker ps | grep homeassistant

echo ""
echo "✅ Emergency fix completed!"
echo "📋 Next steps:"
echo "   1. Wait for Home Assistant to fully start (2-3 minutes)"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Add the Jan MAX! integration"
echo "   4. Configure with IP: 192.168.1.26, Port: 62910"
echo ""
echo "🔍 To check logs: docker logs homeassistant"
echo "🔍 To check if integration is working: docker logs homeassistant | grep -i 'jan_max\|maxcube'"
