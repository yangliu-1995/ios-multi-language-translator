# 📚 Usage Examples

**🌍 Language: [English](USAGE_EXAMPLES.md) | [中文](USAGE_EXAMPLES_cn.md)**

## 🔧 Basic Translation Examples

### Using DeepL API

```python
from translator import create_translator

# Use your actual API key
auth_key = "your-actual-deepl-api-key"
translator = create_translator('deepl', auth_key=auth_key)

# Single translation
result = translator.translate("Hello, world!", "zh")
print(result)  # Output Chinese translation
```

### Using LLM Translator

```python
from translator import create_translator

# Create LLM translator (default: Ollama local service)
translator = create_translator('llm')

# Single translation
result = translator.translate("Welcome to our app", "ja")
print(result)  # Output Japanese translation
```

### Using Mock Translator (Testing)

```python
from translator import create_translator

# Create mock translator (no API key needed)
translator = create_translator('mock')

# Single translation
result = translator.translate("Save", "fr")
print(result)  # Output: [FR] Save
```

## 🎯 Batch Translation

### Batch Processing with DeepL

```python
from translator import create_translator

translator = create_translator('deepl', auth_key='your-api-key')

# Batch translation
texts = {
    "welcome": "Welcome",
    "save": "Save", 
    "cancel": "Cancel",
    "settings": "Settings"
}

results = translator.translate_batch(texts, "es")
for key, translation in results.items():
    print(f"{key}: {translation}")
```

### Batch Processing with LLM

```python
from translator import create_translator

translator = create_translator('llm', 
                              api_url='http://127.0.0.1:11434/api/generate',
                              model='mistral:latest')

# Batch translation
texts = {
    "login": "Log In",
    "logout": "Log Out",
    "profile": "Profile"
}

results = translator.translate_batch(texts, "ko")
for key, translation in results.items():
    print(f"{key}: {translation}")
```

## 📱 Complete iOS Project Example

### Project Setup

```python
import os
from ios_translator import iOSTranslator
from translator import create_translator

# Setup project path
project_path = "/Users/developer/MyiOSApp"

# Create translator
translator = create_translator('deepl', auth_key='your-api-key')

# Create iOS translator instance
ios_translator = iOSTranslator(project_path, translator)

# Run full translation process
success = ios_translator.run(
    generate_swift=True,
    generate_objc=True,
    output_dir=None  # Uses project root directory
)

if success:
    print("✅ Translation completed successfully!")
else:
    print("❌ Translation failed!")
```

## 🔍 Strings Parser Examples

### Reading Localizable.strings

```python
from strings_parser import StringsParser

parser = StringsParser()

# Parse existing strings file
strings_dict = parser.parse_strings_file('/path/to/Localizable.strings')

# Print all strings
for key, value in strings_dict.items():
    print(f'"{key}" = "{value}";')
```

### Writing Localizable.strings

```python
from strings_parser import StringsParser

parser = StringsParser()

# Create new strings
new_strings = {
    "welcome_title": "Welcome",
    "save_button": "Save",
    "cancel_button": "Cancel"
}

# Write to file
success = parser.write_strings_file(
    new_strings, 
    '/path/to/Localizable.strings',
    preserve_order=True
)

if success:
    print("✅ Strings file written successfully!")
```

### Updating Existing Strings

```python
from strings_parser import StringsParser

parser = StringsParser()

# New translations to add
new_translations = {
    "new_feature": "New Feature",
    "coming_soon": "Coming Soon"
}

# Update existing file
success = parser.update_strings_file(
    '/path/to/zh-Hans.lproj/Localizable.strings',
    new_translations,
    reference_order=english_strings  # Maintain English file order
)
```

## 🎨 Code Generation Examples

### Swift Extension Generation

```python
from code_generator import LocalizationCodeGenerator

generator = LocalizationCodeGenerator()

# English strings
strings_dict = {
    "welcome_message": "Welcome to our app!",
    "save_button": "Save",
    "settings_title": "Settings"
}

# Generate Swift extensions
swift_code = generator.generate_swift_extensions(
    strings_dict, 
    '/path/to/LocalizedStrings.swift'
)

print("Generated Swift code:")
print(swift_code)
```

### Objective-C Header Generation

```python
from code_generator import LocalizationCodeGenerator

generator = LocalizationCodeGenerator()

# Generate Objective-C header
objc_code = generator.generate_objc_header(
    strings_dict,
    '/path/to/LocalizedStrings.h'
)

print("Generated Objective-C code:")
print(objc_code)
```

## 🌐 Multi-language Setup Example

### Complete Project Setup

