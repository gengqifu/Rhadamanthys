# App Overall Vision

## 概述
为 iOS 应用上线前提供离线合规自检工具，依据 App Store Review Guidelines 与 HIG 自动扫描本地代码与配置，输出中文报告，降低审核风险。

## 核心目标
- 覆盖可机检的高风险项（隐私、支付、登录、网络、私有 API 等），区分高置信与需人工复核。
- 提供清晰的中文报告与改进建议，支持 Excel 主输出，可选 JSON/CSV。
- 保持规则库可扩展、可版本化，支持离线运行与可诊断的日志/预检。

## 范围
- 输入：iOS 客户端源码与配置（Swift/ObjC、Info.plist、Entitlements、Podfile/Package.swift 等）。
- 输出：风险清单与覆盖统计；终端日志。
- 环境：macOS，Python 2.7.18；离线，无服务端依赖。

## 成功度量
- 关键风险项的检出率（权限文案缺失、ATS 全关、无 ATT+跟踪 SDK、外链/第三方支付、缺少 Apple 登录、私有 API、明文 HTTP）。
- 报告可读性与中文建议满意度。
- 运行稳定性（预检通过率、错误可诊断性）。
