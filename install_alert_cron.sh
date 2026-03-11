#!/bin/bash
# ==================== 股价预警 Cron 配置脚本 ====================
# 用法：
#   ./install_alert_cron.sh install   - 安装定时任务
#   ./install_alert_cron.sh uninstall - 卸载定时任务
#   ./install_alert_cron.sh status    - 查看状态

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALERT_SCRIPT="$SCRIPT_DIR/price_alert_monitor.py"
CRON_LOG="$SCRIPT_DIR/logs/alert_cron.log"

# 确保日志目录存在
mkdir -p "$SCRIPT_DIR/logs"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# 检查脚本是否存在
check_script() {
    if [ ! -f "$ALERT_SCRIPT" ]; then
        print_error "预警脚本不存在：$ALERT_SCRIPT"
        exit 1
    fi
    print_info "预警脚本：$ALERT_SCRIPT"
}

# 安装 Cron 任务
install_cron() {
    print_info "安装股价预警 Cron 任务..."
    
    # 创建 Cron 表达式（交易时间每 5 分钟检查一次）
    # 上午：9:30-11:30
    # 下午：13:00-15:00
    CRON_ENTRIES="# 股价异常预警 - 交易时间每 5 分钟检查
*/5 9-11 * * 1-5 /usr/bin/python3 $ALERT_SCRIPT >> $CRON_LOG 2>&1
*/5 13-14 * * 1-5 /usr/bin/python3 $ALERT_SCRIPT >> $CRON_LOG 2>&1
0-5/5 15 * * 1-5 /usr/bin/python3 $ALERT_SCRIPT >> $CRON_LOG 2>&1"

    # 备份当前 crontab
    BACKUP_FILE="$HOME/crontab_backup_$(date +%Y%m%d_%H%M%S).txt"
    crontab -l > "$BACKUP_FILE" 2>/dev/null || true
    print_info "已备份当前 crontab: $BACKUP_FILE"
    
    # 检查是否已安装
    if crontab -l 2>/dev/null | grep -q "price_alert_monitor.py"; then
        print_warn "检测到已存在的预警任务，先移除..."
        crontab -l | grep -v "price_alert_monitor.py" | crontab -
    fi
    
    # 添加新任务
    (crontab -l 2>/dev/null | grep -v "^# 股价异常预警"; echo "$CRON_ENTRIES") | crontab -
    
    print_info "✅ 股价预警 Cron 任务安装完成！"
    print_info "执行时间：交易日 9:30-11:30, 13:00-15:00 (每 5 分钟)"
    print_info "日志文件：$CRON_LOG"
}

# 卸载 Cron 任务
uninstall_cron() {
    print_info "卸载股价预警 Cron 任务..."
    
    # 移除相关任务
    crontab -l 2>/dev/null | grep -v "price_alert_monitor.py" | grep -v "# 股价异常预警" | crontab -
    
    print_info "✅ 股价预警 Cron 任务已卸载！"
}

# 查看状态
show_status() {
    print_info "当前 Cron 任务状态："
    echo ""
    
    if crontab -l 2>/dev/null | grep -q "price_alert_monitor.py"; then
        print_info "✅ 股价预警任务已安装"
        echo ""
        print_info "任务列表："
        crontab -l | grep -A5 "股价异常预警" || true
    else
        print_warn "❌ 股价预警任务未安装"
    fi
    
    echo ""
    print_info "预警脚本：$ALERT_SCRIPT"
    if [ -f "$ALERT_SCRIPT" ]; then
        print_info "脚本状态：✅ 存在"
    else
        print_error "脚本状态：❌ 不存在"
    fi
    
    echo ""
    if [ -f "$CRON_LOG" ]; then
        print_info "日志文件：$CRON_LOG"
        print_info "最近 5 条日志："
        tail -5 "$CRON_LOG" 2>/dev/null || echo "(无日志)"
    else
        print_warn "日志文件：尚未生成"
    fi
}

# 测试执行
test_run() {
    print_info "测试执行预警脚本..."
    python3 "$ALERT_SCRIPT"
}

# 主函数
main() {
    case "${1:-}" in
        install)
            check_script
            install_cron
            ;;
        uninstall)
            uninstall_cron
            ;;
        status)
            show_status
            ;;
        test)
            check_script
            test_run
            ;;
        *)
            echo "用法：$0 {install|uninstall|status|test}"
            echo ""
            echo "命令说明："
            echo "  install   - 安装股价预警定时任务"
            echo "  uninstall - 卸载股价预警定时任务"
            echo "  status    - 查看当前状态"
            echo "  test      - 测试执行预警脚本"
            echo ""
            echo "示例："
            echo "  $0 install   # 安装定时任务"
            echo "  $0 status    # 查看状态"
            echo "  $0 test      # 测试执行"
            exit 1
            ;;
    esac
}

main "$@"
