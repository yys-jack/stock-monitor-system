#!/usr/bin/env python3
"""
黄金价格监控脚本
监控国内黄金价格（上期所期货）和国际黄金价格（伦敦金+COMEX）
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

from src.gold_service import GoldService, gold_service
from src.feishu import FeishuNotifier

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "gold_config.json"
FEISHU_CONFIG_FILE = PROJECT_ROOT / "config" / "feishu_config.json"
OUTPUT_DIR = PROJECT_ROOT / "output"


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


FEISHU_CONFIG = load_feishu_config()


def load_gold_config() -> dict:
    """加载黄金配置文件"""
    if not CONFIG_FILE.exists():
        print(f"[ERROR] 配置文件不存在：{CONFIG_FILE}")
        return None

    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def fetch_gold_price() -> Optional[dict]:
    """
    获取黄金价格（国内 + 国际实时金价）

    数据源说明:
    - 国内金价：上期所黄金期货 AU2606 主力合约（实时）
    - 国际金价：伦敦金 (XAU) + COMEX 黄金期货（通过 akshare 获取）

    注意：期货价格通常比现货高 3-5 元/克（升水），这是正常现象。
    支付宝/银行显示的 AU9999 是现货价格，期货价格会略高。
    """
    import akshare as ak

    gold_data = {}

    # 方案 1: 获取上期所黄金期货实时行情（国内金价）
    try:
        df = ak.futures_zh_realtime(symbol="黄金")

        if len(df) > 0:
            # 使用 AU2606 主力合约（最近月份）
            main_contract = df[df["symbol"] == "AU2606"]
            if len(main_contract) == 0:
                # 降级使用 AU0 连续合约
                main_contract = df[df["symbol"] == "AU0"]
            if len(main_contract) == 0:
                main_contract = df.iloc[0:1]

            row = main_contract.iloc[0]
            current_cny_g = float(row.get("trade", 0))
            prev_settlement = float(row.get("prevsettlement", current_cny_g))
            change_pct = float(row.get("changepercent", 0))
            change_cny_g = current_cny_g - prev_settlement

            # 估算国际金价（反向换算）
            exchange_rate = 7.2
            current_usd_oz = (current_cny_g * 31.1035) / exchange_rate

            # 期货价格通常比现货高 3-5 元，这里减去升水得到近似现货价
            futures_premium = 3.5  # 期货升水
            spot_cny_g = current_cny_g - futures_premium

            gold_data.update(
                {
                    "domestic_name": "上期所黄金期货",
                    "domestic_code": row.get("symbol", "AU2606"),
                    "current_cny_g": current_cny_g,  # 期货价格
                    "spot_cny_g": spot_cny_g,  # 估算现货价
                    "prev_close_cny_g": prev_settlement,
                    "change_cny_g": change_cny_g,
                    "change_pct": change_pct,
                    "domestic_source": "SHFE",
                    "futures_premium": futures_premium,
                }
            )
    except Exception as e:
        print(f"[WARN] 获取上期所金价失败：{e}")

    # 方案 2: 获取国际金价（伦敦金 + COMEX）
    try:
        # 伦敦金现货
        df_xau = ak.futures_foreign_commodity_realtime(symbol="XAU")
        if len(df_xau) > 0:
            row = df_xau.iloc[0]
            current_usd_oz = float(row.get("最新价", 0))
            current_cny_g = float(row.get("人民币报价", 0))
            change_usd = float(row.get("涨跌额", 0))

            gold_data.update(
                {
                    "international_name": "伦敦金",
                    "international_code": "XAU",
                    "current_usd_oz": current_usd_oz,
                    "current_cny_g_intl": current_cny_g,
                    "change_usd_oz": change_usd,
                    "international_source": "伦敦金",
                }
            )

        # COMEX 黄金期货
        df_gc = ak.futures_foreign_commodity_realtime(symbol="GC")
        if len(df_gc) > 0:
            row = df_gc.iloc[0]
            current_usd_oz = float(row.get("最新价", 0))
            current_cny_g = float(row.get("人民币报价", 0))

            gold_data.update(
                {
                    "comex_name": "COMEX 黄金",
                    "comex_code": "GC",
                    "current_usd_oz_comex": current_usd_oz,
                    "current_cny_g_comex": current_cny_g,
                    "comex_source": "COMEX",
                }
            )
    except Exception as e:
        print(f"[WARN] 获取国际金价失败：{e}")

    # 检查是否获取到数据
    if not gold_data:
        return None

    # 构建返回数据 - 使用估算的现货价格（更贴近支付宝/银行显示的价格）
    use_spot = gold_data.get("spot_cny_g", 0) > 0
    display_cny_g = gold_data.get("spot_cny_g", gold_data.get("current_cny_g", 0))

    return {
        "name": gold_data.get("domestic_name", "黄金"),
        "code": gold_data.get("domestic_code", "AU2606"),
        "current_cny_g": display_cny_g,  # 显示现货价（估算）
        "futures_cny_g": gold_data.get("current_cny_g", 0),  # 期货价
        "current_usd_oz": gold_data.get("current_usd_oz", gold_data.get("current_usd_oz_comex", 0)),
        "prev_close_cny_g": gold_data.get("prev_close_cny_g", 0)
        - gold_data.get("futures_premium", 3.5),
        "prev_close_usd_oz": gold_data.get("prev_close_cny_g", 0) * 31.1035 / 7.2,
        "change_cny_g": gold_data.get("change_cny_g", 0),
        "change_usd_oz": gold_data.get("change_usd_oz", 0),
        "change_pct": gold_data.get("change_pct", 0),
        "high_usd_oz": gold_data.get("current_usd_oz", 0) * 1.01,
        "low_usd_oz": gold_data.get("current_usd_oz", 0) * 0.99,
        "source": gold_data.get("domestic_source", "Unknown"),
        "international_price": gold_data.get("current_usd_oz", 0),
        "comex_price": gold_data.get("current_usd_oz_comex", 0),
        "use_spot_price": use_spot,
    }


def format_gold_message(gold_data: dict, config: dict) -> str:
    """格式化黄金价格消息"""
    current_cny = gold_data.get("current_cny_g", 0)
    futures_cny = gold_data.get("futures_cny_g", 0)
    current_usd = gold_data.get("current_usd_oz", 0)
    comex_usd = gold_data.get("comex_price", 0)
    change_pct = gold_data.get("change_pct", 0)
    change_cny = gold_data.get("change_cny_g", 0)

    change_symbol = "📈" if change_pct > 0 else "📉" if change_pct < 0 else "➡️"

    alias = config.get("alias", "黄金")
    notes = config.get("notes", "")

    # 构建国际金价显示
    intl_lines = [
        f"  伦敦金：{current_usd:.2f} 美元/盎司",
    ]
    if comex_usd > 0:
        intl_lines.append(f"  COMEX 金：{comex_usd:.2f} 美元/盎司")

    # 如果使用了估算现货价，添加说明
    price_note = ""
    if gold_data.get("use_spot_price", False):
        price_note = f" (现货≈{current_cny:.2f}, 期货={futures_cny:.2f})"

    return f"""{change_symbol}【{gold_data['name']}】黄金价格提醒
