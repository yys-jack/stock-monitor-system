# Archive - 归档文件

本目录存放已废弃但保留参考价值的文件。

## 归档内容

### 2026-03-29 项目清理

| 文件 | 说明 | 替代方案 |
|------|------|----------|
| `app.py` | 旧 Flask 应用入口 | 使用 `app/main.py` (FastAPI) |
| `install_crontab.sh` | 旧 cron 安装脚本 | `cron_install.sh` |
| `verify_push.sh` | 推送验证脚本（路径硬编码失效） | 手动验证日志 |
| `verify_predictions.py` | 预测验证脚本 | - |
| `cron_prediction_push.py` | 预测推送脚本（重复） | `prediction_push.py` |
| `FASTAPI_MIGRATION.md` | FastAPI 迁移文档 | 迁移已完成 |
| `PROJECT_STRUCTURE.md` | 项目结构文档 | 已合并到 README.md |
| `QUICKSTART.md` | 快速开始指南 | 已合并到 README.md |

## 恢复文件

如需恢复某个文件：
```bash
mv archive/<filename> <original_path>
```
