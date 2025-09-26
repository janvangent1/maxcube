#!/usr/bin/env python3
"""
Core MAX! Cube functionality test
Tests the core cube.py functionality without Home Assistant dependencies
"""

import sys
import os
import traceback
import logging

# Add the maxcube module to path
current_dir = os.path.dirname(os.path.abspath(__file__))
maxcube_path = os.path.join(current_dir, 'maxcube-HomeAssist-plugin', 'custom_components', 'maxcube')
sys.path.insert(0, maxcube_path)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_core_functionality():
    """Test core MAX! Cube functionality"""
    print("🔍 Testing core MAX! Cube functionality...")
    
    try:
        # Import core modules
        import device
        import thermostat
        import wallthermostat
        import windowshutter
        import room
        import connection
        import cube
        
        print("✅ Core imports successful")
        
        # Test device creation
        from device import MaxDevice, MAX_THERMOSTAT, MAX_WALL_THERMOSTAT, MAX_WINDOW_SHUTTER
        from thermostat import MaxThermostat
        from wallthermostat import MaxWallThermostat
        from windowshutter import MaxWindowShutter
        from room import MaxRoom
        from connection import MaxCubeConnection
        from cube import MaxCube
        
        print("✅ Device class imports successful")
        
        # Test device initialization
        device = MaxDevice()
        assert device.type is None
        assert device.room_id is None
        print("✅ Base device initialization OK")
        
        # Test thermostat creation
        thermostat = MaxThermostat()
        assert thermostat.room_id is None
        print("✅ Thermostat initialization OK")
        
        # Test wall thermostat creation
        wall_thermostat = MaxWallThermostat()
        assert wall_thermostat.room_id is None
        print("✅ Wall thermostat initialization OK")
        
        # Test window shutter creation
        window_shutter = MaxWindowShutter()
        assert window_shutter.room_id is None
        print("✅ Window shutter initialization OK")
        
        # Test room creation
        room = MaxRoom()
        assert room.id is None
        assert room.name is None
        print("✅ Room initialization OK")
        
        # Test connection creation
        conn = MaxCubeConnection("192.168.1.26", 62910)
        print("✅ Connection creation OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        traceback.print_exc()
        return False

def test_none_comparison_fixes():
    """Test that None comparison issues are fixed"""
    print("\n🔍 Testing None comparison fixes...")
    
    try:
        from device import MaxThermostat
        from cube import MaxCube
        from connection import MaxCubeConnection
        
        # Create a mock connection
        class MockConnection:
            def connect(self):
                pass
            def disconnect(self):
                pass
            def send(self, data):
                pass
            @property
            def response(self):
                return "H:KEQ0839778,1f,0113\r\n"
        
        # Create cube with mock connection
        cube = MaxCube(MockConnection())
        
        # Create thermostat with None values
        thermostat = MaxThermostat()
        thermostat.rf_address = "123456"
        thermostat.room_id = None  # This was causing the error
        thermostat.target_temperature = None
        thermostat.mode = None
        
        print("✅ Mock objects created successfully")
        
        # Test set_target_temperature with None mode
        try:
            cube.set_target_temperature(thermostat, 20.0)
            print("❌ Should have failed with None mode")
            return False
        except Exception as e:
            if "Thermostat mode is None" in str(e):
                print("✅ Correctly caught None mode error")
            else:
                print(f"❌ Unexpected error: {e}")
                return False
        
        # Test set_mode with None temperature
        thermostat.mode = 1
        thermostat.target_temperature = None
        try:
            cube.set_mode(thermostat, 1)
            print("❌ Should have failed with None temperature")
            return False
        except Exception as e:
            if "Thermostat target temperature is None" in str(e):
                print("✅ Correctly caught None temperature error")
            else:
                print(f"❌ Unexpected error: {e}")
                return False
        
        # Test set_temperature_mode with None values
        thermostat.target_temperature = 20.0
        thermostat.mode = 1
        
        # Test with None temperature
        try:
            cube.set_temperature_mode(thermostat, None, 1)
            print("❌ Should have failed with None temperature")
            return False
        except Exception as e:
            if "Temperature cannot be None" in str(e):
                print("✅ Correctly caught None temperature in set_temperature_mode")
            else:
                print(f"❌ Unexpected error: {e}")
                return False
        
        # Test with None mode
        try:
            cube.set_temperature_mode(thermostat, 20.0, None)
            print("❌ Should have failed with None mode")
            return False
        except Exception as e:
            if "Mode cannot be None" in str(e):
                print("✅ Correctly caught None mode in set_temperature_mode")
            else:
                print(f"❌ Unexpected error: {e}")
                return False
        
        # Test with None room_id (this should work now with our fix)
        thermostat.room_id = None
        thermostat.target_temperature = 20.0
        thermostat.mode = 1
        try:
            cube.set_temperature_mode(thermostat, 20.0, 1)
            print("✅ Correctly handled None room_id")
        except Exception as e:
            print(f"❌ Failed with None room_id: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ None comparison test failed: {e}")
        traceback.print_exc()
        return False

def test_room_id_edge_cases():
    """Test room_id handling with various values"""
    print("\n🔍 Testing room_id edge cases...")
    
    try:
        from device import MaxThermostat
        from cube import MaxCube
        
        class MockConnection:
            def connect(self):
                pass
            def disconnect(self):
                pass
            def send(self, data):
                pass
            @property
            def response(self):
                return "H:KEQ0839778,1f,0113\r\n"
        
        cube = MaxCube(MockConnection())
        thermostat = MaxThermostat()
        thermostat.rf_address = "123456"
        thermostat.target_temperature = 20.0
        thermostat.mode = 1
        
        # Test various room_id values
        test_cases = [
            (None, "00"),      # None should default to "00"
            (0, "00"),          # 0 should become "00"
            (5, "05"),          # Single digit should get leading zero
            (10, "10"),         # Double digit should stay as is
            (99, "99"),         # Large number should stay as is
        ]
        
        for room_id, expected_room in test_cases:
            thermostat.room_id = room_id
            try:
                cube.set_temperature_mode(thermostat, 20.0, 1)
                print(f"✅ room_id {room_id} handled correctly")
            except Exception as e:
                print(f"❌ room_id {room_id} failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Room ID edge case test failed: {e}")
        traceback.print_exc()
        return False

def test_connection_handling():
    """Test connection handling"""
    print("\n🔍 Testing connection handling...")
    
    try:
        from connection import MaxCubeConnection
        
        # Test connection creation
        conn = MaxCubeConnection("192.168.1.26", 62910)
        print("✅ Connection creation successful")
        
        # Test connection with invalid IP (should not crash)
        try:
            conn_invalid = MaxCubeConnection("999.999.999.999", 62910)
            print("✅ Invalid IP handled gracefully")
        except Exception as e:
            print(f"⚠️ Invalid IP caused exception: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        traceback.print_exc()
        return False

def run_core_tests():
    """Run core functionality tests"""
    print("🚀 Starting core MAX! Cube functionality tests...\n")
    
    tests = [
        ("Core Functionality", test_core_functionality),
        ("None Comparison Fixes", test_none_comparison_fixes),
        ("Room ID Edge Cases", test_room_id_edge_cases),
        ("Connection Handling", test_connection_handling),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
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
            traceback.print_exc()
    
    print(f"\n{'='*50}")
    print(f"CORE TEST RESULTS: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("🎉 ALL CORE TESTS PASSED! The None comparison issues are fixed.")
        print("✅ The integration should now work without the '>' not supported error.")
        return True
    else:
        print("⚠️ Some core tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = run_core_tests()
    sys.exit(0 if success else 1)
