# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 Web 界面 (FastAPI)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# 访问：http://localhost:8000
# API 文档：http://localhost:8000/docs
# 模拟交易：http://localhost:8000/trading

# 运行监控脚本
python3 scripts/multi_stocks_monitor.py    # 股票监控
python3 scripts/gold_monitor.py            # 黄金监控
python3 scripts/prediction_push.py         # 预测推送
python3 scripts/price_alert_monitor.py     # 股价预警
python3 scripts/paper_trading.py           # 模拟交易
```

## Makefile 命令

```bash
make install       # 安装生产环境依赖
make dev           # 安装开发环境依赖 (pytest, black, ruff, mypy)
make test          # 运行测试 (scripts/tests/)
make lint          # 代码风格检查 (ruff)
make type-check    # 类型检查 (mypy)
make clean         # 清理缓存和构建文件
make run-web       # 启动 Web 界面
make run-monitor   # 运行股票监控
make run-gold      # 运行黄金监控
```

## 测试

```bash
# 运行所有测试
python -m pytest scripts/tests/ -v --cov=scripts --cov-report=html

# 运行单个测试文件
python -m pytest scripts/tests/test_trading.py -v

# 运行特定测试
python -m pytest scripts/tests/test_trading.py::test_buy_order -v
```

## 项目结构

```
stock-monitor-system/
├── app/                      # FastAPI 应用
│   ├── main.py               # 应用入口，创建 FastAPI 实例
│   ├── api/                  # API 路由
│   │   ├── api.py            # REST API 端点 (/api/*)
│   │   ├── views.py          # 页面路由 (/，/trading)
│   │   └── trading.py        # 模拟交易 API
│   ├── core/                 # 核心配置
│   │   ├── config.py         # Pydantic Settings 配置
│   │   └── middleware.py     # 中间件 (CORS, 请求日志)
│   ├── models/               # Pydantic 模型
│   │   └── schemas.py        # 请求/响应数据模型
│   ├── services/             # 业务逻辑层
│   │   ├── config_loader.py  # 配置文件加载/保存
│   │   └── stock_service.py  # 股票数据获取服务
│   └── templates/            # Jinja2 HTML 模板
│
├── src/                      # 核心服务模块 (可复用)
│   ├── __init__.py           # 公共导出
│   ├── stock_service.py      # 股票服务 (腾讯财经 API)
│   ├── gold_service.py       # 黄金服务 (SHFE/COMEX)
│   ├── predictor.py          # 股票预测器 (技术指标+ML)
│   ├── feishu.py             # 飞书推送
│   ├── logging_config.py     # 日志配置
│   ├── config_loader.py      # 配置加载器
│   ├── trading/              # 量化交易模拟盘
│   │   ├── engine.py         # 交易引擎
│   │   ├── account.py        # 账户管理
│   │   ├── order.py          # 订单管理
│   │   ├── position.py       # 持仓管理
│   │   ├── strategy.py       # 交易策略
│   │   ├── calendar.py       # 交易日历
│   │   └── market_data.py    # 行情数据
│   └── utils/                # 工具函数
│
├── scripts/                  # 监控脚本
│   ├── multi_stocks_monitor.py
│   ├── gold_monitor.py
│   ├── prediction_push.py
│   ├── price_alert_monitor.py
│   ├── paper_trading.py
│   ├── auto_trader.py
│   └── tests/                # 单元测试
│
├── config/                   # 配置文件
│   ├── stocks_config.json    # 股票配置
│   ├── gold_config.json      # 黄金配置
│   ├── feishu_config.json    # 飞书凭证 (敏感)
│   └── trading_config.json   # 交易配置
│
└── cron_install.sh           # Cron 定时任务管理
```

## 核心架构

### 数据流

```
用户请求 → FastAPI (app/main.py)
         ↓
    API Router (app/api/api.py)
         ↓
    Service Layer (src/*.py, app/services/*.py)
         ↓
    外部 API (腾讯财经，AkShare, 飞书)
```

### 配置管理

- **Pydantic Settings**: `app/core/config.py` - 应用配置 (单例模式)
- **JSON 配置文件**: `config/*.json` - 业务配置 (股票列表，飞书凭证，交易参数)
- **配置加载器**: `src/config_loader.py` - 加载/保存 JSON 配置

### 服务层设计

- `src/` 目录包含可复用的核心服务，提供统一的 API
- `app/services/` 包含 FastAPI 特定的业务逻辑封装
- 所有服务使用依赖注入模式 (如 `stock_service`, `config_loader`)

### 模拟交易架构

```
TradingEngine (engine.py)
    ↓
Account (账户管理) + OrderManager (订单管理) + PositionManager (持仓管理)
    ↓
TradingStrategy (策略信号生成)
    ↓
MarketData + TradingCalendar (行情和交易日历)
```

## Cron 定时任务

```bash
./cron_install.sh install      # 安装所有任务
./cron_install.sh status       # 查看状态
./cron_install.sh stocks       # 只安装股票推送
./cron_install.sh gold         # 只安装黄金监控
./cron_install.sh alert        # 只安装股价预警
./cron_install.sh uninstall    # 卸载所有任务
```

**推送时间表 (交易日):**
| 任务 | 时间 | 频率 |
|------|------|------|
| 股票推送 | 9:30-15:00 | 每 30 分钟 |
| 黄金监控 | 9:30-15:00 | 每小时 |
| 股价预警 | 9:30-15:00 | 每 5 分钟 (±5% 阈值) |
| 预测推送 | 15:30 | 每日一次 |

## 开发规范

**Git 工作流:**
```bash
git checkout -b feature/xxx    # 创建分支
# 开发 + 测试
git add .
git commit -m "feat: 描述"     # type: feat/fix/docs/refactor/test/chore
git push -u origin feature/xxx
# GitHub 创建 PR → 审查 → 合并到 main
```

**代码风格:**
- Line length: 100 (black, ruff)
- Python 3.8+ 类型提示
- 使用 `ruff check` 和 `mypy` 进行代码检查

**关键约束:**
- 禁止直接在 main 分支开发
- 禁止跳过 PR 审查
- 禁止未测试就提交
- 单 PR >10 文件需拆分
- 重构后必须更新配置

## 数据源

| 数据类型 | 数据源 | 说明 |
|---------|--------|------|
| 实时行情 | 腾讯财经 | A 股实时股价 |
| 历史行情 | AkShare | 历史 K 线数据 |
| 新闻/公告 | AkShare/东方财富 | 股票相关资讯 |
| 黄金价格 | SHFE/COMEX | 上海期货交易所/COMEX 期货 |
| 技术指标 | 自研 + TA-Lib | MA/MACD/RSI/KDJ/布林带 |
| 预测模型 | scikit-learn | 机器学习预测 |

## 常见问题

**Q: 飞书推送不工作？**
A: 检查 `config/feishu_config.json` 中的 `app_id` 和 `app_secret` 是否正确

**Q: 股票数据获取失败？**
A: 确保服务器可访问外网，检查 AkShare 和腾讯财经 API 可用性

**Q: 模拟交易数据库错误？**
A: 删除 `data/paper_trading.db` 并重启服务

**Q: Cron 任务不执行？**
A: 运行 `./cron_install.sh status` 检查状态，确保 Python 路径正确
