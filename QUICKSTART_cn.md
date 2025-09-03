# 🚀 快速开始指南

**🌍 Language: [English](QUICKSTART.md) | [中文](QUICKSTART_cn.md)**

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

> 注意：脚本现在使用官方的 `deepl` Python库，提供更好的性能和批量翻译优化。

## 2. 准备项目结构

确保您的iOS项目有以下结构：

```
YourProject/
├── en.lproj/
│   └── Localizable.strings    # 必须存在
├── zh-Hans.lproj/            # 可选，会自动创建
├── ja.lproj/                 # 可选，会自动创建
└── ... 其他语言目录
```

## 3. 运行翻译

### 使用DeepL API（推荐）

```bash
python ios_translator.py /path/to/your/project --auth-key "your-deepl-api-key"
```

### 使用LLM翻译器（本地大语言模型）

```bash
# 使用默认配置 (Ollama本地服务)
python ios_translator.py /path/to/your/project --translator llm

# 使用自定义LLM服务
python ios_translator.py /path/to/your/project --translator llm \
  --llm-url "http://127.0.0.1:11434/api/generate" \
  --llm-model "llama2"
```

### 使用模拟翻译器（测试）

```bash
python ios_translator.py /path/to/your/project --translator mock
```

## 4. 运行示例

```bash
# 基本示例
python example.py

# DeepL翻译演示
python demo_deepl.py

# LLM翻译演示
python demo_llm.py
```

这些脚本会创建示例项目并运行不同的翻译演示。

## 5. 测试功能

```bash
python test_functionality.py
```

运行所有功能测试以确保脚本正常工作。

## 6. 使用生成的Swift代码

脚本会生成 `LocalizedStrings.swift` 文件，您可以直接在项目中使用：

```swift
// UIKit
label.text = .welcomeMessage
button.setTitle(.saveButton, for: .normal)

// SwiftUI
Text(.welcomeMessage)
Button(.saveButton) { /* action */ }
```

## 常见问题

### Q: 如何获取DeepL API密钥？
A: 访问 https://www.deepl.com/pro-api 注册账户并获取API密钥。

### Q: 如何设置LLM翻译器？
A: 
1. 安装Ollama: https://ollama.ai
2. 启动服务: `ollama serve`
3. 下载模型: `ollama pull llama2`
4. 使用LLM翻译器: `--translator llm`

### Q: 支持哪些语言？
A: 支持所有iOS标准语言代码，包括中文、日语、韩语、法语、德语等。

### Q: 翻译质量如何？
A: DeepL提供专业级翻译质量，LLM翻译器质量取决于使用的模型。

### Q: 如何处理翻译错误？
A: 脚本会保留原始文本，您可以手动编辑Localizable.strings文件。

## 高级用法

```bash
# 只生成代码，不翻译
python ios_translator.py /path/to/project --no-swift

# 生成Objective-C头文件
python ios_translator.py /path/to/project --generate-objc

# 检查DeepL API使用情况
python ios_translator.py /path/to/project --check-usage

# 使用自定义LLM服务器
python ios_translator.py /path/to/project --translator llm \
  --llm-url "http://192.168.1.100:8000/api/chat" \
  --llm-model "gpt-3.5-turbo"

# 使用不同的Ollama模型
python ios_translator.py /path/to/project --translator llm \
  --llm-model "mistral"
```
