# iOS多语言翻译工具

**🌍 Language: [English](README.md) | [中文](README_cn.md)**

一个自动化的iOS多语言翻译脚本，用于处理Localizable.strings文件的翻译和Swift代码生成。

## 功能特性

- 🔍 **自动扫描**: 读取`en.lproj`文件夹下的`Localizable.strings`文件
- 🌐 **批量翻译**: 自动翻译缺失的本地化字符串到各种语言
- 📝 **代码生成**: 生成Swift extension代码，支持UIKit和SwiftUI
- 🔌 **多翻译引擎**: 支持DeepL、LLM（大语言模型）和Mock翻译器
- 🚀 **DeepL集成**: 使用官方DeepL Python库，提供专业级翻译质量
- 🧠 **LLM支持**: 支持本地和远程大语言模型API（如Ollama、ChatGPT等）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

### 首次使用（推荐）

```bash
# 1. 设置配置
python setup_config.py

# 2. 编辑配置文件（添加您的API密钥）
vim .env

# 3. 检查配置
python ios_translator.py --show-config

# 4. 运行翻译
python ios_translator.py /path/to/your/ios/project
```

### 直接使用

```bash
python ios_translator.py /path/to/your/ios/project
```

### 高级选项

```bash
# 使用DeepL翻译器（推荐）
python ios_translator.py /path/to/project --auth-key "your-api-key"

# 使用LLM翻译器（本地大语言模型）
python ios_translator.py /path/to/project --translator llm

# 使用自定义LLM服务
python ios_translator.py /path/to/project --translator llm \
  --llm-url "http://127.0.0.1:11434/api/generate" --llm-model "llama2"

# 生成Objective-C头文件
python ios_translator.py /path/to/project --generate-objc

# 指定自定义输出目录（默认输出到项目根目录）
python ios_translator.py /path/to/project --output-dir /path/to/custom/output

# 使用模拟翻译器（测试用）
python ios_translator.py /path/to/project --translator mock

# 检查DeepL API使用情况
python ios_translator.py /path/to/project --check-usage
```

## 目录结构要求

您的iOS项目应该具有以下结构：

```
YourProject/
├── en.lproj/
│   └── Localizable.strings    # 英文基础文件
├── zh-Hans.lproj/
│   └── Localizable.strings    # 中文简体（可选，会自动创建缺失的键）
├── ja.lproj/
│   └── Localizable.strings    # 日语（可选）
└── ... 其他语言目录
```

## Localizable.strings 文件格式

```objc
/* 按钮标题 */
"done_button_default_title" = "Done";

/* 欢迎消息 */
"welcome_message" = "Welcome to our app!";

/* 错误提示 */
"error_network_unavailable" = "Network unavailable. Please try again.";
```

## 生成的Swift代码

脚本会生成`LocalizedStrings.swift`文件，包含String和LocalizedStringKey的extension：

### UIKit 使用方式

```swift
// 设置Label文本
label.text = .doneButtonDefaultTitle

// 设置Button标题
button.setTitle(.welcomeMessage, for: .normal)

// Alert标题
let alert = UIAlertController(title: .errorNetworkUnavailable, message: nil, preferredStyle: .alert)
```

### SwiftUI 使用方式

```swift
// Text视图
Text(.welcomeMessage)

// Button标题
Button(.doneButtonDefaultTitle) {
    // 按钮动作
}

// Alert标题
.alert(.errorNetworkUnavailable, isPresented: $showAlert) {
    // Alert内容
}
```

## 支持的语言

脚本支持以下iOS本地化语言代码：

- `en` - 英语
- `zh-Hans` - 中文简体
- `zh-Hant` - 中文繁体
- `ja` - 日语
- `ko` - 韩语
- `fr` - 法语
- `de` - 德语
- `es` - 西班牙语
- `it` - 意大利语
- `pt` - 葡萄牙语
- `pt-BR` - 巴西葡萄牙语
- `ru` - 俄语
- `ar` - 阿拉伯语
- `tr` - 土耳其语
- 以及更多...

## 支持的翻译器

### 1. DeepL翻译器（推荐）
- 专业级翻译质量
- 支持批量翻译优化
- 需要API密钥

### 2. LLM翻译器（大语言模型）
- 支持本地和远程LLM服务
- 兼容Ollama、ChatGPT等API
- 可自定义模型和提示词

