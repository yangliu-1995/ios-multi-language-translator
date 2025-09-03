# 📚 使用示例

**🌍 Language: [English](USAGE_EXAMPLES.md) | [中文](USAGE_EXAMPLES_cn.md)**

## 基本使用

### 1. 使用您的DeepL API密钥

```python
from translator import create_translator

# 使用您提供的API密钥
auth_key = "your-actual-deepl-api-key"
translator = create_translator('deepl', auth_key=auth_key)

# 单个翻译
result = translator.translate("Hello, world!", "zh")
print(result)  # 输出中文翻译

# 批量翻译
texts = {
    "greeting": "Hello",
    "welcome": "Welcome to our app",
    "save": "Save",
    "cancel": "Cancel"
}
results = translator.translate_batch(texts, "ja")
for key, translation in results.items():
    print(f"{key}: {translation}")
```

### 2. 完整的项目翻译

```bash
# 翻译整个iOS项目
python ios_translator.py /path/to/your/ios/project

# 使用自定义API密钥
python ios_translator.py /path/to/project --auth-key "your-api-key"

# 生成Swift代码和Objective-C头文件
python ios_translator.py /path/to/project --generate-objc

# 指定输出目录
python ios_translator.py /path/to/project --output-dir ./generated
```

### 3. 运行演示

```bash
# 运行基本示例
python example.py

# 运行DeepL演示
python demo_deepl.py

# 运行功能测试
python test_functionality.py
```

## 生成的Swift代码使用

### UIKit中使用

```swift
import UIKit

class ViewController: UIViewController {
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var saveButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // 使用生成的本地化字符串
        titleLabel.text = .appTitle
        saveButton.setTitle(.saveButton, for: .normal)
        
        // 显示警告
        showAlert(title: .alertTitleWarning, message: .msgError)
    }
    
    func showAlert(title: String, message: String) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: .btnConfirm, style: .default))
        present(alert, animated: true)
    }
}
```

### SwiftUI中使用

```swift
import SwiftUI

struct ContentView: View {
    @State private var showAlert = false
    
    var body: some View {
        VStack(spacing: 20) {
            Text(.welcomeMessage)
                .font(.title)
            
            Button(.saveButton) {
                saveData()
            }
            .buttonStyle(.borderedProminent)
            
            Button(.cancelButton) {
                showAlert = true
            }
            .buttonStyle(.bordered)
        }
        .alert(.alertTitleWarning, isPresented: $showAlert) {
            Button(.btnConfirm) { }
            Button(.btnCancel) { }
        } message: {
            Text(.alertMsgDeleteConfirm)
        }
    }
    
    func saveData() {
        // 保存逻辑
    }
}
```

## 项目结构示例

```
YourProject/
├── en.lproj/
│   └── Localizable.strings           # 英文基础文件
├── zh-Hans.lproj/
│   └── Localizable.strings           # 中文简体（自动生成/更新）
├── ja.lproj/
│   └── Localizable.strings           # 日语（自动生成/更新）
├── LocalizedStrings.swift            # 生成的Swift扩展
├── LocalizedStrings.h                # 生成的ObjC头文件（可选）
└── ... 其他项目文件
```

## Localizable.strings 文件示例

### 英文版本 (en.lproj/Localizable.strings)
```objc
/* App Information */
"app_title" = "My Awesome App";
"app_version" = "Version 1.0";

/* Navigation */
"nav_home" = "Home";
"nav_settings" = "Settings";
"nav_profile" = "Profile";

/* Buttons */
"btn_save" = "Save";
"btn_cancel" = "Cancel";
"btn_delete" = "Delete";
"btn_confirm" = "Confirm";

/* Messages */
"msg_welcome" = "Welcome to our app!";
"msg_success" = "Operation completed successfully";
"msg_error" = "An error occurred. Please try again.";
"msg_loading" = "Loading...";

/* Alerts */
"alert_title_warning" = "Warning";
"alert_title_error" = "Error";
"alert_msg_delete_confirm" = "Are you sure you want to delete this item?";
```

### 中文版本 (zh-Hans.lproj/Localizable.strings) - 自动生成
```objc
/* App Information */
"app_title" = "我的应用程序";
"app_version" = "版本 1.0";

/* Navigation */
"nav_home" = "首页";
"nav_settings" = "设置";
"nav_profile" = "个人资料";

/* Buttons */
"btn_save" = "保存";
"btn_cancel" = "取消";
"btn_delete" = "删除";
"btn_confirm" = "确认";

/* Messages */
"msg_welcome" = "欢迎使用我们的应用程序！";
"msg_success" = "操作成功完成";
"msg_error" = "发生错误，请重试。";
"msg_loading" = "加载中...";

/* Alerts */
"alert_title_warning" = "警告";
"alert_title_error" = "错误";
"alert_msg_delete_confirm" = "您确定要删除此项目吗？";
```

## 最佳实践

1. **键名规范**: 使用下划线分隔的小写字母，如 `button_save_title`
2. **分组注释**: 使用注释对相关字符串进行分组
3. **语义化命名**: 键名应该描述用途而不是内容
4. **定期更新**: 在添加新字符串后运行翻译脚本
5. **人工审核**: 机器翻译后建议进行人工审核
6. **版本控制**: 将生成的代码加入版本控制系统
