# 示例用例与报告生成

本目录通过固定的示例 Findings 生成多种格式报告，帮助新用户在不依赖 libclang/真实项目的情况下，快速熟悉报告结构与配色。

## 适用场景
- 想了解主 CLI 扫描后报告长什么样（字段、排序、配色、覆盖统计）。
- 本地未安装 libclang 或没有待测 iOS 项目时，先验证报告生成链路。

## 环境准备
- Python 3.8+；无需 libclang。  
- 可选：`openpyxl` 用于生成 Excel 报告（未安装则跳过 Excel，JSON/CSV 仍可用）。安装示例：
  ```bash
  python3 -m pip install openpyxl==3.1.2
  ```

## 快速运行
在仓库根目录执行（默认输出到 `examples/output`，同名文件会覆盖）：
```bash
python3 examples/generate_sample_reports.py --outdir examples/output
```
退出码 0 表示生成成功；非 0 请按终端提示检查依赖或路径。

## 输出文件与示例
- `sample_report.json`：字段/排序校验。  
- `sample_report.csv`：与 JSON 同字段。  
- `sample_report.xlsx`：字段+配色（高红/中黄/低绿）+覆盖统计（需 openpyxl）。  

JSON 片段示例：
```json
{
  "rule_id": "PRIV-001",
  "group": "PRIV",
  "severity": "high",
  "file": "Info.plist",
  "evidence": "缺少权限文案 NSCameraUsageDescription",
  "reason": "权限文案缺失",
  "suggestion": "在 Info.plist 中添加 NSCameraUsageDescription 并填入用途说明。",
  "needs_review": false
}
```

## 工作原理与与主 CLI 的关系
- `sample_findings.json`：内置 7 条覆盖常见 App Store 审核风险（权限文案缺失、ATS 关闭、第三方支付、缺少苹果登录、私有 API、明文 HTTP、后台模式）。
- `generate_sample_reports.py`：直接调用 `scanner/report/generator.py` 生成 Excel/JSON/CSV，流程与主 CLI 的报告生成一致，只是跳过了扫描步骤。
- 适合作为主 CLI 输出的对照样例，也可用于检查自定义规则/样本时的格式。
