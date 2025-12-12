# Rhadamanthys
一个用来检查新发布 iOS app 是否符合 App Store 上架标准的工具。

- 工作流程规范：`rules/core-rules/workflow-agile-manual.mdc`
- 发布说明：见 `RELEASE_NOTES.md`

## 使用说明
- 预检：`python scanner/cli.py <project_path>`（默认命令为 scan，会先执行预检；若路径或依赖缺失会输出中文错误与退出码）。
- 扫描并生成报告（Excel 默认）：`python scanner/cli.py <project_path> --out report.xlsx --format excel`
  - 可选：`--format json` 或 `--format csv`
  - 可选：`--include src/ app/`、`--exclude Pods/ build/`
  - 日志频率：`--log-interval-ms 1000`，可加 `--verbose`/`--debug`
- 规则库更新（占位命令）：`python scanner/cli.py --command update-rules <project_path>`
- 示例报告：`python examples/generate_sample_reports.py --outdir examples/output`

## 技术原理
- 离线 CLI：Python 2.7 运行，无需联网；预检 Python/依赖/libclang/路径。
- 规则扫描：Plist/Entitlements（权限文案、ATS/HTTP、后台模式、URL Schemes、导出合规），代码正则/标记扫描（跟踪 SDK/IDFA、第三方支付/登录、私有 API、明文 HTTP、后台模式实现），元数据/资源（HTTP/支付域、敏感描述、占位符截图）。
- 报告生成：Excel/JSON/CSV，风险降序+规则 ID 升序，高/中/低配色，证据含路径/行/片段与中文建议，覆盖统计。
- 架构参考：详见 `.ai/architecture/ios-appstore-compliance-arch.md`。

## 安装（含离线说明）
- 依赖：Python 2.7.18；pandas/openpyxl（2.6.4 等兼容版本）；llvm/libclang。
- macOS + Homebrew 在线安装：
  1) `brew install llvm`（示例路径 `/usr/local/opt/llvm` 或 `/opt/homebrew/opt/llvm`）
  2) 设置 `export LIBCLANG_PATH=/opt/homebrew/opt/llvm/lib`（视 Homebrew 前缀调整）
- 离线安装 llvm/libclang（思路）：在有网机器上执行 `brew fetch llvm`，将缓存的 bottle 与 `Cellar/llvm` 拷贝到离线机相同前缀，再运行 `brew install --cache llvm` 或直接解压到 `/usr/local/opt/llvm`。确保 `libclang.dylib` 可由 `LIBCLANG_PATH` 指向。
- 运行前可执行预检（实现于 `scanner/cli.py` 的 `preflight`）：缺失依赖或路径错误时输出中文错误与退出码。
- 离线安装 Python 包（示例）：在联网机器下载 wheel（Python 2.7 最后一版）
  - `pandas==0.24.2`、`openpyxl==2.6.4`、`jdcal==1.4.1`、`et_xmlfile==1.0.1`
  - 使用 `pip download -d pkgs pandas==0.24.2 openpyxl==2.6.4 jdcal==1.4.1 et_xmlfile==1.0.1`
  - 拷贝 `pkgs/` 到离线机后执行 `python -m pip install --no-index --find-links pkgs pandas==0.24.2 openpyxl==2.6.4 jdcal==1.4.1 et_xmlfile==1.0.1`

## FAQ（离线/安装常见问题）
- 找不到 `libclang.dylib`：确认 Homebrew 路径（如 `/opt/homebrew/opt/llvm/lib`），或设置 `LIBCLANG_PATH` 指向实际的 `libclang.dylib` 目录。
- pip 源不可用：使用 `pip download -d <目录> ...` 在联网机器准备 wheel，离线机用 `--no-index --find-links` 安装。
- 预检失败：运行 `python scanner/cli.py <project_path>`，根据中文错误提示补齐 Python/依赖/libclang/路径，再重试。
