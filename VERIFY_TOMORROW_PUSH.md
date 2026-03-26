# 📋 明日推送验证指南

**创建时间:** 2026-03-26 15:35  
**目的:** 验证股票监控推送是否正常工作

---

## ✅ 已完成操作

### 1. 日志文件清理
```bash
# 备份旧日志
mv logs/push_cron.log logs/push_cron.log.backup.20260326

# 创建新日志文件
touch logs/push_cron.log
```

### 2. 验证脚本创建
- 位置：`scripts/verify_push.sh`
- 权限：已设置为可执行 (chmod +x)
- 用途：快速检查推送状态

### 3. Crontab 配置确认
```bash
# 股票推送 - 交易日每 30 分钟
30 9-11 * * 1-5  → 9:30, 10:30, 11:30
0 10-11 * * 1-5  → 10:00, 11:00
0,30 13-14 * * 1-5 → 13:00, 13:30, 14:00, 14:30
0 15 * * 1-5 → 15:00
```

---

## 🔍 明日验证步骤 (2026-03-27)

### 方法 A: 运行验证脚本（推荐）
```bash
cd /home/yy/.openclaw/workspace-partrickstar/stock-monitor-system
./scripts/verify_push.sh
```

### 方法 B: 手动检查

#### 1. 检查日志文件
```bash
ls -lh logs/push_cron.log
tail -30 logs/push_cron.log
```

**预期结果：**
- 日志文件大小 > 0
- 包含 `🦞 多股票监控` 和 `✅ 飞书推送成功` 记录

#### 2. 检查输出文件
```bash
ls -lth output/stock_*.txt | head -5
```

**预期结果：**
- 最新的股票输出文件时间戳为今天

#### 3. 检查 Cron 执行记录
```bash
grep "multi_stocks_monitor.py" /var/log/syslog | tail -10
```

**预期结果：**
- 显示今天的 cron 执行记录

#### 4. 检查飞书消息
- 打开飞书
- 查看是否收到股票推送消息

---

## 📅 推送时间表（交易日）

| 时间 | Cron 表达式 | 预期推送 |
|------|-----------|---------|
| 09:30 | `30 9-11 * * 1-5` | ✅ |
| 10:00 | `0 10-11 * * 1-5` | ✅ |
| 10:30 | `30 9-11 * * 1-5` | ✅ |
| 11:00 | `0 10-11 * * 1-5` | ✅ |
| 11:30 | `30 9-11 * * 1-5` | ✅ |
| 13:00 | `0,30 13-14 * * 1-5` | ✅ |
| 13:30 | `0,30 13-14 * * 1-5` | ✅ |
| 14:00 | `0,30 13-14 * * 1-5` | ✅ |
| 14:30 | `0,30 13-14 * * 1-5` | ✅ |
| 15:00 | `0 15 * * 1-5` | ✅ |

**合计：** 每天 10 次推送（周一至周五）

---

## ⚠️ 常见问题排查

### 问题 1: 日志文件为空
```bash
# 检查 cron 服务状态
systemctl status cron

# 检查 syslog 中的执行记录
grep "multi_stocks" /var/log/syslog | tail -10
```

### 问题 2: 脚本执行失败
```bash
# 手动测试脚本
cd /home/yy/.openclaw/workspace-partrickstar/stock-monitor-system
source venv/bin/activate
python3 scripts/multi_stocks_monitor.py
```

### 问题 3: 飞书推送失败
```bash
# 检查飞书配置
cat config/feishu_config.json

# 检查配置是否启用
# "enabled": true
```

---

## 📊 验证结果记录

### 2026-03-27 (明天)

**验证时间:** _________

**验证人:** _________

**检查结果:**
- [ ] 日志文件有更新
- [ ] 包含成功的推送记录
- [ ] 飞书收到推送消息
- [ ] 输出文件时间戳正确

**备注:**
```
_________________________________
_________________________________
```

---

## 📝 相关文档

- [CHANGELOG_CRON_FIX.md](CHANGELOG_CRON_FIX.md) - Crontab 路径修复记录
- [PUSH_INVESTIGATION_REPORT.md](PUSH_INVESTIGATION_REPORT.md) - 推送排查报告

---

**最后更新:** 2026-03-26 15:35
