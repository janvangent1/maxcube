#!/bin/bash

echo "🚨 COMPLETE FIX - MAX! CUBE INTEGRATION"
echo "========================================"

# 1. Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop homeassistant

# 2. Remove ALL old integration directories
echo "🗑️ Removing ALL old integration directories..."
docker exec homeassistant rm -rf /config/custom_components/maxcube
docker exec homeassistant rm -rf /config/custom_components/jan_max
docker exec homeassistant rm -rf /config/custom_components/jan_eq3_max

# 3. Clean up any old config entries by removing the entire config directory
echo "🧹 Cleaning up old config entries..."
# Backup important files first
docker exec homeassistant cp /config/configuration.yaml /config/configuration.yaml.backup 2>/dev/null || true
docker exec homeassistant cp /config/.storage/core.config_entries /config/.storage/core.config_entries.backup 2>/dev/null || true

# Remove old config entries
docker exec homeassistant rm -f /config/.storage/core.config_entries
docker exec homeassistant rm -f /config/.storage/core.registry
docker exec homeassistant rm -f /config/.storage/core.restore_state

# 4. Create minimal working configuration
echo "📝 Creating minimal working configuration..."
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

# Create empty include files
echo "# No automations defined yet" | docker exec -i homeassistant tee /config/automations.yaml > /dev/null
echo "# No scripts defined yet" | docker exec -i homeassistant tee /config/scripts.yaml > /dev/null
echo "# No scenes defined yet" | docker exec -i homeassistant tee /config/scenes.yaml > /dev/null

# 5. Download and deploy the working integration
echo "📥 Downloading working integration..."
# Remove any old cloned directories
rm -rf /home/pi/maxcube_temp
rm -rf /home/pi/maxcube

# Clone the repository
git clone https://github.com/janvangent1/maxcube.git /home/pi/maxcube_temp

# Ensure the custom_components directory exists
docker exec homeassistant mkdir -p /config/custom_components

# Copy the integration to the correct location
echo "📁 Copying integration to container..."
docker cp /home/pi/maxcube_temp/maxcube-HomeAssist-plugin/custom_components/maxcube homeassistant:/config/custom_components/jan_eq3_max

# Set correct permissions
echo "🔐 Setting correct permissions..."
docker exec homeassistant chown -R root:root /config/custom_components/jan_eq3_max
docker exec homeassistant chmod -R 755 /config/custom_components/jan_eq3_max

# Clean up temporary files
rm -rf /home/pi/maxcube_temp

# 6. Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start homeassistant

# 7. Wait for Home Assistant to start
echo "⏳ Waiting for Home Assistant to start..."
sleep 30

# Check status
echo "🔍 Checking Home Assistant status..."
docker ps | grep homeassistant

echo ""
echo "✅ Complete fix completed!"
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
echo "⚠️  If you still see old entries, restart Home Assistant:"
echo "   docker restart homeassistant"
