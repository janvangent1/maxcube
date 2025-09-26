#!/usr/bin/env python3
"""
Setup script for local Home Assistant development environment
Installs Home Assistant Core for testing custom integrations
"""

import subprocess
import sys
import os
import venv

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Set up Home Assistant development environment."""
    print("🏠 Setting up Home Assistant Development Environment")
    print("=" * 60)
    
    # Check if Python 3.9+ is available
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required for Home Assistant")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment
    venv_path = "homeassistant_dev"
    if not os.path.exists(venv_path):
        print(f"📦 Creating virtual environment: {venv_path}")
        venv.create(venv_path, with_pip=True)
    else:
        print(f"✅ Virtual environment already exists: {venv_path}")
    
    # Activate virtual environment and install Home Assistant
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_path, "Scripts", "activate")
        pip_path = os.path.join(venv_path, "Scripts", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python")
    else:  # Linux/macOS
        activate_script = os.path.join(venv_path, "bin", "activate")
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")
    
    # Install Home Assistant Core
    commands = [
        (f'"{pip_path}" install --upgrade pip', "Upgrading pip"),
        (f'"{pip_path}" install homeassistant', "Installing Home Assistant Core"),
        (f'"{pip_path}" install pytest pytest-asyncio', "Installing testing tools"),
        (f'"{pip_path}" install voluptuous', "Installing voluptuous"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("\n🎉 Home Assistant development environment setup complete!")
    print("\n📋 Next steps:")
    print(f"1. Activate the environment:")
    if os.name == 'nt':  # Windows
        print(f"   {activate_script}")
    else:  # Linux/macOS
        print(f"   source {activate_script}")
    print("2. Run the integration test:")
    print("   python test_integration.py")
    print("3. Start Home Assistant for testing:")
    print("   hass --open-ui")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
