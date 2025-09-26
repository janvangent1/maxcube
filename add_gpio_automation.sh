#!/bin/bash

echo "🔧 ADDING GPIO AUTOMATION"
echo "========================="

# Get container name
CONTAINER_NAME=$(docker ps --format "table {{.Names}}" | grep -v NAMES | head -1)
echo "Using container: $CONTAINER_NAME"

# Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop $CONTAINER_NAME

# Backup current configuration
echo "💾 Backing up current configuration..."
docker exec $CONTAINER_NAME cp /config/configuration.yaml /config/configuration.yaml.backup

# Add REST commands to configuration
echo "📝 Adding REST commands to configuration..."
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

# Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start $CONTAINER_NAME

echo "⏳ Waiting for Home Assistant to start..."
sleep 30

echo ""
echo "✅ GPIO REST commands added!"
echo "📋 Next steps:"
echo "   1. Wait 2-3 minutes for Home Assistant to fully start"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Go to Settings > Automations & Scenes"
echo "   4. Click 'Create Automation'"
echo "   5. Choose 'Start with an empty automation'"
echo ""
echo "🔧 Automation setup:"
echo "   Trigger 1: State change from 'off' to 'on' for heat demand switch"
echo "   Action 1: Call service 'rest_command.gpio_on'"
echo "   Trigger 2: State change from 'on' to 'off' for heat demand switch"
echo "   Action 2: Call service 'rest_command.gpio_off'"
echo ""
echo "🔍 To check if REST commands are loaded:"
echo "   Go to Developer Tools > Services and look for 'rest_command.gpio_on' and 'rest_command.gpio_off'"
