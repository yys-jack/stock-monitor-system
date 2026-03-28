#!/usr/bin/env python3
"""
股票预测推送脚本
生成预测报告并推送到飞书
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import requests

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "feishu_config.json"
STOCK_CONFIG = PROJECT_ROOT / "config" / "stocks_config.json"


def load_feishu_config() -> dict:
    """加载飞书配置文件"""
    if not CONFIG_FILE.exists():
        return {
            "enabled": False,
            "user_id": "",
            "app_id": "",
            "app_secret": "",
            "retry_times": 3,
            "retry_delay": 2,
        }

    with open(CONFIG_FILE, encoding="utf-8") as f:
        config = json.load(f)
        return config.get("feishu", {})


def load_stock_config() -> list:
    """加载股票配置列表"""
    if not STOCK_CONFIG.exists():
        return [{"code": "000063", "name": "中兴通讯", "enabled": True}]

    with open(STOCK_CONFIG, encoding="utf-8") as f:
        config = json.load(f)
        stocks = config.get("stocks", [])
        # 只返回启用的股票
        return [s for s in stocks if s.get("enabled", True)]


# 加载配置
FEISHU_CONFIG = load_feishu_config()
ENABLED_STOCKS = load_stock_config()

# 配置
CONFIG = {
    "stocks": ENABLED_STOCKS,
    # 飞书配置
    "feishu": FEISHU_CONFIG,
    # 推送时间（每个交易日 15:30 推送，收盘后）
    "push_time": "15:30",
}


def fetch_stock_price_tencent(code: str) -> Optional[Dict]:
    """从腾讯财经获取股票实时数据（备用数据源）"""
    try:
        # 确定市场前缀
        if code.startswith("6"):
            market = "sh"
        else:
            market = "sz"

        url = f"https://qt.gtimg.cn/q={market}{code}"
        headers = {"User-Agent": "Mozilla/5.0"}

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
        print(f"[WARN] 腾讯数据源获取失败：{e}")
        return None


def generate_prediction_report(stock_code: str) -> dict:
    """生成预测报告（带备用数据源）"""
    # 使用 StockPredictor 的 predict 方法（会保存历史记录）
    try:
        from src.predictor import StockPredictor

        predictor = StockPredictor(stock_code)

        # 获取预测结果（会自动保存到历史记录）
        prediction_result = predictor.predict()

        # 获取当前股价
        price_data = fetch_stock_price_tencent(stock_code)
        if not price_data:
            return {"success": False, "error": "获取股价失败", "data": {}}

        return {
            "success": True,
            "data": {
                "stock_code": stock_code,
                "stock_name": predictor.stock_name,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "current_price": price_data["current"],
                "change_pct": price_data["change_pct"],
                "volume": price_data.get("volume", 0),
                # 预测结果
                "signal": prediction_result.get("signal", "观望"),
                "trend": prediction_result.get("trend", "震荡"),
                "confidence": prediction_result.get("confidence", 0),
                "predicted_change": prediction_result.get("change_pct", 0),
                "support_level": prediction_result.get("support", 0),
                "pressure_level": prediction_result.get("resistance", 0),
                # 历史准确率
                "historical_accuracy": prediction_result.get("historical_accuracy", 0),
            },
            "source": "akshare",
        }
    except Exception as e:
        print(f"[WARN] akshare 数据源失败：{e}")

    # 备用方案：使用腾讯数据源生成简化报告
    print("[INFO] 使用备用数据源（腾讯财经）生成简化报告...")
    tencent_data = fetch_stock_price_tencent(stock_code)

    if tencent_data:
        # 基于当前价格和简单规则生成预测
        current = tencent_data["current"]
        change_pct = tencent_data["change_pct"]

        # 简单趋势判断
        if change_pct > 3:
            signal = "买入"
            trend = "强势上涨"
            confidence = 65
        elif change_pct > 1:
            signal = "观望"
            trend = "温和上涨"
            confidence = 50
        elif change_pct < -3:
            signal = "卖出"
            trend = "强势下跌"
            confidence = 65
        elif change_pct < -1:
            signal = "观望"
            trend = "温和下跌"
            confidence = 50
        else:
            signal = "观望"
            trend = "震荡"
            confidence = 45

        # 估算支撑/压力位
        support = current * 0.97
        pressure = current * 1.03

        return {
            "success": True,
            "data": {
                "stock_code": stock_code,
                "stock_name": tencent_data["name"],
                "date": datetime.now().strftime("%Y-%m-%d"),
                "current_price": current,
                "change_pct": change_pct,
                "volume": tencent_data["volume"],
                # 技术指标（简化版）
                "ma5": current,
                "ma10": current,
                "ma20": current,
                "macd": 0,
                "rsi": 50,
                "kdj_k": 50,
                "kdj_d": 50,
                # 预测结果
                "signal": signal,
                "trend": trend,
                "confidence": confidence,
                "predicted_change": change_pct * 0.5,
                "support_level": support,
                "pressure_level": pressure,
            },
            "source": "tencent",
        }

    return {"success": False, "error": "所有数据源均不可用"}


def format_prediction_message(report: dict) -> str:
    """格式化预测消息"""
    data = report["data"]
    source = report.get("source", "akshare")

    # 信号图标
    signal = data["signal"]
    if signal == "买入":
        signal_icon = "🟢"
    elif signal == "卖出":
        signal_icon = "🔴"
    else:
        signal_icon = "🟡"

    # 置信度
    confidence = data["confidence"]
    if confidence > 70:
        confidence_level = "高"
    elif confidence > 50:
        confidence_level = "中"
    else:
        confidence_level = "低"

    # 数据源标识
    source_tag = "🔄 简化版" if source == "tencent" else ""

    # 历史准确率
    historical_accuracy = data.get("historical_accuracy", 0)
    history_tag = f"\n📈 历史准确率：{historical_accuracy:.1f}%" if historical_accuracy > 0 else ""

    message = f"""{signal_icon}【{data['stock_name']} 预测报告】{source_tag}
