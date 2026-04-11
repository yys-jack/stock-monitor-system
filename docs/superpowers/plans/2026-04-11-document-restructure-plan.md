# 文档整理实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重构项目文档结构，将用户指南与开发文档分离，精简 README.md 至 ~100 行。

**Architecture:** 创建 `docs/guide/` 和 `docs/dev/` 两个子目录，分别存放用户指南和开发文档。README.md 保留项目简介和快速开始，其他详细内容迁移到对应子目录。

**Tech Stack:** Markdown 文档，Git 版本控制

---

### Task 1: 创建文档目录结构

**Files:**
- Create: `docs/guide/`
- Create: `docs/dev/`
- Create: `docs/archive/`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p docs/guide docs/dev docs/archive
```

- [ ] **Step 2: 验证目录创建成功**

```bash
ls -la docs/
```

Expected: 显示 `guide/`, `dev/`, `archive/` 三个子目录

- [ ] **Step 3: 提交**

```bash
git add docs/
git commit -m "docs: 创建新的文档目录结构"
```

---

### Task 2: 删除 archive 目录旧内容

**Files:**
- Delete: `archive/FASTAPI_MIGRATION.md`
- Delete: `archive/PROJECT_STRUCTURE.md`
- Delete: `archive/README.md`
- Delete: `archive/QUICKSTART.md`

- [ ] **Step 1: 删除旧 archive 文件**

```bash
rm -rf archive/
```

- [ ] **Step 2: 创建新的 archive 索引**

```markdown
# 历史归档

本目录存放已废弃的文档，供历史参考。

## 归档记录

- 2026-04-11: 删除 FastAPI 迁移文档（迁移已完成）
- 2026-04-11: 删除旧项目结构文档（已合并到 architecture.md）
- 2026-04-11: 删除旧 README 和 QUICKSTART（已整合到新结构）

如需查看历史版本文档，请参考 git 历史：
```bash
git log --all --full-history -- docs/
```
```

文件：`docs/archive/README.md`

- [ ] **Step 3: 提交**

```bash
git add -A archive/ docs/archive/
git commit -m "docs: 清理过时的 archive 文档"
```

---

### Task 3: 创建用户指南索引

**Files:**
- Create: `docs/guide/README.md`

- [ ] **Step 1: 创建用户指南索引**

```markdown
# 用户指南

本目录包含股票监控系统的使用指南。

## 快速开始

| 文档 | 说明 |
|------|------|
| [快速开始](quickstart.md) | 5 分钟上手指南 |
| [部署指南](deployment.md) | 生产环境部署（本地/Docker） |
| [配置说明](config.md) | 股票/黄金/飞书配置详解 |

## 功能使用

| 文档 | 说明 |
|------|------|
| [股票监控](stock-monitoring.md) | 多股票监控使用 |
| [黄金监控](gold-monitoring.md) | 黄金价格监控 |
| [智能预测](prediction.md) | 股票预测功能 |
| [模拟交易](trading.md) | 量化交易模拟盘 |

## 运维

| 文档 | 说明 |
|------|------|
| [Cron 定时任务](cron.md) | 定时任务管理 |
| [故障排除](troubleshooting.md) | 常见问题解答 |

## 返回项目首页

- [README](../../README.md)
```

- [ ] **Step 2: 提交**

```bash
git add docs/guide/README.md
git commit -m "docs: 创建用户指南索引"
```

---

### Task 4: 创建快速开始文档

**Files:**
- Create: `docs/guide/quickstart.md`

- [ ] **Step 1: 从 README.md 提取快速开始内容**

读取 `README.md` 第 27-52 行内容

- [ ] **Step 2: 创建快速开始文档**

```markdown
# 快速开始

> 5 分钟上手股票监控系统

## 前置要求

