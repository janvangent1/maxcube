# MAX! Cube Integration - Reload Functionality

## 🔄 **New Reload Services**

The MAX! Cube integration now includes two new services to help manage device discovery and troubleshooting:

### **Service 1: `maxcube.reload_devices`**
**Purpose**: Reload all devices by scanning the MAX! Cube again without clearing cached data.

**Usage**:
```yaml
service: maxcube.reload_devices
data:
  cube_address: "192.168.1.26"
```

### **Service 2: `maxcube.clear_and_reload_devices`**
**Purpose**: Clear all cached data and perform a fresh scan of the MAX! Cube.

**Usage**:
```yaml
service: maxcube.clear_and_reload_devices
data:
  cube_address: "192.168.1.26"
```

## 🎯 **When to Use These Services**

### **Use `reload_devices` when:**
- ✅ You've added new thermostats to your MAX! Cube
- ✅ You've moved devices to different rooms
- ✅ You want to refresh device data without losing cache
- ✅ Devices are not showing up after installation

### **Use `clear_and_reload_devices` when:**
- ✅ You're experiencing persistent issues with device data
- ✅ You want to completely reset the integration
- ✅ After updating the integration
- ✅ When troubleshooting connection issues

## 🔧 **How to Use the Services**

### **Method 1: Developer Tools (Easiest)**
1. **Go to Settings** → **Developer Tools** → **Services**
2. **Select service**: `maxcube.reload_devices` or `maxcube.clear_and_reload_devices`
3. **Enter service data**:
   ```json
   {
     "cube_address": "192.168.1.26"
   }
   ```
4. **Click "Call Service"**

### **Method 2: Automation**
```yaml
automation:
  - alias: "Reload MAX! Cube Devices"
    trigger:
      - platform: time
        at: "06:00:00"  # Daily at 6 AM
    action:
      - service: maxcube.reload_devices
        data:
          cube_address: "192.168.1.26"
```

### **Method 3: Script**
```yaml
script:
  reload_maxcube:
    alias: "Reload MAX! Cube Devices"
    sequence:
      - service: maxcube.clear_and_reload_devices
        data:
          cube_address: "192.168.1.26"
```

## 📋 **Service Response**

Both services will:
- ✅ **Log the operation** in Home Assistant logs
- ✅ **Return success/failure status**
- ✅ **Update all device entities** automatically
- ✅ **Refresh room information**

## 🔍 **Monitoring the Services**

### **Check Logs**:
1. **Go to Settings** → **System** → **Logs**
2. **Look for entries** starting with `maxcube`
3. **Success messages**:
   - `"Reloading MAX! Cube devices..."`
   - `"Successfully reloaded X devices and Y rooms"`

### **Check Entities**:
1. **Go to Settings** → **Devices & Services**
2. **Find your MAX! Cube device**
3. **Verify all entities are updated**

## ⚠️ **Troubleshooting**

### **If Service Fails**:
1. **Check cube address** is correct
2. **Verify network connectivity** to the cube
3. **Check Home Assistant logs** for error details
4. **Try the clear_and_reload_devices** service instead

### **Common Issues**:
- **"No MAX! Cube coordinator found"**: Integration not properly installed
- **"Error communicating with MAX! Cube"**: Network or cube connectivity issue
- **"Device not found"**: Device may have been removed or RF address changed

## 🎉 **Benefits**

- ✅ **Easy device discovery** without restarting Home Assistant
- ✅ **Troubleshooting tool** for integration issues
- ✅ **Automated refresh** capabilities
- ✅ **No manual file editing** required
- ✅ **User-friendly** through Home Assistant UI

## 📚 **Example Use Cases**

### **Daily Refresh**:
```yaml
automation:
  - alias: "Daily MAX! Cube Refresh"
    trigger:
      - platform: time
        at: "02:00:00"
    action:
      - service: maxcube.reload_devices
        data:
          cube_address: "192.168.1.26"
```

### **After Adding New Devices**:
```yaml
script:
  add_new_thermostat:
    alias: "Add New Thermostat"
    sequence:
      - service: maxcube.clear_and_reload_devices
        data:
          cube_address: "192.168.1.26"
      - delay: "00:00:10"  # Wait 10 seconds
      - service: notify.mobile_app_your_phone
        data:
          message: "MAX! Cube devices refreshed - check for new thermostats"
```

The reload functionality makes managing your MAX! Cube integration much easier and more reliable! 🚀
