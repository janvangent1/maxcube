#!/bin/bash

echo "🐳 COMPLETE DOCKER INSTALLATION"
echo "==============================="

# 1. Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop homeassistant

# 2. Remove ALL old integration directories INSIDE the container
echo "🗑️ Removing ALL old integration directories INSIDE container..."
docker exec homeassistant rm -rf /config/custom_components/maxcube
docker exec homeassistant rm -rf /config/custom_components/jan_max
docker exec homeassistant rm -rf /config/custom_components/jan_eq3_max

# 3. Clean up old config entries INSIDE the container
echo "🧹 Cleaning up old config entries INSIDE container..."
docker exec homeassistant rm -f /config/.storage/core.config_entries
docker exec homeassistant rm -f /config/.storage/core.registry
docker exec homeassistant rm -f /config/.storage/core.restore_state
docker exec homeassistant rm -f /config/.storage/core.entity_registry

# 4. Create minimal working configuration INSIDE the container
echo "📝 Creating minimal working configuration INSIDE container..."
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

# Create empty include files INSIDE the container
echo "# No automations defined yet" | docker exec -i homeassistant tee /config/automations.yaml > /dev/null
echo "# No scripts defined yet" | docker exec -i homeassistant tee /config/scripts.yaml > /dev/null
echo "# No scenes defined yet" | docker exec -i homeassistant tee /config/scenes.yaml > /dev/null

# 5. Download the integration files to host first
echo "📥 Downloading integration files..."
rm -rf /home/pi/maxcube_temp
git clone https://github.com/janvangent1/maxcube.git /home/pi/maxcube_temp

# 6. Ensure the custom_components directory exists INSIDE the container
echo "📁 Ensuring custom_components directory exists INSIDE container..."
docker exec homeassistant mkdir -p /config/custom_components

# 7. Copy ALL integration files INSIDE the container
echo "📂 Copying ALL integration files INSIDE container..."
docker cp /home/pi/maxcube_temp/maxcube-HomeAssist-plugin/custom_components/maxcube homeassistant:/config/custom_components/jan_eq3_max

# 8. Set correct permissions INSIDE the container
echo "🔐 Setting correct permissions INSIDE container..."
docker exec homeassistant chown -R root:root /config/custom_components/jan_eq3_max
docker exec homeassistant chmod -R 755 /config/custom_components/jan_eq3_max

# 9. Verify the files are there INSIDE the container
echo "✅ Verifying integration files INSIDE container..."
docker exec homeassistant ls -la /config/custom_components/jan_eq3_max/
docker exec homeassistant ls -la /config/custom_components/jan_eq3_max/*.py

# 10. Clean up temporary files
rm -rf /home/pi/maxcube_temp

# 11. Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start homeassistant

# 12. Wait for Home Assistant to start
echo "⏳ Waiting for Home Assistant to start..."
sleep 30

# Check status
echo "🔍 Checking Home Assistant status..."
docker ps | grep homeassistant

# Check if integration is loaded
echo "🔍 Checking if integration is loaded..."
sleep 10
docker logs homeassistant 2>&1 | grep -i "jan_eq3_max" | tail -5

echo ""
echo "✅ Complete installation completed INSIDE Docker container!"
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
echo "⚠️  If you still don't see the integration, restart Home Assistant:"
echo "   docker restart homeassistant"
