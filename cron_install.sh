#!/bin/bash
# ==================== Cron 定时任务管理脚本 ====================
# 用法：
#   ./cron_install.sh install    - 安装所有定时任务
#   ./cron_install.sh uninstall  - 卸载所有定时任务
#   ./cron_install.sh status     - 查看状态
#   ./cron_install.sh stocks     - 只安装股票推送任务
#   ./cron_install.sh gold       - 只安装黄金监控任务
#   ./cron_install.sh alert      - 只安装股价预警任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_FILE="$SCRIPT_DIR/logs/crontab_backup.txt"

# 确保日志目录存在
mkdir -p "$SCRIPT_DIR/logs"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_blue() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# ==================== Cron 任务定义 ====================

# 股票价格推送（交易时间每 30 分钟）
STOCKS_CRON="# 股票价格推送 - 交易时间每 30 分钟
30 9-11 * * 1-5 /bin/bash -c 'cd $SCRIPT_DIR && source venv/bin/activate && python3 $SCRIPT_DIR/multi_stocks_monitor.py' >> $SCRIPT_DIR/logs/push_cron.log 2>&1
0 10-11 * * 1-5 /bin/bash -c 'cd $SCRIPT_DIR && source venv/bin/activate && python3 $SCRIPT_DIR/multi_stocks_monitor.py' >> $SCRIPT_DIR/logs/push_cron.log 2>&1
0,30 13-14 * * 1-5 /bin/bash -c 'cd $SCRIPT_DIR && source venv/bin/activate && python3 $SCRIPT_DIR/multi_stocks_monitor.py' >> $SCRIPT_DIR/logs/push_cron.log 2>&1
0 15 * * 1-5 /bin/bash -c 'cd $SCRIPT_DIR && source venv/bin/activate && python3 $SCRIPT_DIR/multi_stocks_monitor.py' >> $SCRIPT_DIR/logs/push_cron.log 2>&1"

# 黄金价格监控（交易时间每小时）
GOLD_CRON="# 黄金价格推送 - 交易时间每小时
30 9-11 * * 1-5 /bin/bash -c 'cd $SCRIPT_DIR && source venv/bin/activate && python3 $SCRIPT_DIR/gold_monitor.py' >> $SCRIPT_DIR/logs/gold_cron.log 2>&1
30 13-14 * * 1-5 /bin/bash -c 'cd $SCRIPT_DIR && source venv/bin/activate && python3 $SCRIPT_DIR/gold_monitor.py' >> $SCRIPT_DIR/logs/gold_cron.log 2>&1"

# 股价异常预警（交易时间每 5 分钟）
ALERT_CRON="# 股价异常预警 - 交易时间每 5 分钟
*/5 9-11 * * 1-5 /bin/bash -c 'cd $SCRIPT_DIR && source venv/bin/activate && python3 $SCRIPT_DIR/price_alert_monitor.py' >> $SCRIPT_DIR/logs/alert_cron.log 2>&1
*/5 13-14 * * 1-5 /bin/bash -c 'cd $SCRIPT_DIR && source venv/bin/activate && python3 $SCRIPT_DIR/price_alert_monitor.py' >> $SCRIPT_DIR/logs/alert_cron.log 2>&1
0-5/5 15 * * 1-5 /bin/bash -c 'cd $SCRIPT_DIR && source venv/bin/activate && python3 $SCRIPT_DIR/price_alert_monitor.py' >> $SCRIPT_DIR/logs/alert_cron.log 2>&1"

# ==================== 功能函数 ====================

# 备份当前 crontab
backup_crontab() {
    local backup_file="$SCRIPT_DIR/logs/crontab_backup_$(date +%Y%m%d_%H%M%S).txt"
    crontab -l > "$backup_file" 2>/dev/null || true
    print_info "已备份当前 crontab: $backup_file"
}

# 检查脚本是否存在
check_scripts() {
    local scripts=("$SCRIPT_DIR/multi_stocks_monitor.py" "$SCRIPT_DIR/gold_monitor.py" "$SCRIPT_DIR/price_alert_monitor.py")
    local all_exist=true
    
    for script in "${scripts[@]}"; do
        if [ ! -f "$script" ]; then
            print_warn "脚本不存在：$script"
            all_exist=false
        fi
    done
    
    if [ "$all_exist" = true ]; then
        print_info "✅ 所有监控脚本存在"
    fi
}

# 安装所有任务
install_all() {
    print_blue "📦 安装所有 Cron 任务..."
    backup_crontab
    
    # 移除旧的任务
    crontab -l 2>/dev/null | grep -v "# 股票价格推送" | grep -v "# 黄金价格推送" | grep -v "# 股价异常预警" > /tmp/crontab_temp.txt
    
    # 添加新任务
    echo "" >> /tmp/crontab_temp.txt
    echo "$STOCKS_CRON" >> /tmp/crontab_temp.txt
    echo "" >> /tmp/crontab_temp.txt
    echo "$GOLD_CRON" >> /tmp/crontab_temp.txt
    echo "" >> /tmp/crontab_temp.txt
    echo "$ALERT_CRON" >> /tmp/crontab_temp.txt
    
    crontab /tmp/crontab_temp.txt
    rm /tmp/crontab_temp.txt
    
    print_info "✅ 所有 Cron 任务安装完成！"
    show_status
}

