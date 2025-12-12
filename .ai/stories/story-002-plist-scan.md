# 用户故事：Info.plist 与 Entitlements 扫描
- 状态：Draft
- 故事点：3 SP

## 背景
需要自动检查 iOS 配置文件中的合规项（权限文案、ATS、后台模式等）。

## 需求
- 解析 Info.plist、Entitlements，支持多语言或缺失键的提示。
- 检查权限文案是否存在且非空；输出中文建议。
- 检查 ATS 配置（是否全关/例外过多）、明文 HTTP 域。
- 检查 UIBackgroundModes 合规性，缺少对应功能时标记风险。
- 检查 Sign in with Apple 配置、URL Schemes、导出合规标记。

## 验收标准
- 对示例项目能识别权限文案缺失/空、ATS 全关、异常后台模式。
- 输出包含规则ID、风险等级、文件/行/证据、中文建议、是否需人工复核。
