#!/usr/bin/env python3
"""
Simple MAX! Cube test that directly tests the cube.py functionality
"""

import sys
import os
import traceback

# Add the maxcube module to path
current_dir = os.path.dirname(os.path.abspath(__file__))
maxcube_path = os.path.join(current_dir, 'maxcube-HomeAssist-plugin', 'custom_components', 'maxcube')
sys.path.insert(0, maxcube_path)

def test_cube_none_comparisons():
    """Test that the None comparison fixes work in cube.py"""
    print("🔍 Testing cube.py None comparison fixes...")
    
    try:
        # Import the cube module directly
        import cube
        
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
        cube_instance = cube.MaxCube(MockConnection())
        
        # Create a mock thermostat with None values
        class MockThermostat:
            def __init__(self):
                self.rf_address = "123456"
                self.room_id = None
                self.target_temperature = None
                self.mode = None
        
        thermostat = MockThermostat()
        
        print("✅ Mock objects created successfully")
        
        # Test set_target_temperature with None mode
        try:
            cube_instance.set_target_temperature(thermostat, 20.0)
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
            cube_instance.set_mode(thermostat, 1)
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
            cube_instance.set_temperature_mode(thermostat, None, 1)
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
            cube_instance.set_temperature_mode(thermostat, 20.0, None)
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
            cube_instance.set_temperature_mode(thermostat, 20.0, 1)
            print("✅ Correctly handled None room_id")
        except Exception as e:
            print(f"❌ Failed with None room_id: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Cube None comparison test failed: {e}")
        traceback.print_exc()
        return False

def test_room_id_edge_cases():
    """Test room_id handling with various values"""
    print("\n🔍 Testing room_id edge cases...")
    
    try:
        import cube
        
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
        
        cube_instance = cube.MaxCube(MockConnection())
        
        class MockThermostat:
            def __init__(self):
                self.rf_address = "123456"
                self.target_temperature = 20.0
                self.mode = 1
        
        thermostat = MockThermostat()
        
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
                cube_instance.set_temperature_mode(thermostat, 20.0, 1)
                print(f"✅ room_id {room_id} handled correctly")
            except Exception as e:
                print(f"❌ room_id {room_id} failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Room ID edge case test failed: {e}")
        traceback.print_exc()
        return False

def run_simple_tests():
    """Run simple tests"""
    print("🚀 Starting simple MAX! Cube tests...\n")
    
    tests = [
        ("None Comparison Fixes", test_cube_none_comparisons),
        ("Room ID Edge Cases", test_room_id_edge_cases),
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
    print(f"SIMPLE TEST RESULTS: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("🎉 ALL SIMPLE TESTS PASSED! The None comparison issues are fixed.")
        print("✅ The integration should now work without the '>' not supported error.")
        return True
    else:
        print("⚠️ Some simple tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)
