# Update MAX! Cube integration on Home Assistant
# Run this script on your Home Assistant instance

Write-Host "🔄 Updating MAX! Cube integration..." -ForegroundColor Green

# Step 1: Remove old integration
Write-Host "🗑️ Removing old integration..." -ForegroundColor Yellow
if (Test-Path "/config/custom_components/maxcube") {
    Remove-Item -Recurse -Force "/config/custom_components/maxcube"
}

# Step 2: Clear cached data
Write-Host "🧹 Clearing cached data..." -ForegroundColor Yellow
if (Test-Path "/config/.storage/core.config_entries") {
    Remove-Item -Recurse -Force "/config/.storage/core.config_entries"
}
if (Test-Path "/config/.storage/core.device_registry") {
    Remove-Item -Recurse -Force "/config/.storage/core.device_registry"
}
if (Test-Path "/config/.storage/core.entity_registry") {
    Remove-Item -Recurse -Force "/config/.storage/core.entity_registry"
}

# Step 3: Clone updated integration
Write-Host "📥 Downloading updated integration..." -ForegroundColor Yellow
Set-Location "/config"
git clone https://github.com/janvangent1/maxcube.git temp_maxcube

# Step 4: Install integration
Write-Host "📦 Installing integration..." -ForegroundColor Yellow
Move-Item "temp_maxcube/custom_components/maxcube" "./"
Remove-Item -Recurse -Force "temp_maxcube"

# Step 5: Verify installation
Write-Host "✅ Verifying installation..." -ForegroundColor Yellow
if (Test-Path "/config/custom_components/maxcube/cube.py") {
    Write-Host "✅ Integration files installed successfully" -ForegroundColor Green
    
    # Check if our fix is in the file
    $content = Get-Content "/config/custom_components/maxcube/cube.py" -Raw
    if ($content -match "room = str\(thermostat\.room_id\) if thermostat\.room_id is not None else '00'") {
        Write-Host "✅ None comparison fix is present" -ForegroundColor Green
    } else {
        Write-Host "❌ None comparison fix NOT found!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Integration installation failed!" -ForegroundColor Red
    exit 1
}

# Step 6: Restart Home Assistant
Write-Host "🔄 Restarting Home Assistant..." -ForegroundColor Yellow
ha core restart

Write-Host "🎉 Update complete! The integration should now work without the None comparison error." -ForegroundColor Green
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Go to Settings → Devices & Services" -ForegroundColor White
Write-Host "   2. Click '+ Add Integration'" -ForegroundColor White
Write-Host "   3. Search for 'MAX! Cube'" -ForegroundColor White
Write-Host "   4. Configure with your settings" -ForegroundColor White
