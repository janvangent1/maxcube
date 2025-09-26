#!/bin/bash

echo "🐳 VERIFYING AND FIXING GPIO INSIDE DOCKER"
echo "=========================================="

# Get container name
CONTAINER_NAME=$(docker ps --format "table {{.Names}}" | grep -v NAMES | head -1)
echo "Using container: $CONTAINER_NAME"

# Check current configuration INSIDE the container
echo "📋 Checking current configuration INSIDE container..."
docker exec $CONTAINER_NAME cat /config/configuration.yaml

# Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop $CONTAINER_NAME

# Backup current configuration INSIDE the container
echo "💾 Backing up current configuration INSIDE container..."
docker exec $CONTAINER_NAME cp /config/configuration.yaml /config/configuration.yaml.backup

# Remove any existing rest_command section INSIDE the container
echo "🗑️ Removing existing rest_command section INSIDE container..."
docker exec $CONTAINER_NAME sed -i '/^rest_command:/,/^[^ ]/d' /config/configuration.yaml

# Add the REST commands INSIDE the container
echo "📝 Adding REST commands INSIDE container..."
cat <<EOF | docker exec -i $CONTAINER_NAME tee -a /config/configuration.yaml > /dev/null

# REST Commands for GPIO control
rest_command:
  gpio_on:
    url: "http://192.168.1.190/control?cmd=gpio,5,1"
    method: GET
    timeout: 10
  gpio_off:
    url: "http://192.168.1.190/control?cmd=gpio,5,0"
    method: GET
    timeout: 10
EOF

# Verify the configuration was added INSIDE the container
echo "✅ Verifying configuration INSIDE container..."
docker exec $CONTAINER_NAME cat /config/configuration.yaml

# Check if the rest_command section exists INSIDE the container
echo "🔍 Checking if rest_command section exists INSIDE container..."
docker exec $CONTAINER_NAME grep -A 10 "rest_command:" /config/configuration.yaml

# Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start $CONTAINER_NAME

echo "⏳ Waiting for Home Assistant to start..."
sleep 30

# Check Home Assistant logs for any errors
echo "📝 Checking Home Assistant logs for errors..."
docker logs $CONTAINER_NAME 2>&1 | grep -i "rest_command\|error" | tail -10

echo ""
echo "✅ GPIO configuration added INSIDE Docker container!"
echo "📋 Next steps:"
echo "   1. Wait 2-3 minutes for Home Assistant to fully start"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Go to Developer Tools > Services"
echo "   4. Search for 'rest_command'"
echo "   5. You should see 'gpio_on' and 'gpio_off'"
echo ""
echo "🔍 If you still don't see them:"
echo "   1. Check the logs above for any errors"
echo "   2. Go to Developer Tools > Services"
echo "   3. Look for any services starting with 'rest_command'"
echo "   4. If nothing appears, restart Home Assistant: docker restart $CONTAINER_NAME"
echo ""
echo "🔧 Alternative approach - use the existing gpio_control:"
echo "   If rest_command services don't appear, you can use the existing gpio_control"
echo "   and pass the command as a parameter in the automation"
