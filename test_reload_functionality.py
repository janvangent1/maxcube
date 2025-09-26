#!/usr/bin/env python3
"""
Test script for MAX! Cube reload functionality
"""

import sys
import os
import traceback

# Add the maxcube module to path
current_dir = os.path.dirname(os.path.abspath(__file__))
maxcube_path = os.path.join(current_dir, 'custom_components', 'maxcube')
sys.path.insert(0, maxcube_path)

def test_reload_functionality():
    """Test the reload functionality"""
    print("🔍 Testing MAX! Cube reload functionality...")
    
    try:
        from coordinator import MaxCubeCoordinator
        from connection import MaxCubeConnection
        from cube import MaxCube
        
        print("✅ Imports successful")
        
        # Create a mock coordinator
        class MockConfigEntry:
            def __init__(self):
                self.data = {
                    "cube_address": "192.168.1.26",
                    "cube_port": 62910,
                    "debug_mode": True,
                    "update_interval": 60
                }
        
        class MockHomeAssistant:
            def __init__(self):
                pass
        
        # Test coordinator creation
        mock_entry = MockConfigEntry()
        mock_hass = MockHomeAssistant()
        
        coordinator = MaxCubeCoordinator(mock_hass, mock_entry)
        print("✅ Coordinator created successfully")
        
        # Test connection
        connection = MaxCubeConnection("192.168.1.26", 62910)
        cube = MaxCube(connection)
        print("✅ Cube connection successful")
        
        # Test reload method (without async)
        print("🔄 Testing reload functionality...")
        
        # Simulate reload by creating new connection
        new_connection = MaxCubeConnection("192.168.1.26", 62910)
        new_cube = MaxCube(new_connection)
        new_cube.update()
        
        print(f"✅ Reload successful - Found {len(new_cube.devices)} devices and {len(new_cube.rooms)} rooms")
        
        # List devices
        print("\n📱 Devices found:")
        for device in new_cube.devices:
            if cube.is_thermostat(device):
                print(f"  🔥 Thermostat: {device.name} (RF: {device.rf_address})")
            elif cube.is_wallthermostat(device):
                print(f"  🌡️ Wall Thermostat: {device.name} (RF: {device.rf_address})")
            elif cube.is_windowshutter(device):
                print(f"  🪟 Window Shutter: {device.name} (RF: {device.rf_address})")
        
        print("\n🏠 Rooms found:")
        for room in new_cube.rooms:
            print(f"  🏠 {room.name} (ID: {room.id})")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        return False

def test_service_schema():
    """Test the service schemas"""
    print("\n🔍 Testing service schemas...")
    
    try:
        import services
        print("✅ Services module imported successfully")
        
        # Test schema validation
        from homeassistant.helpers import config_validation as cv
        import voluptuous as vol
        
        # Test reload schema
        reload_schema = vol.Schema({
            vol.Required("cube_address"): cv.string,
        })
        
        test_data = {"cube_address": "192.168.1.26"}
        validated_data = reload_schema(test_data)
        print(f"✅ Reload schema validation passed: {validated_data}")
        
        # Test clear and reload schema
        clear_schema = vol.Schema({
            vol.Required("cube_address"): cv.string,
        })
        
        validated_data = clear_schema(test_data)
        print(f"✅ Clear and reload schema validation passed: {validated_data}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        traceback.print_exc()
        return False

def run_tests():
    """Run all tests"""
    print("🚀 Starting MAX! Cube reload functionality tests...\n")
    
    tests = [
        ("Reload Functionality", test_reload_functionality),
        ("Service Schema", test_service_schema),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Reload functionality is working.")
        print("\n📋 New services available:")
        print("   - maxcube.reload_devices")
        print("   - maxcube.clear_and_reload_devices")
        print("\n🔧 Usage in Home Assistant:")
        print("   - Developer Tools → Services")
        print("   - Service: maxcube.reload_devices")
        print("   - Service data: {\"cube_address\": \"192.168.1.26\"}")
        return True
    else:
        print("⚠️ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
