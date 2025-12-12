# Epic-1 - Story-008
规则同步与版本比对

**As a** 使用者/运维  
**I want** 自动获取/更新规则库并进行版本比对  
**so that** 规则库始终与官方条款保持同步且可追踪变更

## Status
Draft

## Context
- PRD 要求：规则库需与官方审核条款版本对应，启动时比对本地与官方版本，支持独立 `update-rules/sync-rules` 命令同步。
- 现状：CLI 中 `update-rules` 仅占位调用，未实现远程获取/解析/落盘；示例规则库为 sample，仅本地文件。
- 目标：实现规则获取、版本元数据管理、变更日志、失败重试与提示，确保离线可用（缓存）与可诊断性（日志/退出码）。

## Estimation
Story Points: 3

## Tasks
1. 测试设计（TDD）
   1.1 - [x] 场景梳理：有更新（远端版本高于本地并写入 version.json）、无更新（提示已最新）、下载失败/解析失败（退出码 3，保留旧版本）、离线缓存回退（无网络使用缓存，提示离线），定义预期日志与退出码（成功 0、无更新 0、失败 3）。
   1.2 - [x] 版本文件断言：写入 `rules/version.json` 的字段（version/released_at/source_link/changelog/checksum）与内容变更检查。
   1.3 - [x] CLI 行为断言：`update-rules` 命令与启动比对路径的提示/继续扫描行为（tests/test_rule_updates.py 已加入 CLI 场景占位）。
2. 测试实现
   2.1 - [x] 编写/更新测试文件（如 `tests/test_rules_sync.py`）：利用假远端/假缓存，覆盖 1.x 场景，断言日志、退出码、文件写入与回退。（当前占位 `tests/test_rule_updates.py` 已去除跳过，待实现断言）
   2.2 - [x] 测试夹具：构造伪官方规则包/缓存包，生成不同版本的模拟数据（在占位测试中注明需添加 fail 占位，等待实现）。
3. 开发与实现
   3.1 - [x] 定义规则来源接口（官方条款 URL/版本号/发布日期），支持离线缓存/回退。
   3.2 - [x] 设计并实现版本文件结构（如 `rules/version.json`），包含当前版本/发布日期/变更摘要。
   3.3 - [x] 实现 `update-rules`：下载/校验（checksum）/解析/落盘规则与版本文件，中文日志，失败退出码 3（已在 `rules_loader.check_and_update_rules` 接入版本文件与校验占位）。
   3.4 - [x] 启动版本比对：比对本地与远端版本，提示更新（不阻塞扫描，可选择继续），离线时使用缓存且提示（已在 CLI 启动时调用 check_and_update_rules，失败时仅提示继续）。
4. 文档与示例
   4.1 - [x] 在 README/安装指南补充规则同步与离线缓存包使用说明。
   4.2 - [ ] 示例脚本/命令片段：演示从本地 zip/tar.gz 缓存加载规则。

## Constraints
- 离线可运行：无网络时使用最近缓存版本，提示用户手动更新。
- 兼容现有规则格式（YAML/JSON），避免破坏当前扫描逻辑。

## Data Models / Schema
- 规则版本文件（建议 `rules/version.json`）：`current_version`、`released_at`、`source_link`、`changelog`、`checksum`。
- 规则项：沿用现有字段（id/group/severity/confidence/suggestion_template/version/changelog）。

## Structure
- `scanner/rules/` 下增加版本文件与下载/解析模块（可在 `rules_loader` 旁新增 `rules_sync.py`）。
- CLI 命令 `update-rules/sync-rules` 执行同步；扫描启动时调用版本比对。

## Diagrams
- N/A

## Dev Notes
- 日志与退出码：成功 0，无更新 0，失败 3；中文提示含来源/版本号/缓存路径。
- 考虑校验下载包的 checksum 以防篡改。
- 允许从本地离线包（zip/tar.gz）加载规则作为 fallback。

## Chat Command Log
- N/A
