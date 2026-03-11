# 📈 股票监控系统

> 中兴通讯 (000063) 及多股票监控解决方案 | 实时股价 + 公告新闻 + Web 界面 + 飞书推送

---

## 🎯 功能概览

| 模块 | 功能 | 状态 |
|------|------|------|
| 📊 **单股监控** | 中兴通讯完整监控（行情 + 公告 + 新闻 + 研报 + 财务） | ✅ 就绪 |
| 📈 **多股监控** | 批量监控多只股票，支持配置管理 | ✅ 就绪 |
| ⏰ **股价提醒** | 交易时间每 30 分钟推送实时股价 | ✅ 就绪 |
| 🌐 **Web 界面** | 实时股价、新闻资讯、历史走势图表 | ✅ 就绪 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace-jerry/scripts
pip install -r requirements.txt
```

### 2. 选择使用方式

#### 方式 A: 单股完整监控（中兴通讯）
```bash
python3 zte_monitor.py
```

#### 方式 B: 多股票批量监控
```bash
# 先配置 stocks_config.json
python3 multi_stocks_monitor.py
```

#### 方式 C: 仅股价提醒
```bash
python3 stock_price_alert.py
```

#### 方式 D: Web 界面
```bash
bash start_web.sh
# 访问 http://localhost:5000
```

---

## 📁 文件结构

```
scripts/
├── 核心脚本
│   ├── zte_monitor.py           # 单股完整监控（中兴通讯）
│   ├── multi_stocks_monitor.py  # 多股票批量监控
│   ├── stock_price_alert.py     # 股价实时提醒
│   └── web_server.py            # Web 界面服务器
│
├── 配置文件
│   ├── stocks_config.json       # 多股票配置
│   └── requirements.txt         # Python 依赖
│
├── Web 界面
│   ├── templates/
│   │   └── index.html           # 前端页面
│   └── start_web.sh             # 启动脚本
│
├── 数据存储
│   ├── data/
│   │   └── zte_monitor.db       # SQLite 数据库
│   ├── logs/                    # 运行日志
│   └── output/                  # 推送消息输出
│
└── 文档
    └── README.md                # 本文件
```

---

## 📊 数据源状态

| 数据类型 | 数据源 | 状态 |
|---------|--------|------|
| 📈 **行情** | 腾讯财经 | ✅ **真实数据** |
| 📄 **公告** | 东方财富/巨潮资讯网 | 🔶 模拟数据 |
| 📰 **新闻** | 东方财富搜索 API | 🔶 模拟数据 |
| 🔬 **研报** | 模拟数据 | 🔶 框架就绪 |
| 📊 **财务** | 模拟数据 | 🔶 框架就绪 |

---

## 📋 模块详解

### 1️⃣ 单股完整监控 (`zte_monitor.py`)

**功能：** 中兴通讯全方位监控

**输出内容：**
- 📈 实时行情（昨收、开盘、当前价、涨跌、成交量）
- 📄 新增公告
- 📰 重要新闻
- 🔬 券商研报
- 📊 财务摘要

**配置：** 编辑 `zte_monitor.py` 顶部 `CONFIG` 字典

---

### 2️⃣ 多股票监控 (`multi_stocks_monitor.py`)

**功能：** 批量监控多只股票

**配置文件：** `stocks_config.json`

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
    },
    {
      "code": "000001",
      "name": "平安银行",
      "market": "sz",
      "enabled": true
    }
  ],
  "settings": {
    "push_interval_minutes": 30,
    "push_format": "single"
  }
}
```

**推送格式：**
- `single`: 每只股票独立消息
- `combined`: 所有股票合并为一条消息

---

### 3️⃣ 股价实时提醒 (`stock_price_alert.py`)

**功能：** 交易时间定时推送股价

**推送时间（交易日）：**
| 时段 | 时间点 |
|------|--------|
| 上午 | 9:30, 10:00, 10:30, 11:00, 11:30 |
| 下午 | 13:00, 13:30, 14:00, 14:30, 15:00 |

