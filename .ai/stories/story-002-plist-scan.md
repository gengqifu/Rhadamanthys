# Epic-2 - Story-002
Info.plist 与 Entitlements 扫描

**As a** iOS 审核自检用户  
**I want** 自动检查配置文件中的合规项  
**so that** 能提前发现权限文案/ATS/后台模式等风险

## Status
Draft

## Context
- PRD 要求：权限文案、ATS、后台模式、Sign in with Apple、URL Schemes、导出合规。
- 需输出中文建议与证据，应用规则库风险/置信标记。

## Estimation
Story Points: 3

## Tasks
1. 测试任务
   1.1 - [x] 设计测试夹具：多语言/缺失权限文案、ATS 全关/例外过多、异常后台模式、缺 Sign in with Apple/URL Schemes
   1.2 - [x] 编写测试断言：规则命中、风险级与中文建议、需复核标记
2. 开发任务
   2.1 - [x] 解析 Info.plist/Entitlements（含多语言），实现检测逻辑
   2.2 - [x] 产出 Findings（文件/行/片段、中文理由与建议、风险级、需人工复核标记）
3. 验证
   3.1 - [x] 运行测试，全部通过后标记完成

## Constraints
- 离线运行；支持目录/大小过滤。

## Data Models / Schema
- Finding：rule_id、severity、file、line、evidence、reason、suggestion、needs_review。

## Structure
- 扫描器模块示例：`scanner/scanners/plist.py`。

## Diagrams
- N/A

## Dev Notes
- ATS/HTTP 检查需考虑例外域名列表。

## Chat Command Log
- N/A
