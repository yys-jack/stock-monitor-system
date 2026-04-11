#!/usr/bin/env python3
"""
中兴通讯 (000063) 股价异常预警脚本
涨跌幅超过阈值时立即推送通知
"""

import json
from datetime import datetime
from pathlib import Path

import requests

from src.feishu import notifier, send_post

# ==================== 配置文件路径 ====================

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "stocks_config.json"
FEISHU_CONFIG_FILE = PROJECT_ROOT / "config" / "feishu_config.json"

# ==================== 加载配置 ====================


def load_feishu_config() -> dict:
    """加载飞书配置文件"""
    if not FEISHU_CONFIG_FILE.exists():
        return {
            "enabled": False,
            "user_id": "",
            "app_id": "",
            "app_secret": "",
            "retry_times": 3,
            "retry_delay": 2,
        }

    with open(FEISHU_CONFIG_FILE, encoding="utf-8") as f:
        config = json.load(f)
        return config.get("feishu", {})


def load_stock_config() -> dict:
    """加载股票配置"""
    if not CONFIG_FILE.exists():
        return {
            "stocks": [{"code": "000063", "name": "中兴通讯", "market": "sz"}],
            "settings": {"alert_threshold_up": 5.0, "alert_threshold_down": -5.0},
        }

    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


# 加载配置
stocks_config = load_stock_config()
feishu_config = load_feishu_config()

# 初始化 notifier 配置
_feishu_cfg = feishu_config
if _feishu_cfg:
    notifier.enabled = _feishu_cfg.get("enabled", False)
    notifier.user_id = _feishu_cfg.get("user_id", "")
    notifier.app_id = _feishu_cfg.get("app_id", "")
    notifier.app_secret = _feishu_cfg.get("app_secret", "")

# 获取第一只启用的股票
enabled_stocks = [s for s in stocks_config.get("stocks", []) if s.get("enabled", True)]
stock_info = (
    enabled_stocks[0] if enabled_stocks else {"code": "000063", "name": "中兴通讯", "market": "sz"}
)
settings = stocks_config.get("settings", {})

# ==================== 配置区域 ====================

CONFIG = {
    "stock_code": stock_info.get("code", "000063"),
    "stock_name": stock_info.get("name", "中兴通讯"),
    "market": stock_info.get("market", "sz"),
    # 预警阈值（百分比）
    "threshold_up": settings.get("alert_threshold_up", 5.0),
    "threshold_down": settings.get("alert_threshold_down", -5.0),
    # 数据目录
    "data_dir": Path(__file__).parent / "data",
}

# ==================== 数据获取 ====================


def fetch_price_tencent() -> dict:
    """从腾讯财经获取实时股价"""
    try:
        code = CONFIG["stock_code"]
        prefix = CONFIG["market"]
        url = f"https://qt.gtimg.cn/q={prefix}{code}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = "gbk"

        if resp.status_code != 200:
            return None

        content = resp.text.strip()
        if not content.startswith("v_"):
            return None

        data_str = content.split('="')[1].rstrip('";')
        fields = data_str.split("~")

        if len(fields) < 35:
            return None

        return {
            "name": fields[1],
            "code": fields[2],
            "current": float(fields[3]) if fields[3] else 0,
            "prev_close": float(fields[4]) if fields[4] else 0,
            "open": float(fields[5]) if fields[5] else 0,
            "volume": int(fields[6]) if fields[6] else 0,
            "high": float(fields[33]) if fields[33] else 0,
            "low": float(fields[34]) if fields[34] else 0,
            "change_amt": float(fields[31]) if fields[31] else 0,
            "change_pct": float(fields[32]) if fields[32] else 0,
            "time": fields[30] if len(fields) > 30 else "",
        }
    except Exception as e:
        print(f"[ERROR] 获取股价失败：{e}")
        return None


# ==================== 飞书推送 ====================


