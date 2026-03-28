"""
飞书推送服务

封装飞书通知功能
"""

from typing import Any, Dict, List, Optional

import requests

from src.config_loader import config_loader


class FeishuService:
    """飞书推送服务类"""

    def __init__(self):
        self.config = config_loader.load_feishu_config()
        self.enabled = self.config is not None and self.config.get("enabled", False)
        self.webhook_url = self.config.get("webhook_url", "") if self.config else ""

    def send_text(self, content: str, mentioned_all: bool = False) -> bool:
        """
        发送文本消息

        Args:
            content: 消息内容
            mentioned_all: 是否@所有人

        Returns:
            是否发送成功
        """
        if not self.enabled or not self.webhook_url:
            print("[WARN] 飞书推送未启用或配置缺失")
            return False

        try:
            data = {"msg_type": "text", "content": {"text": content}}

            if mentioned_all:
                data["at"] = {"at_all": True}

            response = requests.post(self.webhook_url, json=data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get("StatusCode") == 0 or result.get("code") == 0:
                    return True

            print(f"[ERROR] 飞书推送失败：{response.text}")
            return False

        except Exception as e:
            print(f"[ERROR] 飞书推送异常：{e}")
            return False

    def send_post(
        self,
        title: str,
        content: List[List[Dict[str, Any]]],
        mentioned_all: bool = False,
    ) -> bool:
        """
        发送 POST 消息（富文本）

        Args:
            title: 消息标题
            content: 消息内容（富文本格式）
            mentioned_all: 是否@所有人

        Returns:
            是否发送成功
        """
        if not self.enabled or not self.webhook_url:
            print("[WARN] 飞书推送未启用或配置缺失")
            return False

        try:
            data = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {"title": title, "content": content},
                    }
                },
            }

            if mentioned_all:
                data["at"] = {"at_all": True}

            response = requests.post(self.webhook_url, json=data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get("StatusCode") == 0 or result.get("code") == 0:
                    return True

            print(f"[ERROR] 飞书推送失败：{response.text}")
            return False

        except Exception as e:
            print(f"[ERROR] 飞书推送异常：{e}")
            return False

    def send_stock_alert(
        self,
        stock_code: str,
        stock_name: str,
        current_price: float,
        change_pct: float,
        signal: str,
    ) -> bool:
        """
        发送股票预警消息

        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            current_price: 当前价格
            change_pct: 涨跌幅
            signal: 信号

        Returns:
            是否发送成功
        """
        title = f"📊 股票预警 - {stock_name}"

        change_symbol = "📈" if change_pct > 0 else "📉" if change_pct < 0 else "➖"
        signal_emoji = (
            "🟢" if "买入" in signal else "🔴" if "卖出" in signal else "🟡"
        )

        content = [
            [
                {"tag": "text", "text": f"代码：{stock_code}\n"},
                {"tag": "text", "text": f"价格：{current_price:.2f}\n"},
                {"tag": "text", "text": f"{change_symbol} 涨跌幅：{change_pct:+.2f}%\n"},
                {"tag": "text", "text": f"{signal_emoji} 信号：{signal}\n"},
                {"tag": "text", "text": "\n仅供参考，投资需谨慎"},
            ]
        ]

        return self.send_post(title, content)


# 全局实例
feishu_service = FeishuService()
