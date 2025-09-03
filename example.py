#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of iOS Translation Script
Usage example for iOS translation script
"""

import os
from ios_translator import iOSTranslator
from translator import create_translator


def create_example_project():
    """Create example project structure for demonstration"""
    
    # Create example directory structure
    example_dir = "example_project"
    
    # Create en.lproj directory
    en_dir = os.path.join(example_dir, "en.lproj")
    os.makedirs(en_dir, exist_ok=True)
    
    # Create example English strings file
    en_strings = '''/* App Title */
"app_title" = "My Awesome App";

/* Navigation */
"nav_home" = "Home";
"nav_settings" = "Settings";
"nav_profile" = "Profile";

/* Buttons */
"btn_save" = "Save";
"btn_cancel" = "Cancel";
"btn_delete" = "Delete";
"btn_confirm" = "Confirm";

/* Messages */
"msg_welcome" = "Welcome to our app!";
"msg_success" = "Operation completed successfully";
"msg_error" = "An error occurred. Please try again.";
"msg_loading" = "Loading...";

/* Alerts */
"alert_title_warning" = "Warning";
"alert_title_error" = "Error";
"alert_msg_delete_confirm" = "Are you sure you want to delete this item?";
'''
    
    with open(os.path.join(en_dir, "Localizable.strings"), "w", encoding="utf-8") as f:
        f.write(en_strings)
    
    # Create other language directories (empty, let the script fill them)
    for lang in ["zh-Hans.lproj", "ja.lproj", "fr.lproj"]:
        lang_dir = os.path.join(example_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        # Create empty or partially filled strings file
        localizable_path = os.path.join(lang_dir, "Localizable.strings")
        with open(localizable_path, "w", encoding="utf-8") as f:
            f.write("/* Localizable.strings */\n")
    
    print(f"Created example project in: {os.path.abspath(example_dir)}")
    return os.path.abspath(example_dir)


def run_translation_example():
    """Run translation example"""
    
    # Create example project
    project_path = create_example_project()
    
    print("=" * 50)
    print("Running translation example...")
    print("=" * 50)
    
    try:
        # Create mock translator for demonstration
        translator = create_translator('mock')
        
        # Create translator instance
        ios_translator = iOSTranslator(project_path, translator)
        
        # Run translation
        success = ios_translator.run(
            generate_swift=True,
            generate_objc=True,
            output_dir=project_path
        )
        
        if success:
            print("\n✅ Example translation completed!")
            print(f"Check the generated files in: {project_path}")
            print("Generated files:")
            print("- LocalizedStrings.swift")
            print("- LocalizedStrings.h")
            print("- Updated Localizable.strings in all language directories")
        else:
            print("\n❌ Example translation failed!")
            
    except Exception as e:
        print(f"Error running example: {e}")


if __name__ == "__main__":
    run_translation_example()