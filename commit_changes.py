#!/usr/bin/env python3
"""
Git commit script for MAX! Cube integration
This script ensures proper commits by excluding unwanted files
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a git command and return the result"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return result.stdout.strip()
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return None

def check_gitignore():
    """Ensure .gitignore exists and excludes unwanted files"""
    gitignore_content = """# Exclude Home Assistant development environment
homeassistant_dev/

# Python cache files
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtual environments
venv/
env/
ENV/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Test files (optional - uncomment if you don't want to commit tests)
# test_*.py
# *_test.py
"""
    
    if not os.path.exists('.gitignore'):
        print("📝 Creating .gitignore file...")
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ .gitignore created")
    else:
        print("✅ .gitignore already exists")

def check_homeassistant_dev_in_history():
    """Check if homeassistant_dev was previously committed"""
    print("🔍 Checking if homeassistant_dev was previously committed...")
    
    # Check if homeassistant_dev exists in git history
    result = run_command("git log --name-only --oneline | grep -i homeassistant_dev", 
                       "Checking git history for homeassistant_dev")
    
    if result:
        print("⚠️ homeassistant_dev folder was found in git history!")
        print("📋 Commands to remove it from git history:")
        print("   git filter-branch --tree-filter 'rm -rf homeassistant_dev' HEAD")
        print("   git push origin --force")
        return True
    else:
        print("✅ homeassistant_dev not found in git history")
        return False

def commit_changes():
    """Commit changes properly"""
    print("🚀 Starting proper commit process...")
    
    # Step 1: Check .gitignore
    check_gitignore()
    
    # Step 2: Check if homeassistant_dev was previously committed
    was_committed = check_homeassistant_dev_in_history()
    
    # Step 3: Add files selectively (excluding unwanted files)
    print("\n📁 Adding files to commit...")
    
    # Add core integration files
    files_to_add = [
        "custom_components/maxcube/",
        "comprehensive_test_maxcube.py",
        "core_test_maxcube.py", 
        "direct_test_maxcube.py",
        "simple_cube_test.py",
        ".gitignore"
    ]
    
    for file_pattern in files_to_add:
        if os.path.exists(file_pattern):
            result = run_command(f"git add {file_pattern}", f"Adding {file_pattern}")
            if result is None:
                return False
        else:
            print(f"⚠️ {file_pattern} not found, skipping")
    
    # Step 4: Check what's staged
    print("\n📋 Checking staged files...")
    staged_files = run_command("git diff --cached --name-only", "Checking staged files")
    if staged_files:
        print("📁 Files staged for commit:")
        for line in staged_files.split('\n'):
            if line.strip():
                print(f"   ✅ {line}")
    else:
        print("❌ No files staged for commit")
        return False
    
    # Step 5: Commit
    commit_message = "Fix None comparison errors and add comprehensive tests\n\n- Fixed room_id None comparison in cube.py\n- Added None checks for temperature and mode parameters\n- Added comprehensive test scripts to catch issues before deployment\n- Excluded homeassistant_dev folder from commits"
    
    result = run_command(f'git commit -m "{commit_message}"', "Committing changes")
    if result is None:
        return False
    
    # Step 6: Push
    result = run_command("git push origin master", "Pushing to GitHub")
    if result is None:
        return False
    
    print("\n🎉 Commit process completed successfully!")
    
    if was_committed:
        print("\n⚠️ IMPORTANT: homeassistant_dev was found in git history!")
        print("📋 To remove it completely, run these commands:")
        print("   git filter-branch --tree-filter 'rm -rf homeassistant_dev' HEAD")
        print("   git push origin --force")
        print("   ⚠️ WARNING: This will rewrite git history!")
    
    return True

def main():
    """Main function"""
    print("🔧 MAX! Cube Integration - Git Commit Script")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository!")
        return False
    
    # Run commit process
    success = commit_changes()
    
    if success:
        print("\n✅ All done! Changes committed and pushed to GitHub.")
        print("📋 Next steps:")
        print("   1. Update your Home Assistant instance")
        print("   2. Remove the old integration (see instructions below)")
        print("   3. Add the new integration")
    else:
        print("\n❌ Commit process failed!")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
