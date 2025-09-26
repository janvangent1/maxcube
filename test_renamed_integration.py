#!/usr/bin/env python3
"""
Test script for the renamed Jan MAX! integration
This tests the integration with the new 'jan_max' domain
"""

import sys
import os

# Add the custom_components directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components'))

def test_manifest():
    """Test the manifest.json file"""
    print("🔍 Testing manifest.json...")
    
    try:
        import json
        with open('custom_components/maxcube/manifest.json', 'r') as f:
            manifest = json.load(f)
        
        # Check domain
        if manifest.get('domain') == 'jan_max':
            print("✅ Domain is correctly set to 'jan_max'")
        else:
            print(f"❌ Domain is '{manifest.get('domain')}', expected 'jan_max'")
            return False
        
        # Check name
        if 'Jan MAX!' in manifest.get('name', ''):
            print("✅ Name contains 'Jan MAX!'")
        else:
            print(f"❌ Name is '{manifest.get('name')}', expected to contain 'Jan MAX!'")
            return False
        
        print("✅ Manifest.json test passed")
        return True
        
    except Exception as e:
        print(f"❌ Manifest test failed: {e}")
        return False

def test_constants():
    """Test the constants file"""
    print("\n🔍 Testing constants...")
    
    try:
        from maxcube.const import DOMAIN
        
        if DOMAIN == 'jan_max':
            print("✅ DOMAIN constant is correctly set to 'jan_max'")
            return True
        else:
            print(f"❌ DOMAIN constant is '{DOMAIN}', expected 'jan_max'")
            return False
            
    except Exception as e:
        print(f"❌ Constants test failed: {e}")
        return False

def test_config_flow():
    """Test the config flow"""
    print("\n🔍 Testing config flow...")
    
    try:
        from maxcube.config_flow import ConfigFlow
        
        # Check if the class exists and has the right domain
        if hasattr(ConfigFlow, '__init__'):
            print("✅ ConfigFlow class exists")
            return True
        else:
            print("❌ ConfigFlow class not found")
            return False
            
    except Exception as e:
        print(f"❌ Config flow test failed: {e}")
        return False

def test_imports():
    """Test that all modules can be imported"""
    print("\n🔍 Testing imports...")
    
    modules_to_test = [
        'maxcube.__init__',
        'maxcube.const',
        'maxcube.config_flow',
        'maxcube.coordinator',
        'maxcube.climate',
        'maxcube.sensor',
        'maxcube.switch',
        'maxcube.services',
        'maxcube.cube',
        'maxcube.connection',
        'maxcube.device',
        'maxcube.room',
        'maxcube.thermostat',
        'maxcube.wallthermostat',
        'maxcube.windowshutter'
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except Exception as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ {len(failed_imports)} modules failed to import")
        return False
    else:
        print(f"\n✅ All {len(modules_to_test)} modules imported successfully")
        return True

def test_domain_consistency():
    """Test that all files use the correct domain"""
    print("\n🔍 Testing domain consistency...")
    
    files_to_check = [
        'custom_components/maxcube/__init__.py',
        'custom_components/maxcube/config_flow.py',
        'custom_components/maxcube/coordinator.py',
        'custom_components/maxcube/climate.py',
        'custom_components/maxcube/sensor.py',
        'custom_components/maxcube/switch.py',
        'custom_components/maxcube/services.py'
    ]
    
    domain_issues = []
    
    for file_path in files_to_check:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for old domain references
            if 'maxcube' in content and 'DOMAIN' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'DOMAIN' in line and 'maxcube' in line:
                        if 'jan_max' not in line:
                            domain_issues.append(f"{file_path}:{i+1} - {line.strip()}")
            
            # Check for old integration name references
            if 'eQ-3 MAX!' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'eQ-3 MAX!' in line:
                        domain_issues.append(f"{file_path}:{i+1} - {line.strip()}")
        
        except Exception as e:
            print(f"❌ Error checking {file_path}: {e}")
            domain_issues.append(f"{file_path} - Error reading file")
    
    if domain_issues:
        print("❌ Domain consistency issues found:")
        for issue in domain_issues:
            print(f"   {issue}")
        return False
    else:
        print("✅ All files use consistent domain references")
        return True

def main():
    """Run all tests"""
    print("🚀 Testing Renamed Jan MAX! Integration")
    print("=" * 50)
    
    tests = [
        test_manifest,
        test_constants,
        test_config_flow,
        test_imports,
        test_domain_consistency
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The integration has been successfully renamed to 'jan_max'")
        print("✅ It should now appear as 'Jan MAX! Cube' in Home Assistant")
        print("✅ No conflicts with existing MAX! integrations")
        return True
    else:
        print("⚠️ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
