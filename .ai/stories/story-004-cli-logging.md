# Epic-3 - Story-004
CLI、预检与日志

**As a** CLI 使用者  
**I want** 清晰的参数、预检与可配置日志  
**so that** 工具可在离线环境可靠运行并易于诊断

## Status
Complete

## Context
- PRD：CLI 参数（路径、规则分组、out、format、log-interval-ms、verbose、debug、include/exclude），预检 Python/依赖/libclang/路径，退出码 0/1/2/3，日志中文且可配置频率。

## Estimation
Story Points: 3

## Tasks
1. 测试任务
   - [x] 设计测试：参数解析（log-interval-ms/format/include/exclude）、预检失败场景（版本/依赖/libclang/路径）
   - [x] 编写测试断言：退出码 0/1/2/3、中文错误输出、日志频率配置
2. 开发任务
   - [x] 实现 CLI 参数解析与预检（Python 2.7.18、依赖、libclang、路径）
   - [x] 日志封装：默认 1s，可调至 30ms（提示 I/O 开销）；模块阶段汇总
3. 验证
   - [x] 运行测试，全部通过后标记完成

## Constraints
- 离线运行；macOS 环境。

## Data Models / Schema
- 预检结果结构：`ok`、`errors`、`exit_code`。

## Structure
- `scanner/cli.py`；`scanner/logging_utils.py`；`scanner/preflight.py`。

## Diagrams
- N/A

## Dev Notes
- log-interval-ms 需有最小值保护；verbose/debug 控制输出粒度。

## Chat Command Log
- N/A