```python
#!/usr/bin/env python3
"""
Complete iOS localization setup example
"""

import os
from translator import create_translator
from ios_translator import iOSTranslator

def setup_multilanguage_project(project_path, api_key):
    """Setup complete multi-language project"""
    
    print(f"Setting up multi-language support for: {project_path}")
    
    # Verify English strings exist
    en_strings_path = os.path.join(project_path, 'en.lproj', 'Localizable.strings')
    if not os.path.exists(en_strings_path):
        print("❌ English Localizable.strings not found!")
        return False
    
    # Create translator
    translator = create_translator('deepl', auth_key=api_key)
    
    # Setup iOS translator
    ios_translator = iOSTranslator(project_path, translator)
    
    # Run translation for all languages
    success = ios_translator.run(
        generate_swift=True,
        generate_objc=True
    )
    
    if success:
        print("✅ Multi-language setup completed!")
        print(f"📄 Swift code: {project_path}/LocalizedStrings.swift")
        print(f"📄 ObjC header: {project_path}/LocalizedStrings.h")
        
        # Show usage examples
        print("\n📱 Usage in your iOS app:")
        print("Swift: String.welcomeMessage")
        print("SwiftUI: Text(.welcomeMessage)")
        print("ObjC: [LocalizedStrings welcomeMessage]")
        
        return True
    else:
        print("❌ Multi-language setup failed!")
        return False

# Example usage
if __name__ == "__main__":
    project_path = "/Users/developer/MyiOSApp"
    api_key = "your-deepl-api-key"
    
    setup_multilanguage_project(project_path, api_key)
```

## 🔧 Configuration Examples

### Using Environment Variables

```bash
#!/bin/bash
# setup_env.sh

# Set environment variables
export DEEPL_API_KEY="your-actual-api-key"
export LLM_API_URL="http://127.0.0.1:11434/api/generate"
export LLM_MODEL="mistral:latest"
export DEFAULT_TRANSLATOR="deepl"

# Run translation
python ios_translator.py /path/to/project
```

### Using Configuration Files

```python
# config.py example
DEEPL_API_KEY = "your-actual-api-key"

LLM_CONFIG = {
    "api_url": "http://127.0.0.1:11434/api/generate",
    "model": "mistral:latest",
    "timeout": 60
}

TRANSLATION_CONFIG = {
    "default_translator": "deepl",
    "rate_limit_delay": 1.0,
    "preserve_order": True
}
```

## 🧪 Testing Examples

### Unit Testing

```python
import unittest
from translator import create_translator

class TestTranslators(unittest.TestCase):
    
    def test_mock_translator(self):
        """Test mock translator"""
        translator = create_translator('mock')
        result = translator.translate("Hello", "zh")
        self.assertEqual(result, "[ZH] Hello")
    
    def test_deepl_translator(self):
        """Test DeepL translator (requires API key)"""
        translator = create_translator('deepl', auth_key='your-test-key')
        result = translator.translate("Hello", "zh")
        self.assertIsNotNone(result)
        self.assertNotEqual(result, "Hello")  # Should be translated
    
    def test_llm_translator(self):
        """Test LLM translator (requires running LLM)"""
        translator = create_translator('llm')
        result = translator.translate("Hello", "zh")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```python
#!/usr/bin/env python3
"""
Integration test example
"""

import tempfile
import os
from translator import create_translator
from ios_translator import iOSTranslator

def test_full_workflow():
    """Test complete translation workflow"""
    
    # Create temporary test project
    with tempfile.TemporaryDirectory() as temp_dir:
        # Setup test project structure
        en_dir = os.path.join(temp_dir, 'en.lproj')
        os.makedirs(en_dir)
        
        # Create test English strings
        en_strings_path = os.path.join(en_dir, 'Localizable.strings')
        with open(en_strings_path, 'w', encoding='utf-8') as f:
            f.write('/* Test strings */\n')
            f.write('"hello" = "Hello";\n')
            f.write('"world" = "World";\n')
        
        # Use mock translator for testing
        translator = create_translator('mock')
        ios_translator = iOSTranslator(temp_dir, translator)
        
        # Run translation
        success = ios_translator.run(generate_swift=True)
        
        if success:
            print("✅ Integration test passed!")
            
            # Check generated files
            swift_file = os.path.join(temp_dir, 'LocalizedStrings.swift')
            if os.path.exists(swift_file):
                print("✅ Swift file generated successfully!")
            else:
                print("❌ Swift file not generated!")
        else:
            print("❌ Integration test failed!")

if __name__ == "__main__":
    test_full_workflow()
```

---

These examples demonstrate the complete usage of the iOS Multi-language Translator tool. For more information, check the [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md) files.