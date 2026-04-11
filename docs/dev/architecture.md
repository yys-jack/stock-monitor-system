# 架构说明

## 系统架构

```
用户请求 → FastAPI (app/main.py)
         ↓
    API Router (app/api/api.py)
         ↓
    Service Layer (src/*.py)     ← 统一服务层
         ↓
    外部 API (腾讯财经，AkShare, 飞书)
```

## 项目结构

```
stock-monitor-system/
├── app/                      # FastAPI 应用
│   ├── main.py               # 应用入口
│   ├── api/                  # API 路由（拆分为独立模块）
│   │   ├── api.py            # 路由聚合
│   │   ├── stock_routes.py   # 股票行情路由
│   │   ├── predict_routes.py # 预测路由
│   │   └── config_routes.py  # 配置管理路由
│   ├── core/                 # 核心配置
│   ├── models/               # Pydantic 模型
│   └── templates/            # HTML 模板
│
├── src/                      # 核心服务模块（唯一服务层）
│   ├── stock_service.py      # 股票服务
│   ├── gold_service.py       # 黄金服务
│   ├── predictor.py          # 股票预测器
│   ├── feishu.py             # 飞书推送
│   └── trading/              # 量化交易模拟盘
│
├── scripts/                  # 监控脚本（使用 src/ 服务）
├── config/                   # 配置文件
├── archive/                  # 归档代码
│   └── webapp-old/           # 旧 Flask 应用
└── docs/                     # 文档
```

## 核心模块

### 配置管理

- **Pydantic Settings**: `app/core/config.py` - 应用配置（单例模式）
- **JSON 配置文件**: `config/*.json` - 业务配置
- **配置加载器**: `src/config_loader.py` - 加载/保存 JSON 配置

### 服务层设计

- `src/` 目录包含可复用的核心服务（唯一服务层）
- `app/services/` 已删除，统一使用 `src/`
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
