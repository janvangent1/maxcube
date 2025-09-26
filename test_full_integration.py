#!/usr/bin/env python3
"""
Full integration test for MAX! Cube Home Assistant integration
Tests the integration with actual Home Assistant modules
"""

import sys
import os
import logging
import traceback

# Activate the virtual environment
venv_python = os.path.join(os.path.dirname(__file__), 'homeassistant_dev', 'Scripts', 'python.exe')
if not os.path.exists(venv_python):
    print("❌ Home Assistant virtual environment not found!")
    print("Run: python setup_dev_env.py")
    sys.exit(1)

# Add the maxcube library to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components', 'maxcube'))

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_homeassistant_imports():
    """Test Home Assistant imports."""
    print("🔍 Testing Home Assistant imports...")
    
    try:
        import homeassistant
        print("✅ Home Assistant imported")
        
        from homeassistant.config_entries import ConfigEntry
        print("✅ ConfigEntry imported")
        
        from homeassistant.core import HomeAssistant
        print("✅ HomeAssistant core imported")
        
        from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
        print("✅ DataUpdateCoordinator imported")
        
        from homeassistant.components.climate import ClimateEntity
        print("✅ ClimateEntity imported")
        
        from homeassistant.components.sensor import SensorEntity
        print("✅ SensorEntity imported")
        
        from homeassistant.components.switch import SwitchEntity
        print("✅ SwitchEntity imported")
        
        import voluptuous as vol
        print("✅ Voluptuous imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Home Assistant import error: {e}")
        traceback.print_exc()
        return False

def test_integration_imports():
    """Test integration imports with Home Assistant available."""
    print("\n🔍 Testing integration imports...")
    
    try:
        from custom_components.maxcube import const
        print("✅ const.py imported successfully")
        
        from custom_components.maxcube import connection
        print("✅ connection.py imported successfully")
        
        from custom_components.maxcube import cube
        print("✅ cube.py imported successfully")
        
        from custom_components.maxcube import coordinator
        print("✅ coordinator.py imported successfully")
        
        from custom_components.maxcube import config_flow
        print("✅ config_flow.py imported successfully")
        
        from custom_components.maxcube import climate
        print("✅ climate.py imported successfully")
        
        from custom_components.maxcube import sensor
        print("✅ sensor.py imported successfully")
        
        from custom_components.maxcube import switch
        print("✅ switch.py imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration import error: {e}")
        traceback.print_exc()
        return False

def test_config_flow_class():
    """Test config flow class instantiation."""
    print("\n🔍 Testing config flow class...")
    
    try:
        from custom_components.maxcube.config_flow import ConfigFlow
        
        # Check if class exists and has required methods
        if not hasattr(ConfigFlow, 'async_step_user'):
            print("❌ ConfigFlow missing async_step_user method")
            return False
        
        if not hasattr(ConfigFlow, 'VERSION'):
            print("❌ ConfigFlow missing VERSION attribute")
            return False
        
        print("✅ ConfigFlow class is valid")
        print(f"   Version: {ConfigFlow.VERSION}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config flow error: {e}")
        traceback.print_exc()
        return False

def test_coordinator_class():
    """Test coordinator class."""
    print("\n🔍 Testing coordinator class...")
    
    try:
        from custom_components.maxcube.coordinator import MaxCubeCoordinator
        
        # Check if class exists
        if not MaxCubeCoordinator:
            print("❌ MaxCubeCoordinator class not found")
            return False
        
        print("✅ MaxCubeCoordinator class is valid")
        
        return True
        
    except Exception as e:
        print(f"❌ Coordinator error: {e}")
        traceback.print_exc()
        return False

def test_maxcube_connection():
    """Test MAX! Cube connection."""
    print("\n🔍 Testing MAX! Cube connection...")
    
    try:
        from custom_components.maxcube.connection import MaxCubeConnection
        from custom_components.maxcube.cube import MaxCube
        
        # Test connection to your cube
        connection = MaxCubeConnection("192.168.1.26", 62910)
        cube = MaxCube(connection)
        
        print("✅ MAX! Cube connection successful")
        print(f"   RF Address: {cube.rf_address}")
        print(f"   Firmware: {cube.firmware_version}")
        print(f"   Devices: {len(cube.devices)}")
        print(f"   Rooms: {len(cube.rooms)}")
        
        return True
        
    except Exception as e:
        print(f"❌ MAX! Cube connection error: {e}")
        return False

def test_platform_functions():
    """Test platform setup functions."""
    print("\n🔍 Testing platform functions...")
    
    try:
        from custom_components.maxcube import climate, sensor, switch
        
        # Check for async_setup_entry functions
        if not hasattr(climate, 'async_setup_entry'):
            print("❌ climate.py missing async_setup_entry function")
            return False
        
        if not hasattr(sensor, 'async_setup_entry'):
            print("❌ sensor.py missing async_setup_entry function")
            return False
        
        if not hasattr(switch, 'async_setup_entry'):
            print("❌ switch.py missing async_setup_entry function")
            return False
        
        print("✅ All platform functions are valid")
        
        return True
        
    except Exception as e:
        print(f"❌ Platform functions error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 MAX! Cube Home Assistant Integration Full Test")
    print("=" * 60)
    
    tests = [
        ("Home Assistant Imports", test_homeassistant_imports),
        ("Integration Imports", test_integration_imports),
        ("Config Flow Class", test_config_flow_class),
        ("Coordinator Class", test_coordinator_class),
        ("Platform Functions", test_platform_functions),
        ("MAX! Cube Connection", test_maxcube_connection),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test PASSED")
        else:
            print(f"❌ {test_name} test FAILED")
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is ready for Home Assistant.")
        print("\n📋 Next steps:")
        print("1. Commit and push to GitHub")
        print("2. Update Home Assistant")
        print("3. Add the integration")
    else:
        print("⚠️ Some tests failed. Fix the issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
