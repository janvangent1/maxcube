#!/usr/bin/env python3
"""
Simple test script for the renamed Jan MAX! integration
This tests the file structure and content without requiring Home Assistant
"""

import os
import json

def test_file_structure():
    """Test that all required files exist"""
    print("🔍 Testing file structure...")
    
    required_files = [
        'custom_components/maxcube/manifest.json',
        'custom_components/maxcube/__init__.py',
        'custom_components/maxcube/const.py',
        'custom_components/maxcube/config_flow.py',
        'custom_components/maxcube/coordinator.py',
        'custom_components/maxcube/climate.py',
        'custom_components/maxcube/sensor.py',
        'custom_components/maxcube/switch.py',
        'custom_components/maxcube/services.py',
        'custom_components/maxcube/cube.py',
        'custom_components/maxcube/connection.py',
        'custom_components/maxcube/device.py',
        'custom_components/maxcube/room.py',
        'custom_components/maxcube/thermostat.py',
        'custom_components/maxcube/wallthermostat.py',
        'custom_components/maxcube/windowshutter.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ {len(missing_files)} files are missing")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files exist")
        return True

def test_manifest():
    """Test the manifest.json file"""
    print("\n🔍 Testing manifest.json...")
    
    try:
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
        
        # Check other required fields
        required_fields = ['domain', 'name', 'version', 'config_flow', 'iot_class']
        for field in required_fields:
            if field in manifest:
                print(f"✅ {field}: {manifest[field]}")
            else:
                print(f"❌ Missing required field: {field}")
                return False
        
        print("✅ Manifest.json test passed")
        return True
        
    except Exception as e:
        print(f"❌ Manifest test failed: {e}")
        return False

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

def test_constants_file():
    """Test the constants file"""
    print("\n🔍 Testing constants file...")
    
    try:
        with open('custom_components/maxcube/const.py', 'r') as f:
            content = f.read()
        
        # Check for DOMAIN constant
        if "DOMAIN = \"jan_max\"" in content:
            print("✅ DOMAIN constant is correctly set to 'jan_max'")
        else:
            print("❌ DOMAIN constant not found or incorrect")
            return False
        
        # Check for old references
        if 'maxcube' in content and 'DOMAIN' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'DOMAIN' in line and 'maxcube' in line and 'jan_max' not in line:
                    print(f"❌ Old domain reference found: {file_path}:{i+1} - {line.strip()}")
                    return False
        
        print("✅ Constants file test passed")
        return True
        
    except Exception as e:
        print(f"❌ Constants file test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Renamed Jan MAX! Integration")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_manifest,
        test_domain_consistency,
        test_constants_file
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
        print("\n📋 Next steps:")
        print("   1. Commit and push the changes")
        print("   2. Update your Home Assistant instance")
        print("   3. Look for 'Jan MAX! Cube' in the integrations list")
        return True
    else:
        print("⚠️ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
