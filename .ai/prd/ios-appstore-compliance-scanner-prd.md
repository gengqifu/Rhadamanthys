# 1. Title: iOS App Store 合规扫描器 PRD

<version>1.0.0</version>

## Status: Draft

## Intro
一个离线运行的命令行工具，扫描本地 iOS 客户端代码与配置，依据 App Store Review Guidelines 与 HIG 识别潜在违规，生成中文报告（Excel 主输出，可选 JSON/CSV），为上线前合规自检提供自动化支持。

## Goals
- 识别可机检的审核/合规风险，输出高置信命中与需人工复核项。
- 生成结构化中文报告，含风险等级、位置、证据与改进建议。
- 提供可配置的日志与预检机制，保证可运行性与可诊断性。
- 支持规则库扩展与版本化管理。

## Features and Requirements
- 功能：规则库（分组、版本、条款链接、高置信/人工复核标记）、plist/Entitlements 扫描、代码与依赖扫描、报告生成（Excel/可选 JSON/CSV）、CLI 与预检、日志与错误输出。
- 规则更新：规则库需与苹果官方审核规则版本对应；启动时检测官方更新，先同步本地规则库（提示开始/进度/完成）再扫描。
- 非功能：离线运行，Python 2.7.18 兼容，macOS + Homebrew clang/libclang 支持；性能可控（目录/大小过滤），模块化可维护。
- 体验：日志中文，默认 1s 频率，可降至 30ms（提示 I/O 开销）；输出证据包含文件/行/片段与中文理由/建议。
- 集成/合规：规则来源记录官方条款链接与版本日期；风险配色高红/中黄/低绿，排序风险降序+规则ID 升序；覆盖统计 Sheet。

## Epic List
### Epic-1: 规则库与预检
### Epic-2: 扫描器（配置/代码/依赖）
### Epic-3: 报告与日志
### Epic-4: 测试与示例

## Epic 1: Story List
- Story 1: 规则库与版本管理 — Status: Complete
  - 规则 Schema（ID 分组、条款链接、风险级、高置信/人工复核、版本/变更）；YAML/JSON 加载与校验。

## Epic 2: Story List
- Story 2: Info.plist/Entitlements 扫描 — Status: Complete
  - 权限文案、ATS/HTTP、后台模式、Sign in with Apple、URL Schemes、导出合规。
- Story 3: 代码级合规扫描 — Status: Complete
  - ATT/跟踪 SDK/IDFA、StoreKit/IAP、外链/第三方支付、第三方登录缺苹果登录、私有 API/反射、明文 HTTP、后台模式实现缺失；目录与大小过滤。
- Story 4: 依赖扫描 — Status: Planned
  - 解析 Podfile/Package.swift/SwiftPM，识别广告/支付/登录等 SDK。

## Epic 3: Story List
- Story 5: CLI、日志与预检 — Status: Complete
  - CLI 参数解析；预检 Python/依赖/libclang/路径；日志频率可配；退出码约定。
- Story 6: 报告生成 — Status: Complete
  - Excel 主输出（红/黄/绿配色，风险降序+规则ID 升序，覆盖统计 Sheet）；可选 JSON/CSV；证据格式中文化。

## Epic 4: Story List
- Story 7: 测试与示例 — Status: Planned
  - 示例项目与报告；关键用例覆盖（权限文案缺失、ATS 全关、无 ATT+跟踪 SDK、第三方登录缺苹果登录、外链/第三方支付、私有 API、明文 HTTP、后台模式滥用、规则库缺失）。

## Technology Stack
| Technology | Description |
| ---------- | ----------- |
| Python 2.7.18 | 主语言，需锁定 pandas/openpyxl 等兼容版本 |
| libclang/llvm | Swift/ObjC 解析（clang.cindex），macOS 下通过 Homebrew 安装 |
| argparse/logging | CLI 参数与日志 |
| pandas + openpyxl | Excel 报告生成（需选 2.7 兼容版） |
| JSON/YAML 解析 | 规则库存储与加载 |

## Reference
- App Store Review Guidelines（官方链接）
- Human Interface Guidelines（官方链接）
- 规则库需记录条款编号、来源链接、发布日期，并维护与官方版本的对应关系。

## Data Models, API Specs, Schemas, etc...
- Rule：`id`、`group`（PRIV/PAY/AUTH/NET/API/META）、`title`、`source_link`、`section`、`severity`、`confidence`（high/manual）、`suggestion_template`、`version`、`changelog`。
- Finding：`rule_id`、`severity`、`file`、`line`、`evidence`、`reason`、`suggestion`、`needs_review`、`group`。
- Report：`findings`、`coverage_stats`、`formats`（excel/json/csv）。

## Project Structure
```text
.ai/
  prd/                       # PRD
  stories/                   # 用户故事
  architecture/              # 架构文档
scanner/
  rules/                     # 机读规则库（YAML/JSON）
  scanners/                  # 模块化扫描器（plist/code/deps等）
  cli.py                     # CLI 入口
  report/                    # 报告生成器
```

## Change Log
| Change        | Story ID | Description          |
| ------------- | -------- | -------------------- |
| 初稿          | N/A      | 生成 iOS 合规扫描器 PRD |
