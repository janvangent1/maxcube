#!/bin/bash
# MAX! Cube Integration - Complete Installation Script
# Copy and paste this entire script into your SSH terminal

set -e  # Exit on any error

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

echo "🚀 MAX! Cube Integration - Complete Installation Script"
echo "======================================================"
echo ""

# Step 1: Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y
print_success "System updated"

# Step 2: Install useful tools
print_status "Installing useful tools..."
sudo apt install -y git curl wget nano htop tree
print_success "Tools installed"

# Step 3: Install Samba for easy file access
print_status "Installing Samba for file sharing..."
sudo apt install -y samba samba-common-bin
print_success "Samba installed"

# Step 4: Configure Samba
print_status "Configuring Samba..."
sudo tee -a /etc/samba/smb.conf > /dev/null << 'EOF'

# Home Assistant share
[homeassistant]
   comment = Home Assistant Configuration
   path = /home/pi/ha
   browseable = yes
   read only = no
   guest ok = no
   create mask = 0775
   directory mask = 0775
   valid users = pi

# Pi home directory share
[pi]
   comment = Pi Home Directory
   path = /home/pi
   browseable = yes
   read only = no
   guest ok = no
   create mask = 0775
   directory mask = 0775
   valid users = pi
EOF

# Set Samba password for pi user
print_status "Setting up Samba user..."
echo "Please set a password for Samba access (you can use the same as your Pi password):"
sudo smbpasswd -a pi

# Restart Samba
sudo systemctl restart smbd
sudo systemctl enable smbd
print_success "Samba configured"

# Step 5: Check if Home Assistant is running
print_status "Checking Home Assistant container..."
if docker ps | grep -q homeassistant; then
    print_success "Home Assistant container is running"
    HA_CONFIG_PATH="/home/pi/ha"
else
    print_warning "Home Assistant container not found. Please make sure it's running first."
    print_status "You can start it with: docker start homeassistant"
    exit 1
fi

# Step 6: Create custom components directory
print_status "Setting up custom components directory..."
mkdir -p "$HA_CONFIG_PATH/custom_components"
print_success "Custom components directory created"

# Step 7: Install MAX! Cube integration
print_status "Installing MAX! Cube integration..."
cd "$HA_CONFIG_PATH/custom_components"

# Remove old integration if it exists
if [ -d "maxcube" ]; then
    print_warning "Removing old MAX! Cube integration..."
    rm -rf maxcube
fi

# Clone the latest integration
git clone https://github.com/janvangent1/maxcube.git
print_success "MAX! Cube integration installed"

# Step 8: Set correct permissions
print_status "Setting correct permissions..."
sudo chown -R pi:pi "$HA_CONFIG_PATH"
chmod -R 755 "$HA_CONFIG_PATH/custom_components"
print_success "Permissions set"

# Step 9: Restart Home Assistant
print_status "Restarting Home Assistant container..."
docker restart homeassistant
print_success "Home Assistant restarted"

# Step 10: Wait for Home Assistant to start
print_status "Waiting for Home Assistant to start (30 seconds)..."
sleep 30

# Step 11: Check if Home Assistant is accessible
print_status "Checking Home Assistant accessibility..."
if curl -s http://localhost:8123 > /dev/null; then
    print_success "Home Assistant is accessible"
else
    print_warning "Home Assistant might still be starting up"
fi

# Step 12: Create useful aliases
print_status "Creating useful aliases..."
cat >> ~/.bashrc << 'EOF'

# Home Assistant aliases
alias ha-logs='docker logs homeassistant'
alias ha-restart='docker restart homeassistant'
alias ha-stop='docker stop homeassistant'
alias ha-start='docker start homeassistant'
alias ha-status='docker ps | grep homeassistant'
alias ha-update='cd /home/pi/ha/custom_components/maxcube && git pull origin master && docker restart homeassistant'

# MAX! Cube aliases
alias maxcube-update='cd /home/pi/ha/custom_components/maxcube && git pull origin master && docker restart homeassistant'
alias maxcube-logs='docker logs homeassistant | grep -i maxcube'

# System aliases
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
EOF

print_success "Aliases created"

# Step 13: Create update script
print_status "Creating update script..."
cat > ~/update-maxcube.sh << 'EOF'
#!/bin/bash
echo "🔄 Updating MAX! Cube integration..."
cd /home/pi/ha/custom_components/maxcube
git pull origin master
echo "✅ Integration updated"
docker restart homeassistant
echo "✅ Home Assistant restarted"
echo "🎉 Update complete!"
EOF

chmod +x ~/update-maxcube.sh
print_success "Update script created"

# Step 14: Display completion information
echo ""
echo "🎉 INSTALLATION COMPLETE!"
echo "========================"
echo ""
print_success "MAX! Cube integration installed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Go to http://$(hostname -I | awk '{print $1}'):8123"
echo "   2. Go to Settings → Devices & Services"
echo "   3. Click '+ Add Integration'"
echo "   4. Search for 'MAX! Cube'"
echo "   5. Configure with your settings:"
echo "      - Cube Address: 192.168.1.26"
echo "      - Port: 62910"
echo "      - Enable all options you want"
echo ""
echo "🔧 Useful commands:"
echo "   - ha-logs          # View Home Assistant logs"
echo "   - ha-restart       # Restart Home Assistant"
echo "   - maxcube-update    # Update MAX! Cube integration"
echo "   - maxcube-logs      # View MAX! Cube specific logs"
echo "   - ~/update-maxcube.sh # Run update script"
echo ""
echo "📁 File access:"
echo "   - Samba share: \\\\$(hostname -I | awk '{print $1}')\\pi"
echo "   - Home Assistant config: /home/pi/ha"
echo "   - MAX! Cube integration: /home/pi/ha/custom_components/maxcube"
echo ""
echo "🔄 To update the integration in the future:"
echo "   ./update-maxcube.sh"
echo ""
print_success "Installation completed successfully!"
