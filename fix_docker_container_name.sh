#!/bin/bash

echo "🐳 FIXING DOCKER CONTAINER NAME"
echo "==============================="

# 1. Check what containers are running
echo "🔍 Checking running containers..."
docker ps

# 2. Get the correct container name/ID
echo "📋 Getting container name/ID..."
CONTAINER_NAME=$(docker ps --format "table {{.Names}}" | grep -v NAMES | head -1)
CONTAINER_ID=$(docker ps --format "table {{.ID}}" | grep -v CONTAINER | head -1)

echo "Container Name: $CONTAINER_NAME"
echo "Container ID: $CONTAINER_ID"

# 3. Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop $CONTAINER_NAME

# 4. Remove ALL old integration directories INSIDE the container
echo "🗑️ Removing ALL old integration directories INSIDE container..."
docker exec $CONTAINER_NAME rm -rf /config/custom_components/maxcube
docker exec $CONTAINER_NAME rm -rf /config/custom_components/jan_max
docker exec $CONTAINER_NAME rm -rf /config/custom_components/jan_eq3_max

# 5. Clean up old config entries INSIDE the container
echo "🧹 Cleaning up old config entries INSIDE container..."
docker exec $CONTAINER_NAME rm -f /config/.storage/core.config_entries
docker exec $CONTAINER_NAME rm -f /config/.storage/core.registry
docker exec $CONTAINER_NAME rm -f /config/.storage/core.restore_state
docker exec $CONTAINER_NAME rm -f /config/.storage/core.entity_registry

# 6. Create minimal working configuration INSIDE the container
echo "📝 Creating minimal working configuration INSIDE container..."
cat <<EOF | docker exec -i $CONTAINER_NAME tee /config/configuration.yaml > /dev/null
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
echo "# No automations defined yet" | docker exec -i $CONTAINER_NAME tee /config/automations.yaml > /dev/null
echo "# No scripts defined yet" | docker exec -i $CONTAINER_NAME tee /config/scripts.yaml > /dev/null
echo "# No scenes defined yet" | docker exec -i $CONTAINER_NAME tee /config/scenes.yaml > /dev/null

# 7. Download the integration files to host first
echo "📥 Downloading integration files..."
rm -rf /home/pi/maxcube_temp
git clone https://github.com/janvangent1/maxcube.git /home/pi/maxcube_temp

# 8. Check what was downloaded
echo "📂 Checking downloaded files..."
ls -la /home/pi/maxcube_temp/
ls -la /home/pi/maxcube_temp/maxcube-HomeAssist-plugin/

# 9. Ensure the custom_components directory exists INSIDE the container
echo "📁 Ensuring custom_components directory exists INSIDE container..."
docker exec $CONTAINER_NAME mkdir -p /config/custom_components

# 10. Copy ALL integration files INSIDE the container
echo "📂 Copying ALL integration files INSIDE container..."
docker cp /home/pi/maxcube_temp/maxcube-HomeAssist-plugin/custom_components/maxcube $CONTAINER_NAME:/config/custom_components/jan_eq3_max

# 11. Set correct permissions INSIDE the container
echo "🔐 Setting correct permissions INSIDE container..."
docker exec $CONTAINER_NAME chown -R root:root /config/custom_components/jan_eq3_max
docker exec $CONTAINER_NAME chmod -R 755 /config/custom_components/jan_eq3_max

# 12. Verify the files are there INSIDE the container
echo "✅ Verifying integration files INSIDE container..."
docker exec $CONTAINER_NAME ls -la /config/custom_components/jan_eq3_max/
docker exec $CONTAINER_NAME ls -la /config/custom_components/jan_eq3_max/*.py

# 13. Clean up temporary files
rm -rf /home/pi/maxcube_temp

# 14. Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start $CONTAINER_NAME

# 15. Wait for Home Assistant to start
echo "⏳ Waiting for Home Assistant to start..."
sleep 30

# Check status
echo "🔍 Checking Home Assistant status..."
docker ps | grep $CONTAINER_NAME

# Check if integration is loaded
echo "🔍 Checking if integration is loaded..."
sleep 10
docker logs $CONTAINER_NAME 2>&1 | grep -i "jan_eq3_max" | tail -5

echo ""
echo "✅ Installation completed INSIDE Docker container!"
echo "📋 Next steps:"
echo "   1. Wait for Home Assistant to fully start (3-5 minutes)"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Complete the initial setup if prompted"
echo "   4. Go to Settings > Devices & Services"
echo "   5. Click 'Add Integration'"
echo "   6. Search for 'Jan eQ-3 MAX!'"
echo "   7. Configure with IP: 192.168.1.26, Port: 62910"
echo ""
echo "🔍 To check logs: docker logs $CONTAINER_NAME"
echo "🔍 To check if integration is working: docker logs $CONTAINER_NAME | grep -i 'jan_eq3_max'"
echo ""
echo "⚠️  If you still don't see the integration, restart Home Assistant:"
echo "   docker restart $CONTAINER_NAME"
