# Epic-1 - Story-007
离线安装与依赖管理

**As a** 使用者/运维  
**I want** 在离线环境完成依赖安装与预检  
**so that** 工具可可靠运行并便于部署

## Status
Draft

## Context
- PRD：Python 2.7.18、Homebrew llvm/libclang、锁定 pandas/openpyxl 等版本；需提供离线安装指引与预检。
- 预检失败需有中文错误与退出码。

## Estimation
Story Points: 2

## Tasks
1. 测试任务
   1.1 - [x] 设计测试：预检缺少 Python/依赖/libclang/路径错误的场景与期望退出码/提示
       - Python 版本不符（非 2.7.18）：返回 exit_code=2，错误提示包含 “Python 版本不支持”。
       - 缺少依赖包（如 pandas/openpyxl）：返回 exit_code=2，提示缺失包名并给出离线安装指引关键字。
       - 找不到 libclang/llvm（环境变量或默认路径缺失）：返回 exit_code=2，提示配置 `LIBCLANG_PATH` 或 Homebrew 路径。
       - 项目路径不存在：返回 exit_code=1，提示 “项目路径不存在”。
       - 路径存在但不可读/无权限：返回 exit_code=1，提示 “无法读取路径/权限不足”。
   1.2 - [ ] 编写测试断言：预检失败的错误文案与退出码符合规范
2. 开发任务
   2.1 - [ ] 提供 Homebrew 安装 llvm/libclang 步骤与 libclang 路径配置（含离线说明）
   2.2 - [ ] 提供离线 Python 包安装方案（wheel/requirements），锁定版本
   2.3 - [ ] 安装指引/FAQ 文档与示例验证步骤，确保预检通过
3. 验证
   3.1 - [ ] 运行预检测试并通过

## Constraints
- 完全离线可执行；依赖版本需固定。

## Data Models / Schema
- 预检结果结构与 Story-004 复用。

## Structure
- 文档位于 README/安装指南；预检在 `scanner/preflight.py`。

## Diagrams
- N/A

## Dev Notes
- 需说明常见问题（找不到 libclang、pip 源不可用等）。

## Chat Command Log
- N/A
