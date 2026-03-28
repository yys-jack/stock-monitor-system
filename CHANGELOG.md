# 更新日志

所有重要的项目变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [未发布]

### Added
- 添加 `pyproject.toml` 支持现代化 Python 项目管理
- 添加 `Makefile` 提供常用命令快捷方式
- 添加 `Dockerfile` 和 `.dockerignore` 支持容器化部署
- 添加 GitHub Actions CI/CD 工作流
- 添加 `logging_config.py` 统一日志配置
- 添加 `config_loader.py` 统一配置加载器
- 添加 `.pre-commit-config.yaml` 代码提交前检查
- 添加 `CONTRIBUTING.md` 贡献指南
- 添加 `QUICKSTART.md` 快速开始指南
- 添加 `LICENSE` MIT 许可证
- 添加配置文件示例 (`stocks_config.example.json`, `feishu_config.example.json`)
- 添加 `.env.example` 环境变量模板

### Changed
- 更新 `requirements.txt` 添加完整依赖列表
- 更新 `.gitignore` 添加更多忽略规则

### Improved
- 项目结构更加规范化
- 支持 Docker 容器化部署
- 支持 CI/CD 自动化测试和部署
- 改进配置管理，支持缓存和环境变量

---

## [5.5.0] - 2026-03-28

### Added
- 预测历史记录功能
- 根据历史准确率调整置信度

---

## [5.4.0] - 2026-03-27

### Added
- 多股票预测推送支持
- 与 stocks_config.json 关联

---

## [5.3.0] - 2026-03-26

### Fixed
- 使用 venv 绝对路径解决 cron 环境问题

---

## [5.2.0] - 2026-03-25

### Added
- 添加 PYTHONUNBUFFERED=1 解决日志缓冲问题
- 黄金价格监控功能

---

## [5.0.0] - 2026-03-10

### Added
- 基础股票监控系统
- 飞书推送
- Web 界面
- 定时任务支持

---

## 版本说明

- **主版本号 (Major)**: 不兼容的 API 变更
- **次版本号 (Minor)**: 向后兼容的功能新增
- **修订号 (Patch)**: 向后兼容的问题修复