- Python 3.8+
- pip 包管理器
- 飞书应用（可选，用于推送通知）

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
# 或使用 Make
make install
```

### 4. 配置飞书推送（可选）

```bash
cp config/feishu_config.example.json config/feishu_config.json
vim config/feishu_config.json
```

**获取飞书凭证：**
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `app_id` 和 `app_secret`
4. 在应用中添加用户 ID

> ⚠️ **注意：** `feishu_config.json` 已加入 `.gitignore`，不会被提交到 Git。

### 5. 配置股票

```bash
cp config/stocks_config.example.json config/stocks_config.json
vim config/stocks_config.json
```

示例配置：
```json
{
  "stocks": [
    {
      "code": "000063",
      "name": "中兴通讯",
      "market": "sz",
      "enabled": true,
      "alias": "ZTE",
      "notes": "5G 通信设备龙头"
    }
  ]
}
```

### 6. 启动服务

#### Web 界面（推荐）
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：http://localhost:8000

#### 命令行监控
```bash
python3 scripts/multi_stocks_monitor.py
```

## 下一步

- [配置说明](config.md) - 详细配置选项
- [部署指南](deployment.md) - 生产环境部署
- [故障排除](troubleshooting.md) - 常见问题
```

- [ ] **Step 3: 提交**

```bash
git add docs/guide/quickstart.md
git commit -m "docs: 创建快速开始文档"
```

---

### Task 5: 创建部署指南文档

**Files:**
- Create: `docs/guide/deployment.md`

- [ ] **Step 1: 读取现有 DEPLOYMENT.md**

- [ ] **Step 2: 创建部署指南文档**

```markdown
# 部署指南

## 本地开发环境

```bash
# 1. 克隆
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system

# 2. 虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置
cp config/feishu_config.example.json config/feishu_config.json
cp .env.example .env

# 5. 运行
uvicorn app.main:app --reload
```

## 生产环境部署

### 方案 A: 直接部署

```bash
# 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 配置
vim config/feishu_config.json
vim config/stocks_config.json

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app

# 定时任务
bash cron_install.sh install
```

### 方案 B: Docker 部署

```bash
# 构建镜像
docker build -t stock-monitor-system .

# 运行容器
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/config:/app/config \
  --name stock-monitor \
  stock-monitor-system
```

### 方案 C: Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

运行：
```bash
docker-compose up -d
```

## Cron 定时任务

```bash
# 安装所有任务
./cron_install.sh install

# 查看状态
./cron_install.sh status

# 卸载任务
./cron_install.sh uninstall
```

详见：[Cron 定时任务](cron.md)

## 验证部署

```bash
# 健康检查
curl http://localhost:8000/health

