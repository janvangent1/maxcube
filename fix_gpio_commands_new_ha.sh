#!/bin/bash

echo "🔧 FIXING GPIO COMMANDS FOR NEW HOME ASSISTANT"
echo "=============================================="

# Get container name
CONTAINER_NAME=$(docker ps --format "table {{.Names}}" | grep -v NAMES | head -1)
echo "Using container: $CONTAINER_NAME"

# Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop $CONTAINER_NAME

# Backup current configuration
echo "💾 Backing up current configuration..."
docker exec $CONTAINER_NAME cp /config/configuration.yaml /config/configuration.yaml.backup

# Remove any existing rest_command section
echo "🗑️ Removing existing rest_command section..."
docker exec $CONTAINER_NAME sed -i '/^rest_command:/,/^[^ ]/d' /config/configuration.yaml

# Add the correct REST commands for new HA
echo "📝 Adding REST commands for new Home Assistant..."
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
echo "📋 Next steps for NEW Home Assistant:"
echo "   1. Wait 2-3 minutes for Home Assistant to fully start"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Go to Settings > Automations & Scenes"
echo "   4. Click 'Create Automation'"
echo "   5. Choose 'Start with an empty automation'"
echo ""
echo "🔧 Automation setup for NEW HA:"
echo "   Name: 'Heat Demand GPIO Control'"
echo "   "
echo "   Trigger 1:"
echo "   - Type: State"
echo "   - Entity: switch.heat_demand (or your heat demand switch)"
echo "   - From: off"
echo "   - To: on"
echo "   "
echo "   Action 1:"
echo "   - Type: Perform action"
echo "   - Service: rest_command.gpio_on"
echo "   "
echo "   Trigger 2:"
echo "   - Type: State"
echo "   - Entity: switch.heat_demand"
echo "   - From: on"
echo "   - To: off"
echo "   "
echo "   Action 2:"
echo "   - Type: Perform action"
echo "   - Service: rest_command.gpio_off"
echo ""
echo "🔍 To verify services are loaded:"
echo "   Go to Developer Tools > Services and search for 'rest_command'"
echo "   You should see 'gpio_on' and 'gpio_off'"
