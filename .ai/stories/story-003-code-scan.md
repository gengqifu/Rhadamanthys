# 用户故事：代码级合规扫描
- 状态：Draft
- 故事点：5 SP

## 背景
需要在 Swift/ObjC 代码中检测 ATT/跟踪、支付、登录、私有 API、网络等风险。

## 需求
- 支持 Swift/ObjC 静态扫描（libclang/SourceKitten 可选）。
- 检测 ATT 申请与跟踪/广告 SDK（IDFA 访问）、无 ATT + SDK 情况提示。
- 检测 StoreKit/IAP 与外链支付/WebView 支付/第三方支付 SDK。
- 检测第三方登录存在时缺少苹果登录的风险。
- 检测私有 API/反射黑名单、动态加载私有框架。
- 检测明文 HTTP、ATS 例外域，以及后台模式对应实现缺失。
- 支持目录/文件大小过滤，忽略 build/DerivedData/Pods/.git/node_modules 等。

## 验收标准
- 对示例代码能识别上述风险并输出证据（文件/行/片段）。
- 区分高置信与需人工复核项，输出中文命中理由与建议。
