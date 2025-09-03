# 🚀 Quick Start Guide

**🌍 Language: [English](QUICKSTART.md) | [中文](QUICKSTART_cn.md)**

## 🔧 Prerequisites

- Python 3.7+ installed
- iOS project with `en.lproj/Localizable.strings`

## 📦 1. Install Dependencies

```bash
cd AppleStringsTranslator
pip install -r requirements.txt
```

## ⚙️ 2. Setup Configuration

```bash
# Run configuration setup tool
python setup_config.py

# Edit configuration file
vim .env
```

Add your API key to `.env`:
```bash
DEEPL_API_KEY=your-actual-deepl-api-key
```

## 🎯 3. Run Translation

### Using DeepL API (Recommended)

```bash
python ios_translator.py /path/to/your/project --auth-key "your-deepl-api-key"
```

### Using LLM Translator (Local Large Language Model)

```bash
# Use default configuration (Ollama local service)
python ios_translator.py /path/to/your/project --translator llm

# Use custom LLM service
python ios_translator.py /path/to/your/project --translator llm \
  --llm-url "http://127.0.0.1:11434/api/generate" \
  --llm-model "llama2"
```

### Using Mock Translator (Testing)

```bash
python ios_translator.py /path/to/your/project --translator mock
```

## 🧪 4. Run Examples

```bash
# Basic example
python example.py

# DeepL translation demo
python demo_deepl.py

# LLM translation demo
python demo_llm.py
```

These scripts will create example projects and run different translation demos.

## ✅ 5. Test Functionality

```bash
python test_functionality.py
```

## 📱 6. Generated Code Usage

### In UIKit:

```swift
import UIKit

// Use generated String extensions
welcomeLabel.text = String.welcomeMessage
saveButton.setTitle(String.saveButton, for: .normal)
```

### In SwiftUI:

```swift
import SwiftUI

// Use generated LocalizedStringKey extensions
Text(.welcomeMessage)
Button(.saveButton) { /* action */ }
```

## ❓ FAQ

### Q: How to get DeepL API key?
A: Visit https://www.deepl.com/pro-api to register an account and get API key.

### Q: How to setup LLM translator?
A: 
1. Install Ollama: https://ollama.ai
2. Start service: `ollama serve`
3. Download model: `ollama pull llama2`
4. Use LLM translator: `--translator llm`

### Q: Which languages are supported?
A: Supports all iOS standard language codes including Chinese, Japanese, Korean, French, German, etc.

### Q: How's the translation quality?
A: DeepL provides professional-grade translation quality, LLM translator quality depends on the model used.

### Q: How to handle translation errors?
A: The script preserves original text, you can manually edit Localizable.strings files.

## 🔧 Advanced Usage

```bash
# Only generate code, no translation
python ios_translator.py /path/to/project --no-swift

# Generate Objective-C header file
python ios_translator.py /path/to/project --generate-objc

# Check DeepL API usage
python ios_translator.py /path/to/project --check-usage

# Use custom LLM server
python ios_translator.py /path/to/project --translator llm \
  --llm-url "http://192.168.1.100:8000/api/chat" \
  --llm-model "gpt-3.5-turbo"

# Use different Ollama model
python ios_translator.py /path/to/project --translator llm \
  --llm-model "mistral"
```

## 🎉 All Set!

Your iOS multi-language translation workflow is now ready! 

For more detailed information, check:
- [README.md](README.md) - Complete documentation
- [SECURITY.md](SECURITY.md) - Security configuration guide
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Usage examples