#!/bin/bash

echo "🔍 CHECKING REST COMMAND CONFIGURATION"
echo "======================================="

# Get container name
CONTAINER_NAME=$(docker ps --format "table {{.Names}}" | grep -v NAMES | head -1)
echo "Using container: $CONTAINER_NAME"

# Check current configuration
echo "📋 Checking current configuration..."
docker exec $CONTAINER_NAME cat /config/configuration.yaml

echo ""
echo "🔍 Looking for rest_command section..."
docker exec $CONTAINER_NAME grep -A 20 "rest_command:" /config/configuration.yaml

echo ""
echo "📝 How rest_command works:"
echo "   The URL is defined in the rest_command configuration"
echo "   The 'command' parameter gets appended to the URL"
echo "   So if URL is 'http://192.168.1.190/control?cmd='"
echo "   And command is 'gpio,5,1'"
echo "   The final URL becomes 'http://192.168.1.190/control?cmd=gpio,5,1'"
echo ""
echo "🔧 If gpio_control doesn't exist, we need to add it to configuration.yaml"
