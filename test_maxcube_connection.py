#!/usr/bin/env python3
import socket
import time
import subprocess
import re
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def scan_network_for_cubes():
    """Scan the network for MAX! Cubes using pure Python"""
    print("🔍 Scanning network for MAX! Cubes...")
    
    # Common network ranges to scan
    networks_to_scan = [
        ("192.168.1", range(1, 255)),    # Most common home network
        ("192.168.0", range(1, 255)),    # Alternative home network
        ("10.0.0", range(1, 255)),       # Some home networks
        ("172.16.0", range(1, 255)),     # Some corporate networks
    ]
    
    found_devices = []
    
    for network_base, ip_range in networks_to_scan:
        print(f"📡 Scanning network: {network_base}.x")
        
        for i in ip_range:
            ip = f"{network_base}.{i}"
            try:
                # Quick ping test
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)  # Very quick timeout
                result = sock.connect_ex((ip, 80))  # Try common web port
                sock.close()
                
                if result == 0:
                    found_devices.append(ip)
                    print(f"   📱 Found device: {ip}")
                    
            except Exception:
                pass  # Ignore errors for speed
    
    return found_devices

def scan_ports_on_device(ip, ports):
    """Scan specific ports on a device"""
    print(f"🔌 Scanning ports on {ip}...")
    
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                print(f"   ✅ Port {port}: OPEN")
            else:
                print(f"   ❌ Port {port}: CLOSED")
        except Exception as e:
            print(f"   ❌ Port {port}: ERROR - {e}")

def test_maxcube_connection():
    print("🔍 Testing MAX! Cube connection...")
    
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 10 second timeout
        
        # Connect to MAX! Cube
        print("📡 Connecting to 192.168.1.26:62910...")
        sock.connect(('192.168.1.26', 62910))
        print("✅ Connected successfully!")
        
        # Send a basic command
        print("📤 Sending command: l:")
        sock.send(b'l:\r\n')
        
        # Wait for response
        print("⏳ Waiting for response...")
        time.sleep(2)
        
        # Try to receive data
        try:
            data = sock.recv(1024)
            if data:
                print(f"📥 Received: {data}")
            else:
                print("📥 No data received")
        except socket.timeout:
            print("⏰ Timeout waiting for response")
        
        # Close connection
        sock.close()
        print("✅ Connection test completed")
        
    except socket.timeout:
        print("❌ Connection timeout")
    except ConnectionRefusedError:
        print("❌ Connection refused - port might be closed")
    except Exception as e:
        print(f"❌ Error: {e}")

def scan_all_devices_for_maxcube_ports(found_devices):
    """Scan all found devices for MAX! Cube ports"""
    print("\n🔍 Scanning all devices for MAX! Cube ports...")
    
    maxcube_ports = [62910, 62911, 62912, 62913, 62914, 62915]
    web_ports = [80, 443, 8080, 8443]
    all_ports = maxcube_ports + web_ports
    
    potential_cubes = []
    
    for device in found_devices:
        print(f"\n📱 Checking device: {device}")
        open_ports = []
        
        for port in all_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((device, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    if port in maxcube_ports:
                        print(f"   🎯 MAX! Cube port {port}: OPEN")
                    else:
                        print(f"   🌐 Web port {port}: OPEN")
            except Exception as e:
                pass  # Ignore errors for speed
        
        if open_ports:
            potential_cubes.append((device, open_ports))
            print(f"   ✅ Device {device} has {len(open_ports)} open ports: {open_ports}")
        else:
            print(f"   ❌ Device {device}: No open ports")
    
    return potential_cubes

def test_maxcube_on_device(ip, port=62910):
    """Test MAX! Cube connection on a specific device and port"""
    print(f"\n🔍 Testing MAX! Cube connection on {ip}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        sock.connect((ip, port))
        print(f"✅ Connected to {ip}:{port}!")
        
        # Send MAX! Cube command
        sock.send(b'l:\r\n')
        time.sleep(1)
        
        try:
            data = sock.recv(1024)
            if data:
                print(f"📥 Received response: {data}")
                sock.close()
                return True
            else:
                print("📥 No response received")
        except socket.timeout:
            print("⏰ Timeout waiting for response")
        
        sock.close()
        return False
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    print("🚀 MAX! Cube Network Scanner & Connection Tester")
    print("=" * 60)
    
    # Step 1: Scan all networks for devices
    found_devices = scan_network_for_cubes()
    
    if not found_devices:
        print("\n❌ No devices found on any network!")
        print("📋 Make sure:")
        print("   • You're connected to a network")
        print("   • Network allows scanning")
        print("   • Try running this script on your Raspberry Pi instead")
        return
    
    print(f"\n📊 Found {len(found_devices)} devices total")
    
    # Step 2: Scan all devices for MAX! Cube ports
    potential_cubes = scan_all_devices_for_maxcube_ports(found_devices)
    
    print("\n" + "=" * 60)
    
    # Step 3: Test connections to potential MAX! Cubes
    if potential_cubes:
        print("🎯 Testing connections to potential MAX! Cubes...")
        working_cubes = []
        
        for device, ports in potential_cubes:
            maxcube_ports = [p for p in ports if p in [62910, 62911, 62912, 62913, 62914, 62915]]
            
            for port in maxcube_ports:
                if test_maxcube_on_device(device, port):
                    working_cubes.append((device, port))
                    print(f"🎉 FOUND WORKING MAX! CUBE: {device}:{port}")
    else:
        print("❌ No devices with open MAX! Cube ports found")
    
    print("\n" + "=" * 60)
    print("📋 FINAL SUMMARY:")
    
    if potential_cubes:
        print("🔍 Devices with open ports:")
        for device, ports in potential_cubes:
            print(f"   📱 {device}: {ports}")
    
    print("\n💡 Next steps:")
    print("   • If no MAX! Cube found: Check power and network connection")
    print("   • If MAX! Cube found: Update Home Assistant with correct IP:port")
    print("   • Try power cycling the MAX! Cube if it's not responding")

if __name__ == "__main__":
    main()
