# 规则缓存包使用示例（占位）

> 目标：演示从本地 zip/tar.gz 缓存加载规则的命令占位，待 `rules_sync` 实现后补充实际逻辑。

## 在线更新（当前占位）
```bash
python scanner/cli.py --command update-rules <project_path>
# 成功/无更新退出码 0，失败退出码 3，失败时保留本地规则
```

## 离线缓存包（规划）
```bash
# 预期命令示例，待规则同步实现后生效
python scanner/cli.py --command update-rules <project_path> --rules-package /path/to/rules-cache.zip
```

- 缓存包内容：规则文件（YAML/JSON）+ `version.json`（version/released_at/source_link/checksum）。
- 兼容方式：如未实现自动加载，可手动将缓存包解压覆盖 `scanner/rules/` 并更新 `version.json`。

## 注意
- 当前版本仅提供占位接口与文档示例，真实的下载/校验/回退逻辑尚未落地。***
