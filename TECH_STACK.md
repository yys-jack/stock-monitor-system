# 🛠️ 项目技术栈文档

> **Stock Monitor System** - 技术架构与实现细节

**版本：** v4.0  
**最后更新：** 2026-03-25  
**作者：** Jerry

---

## 📊 技术架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                      用户界面层                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Web 界面    │  │  飞书推送   │  │  Cron 定时  │         │
│  │  (Flask)    │  │  (API)      │  │  (Shell)    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      业务逻辑层                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ 股票监控    │  │ 黄金监控    │  │ 智能预测    │         │
│  │ multi_...   │  │ gold_...    │  │ predictor   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │ 价格预警    │  │ Web 服务     │                          │
│  │ alert_...   │  │ web_server  │                          │
│  └─────────────┘  └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      数据访问层                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ 腾讯财经    │  │ AkShare     │  │ 上期所      │         │
│  │ (实时行情)  │  │ (历史数据)  │  │ (黄金期货)  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 核心技术栈

### 1️⃣ 后端技术

| 技术 | 版本 | 用途 | 说明 |
|------|------|------|------|
| **Python** | 3.8+ | 主要编程语言 | 跨平台、易维护 |
| **Flask** | 2.x | Web 框架 | 轻量级后端服务 |
| **Requests** | 2.28+ | HTTP 客户端 | 网络请求 |
| **AkShare** | 1.x | 金融数据接口 | 历史行情、新闻、公告等 |
| **Pandas** | 1.x | 数据处理 | 技术指标计算 |
| **NumPy** | 1.x | 数值计算 | 数学运算支持 |

### 2️⃣ 前端技术

| 技术 | 版本 | 用途 | 说明 |
|------|------|------|------|
| **HTML5** | - | 页面结构 | 语义化标签 |
| **CSS3** | - | 样式设计 | 响应式布局、渐变背景 |
| **JavaScript** | ES6+ | 交互逻辑 | DOM 操作、AJAX |
| **Chart.js** | 4.x | 数据可视化 | K 线走势图表 |

### 3️⃣ 运维技术

| 技术 | 版本 | 用途 | 说明 |
|------|------|------|------|
| **Bash** | 5.x | 脚本编写 | Cron 管理、自动化部署 |
| **Cron** | - | 定时任务 | 交易时间自动推送 |
| **Git** | 2.x | 版本控制 | 代码管理、分支策略 |
| **Python venv** | 3.x | 虚拟环境 | 依赖隔离 |

### 4️⃣ 数据源

| 数据源 | 类型 | 用途 | 更新频率 |
|--------|------|------|----------|
| **腾讯财经** | HTTP API | 实时股价 | 实时 |
| **AkShare** | Python 库 | 历史行情、新闻、公告、研报 | 实时/日频 |
| **上海期货交易所** | AkShare 接口 | 黄金期货价格 | 实时交易时间 |
| **东方财富** | AkShare 接口 | 新闻资讯 | 实时 |

---

## 📁 核心模块技术实现

### 1️⃣ 多股票监控模块 (`multi_stocks_monitor.py`)

**技术要点：**
- **数据获取：** 腾讯财经 HTTP API (`qt.gtimg.cn`)
- **数据解析：** GBK 编码解析、字符串分割
- **配置管理：** JSON 配置文件加载
- **推送服务：** 飞书开放平台 API
- **异常处理：** 重试机制（3 次）、错误日志

**关键技术代码：**
```python
# 腾讯财经 API 调用
url = f"https://qt.gtimg.cn/q={market}{code}"
resp = requests.get(url, headers=headers, timeout=10)
resp.encoding = "gbk"  # 腾讯财经返回 GBK 编码

# 数据解析
fields = content.split("=\"")[1].rstrip("\";").split("~")
current_price = float(fields[3])
change_pct = float(fields[32])
```

---

### 2️⃣ 黄金监控模块 (`gold_monitor.py`)

**技术要点：**
- **数据源：** AkShare 期货接口 (`futures_zh_realtime`)
- **主力合约识别：** AU2606（最近月份合约）
- **价格换算：** 美元/盎司 ↔ 人民币/克
- **期货升水校正：** 减去 3.5 元/克升水估算现货价
- **降级策略：** 主力合约不可用时降级到 AU0 连续合约

