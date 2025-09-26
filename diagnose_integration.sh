#!/bin/bash

echo "🔍 DIAGNOSING INTEGRATION ISSUES"
echo "================================="

# Check if Home Assistant is running
echo "📊 Checking Home Assistant status..."
docker ps | grep homeassistant

# Check if integration directory exists
echo "📁 Checking integration directory..."
docker exec homeassistant ls -la /config/custom_components/

# Check if jan_eq3_max directory exists
echo "📂 Checking jan_eq3_max directory..."
docker exec homeassistant ls -la /config/custom_components/jan_eq3_max/

# Check manifest.json
echo "📋 Checking manifest.json..."
docker exec homeassistant cat /config/custom_components/jan_eq3_max/manifest.json

# Check if all required files exist
echo "📄 Checking required files..."
docker exec homeassistant ls -la /config/custom_components/jan_eq3_max/*.py

# Check Home Assistant logs for integration errors
echo "📝 Checking Home Assistant logs for integration errors..."
docker logs homeassistant 2>&1 | grep -i "jan_eq3_max\|maxcube\|error" | tail -20

# Check if integration is loaded
echo "🔍 Checking if integration is loaded..."
docker logs homeassistant 2>&1 | grep -i "custom integration.*jan_eq3_max"

# Check configuration
echo "⚙️ Checking configuration..."
docker exec homeassistant cat /config/configuration.yaml

echo ""
echo "✅ Diagnosis complete!"
echo "📋 If the integration is not showing up:"
echo "   1. Check the logs above for errors"
echo "   2. Restart Home Assistant: docker restart homeassistant"
echo "   3. Wait 2-3 minutes and try again"
echo "   4. Check if the integration appears in the UI"