# 查看日志
tail -f logs/*.log
```
```

- [ ] **Step 3: 提交**

```bash
git add docs/guide/deployment.md
git commit -m "docs: 创建部署指南文档"
```

---

### Task 6: 创建配置说明文档

**Files:**
- Create: `docs/guide/config.md`

- [ ] **Step 1: 创建配置说明文档**

```markdown
# 配置说明

## 配置文件位置

所有配置文件位于 `config/` 目录：

```
config/
├── stocks_config.json         # 股票配置
├── gold_config.json           # 黄金配置
├── feishu_config.json         # 飞书推送配置 ⚠️ 敏感
└── trading_config.json        # 交易配置
```

## 股票配置

文件：`config/stocks_config.json`

```json
{
  "stocks": [
    {
      "code": "000063",
      "name": "中兴通讯",
      "market": "sz",
      "enabled": true,
      "alias": "ZTE",
      "notes": "5G 通信设备龙头"
    }
  ],
  "settings": {
    "push_interval_minutes": 30,
    "alert_threshold_up": 5.0,
    "alert_threshold_down": -5.0,
    "push_format": "single"
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | string | ✅ | 股票代码 |
| `name` | string | ✅ | 股票名称 |
| `market` | string | ✅ | 市场：`sz`/`sh` |
| `enabled` | boolean | ❌ | 是否启用（默认 true） |
| `alias` | string | ❌ | 别名 |
| `notes` | string | ❌ | 备注 |

## 黄金配置

文件：`config/gold_config.json`

```json
{
  "type": "AU9999",
  "alias": "黄金",
  "notes": "上海黄金交易所 AU9999 现货基准价",
  "settings": {
    "push_interval_minutes": 60,
    "retry_times": 3,
    "retry_delay_seconds": 2
  }
}
```

## 飞书推送配置

文件：`config/feishu_config.json`

```json
{
  "app_id": "cli_xxxxxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxx",
  "user_ids": ["xxxxxxxxxxxxx"]
}
```

> ⚠️ **安全提示：** 此文件包含敏感信息，已加入 `.gitignore`，不要提交到 Git。

## 交易配置

文件：`config/trading_config.json`

```json
{
  "paper_trading": {
    "initial_capital": 100000,
    "commission_rate": 0.0003,
    "stamp_duty_rate": 0.001,
    "max_position_pct": 0.3,
    "stop_loss_pct": -10.0,
    "take_profit_pct": 20.0,
    "min_buy_amount": 1000
  },
  "auto_trading": {
    "enabled": false,
    "signal_confidence_threshold": 70,
    "check_interval_minutes": 30,
    "max_orders_per_cycle": 5
  }
}
```
```

- [ ] **Step 2: 提交**

```bash
git add docs/guide/config.md
git commit -m "docs: 创建配置说明文档"
```

---

### Task 7: 创建 Cron 定时任务文档

**Files:**
- Create: `docs/guide/cron.md`

- [ ] **Step 1: 从 README.md 提取 Cron 相关内容**

- [ ] **Step 2: 创建 Cron 定时任务文档**

```markdown
# Cron 定时任务管理

## 统一命令

```bash
# 安装所有任务
./cron_install.sh install

# 查看状态
./cron_install.sh status

# 卸载所有任务
./cron_install.sh uninstall

# 单独安装
./cron_install.sh stocks  # 只安装股票推送
./cron_install.sh gold    # 只安装黄金监控
./cron_install.sh alert   # 只安装股价预警
```

## 推送时间表（交易日）

| 任务 | 时间 | 频率 |
|------|------|------|
| 股票推送 | 9:30-15:00 | 每 30 分钟 |
| 黄金监控 | 9:30-15:00 | 每小时 |
| 股价预警 | 9:30-15:00 | 每 5 分钟 (±5% 阈值) |
| 预测推送 | 15:30 | 每日一次 |

## Cron 表达式详解

### 股票推送

```bash
# 9:30 开盘
30 9 * * 1-5

# 10:00, 10:30, 11:00, 11:30
0,30 10-11 * * 1-5

# 13:00, 13:30, 14:00, 14:30
0,30 13-14 * * 1-5

# 15:00 收盘
0 15 * * 1-5
```

### 黄金监控

```bash
# 每小时 30 分
30 9-11 * * 1-5
30 13-14 * * 1-5
```

### 股价预警

```bash
# 每 5 分钟
*/5 9-11 * * 1-5
*/5 13-14 * * 1-5
0-5/5 15 * * 1-5
```

## 日志查看

```bash
# 股票推送日志
tail -f logs/push_cron.log

# 黄金监控日志
tail -f logs/gold_cron.log

# 股价预警日志
tail -f logs/alert_cron.log
```

## 故障排除

### Cron 任务未执行

1. 检查 Cron 服务状态：
```bash
systemctl status cron
```

2. 查看 Cron 日志：
```bash
grep CRON /var/log/syslog
```

3. 验证 Python 路径：
```bash
which python3
```

### 飞书推送失败

检查 `config/feishu_config.json` 凭证是否正确。
```

- [ ] **Step 3: 提交**

```bash
git add docs/guide/cron.md
git commit -m "docs: 创建 Cron 定时任务文档"
```

---

### Task 8: 创建模拟交易文档

**Files:**
- Create: `docs/guide/trading.md`

- [ ] **Step 1: 读取 docs/TRADING.md**

- [ ] **Step 2: 移动到 docs/guide/trading.md**

```bash
mv docs/TRADING.md docs/guide/trading.md
```

- [ ] **Step 3: 提交**

```bash
git add docs/guide/trading.md
git commit -m "docs: 移动模拟交易文档到用户指南"
```

---

### Task 9: 创建故障排除文档

**Files:**
- Create: `docs/guide/troubleshooting.md`

