#!/bin/bash
# MAX! Cube Integration - Quick Install Script
# Copy and paste this into your SSH terminal

echo "🚀 Installing MAX! Cube Integration..."

# Check if Home Assistant is running
if ! docker ps | grep -q homeassistant; then
    echo "❌ Home Assistant container not running!"
    echo "Please start it first: docker start homeassistant"
    exit 1
fi

# Create custom components directory
mkdir -p /home/pi/ha/custom_components

# Install MAX! Cube integration
cd /home/pi/ha/custom_components
rm -rf maxcube 2>/dev/null || true
git clone https://github.com/janvangent1/maxcube.git

# Set permissions
sudo chown -R pi:pi /home/pi/ha
chmod -R 755 /home/pi/ha/custom_components

# Restart Home Assistant
docker restart homeassistant

echo "✅ MAX! Cube integration installed!"
echo "🌐 Go to http://$(hostname -I | awk '{print $1}'):8123"
echo "📋 Add integration: Settings → Devices & Services → + Add Integration → Search 'MAX! Cube'"
