# 更新日志

格式遵循 [Keep a Changelog](https://keepachangelog.com/)，版本遵循 [语义化版本](https://semver.org/)。

---

## [5.6.0] - 2026-03-28

### Added
- `pyproject.toml` 现代化 Python 项目配置
- `Makefile` 常用命令快捷方式
- `Dockerfile` 容器化部署支持
- GitHub Actions CI/CD 工作流
- `logging_config.py` 统一日志配置
- `config_loader.py` 统一配置加载器
- 单元测试框架 (`scripts/tests/`)
- `.pre-commit-config.yaml` 代码提交检查
- 配置模板和 `.env.example`
- 文档：CONTRIBUTING, QUICKSTART, DEPLOYMENT

### Changed
- 完善 `requirements.txt` 依赖列表
- 更新 `.gitignore` 忽略规则
- 代码格式化 (Black + Ruff)

### Removed
- 删除临时文档 (OPTIMIZATION_SUMMARY, POSTMORTEM, PUSH_INVESTIGATION)
- 删除冗余文档 (AGILE_DEVELOPMENT, GIT_WORKFLOW, TESTING, TECH_STACK)

---

## [5.5.0] - 2026-03-28

### Added
- 预测历史记录功能
- 根据历史准确率调整置信度

---

## [5.4.0] - 2026-03-27

### Added
- 多股票预测推送支持

---

## [5.3.0] - 2026-03-26

### Fixed
- 使用 venv 绝对路径解决 cron 环境问题

---

## [5.0.0] - 2026-03-10

### Added
- 基础股票监控系统
- 飞书推送、Web 界面、定时任务

---

## 版本说明

- **Major:** 不兼容的 API 变更
- **Minor:** 向后兼容的功能新增
- **Patch:** 向后兼容的问题修复
