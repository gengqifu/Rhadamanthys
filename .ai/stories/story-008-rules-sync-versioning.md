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
1. 需求与接口
   1.1 - [ ] 定义规则来源接口（官方条款 URL/版本号/发布日期），支持离线缓存/回退。
   1.2 - [ ] 设计规则元数据与版本文件结构（如 `rules/version.json`），包含当前版本/发布日期/变更摘要。
2. 开发与实现
   2.1 - [ ] 实现 `update-rules` 命令：下载/解析官方规则，生成/更新本地规则库与版本文件，输出中文日志。
   2.2 - [ ] 启动时版本比对：若远端新版本则提示更新，可选择继续/退出（默认提示，不阻塞扫描）。
   2.3 - [ ] 异常与回退：网络失败/解析失败时保持现有规则，提供缓存回退与错误退出码（3）。
3. 测试与验证
   3.1 - [ ] 编写测试：有更新/无更新/下载失败/解析失败场景，断言日志与退出码；验证版本文件写入与缓存回退。
   3.2 - [ ] 示例/脚本：给出离线缓存规则包的使用说明（在 README/安装指南中引用）。

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