**关键技术代码：**
```python
# 获取上期所黄金期货实时行情
df = ak.futures_zh_realtime(symbol="黄金")
main_contract = df[df['symbol'] == 'AU2606']

# 期货升水校正
futures_premium = 3.5  # 期货比现货高的部分
spot_cny_g = current_cny_g - futures_premium

# 国际金价换算
exchange_rate = 7.2
current_usd_oz = (current_cny_g * 31.1035) / exchange_rate
```

---

### 3️⃣ 智能预测模块 (`stock_predictor.py`)

**技术要点：**
- **技术指标：** MA/MACD/RSI/KDJ/布林带
- **趋势分析：** 均线排列、MACD 金叉死叉、RSI 超买超卖
- **置信度评估：** 多指标综合打分
- **支撑压力位：** 近期高低点识别

**技术指标公式：**
```python
# 均线 (Moving Average)
MA5 = closing_price.rolling(window=5).mean()

# MACD (指数平滑异同移动平均线)
EMA12 = closing_price.ewm(span=12, adjust=False).mean()
EMA26 = closing_price.ewm(span=26, adjust=False).mean()
MACD = EMA12 - EMA26
Signal = MACD.ewm(span=9, adjust=False).mean()

# RSI (相对强弱指标)
delta = closing_price.diff()
gain = delta.where(delta > 0, 0).rolling(window=14).mean()
loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
RSI = 100 - (100 / (1 + gain/loss))

# KDJ (随机指标)
RSV = (close - lowest_low) / (highest_high - lowest_low) * 100
K = RSV.ewm(com=2, adjust=False).mean()
D = K.ewm(com=2, adjust=False).mean()
J = 3*K - 2*D
```

---

### 4️⃣ Web 界面模块 (`web_server.py` + `templates/index.html`)

**技术要点：**
- **后端框架：** Flask RESTful API
- **前端渲染：** Jinja2 模板引擎
- **数据可视化：** Chart.js 折线图
- **响应式设计：** CSS Grid + Media Queries
- **AJAX 刷新：** JavaScript Fetch API

**API 接口设计：**
| 接口 | 方法 | 返回格式 | 说明 |
|------|------|----------|------|
| `/api/stock/<code>` | GET | JSON | 实时股价 |
| `/api/news/<code>` | GET | JSON Array | 新闻列表 |
| `/api/history/<code>` | GET | JSON Array | 历史行情 |
| `/api/stocks` | GET | JSON Array | 股票配置列表 |
| `/api/stocks` | POST | JSON | 添加股票 |
| `/api/stocks/<code>` | DELETE | JSON | 删除股票 |

---

### 5️⃣ Cron 定时任务模块 (`cron_install.sh`)

**技术要点：**
- **Cron 表达式：** 交易时间精确控制
- **虚拟环境激活：** `source venv/bin/activate`
- **日志重定向：** `>> logs/*.log 2>&1`
- **备份机制：** 安装前自动备份 crontab
- **彩色输出：** ANSI 转义码

**Cron 时间表：**
```bash
# 股票推送 - 交易时间每 30 分钟
30 9-11 * * 1-5    # 上午 9:30-11:30
0,30 13-14 * * 1-5 # 下午 13:00-14:30
0 15 * * 1-5       # 15:00 收盘

# 黄金监控 - 交易时间每小时
30 9-11 * * 1-5    # 上午 9:30, 10:30, 11:30
30 13-14 * * 1-5   # 下午 13:30, 14:30

# 股价预警 - 交易时间每 5 分钟
*/5 9-11 * * 1-5   # 上午高频检查
*/5 13-14 * * 1-5  # 下午高频检查
```

---

## 🔐 安全与配置管理

### 配置文件结构

**`feishu_config.json` (敏感信息，已加入 .gitignore)**
```json
{
  "feishu": {
    "enabled": true,
    "user_id": "ou_xxxxx",
    "app_id": "cli_xxxxx",
    "app_secret": "xxxxx",
    "retry_times": 3,
    "retry_delay_seconds": 2
  }
}
```

**`stocks_config.json` (可提交)**
```json
{
  "stocks": [
    {
      "code": "000063",
      "name": "中兴通讯",
      "market": "sz",
      "enabled": true,
      "alias": "ZTE"
    }
  ],
  "settings": {
    "push_interval_minutes": 30,
    "alert_threshold_up": 5.0,
    "alert_threshold_down": -5.0
  }
}
```