def send_feishu_alert(message: str, alert_type: str = "warning") -> bool:
    """
    发送飞书预警消息
    alert_type: warning (警告), info (信息), danger (危险)
    """
    # 使用富文本格式发送
    title = "⚠️ 股价异常预警"
    content_list = [
        [{"tag": "text", "text": message}],
        [
            {
                "tag": "text",
                "text": f"\n预警时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            }
        ],
    ]

    return send_post(title, content_list)


# ==================== 预警逻辑 ====================


def check_price_alert(data: dict) -> tuple:
    """
    检查是否触发预警
    返回：(是否触发，预警类型，预警消息)
    """
    change_pct = data.get("change_pct", 0)
    current = data.get("current", 0)
    prev_close = data.get("prev_close", 0)

    # 检查上涨预警
    if change_pct >= CONFIG["threshold_up"]:
        msg = f"""🚨 股价大幅上涨预警！

📈 {data['name']} {data['code']}
💹 当前价：{current:.2f} 元
📊 涨跌幅：+{change_pct:.2f}%
💰 涨跌额：+{data.get('change_amt', 0):.2f} 元
📉 昨收价：{prev_close:.2f} 元

⚠️ 涨幅已超过 {CONFIG['threshold_up']}% 预警线！"""
        return True, "danger", msg

    # 检查下跌预警
    if change_pct <= CONFIG["threshold_down"]:
        msg = f"""🚨 股价大幅下跌预警！

📉 {data['name']} {data['code']}
💹 当前价：{current:.2f} 元
📊 涨跌幅：{change_pct:.2f}%
💰 涨跌额：{data.get('change_amt', 0):.2f} 元
📈 昨收价：{prev_close:.2f} 元

⚠️ 跌幅已超过 {CONFIG['threshold_down']}% 预警线！"""
        return True, "danger", msg

    # 检查接近预警线（80% 阈值）
    if change_pct >= CONFIG["threshold_up"] * 0.8:
        msg = f"""📊 股价快速上涨提醒

📈 {data['name']} {data['code']}
💹 当前价：{current:.2f} 元
📊 涨跌幅：+{change_pct:.2f}%

⚠️ 涨幅接近 {CONFIG['threshold_up']}% 预警线，请密切关注！"""
        return True, "warning", msg

    if change_pct <= CONFIG["threshold_down"] * 0.8:
        msg = f"""📊 股价快速下跌提醒

📉 {data['name']} {data['code']}
💹 当前价：{current:.2f} 元
📊 涨跌幅：{change_pct:.2f}%

⚠️ 跌幅接近 {CONFIG['threshold_down']}% 预警线，请密切关注！"""
        return True, "warning", msg

    return False, None, None


# ==================== 状态管理 ====================


def get_alert_state_file() -> Path:
    """获取状态文件路径"""
    CONFIG["data_dir"].mkdir(parents=True, exist_ok=True)
    return CONFIG["data_dir"] / "alert_state.json"


def load_alert_state() -> dict:
    """加载预警状态"""
    state_file = get_alert_state_file()
    if state_file.exists():
        try:
            with open(state_file) as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_alert": None, "alert_count": 0}


def save_alert_state(state: dict):
    """保存预警状态"""
    state_file = get_alert_state_file()
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


# ==================== 主程序 ====================


def main():
    """主函数"""
    print(f"🦞 股价预警脚本 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"预警阈值：上涨≥{CONFIG['threshold_up']}% | 下跌≤{CONFIG['threshold_down']}%")
    print("=" * 60)

    # 获取股价
    data = fetch_price_tencent()
    if not data:
        print("[ERROR] 获取股价数据失败")
        return False

    print(f"[INFO] {data['name']} 当前价：{data['current']:.2f} 元 ({data['change_pct']:+.2f}%)")

    # 检查预警
    triggered, alert_type, message = check_price_alert(data)

    if triggered:
        print(f"\n[ALERT] ⚠️ 触发{alert_type}预警！")

        # 加载状态，避免重复推送
        state = load_alert_state()
        last_alert = state.get("last_alert")

        # 如果 30 分钟内已推送过相同类型的预警，则跳过
        if last_alert:
            last_time = datetime.fromisoformat(last_alert)
            time_diff = (datetime.now() - last_time).total_seconds() / 60
            if time_diff < 30:
                print(f"[INFO] 已在{time_diff:.0f}分钟内推送过，跳过本次推送")
                return True

        # 发送飞书预警
        if notifier.enabled:
            print("[INFO] 正在发送飞书预警...")
            if send_feishu_alert(message, alert_type):
                print("[INFO] ✅ 预警推送成功！")

                # 更新状态
                state["last_alert"] = datetime.now().isoformat()
                state["alert_count"] = state.get("alert_count", 0) + 1
                state["last_change_pct"] = data["change_pct"]
                save_alert_state(state)
        else:
            print("[WARN] 飞书推送未启用")
            print("\n" + message)
    else:
        print("[INFO] ✅ 股价正常，未触发预警")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
