#!/bin/bash
# 股票监控推送验证脚本
# 用于检查 cron 推送是否正常工作

LOGS_DIR="/home/yy/.openclaw/workspace-partrickstar/stock-monitor-system/logs"
OUTPUT_DIR="/home/yy/.openclaw/workspace-partrickstar/stock-monitor-system/output"

echo "=============================================="
echo "📊 股票监控推送验证报告"
echo "=============================================="
echo "检查时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查日志文件
echo "📁 日志文件状态:"
ls -lh "$LOGS_DIR"/push_cron.log 2>/dev/null || echo "  ❌ push_cron.log 不存在"
ls -lh "$LOGS_DIR"/gold_cron.log 2>/dev/null || echo "  ❌ gold_cron.log 不存在"
echo ""

# 检查最近的推送记录
echo "📝 最近推送记录 (push_cron.log):"
if [ -f "$LOGS_DIR/push_cron.log" ]; then
    tail -20 "$LOGS_DIR/push_cron.log" | grep -E "🦞 多股票监控 |✅ 飞书推送成功 |❌|ERROR" || echo "  (无推送记录)"
else
    echo "  ❌ 日志文件不存在"
fi
echo ""

# 检查输出文件
echo "📤 输出文件状态:"
ls -lh "$OUTPUT_DIR"/stock_*.txt 2>/dev/null | tail -5 || echo "  ❌ 无股票输出文件"
echo ""

# 检查 crontab 配置
echo "⏰ Crontab 配置:"
crontab -l 2>/dev/null | grep multi_stocks | head -4 || echo "  ❌ 无股票监控 cron 任务"
echo ""

# 检查 cron 服务状态
echo "🔧 Cron 服务状态:"
systemctl is-active cron 2>/dev/null || service cron status 2>/dev/null | grep -i active || echo "  ❌ 无法检查 cron 状态"
echo ""

# 检查 syslog 中的执行记录
echo "📋 Syslog 执行记录 (最近 5 条):"
grep "multi_stocks_monitor.py" /var/log/syslog 2>/dev/null | tail -5 || echo "  ❌ 无执行记录"
echo ""

echo "=============================================="
echo "✅ 验证完成"
echo "=============================================="
