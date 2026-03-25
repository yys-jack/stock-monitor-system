#!/bin/bash
# 黄金价格监控 Cron 配置脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOLD_SCRIPT="$SCRIPT_DIR/gold_monitor.py"
CRON_LOG="$SCRIPT_DIR/logs/gold_cron.log"

mkdir -p "$SCRIPT_DIR/logs"

# 配置：交易时间每小时推送一次
# 上午：9:30, 10:30, 11:30
# 下午：13:30, 14:30
CRON_ENTRIES="# 黄金价格推送 - 交易时间每小时
30 9-11 * * 1-5 cd $SCRIPT_DIR && source venv/bin/activate && python3 $GOLD_SCRIPT >> $CRON_LOG 2>&1
30 13-14 * * 1-5 cd $SCRIPT_DIR && source venv/bin/activate && python3 $GOLD_SCRIPT >> $CRON_LOG 2>&1"

# 移除旧的黄金推送任务
crontab -l 2>/dev/null | grep -v "gold_monitor.py" | grep -v "# 黄金价格推送" > /tmp/crontab_temp.txt

# 添加新任务
echo "$CRON_ENTRIES" >> /tmp/crontab_temp.txt
crontab /tmp/crontab_temp.txt
rm /tmp/crontab_temp.txt

echo "✅ 黄金监控 Cron 任务安装完成！"
echo "执行时间：交易日 9:30-11:30, 13:00-15:00 (每小时)"
echo "日志文件：$CRON_LOG"
