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
