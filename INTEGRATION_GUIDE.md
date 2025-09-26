# MAX! Cube Integration - Removal and Installation Guide

## 🗑️ **Removing the Existing Integration**

The existing integration has cached entries that need to be removed. Follow these steps:

### **Step 1: Remove Integration via Home Assistant UI**
1. Go to **Settings** → **Devices & Services**
2. Find **"eQ-3 MAX! Cube"** in the list
3. Click on it
4. Click the **"..."** menu (three dots)
5. Select **"Delete"**
6. Confirm the deletion

### **Step 2: Remove Integration Files (SSH)**
```bash
# SSH into your Home Assistant
ssh homeassistant@192.168.1.190

# Navigate to config directory
cd /config

# Remove the old integration completely
rm -rf custom_components/maxcube

# Clear any cached files
rm -rf .storage/core.config_entries
rm -rf .storage/core.device_registry
rm -rf .storage/core.entity_registry

# Restart Home Assistant
ha core restart
```

### **Step 3: Verify Removal**
1. Go to **Settings** → **Devices & Services**
2. Confirm **"eQ-3 MAX! Cube"** is no longer listed
3. Check **Settings** → **System** → **Logs** for any remaining references

---

## 🚀 **Installing the Fixed Integration**

### **Step 1: Update Integration Files**
```bash
# SSH into your Home Assistant
ssh homeassistant@192.168.1.190

# Navigate to config directory
cd /config

# Clone the updated integration
git clone https://github.com/janvangent1/maxcube.git temp_maxcube
mv temp_maxcube/custom_components/maxcube ./
rm -rf temp_maxcube

# Restart Home Assistant
ha core restart
```

### **Step 2: Add Integration via UI**
1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"MAX! Cube"**
4. Click on **"MAX! Cube"** when it appears
5. Configure with your settings:
   - **Cube Address**: `192.168.1.26`
   - **Port**: `62910`
   - **Valve Positions**: Enable
   - **Thermostat Modes**: Enable
   - **Heat Demand Switch**: Enable
   - **Min Valve Position**: `5`
   - **Update Interval**: `60`
   - **Debug Mode**: Enable (for troubleshooting)

### **Step 3: Verify Installation**
1. Check **Settings** → **System** → **Logs** for any errors
2. Look for **"MAX! Cube"** entries in the logs
3. Verify entities are created in **Settings** → **Devices & Services**

---

## 🔧 **Troubleshooting**

### **If Integration Still Shows Old Entries:**
```bash
# Force clear all cached data
ha core stop
rm -rf .storage/
ha core start
```

### **If You Get Import Errors:**
```bash
# Check file permissions
ls -la custom_components/maxcube/
chmod -R 755 custom_components/maxcube/
```

### **If Connection Fails:**
1. Verify MAX! Cube IP: `192.168.1.26`
2. Test connectivity: `ping 192.168.1.26`
3. Check port: `telnet 192.168.1.26 62910`

---

## 📋 **Expected Entities After Installation**

You should see these entities:
- **Climate**: `climate.living_room_thermostat`
- **Temperature**: `sensor.living_room_temperature`
- **Valve Position**: `sensor.living_room_valve_position`
- **Battery**: `sensor.living_room_battery`
- **Heat Demand**: `switch.heat_demand`

---

## 🎯 **Future Commit Script Usage**

Use the `commit_changes.py` script for future commits:

```bash
# Run the commit script
python commit_changes.py
```

This script will:
- ✅ Exclude `homeassistant_dev/` folder
- ✅ Exclude Python cache files
- ✅ Add only relevant files
- ✅ Create proper commit messages
- ✅ Push to GitHub

---

## ✅ **Success Indicators**

The integration is working correctly when:
1. No errors in Home Assistant logs
2. Entities show current data
3. Temperature changes work
4. Valve positions update
5. Heat demand switch functions

If you see any issues, check the logs and run the troubleshooting steps above.
