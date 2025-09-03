# 🔐 Security Guidelines

**🌍 Language: [English](SECURITY.md) | [中文](SECURITY_cn.md)**

## Configuration Management Best Practices

This project provides various elegant methods to manage sensitive information (such as API keys) to ensure open source security.

### 🎯 Configuration Priority

Configuration loading priority (from high to low):

1. **Command line arguments** - Highest priority
2. **Environment variables** - System-level configuration
3. **`.env` file** - Project-level configuration
4. **`config.py` file** - Python configuration file
5. **Default values** - Lowest priority

### 🛠️ Configuration Methods

#### Method 1: Environment Variables (Recommended)

```bash
# Set environment variables
export DEEPL_API_KEY="your-actual-api-key"
export LLM_API_URL="http://127.0.0.1:11434/api/generate"
export LLM_MODEL="mistral:latest"

# Run program
python ios_translator.py /path/to/project
```

#### Method 2: .env File

```bash
# 1. Copy template file
cp env.example .env

# 2. Edit .env file
vim .env

# 3. Add actual API keys
DEEPL_API_KEY=your-actual-api-key
LLM_API_URL=http://127.0.0.1:11434/api/generate
LLM_MODEL=mistral:latest
```

#### Method 3: config.py File

```bash
# 1. Copy template file
cp config.py.example config.py

# 2. Edit config.py file
vim config.py

# 3. Add actual API keys
DEEPL_API_KEY = "your-actual-api-key"
```

#### Method 4: Command Line Arguments

```bash
# Temporary use (not recommended in scripts)
python ios_translator.py /path/to/project --auth-key "your-actual-api-key"
```

### 🚨 Security Considerations

#### ✅ Secure Practices

1. **Use configuration files** - `.env` or `config.py`
2. **Add to .gitignore** - Prevent accidental commits
3. **Use environment variables** - In production environments
4. **Regular key rotation** - Improve security
5. **Principle of least privilege** - Only necessary permissions

#### ❌ Practices to Avoid

1. **Hardcoded keys** - Don't write in code
2. **Commit sensitive info** - Check git history
3. **Share keys publicly** - Don't send in chats, emails
4. **Use same keys** - Different keys for different projects

### 📂 File Description

```
Project root/
├── .env.example          # Environment variable template (safe, can commit)
├── .env                  # Actual configuration (sensitive, don't commit)
├── config.py.example     # Python configuration template (safe, can commit)
├── config.py             # Actual configuration (sensitive, don't commit)
├── .gitignore            # Ignore sensitive files
└── config_manager.py     # Configuration manager (safe, can commit)
```

### 🔧 Configuration Management Tools

#### Auto-setup Configuration

```bash
# Run configuration setup tool
python setup_config.py
```

#### Check Configuration Status

```bash
# Display current configuration status (hide sensitive info)
python ios_translator.py --show-config
```

### 🌍 Environment Variables List

| Variable | Description | Example |
|----------|-------------|---------|
| `DEEPL_API_KEY` | DeepL API Key | `your-actual-api-key` |
| `LLM_API_URL` | LLM API Endpoint | `http://127.0.0.1:11434/api/generate` |
| `LLM_MODEL` | LLM Model Name | `mistral:latest` |
| `DEFAULT_TRANSLATOR` | Default Translator | `deepl` / `llm` / `mock` |
| `DEFAULT_OUTPUT_DIR` | Default Output Directory | Project root directory (customizable) |

### 🔍 Security Checklist

Before open sourcing, please confirm:

- [ ] `.env` and `config.py` are added to `.gitignore`
- [ ] No hardcoded API keys in code
- [ ] `.example` template files are provided
- [ ] Configuration methods are explained in README
- [ ] Different configuration method priorities are tested
- [ ] Git history checked for key leaks

### 🆘 Key Leak Emergency Response

If API keys are accidentally committed:

1. **Immediate action**
   - Rotate affected API keys
   - Assess impact scope
   - Prepare patches

2. **Notify users**
   - Issue security announcement
   - Notify through multiple channels
   - Provide solutions

3. **Follow-up processing**
   - Analyze root cause
   - Improve security processes
   - Update documentation

### 📞 Technical Support

For configuration issues, please:
1. Run `python ios_translator.py --show-config` to check status
2. Check GitHub Issues
3. Refer to QUICKSTART.md documentation