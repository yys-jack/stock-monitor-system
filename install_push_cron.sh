#!/bin/bash
# 股票价格推送 Cron 配置脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUSH_SCRIPT="$SCRIPT_DIR/multi_stocks_monitor.py"
CRON_LOG="$SCRIPT_DIR/logs/push_cron.log"

mkdir -p "$SCRIPT_DIR/logs"

# 配置：交易时间每 30 分钟推送一次
# 上午：9:30-11:30 (9:30, 10:00, 10:30, 11:00, 11:30)
# 下午：13:00-15:00 (13:00, 13:30, 14:00, 14:30, 15:00)
CRON_ENTRIES="# 股票价格推送 - 交易时间每 30 分钟
30 9-11 * * 1-5 cd $SCRIPT_DIR && source venv/bin/activate && python3 $PUSH_SCRIPT >> $CRON_LOG 2>&1
0 10-11 * * 1-5 cd $SCRIPT_DIR && source venv/bin/activate && python3 $PUSH_SCRIPT >> $CRON_LOG 2>&1
0,30 13-14 * * 1-5 cd $SCRIPT_DIR && source venv/bin/activate && python3 $PUSH_SCRIPT >> $CRON_LOG 2>&1
0 15 * * 1-5 cd $SCRIPT_DIR && source venv/bin/activate && python3 $PUSH_SCRIPT >> $CRON_LOG 2>&1"

# 移除旧的推送任务
crontab -l 2>/dev/null | grep -v "multi_stocks_monitor.py" | grep -v "# 股票价格推送" > /tmp/crontab_temp.txt

# 添加新任务
echo "$CRON_ENTRIES" >> /tmp/crontab_temp.txt
crontab /tmp/crontab_temp.txt
rm /tmp/crontab_temp.txt

echo "✅ 股票推送 Cron 任务安装完成！"
echo "执行时间：交易日 9:30-11:30, 13:00-15:00 (每 30 分钟)"
