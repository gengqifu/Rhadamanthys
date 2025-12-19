# Rhadamanthys
一个用来检查新发布 iOS app 是否符合 App Store 上架标准的工具。

- 发布说明：见 `RELEASE_NOTES.md`

## 快速开始
1) 准备环境：Python 3.8+，可用 `python3 -V` 验证；安装 llvm/libclang（macOS 建议 `brew install llvm`，并设置 `export LIBCLANG_PATH=/opt/homebrew/opt/llvm/lib` 或对应前缀）。  
2) 安装依赖（推荐虚拟环境）：
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip setuptools wheel
python3 -m pip install PyYAML==6.0.1 openpyxl==3.1.2
```
3) 运行扫描并生成报告（Excel 默认）：
```
python3 scanner/cli.py <project_path> --out report.xlsx --format excel
```
退出码 0 表示生成成功；非 0 按终端中文错误提示补齐依赖/路径后重试。若想先查看报告格式，可运行 `python3 examples/generate_sample_reports.py --outdir examples/output` 生成示例。

## 使用说明
- 预检+扫描并生成报告（Excel 默认）：`python3 scanner/cli.py <project_path> --out report.xlsx --format excel`
- 更新规则库：`python3 scanner/cli.py --command update-rules <project_path>`
- 示例报告：`python3 examples/generate_sample_reports.py --outdir examples/output`

### 命令参数（scanner/cli.py）
- `project_path`：必填，待扫描项目根目录。
- `--command`：`scan`（默认）或 `update-rules`。
- `--out`：报告输出路径，默认 `report.xlsx`。
- `--format`：报告格式，`excel`（默认）/`json`/`csv`。
- `--include`：仅扫描指定相对路径（可多值，如 `--include src app`）。
- `--exclude`：跳过指定相对路径（可多值，如 `--exclude Pods build`）。
- `--log-interval-ms`：日志间隔提示配置，默认 1000（当前仅提示用途）。
- `--verbose`：输出详细 INFO 级别日志（默认已是 INFO，可用来显式声明）。
- `--debug`：输出 DEBUG 级别日志。

### 报告解读
- 输出格式：Excel/JSON/CSV。Excel 包含两个 Sheet：`Findings`（明细）和 `Coverage`（覆盖统计）。
- 明细字段：`rule_id`、`rule_title`、`section`（对应审核条款章节）、`group`、`severity`（高红/中黄/低绿）、`needs_review`（是否需人工复核）、`file`、`line`、`evidence`（含路径/行/片段）、`reason`、`suggestion`。
- 风险排序：按 `severity` 高→中→低，同行按 `rule_id` 升序。
- 覆盖统计：按 `group` 聚合高/中/低/需复核/总计，底部 `合计` 汇总全局。
- 若规则库可匹配到 `rule_id`，报告会自动补充 `rule_title` 与 `section`；未匹配时 section 可能为 `-`。
- 输出示例（JSON 片段，字段同 Excel）：  
```json
[
  {
    "rule_id": "NET-HTTP",
    "rule_title": "明文 HTTP 调用",
    "section": "2.5.1",
    "severity": "high",
    "needs_review": false,
    "file": "App/Networking/Client.swift",
    "line": 42,
    "evidence": "http://example.com/api",
    "reason": "检测到明文 HTTP 请求",
    "suggestion": "改为 HTTPS 或配置 ATS 例外并说明理由"
  }
]
```

## 技术原理
工具通过 CLI 预检 → 加载规则 → 扫描各模块 → 汇总 Findings → 生成报告：
- 预检：验证 Python/依赖/libclang 及项目路径可用性，失败返回中文错误与退出码。
- 扫描：
  - Plist/Entitlements：检查权限文案、ATS/HTTP 配置、后台模式、URL Schemes、导出合规。
  - 代码：基于标记文本扫描跟踪 SDK/IDFA、第三方支付/登录、私有 API、明文 HTTP、后台模式实现。
  - 元数据/资源：检测 HTTP/支付域链接、敏感/夸大描述、占位符截图。
- 报告：按风险降序+规则 ID 升序输出 Excel/JSON/CSV；Excel 含高/中/低配色与覆盖统计，证据包含路径/行/片段与中文建议。
- 更多架构细节见 `.ai/architecture/ios-appstore-compliance-arch.md`。

## 安装（含离线说明）
- 依赖：Python 3.8+；PyYAML（6.0.1）；openpyxl（3.1.2，用于 Excel 报告）；llvm/libclang。
- 检查是否已安装：
  - Python 版本：`python3 -V`
  - PyYAML/openpyxl：`python3 - <<'PY'\nimport yaml, openpyxl\nprint(yaml.__version__, openpyxl.__version__)\nPY`
  - libclang：检查 `echo $LIBCLANG_PATH`，并确认目录下存在 `libclang.dylib`
- macOS + Homebrew 在线安装：
  1) `brew install python`（或指定版本 `python@3.11` 等）+ `brew install llvm`
  2) 设置 `export LIBCLANG_PATH=/opt/homebrew/opt/llvm/lib`（视 Homebrew 前缀调整）
- Python 包安装（推荐虚拟环境）：
  ```
  python3 -m venv .venv
  source .venv/bin/activate
  python3 -m pip install -U pip setuptools wheel
  python3 -m pip install PyYAML==6.0.1 openpyxl==3.1.2
  ```
- 离线安装 PyYAML/openpyxl：在有网机器下载 wheel
  - `python3 -m pip download -d pkgs PyYAML==6.0.1 openpyxl==3.1.2`
  - 拷贝 `pkgs/` 到离线机后执行 `python3 -m pip install --no-index --find-links pkgs PyYAML==6.0.1 openpyxl==3.1.2`
- 离线安装 llvm/libclang（思路）：在有网机器上执行 `brew fetch llvm`，将缓存的 bottle 与 `Cellar/llvm` 拷贝到离线机相同前缀，再运行 `brew install --cache llvm` 或直接解压到 `/usr/local/opt/llvm`。确保 `libclang.dylib` 可由 `LIBCLANG_PATH` 指向。
- 运行前可执行预检（实现于 `scanner/cli.py` 的 `preflight`）：缺失依赖或路径错误时输出中文错误与退出码。

## 平台支持
- 已验证：macOS（Apple Silicon/Intel，需安装 llvm/libclang）。
- Linux：理论可行，需手动安装 llvm/libclang 并设置 `LIBCLANG_PATH`；未做充分验证。
- Windows：未验证，建议在 WSL 或 CI Linux/macOS 环境运行。

## 规则库与更新
- 本地规则位于 `scanner/rules/`，版本文件 `scanner/rules/version.json`；启动扫描时会尝试比对/提示版本。
- 运行 `python3 scanner/cli.py --command update-rules <project_path>` 可同步规则；失败会回退到本地规则并提示错误。
- 离线更新思路：将外部获取的规则 YAML 与 `version.json` 覆盖到 `scanner/rules/`，再运行扫描；保持 `version` 字段可用于版本提示。

## FAQ（离线/安装常见问题）
- 找不到 `libclang.dylib`：确认 Homebrew 路径（如 `/opt/homebrew/opt/llvm/lib`），或设置 `LIBCLANG_PATH` 指向实际的 `libclang.dylib` 目录。
- pip 源不可用：使用 `pip download -d <目录> ...` 在联网机器准备 wheel，离线机用 `--no-index --find-links` 安装。
  - 预检失败：运行 `python3 scanner/cli.py <project_path>`，根据中文错误提示补齐 Python/依赖/libclang/路径，再重试。
