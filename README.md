# iOS Multi-language Translator

**🌍 Language: [English](README.md) | [中文](README_cn.md)**

## Overview

An intelligent iOS multi-language translation tool that supports DeepL API, Local LLM, and automatic code generation. Designed for iOS developers to streamline the localization process.

## ✨ Features

- 🔍 **Auto-scan**: Reads `Localizable.strings` from `en.lproj` folder
- 🌐 **Batch translation**: Automatically translates missing localization strings to various languages
- 📝 **Code generation**: Generates Swift extension code with UIKit and SwiftUI support
- 🔌 **Multiple translation engines**: Supports DeepL, LLM (Large Language Models), and Mock translators
- 🚀 **DeepL integration**: Uses official DeepL Python library for professional-grade translation quality
- 🧠 **LLM support**: Supports local and remote LLM APIs (Ollama, ChatGPT, etc.)

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### First-time Setup (Recommended)

```bash
# 1. Setup configuration
python setup_config.py

# 2. Edit configuration file (add your API keys)
vim .env

# 3. Check configuration
python ios_translator.py --show-config

# 4. Run translation
python ios_translator.py /path/to/your/ios/project
```

### Direct Usage

```bash
python ios_translator.py /path/to/your/ios/project
```

### Advanced Options

```bash
# Use DeepL translator (recommended)
python ios_translator.py /path/to/project --auth-key "your-api-key"

# Use LLM translator (local large language model)
python ios_translator.py /path/to/project --translator llm

# Use custom LLM service
python ios_translator.py /path/to/project --translator llm \
  --llm-url "http://127.0.0.1:11434/api/generate" --llm-model "llama2"

# Generate Objective-C header file
python ios_translator.py /path/to/project --generate-objc

# Specify custom output directory (default outputs to project root)
python ios_translator.py /path/to/project --output-dir /path/to/custom/output

# Use mock translator (for testing)
python ios_translator.py /path/to/project --translator mock

# Check DeepL API usage
python ios_translator.py /path/to/project --check-usage
```

## 📁 Required Directory Structure

Your iOS project should have the following structure:

```
YourProject/
├── en.lproj/
│   └── Localizable.strings    # Required: English strings
├── zh-Hans.lproj/            # Optional, will be created automatically
├── ja.lproj/                 # Optional, will be created automatically
└── ... other language directories
```

## 📱 Generated Code Examples

### Swift Extensions

```swift
// UIKit
label.text = String.welcomeMessage
button.setTitle(String.saveButton, for: .normal)

// SwiftUI
Text(.welcomeMessage)
Button(.saveButton) { /* action */ }
```

## 🔐 Configuration Management (Open Source Safe)

To safely open source the project, this tool provides multiple configuration methods to protect API keys:

### 🚀 Quick Configuration

```bash
# 1. Run configuration setup tool
python setup_config.py

# 2. Edit configuration file
vim .env  # or vim config.py

# 3. Add your API keys
DEEPL_API_KEY=your-actual-api-key

# 4. Check configuration
python ios_translator.py --show-config
```

### 📋 Configuration Priority

1. **Command line arguments** (Highest priority)
2. **Environment variables**
3. **`.env` file**
4. **`config.py` file**
5. **Default values** (Lowest priority)

### 🔧 Configuration Methods

#### Method 1: Environment Variables (Recommended for production)
```bash
export DEEPL_API_KEY="your-api-key"
export LLM_API_URL="http://127.0.0.1:11434/api/generate"
python ios_translator.py /path/to/project
```

#### Method 2: .env file (Recommended for development)
```bash
cp env.example .env
# Edit .env file to add actual keys
```

#### Method 3: config.py file
```bash
cp config.py.example config.py
# Edit config.py file to add actual keys
```

#### Method 4: Command line arguments (Temporary use)
```bash
python ios_translator.py /path/to/project --auth-key "your-api-key"
```

### 🔒 Security Features

- ✅ **Auto-ignore sensitive files** - `.env` and `config.py` are added to `.gitignore`
- ✅ **Template files** - Provides `.example` files for safe open source sharing
- ✅ **Configuration validation** - Automatically checks configuration correctness
- ✅ **Sensitive data masking** - Automatically hides keys when displaying configuration

