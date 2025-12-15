# Rhadamanthys
一个用来检查新发布 iOS app 是否符合 App Store 上架标准的工具。

- 发布说明：见 `RELEASE_NOTES.md`

## 使用说明
- 预检：`python3 scanner/cli.py <project_path>`（默认命令为 scan，会先执行预检；若路径或依赖缺失会输出中文错误与退出码）。
- 扫描并生成报告（Excel 默认）：`python3 scanner/cli.py <project_path> --out report.xlsx --format excel`
  - 可选：`--format json` 或 `--format csv`
  - 可选：`--include src/ app/`、`--exclude Pods/ build/`
  - 日志频率：`--log-interval-ms 1000`，可加 `--verbose`/`--debug`
- 规则库更新：`python3 scanner/cli.py --command update-rules <project_path>`（默认以苹果审核指南页面为来源，内容哈希作为版本；成功/无更新退出码 0，失败 3，失败时保留本地规则并提示。离线包自动更新待实现，可手动替换 `scanner/rules/` 与 `version.json`）
- 示例报告：`python3 examples/generate_sample_reports.py --outdir examples/output`

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

## FAQ（离线/安装常见问题）
- 找不到 `libclang.dylib`：确认 Homebrew 路径（如 `/opt/homebrew/opt/llvm/lib`），或设置 `LIBCLANG_PATH` 指向实际的 `libclang.dylib` 目录。
- pip 源不可用：使用 `pip download -d <目录> ...` 在联网机器准备 wheel，离线机用 `--no-index --find-links` 安装。
  - 预检失败：运行 `python3 scanner/cli.py <project_path>`，根据中文错误提示补齐 Python/依赖/libclang/路径，再重试。
