#!/bin/bash
# Update MAX! Cube integration on Home Assistant
# Run this script on your Home Assistant instance

echo "🔄 Updating MAX! Cube integration..."

# Step 1: Remove old integration
echo "🗑️ Removing old integration..."
rm -rf /config/custom_components/maxcube

# Step 2: Clear cached data
echo "🧹 Clearing cached data..."
rm -rf /config/.storage/core.config_entries
rm -rf /config/.storage/core.device_registry
rm -rf /config/.storage/core.entity_registry

# Step 3: Clone updated integration
echo "📥 Downloading updated integration..."
cd /config
git clone https://github.com/janvangent1/maxcube.git temp_maxcube

# Step 4: Install integration
echo "📦 Installing integration..."
mv temp_maxcube/custom_components/maxcube ./
rm -rf temp_maxcube

# Step 5: Verify installation
echo "✅ Verifying installation..."
if [ -f "/config/custom_components/maxcube/cube.py" ]; then
    echo "✅ Integration files installed successfully"
    
    # Check if our fix is in the file
    if grep -q "room = str(thermostat.room_id) if thermostat.room_id is not None else '00'" /config/custom_components/maxcube/cube.py; then
        echo "✅ None comparison fix is present"
    else
        echo "❌ None comparison fix NOT found!"
        exit 1
    fi
else
    echo "❌ Integration installation failed!"
    exit 1
fi

# Step 6: Restart Home Assistant
echo "🔄 Restarting Home Assistant..."
ha core restart

echo "🎉 Update complete! The integration should now work without the None comparison error."
echo "📋 Next steps:"
echo "   1. Go to Settings → Devices & Services"
echo "   2. Click '+ Add Integration'"
echo "   3. Search for 'MAX! Cube'"
echo "   4. Configure with your settings"
