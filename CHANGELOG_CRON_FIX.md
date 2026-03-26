# Crontab 路径修复记录

## 问题描述

股票监控推送 crontab 配置中脚本路径错误，导致 cron 任务执行失败。

### 错误现象

```
python3: can't open file '/home/yy/.openclaw/workspace-partrickstar/stock-monitor-system/multi_stocks_monitor.py': [Errno 2] No such file or directory
```

### 根本原因

脚本实际位于 `scripts/multi_stocks_monitor.py`，但 crontab 中配置的路径是项目根目录下的 `multi_stocks_monitor.py`。

## 修复内容

### 修复前
```bash
# 股票价格推送 - 交易时间每 30 分钟 (v2)
30 9-11 * * 1-5 /bin/bash -c 'cd /home/yy/.openclaw/workspace-partrickstar/stock-monitor-system && source venv/bin/activate && python3 /home/yy/.openclaw/workspace-partrickstar/stock-monitor-system/multi_stocks_monitor.py' >> logs/push_cron.log 2>&1
```

### 修复后
```bash
# 股票价格推送 - 交易时间每 30 分钟 (v3 - 修复路径)
30 9-11 * * 1-5 cd /home/yy/.openclaw/workspace-partrickstar/stock-monitor-system && source venv/bin/activate && python3 scripts/multi_stocks_monitor.py >> logs/push_cron.log 2>&1
```

## 推送时间安排

### 股票推送（交易日）
- **上午**: 9:30, 10:00, 10:30, 11:00, 11:30（每 30 分钟）
- **下午**: 13:00, 13:30, 14:00, 14:30, 15:00（每 30 分钟）

### 黄金推送（交易日）
- **上午**: 9:30, 10:30, 11:30
- **下午**: 13:30, 14:30

## 验证结果

```bash
$ cd /home/yy/.openclaw/workspace-partrickstar/stock-monitor-system && source venv/bin/activate && python3 scripts/multi_stocks_monitor.py
🦞 多股票监控 - 2026-03-26 13:33:19
============================================================
[INFO] 配置股票数量：4
[INFO] 启用股票数量：4
[INFO] 获取 中兴通讯 (000063) 股价...
  ✅ 当前价：32.66 元 (-2.36%)
...
[INFO] ✅ 飞书推送成功！
```

## 提交记录

- 修复 crontab 路径配置
- 简化 crontab 命令格式（移除不必要的 `/bin/bash -c`）

---
**修复日期:** 2026-03-26  
**修复人:** partrickstar
