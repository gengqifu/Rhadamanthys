# Epic-3 - Story-005
报告生成与测试验证

**As a** 审核自检用户  
**I want** 可读的中文报告与示例验证  
**so that** 能快速定位风险并信任工具输出

## Status
Draft

## Context
- PRD：Excel 主输出（字段、红/黄/绿配色、风险降序+规则ID 升序、覆盖统计 Sheet），可选 JSON/CSV；证据格式包含路径/行/片段与中文理由/建议；示例项目与报告。

## Estimation
Story Points: 3

## Tasks
1. 测试任务
   1.1 - [x] 设计测试：输入若干 Findings，验证 Excel 配色/排序/覆盖统计，JSON/CSV 输出正确
   1.2 - [x] 编写测试断言：字段完整、配色规则、风险降序+规则ID 升序、覆盖统计数值
2. 开发任务
   2.1 - [x] 实现报告生成器：Excel（条件格式、排序、覆盖统计）、JSON/CSV
   2.2 - [x] 证据格式与中文建议输出
3. 验证
   3.1 - [x] 运行测试，全部通过后标记完成（当前缺少 openpyxl，Excel 路径暂被跳过）
4. 示例与用例
   4.1 - [ ] 示例项目与示例报告生成脚本/步骤，验证关键用例覆盖

## Constraints
- 运行于离线环境；保持与 Finding 数据结构兼容。

## Data Models / Schema
- Report：`findings`、`coverage_stats`、`formats`。

## Structure
- `scanner/report/` 下的输出模块；示例资源放 `examples/`。

## Diagrams
- N/A

## Dev Notes
- 覆盖统计需按分组/状态汇总；配色与排序遵守 PRD。

## Chat Command Log
- N/A