## 🌐 Translation Service Configuration

### DeepL API Setup

1. Register an account at [DeepL website](https://www.deepl.com/pro-api)
2. Get API key
3. Set key via configuration files or environment variables

**Free vs Professional versions**:
- Free version: 500,000 characters per month limit
- Professional version: Unlimited with higher API call frequency

### LLM Service Setup

**Using Ollama (Recommended local solution)**:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start service
ollama serve

# Download models
ollama pull llama2
ollama pull mistral

# Use LLM translator
python ios_translator.py /path/to/project --translator llm
```

**Other LLM services**:
- OpenAI API
- Claude API  
- Self-hosted LLM services
- Any compatible API endpoint

## 🗣️ Supported Languages

- `zh` - Chinese (Simplified)
- `zh-Hans` - Chinese (Simplified)
- `zh-Hant` - Chinese (Traditional)
- `zh-TW` - Chinese (Taiwan)
- `ja` - Japanese
- `ko` - Korean
- `fr` - French
- `de` - German
- `es` - Spanish
- `it` - Italian
- `pt` - Portuguese
- `pt-BR` - Portuguese (Brazil)
- `ru` - Russian
- `ar` - Arabic
- `tr` - Turkish
- And more...

## 🔌 Supported Translators

### 1. DeepL Translator (Recommended)
- Professional-grade translation quality
- Supports batch translation optimization
- Requires API key

### 2. LLM Translator (Large Language Models)
- Supports local and remote LLM services
- Compatible with Ollama, ChatGPT, etc.
- Customizable models and prompts

### 3. Mock Translator
- For testing and development
- No network connection required

## 🚀 Extending Translators

Modular design makes it easy to add new translation services:

```python
from translators import TranslatorBase

class MyCustomTranslator(TranslatorBase):
    def translate(self, text: str, target_language: str, source_language: str = 'en'):
        # Implement your translation logic
        pass
    
    def get_supported_languages(self):
        # Return supported language list
        pass
```

## ⚠️ Error Handling

The script includes comprehensive error handling:

- API quota exceeded handling
- Network timeout handling
- Invalid language code handling
- File permission error handling

## 💡 Best Practices

1. **Backup**: It's recommended to backup existing localization files before running the script
2. **Testing**: Use mock translator for testing workflows
3. **Review**: Manually review translations for important content
4. **Encoding**: Ensure .strings files use UTF-8 or UTF-16 encoding

## 📂 Project Structure

```
AppleStringsTranslator/
├── README.md                    # Main documentation (English)
├── README_cn.md                 # Chinese documentation
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── ios_translator.py            # Main script ⭐
├── config.py                    # User configuration (auto-generated)
├── .gitignore                   # Git ignore rules
├── docs/                        # 📚 Documentation
│   ├── QUICKSTART.md            # Quick start guide
│   ├── SECURITY.md              # Security configuration
│   ├── USAGE_EXAMPLES.md        # Detailed examples
│   ├── OPENSOURCE_GUIDE.md      # Open source guide
│   └── PROJECT_SUMMARY.md       # Project summary
├── src/                         # 🔧 Source code
│   ├── translator.py            # Translator interface
│   ├── strings_parser.py        # .strings file parser
│   ├── code_generator.py        # Swift/ObjC code generator
│   ├── config_manager.py        # Configuration management
│   └── translators/             # Translation implementations
│       ├── base.py              # Base translator class
│       ├── deepl_translator.py  # DeepL API
│       ├── llm_translator.py    # LLM API ⭐
│       └── mock_translator.py   # Testing translator
├── examples/                    # 📝 Usage examples
│   ├── example.py               # Basic usage example
│   ├── demo_deepl.py            # DeepL demo
│   └── demo_llm.py              # LLM demo ⭐
├── tests/                       # 🧪 Test suite
│   ├── test_functionality.py    # Functionality tests
│   └── verify_setup.py          # Setup verification
├── scripts/                     # 🛠️ Utility scripts
│   └── setup_config.py          # Configuration setup
└── config/                      # ⚙️ Configuration templates
    ├── env.example              # Environment template
    └── config.py.example        # Python config template
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.