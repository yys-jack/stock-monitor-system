# 量化交易模拟盘使用指南

## 功能概述

量化交易模拟盘提供一个虚拟交易环境，让你可以在不承担真实风险的情况下练习股票交易和测试交易策略。

### 核心功能

| 功能 | 说明 |
|------|------|
| 💰 模拟账户 | 初始资金 ¥100,000 虚拟资金 |
| 📈 买卖交易 | 支持买入/卖出委托 |
| 📋 订单管理 | 委托、撤单、状态跟踪 |
| 💼 持仓管理 | 成本核算、盈亏计算 |
| 📊 成交记录 | 完整的成交历史 |
| 🤖 自动交易 | 基于预测信号自动下单 |
| 🛑 止盈止损 | 自动止盈止损控制 |

---

## 快速开始

### 1. 启动 Web 服务

```bash
cd /home/yy/PyCharmMiscProject/stock-monitor-system
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：http://localhost:8000/trading

### 2. 命令行模式

```bash
python3 scripts/paper_trading.py
```

---

## 使用方法

### Web 界面

1. **查看账户概览**
   - 总资产、可用资金、持仓市值
   - 累计盈亏、收益率

2. **买入股票**
   - 点击"交易"标签
   - 输入股票代码、名称、价格、数量
   - 点击"买入"提交委托

3. **卖出股票**
   - 点击"交易"标签
   - 输入要卖出的股票信息
   - 点击"卖出"提交委托

4. **查看持仓**
   - 点击"持仓"标签
   - 查看每只股票的成本价、当前价、盈亏

5. **查看订单**
   - 点击"订单"标签
   - 查看委托状态
   - 可以撤销待成交订单

6. **查看成交**
   - 点击"成交"标签
   - 查看历史成交记录

### 命令行模式

```
==================================================
📊 量化交易模拟盘
==================================================
1. 查看账户信息
2. 查看持仓
3. 查看订单
4. 买入股票
5. 卖出股票
6. 撤销订单
7. 生成交易信号
8. 执行自动交易
9. 重置账户
0. 退出
==================================================
```

---

## API 接口

### RESTful API

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/trading/account` | GET | 获取账户信息 |
| `/api/trading/position` | GET | 获取持仓列表 |
| `/api/trading/order` | GET | 获取订单列表 |
| `/api/trading/order` | POST | 下单委托 |
| `/api/trading/order/{id}` | DELETE | 撤销订单 |
| `/api/trading/fill` | GET | 获取成交记录 |
| `/api/trading/signal` | POST | 生成交易信号 |
| `/api/trading/auto` | POST | 执行自动交易 |
| `/api/trading/summary` | GET | 获取交易汇总 |

### 示例

```bash
# 获取账户信息
curl http://localhost:8000/api/trading/account

# 买入股票
curl -X POST http://localhost:8000/api/trading/order \
  -H "Content-Type: application/json" \
  -d '{
    "stock_code": "000063",
    "stock_name": "中兴通讯",
    "side": "BUY",
    "price": 37.50,
    "quantity": 100
  }'

# 查看持仓
curl http://localhost:8000/api/trading/position
```

---

## 配置说明

### 配置文件：`config/trading_config.json`

```json
{
  "paper_trading": {
    "initial_capital": 100000,        // 初始资金
    "commission_rate": 0.0003,        // 佣金比例（万分之三）
    "stamp_duty_rate": 0.001,         // 印花税（千分之一，仅卖出）
    "max_position_pct": 0.3,          // 单只股票最大仓位（30%）
    "stop_loss_pct": -10.0,           // 止损比例（-10%）
    "take_profit_pct": 20.0,          // 止盈比例（20%）
    "min_buy_amount": 1000            // 最小买入金额
  },
  "auto_trading": {
    "enabled": false,                 // 是否启用自动交易
    "signal_confidence_threshold": 70, // 信号置信度阈值
    "check_interval_minutes": 30,     // 检查间隔（分钟）
    "max_orders_per_cycle": 5         // 每轮最大订单数
  }
}
```

---

## 自动交易

### 启用自动交易

1. 编辑配置文件 `config/trading_config.json`
2. 设置 `"enabled": true`
3. 配置股票列表

### 运行自动交易

```bash
# 命令行模式选择选项 8
python3 scripts/paper_trading.py
# 选择 8. 执行自动交易

# 或通过 API
curl -X POST http://localhost:8000/api/trading/auto \
  -H "Content-Type: application/json" \
  -d '{"enabled": true, "max_orders": 5}'
```

### 交易逻辑

自动交易基于现有预测功能生成信号：

1. **买入信号**: 预测"强烈买入"且置信度 > 70%
2. **卖出信号**: 预测"强烈卖出"或置信度 < 40%
3. **止盈止损**: 自动监控持仓盈亏

---

## 交易规则

### 买入规则
- 数量必须是 100 股的整数倍
- 需要足够的可用资金
- 单只股票不超过最大仓位限制

### 卖出规则
- 必须有足够持仓
- 卖出后资金立即可用

### 费用计算
- **佣金**: 成交金额的 0.03%，最低 5 元
- **印花税**: 成交金额的 0.1%（仅卖出收取）

### 撮合逻辑
- **限价单**: 价格满足条件时成交
  - 买入：市价 <= 限价
  - 卖出：市价 >= 限价
- **市价单**: 按当前价格立即成交

---

## 注意事项

1. **模拟盘 ≠ 实盘**
   - 不考虑流动性冲击
   - 假设限价单必然成交
   - 无滑点影响

2. **数据延迟**
   - 使用公开行情数据
   - 非交易所实时数据

3. **仅供参考**
   - 不构成投资建议
   - 实盘风险更大

---

## 故障排除

### 问题：无法创建订单

**原因**: 数据库表结构问题

**解决**:
```bash
# 删除旧数据库
rm data/paper_trading.db

# 重启服务
uvicorn app.main:app --reload
```

### 问题：预测功能失败

**原因**: 需要安装 scikit-learn

**解决**:
```bash
pip install scikit-learn
```

### 问题：API 返回 404

**原因**: 路由未注册

**解决**: 确保 `app/main.py` 中包含 `trading_router` 注册

---

**最后更新**: 2026-04-11
