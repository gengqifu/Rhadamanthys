# 示例项目与报告生成

本目录提供示例 Findings 及报告生成脚本，用于验证关键用例覆盖与报告格式。

## 内容
- `sample_findings.json`：涵盖权限文案缺失、ATS 关闭、第三方支付、第三方登录缺苹果登录、私有 API、明文 HTTP、后台模式等风险。
- `generate_sample_reports.py`：读取示例 Findings，生成 Excel/JSON/CSV 报告（缺少 `openpyxl` 时自动跳过 Excel）。
- `output/`：脚本默认输出目录（运行后生成）。

## 运行
在仓库根目录执行：
```bash
python3 examples/generate_sample_reports.py --outdir examples/output
```

输出文件：
- `sample_report.json`：排序/字段校验
- `sample_report.csv`：排序/字段校验
- `sample_report.xlsx`：字段+配色（高红/中黄/低绿）+覆盖统计（需安装 openpyxl）

若未安装 `openpyxl`，脚本会提示并跳过 Excel 生成，可按需离线安装后重试。
