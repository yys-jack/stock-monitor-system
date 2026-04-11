# 📈 股票监控系统

> **Stock Monitor System** - 实时股价监控 + 智能预测 + Web 界面 + 飞书推送

[![GitHub](https://img.shields.io/github/license/yys-jack/stock-monitor-system)](https://github.com/yys-jack/stock-monitor-system)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CI/CD](https://github.com/yys-jack/stock-monitor-system/actions/workflows/ci.yml/badge.svg)](https://github.com/yys-jack/stock-monitor-system/actions/workflows/ci.yml)

## ⚡ 快速开始

```bash
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system
pip install -r requirements.txt
uvicorn app.main:app --reload
```

访问 http://localhost:8000

## 📚 文档索引

| 类型 | 文档 |
|------|------|
| 📖 用户指南 | [docs/guide/](docs/guide/) |
| 💻 开发文档 | [docs/dev/](docs/dev/) |
| 📋 更新日志 | [CHANGELOG.md](CHANGELOG.md) |
| 🗺️ 路线图 | [ROADMAP.md](ROADMAP.md) |

## 🎯 功能概览

| 模块 | 状态 |
|------|------|
| 📊 多股票监控 | ✅ |
| 🥇 黄金监控 | ✅ |
| 🔮 智能预测 | ✅ |
| 🌐 Web 界面 | ✅ |
| 💹 模拟交易 | ✅ |

## 📬 飞书推送

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `app_id` 和 `app_secret`
4. 配置 `config/feishu_config.json`

详见：[快速开始](docs/guide/quickstart.md)

## 🤖 贡献

欢迎提交 Issue 和 Pull Request!

---

**许可证:** MIT
