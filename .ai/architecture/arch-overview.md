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
- 规则同步：独立命令 `update-rules/sync-rules` 从官方文档生成/更新本地规则库；扫描前仅做版本比对与提示。
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

## 7) 依赖与兼容矩阵
- Python 2.7.18；pandas 0.24.2、openpyxl 2.6.4（已验证 Py2）；PyYAML 5.4.x；需本地 wheel 离线安装包。
- libclang 14（Homebrew llvm@14）主解析链；支持 ObjC/C/基础 Swift 符号；若 Swift 语法不兼容则回落 SourceKitten 0.34.x（输出 JSON 由正则/符号匹配）。
- 操作系统：macOS 12+；Xcode/Command Line Tools 提供 SDK；要求 brew 安装路径可探测。
- 语法覆盖：Swift 5.7-/ObjC（ARC/MRC）；遇宏/模板/生成代码复杂度高时降级正则检测并标记 `needs_review`。
- 兼容检查：预检阶段验证 Python 版本、pandas/openpyxl/libclang 可用性与版本范围，不满足则退出码 2。

## 8) 规则库设计与安全
- Schema（YAML/JSON）：`id`、`group`、`title`、`guideline_links[]`、`severity{high/medium/low}`、`confidence{high/manual}`、`needs_review_default`、`evidence_hint`、`suggestion_template`、`version`、`changelog`、`tests`（示例路径与期望）。
- 版本策略：语义化版本（MAJOR.MINOR.PATCH），`changelog` 记录条款更新或检测逻辑变更，扫描结果写入规则版本号。
- 同步安全：`sync-rules` 下载后校验 SHA256/签名，失败不覆盖现有规则；保留上一个版本备份与回滚提示。
- 规则测试：内置示例工程+规则单元测试（针对 evidence/需要人工复核）；`--validate-rules` 命令校验 Schema 与示例输出。

## 9) 性能、并发与降级
- 并发模型：默认进程池（上限 min(4, CPU 核心)）；CLI `--workers` 可调，过大时提示内存风险。
- 文件过滤：忽略 build/DerivedData/Pods/.git/node_modules；大文件阈值默认 5MB，可配置；二进制/图片后缀跳过。
- 时间/内存：记录单文件耗时，超过 3s 标记并降级正则；可选全局超时提示用户分模块扫描。
- 日志节流：默认 1s；可降到 200ms，低于该值提示 I/O 风险；阶段汇总包含扫描文件数/跳过原因/耗时分位。
- 误报与降级策略：私有 API/反射检测优先符号+黑名单组合，解析失败回落正则并标记 `needs_review`；SourceKitten 失败时退回 libclang/正则。

## 10) 报告与可追溯性
- 报告元信息：项目路径、扫描时间、规则版本、工具版本、Git commit（可选）、耗时、扫描文件数。
- 覆盖统计：按规则分组统计命中/未命中/跳过；覆盖率=被扫描文件数/符合过滤条件文件总数。
- 输出路径：默认 `reports/{project_name}-{timestamp}/`，包含 `report.xlsx`、可选 `report.json/csv`、`scan.log`、`rules-version.txt`。
- 错误码：0 成功、1 扫描发现高/中风险、2 预检失败、3 执行异常（含依赖缺失/解析错误）；日志中文且含阶段标签。

## 11) Risks & Mitigations
- Python 2.7 依赖受限：提前选定兼容版本；必要时降级特性。
- 日志高频（30ms）I/O 压力：默认 1s，可配置，提醒风险。
- SourceKitten 兼容性不稳：以 libclang 为主，保留正则/符号降级方案。
- 大型工程性能：过滤目录/文件大小；可配置并发。

## 12) Next Steps
- 确定依赖版本矩阵（pandas/openpyxl/libclang）并写预检。
- 落地规则 Schema 与示例规则；实现规则加载校验。
- 先实现 CLI+预检+Plist 扫描与报告骨架，再迭代代码/依赖扫描。

## Change Log
| Change | Story ID | Description |
| ------ | -------- | ----------- |
| 审阅补充 | N/A | 补齐依赖矩阵、规则库安全/测试、性能与降级策略、报告可追溯性；新增 Change Log |
