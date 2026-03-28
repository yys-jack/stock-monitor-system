#!/usr/bin/env python3
"""
多股票股价监控脚本
支持配置多只股票，批量获取股价并推送
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "stocks_config.json"
FEISHU_CONFIG_FILE = PROJECT_ROOT / "config" / "feishu_config.json"
OUTPUT_DIR = PROJECT_ROOT / "output"


def load_feishu_config() -> dict:
    """加载飞书配置文件"""
    if not FEISHU_CONFIG_FILE.exists():
        print(f"[ERROR] 飞书配置文件不存在：{FEISHU_CONFIG_FILE}")
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


# 飞书配置
FEISHU_CONFIG = load_feishu_config()


def load_stocks_config() -> dict:
    """加载股票配置文件"""
    if not CONFIG_FILE.exists():
        print(f"[ERROR] 配置文件不存在：{CONFIG_FILE}")
        return None

    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def fetch_stock_price(code: str, market: str) -> Optional[dict]:
    """从腾讯财经获取单只股票价格"""
    try:
        url = f"https://qt.gtimg.cn/q={market}{code}"

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
        }
    except Exception as e:
        print(f"[ERROR] 获取{code}股价失败：{e}")
        return None


def format_single_message(stock_info: dict, price_data: dict) -> str:
    """格式化单只股票消息"""
    change = price_data.get("change_pct", 0)
    change_symbol = "📈" if change > 0 else "📉" if change < 0 else "➡️"

    alias = stock_info.get("alias", stock_info["name"])

    return f"""{change_symbol}【{stock_info["name"]} {stock_info["code"]}】股价提醒
🏷️ 别名：{alias}
⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

💹 实时股价
  当前价：{price_data['current']:.2f} 元 ({change:+.2f}%)
  涨跌额：{price_data['change_amt']:+.2f} 元

📊 今日行情
  昨收：{price_data['prev_close']:.2f} 元
  开盘：{price_data['open']:.2f} 元
  最高：{price_data['high']:.2f} 元
  最低：{price_data['low']:.2f} 元
  成交量：{price_data['volume']:,} 手