- [ ] **Step 1: 创建故障排除文档**

```markdown
# 故障排除

## 常见问题

### 飞书推送不工作

**症状：** 收不到飞书消息推送

**原因：** 凭证配置错误

**解决方法：**
1. 检查 `config/feishu_config.json` 中的 `app_id` 和 `app_secret` 是否正确
2. 确认飞书应用已发布
3. 验证用户 ID 是否正确添加

### 股票数据获取失败

**症状：** API 返回空数据或错误

**原因：** 网络问题或 API 不可用

**解决方法：**
1. 确保服务器可访问外网
2. 检查 AkShare 和腾讯财经 API 可用性
3. 查看日志文件：`logs/*.log`

### 模拟交易数据库错误

**症状：** 无法创建订单或查询持仓

**原因：** 数据库表结构问题

**解决方法：**
```bash
# 删除旧数据库
rm data/paper_trading.db

# 重启服务
uvicorn app.main:app --reload
```

### Cron 任务不执行

**症状：** 定时任务未运行

**原因：** Cron 服务未启动或路径错误

**解决方法：**
```bash
# 检查 Cron 服务
systemctl status cron

# 重新安装 Cron 任务
./cron_install.sh uninstall
./cron_install.sh install

# 验证 Python 路径
which python3
```

### Web 界面无法访问

**症状：** 浏览器显示无法连接

**原因：** 服务未启动或端口被占用

**解决方法：**
```bash
# 检查服务是否运行
ps aux | grep uvicorn

# 查看端口占用
lsof -i :8000

# 重启服务
uvicorn app.main:app --reload --port 8001
```

## 日志文件位置

```
logs/
├── push_cron.log      # 股票推送
├── gold_cron.log      # 黄金监控
├── alert_cron.log     # 股价预警
└── app.log            # Web 应用
```

## 获取帮助

- [GitHub Issues](https://github.com/yys-jack/stock-monitor-system/issues)
- [讨论区](https://github.com/yys-jack/stock-monitor-system/discussions)
```

- [ ] **Step 2: 提交**

```bash
git add docs/guide/troubleshooting.md
git commit -m "docs: 创建故障排除文档"
```

---

### Task 10: 创建开发文档索引

**Files:**
- Create: `docs/dev/README.md`

- [ ] **Step 1: 创建开发文档索引**

```markdown
# 开发文档

本目录包含开发者相关的文档。

## 入门

| 文档 | 说明 |
|------|------|
| [开发环境设置](setup.md) | 本地开发环境配置 |
| [贡献指南](contributing.md) | 代码贡献流程 |

## 技术文档

| 文档 | 说明 |
|------|------|
| [架构说明](architecture.md) | 系统架构和数据流 |
| [API 文档](api.md) | REST API 接口说明 |

## 返回项目首页

- [README](../../README.md)
```

- [ ] **Step 2: 提交**

```bash
git add docs/dev/README.md
git commit -m "docs: 创建开发文档索引"
```

---

### Task 11: 创建开发环境设置文档

**Files:**
- Create: `docs/dev/setup.md`

- [ ] **Step 1: 创建开发环境设置文档**

```markdown
# 开发环境设置

## 前置要求

- Python 3.8+
- Git
- 代码编辑器（VS Code/PyCharm）

## 克隆项目

```bash
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system
```

## 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装生产依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt
# 或
make dev
```

## 代码质量工具

```bash
# 代码风格检查
make lint      # ruff

# 类型检查
make type-check  # mypy

# 运行测试
make test      # pytest
```

## Pre-commit 钩子

```bash
# 安装 pre-commit
pip install pre-commit
pre-commit install

# 手动运行检查
pre-commit run --all-files
```

## 运行开发服务器

```bash
# Web 界面
uvicorn app.main:app --reload

# 访问 http://localhost:8000
```
```

- [ ] **Step 2: 提交**

```bash
git add docs/dev/setup.md
git commit -m "docs: 创建开发环境设置文档"
```

---

### Task 12: 创建贡献指南文档

**Files:**
- Create: `docs/dev/contributing.md`

- [ ] **Step 1: 读取现有 CONTRIBUTING.md**

- [ ] **Step 2: 移动到 docs/dev/contributing.md**

```bash
mv CONTRIBUTING.md docs/dev/contributing.md
```

- [ ] **Step 3: 更新内容添加开发规范**

在文件末尾添加：

```markdown
## 开发规范

详见：[CLAUDE.md](../../.claude/CLAUDE.md)

### Git 工作流

```bash
# 1. 创建分支
git checkout -b feature/xxx

# 2. 开发 + 测试
# 编写代码 → 运行测试 → 通过

# 3. 提交
git add .
git commit -m "feat: 描述"
git push -u origin feature/xxx

# 4. PR 审查
# GitHub 创建 Pull Request

# 5. 合并
# 审查通过后合并到 main
```

### Commit 规范

格式：`<type>: <description>`

| 类型 | 说明 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | Bug 修复 |
| `docs:` | 文档更新 |
| `refactor:` | 重构 |
| `test:` | 测试 |
| `chore:` | 配置/工具 |
```

- [ ] **Step 4: 提交**

```bash
git add docs/dev/contributing.md
git commit -m "docs: 移动并更新贡献指南"
```

---

### Task 13: 创建架构说明文档

**Files:**
- Create: `docs/dev/architecture.md`

- [ ] **Step 1: 创建架构说明文档**

```markdown
# 架构说明

## 系统架构

```
用户请求 → FastAPI (app/main.py)
         ↓
    API Router (app/api/api.py)
         ↓
    Service Layer (src/*.py, app/services/*.py)
         ↓
    外部 API (腾讯财经，AkShare, 飞书)
```

## 项目结构

```
stock-monitor-system/
├── app/                      # FastAPI 应用
│   ├── main.py               # 应用入口
│   ├── api/                  # API 路由
│   ├── core/                 # 核心配置
│   ├── models/               # Pydantic 模型
│   ├── services/             # 业务逻辑
│   └── templates/            # HTML 模板
│
├── src/                      # 核心服务模块
│   ├── stock_service.py      # 股票服务
│   ├── gold_service.py       # 黄金服务
│   ├── predictor.py          # 股票预测器
│   ├── feishu.py             # 飞书推送
│   └── trading/              # 量化交易模拟盘
│
├── scripts/                  # 监控脚本
├── config/                   # 配置文件
└── docs/                     # 文档
```

## 核心模块

### 配置管理

- **Pydantic Settings**: `app/core/config.py` - 应用配置（单例模式）
- **JSON 配置文件**: `config/*.json` - 业务配置
- **配置加载器**: `src/config_loader.py` - 加载/保存 JSON 配置

### 服务层设计

- `src/` 目录包含可复用的核心服务
- `app/services/` 包含 FastAPI 特定的业务逻辑封装
- 所有服务使用依赖注入模式

### 模拟交易架构

```
TradingEngine (engine.py)
    ↓
Account + OrderManager + PositionManager
    ↓
TradingStrategy
    ↓
MarketData + TradingCalendar
```

## 数据源

| 数据类型 | 数据源 | 说明 |
|---------|--------|------|
| 实时行情 | 腾讯财经 | A 股实时股价 |
| 历史行情 | AkShare | 历史 K 线数据 |
| 新闻/公告 | AkShare/东方财富 | 股票相关资讯 |
| 黄金价格 | SHFE/COMEX | 期货价格 |
```

- [ ] **Step 2: 提交**

```bash
git add docs/dev/architecture.md
git commit -m "docs: 创建架构说明文档"
```

---

### Task 14: 创建 API 文档

**Files:**
- Create: `docs/dev/api.md`

- [ ] **Step 1: 创建 API 文档**

```markdown
# API 文档

## RESTful API

访问 API 文档：http://localhost:8000/docs

### 股票相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/stock/{code}` | GET | 获取股票实时数据 |
| `/api/news/{code}` | GET | 获取股票新闻 |
| `/api/history/{code}` | GET | 获取历史行情 |
| `/api/predict/{code}` | GET | 获取预测数据 |

### 配置管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/stocks` | GET | 获取股票配置列表 |
| `/api/stocks` | POST | 添加股票 |
| `/api/stocks/{code}` | DELETE | 删除股票 |
| `/api/stocks/{code}/toggle` | POST | 切换启用状态 |

### 模拟交易

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/trading/account` | GET | 获取账户信息 |
| `/api/trading/position` | GET | 获取持仓列表 |
| `/api/trading/order` | GET | 获取订单列表 |
| `/api/trading/order` | POST | 下单委托 |
| `/api/trading/order/{id}` | DELETE | 撤销订单 |

## 示例

### 获取股票数据

```bash
curl http://localhost:8000/api/stock/000063
```

### 添加股票

```bash
curl -X POST http://localhost:8000/api/stocks \
  -H "Content-Type: application/json" \
  -d '{
    "code": "000063",
    "name": "中兴通讯",
    "market": "sz"
  }'
```

### 买入股票

```bash
curl -X POST http://localhost:8000/api/trading/order \
  -H "Content-Type: application/json" \
  -d '{
    "stock_code": "000063",
    "stock_name": "中兴通讯",
    "side": "BUY",
    "price": 37.50,
    "quantity": 100
  }'
```
```

- [ ] **Step 2: 提交**

```bash
git add docs/dev/api.md
git commit -m "docs: 创建 API 文档"
```

---

### Task 15: 精简 README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 备份当前 README**

```bash
cp README.md README.md.backup
```

- [ ] **Step 2: 重写 README.md**

```markdown
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
```

- [ ] **Step 3: 删除备份**

```bash
rm README.md.backup
```

- [ ] **Step 4: 提交**

```bash
git add README.md
git commit -m "docs: 精简 README.md 并添加文档索引"
```

---

### Task 16: 删除 DEPLOYMENT.md 和 CONTRIBUTING.md

**Files:**
- Delete: `DEPLOYMENT.md`
- Delete: `CONTRIBUTING.md`

- [ ] **Step 1: 确认内容已迁移**

验证：
- `docs/guide/deployment.md` 存在
- `docs/dev/contributing.md` 存在

- [ ] **Step 2: 删除旧文件**

```bash
rm DEPLOYMENT.md CONTRIBUTING.md
```

- [ ] **Step 3: 提交**

```bash
git add -A
git commit -m "docs: 删除已迁移的旧文档"
```

---

### Task 17: 验证文档链接

**Files:**
- 验证所有 Markdown 文件中的链接

- [ ] **Step 1: 运行链接检查**

```bash
# 检查 README.md 中的链接
grep -E '\[.*\]\(' README.md | while read -r line; do
  url=$(echo "$line" | grep -oP '\(\K[^\)]+')
  if [[ ! "$url" =~ ^http ]]; then
    test -f "$url" && echo "✅ $url" || echo "❌ $url 不存在"
  fi
done
```

- [ ] **Step 2: 修复损坏的链接**

如有损坏的链接，逐一修复

- [ ] **Step 3: 提交**

```bash
git add -A
git commit -m "docs: 修复损坏的文档链接"
```

---

### Task 18: 最终验证和清理

- [ ] **Step 1: 查看最终文档结构**

```bash
find docs -name "*.md" | sort
```

- [ ] **Step 2: 运行 git status**

```bash
git status
```

- [ ] **Step 3: 提交所有剩余更改**

```bash
git add -A
git commit -m "docs: 完成文档重构"
```

---

## 计划完成

**文档结构已完成：**

```
stock-monitor-system/
├── README.md                  # 精简版
├── CHANGELOG.md               # 保留
├── ROADMAP.md                 # 保留
├── docs/
│   ├── guide/                 # 用户指南（7 个文档）
│   ├── dev/                   # 开发文档（5 个文档）
│   └── archive/               # 归档说明
└── .claude/
    └── CLAUDE.md              # 保留
```

**下一步：** 选择执行方式

1. **Subagent-Driven** (推荐) - 每个 Task 由独立 subagent 执行
2. **Inline Execution** - 在当前会话中批量执行

请选择执行方式。
