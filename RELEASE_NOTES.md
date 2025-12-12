# Release Notes

## 版本：0.1.0（内部草稿）
- 范围：离线 CLI 扫描 iOS 客户端（Swift/ObjC）代码与配置，输出中文合规报告（Excel 主、可选 JSON/CSV）。
- 功能亮点：
  - 规则扫描：Plist/Entitlements（权限文案、ATS/HTTP、后台模式、URL Schemes、导出合规）、代码（跟踪 SDK/IDFA、第三方支付/登录、私有 API、明文 HTTP、后台模式实现）、元数据与资源（HTTP/支付域、敏感/夸大描述、占位符截图），需复核项标记 `needs_review`。
  - 报告生成：Excel/JSON/CSV，风险降序+规则 ID 升序，高/中/低配色，覆盖统计 Sheet，证据含路径/行/片段与中文建议。
  - CLI 与预检：项目路径、输出格式、include/exclude、日志频率；预检 Python/依赖/libclang/路径，中文错误与退出码。
  - 离线支持：提供 pandas/openpyxl 等 wheel 下载方案；Homebrew llvm/libclang 离线安装思路与 `LIBCLANG_PATH` 配置。
- 已知限制/待办：
  - 依赖扫描（Podfile/SwiftPM）与截图 OCR 未实现。
  - 规则库为示例版，需补充官方条款映射与版本同步。
  - 预检部分测试仍跳过未实现的细节（如精确权限检测）。
- 兼容性：Python 2.7.18；macOS；需 openpyxl（2.6.4）生成 Excel；pandas 0.24.x。
