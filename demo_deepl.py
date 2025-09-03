#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepL API Demo Script
Demonstrate how to use the new official DeepL library
"""

from translator import create_translator


def demo_deepl_translator():
    """Demonstrate DeepL translator usage"""
    
    print("DeepL Translator Demo")
    print("=" * 50)
    
    # Use the provided API key
    # Use your actual API key or configure it via .env file
    from config_manager import get_config
    config = get_config()
    auth_key = config.get_deepl_key()
    
    if not auth_key:
        print("❌ No DeepL API key configured!")
        print("Please set up your API key using one of these methods:")
        print("1. Run: python setup_config.py")
        print("2. Edit .env file: DEEPL_API_KEY=your-key-here")
        print("3. Set environment: export DEEPL_API_KEY=your-key-here")
        return
    
    try:
        # Create DeepL translator
        print("Initializing DeepL translator...")
        translator = create_translator('deepl', auth_key=auth_key)
        print("✅ DeepL translator initialized successfully!")
        
        # Check API usage
        print("\nChecking API usage...")
        usage = translator.check_api_usage()
        if usage:
            print(f"Characters used: {usage['character_count']}/{usage['character_limit']}")
            if usage['character_limit_reached']:
                print("⚠️ Character limit reached!")
            else:
                remaining = usage['character_limit'] - usage['character_count']
                print(f"Characters remaining: {remaining}")
        
        # Get supported languages
        print("\nGetting supported languages...")
        languages = translator.get_supported_languages()
        print(f"Supported languages ({len(languages)}): {', '.join(languages[:10])}...")
        
        # Test single translation
        print("\nTesting single translation...")
        test_text = "Hello, welcome to our app!"
        result = translator.translate(test_text, "zh")
        if result:
            print(f"EN: {test_text}")
            print(f"ZH: {result}")
        
        # Test batch translation
        print("\nTesting batch translation...")
        test_texts = {
            "greeting": "Hello",
            "welcome": "Welcome to our app",
            "save_button": "Save",
            "cancel_button": "Cancel",
            "error_message": "An error occurred"
        }
        
        results = translator.translate_batch(test_texts, "ja")
        print("Batch translation results (EN -> JA):")
        for key, original in test_texts.items():
            translated = results.get(key, "Translation failed")
            print(f"  {key}: {original} -> {translated}")
        
        print("\n✅ DeepL demo completed successfully!")
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Please install the deepl library: pip install deepl")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("This might be due to network issues or API key problems.")


def demo_mock_translator():
    """Demonstrate mock translator usage"""
    
    print("\nMock Translator Demo")
    print("=" * 50)
    
    try:
        # Create mock translator
        translator = create_translator('mock')
        print("✅ Mock translator initialized!")
        
        # Test batch translation
        test_texts = {
            "greeting": "Hello",
            "welcome": "Welcome to our app",
            "save_button": "Save",
            "cancel_button": "Cancel"
        }
        
        results = translator.translate_batch(test_texts, "zh")
        print("Mock translation results (EN -> ZH):")
        for key, original in test_texts.items():
            translated = results.get(key, "Translation failed")
            print(f"  {key}: {original} -> {translated}")
        
        print("✅ Mock demo completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function"""
    print("iOS Translation Script - DeepL Demo")
    print("=" * 60)
    
    # Demonstrate DeepL translator
    demo_deepl_translator()
    
    # Demonstrate mock translator
    demo_mock_translator()
    
    print("\n" + "=" * 60)
    print("Demo completed!")


if __name__ == "__main__":
    main()