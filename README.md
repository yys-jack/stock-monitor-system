# 📈 股票监控系统

> **Stock Monitor System** - 实时股价监控 + 智能预测 + Web 界面 + 飞书推送

[![GitHub](https://img.shields.io/github/license/yys-jack/stock-monitor-system)](https://github.com/yys-jack/stock-monitor-system)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-stable-green)](https://github.com/yys-jack/stock-monitor-system)
[![CI/CD](https://github.com/yys-jack/stock-monitor-system/actions/workflows/ci.yml/badge.svg)](https://github.com/yys-jack/stock-monitor-system/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/)

---

## 🎯 功能概览

| 模块 | 功能 | 状态 |
|------|------|------|
| 📊 **多股票监控** | 批量监控多只股票，支持配置管理 | ✅ 就绪 |
| 🥇 **黄金监控** | 监控 COMEX 黄金期货价格（美元/盎司 + 人民币/克） | ✅ 就绪 |
| ⏰ **定时推送** | 交易时间每 30 分钟推送实时股价 | ✅ 就绪 |
| 🔮 **智能预测** | 技术指标分析 + 趋势预测（MA/MACD/RSI/KDJ） | ✅ 就绪 |
| 🌐 **Web 界面** | 实时股价、新闻资讯、历史走势图表、股票配置管理 | ✅ 就绪 |
| 📬 **飞书推送** | 股价提醒 + 预测报告自动推送到飞书 | ✅ 就绪 |
| ⚠️ **异常预警** | 涨跌幅超阈值即时通知（±5%） | ✅ 就绪 |

---

## 🚀 快速开始

### ⚡ 5 分钟上手

详细指南请查看 [QUICKSTART.md](QUICKSTART.md)

```bash
# 1. 克隆项目
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system

# 2. 安装依赖
pip install -r requirements.txt
# 或使用 Make
make install

# 3. 配置飞书推送
cp config/feishu_config.example.json config/feishu_config.json
vim config/feishu_config.json

# 4. 配置股票
cp config/stocks_config.example.json config/stocks_config.json
vim config/stocks_config.json

# 5. 启动 Web 界面
python app.py
# 访问 http://localhost:5000
```

**获取飞书凭证：**
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `app_id` 和 `app_secret`
4. 在应用中添加用户 ID

> ⚠️ **注意：** `feishu_config.json` 已加入 `.gitignore`，不会被提交到 Git，保护你的凭证安全。

### 4. 配置股票

编辑 `stocks_config.json`：

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

### 5. 启动服务

#### 方式 A: Web 界面（推荐）⭐
```bash
python3 app.py
# 访问 http://localhost:5000
```

#### 方式 B: 多股票监控（命令行）
```bash
python3 scripts/multi_stocks_monitor.py
```

#### 方式 C: 预测推送
```bash
python3 scripts/prediction_push.py
```

#### 方式 D: 黄金监控
```bash
python3 scripts/gold_monitor.py
```

---

## 📁 项目结构

```
stock-monitor-system/
├── 🌐 Web 应用 (Flask)
│   ├── app.py                     # 应用入口 ⭐
│   └── webapp/                    # Flask 应用包
│       ├── __init__.py
│       ├── routes/                # 路由模块
│       │   ├── api.py             # API 路由 (/api/*)
│       │   └── views.py           # 页面路由 (/)
│       └── templates/             # 模板文件
│           └── index.html         # Web 界面
│
├── 📄 监控脚本 (scripts/)
│   ├── multi_stocks_monitor.py    # 多股票监控
│   ├── gold_monitor.py            # 黄金价格监控
│   ├── price_alert_monitor.py     # 股价异常预警
│   ├── prediction_push.py         # 预测推送
│   └── tests/                     # 单元测试
│       ├── test_stock_service.py
│       ├── test_gold_service.py
│       ├── test_predictor.py
│       └── test_feishu.py
│
├── ⚙️ 核心模块 (src/)
│   ├── __init__.py                # 公共导出
│   ├── stock_service.py           # 股票服务 ⭐
│   ├── gold_service.py            # 黄金服务
│   ├── predictor.py               # 股票预测器
│   ├── feishu.py                  # 飞书推送
│   ├── config_loader.py           # 配置加载
│   └── logging_config.py          # 日志配置
│
├── ⚙️ 配置 (config/)
│   ├── stocks_config.json         # 股票配置
│   ├── gold_config.json           # 黄金配置
│   ├── feishu_config.json         # 飞书推送配置 ⚠️ 敏感
│   └── feishu_config.example.json # 配置模板
│
├── 📚 文档
│   ├── README.md                  # 使用说明
│   ├── TECH_STACK.md              # 技术栈文档 ⭐
│   ├── AGILE_DEVELOPMENT.md       # 敏捷开发文档
│   ├── GIT_WORKFLOW.md            # Git 工作流程
│   ├── ROADMAP.md                 # 版本路线图
│   ├── MEMORY.md                  # 开发规范与教训 ⭐
│   ├── POSTMORTEM_20260326.md     # Crontab 路径错误复盘
│   └── PUSH_INVESTIGATION_REPORT.md  # 推送问题调查报告
│
├── 🛠️ 运维脚本
│   ├── cron_install.sh            # Cron 统一管理 ⭐
│   └── verify_push.sh             # 推送验证脚本
│
└── 📊 数据目录
    ├── data/                      # 数据库文件
    └── logs/                      # 日志文件
```

---

## 📊 核心功能详解

### 1️⃣ 多股票监控 (`multi_stocks_monitor.py`)

**功能：** 批量监控多只股票，获取实时股价并推送

**特性：**
- ✅ 支持多股票配置管理
- ✅ 每只股票可独立启用/禁用
- ✅ 交易时间判断（非交易时间自动跳过）
- ✅ 推送失败重试机制（3 次）
- ✅ 单条/合并推送模式

**运行：**
```bash
python3 multi_stocks_monitor.py
```

**输出：**
- 飞书消息推送
- `output/stock_<code>.txt` 消息文件

---

### 2️⃣ 黄金价格监控 (`gold_monitor.py`)

**功能：** 监控黄金价格，提供美元/盎司和人民币/克双价格

**特性：**
- ✅ **优先使用上海期货交易所 (SHFE) 黄金期货主力合约**（实时交易价格）
- ✅ 降级使用 COMEX 黄金期货价格（国际参考）
- ✅ 自动换算人民币/克价格
- ✅ 显示涨跌幅和涨跌额
- ✅ 交易时间每小时推送一次
- ✅ 飞书消息推送

**数据源说明：**
| 数据源 | 类型 | 更新频率 | 准确性 |
|--------|------|----------|--------|
| SHFE (上海期货交易所) | 黄金期货主力 (AU0) | 实时交易 | ⭐⭐⭐⭐⭐ 国内实时 |
| COMEX (腾讯财经) | 国际期货价格 | 实时 | ⭐⭐⭐⭐ 国际参考 |

> ✅ **当前使用 SHFE 实时数据，价格准确！** 之前使用的 SGE 基准价每日只更新 2 次，现已优化为上期所期货实时行情。

**配置：** 编辑 `gold_config.json`：
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

**运行：**
```bash
python3 gold_monitor.py
```

**安装 Cron（交易时间每小时推送）：**
```bash
./cron_install.sh gold    # 只安装黄金监控
# 或
./cron_install.sh install # 安装所有任务
```

**输出：**
- 飞书消息推送
- `output/gold_price.txt` 消息文件

---

### 🛠️ Cron 定时任务管理

**统一使用 `cron_install.sh` 管理所有定时任务：**

```bash
# 安装所有任务（股票 + 黄金 + 预警）
./cron_install.sh install

# 查看状态
./cron_install.sh status

# 卸载所有任务
./cron_install.sh uninstall

# 单独安装某项任务
./cron_install.sh stocks  # 只安装股票推送
./cron_install.sh gold    # 只安装黄金监控
./cron_install.sh alert   # 只安装股价预警
```

**推送时间表：**
| 任务 | 推送时间 | 频率 |
|------|---------|------|
| 股票推送 | 交易日 9:30-11:30, 13:00-15:00 | 每 30 分钟 |
| 黄金监控 | 交易日 9:30-11:30, 13:00-15:00 | 每小时 |
| 股价预警 | 交易日 9:30-11:30, 13:00-15:00 | 每 5 分钟 |

**已废弃的旧脚本：**
- ❌ `install_push_cron.sh` - 已废弃，使用 `cron_install.sh stocks`
- ❌ `install_gold_cron.sh` - 已废弃，使用 `cron_install.sh gold`

---

### 3️⃣ 股价异常预警 (`price_alert_monitor.py`)

**功能：** 监控股价涨跌幅，超过阈值时即时推送

**特性：**
- ✅ 可配置涨跌阈值（默认 ±5%）
- ✅ 交易时间每 5 分钟检查
- ✅ 飞书即时通知

**安装 Cron：**
```bash
./install_alert_cron.sh install
```

**命令：**
```bash
./install_alert_cron.sh install    # 安装定时任务
./install_alert_cron.sh status     # 查看状态
./install_alert_cron.sh test       # 测试执行
./install_alert_cron.sh uninstall  # 卸载任务
```

---

### 3️⃣ 智能预测推送 (`prediction_push.py` + `stock_predictor.py`)

**功能：** 生成股票预测报告，包含技术指标和趋势预测

**技术指标：**
- 📈 均线系统（MA5/10/20/60）
- 📊 MACD（指数平滑异同移动平均线）
- 📉 RSI（相对强弱指标）
- 📐 KDJ（随机指标）
- 📏 布林带（Bollinger Bands）

**预测结果：**
- 🔮 趋势预测（买入/卖出/观望）
- 📊 置信度评估
- 📈 支撑位/压力位
- 📅 未来 5 日价格预测

**运行：**
```bash
python3 prediction_push.py
```

**推送时间：** 每个交易日 15:30（收盘后）

---

### 4️⃣ Web 界面 (`web_server.py`)

**功能：** 浏览器访问的股票监控面板

**特性：**
- ✅ 实时股价（支持多股票切换）
- ✅ 新闻资讯列表
- ✅ 历史走势图表（Chart.js K 线图）
- ✅ 预测数据展示
- ✅ ⚙️ **股票配置管理**（添加/删除/启用/禁用）
- ✅ 响应式设计（手机/电脑适配）

**启动：**
```bash
python3 web_server.py
```

**访问：** http://localhost:5000

**API 接口：**
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/stock/<code>` | GET | 获取股票实时数据 |
| `/api/news/<code>` | GET | 获取新闻列表 |
| `/api/history/<code>` | GET | 获取历史行情 |
| `/api/overview` | GET | 获取市场概览 |
| `/api/stocks` | GET | 获取股票配置列表 |
| `/api/stocks` | POST | 添加股票 |
| `/api/stocks/<code>` | DELETE | 删除股票 |
| `/api/stocks/<code>/toggle` | POST | 切换启用状态 |
| `/api/predict/<code>` | GET | 获取预测数据 |

---

## ⚙️ 定时任务配置

### 方式 A: 使用安装脚本（推荐）

```bash
cd stock-monitor-system
./cron_install.sh install
```

### 方式 B: 手动配置 Cron

```bash
crontab -e
```

添加以下内容：

```bash
# 多股票监控 - 交易时间每 30 分钟推送
30 9 * * 1-5 python3 /path/to/multi_stocks_monitor.py
0 10,11 * * 1-5 python3 /path/to/multi_stocks_monitor.py
0,30 13,14 * * 1-5 python3 /path/to/multi_stocks_monitor.py
0 15 * * 1-5 python3 /path/to/multi_stocks_monitor.py

# 股价预警 - 交易时间每 5 分钟检查
*/5 9-11 * * 1-5 python3 /path/to/price_alert_monitor.py
*/5 13-14 * * 1-5 python3 /path/to/price_alert_monitor.py
0-5/5 15 * * 1-5 python3 /path/to/price_alert_monitor.py

# 预测推送 - 每个交易日 15:30（收盘后）
30 15 * * 1-5 python3 /path/to/prediction_push.py
```

---

## 📬 飞书推送配置

### 配置飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `app_id` 和 `app_secret`
4. 在 `stocks_config.json` 或脚本中配置

### 推送格式

**股价提醒：**
```
📈【中兴通讯 000063】股价提醒
🏷️ 别名：ZTE
⏰ 时间：2026-03-11 15:30

💹 实时股价
  当前价：37.12 元 (+0.68%)
  涨跌额：+0.25 元
  
📊 今日行情
  昨收：36.87 元
  开盘：37.00 元
  最高：37.90 元
  最低：36.99 元
  成交量：1,135,850 手
```

**预测报告：**
```
🟡【中兴通讯 预测报告】
📅 日期：2026-03-11

💹 当前股价
  收盘价：¥37.12
  涨跌幅：+0.68%
  
📊 技术指标
  MA5: ¥37.03 | MA10: ¥37.39
  MACD: -0.62 | RSI: 49.8
  
🔮 趋势预测
  信号：🟡 观望
  置信度：中 (61.4%)
  
📈 关键价位
  支撑位：¥35.70
  压力位：¥38.76
```

---

## 📊 数据源

| 数据类型 | 数据源 | 状态 |
|---------|--------|------|
| 📈 **行情** | 腾讯财经 | ✅ 真实数据 |
| 📊 **历史行情** | AkShare | ✅ 真实数据 |
| 📰 **新闻** | AkShare/东方财富 | ✅ 真实数据 |
| 📄 **公告** | AkShare | ✅ 真实数据 |
| 🔬 **研报** | AkShare | ✅ 真实数据 |
| 📊 **财务** | AkShare | ✅ 真实数据 |

---

## 🛠️ 常用命令

```bash
# 🌐 Web 服务
python3 app.py                        # 启动 Web 界面

# 📄 监控脚本
python3 scripts/multi_stocks_monitor.py   # 多股票监控
python3 scripts/gold_monitor.py           # 黄金监控
python3 scripts/prediction_push.py        # 预测推送
python3 scripts/price_alert_monitor.py    # 股价预警

# 🛠️ Cron 管理
./cron_install.sh install             # 安装所有任务
./cron_install.sh status              # 查看状态
./cron_install.sh uninstall           # 卸载任务

# 📊 日志查看
tail -f logs/push_cron.log            # 股票推送日志
tail -f logs/gold_cron.log            # 黄金监控日志
tail -f logs/alert_cron.log           # 预警日志

# 📝 输出文件
cat output/stock_000063.txt           # 查看股票推送
cat output/gold_price.txt             # 查看黄金推送

# 🔧 配置编辑
vim config/stocks_config.json         # 编辑股票配置
vim config/feishu_config.json         # 编辑飞书配置

# 📚 Git 操作
git status
git add -A
git commit -m "feat: 描述你的改动"
git push origin main
```

---

## 📋 推送时间表（周一至周五）

| 时间 | 类型 | 说明 |
|------|------|------|
| 9:30 | 股价推送 | 开盘推送 |
| 10:00 | 股价推送 | 定时推送 |
| 10:30 | - | - |
| 11:00 | 股价推送 | 定时推送 |
| 11:30 | - | - |
| 13:00 | 股价推送 | 下午开盘 |
| 13:30 | 股价推送 | 定时推送 |
| 14:00 | 股价推送 | 定时推送 |
| 14:30 | 股价推送 | 定时推送 |
| 15:00 | 股价推送 | 收盘推送 |
| 15:30 | **预测推送** | **每日预测报告** |

**共 7 次股价推送 + 1 次预测推送/交易日**

---

## ⚠️ 注意事项

1. **交易时间** - 推送仅在交易日（周一至周五 9:30-15:00）执行
2. **数据延迟** - 行情数据可能有 1-2 分钟延迟
3. **网络请求** - 确保服务器可访问外网
4. **飞书配置** - 确保飞书应用权限正确
5. **投资风险提示** - 数据仅供参考，不构成投资建议

---

## 📝 更新日志

### v3.0 (2026-03-11) - Sprint 3
- ✅ 多股票支持（配置文件管理）
- ✅ 飞书推送优化（重试机制）
- ✅ 股价预警 Cron 配置（一键安装脚本）
- ✅ Web 界面股票配置管理（添加/删除/启用/禁用）
- ✅ 预测推送功能（技术指标 + 趋势预测）

### v2.0 (2026-03-10)
- ✅ 完整实现公告、新闻、研报、财务数据模块
- ✅ 使用 SQLite 存储历史数据
- ✅ Web 界面上线
- ✅ 股价实时提醒

### v1.0 (2026-03-10)
- ✅ 初始版本
- ✅ 接入腾讯财经真实行情 API

---

## 🎯 下一步计划

### 待扩展功能
- [ ] 更多股票数据源接入
- [ ] 重大事件实时预警
- [ ] 邮件/短信通知
- [ ] 数据可视化图表增强
- [ ] 用户登录认证
- [ ] 数据导出（CSV/Excel）
- [ ] 移动端适配优化
- [ ] 自动化测试

---

## 📚 更多文档

| 文档 | 说明 |
|------|------|
| [⚡ QUICKSTART.md](QUICKSTART.md) | 5 分钟快速上手 |
| [📦 DEPLOYMENT.md](DEPLOYMENT.md) | 部署指南 |
| [📁 PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | 项目结构 |
| [📝 CONTRIBUTING.md](CONTRIBUTING.md) | 贡献指南 |
| [📋 CHANGELOG.md](CHANGELOG.md) | 更新日志 |
| [🗺️ ROADMAP.md](ROADMAP.md) | 版本路线图 |

---

## 📄 许可证

MIT License

---

## 👤 开发者

- **开发:** Jerry
- **产品:** Tom
- **测试:** 派大星

**GitHub:** https://github.com/yys-jack/stock-monitor-system

**最后更新:** 2026-03-28

---

🤖 **有问题？欢迎提交 Issue 或 PR！**
