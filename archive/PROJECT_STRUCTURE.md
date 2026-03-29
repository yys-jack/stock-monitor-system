# 📁 项目结构

```
stock-monitor-system/
├── app.py                          # Flask Web 应用入口
├── pyproject.toml                  # Python 项目配置
├── Makefile                        # 常用命令
├── requirements.txt                # 依赖列表
├── README.md                       # 项目说明
│
├── config/                         # 配置文件
│   ├── stocks_config.json          # 股票配置
│   ├── gold_config.json            # 黄金配置
│   └── feishu_config.json          # 飞书配置
│
├── scripts/                        # 核心脚本
│   ├── multi_stocks_monitor.py     # 多股票监控
│   ├── gold_monitor.py             # 黄金监控
│   ├── stock_predictor.py          # 股票预测
│   ├── prediction_push.py          # 预测推送
│   ├── price_alert_monitor.py      # 价格预警
│   ├── logging_config.py           # 日志配置
│   ├── config_loader.py            # 配置加载器
│   └── tests/                      # 单元测试
│
├── webapp/                         # Web 应用
│   ├── routes/                     # 路由
│   ├── services/                   # 业务逻辑
│   ├── utils/                      # 工具函数
│   └── templates/                  # HTML 模板
│
├── data/                           # 数据存储
├── logs/                           # 日志目录
├── output/                         # 输出目录
└── venv/                           # Python 虚拟环境
```

## 📄 文档说明

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目说明和快速开始 |
| [QUICKSTART.md](QUICKSTART.md) | 5 分钟上手指南 |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 部署指南 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献指南 |
| [CHANGELOG.md](CHANGELOG.md) | 版本历史 |
| [ROADMAP.md](ROADMAP.md) | 版本路线图 |

---

_详细文档请查看各文件说明。_