# 卸载所有任务
uninstall_all() {
    print_blue "🗑️  卸载所有 Cron 任务..."
    backup_crontab
    
    crontab -l 2>/dev/null | grep -v "# 股票价格推送" | grep -v "# 黄金价格推送" | grep -v "# 股价异常预警" | grep -v "^$" > /tmp/crontab_temp.txt
    crontab /tmp/crontab_temp.txt
    rm /tmp/crontab_temp.txt
    
    print_info "✅ 所有 Cron 任务已卸载！"
}

# 只安装股票推送
install_stocks() {
    print_blue "📈 安装股票推送 Cron 任务..."
    backup_crontab
    
    crontab -l 2>/dev/null | grep -v "# 股票价格推送" > /tmp/crontab_temp.txt
    echo "" >> /tmp/crontab_temp.txt
    echo "$STOCKS_CRON" >> /tmp/crontab_temp.txt
    
    crontab /tmp/crontab_temp.txt
    rm /tmp/crontab_temp.txt
    
    print_info "✅ 股票推送 Cron 任务安装完成！"
}

# 只安装黄金监控
install_gold() {
    print_blue "🥇 安装黄金监控 Cron 任务..."
    backup_crontab
    
    crontab -l 2>/dev/null | grep -v "# 黄金价格推送" > /tmp/crontab_temp.txt
    echo "" >> /tmp/crontab_temp.txt
    echo "$GOLD_CRON" >> /tmp/crontab_temp.txt
    
    crontab /tmp/crontab_temp.txt
    rm /tmp/crontab_temp.txt
    
    print_info "✅ 黄金监控 Cron 任务安装完成！"
}

# 只安装股价预警
install_alert() {
    print_blue "⚠️  安装股价预警 Cron 任务..."
    backup_crontab
    
    crontab -l 2>/dev/null | grep -v "# 股价异常预警" > /tmp/crontab_temp.txt
    echo "" >> /tmp/crontab_temp.txt
    echo "$ALERT_CRON" >> /tmp/crontab_temp.txt
    
    crontab /tmp/crontab_temp.txt
    rm /tmp/crontab_temp.txt
    
    print_info "✅ 股价预警 Cron 任务安装完成！"
}

# 查看状态
show_status() {
    print_blue "📊 当前 Cron 任务状态："
    echo ""
    
    local stock_count=$(crontab -l 2>/dev/null | grep -c "股票价格推送" 2>/dev/null || echo "0")
    local gold_count=$(crontab -l 2>/dev/null | grep -c "黄金价格推送" 2>/dev/null || echo "0")
    local alert_count=$(crontab -l 2>/dev/null | grep -c "股价异常预警" 2>/dev/null || echo "0")
    
    # 确保是整数
    stock_count=${stock_count:-0}
    gold_count=${gold_count:-0}
    alert_count=${alert_count:-0}
    
    if [ "$stock_count" -gt 0 ] 2>/dev/null; then
        print_info "✅ 股票推送任务：已安装"
    else
        print_warn "❌ 股票推送任务：未安装"
    fi
    
    if [ "$gold_count" -gt 0 ] 2>/dev/null; then
        print_info "✅ 黄金监控任务：已安装"
    else
        print_warn "❌ 黄金监控任务：未安装"
    fi
    
    if [ "$alert_count" -gt 0 ] 2>/dev/null; then
        print_info "✅ 股价预警任务：已安装"
    else
        print_warn "❌ 股价预警任务：未安装"
    fi
    
    echo ""
    print_info "监控脚本："
    check_scripts
    
    echo ""
    print_info "日志文件："
    ls -lh "$SCRIPT_DIR/logs/"*.log 2>/dev/null || print_warn "暂无日志文件"
}

# 显示帮助
show_help() {
    echo "用法：$0 {install|uninstall|status|stocks|gold|alert}"
    echo ""
    echo "命令说明："
    echo "  install    - 安装所有定时任务（股票 + 黄金 + 预警）"
    echo "  uninstall  - 卸载所有定时任务"
    echo "  status     - 查看当前状态"
    echo "  stocks     - 只安装股票推送任务"
    echo "  gold       - 只安装黄金监控任务"
    echo "  alert      - 只安装股价预警任务"
    echo ""
    echo "示例："
    echo "  $0 install   # 安装所有任务"
    echo "  $0 status    # 查看状态"
    echo "  $0 stocks    # 只安装股票推送"
    echo ""
    echo "推送时间："
    echo "  股票推送：交易日 9:30-11:30, 13:00-15:00 (每 30 分钟)"
    echo "  黄金监控：交易日 9:30-11:30, 13:00-15:00 (每小时)"
    echo "  股价预警：交易日 9:30-11:30, 13:00-15:00 (每 5 分钟)"
}

# ==================== 主函数 ====================

main() {
    case "${1:-}" in
        install)
            install_all
            ;;
        uninstall)
            uninstall_all
            ;;
        status)
            show_status
            ;;
        stocks)
            install_stocks
            ;;
        gold)
            install_gold
            ;;
        alert)
            install_alert
            ;;
        *)
            show_help
            exit 1
            ;;
    esac
}

main "$@"