📅 日期：{data['date']}

💹 当前股价
  收盘价：¥{data['current_price']:.2f}
  涨跌幅：{data['change_pct']:+.2f}%
  成交量：{data['volume']/10000:.1f}万手

🔮 趋势预测
  信号：{signal_icon} {signal}
  趋势：{data['trend']}
  置信度：{confidence_level} ({confidence:.1f}%){history_tag}
  预计涨跌：{data['predicted_change']:+.2f}%

📈 关键价位
  支撑位：¥{data['support_level']:.2f}
  压力位：¥{data['pressure_level']:.2f}

---
🤖 AI 预测 | 历史数据参考 | 仅供参考，不构成投资建议"""

    return message


def send_feishu_message(message: str) -> bool:
    """发送飞书消息"""
    config = CONFIG["feishu"]

    if not config.get("enabled"):
        print("[INFO] 飞书推送未启用")
        return False

    retry_times = config.get("retry_times", 3)
    retry_delay = config.get("retry_delay", 2)

    for attempt in range(1, retry_times + 1):
        try:
            if attempt > 1:
                print(f"[INFO] 重试推送 (第 {attempt}/{retry_times} 次)...")
                import time

                time.sleep(retry_delay)

            # 获取 token
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = {"app_id": config["app_id"], "app_secret": config["app_secret"]}
            token_resp = requests.post(token_url, json=token_data, timeout=10)
            if token_resp.status_code != 200:
                continue

            token_result = token_resp.json()
            if token_result.get("code") != 0:
                continue

            tenant_token = token_result.get("tenant_access_token")

            # 发送消息
            msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
            headers = {
                "Authorization": f"Bearer {tenant_token}",
                "Content-Type": "application/json",
            }
            msg_data = {
                "receive_id": config["user_id"],
                "msg_type": "text",
                "content": json.dumps({"text": message}),
            }

            msg_resp = requests.post(msg_url, headers=headers, json=msg_data, timeout=10)
            if msg_resp.status_code == 200:
                result = msg_resp.json()
                if result.get("code") == 0:
                    print("[INFO] ✅ 飞书推送成功！")
                    return True

            print(
                f"[WARN] 飞书发送失败：{msg_resp.json() if msg_resp.text else msg_resp.status_code}"
            )

        except Exception as e:
            print(f"[ERROR] 飞书推送异常 (第 {attempt} 次): {e}")

        if attempt < retry_times:
            print(f"[INFO] 等待 {retry_delay} 秒后重试...")

    print(f"[ERROR] ❌ 飞书推送失败，已重试 {retry_times} 次")
    return False


def main():
    """主函数 - 为所有启用的股票生成预测并推送汇总"""
    print(f"🔮 股票预测推送 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    stocks = CONFIG.get("stocks", [])
    print(f"[INFO] 启用股票数量：{len(stocks)}")

    if not stocks:
        print("[ERROR] 没有启用的股票")
        return False

    all_reports = []

    # 为每只股票生成预测报告
    for stock in stocks:
        stock_code = stock.get("code", "")
        stock_name = stock.get("name", "")

        print(f"\n[INFO] 生成 {stock_name}({stock_code}) 预测报告...")

        report = generate_prediction_report(stock_code)

        if not report["success"]:
            print(f"[WARN] {stock_name} 生成预测失败：{report['error']}")
            continue

        data = report["data"]
        source = report.get("source", "akshare")
        print(f"[INFO] 数据源：{source}")
        print(f"[INFO] 当前股价：¥{data['current_price']:.2f} ({data['change_pct']:+.2f}%)")
        print(f"[INFO] 预测信号：{data['signal']} (置信度：{data['confidence']:.1f}%)")

        # 写入单个文件
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"prediction_{stock_code}.txt"
        message = format_prediction_message(report)
        output_file.write_text(message, encoding="utf-8")
        print(f"[INFO] 报告已写入：{output_file}")

        all_reports.append({"stock": stock, "report": report, "message": message})

    if not all_reports:
        print("[ERROR] 所有股票预测生成失败")
        return False

    # 生成汇总消息并推送
    print("\n[INFO] 生成汇总推送消息...")
    summary_message = format_summary_message(all_reports)
    print(summary_message)

    # 发送飞书汇总消息
    if CONFIG["feishu"].get("enabled"):
        print("\n[INFO] 发送飞书汇总消息...")
        success = send_feishu_message(summary_message)
        return success

    return True


def format_summary_message(all_reports: list) -> str:
    """格式化汇总消息"""
    today = datetime.now().strftime("%Y-%m-%d")
    message = f"🔮 **股票预测汇总** - {today}\n\n"

    for item in all_reports:
        stock = item["stock"]
        report = item["report"]
        data = report["data"]

        signal_emoji = (
            "🟢" if data["signal"] == "买入" else ("🔴" if data["signal"] == "卖出" else "🟡")
        )
        trend_emoji = (
            "📈" if data["trend"] == "上涨" else ("📉" if data["trend"] == "下跌" else "➡️")
        )

        message += f"**{stock['name']} ({stock['code']})**\n"
        message += f"{signal_emoji} 信号：{data['signal']}\n"
        message += f"{trend_emoji} 趋势：{data['trend']}\n"
        message += f"🎯 置信度：{data['confidence']:.1f}%\n"
        message += (
            f"💰 支撑位：¥{data['support_level']:.2f} | 压力位：¥{data['pressure_level']:.2f}\n\n"
        )

    message += "---\n⚠️ 预测仅供参考，不构成投资建议\n📊 数据源：akshare + 技术分析"

    return message


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
