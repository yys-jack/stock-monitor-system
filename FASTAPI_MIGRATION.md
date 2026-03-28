# FastAPI 迁移指南

## 概述

本项目已从 Flask 框架迁移到 FastAPI 框架，提供更好的性能、类型安全和 API 文档支持。

## 主要变更

### 1. 项目结构

```
stock-monitor-system/
├── app/                    # FastAPI 应用主目录
│   ├── api/               # API 路由
│   │   ├── api.py        # API 端点
│   │   └── views.py      # 页面视图
│   ├── core/             # 核心配置
│   │   ├── config.py     # 应用配置
│   │   └── middleware.py # 中间件
│   ├── models/           # Pydantic 模型
│   │   └── schemas.py    # 数据模型定义
│   ├── services/         # 服务层
│   │   └── feishu_service.py
│   └── main.py           # 应用入口
├── src/                  # 共享服务层 (保留)
├── templates/            # HTML 模板
├── tests/                # 测试用例
└── requirements.txt      # 依赖配置
```

### 2. 依赖更新

**新增:**
- `fastapi>=0.109.0`
- `uvicorn[standard]>=0.27.0`
- `pydantic>=2.5.0`
- `pydantic-settings>=2.1.0`
- `jinja2>=3.1.2`
- `pytest-asyncio>=0.21.0`
- `httpx>=0.25.0`

**移除:**
- `Flask>=3.0.0`

### 3. API 端点

所有原有 API 端点已完全迁移，保持向后兼容：

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/stock/{code}` | GET | 获取股票实时数据 |
| `/api/news/{code}` | GET | 获取新闻 |
| `/api/history/{code}` | GET | 获取历史行情 |
| `/api/overview` | GET | 获取概览数据 |
| `/api/predict/{code}` | GET | 获取预测数据 |
| `/api/stocks` | GET/POST | 股票配置管理 |
| `/api/stocks/{code}` | DELETE | 删除股票 |
| `/api/stocks/{code}/toggle` | POST | 切换状态 |
| `/` | GET | 首页 |
| `/stock/{code}` | GET | 股票详情页 |

### 4. 新特性

- **Swagger UI**: 访问 `/docs` 查看交互式 API 文档
- **ReDoc**: 访问 `/redoc` 查看备用文档
- **类型验证**: 所有请求/响应使用 Pydantic 模型验证
- **异步处理**: API 端点使用 async/await
- **请求日志**: 自动记录所有请求的处理时间
- **CORS 支持**: 配置跨域资源共享

### 5. 运行应用

```bash
# 安装依赖
pip install -r requirements.txt

# 开发模式运行
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式运行
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 6. 运行测试

```bash
# 运行所有测试
pytest tests/test_fastapi.py -v

# 运行特定测试
pytest tests/test_fastapi.py::TestStockAPI::test_get_stock -v
```

## 兼容性说明

- `src/` 模块保持不变，作为共享服务层
- 所有 API 响应格式与 Flask 版本完全兼容
- 配置文件格式不变

## 迁移日期

2026-03-29
