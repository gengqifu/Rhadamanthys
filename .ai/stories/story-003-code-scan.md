# Epic-2 - Story-003
代码级合规扫描

**As a** iOS 审核自检用户  
**I want** 扫描 Swift/ObjC 代码中的合规风险  
**so that** 及时发现支付/登录/隐私/网络/私有 API 等问题

## Status
Draft

## Context
- PRD/架构：ATT/跟踪 SDK/IDFA、StoreKit/IAP、外链/第三方支付、第三方登录缺苹果登录、私有 API/反射、明文 HTTP、后台模式实现缺失。
- 需支持目录/大小过滤，输出中文证据与建议。

## Estimation
Story Points: 5

## Tasks
1. 测试任务
   1.1 - [x] 设计测试夹具：Swift/ObjC 样例覆盖 ATT 缺失+跟踪 SDK、外链/第三方支付、缺苹果登录、私有 API 反射、明文 HTTP、后台模式缺失
   1.2 - [x] 编写测试断言：命中规则ID、风险级、高置信/需复核、中文建议、证据行号
2. 开发任务
   2.1 - [ ] 集成 libclang/SourceKitten 输出解析，遍历 Swift/ObjC（支持过滤）
   2.2 - [ ] 实现检测：ATT/广告 SDK/IDFA、支付、登录、私有 API/反射、HTTP、后台模式
   2.3 - [ ] 应用过滤（目录/大小）、返回 Findings（证据/中文建议/风险/需复核）
3. 验证
   3.1 - [ ] 运行测试，全部通过后标记完成

## Constraints
- Python 2.7.18；离线；性能需可控。

## Data Models / Schema
- Finding 同上；可按 group 标注（PAY/PRIV/AUTH/NET/API）。

## Structure
- 扫描器模块示例：`scanner/scanners/code.py`。

## Diagrams
- N/A

## Dev Notes
- 对 SourceKitten 兼容性保留退化方案（libclang + 正则）。

## Chat Command Log
- N/A
