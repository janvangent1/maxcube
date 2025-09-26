#!/bin/bash

echo "🚀 DEPLOYING MAX! CUBE INTEGRATION TO DOCKER"
echo "============================================="

# Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop homeassistant

# Remove old integration
echo "🗑️ Removing old integration..."
docker exec homeassistant rm -rf /config/custom_components/maxcube

# Copy integration to container
echo "📁 Copying integration to container..."
docker cp ./custom_components/maxcube homeassistant:/config/custom_components/

# Set correct permissions
echo "🔐 Setting correct permissions..."
docker exec homeassistant chown -R root:root /config/custom_components/maxcube
docker exec homeassistant chmod -R 755 /config/custom_components/maxcube

# Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start homeassistant

echo "⏳ Waiting for Home Assistant to start..."
sleep 30

# Check status
echo "🔍 Checking Home Assistant status..."
docker ps | grep homeassistant

echo ""
echo "✅ Deployment completed!"
echo "📋 Next steps:"
echo "   1. Wait for Home Assistant to fully start (2-3 minutes)"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Add the MAX! integration (not Jan MAX!)"
echo "   4. Configure with IP: 192.168.1.26, Port: 62910"
echo ""
echo "🔍 To check logs: docker logs homeassistant"
echo "🔍 To check if integration is working: docker logs homeassistant | grep -i 'maxcube'"
