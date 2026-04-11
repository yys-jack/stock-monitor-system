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
