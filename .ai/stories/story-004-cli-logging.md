# Epic-3 - Story-004
CLI、预检与日志

**As a** CLI 使用者  
**I want** 清晰的参数、预检与可配置日志  
**so that** 工具可在离线环境可靠运行并易于诊断

## Status
Draft

## Context
- PRD：CLI 参数（路径、规则分组、out、format、log-interval-ms、verbose、debug、include/exclude），预检 Python/依赖/libclang/路径，退出码 0/1/2/3，日志中文且可配置频率。

## Estimation
Story Points: 3

## Tasks
1. 测试任务
   1.1 - [x] 设计测试：参数解析（log-interval-ms/format/include/exclude）、预检失败场景（版本/依赖/libclang/路径）
   1.2 - [x] 编写测试断言：退出码 0/1/2/3、中文错误输出、日志频率配置
   1.3 - [x] 设计测试：启动时规则库更新流程的提示（开始/进度/完成），含有更新/无更新/失败场景
   1.4 - [ ] 设计测试：独立命令 `update-rules`/`sync-rules` 的执行与日志输出（成功/失败/已最新）
2. 开发任务
   2.1 - [ ] 实现 CLI 参数解析与预检（Python 2.7.18、依赖、libclang、路径）
   2.2 - [ ] 日志封装：默认 1s，可调至 30ms（提示 I/O 开销）；模块阶段汇总
   2.3 - [ ] 集成规则库更新检测与提示（开始/进度/完成），必要时先更新再扫描
   2.4 - [ ] 提供独立命令 `update-rules`/`sync-rules`，可离线跳过或使用缓存
3. 验证
   3.1 - [ ] 运行新增测试，确认更新/同步流程通过后标记完成

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
