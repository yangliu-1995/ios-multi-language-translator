#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration setup utility
Helps users set up configuration files for the iOS translator
"""

import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def setup_config():
    """Setup configuration files"""
    
    print("🔧 iOS Translator Configuration Setup")
    print("=" * 50)
    
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up to project root
    
    # Setup .env file
    env_file = os.path.join(current_dir, '.env')
    env_example = os.path.join(current_dir, 'config', 'env.example')
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        print("📄 Creating .env file from template...")
        shutil.copy(env_example, env_file)
        print(f"✅ Created: {env_file}")
        print("   Please edit this file and add your API keys")
    elif os.path.exists(env_file):
        print(f"📄 .env file already exists: {env_file}")
    else:
        print("❌ env.example template not found")
    
    # Setup config.py file
    config_file = os.path.join(current_dir, 'config.py')
    config_example = os.path.join(current_dir, 'config', 'config.py.example')
    
    if not os.path.exists(config_file) and os.path.exists(config_example):
        print("\n📄 Creating config.py file from template...")
        shutil.copy(config_example, config_file)
        print(f"✅ Created: {config_file}")
        print("   Please edit this file and add your API keys")
    elif os.path.exists(config_file):
        print(f"\n📄 config.py file already exists: {config_file}")
    else:
        print("\n❌ config.py.example template not found")
    
    print("\n🔐 Security Notice:")
    print("- .env and config.py contain sensitive API keys")
    print("- These files are in .gitignore and won't be committed")
    print("- Share the .example files, not the actual config files")
    
    print("\n📝 Next Steps:")
    print("1. Edit .env or config.py with your actual API keys")
    print("2. Test with: python ios_translator.py --show-config") 
    print("3. Run translation: python ios_translator.py /path/to/project")


if __name__ == "__main__":
    setup_config()
