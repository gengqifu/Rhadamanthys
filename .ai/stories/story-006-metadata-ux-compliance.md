# Epic-2 - Story-006
元数据与资源合规检查

**As a** 审核自检用户  
**I want** 识别元数据/资源中的潜在违规提示  
**so that** 降低描述/截图/外链导致的审核风险

## Status
Draft

## Context
- PRD 扩展：扫描代码/资源中的 HTTP 链接，提示外链支付/不安全域；可选检测描述/关键词的敏感/夸大表述；可选检测截图占位符。
- 无法高置信的项需标记“需人工复核”。

## Estimation
Story Points: 3

## Tasks
1. 测试任务
   - [ ] 设计测试夹具：含 HTTP 链接、疑似支付域、占位符截图、描述/关键词文本示例
   - [ ] 编写测试断言：命中规则ID、风险级/需复核标记、中文建议、证据路径
2. 开发任务
   - [ ] 实现扫描代码/资源中的 HTTP 链接，识别疑似支付/敏感域并输出证据
   - [ ] 可选元数据文本检测（描述/关键词敏感/夸大），默认标记需复核
   - [ ] 可选截图占位符检测（文件名或简化 OCR）
3. 验证
   - [ ] 将命中纳入报告，遵循配色/排序/复核标记，确保测试通过

## Constraints
- 默认标记低置信项为需人工复核；避免误报。

## Data Models / Schema
- 新增规则 group 可用 META/NET，Finding 保持一致。

## Structure
- 可扩展 `scanner/scanners/resources.py` 或在 code/网络扫描中复用。

## Diagrams
- N/A

## Dev Notes
- 需可配置开启/关闭元数据/截图检测。

## Chat Command Log
- N/A
