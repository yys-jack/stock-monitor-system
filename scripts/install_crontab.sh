#!/bin/bash
# Crontab 安装脚本
# 用途：从模板安装 crontab 配置

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATE_FILE="$PROJECT_ROOT/config/crontab.template"
TEMP_FILE="/tmp/crontab_install_$$.txt"

echo "=============================================="
echo "📦 Crontab 安装脚本"
echo "=============================================="
echo ""

# 检查模板文件
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "❌ 错误：模板文件不存在：$TEMPLATE_FILE"
    exit 1
fi

echo "✅ 模板文件：$TEMPLATE_FILE"
echo ""

# 替换模板变量
echo "🔄 替换模板变量..."
sed "s|{{PROJECT_ROOT}}|$PROJECT_ROOT|g" "$TEMPLATE_FILE" > "$TEMP_FILE"

# 显示预览
echo ""
echo "📋 即将安装的 crontab 配置："
echo "----------------------------------------------"
grep -E "^[^#]" "$TEMP_FILE" | grep -v "^$" | head -20
echo "----------------------------------------------"
echo ""

# 确认安装
read -p "是否继续安装？(y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 安装已取消"
    rm -f "$TEMP_FILE"
    exit 0
fi

# 备份当前 crontab
echo ""
echo "💾 备份当前 crontab..."
BACKUP_FILE="/tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt"
crontab -l > "$BACKUP_FILE" 2>/dev/null || echo "(无现有 crontab)"
echo "✅ 备份文件：$BACKUP_FILE"

# 安装新 crontab
echo ""
echo "📥 安装 crontab..."
crontab "$TEMP_FILE"

# 验证安装
echo ""
echo "✅ 验证安装..."
crontab -l | grep -c "multi_stocks" && echo "✅ 股票监控任务已安装" || echo "❌ 股票监控任务未找到"
crontab -l | grep -c "gold_monitor" && echo "✅ 黄金监控任务已安装" || echo "❌ 黄金监控任务未找到"

# 清理临时文件
rm -f "$TEMP_FILE"

echo ""
echo "=============================================="
echo "✅ Crontab 安装完成！"
echo "=============================================="
echo ""
echo "验证命令："
echo "  crontab -l                          # 查看已安装的任务"
echo "  ./scripts/verify_push.sh            # 运行验证脚本"
echo "  grep multi_stocks /var/log/syslog   # 查看执行日志"
echo ""
