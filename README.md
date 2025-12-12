# Rhadamanthys
一个用来检查新发布 iOS app 是否符合 App Store 上架标准的工具。

- 工作流程规范：`rules/core-rules/workflow-agile-manual.mdc`

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