---
🤖 多股票监控系统 | {stock_info.get('notes', '')}"""


def format_combined_message(stocks_data: list) -> str:
    """格式化合并消息（多只股票一起推送）"""
    lines = [
        f"📊 多股票监控日报 - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    for item in stocks_data:
        stock_info = item["stock_info"]
        price_data = item["price_data"]

        if not price_data:
            lines.append(f"❌ {stock_info['name']} {stock_info['code']} - 获取失败")
            continue

        change = price_data.get("change_pct", 0)
        change_symbol = "📈" if change > 0 else "📉" if change < 0 else "➡️"

        lines.append(f"{change_symbol} **{stock_info['name']} {stock_info['code']}**")
        lines.append(f"  当前价：{price_data['current']:.2f} 元 ({change:+.2f}%)")
        lines.append(f"  成交量：{price_data['volume']:,} 手")
        lines.append("")

    lines.append("---")
    lines.append("🤖 多股票监控系统")

    return "\n".join(lines)


def send_feishu_message(message: str, retry_times: int = None) -> bool:
    """发送飞书消息（带重试机制）"""
    if not FEISHU_CONFIG.get("enabled"):
        print("[INFO] 飞书推送未启用")
        return False

    if retry_times is None:
        retry_times = FEISHU_CONFIG.get("retry_times", 3)

    retry_delay = FEISHU_CONFIG.get("retry_delay", 2)

    for attempt in range(1, retry_times + 1):
        try:
            if attempt > 1:
                print(f"[INFO] 重试推送 (第 {attempt}/{retry_times} 次)...")
                import time

                time.sleep(retry_delay)

            # 1. 获取 tenant_access_token
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = {
                "app_id": FEISHU_CONFIG["app_id"],
                "app_secret": FEISHU_CONFIG["app_secret"],
            }
            token_resp = requests.post(token_url, json=token_data, timeout=10)
            if token_resp.status_code != 200:
                print(f"[WARN] 获取飞书 token 失败：{token_resp.status_code}")
                continue

            token_result = token_resp.json()
            if token_result.get("code") != 0:
                print(f"[WARN] 飞书 token 错误：{token_result}")
                continue

            tenant_token = token_result.get("tenant_access_token")

            # 2. 发送消息
            msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
            headers = {
                "Authorization": f"Bearer {tenant_token}",
                "Content-Type": "application/json",
            }
            msg_data = {
                "receive_id": FEISHU_CONFIG["user_id"],
                "msg_type": "text",
                "content": json.dumps({"text": message}),
            }

            msg_resp = requests.post(msg_url, headers=headers, json=msg_data, timeout=10)
            if msg_resp.status_code == 200:
                result = msg_resp.json()
                if result.get("code") == 0:
                    print("[INFO] ✅ 飞书推送成功！")
                    return True
                else:
                    print(f"[WARN] 飞书发送失败：{result}")
            else:
                print(f"[WARN] 飞书 API 错误：{msg_resp.status_code}")

        except Exception as e:
            print(f"[ERROR] 飞书推送异常 (第 {attempt} 次): {e}")

        if attempt < retry_times:
            print(f"[INFO] 等待 {retry_delay} 秒后重试...")

    print(f"[ERROR] ❌ 飞书推送失败，已重试 {retry_times} 次")
    return False


def is_trading_time() -> bool:
    """判断当前是否在交易时间内"""
    now = datetime.now()

    # 周末不交易
    if now.weekday() >= 5:  # 5=周六，6=周日
        return False

    # 交易时间：上午 9:30-11:30，下午 13:00-15:00
    # 注意：cron 任务可能延迟几秒执行，所以结束时间加 1 分钟容错
    current_time = now.strftime("%H%M")

    # 上午交易时间：9:30-11:31（含 11:30 的推送）
    morning_start = int("0930")
    morning_end = int("1131")  # 加 1 分钟容错

    # 下午交易时间：13:00-15:01（含 15:00 的推送）
    afternoon_start = int("1300")
    afternoon_end = int("1501")  # 加 1 分钟容错

    current = int(current_time)

    if morning_start <= current <= morning_end:
        return True
    if afternoon_start <= current <= afternoon_end:
        return True

    return False


def main():
    """主函数"""
    print(f"🦞 多股票监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 检查是否在交易时间
    if not is_trading_time():
        print("[INFO] 当前非交易时间，跳过推送")
        print("[INFO] 交易时间：周一至周五 9:30-11:30, 13:00-15:00")
        return True

    # 加载配置
    config = load_stocks_config()
    if not config:
        return False

    stocks = config.get("stocks", [])
    settings = config.get("settings", {})
    push_format = settings.get("push_format", "single")  # single 或 combined

    print(f"[INFO] 配置股票数量：{len(stocks)}")

    # 过滤启用的股票
    enabled_stocks = [s for s in stocks if s.get("enabled", True)]
    print(f"[INFO] 启用股票数量：{len(enabled_stocks)}")

    if not enabled_stocks:
        print("[WARN] 没有启用的股票")
        return False

    # 获取股价数据
    stocks_data = []
    for stock in enabled_stocks:
        code = stock["code"]
        market = stock["market"]
        name = stock["name"]

        print(f"\n[INFO] 获取 {name}({code}) 股价...")
        price_data = fetch_stock_price(code, market)

        if price_data:
            print(f"  ✅ 当前价：{price_data['current']:.2f} 元 ({price_data['change_pct']:+.2f}%)")
        else:
            print("  ❌ 获取失败")

        stocks_data.append(
            {
                "stock_info": stock,
                "price_data": price_data,
            }
        )

    # 推送消息
    print(f"\n[INFO] 推送格式：{push_format}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if push_format == "combined":
        # 合并推送（所有股票一条消息）
        message = format_combined_message(stocks_data)
        print("\n[INFO] 合并推送消息")

        # 写入文件
        output_file = OUTPUT_DIR / "multi_stocks_combined.txt"
        output_file.write_text(message, encoding="utf-8")
        print(f"[INFO] 消息已写入：{output_file}")

        # 飞书推送
        if FEISHU_CONFIG.get("enabled"):
            send_feishu_message(message)
    else:
        # 单独推送（每只股票一条消息）
        print("\n[INFO] 单独推送每只股票")

        for i, item in enumerate(stocks_data, 1):
            stock_info = item["stock_info"]
            price_data = item["price_data"]

            if not price_data:
                print(f"\n[WARN] 跳过 {stock_info['name']}（获取失败）")
                continue

            message = format_single_message(stock_info, price_data)

            print(f"\n[{i}/{len(stocks_data)}] {stock_info['name']} - 推送消息")

            # 写入文件
            output_file = OUTPUT_DIR / f"stock_{stock_info['code']}.txt"
            output_file.write_text(message, encoding="utf-8")
            print(f"[INFO] 消息已写入：{output_file}")

            # 飞书推送
            if FEISHU_CONFIG.get("enabled"):
                print("[INFO] 发送飞书消息...")
                send_feishu_message(message)

    print("\n✅ 多股票监控完成！")
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
