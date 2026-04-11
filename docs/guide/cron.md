# Cron 定时任务管理

## 统一命令

```bash
# 安装所有任务
./cron_install.sh install

# 查看状态
./cron_install.sh status

# 卸载所有任务
./cron_install.sh uninstall

# 单独安装
./cron_install.sh stocks  # 只安装股票推送
./cron_install.sh gold    # 只安装黄金监控
./cron_install.sh alert   # 只安装股价预警
```

## 推送时间表（交易日）

| 任务 | 时间 | 频率 |
|------|------|------|
| 股票推送 | 9:30-15:00 | 每 30 分钟 |
| 黄金监控 | 9:30-15:00 | 每小时 |
| 股价预警 | 9:30-15:00 | 每 5 分钟 (±5% 阈值) |
| 预测推送 | 15:30 | 每日一次 |

## Cron 表达式详解

### 股票推送

```bash
# 9:30 开盘
30 9 * * 1-5

# 10:00, 10:30, 11:00, 11:30
0,30 10-11 * * 1-5

# 13:00, 13:30, 14:00, 14:30
0,30 13-14 * * 1-5

# 15:00 收盘
0 15 * * 1-5
```

### 黄金监控

```bash
# 每小时 30 分
30 9-11 * * 1-5
30 13-14 * * 1-5
```

### 股价预警

```bash
# 每 5 分钟
*/5 9-11 * * 1-5
*/5 13-14 * * 1-5
0-5/5 15 * * 1-5
```

## 日志查看

```bash
# 股票推送日志
tail -f logs/push_cron.log

# 黄金监控日志
tail -f logs/gold_cron.log

# 股价预警日志
tail -f logs/alert_cron.log
```

## 故障排除

### Cron 任务未执行

1. 检查 Cron 服务状态：
```bash
systemctl status cron
```

2. 查看 Cron 日志：
```bash
grep CRON /var/log/syslog
```

3. 验证 Python 路径：
```bash
which python3
```

### 飞书推送失败

检查 `config/feishu_config.json` 凭证是否正确。
