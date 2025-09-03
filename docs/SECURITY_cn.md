# 🔐 安全配置指南

**🌍 Language: [English](SECURITY.md) | [中文](SECURITY_cn.md)**

## 配置管理最佳实践

本项目提供多种优雅的方式来管理敏感信息（如API密钥），确保开源安全。

### 🎯 配置优先级

配置加载优先级（从高到低）：

1. **命令行参数** - 最高优先级
2. **环境变量** - 系统级配置
3. **`.env` 文件** - 项目级配置
4. **`config.py` 文件** - Python配置文件
5. **默认值** - 最低优先级

### 🛠️ 配置方法

#### 方法1：环境变量（推荐）

```bash
# 设置环境变量
export DEEPL_API_KEY="your-actual-api-key"
export LLM_API_URL="http://127.0.0.1:11434/api/generate"
export LLM_MODEL="mistral:latest"

# 运行程序
python ios_translator.py /path/to/project
```

#### 方法2：.env 文件

```bash
# 1. 复制模板文件
cp env.example .env

# 2. 编辑 .env 文件
vim .env

# 3. 添加实际的API密钥
DEEPL_API_KEY=your-actual-api-key
LLM_API_URL=http://127.0.0.1:11434/api/generate
LLM_MODEL=mistral:latest
```

#### 方法3：config.py 文件

```bash
# 1. 复制模板文件
cp config.py.example config.py

# 2. 编辑 config.py 文件
vim config.py

# 3. 添加实际的API密钥
DEEPL_API_KEY = "your-actual-api-key"
```

#### 方法4：命令行参数

```bash
# 临时使用（不推荐在脚本中）
python ios_translator.py /path/to/project --auth-key "your-actual-api-key"
```

### 🚨 安全注意事项

#### ✅ 安全做法

1. **使用配置文件** - `.env` 或 `config.py`
2. **添加到 .gitignore** - 防止意外提交
3. **使用环境变量** - 在生产环境
4. **定期轮换密钥** - 提高安全性
5. **最小权限原则** - 只给必要的权限

#### ❌ 避免的做法

1. **硬编码密钥** - 不要写在代码中
2. **提交敏感信息** - 检查 git 历史
3. **公开分享密钥** - 不要在聊天、邮件中发送
4. **使用相同密钥** - 不同项目用不同密钥

### 📂 文件说明

```
项目根目录/
├── .env.example          # 环境变量模板（安全，可提交）
├── .env                  # 实际配置（敏感，不提交）
├── config.py.example     # Python配置模板（安全，可提交）
├── config.py             # 实际配置（敏感，不提交）
├── .gitignore            # 忽略敏感文件
└── config_manager.py     # 配置管理器（安全，可提交）
```

### 🔧 配置管理工具

#### 自动设置配置

```bash
# 运行配置设置工具
python setup_config.py
```

#### 检查配置状态

```bash
# 显示当前配置状态（隐藏敏感信息）
python ios_translator.py --show-config
```

### 🌍 环境变量列表

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DEEPL_API_KEY` | DeepL API 密钥 | `your-actual-api-key` |
| `LLM_API_URL` | LLM API 端点 | `http://127.0.0.1:11434/api/generate` |
| `LLM_MODEL` | LLM 模型名称 | `mistral:latest` |
| `DEFAULT_TRANSLATOR` | 默认翻译器 | `deepl` / `llm` / `mock` |
| `DEFAULT_OUTPUT_DIR` | 默认输出目录 | 项目根目录（可自定义） |

### 🔍 安全检查清单

开源前请确认：

- [ ] `.env` 和 `config.py` 已添加到 `.gitignore`
- [ ] 代码中没有硬编码的API密钥
- [ ] 提供了 `.example` 模板文件
- [ ] README 中说明了配置方法
- [ ] 测试了不同配置方式的优先级
- [ ] 检查了 git 历史中没有密钥泄露

### 🆘 密钥泄露应急处理

如果不小心提交了API密钥：

1. **立即轮换密钥** - 在API提供商处生成新密钥
2. **清理 Git 历史** - 使用 `git filter-branch` 或 `BFG Repo-Cleaner`
3. **通知团队** - 告知其他开发者更新密钥
4. **检查使用情况** - 查看是否有异常API调用

### 📞 技术支持

如有配置问题，请：
1. 运行 `python ios_translator.py --show-config` 检查状态
2. 查看 GitHub Issues
3. 参考 QUICKSTART.md 文档
