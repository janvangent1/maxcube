#!/bin/bash

echo "🧪 TESTING INTEGRATION IMPORT"
echo "============================="

# Test if the integration can be imported
echo "📦 Testing Python import..."
docker exec homeassistant python3 -c "
import sys
sys.path.append('/config/custom_components')
try:
    import jan_eq3_max
    print('✅ Integration imported successfully')
    print(f'Domain: {jan_eq3_max.const.DOMAIN}')
    print(f'Name: {jan_eq3_max.manifest[\"name\"]}')
    print(f'Version: {jan_eq3_max.manifest[\"version\"]}')
except Exception as e:
    print(f'❌ Import failed: {e}')
    import traceback
    traceback.print_exc()
"

# Test if the config flow can be imported
echo "🔧 Testing config flow import..."
docker exec homeassistant python3 -c "
import sys
sys.path.append('/config/custom_components')
try:
    from jan_eq3_max.config_flow import ConfigFlow
    print('✅ Config flow imported successfully')
    print(f'Domain: {ConfigFlow.domain}')
    print(f'Version: {ConfigFlow.VERSION}')
except Exception as e:
    print(f'❌ Config flow import failed: {e}')
    import traceback
    traceback.print_exc()
"

# Test if the coordinator can be imported
echo "📊 Testing coordinator import..."
docker exec homeassistant python3 -c "
import sys
sys.path.append('/config/custom_components')
try:
    from jan_eq3_max.coordinator import MaxCubeCoordinator
    print('✅ Coordinator imported successfully')
except Exception as e:
    print(f'❌ Coordinator import failed: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "✅ Import tests complete!"
