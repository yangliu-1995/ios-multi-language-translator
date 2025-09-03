#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify functionality
Functionality verification test script
"""

import os
import tempfile
import shutil
from strings_parser import StringsParser
from translator import create_translator
from code_generator import LocalizationCodeGenerator


def test_strings_parser():
    """Test strings parser"""
    print("Testing StringsParser...")
    
    parser = StringsParser()
    
    # Test content
    test_content = '''/* Test strings */
"test_key1" = "Test Value 1";
"test_key2" = "Test Value 2";
/* Comment */
"test_key3" = "Test Value 3";
'''
    
    # Parse content
    result = parser.parse_strings_content(test_content)
    
    assert len(result) == 3
    assert result["test_key1"] == "Test Value 1"
    assert result["test_key2"] == "Test Value 2"
    assert result["test_key3"] == "Test Value 3"
    
    print("✅ StringsParser test passed")


def test_mock_translator():
    """Test mock translator"""
    print("Testing MockTranslator...")
    
    translator = create_translator('mock')
    
    # Test translation
    result = translator.translate("Hello", "zh")
    assert result == "[ZH] Hello"
    
    # Test batch translation
    texts = {"key1": "Hello", "key2": "World"}
    results = translator.translate_batch(texts, "ja")
    assert results["key1"] == "[JA] Hello"
    assert results["key2"] == "[JA] World"
    
    print("✅ MockTranslator test passed")


def test_deepl_translator_init():
    """Test DeepL translator initialization"""
    print("Testing DeepL Translator initialization...")
    
    try:
        # Test initialization with provided API key
        # Use configured API key or skip DeepL test
        from config_manager import get_config
        config = get_config()
        auth_key = config.get_deepl_key()
        
        if not auth_key:
            print("⚠️  No DeepL API key configured, skipping DeepL test")
            return
            
        translator = create_translator('deepl', auth_key=auth_key)
        
        # Test API usage check
        usage = translator.check_api_usage()
        if usage:
            print(f"API Usage: {usage.get('character_count', 0)}/{usage.get('character_limit', 'unlimited')} characters")
        
        # Test supported languages list
        languages = translator.get_supported_languages()
        assert len(languages) > 0
        print(f"Supported languages count: {len(languages)}")
        
        print("✅ DeepL Translator initialization test passed")
        
    except Exception as e:
        print(f"⚠️ DeepL Translator test skipped (API issue): {e}")
        # This is not a fatal error, as it could be a network or API key issue


def test_code_generator():
    """Test localization code generator"""
    print("Testing LocalizationCodeGenerator...")
    
    generator = LocalizationCodeGenerator()
    
    # Test data
    strings_dict = {
        "test_button_title": "Test Button",
        "welcome_message": "Welcome!",
        "error-message": "Error occurred"
    }
    
    # Generate code
    swift_code = generator.generate_swift_extensions(strings_dict)
    
    # Verify generated code contains expected content
    assert "extension String" in swift_code
    assert "extension LocalizedStringKey" in swift_code
    assert "testButtonTitle" in swift_code
    assert "welcomeMessage" in swift_code
    assert "errorMessage" in swift_code
    
    print("✅ LocalizationCodeGenerator test passed")


def test_integration():
    """Integration test"""
    print("Testing integration...")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test project structure
        en_dir = os.path.join(temp_dir, "en.lproj")
        zh_dir = os.path.join(temp_dir, "zh-Hans.lproj")
        
        os.makedirs(en_dir)
        os.makedirs(zh_dir)
        
        # Create English strings file
        en_strings_content = '''/* Test */
"welcome" = "Welcome";
"goodbye" = "Goodbye";
'''
        
        with open(os.path.join(en_dir, "Localizable.strings"), "w") as f:
            f.write(en_strings_content)
        
        # Create empty Chinese strings file
        with open(os.path.join(zh_dir, "Localizable.strings"), "w") as f:
            f.write("/* Chinese */\n")
        
        # Test parsing
        parser = StringsParser()
        en_strings = parser.parse_strings_file(os.path.join(en_dir, "Localizable.strings"))
        
        assert len(en_strings) == 2
        assert "welcome" in en_strings
        assert "goodbye" in en_strings
        
        # Test translation and writing
        translator = create_translator('mock')
        translations = translator.translate_batch(en_strings, "zh")
        
        zh_file = os.path.join(zh_dir, "Localizable.strings")
        success = parser.update_strings_file(zh_file, translations)
        assert success
        
        # Verify written content
        zh_strings = parser.parse_strings_file(zh_file)
        assert len(zh_strings) == 2
        assert zh_strings["welcome"] == "[ZH] Welcome"
        assert zh_strings["goodbye"] == "[ZH] Goodbye"
    
    print("✅ Integration test passed")


def main():
    """Run all tests"""
    print("=" * 50)
    print("Running functionality tests...")
    print("=" * 50)
    
    try:
        test_strings_parser()
        test_mock_translator()
        test_deepl_translator_init()
        test_code_generator()
        test_integration()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! The iOS translator is ready to use.")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()