#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Translator Demo Script
Demonstrate how to use the new LLM translator
"""

from translator import create_translator


def demo_llm_translator():
    """Demonstrate LLM translator usage"""
    
    print("LLM Translator Demo")
    print("=" * 50)
    
    # Default API endpoint (Ollama local server)
    api_url = "http://127.0.0.1:11434/api/generate"
    model = "mistral:latest"
    
    try:
        # Create LLM translator
        print(f"Initializing LLM translator...")
        print(f"API URL: {api_url}")
        print(f"Model: {model}")
        
        translator = create_translator('llm', 
                                     api_url=api_url, 
                                     model=model)
        print("✅ LLM translator initialized successfully!")
        
        # Check supported languages
        print(f"\nSupported languages:")
        languages = translator.get_supported_languages()
        print(f"Total: {len(languages)} languages")
        print(f"Sample: {', '.join(languages[:10])}...")
        
        # Test single translation
        print(f"\nTesting single translation...")
        test_text = "Hello, welcome to our app!"
        print(f"Translating: '{test_text}' to Chinese...")
        
        # Note: This will fail if LLM server is not running
        result = translator.translate(test_text, "zh")
        if result:
            print(f"✅ Translation successful:")
            print(f"   EN: {test_text}")
            print(f"   ZH: {result}")
        else:
            print(f"❌ Translation failed (is LLM server running?)")
        
        # Test batch translation
        print(f"\nTesting batch translation...")
        test_texts = {
            "greeting": "Hello",
            "welcome": "Welcome to our app",
            "save_button": "Save",
            "cancel_button": "Cancel"
        }
        
        print(f"Translating {len(test_texts)} texts to Japanese...")
        results = translator.translate_batch(test_texts, "ja")
        
        print(f"Batch translation results:")
        for key, original in test_texts.items():
            translated = results.get(key, "Translation failed")
            print(f"  {key}: {original} -> {translated}")
        
        print(f"\n✅ LLM demo completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Make sure your LLM server is running at {api_url}")
        print(f"2. For Ollama, run: ollama serve")
        print(f"3. Check if model '{model}' is available: ollama list")
        print(f"4. Try a different model with: --llm-model <model_name>")


def demo_custom_llm():
    """Demonstrate custom LLM configuration"""
    
    print("\nCustom LLM Configuration Demo")
    print("=" * 50)
    
    # Example configurations for different LLM services
    configs = [
        {
            "name": "Ollama (Local)",
            "api_url": "http://127.0.0.1:11434/api/generate",
            "model": "mistral:latest"
        },
        {
            "name": "Ollama (Custom Port)",
            "api_url": "http://localhost:8080/api/generate", 
            "model": "mistral"
        },
        {
            "name": "Custom LLM Server",
            "api_url": "http://192.168.1.100:8000/api/chat",
            "model": "gpt-3.5-turbo"
        }
    ]
    
    print("Example LLM configurations:")
    
    for i, config in enumerate(configs, 1):
        print(f"\n{i}. {config['name']}:")
        print(f"   URL: {config['api_url']}")
        print(f"   Model: {config['model']}")
        
        # Show how to create translator with this config
        print(f"   Command: python ios_translator.py /path/to/project \\")
        print(f"            --translator llm \\")
        print(f"            --llm-url {config['api_url']} \\")
        print(f"            --llm-model {config['model']}")


def main():
    """Main function"""
    print("iOS Translation Script - LLM Translator Demo")
    print("=" * 60)
    
    # Basic LLM demo
    demo_llm_translator()
    
    # Custom configuration examples
    demo_custom_llm()
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("\nUsage examples:")
    print("# Use LLM translator with default settings:")
    print("python ios_translator.py /path/to/project --translator llm")
    print("\n# Use custom LLM server:")
    print("python ios_translator.py /path/to/project --translator llm \\")
    print("  --llm-url http://localhost:8080/api/generate --llm-model mistral")


if __name__ == "__main__":
    main()
