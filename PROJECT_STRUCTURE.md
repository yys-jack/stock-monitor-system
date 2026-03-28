# 📁 项目结构说明

```
stock-monitor-system/
├── 📄 核心文件
│   ├── app.py                          # Flask Web 应用入口
│   ├── requirements.txt                # Python 依赖列表
│   ├── pyproject.toml                  # 现代化 Python 项目配置
│   ├── Makefile                        # 常用命令快捷方式
│   └── README.md                       # 项目说明文档
│
├── 📁 config/                          # 配置文件目录
│   ├── stocks_config.json              # 股票配置（代码、名称、市场）
│   ├── stocks_config.example.json      # 股票配置示例
│   ├── gold_config.json                # 黄金监控配置
│   ├── feishu_config.json              # 飞书推送配置（敏感信息）
│   └── feishu_config.example.json      # 飞书配置示例
│
├── 📁 scripts/                         # 核心脚本目录
│   ├── multi_stocks_monitor.py         # 多股票价格监控
│   ├── gold_monitor.py                 # 黄金价格监控
│   ├── stock_predictor.py              # 股票预测（技术指标分析）
│   ├── prediction_push.py              # 预测结果推送
│   ├── price_alert_monitor.py          # 价格异常预警
│   ├── logging_config.py               # 统一日志配置 ⭐新增
│   ├── config_loader.py                # 统一配置加载器 ⭐新增
│   ├── verify_predictions.py           # 预测准确率验证
│   ├── install_crontab.sh              # Cron 任务安装脚本
│   ├── verify_push.sh                  # 推送验证脚本
│   └── tests/                          # 单元测试目录 ⭐新增
│       ├── __init__.py
│       ├── test_config_loader.py       # 配置加载器测试
│       └── test_stock_fetcher.py       # 股价获取测试
│
├── 📁 webapp/                          # Web 应用目录
│   ├── __init__.py
│   ├── routes/                         # 路由处理
│   │   ├── __init__.py
│   │   ├── api.py                      # API 接口
│   │   └── views.py                    # 页面视图
│   ├── services/                       # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── stock_service.py            # 股票服务
│   │   ├── gold_service.py             # 黄金服务
│   │   └── predictor.py                # 预测服务
│   ├── utils/                          # 工具函数
│   │   ├── __init__.py
│   │   ├── config_loader.py            # 配置加载工具
│   │   └── feishu.py                   # 飞书工具
│   └── templates/                      # HTML 模板
│
├── 📁 data/                            # 数据存储目录
│   └── prediction_history.json         # 预测历史记录
│
├── 📁 logs/                            # 日志目录（.gitignore）
│
├── 📁 output/                          # 输出文件目录（.gitignore）
│
├── 📁 venv/                            # Python 虚拟环境（.gitignore）
│
├── 🐳 Docker 相关
│   ├── Dockerfile                      # Docker 镜像构建文件 ⭐新增
│   └── .dockerignore                   # Docker 忽略文件 ⭐新增
│
├── 🔧 CI/CD 相关
│   └── .github/
│       └── workflows/
│           └── ci.yml                  # GitHub Actions 配置 ⭐新增
│
├── 📚 文档目录
│   ├── QUICKSTART.md                   # 快速开始指南 ⭐新增
│   ├── CONTRIBUTING.md                 # 贡献指南 ⭐新增
│   ├── DEPLOYMENT.md                   # 部署指南 ⭐新增
│   ├── CHANGELOG.md                    # 更新日志 ⭐新增
│   ├── TECH_STACK.md                   # 技术栈说明
│   ├── AGILE_DEVELOPMENT.md            # 敏捷开发流程
│   ├── GIT_WORKFLOW.md                 # Git 工作流
│   ├── TESTING.md                      # 测试指南
│   ├── ROADMAP.md                      # 版本路线图
│   ├── POSTMORTEM_20260326.md          # 事故复盘报告
│   └── PUSH_INVESTIGATION_REPORT.md    # 推送问题调查报告
│
├── ⚙️ 配置文件
│   ├── .gitignore                      # Git 忽略规则
│   ├── .env.example                    # 环境变量模板 ⭐新增
│   ├── .pre-commit-config.yaml         # Pre-commit 钩子配置 ⭐新增
│   └── LICENSE                         # MIT 许可证 ⭐新增
│
└── 📝 说明文件
    └── PROJECT_STRUCTURE.md            # 本文件
```

