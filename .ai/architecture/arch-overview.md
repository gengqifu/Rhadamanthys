# Architecture Overview: iOS App Store 合规扫描器

## 1) Context & Goals
- 离线 CLI 工具，扫描 iOS 客户端（Swift/ObjC）代码与配置，依据 App Store Review Guidelines/HIG 输出中文合规报告（Excel 主、可选 JSON/CSV）。
- 核心目标：规则库可扩展、扫描覆盖关键合规项（隐私/支付/登录/网络/私有 API 等）、报告可读且含高置信与人工复核标记，日志/预检可诊断。

## 2) Scope
- 输入：本地 iOS 工程（源码、Info.plist、Entitlements、Podfile/Package.swift 等）。
- 输出：报告文件（Excel 必选，JSON/CSV 可选），终端日志。
- 运行环境：macOS，Python 2.7.18，离线；依赖 Homebrew clang/libclang。

## 3) High-Level Architecture
- CLI & 预检层：参数解析；检查 Python/依赖/libclang/路径；控制日志频率（默认 1s，可降到 30ms 提示 I/O 开销）；统一退出码。
- 扫描协调器：管理目录/文件过滤（忽略 build/DerivedData/Pods/.git/node_modules、大文件阈值）；调度各扫描器；聚合结果。
- 规则库：YAML/JSON，分组/ID（PRIV/PAY/AUTH/NET/API/META），条款链接、风险级、高置信/人工复核标记、版本/变更记录。
- 扫描器模块：
  - Plist/Entitlements：权限文案、ATS/HTTP、后台模式、Sign in with Apple、URL Schemes、导出合规。
  - 代码：ATT/跟踪 SDK/IDFA、StoreKit/IAP、外链/第三方支付、第三方登录缺苹果登录、私有 API/反射、明文 HTTP、后台模式实现缺失。
  - 依赖：Podfile/Package.swift/SwiftPM，识别广告/支付/登录等 SDK。
- 报告生成：Excel（风险配色红/黄/绿，排序风险降序+规则ID 升序，覆盖统计 Sheet），可选 JSON/CSV；证据含路径/行/片段、中文理由与建议。
- 日志与错误：中文输出；模块级阶段汇总；明确错误码 0/1/2/3。

## 4) Component Responsibilities
- `cli.py`：参数/预检入口，设置日志策略，调用协调器。
- `rules/`：规则加载与校验，提供规则元数据与标记。
- `scanners/`：`plist.py`、`code.py`、`deps.py` 等模块化实现，返回 Findings。
- `coordinator.py`：文件过滤、任务调度、结果聚合。
- `report/`：Excel/JSON/CSV 输出与覆盖统计。
- `logging_utils/`：频率控制、阶段汇总、中文错误输出。

## 5) Data Flow (简图)
CLI → 预检 → 规则加载 → 扫描协调器 → {Plist/Code/Deps 扫描器} → 结果聚合 → 报告生成 → 输出文件/日志

## 6) Technology Stack
- Python 2.7.18；pandas+openpyxl（锁定可用版本）；argparse/logging；yaml/json。
- libclang/llvm（clang.cindex）做 Swift/ObjC 解析；SourceKitten 作为备选（解析输出）。

## 7) Risks & Mitigations
- Python 2.7 依赖受限：提前选定兼容版本；必要时降级特性。
- 日志高频（30ms）I/O 压力：默认 1s，可配置，提醒风险。
- SourceKitten 兼容性不稳：以 libclang 为主，保留正则/符号降级方案。
- 大型工程性能：过滤目录/文件大小；可配置并发。

## 8) Next Steps
- 确定依赖版本矩阵（pandas/openpyxl/libclang）并写预检。
- 落地规则 Schema 与示例规则；实现规则加载校验。
- 先实现 CLI+预检+Plist 扫描与报告骨架，再迭代代码/依赖扫描。
