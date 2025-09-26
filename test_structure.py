#!/usr/bin/env python3
"""
Syntax and structure test for MAX! Cube Home Assistant integration
Tests Python syntax and file structure without Home Assistant dependencies
"""

import sys
import os
import json
import ast
import traceback

def test_python_syntax():
    """Test Python syntax of all Python files."""
    print("🔍 Testing Python syntax...")
    
    python_files = [
        'custom_components/maxcube/__init__.py',
        'custom_components/maxcube/const.py',
        'custom_components/maxcube/connection.py',
        'custom_components/maxcube/cube.py',
        'custom_components/maxcube/coordinator.py',
        'custom_components/maxcube/config_flow.py',
        'custom_components/maxcube/climate.py',
        'custom_components/maxcube/sensor.py',
        'custom_components/maxcube/switch.py',
        'custom_components/maxcube/device.py',
        'custom_components/maxcube/room.py',
        'custom_components/maxcube/thermostat.py',
        'custom_components/maxcube/wallthermostat.py',
        'custom_components/maxcube/windowshutter.py',
    ]
    
    passed = 0
    total = len(python_files)
    
    for file_path in python_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        
        if not os.path.exists(full_path):
            print(f"❌ File not found: {file_path}")
            continue
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Parse the AST to check syntax
            ast.parse(source)
            print(f"✅ {file_path} - syntax OK")
            passed += 1
            
        except SyntaxError as e:
            print(f"❌ {file_path} - syntax error: {e}")
        except Exception as e:
            print(f"❌ {file_path} - error: {e}")
    
    print(f"📊 Syntax test: {passed}/{total} files passed")
    return passed == total

def test_manifest():
    """Test manifest.json validity."""
    print("\n🔍 Testing manifest.json...")
    
    try:
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

def test_file_structure():
    """Test that all required files exist."""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'custom_components/maxcube/__init__.py',
        'custom_components/maxcube/manifest.json',
        'custom_components/maxcube/const.py',
        'custom_components/maxcube/config_flow.py',
        'custom_components/maxcube/coordinator.py',
        'custom_components/maxcube/climate.py',
        'custom_components/maxcube/sensor.py',
        'custom_components/maxcube/switch.py',
        'custom_components/maxcube/connection.py',
        'custom_components/maxcube/cube.py',
    ]
    
    passed = 0
    total = len(required_files)
    
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        
        if os.path.exists(full_path):
            print(f"✅ {file_path} - exists")
            passed += 1
        else:
            print(f"❌ {file_path} - missing")
    
    print(f"📊 File structure test: {passed}/{total} files found")
    return passed == total

def test_import_structure():
    """Test import structure without executing."""
    print("\n🔍 Testing import structure...")
    
    try:
        # Check __init__.py for proper imports
        init_path = os.path.join(os.path.dirname(__file__), 'custom_components', 'maxcube', '__init__.py')
        
        with open(init_path, 'r') as f:
            content = f.read()
        
        # Check for required imports
        required_imports = [
            'from homeassistant.config_entries import ConfigEntry',
            'from homeassistant.core import HomeAssistant',
            'from .const import DOMAIN',
            'from .coordinator import MaxCubeCoordinator',
        ]
        
        passed = 0
        total = len(required_imports)
        
        for import_line in required_imports:
            if import_line in content:
                print(f"✅ Found: {import_line}")
                passed += 1
            else:
                print(f"❌ Missing: {import_line}")
        
        print(f"📊 Import structure test: {passed}/{total} imports found")
        return passed == total
        
    except Exception as e:
        print(f"❌ Import structure error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 MAX! Cube Home Assistant Integration Structure Test")
    print("=" * 60)
    
    tests = [
        ("Python Syntax", test_python_syntax),
        ("Manifest", test_manifest),
        ("File Structure", test_file_structure),
        ("Import Structure", test_import_structure),
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
        print("🎉 All structure tests passed! Integration should work in Home Assistant.")
    else:
        print("⚠️ Some tests failed. Fix the issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
