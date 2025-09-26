#!/bin/bash

echo "🔧 MANUAL DOCKER FIX"
echo "===================="

# 1. Check what containers are running
echo "🔍 Checking running containers..."
docker ps

# 2. Get the correct container name/ID
CONTAINER_NAME=$(docker ps --format "table {{.Names}}" | grep -v NAMES | head -1)
echo "Using container: $CONTAINER_NAME"

# 3. Download the integration files
echo "📥 Downloading integration files..."
rm -rf /home/pi/maxcube_temp
git clone https://github.com/janvangent1/maxcube.git /home/pi/maxcube_temp

# 4. Check what was downloaded
echo "📂 Checking downloaded files..."
ls -la /home/pi/maxcube_temp/
ls -la /home/pi/maxcube_temp/custom_components/

# 5. Stop Home Assistant
echo "🛑 Stopping Home Assistant..."
docker stop $CONTAINER_NAME

# 6. Remove old integration directories
echo "🗑️ Removing old integration directories..."
docker exec $CONTAINER_NAME rm -rf /config/custom_components/maxcube
docker exec $CONTAINER_NAME rm -rf /config/custom_components/jan_max
docker exec $CONTAINER_NAME rm -rf /config/custom_components/jan_eq3_max

# 7. Create custom_components directory
echo "📁 Creating custom_components directory..."
docker exec $CONTAINER_NAME mkdir -p /config/custom_components

# 8. Copy integration files
echo "📂 Copying integration files..."
docker cp /home/pi/maxcube_temp/custom_components/maxcube $CONTAINER_NAME:/config/custom_components/jan_eq3_max

# 9. Set permissions
echo "🔐 Setting permissions..."
docker exec $CONTAINER_NAME chown -R root:root /config/custom_components/jan_eq3_max
docker exec $CONTAINER_NAME chmod -R 755 /config/custom_components/jan_eq3_max

# 10. Verify files
echo "✅ Verifying files..."
docker exec $CONTAINER_NAME ls -la /config/custom_components/jan_eq3_max/

# 11. Start Home Assistant
echo "🚀 Starting Home Assistant..."
docker start $CONTAINER_NAME

# 12. Wait and check
echo "⏳ Waiting for Home Assistant to start..."
sleep 30

echo "🔍 Checking status..."
docker ps | grep $CONTAINER_NAME

echo ""
echo "✅ Manual fix completed!"
echo "📋 Next steps:"
echo "   1. Wait 3-5 minutes for Home Assistant to fully start"
echo "   2. Go to http://192.168.1.190:8123"
echo "   3. Go to Settings > Devices & Services"
echo "   4. Click 'Add Integration'"
echo "   5. Search for 'Jan eQ-3 MAX!'"
echo "   6. Configure with IP: 192.168.1.26, Port: 62910"
echo ""
echo "🔍 To check logs: docker logs $CONTAINER_NAME"
echo "🔍 To check if integration is working: docker logs $CONTAINER_NAME | grep -i 'jan_eq3_max'"
