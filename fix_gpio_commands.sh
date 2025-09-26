#!/bin/bash

echo "🔧 FIXING GPIO COMMANDS"
echo "======================="

# Get container name
CONTAINER_NAME=$(docker ps --format "table {{.Names}}" | grep -v NAMES | head -1)
echo "Using container: $CONTAINER_NAME"

# Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop $CONTAINER_NAME

# Backup current configuration
echo "💾 Backing up current configuration..."
docker exec $CONTAINER_NAME cp /config/configuration.yaml /config/configuration.yaml.backup

# Check current configuration
echo "📋 Checking current configuration..."
docker exec $CONTAINER_NAME cat /config/configuration.yaml

# Remove any existing rest_command section
echo "🗑️ Removing existing rest_command section..."
docker exec $CONTAINER_NAME sed -i '/^rest_command:/,/^[^ ]/d' /config/configuration.yaml

# Add the correct REST commands
echo "📝 Adding correct REST commands..."
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

# Show the updated configuration
echo "📋 Updated configuration:"
docker exec $CONTAINER_NAME cat /config/configuration.yaml

# Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start $CONTAINER_NAME

echo "⏳ Waiting for Home Assistant to start..."
sleep 30

echo ""
echo "✅ GPIO REST commands fixed!"
echo "📋 Next steps:"
echo "   1. Wait 2-3 minutes for Home Assistant to fully start"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Go to Developer Tools > Services"
echo "   4. Look for 'rest_command.gpio_on' and 'rest_command.gpio_off'"
echo ""
echo "🔍 If you still don't see them:"
echo "   1. Go to Developer Tools > Services"
echo "   2. Search for 'rest_command'"
echo "   3. You should see both 'gpio_on' and 'gpio_off'"
echo ""
echo "🔧 Then create the automation:"
echo "   Trigger: State change of heat demand switch"
echo "   Action: Call service 'rest_command.gpio_on' or 'rest_command.gpio_off'"
