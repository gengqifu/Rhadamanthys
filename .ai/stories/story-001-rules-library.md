# Epic-1 - Story-001
规则库与版本管理

**As a** PM/规则维护者  
**I want** 将审核条款拆解为可机读规则并版本化管理  
**so that** 扫描器可稳定加载并输出高置信/人工复核标记

## Status
Complete

## Context
- 基于 PRD/架构：需要可扩展的规则库，包含分组、条款链接、风险级、高置信/人工复核标记、版本/变更记录。
- 需提供示例规则，支持 YAML/JSON 加载校验，并记录官方规则链接/版本元数据。

## Estimation
Story Points: 3

## Tasks
1. 测试任务
   1.1 - [x] 设计测试用例：字段缺失/非法值、ID 分组/条款链接校验、版本/变更记录校验
   1.2 - [x] 编写测试断言，涵盖加载成功/失败场景
   1.3 - [x] 设计测试：官方规则版本映射、更新检测与本地规则库同步流程（含无网络/已是最新的场景）
2. 开发任务
   2.1 - [x] 定义规则 Schema（ID、group、title、source_link、section、severity、confidence、suggestion_template、version、changelog）
   2.2 - [x] 实现规则加载与字段校验（YAML/JSON）
   2.3 - [x] 提供示例规则集
   2.4 - [x] 实现官方规则版本检查与本地规则库更新机制（含版本对应关系存储）
3. 验证
   3.1 - [x] 运行新增测试，确认更新流程通过后标记完成

## Constraints
- 保持离线可用；规则库需可扩展与版本化。

## Data Models / Schema
- Rule JSON/YAML Schema，如上字段定义。

## Structure
- `scanner/rules/` 存储规则；加载器在 `scanner/rules_loader.py`（示例命名）。

## Diagrams
- N/A

## Dev Notes
- 高置信/人工复核标记要透传到报告。

## Chat Command Log
- N/A
