#!/bin/bash
# MAX! Cube Integration - Update Script
# Copy and paste this to update your integration

echo "🔄 Updating MAX! Cube integration..."

# Check if integration exists
if [ ! -d "/home/pi/ha/custom_components/maxcube" ]; then
    echo "❌ MAX! Cube integration not found!"
    echo "Please run the installation script first."
    exit 1
fi

# Update the integration
cd /home/pi/ha/custom_components/maxcube
git pull origin master

# Set permissions
sudo chown -R pi:pi /home/pi/ha/custom_components/maxcube
chmod -R 755 /home/pi/ha/custom_components/maxcube

# Restart Home Assistant
docker restart homeassistant

echo "✅ Update complete!"
echo "🔄 Home Assistant is restarting..."
echo "⏳ Wait about 30 seconds before accessing Home Assistant"