**配置：** 通过 OpenClaw cron 定时任务调度

---

### 4️⃣ Web 界面 (`web_server.py`)

**功能：** 浏览器访问的监控面板

**特性：**
- ✅ 实时股价（30 秒自动刷新）
- ✅ 新闻资讯列表
- ✅ 历史走势图表（Chart.js）
- ✅ 多股票切换
- ✅ 响应式设计（手机/电脑适配）

**启动：**
```bash
bash start_web.sh
# 访问 http://localhost:5000
```

**API 接口：**
```bash
GET /api/stock/<code>      # 实时股价
GET /api/news/<code>       # 新闻列表
GET /api/history/<code>    # 历史行情
GET /api/overview          # 市场概览
```

---

## ⚙️ 定时任务配置

### 方式 A: OpenClaw Cron

编辑 `~/.openclaw/cron/jobs.json`：

```json
{
  "id": "multi-stocks",
  "name": "多股票监控",
  "schedule": {
    "type": "cron",
    "expressions": [
      "30 9 * * 1-5",
      "0 10 * * 1-5",
      "30 10 * * 1-5",
      "0 11 * * 1-5",
      "30 11 * * 1-5",
      "0 13 * * 1-5",
      "30 13 * * 1-5",
      "0 14 * * 1-5",
      "30 14 * * 1-5",
      "0 15 * * 1-5"
    ],
    "timezone": "Asia/Shanghai"
  },
  "command": ["python3", "~/.openclaw/workspace-jerry/scripts/multi_stocks_monitor.py"]
}
```

### 方式 B: 系统 Cron

```bash
crontab -e
# 添加定时任务
```

---

## 📬 飞书推送

### 方式 1: OpenClaw 内置（默认）

消息输出到 `output/` 目录，由 OpenClaw 自动推送到飞书。

### 方式 2: 直接 Webhook

1. 在飞书群添加机器人
2. 获取 webhook URL
3. 配置到对应脚本的 `CONFIG` 中

---

## 🗄️ 数据存储

**SQLite 数据库：** `data/zte_monitor.db`

**数据表：**
- `announcements` - 公告
- `news` - 新闻
- `market_data` - 行情数据
- `reports` - 研报

**特性：** 自动去重，避免重复推送

---

## 🛠️ 常用命令

```bash
# 查看状态
git status

# 测试单股监控
python3 zte_monitor.py

# 测试多股监控
python3 multi_stocks_monitor.py

# 测试股价提醒
python3 stock_price_alert.py

# 启动 Web 服务
bash start_web.sh

# 查看日志
tail -f logs/multi_stocks.log
tail -f logs/web_server.log

# 查看推送消息
cat output/stock_000063.txt
```

---

## ⚠️ 注意事项

1. **交易日** - 定时任务仅在周一至周五执行
2. **数据延迟** - 行情数据可能有 1-2 分钟延迟
3. **API 变化** - 网站接口更新时需调整代码
4. **robots.txt** - 控制请求频率，避免被封 IP
5. **投资风险提示** - 数据仅供参考，不构成投资建议

---

## 📝 更新日志

### v2.0 (2026-03-10)
- ✅ 完整实现公告、新闻、研报、财务数据模块
- ✅ 使用 SQLite 存储历史数据
- ✅ 多股票监控功能
- ✅ Web 界面上线
- ✅ 股价实时提醒

### v1.0 (2026-03-10)
- ✅ 初始版本
- ✅ 接入腾讯财经真实行情 API

---

## 🎯 下一步计划

### 待扩展功能
- [ ] 接入真实公告 API
- [ ] 接入真实新闻 API
- [ ] 接入真实研报/财务数据 API
- [ ] 重大事件实时预警
- [ ] 邮件/短信通知
- [ ] 数据可视化图表增强
- [ ] 用户登录认证
- [ ] 数据导出（CSV/Excel）

---

🤖 **开发者:** Jerry | **最后更新:** 2026-03-11
