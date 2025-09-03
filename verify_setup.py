#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification script to check if all dependencies are properly installed
Verification script: Check if all dependencies are correctly installed
"""

def check_dependencies():
    """Check all required dependency packages"""
    
    print("Checking dependencies...")
    print("=" * 50)
    
    try:
        import requests
        print("✅ requests library: OK")
    except ImportError as e:
        print(f"❌ requests library: FAILED - {e}")
        return False
    
    try:
        import deepl
        print("✅ deepl library: OK")
        print(f"   DeepL library version: {getattr(deepl, '__version__', 'unknown')}")
    except ImportError as e:
        print(f"❌ deepl library: FAILED - {e}")
        print("   Please install with: pip install deepl")
        return False
    
    return True


def test_deepl_initialization():
    """Test DeepL initialization"""
    
    print("\nTesting DeepL initialization...")
    print("=" * 50)
    
    try:
        from translator import create_translator
        
        # Use the provided API key
        # Use your actual API key or configure it via .env file
        from config_manager import get_config
        config = get_config()
        auth_key = config.get_deepl_key()
        
        if not auth_key:
            print("⚠️  No DeepL API key configured. Testing with mock translator...")
            auth_key = "test-key"
        
        print("Creating DeepL translator...")
        translator = create_translator('deepl', auth_key=auth_key)
        print("✅ DeepL translator created successfully!")
        
        # Test getting supported languages
        print("Getting supported languages...")
        languages = translator.get_supported_languages()
        print(f"✅ Found {len(languages)} supported languages")
        
        # Test API usage
        print("Checking API usage...")
        usage = translator.check_api_usage()
        if usage:
            print(f"✅ API usage check successful")
            print(f"   Characters used: {usage['character_count']}/{usage['character_limit']}")
        else:
            print("⚠️ Could not retrieve API usage (might be network issue)")
        
        return True
        
    except Exception as e:
        print(f"❌ DeepL initialization failed: {e}")
        return False


def test_basic_translation():
    """Test basic translation functionality"""
    
    print("\nTesting basic translation...")
    print("=" * 50)
    
    try:
        from translator import create_translator
        
        # Test with mock translator for basic testing
        print("Testing with mock translator...")
        mock_translator = create_translator('mock')
        
        result = mock_translator.translate("Hello", "zh")
        expected = "[ZH] Hello"
        
        if result == expected:
            print("✅ Mock translation test passed")
        else:
            print(f"❌ Mock translation test failed: expected '{expected}', got '{result}'")
            return False
        
        # Test batch translation
        texts = {"key1": "Hello", "key2": "World"}
        results = mock_translator.translate_batch(texts, "ja")
        
        if results["key1"] == "[JA] Hello" and results["key2"] == "[JA] World":
            print("✅ Mock batch translation test passed")
        else:
            print(f"❌ Mock batch translation test failed: {results}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Basic translation test failed: {e}")
        return False


def test_strings_parser():
    """Test strings parser"""
    
    print("\nTesting strings parser...")
    print("=" * 50)
    
    try:
        from strings_parser import StringsParser
        
        parser = StringsParser()
        
        # Test parsing
        test_content = '''/* Test */
"key1" = "Value 1";
"key2" = "Value 2";
'''
        result = parser.parse_strings_content(test_content)
        
        if len(result) == 2 and result["key1"] == "Value 1" and result["key2"] == "Value 2":
            print("✅ Strings parser test passed")
            return True
        else:
            print(f"❌ Strings parser test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Strings parser test failed: {e}")
        return False


def test_code_generator():
    """Test localization code generator"""
    
    print("\nTesting localization code generator...")
    print("=" * 50)
    
    try:
        from code_generator import LocalizationCodeGenerator
        
        generator = LocalizationCodeGenerator()
        
        test_strings = {
            "test_key": "Test Value",
            "another_key": "Another Value"
        }
        
        swift_code = generator.generate_swift_extensions(test_strings)
        
        if "extension String" in swift_code and "extension LocalizedStringKey" in swift_code:
            print("✅ Localization code generator test passed")
            return True
        else:
            print("❌ Localization code generator test failed")
            return False
            
    except Exception as e:
        print(f"❌ Localization code generator test failed: {e}")
        return False


def main():
    """Main function"""
    
    print("iOS Multi-language Translator - Setup Verification")
    print("=" * 60)
    
    tests = [
        ("Dependencies", check_dependencies),
        ("DeepL Initialization", test_deepl_initialization),
        ("Basic Translation", test_basic_translation),
        ("Strings Parser", test_strings_parser),
        ("Code Generator", test_code_generator),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed!")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The iOS translator is ready to use.")
        print("\nNext steps:")
        print("1. Run: python ios_translator.py /path/to/your/ios/project")
        print("2. Or try: python demo_deepl.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()