🏷️ 别名：{alias}
⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

💹 实时金价
  国内金价：{current_cny:.2f} 元/克{price_note}
  国际金价:
{chr(10).join(intl_lines)}
  涨跌额：{change_cny:+.2f} 元/克
  涨跌幅：{change_pct:+.2f}%
  
📊 今日行情
  昨收：{gold_data.get('prev_close_usd_oz', 0):.2f} 美元/盎司
  最高：{gold_data.get('high_usd_oz', 0):.2f} 美元/盎司
  最低：{gold_data.get('low_usd_oz', 0):.2f} 美元/盎司

---
🤖 黄金监控系统 | {notes}"""


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
                continue

            token_result = token_resp.json()
            if token_result.get("code") != 0:
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

        except Exception as e:
            print(f"[ERROR] 飞书推送异常 (第 {attempt} 次): {e}")

        if attempt < retry_times:
            print(f"[INFO] 等待 {retry_delay} 秒后重试...")

    print(f"[ERROR] ❌ 飞书推送失败，已重试 {retry_times} 次")
    return False


def main():
    """主函数"""
    print(f"🥇 黄金监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 加载配置
    config = load_gold_config()
    if not config:
        return False

    settings = config.get("settings", {})

    print(f"[INFO] 监控类型：{config.get('type', 'SHFE_AU2606')}")

    # 获取黄金价格
    print("\n[INFO] 获取黄金价格...")

    gold_data = fetch_gold_price()

    if not gold_data:
        print("[ERROR] 黄金价格获取失败")
        return False

    source = gold_data.get("source", "Unknown")
    print(
        f"  ✅ 现货价：{gold_data['current_cny_g']:.2f} 元/克 (期货：{gold_data.get('futures_cny_g', 0):.2f} 元/克)"
    )
    print(f"  📍 数据源：{source}")

    if gold_data.get("use_spot_price", False):
        print(
            f"  ℹ️  已减去期货升水 {gold_data.get('futures_premium', 3.5):.1f} 元，贴近支付宝/银行价格"
        )

    # 格式化消息
    message = format_gold_message(gold_data, config)

    # 写入文件
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "gold_price.txt"
    output_file.write_text(message, encoding="utf-8")
    print(f"[INFO] 消息已写入：{output_file}")

    # 飞书推送
    if FEISHU_CONFIG.get("enabled"):
        print("[INFO] 发送飞书消息...")
        send_feishu_message(message)

    print("\n✅ 黄金监控完成！")
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
