#!/bin/bash
# Automated MAX! Cube Integration Update Script
# This script will automatically update your Home Assistant integration
# Run this directly on your Home Assistant instance

set -e  # Exit on any error

echo "🚀 MAX! Cube Integration Auto-Update Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -d "/config" ]; then
    print_error "Not in Home Assistant config directory!"
    print_status "Changing to /config directory..."
    cd /config
fi

print_status "Starting MAX! Cube integration update..."

# Step 1: Remove old integration
print_status "Removing old integration files..."
if [ -d "custom_components/maxcube" ]; then
    rm -rf custom_components/maxcube
    print_success "Old integration removed"
else
    print_warning "No old integration found"
fi

# Step 2: Clear cached data
print_status "Clearing cached configuration data..."
rm -rf .storage/core.config_entries 2>/dev/null || true
rm -rf .storage/core.device_registry 2>/dev/null || true
rm -rf .storage/core.entity_registry 2>/dev/null || true
print_success "Cached data cleared"

# Step 3: Download updated integration
print_status "Downloading updated integration from GitHub..."
if [ -d "temp_maxcube" ]; then
    rm -rf temp_maxcube
fi

git clone https://github.com/janvangent1/maxcube.git temp_maxcube
print_success "Integration downloaded"

# Step 4: Install integration
print_status "Installing updated integration..."
mv temp_maxcube/custom_components/maxcube ./
rm -rf temp_maxcube
print_success "Integration installed"

# Step 5: Verify the fix is present
print_status "Verifying the None comparison fix..."
if grep -q "room = str(thermostat.room_id) if thermostat.room_id is not None else '00'" custom_components/maxcube/cube.py; then
    print_success "None comparison fix is present"
else
    print_error "None comparison fix NOT found!"
    exit 1
fi

# Step 6: Check file permissions
print_status "Setting correct file permissions..."
chmod -R 755 custom_components/maxcube/
print_success "File permissions set"

# Step 7: Restart Home Assistant
print_status "Restarting Home Assistant..."
ha core restart
print_success "Home Assistant restarted"

echo ""
echo "🎉 UPDATE COMPLETE!"
echo "=================="
echo ""
print_success "The MAX! Cube integration has been updated successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Go to Settings → Devices & Services"
echo "   2. Click '+ Add Integration'"
echo "   3. Search for 'MAX! Cube'"
echo "   4. Configure with your settings:"
echo "      - Cube Address: 192.168.1.26"
echo "      - Port: 62910"
echo "      - Enable all options you want"
echo ""
print_success "The '>' not supported error should now be fixed!"
echo ""
echo "🔍 If you still get errors, check the logs:"
echo "   Settings → System → Logs"
echo ""