### 3. Mock翻译器
- 用于测试和开发
- 无需网络连接

## 翻译器扩展

模块化设计，轻松添加新的翻译服务：

```python
from translators import TranslatorBase

class MyCustomTranslator(TranslatorBase):
    def translate(self, text: str, target_language: str, source_language: str = 'en'):
        # 实现您的翻译逻辑
        pass
    
    def get_supported_languages(self):
        # 返回支持的语言列表
        pass
```

## 🔐 配置管理（开源安全）

为了安全地开源项目，本工具提供多种配置方式来保护API密钥：

### 🚀 快速配置

```bash
# 1. 运行配置设置工具
python setup_config.py

# 2. 编辑配置文件
vim .env  # 或 vim config.py

# 3. 添加您的API密钥
DEEPL_API_KEY=your-actual-api-key

# 4. 检查配置
python ios_translator.py --show-config
```

### 📋 配置优先级

1. **命令行参数** (最高优先级)
2. **环境变量**
3. **`.env` 文件**
4. **`config.py` 文件**
5. **默认值** (最低优先级)

### 🔧 配置方式

#### 方式1：环境变量（推荐生产环境）
```bash
export DEEPL_API_KEY="your-api-key"
export LLM_API_URL="http://127.0.0.1:11434/api/generate"
python ios_translator.py /path/to/project
```

#### 方式2：.env 文件（推荐开发环境）
```bash
cp env.example .env
# 编辑 .env 文件添加实际密钥
```

#### 方式3：config.py 文件
```bash
cp config.py.example config.py
# 编辑 config.py 文件添加实际密钥
```

#### 方式4：命令行参数（临时使用）
```bash
python ios_translator.py /path/to/project --auth-key "your-api-key"
```

### 🔒 安全特性

- ✅ **自动忽略敏感文件** - `.env` 和 `config.py` 已添加到 `.gitignore`
- ✅ **模板文件** - 提供 `.example` 文件供开源分享
- ✅ **配置验证** - 自动检查配置是否正确
- ✅ **敏感信息掩码** - 显示配置时自动隐藏密钥

## 翻译服务配置

### DeepL API设置

1. 在[DeepL网站](https://www.deepl.com/pro-api)注册账户
2. 获取API密钥
3. 通过配置文件或环境变量设置密钥

**免费版vs专业版**:
- 免费版: 每月50万字符限制
- 专业版: 无限制，更高的API调用频率

### LLM服务设置

**使用Ollama（推荐本地方案）**:
```bash
# 安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 启动服务
ollama serve

# 下载模型
ollama pull llama2
ollama pull mistral

# 使用LLM翻译器
python ios_translator.py /path/to/project --translator llm
```

**其他LLM服务**:
- OpenAI API
- Claude API  
- 自建LLM服务
- 任何兼容的API端点

## 错误处理

脚本包含完善的错误处理机制：

- ✅ 网络连接错误重试
- ✅ API限制自动延迟
- ✅ 文件编码自动检测（UTF-8/UTF-16）
- ✅ 保留原文本（翻译失败时）
- ✅ 详细的日志输出

## 注意事项

1. **API限制**: DeepL免费版有月度字符限制，请注意使用量
2. **翻译质量**: 建议人工审核机器翻译的结果
3. **备份**: 运行脚本前建议备份现有的本地化文件
4. **编码**: 确保.strings文件使用UTF-8或UTF-16编码

## 文件说明

- `ios_translator.py` - 主脚本文件
- `strings_parser.py` - Localizable.strings文件解析器
- `translator.py` - 翻译器统一接口（向后兼容）
- `translators/` - 模块化翻译器实现
  - `base.py` - 翻译器基类
  - `deepl_translator.py` - DeepL API实现
  - `llm_translator.py` - LLM API实现  
  - `mock_translator.py` - 测试翻译器
- `code_generator.py` - Swift/ObjC代码生成器
- `config_manager.py` - 配置管理器 ⭐
- `setup_config.py` - 配置设置工具 ⭐
- `env.example` / `config.py.example` - 配置模板文件 ⭐
- `.gitignore` - 忽略敏感配置文件 ⭐
- `SECURITY.md` - 安全配置指南 ⭐
- `requirements.txt` - Python依赖包列表

## 📄 许可证

本项目采用MIT许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持DeepL API翻译
- 生成Swift和Objective-C代码
- 完整的错误处理和日志记录
