#!/usr/bin/env python3
"""
Test script for MAX! Cube Home Assistant integration
Tests the integration locally before deploying to Home Assistant
"""

import sys
import os
import logging
import traceback

# Add the maxcube library to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components', 'maxcube'))

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test all imports to catch import errors."""
    print("🔍 Testing imports...")
    
    try:
        # Test basic imports
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
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_manifest():
    """Test manifest.json validity."""
    print("\n🔍 Testing manifest.json...")
    
    try:
        import json
        
        manifest_path = os.path.join(os.path.dirname(__file__), 'custom_components', 'maxcube', 'manifest.json')
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        required_fields = ['domain', 'name', 'version', 'config_flow']
        
        for field in required_fields:
            if field not in manifest:
                print(f"❌ Missing required field: {field}")
                return False
        
        print("✅ manifest.json is valid")
        print(f"   Domain: {manifest['domain']}")
        print(f"   Name: {manifest['name']}")
        print(f"   Version: {manifest['version']}")
        print(f"   Config Flow: {manifest['config_flow']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Manifest error: {e}")
        return False

def test_config_flow():
    """Test config flow class."""
    print("\n🔍 Testing config flow...")
    
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

def main():
    """Run all tests."""
    print("🧪 MAX! Cube Home Assistant Integration Test")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Manifest", test_manifest),
        ("Config Flow", test_config_flow),
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
    else:
        print("⚠️ Some tests failed. Fix the issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