---

## 🆕 新增文件说明

### 项目管理
- **pyproject.toml**: 现代化 Python 项目配置，支持 pip install -e .
- **Makefile**: 提供 make install/test/lint/clean 等快捷命令
- **LICENSE**: MIT 开源许可证

### 开发工具
- **logging_config.py**: 统一日志配置模块，支持控制台和文件输出
- **config_loader.py**: 统一配置加载器，支持缓存和环境变量
- **scripts/tests/**: 单元测试目录，包含配置和股价测试

### 部署支持
- **Dockerfile**: Docker 容器化部署支持
- **.dockerignore**: Docker 构建忽略文件
- **.github/workflows/ci.yml**: GitHub Actions CI/CD 流程
- **.env.example**: 环境变量配置模板
- **.pre-commit-config.yaml**: Git 提交前自动检查

### 文档
- **QUICKSTART.md**: 5 分钟快速上手指南
- **CONTRIBUTING.md**: 代码贡献指南
- **DEPLOYMENT.md**: 生产环境部署指南
- **CHANGELOG.md**: 版本更新日志

---

## 📂 目录职责

### config/ - 配置中心
所有配置文件集中管理，敏感信息（飞书凭证）通过 .gitignore 保护

### scripts/ - 核心逻辑
- **监控脚本**: 定时获取股价、黄金价格
- **预测脚本**: 技术指标分析、机器学习预测
- **推送脚本**: 飞书消息推送
- **工具脚本**: 配置加载、日志记录、测试验证

### webapp/ - Web 界面
采用 Flask 蓝图（Blueprint）架构：
- **routes/**: URL 路由和请求处理
- **services/**: 业务逻辑封装
- **utils/**: 通用工具函数
- **templates/**: HTML 页面模板

### data/ - 数据存储
- SQLite 数据库（如使用）
- JSON 文件（预测历史、配置备份）

### logs/ - 日志输出
按日期和模块分类的日志文件

---

## 🎯 模块依赖关系

```
app.py (Web 入口)
├── routes/api.py
│   ├── services/stock_service.py
│   ├── services/predictor.py
│   └── utils/config_loader.py
└── routes/views.py
    └── templates/

scripts/multi_stocks_monitor.py
├── config_loader.py (配置加载)
├── logging_config.py (日志记录)
└── utils/feishu.py (飞书推送)

scripts/stock_predictor.py
├── akshare (数据源)
├── pandas (数据处理)
└── data/prediction_history.json (历史记录)
```

---

## 🔄 数据流

### 股价监控流程
```
定时任务 (Cron)
    ↓
scripts/multi_stocks_monitor.py
    ↓
腾讯财经 API → 股价数据
    ↓
格式化消息 → 飞书推送
    ↓
output/ 保存记录
```

### Web 界面流程
```
用户访问 http://localhost:5000
    ↓
routes/views.py (页面路由)
    ↓
services/stock_service.py (获取数据)
    ↓
templates/ (渲染 HTML)
    ↓
返回页面
```

### 预测流程
```
scripts/prediction_push.py
    ↓
akshare 获取历史数据
    ↓
stock_predictor.py 计算指标 (MA/MACD/RSI/KDJ)
    ↓
生成预测结果
    ↓
保存至 data/prediction_history.json
    ↓
飞书推送
```

---

## 📊 代码统计

| 类别 | 文件数 | 代码行数（约） |
|------|--------|----------------|
| 核心脚本 | 7 | ~2000 行 |
| Web 应用 | 8 | ~800 行 |
| 配置文件 | 5 | ~200 行 |
| 测试文件 | 3 | ~150 行 |
| 文档 | 12 | ~3000 行 |
| **总计** | **35+** | **~6000+ 行** |

---

_最后更新：2026-03-28_