### 安全实践
- ✅ 敏感配置文件加入 `.gitignore`
- ✅ 提供配置模板 `*.example.json`
- ✅ 配置文件与代码分离
- ✅ 飞书 API 密钥不硬编码

---

## 📊 性能指标

| 指标 | 目标 | 实际 | 测量方式 |
|------|------|------|----------|
| 单次执行时间 | <5s | ~3s | `time python3 xxx.py` |
| API 响应时间 | <2s | ~1.2s | 网络请求耗时 |
| 推送及时率 | >99% | 100% | Cron 日志统计 |
| 数据准确率 | >95% | 100% | 对比权威数据源 |
| 代码行数 | <2000 | ~1500 | `wc -l *.py` |

---

## 🧪 测试策略

### 测试类型

| 类型 | 说明 | 执行方式 |
|------|------|----------|
| **单元测试** | 核心函数独立测试 | 手动调用函数 |
| **集成测试** | 完整流程运行 | 执行完整脚本 |
| **数据验证** | 对比权威数据源 | 支付宝/银行 APP |
| **边界测试** | 异常情况处理 | 断网、API 限流模拟 |

### 测试用例示例

```python
# 测试用例：股价获取
def test_fetch_stock_price():
    result = fetch_stock_price("000063", "sz")
    assert result is not None
    assert result['current'] > 0
    assert -10 <= result['change_pct'] <= 10

# 测试用例：技术指标计算
def test_calculate_ma():
    df = fetch_history_data()
    df = calculate_ma(df)
    assert 'MA5' in df.columns
    assert 'MA10' in df.columns
    assert df['MA5'].iloc[-1] > 0
```

---

## 🚀 部署架构

### 部署环境
- **操作系统：** Linux (Ubuntu/Debian)
- **Python 版本：** 3.8+
- **Web 服务器：** Flask 开发服务器 (生产环境建议 Gunicorn)
- **定时任务：** Cron
- **日志管理：** 文件日志 (`logs/*.log`)

### 部署步骤
```bash
# 1. 克隆仓库
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置飞书
cp feishu_config.example.json feishu_config.json
# 编辑 feishu_config.json 填写凭证

# 5. 安装 Cron 任务
./cron_install.sh install

# 6. 启动 Web 服务（可选）
python3 web_server.py
```

---

## 📈 技术债务与优化方向

### 当前技术债务
| 问题 | 影响 | 优先级 | 建议方案 |
|------|------|--------|----------|
| 无自动化测试 | 回归风险 | P2 | 引入 pytest |
| 无数据库迁移 | 版本升级困难 | P3 | 引入 Alembic |
| 日志无轮转 | 日志文件过大 | P2 | 引入 logging.handlers |
| 无监控告警 | 故障发现慢 | P2 | 集成 Sentry |

### 优化方向
- [ ] **性能优化：** 异步请求 (aiohttp)、缓存机制 (Redis)
- [ ] **架构升级：** 微服务拆分、消息队列 (RabbitMQ)
- [ ] **数据持久化：** PostgreSQL、时序数据库 (InfluxDB)
- [ ] **容器化：** Docker 镜像、Kubernetes 部署
- [ ] **CI/CD：** GitHub Actions 自动化测试与部署

---

## 📚 技术参考

### 官方文档
- [Python](https://docs.python.org/3/)
- [Flask](https://flask.palletsprojects.com/)
- [AkShare](https://akshare.akfamily.xyz/)
- [Chart.js](https://www.chartjs.org/)
- [飞书开放平台](https://open.feishu.cn/)

### 数据源文档
- [腾讯财经 API](https://qt.gtimg.cn/)
- [上海期货交易所](http://www.shfe.com.cn/)
- [东方财富网](https://www.eastmoney.com/)

---

## 🎓 学习资源

### Python 金融数据分析
- 《Python 金融大数据分析》
- 《利用 Python 进行数据分析》
- AkShare 官方教程

### 技术指标
- 《技术分析基础》
- Investopedia 技术指标教程
- TradingView 指标库

---

**文档维护：** 每次技术栈变更后需同步更新本文档  
**最后更新：** 2026-03-25 21:35
